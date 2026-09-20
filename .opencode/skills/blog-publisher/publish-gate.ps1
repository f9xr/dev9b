# publish-gate.ps1 - Pre-publish quality gate for Dev9b blog posts.
# Usage:  powershell -File publish-gate.ps1 -Slug <post-slug>
# Run for EVERY new post before it is marked draft:false.
# FAIL   = blocking, fix before publish.
# WARN   = advisory, review manually.
# PASS   = checked and OK.
param(
  [Parameter(Mandatory = $true)][string]$Slug
)
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$repo = Split-Path -Parent (Split-Path -Parent $root)   # .../.opencode/skills -> repo root
$file = Join-Path $repo "content\post\$Slug\index.md"
if (-not (Test-Path -LiteralPath $file)) { Write-Error "Post not found: $file"; exit 1 }

$t = [System.IO.File]::ReadAllText($file)
$fmMatch = [regex]::Match($t, '(?s)^---\r?\n(.*?)\r?\n---\r?\n?')
if (-not $fmMatch.Success) { Write-Output 'FAIL front matter: no YAML front matter found'; exit 1 }
$fm = $fmMatch.Groups[1].Value
$body = $t.Substring($fmMatch.Index + $fmMatch.Length)

function Get-Field([string]$key) {
  $x = [regex]::Match($fm, '(?m)^' + [regex]::Escape($key) + ':\s*(.*)$')
  if ($x.Success) { $x.Groups[1].Value.Trim().Trim('"') } else { '' }
}
function Out-R([string]$status, [string]$msg) { Write-Output ("{0}`t{1}" -f $status.ToUpper(), $msg) }

Write-Output ("=== publish-gate: {0} ===" -f $Slug)
$anyFail = $false
function Fail([string]$msg) { Out-R 'FAIL' $msg; $script:anyFail = $true }
function Warn([string]$msg) { Out-R 'WARN' $msg }

# --- 1. Front matter field set (must match site YAML template) ---
foreach ($k in @('title','description','slug','date','image','author','categories','tags','draft','math')) {
  if (-not [regex]::IsMatch($fm, '(?m)^' + [regex]::Escape($k) + ':')) { Fail "front matter missing: $k" }
}
if ([regex]::IsMatch($fm, '(?m)^title:')) {
  $len = (Get-Field 'title').Length
  if ($len -le 0) { Fail 'title is empty' } elseif ($len -gt 60) { Fail "title too long: $len chars (limit 60)" } else { Out-R 'PASS' "title <= 60 chars ($len)" }
}
$desc = Get-Field 'description'
if ($desc -eq '') { Fail 'description missing' } elseif ($desc.Length -gt 160) { Fail "description too long: $($desc.Length) chars (limit 160)" } elseif ($desc.Length -lt 90) { Warn "description short ($($desc.Length) chars): aim ~140-160" } else { Out-R 'PASS' "description length OK ($($desc.Length))" }

# --- 2. Author consistency ---
$author = Get-Field 'author'
if ($author -ne 'F9XR Team') { Fail "author must be 'F9XR Team' unless a real individual is named (got: '$author'). Individuals MUST also set authorUrl + authorGitHub." }
$authUrl = Get-Field 'authorUrl'; $authGit = Get-Field 'authorGitHub'
if ($author -ne 'F9XR Team' -and ($authUrl -eq '' -or $authGit -eq '')) { Fail 'named individual author requires authorUrl AND authorGitHub' }

# --- 3. Tags: max 4, reuse existing slugs ---
$tagSec = [regex]::Match($fm, '(?s)tags:\r?\n(.*?)(?=\r?\n[a-zA-Z])').Groups[1].Value
$tags = @($tagSec -split "`n" | Where-Object { $_ -match '^\s*-\s' } | ForEach-Object { ($_ -replace '^\s*-\s*', '').Trim() })
if ($tags.Count -eq 0) { Fail 'no tags defined' } elseif ($tags.Count -gt 4) { Fail "too many tags: $($tags.Count) (limit 4). Merge near-duplicates, keep only meaningful ones." } else { Out-R 'PASS' "tags = $($tags.Count) (limit 4)" }
$catSec = [regex]::Match($fm, '(?s)categories:\r?\n(.*?)(?=\r?\n[a-zA-Z])').Groups[1].Value
$cats = @($catSec -split "`n" | Where-Object { $_ -match '^\s*-\s' })
if ($cats.Count -ne 1) { Warn "categories: expected exactly 1 (got $($cats.Count))" }

# --- 4. Cover image: local, exists, < 300 KB ---
$img = Get-Field 'image'
if ($img -match '^https?://') { Fail "cover image must be LOCAL to the bundle, not a URL: $img" }
if ($img -ne '') {
  $cover = Join-Path (Split-Path -Parent $file) $img
  if (Test-Path -LiteralPath $cover) {
    $size = (Get-Item -LiteralPath $cover).Length
    if ($size -gt 300KB) { Fail "cover too big: $([math]::Round($size/1KB)) KB (limit 300 KB); resize to 1200px wide, JPEG q80-85" } else { Out-R 'PASS' "cover local, $([math]::Round($size/1KB)) KB" }
  } else { Fail "cover file missing: $cover" }
}

# --- 5. Body bans ---
if ($t -match 'Recommended Reading|Related Links|Further Reading|Related Reading') { Fail 'banned list section found (Recommended Reading / Related Links). Embed all links inline in the body.' }
if ($t -match '\]\(https://f9xr\.org') { Fail 'absolute internal links found. Use relative /p/<slug>/ URLs only.' }
if ($t -match '\]\(https?://[^)]*.f9xr\.org') { Fail 'absolute internal links found (use relative URLs).' }
if ($t -match 'image:\s*https?://') { Fail 'hotlinked cover/inline image URL in front matter. Images must be local files.' }
$generic = [regex]::Matches($t, '\[(here|this|click here|learn more|read more)\]\(', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase).Count
if ($generic -gt 0) { Fail "generic anchor text found ($generic). Use descriptive anchor text." } else { Out-R 'PASS' 'no generic anchors' }
if ($body -notmatch '<!--more-->') { Fail '<!--more--> missing. Add it right after the intro, before the first ## heading.' }
$inCode = $false
$h1InBody = $false
foreach ($line in ($body -split "`n")) {
  if ($line -match '^\s*```') { $inCode = -not $inCode; continue }
  if (-not $inCode -and $line -match '^# ') { $h1InBody = $true; break }
}
if ($h1InBody) { Fail 'H1 (# ) found in body. The theme renders the title as the single H1; start body with ##.' }
$firstHead = [regex]::Match($body, '(?m)^(#{1,3})\s').Groups[1].Value
if ($firstHead -ne '##') { Fail "first heading must be '##' (found '$firstHead'). No H3/H1 first." } else { Out-R 'PASS' 'heading hierarchy OK (starts ##)' }

# --- 6. Word count (welcome/intro pages exempt) ---
$plain = ($body -replace '```.*?```', '' -replace '`[^`]*`', '' -replace '\[.*?\]\(.*?\)', ' ' -replace '\s+', ' ').Trim()
$words = $plain.Split(' ').Count
if ($Slug -eq 'hello-world' -or $Slug -match '(^|-)(welcome|about|intro|hello|index)') {
  Warn "welcome/intro page: word count $words skipped (not a tutorial)."
} elseif ($words -lt 1000) { Fail "thin content: $words words (min 1000, target 1200+)" } elseif ($words -lt 1200) { Warn "on the thin side: $words words (target 1200-2500)" } else { Out-R 'PASS' "word count OK: $words" }

# --- 7. Internal linking: >= 2 relative /p/ links, aim for 3+ ---
$internal = [regex]::Matches($body, '\]\(/p/').Count
if ($internal -lt 2) { Fail "only $internal internal /p/ links (min 2, aim 3+). Weave more related post links inline." } elseif ($internal -lt 3) { Warn "internal links: $internal (aim for 3+). This looks/links fine on a niche topic but prefer 3+. " } else { Out-R 'PASS' "internal links: $internal (>= 3)" }

# --- 8. Images: alt text + local targets ---
$imgs = [regex]::Matches($body, '!\[([^\]]*)\]\(([^)]+)\)')
if ($imgs.Count -gt 0) {
  $noAlt = @($imgs | Where-Object { $_.Groups[1].Value.Trim() -eq '' })
  if ($noAlt.Count -gt 0) { Fail "$($noAlt.Count) image(s) without alt text" } else { Out-R 'PASS' "all $($imgs.Count) images have alt text" }
  $hot = @($imgs | Where-Object { $_.Groups[2].Value -match '^https?://' })
  if ($hot.Count -gt 0) { Fail "hotlinked inline image(s): $($hot.Count). Download them into the page bundle." } else { Out-R 'PASS' 'all inline images local' }
}

# --- 9. Affiliate disclosure ---
$affCount = ([regex]::Matches($t, '(?i)[?&](via|ref|aff|affiliate|partner|subid|clickid)=').Count)
if ($affCount -gt 0 -and $t -notmatch '(?i)affiliate link') { Fail "affiliate/`?via= links present but no disclosure. Add the affiliate-disclosure callout after the intro." }

# --- 10. Required footer links ---
if ($t -notmatch '\]\(/editorial-policy') { Fail '/editorial-policy/ link missing (required closing footer).' }
if ($t -notmatch '\]\(/contribute') { Fail '/contribute/ link missing (required closing footer).' }
if ($t -notmatch '(?m)^faq:|^\[faq|^faq:') { Warn 'no faq front matter. Tutorials should include 3-6 on-page FAQ Q&As + faq: block.' }

# --- 11. Deploy-file sync reminder ---
if ($t -match '^draft:\s*false') {
  Warn 'draft:false - remind user that static/llms.txt, static/articles-urls.txt and deploy.yml IndexNow urlList must include this post.'
}

Write-Output '---'
if ($anyFail) { Write-Output 'RESULT: FAIL - fix the FAIL items above before publishing.'; exit 1 }
Write-Output 'RESULT: PASS (warnings, if any, are advisory)'