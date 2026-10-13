# verify-machine-readable.ps1
# Checks that Dev9b's machine-readable / agent-discovery surface is present and consistent.
# Run after `hugo --gc --minify --cleanDestinationDir` from the repo root:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify-machine-readable.ps1
param(
    [string]$PublicDir = "public",
    [string]$ContentDir = "content/post",
    [switch]$Build
)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repo

$fail = 0
function Ok([string]$m)   { Write-Output ("PASS`t" + $m) }
function Bad([string]$m)  { Write-Output ("FAIL`t" + $m); $script:fail++ }
function Warn([string]$m) { Write-Output ("WARN`t" + $m) }

if ($Build) {
    Write-Output '--- running hugo build ---'
    hugo --gc --minify --cleanDestinationDir | Out-Null
}

if (-not (Test-Path -LiteralPath $PublicDir)) { Bad "build output not found: $PublicDir (run hugo first)"; Write-Output 'RESULT: FAIL'; exit 1 }

# 1. Required generated files
$required = @(
    'llms.txt', 'llms-full.txt', 'articles-urls.txt', 'feed.json', 'robots.txt', 'sitemap.xml',
    '.well-known/ai-catalog.json', '.well-known/agent-skills/index.json', '.well-known/security.txt'
)
foreach ($f in $required) {
    $p = Join-Path $PublicDir $f
    if (Test-Path -LiteralPath $p) { Ok "present: $f" } else { Bad "missing: $f" }
}

# 2. Every published post must have an index.md alternate
$postDirs = @(Get-ChildItem -LiteralPath (Join-Path $PublicDir 'p') -Directory -ErrorAction SilentlyContinue)
$mdMissing = 0
foreach ($post in $postDirs) {
    if (-not (Test-Path -LiteralPath (Join-Path $post.FullName 'index.html'))) { continue }  # not a rendered post
    if (-not (Test-Path -LiteralPath (Join-Path $post.FullName 'index.md'))) {
        Bad "no markdown alternate for post: $($post.Name)"; $mdMissing++
    }
}
if ($mdMissing -eq 0 -and $postDirs.Count -gt 0) { Ok "all $($postDirs.Count) published posts have index.md" }

# 3. articles-urls.txt count matches published post count
$listFile = Join-Path $PublicDir 'articles-urls.txt'
if (Test-Path -LiteralPath $listFile) {
    $listed = (Get-Content -LiteralPath $listFile | Where-Object { $_ -match '/p/' }).Count
    if ($listed -eq $postDirs.Count) { Ok "articles-urls.txt lists $listed posts (matches build output)" }
    else { Bad "articles-urls.txt lists $listed posts but build output has $($postDirs.Count)" }
}

# 4. JSON parse checks
foreach ($f in @('feed.json', '.well-known/ai-catalog.json', '.well-known/agent-skills/index.json')) {
    $p = Join-Path $PublicDir $f
    if (Test-Path -LiteralPath $p) {
        try { $null = Get-Content -LiteralPath $p -Raw | ConvertFrom-Json; Ok "valid JSON: $f" }
        catch { Bad "invalid JSON: $f -> $($_.Exception.Message)" }
    }
}

# 5. Skill digests must match the published SKILL.md copies
$skillIndex = Join-Path $PublicDir '.well-known/agent-skills/index.json'
if (Test-Path -LiteralPath $skillIndex) {
    $idx = Get-Content -LiteralPath $skillIndex -Raw | ConvertFrom-Json
    foreach ($skill in $idx.skills) {
        $urlPath = ([uri]$skill.url).AbsolutePath.TrimStart('/')
        $art = Join-Path $PublicDir ($urlPath -replace '/', '\')
        if (-not (Test-Path -LiteralPath $art)) { Bad "skill artifact missing: $urlPath"; continue }
        $actual = 'sha256:' + (Get-FileHash -LiteralPath $art -Algorithm SHA256).Hash.ToLower()
        if ($actual -eq $skill.digest) { Ok "skill digest matches: $($skill.name)" }
        else { Bad "skill digest mismatch: $($skill.name) (index=$($skill.digest) actual=$actual)" }
    }
}

# 6. No stale hand-maintained duplicates in static/
foreach ($f in @('llms.txt', 'llms-full.txt', 'articles-urls.txt', 'robots.txt')) {
    $s = Join-Path 'static' $f
    if (Test-Path -LiteralPath $s) { Bad "stale static file (should be generated): static/$f" }
}
if (-not (Test-Path -LiteralPath (Join-Path 'static' 'llms.txt')) -and
    -not (Test-Path -LiteralPath (Join-Path 'static' 'robots.txt'))) {
    Ok 'no stale hand-maintained llms/robots files in static/'
}

Write-Output '---'
if ($fail -gt 0) { Write-Output "RESULT: FAIL ($fail)"; exit 1 }
Write-Output 'RESULT: PASS'
