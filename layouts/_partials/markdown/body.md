{{- $raw := .RawContent -}}
{{- $raw = replaceRE `<!--\s*more\s*-->` "" $raw -}}
{{- $raw = replaceRE `<a href="([^"]+)"[^>]*>([^<]+)</a>` "[$2]($1)" $raw -}}
{{- $raw = replaceRE `\{\{<\s*youtube\s+id="([^"]+)"\s*>\}\}` "[Watch on YouTube](https://www.youtube.com/watch?v=$1)" $raw -}}
{{- $raw = replaceRE `\{\{<\s*youtube\s+id=([A-Za-z0-9_-]+)\s*>\}\}` "[Watch on YouTube](https://www.youtube.com/watch?v=$1)" $raw -}}
{{- $raw = replaceRE `\{\{<\s*youtube\s+"([^"]+)"\s*>\}\}` "[Watch on YouTube](https://www.youtube.com/watch?v=$1)" $raw -}}
{{- $raw = replaceRE `\{\{<\s*youtube\s+([A-Za-z0-9_-]+)\s*>\}\}` "[Watch on YouTube](https://www.youtube.com/watch?v=$1)" $raw -}}
{{- $raw = replaceRE `\{\{<\s*bilibili\s+([A-Za-z0-9]+)\s*>\}\}` "[Watch on Bilibili](https://www.bilibili.com/video/$1)" $raw -}}
{{- $base := site.BaseURL -}}
{{- $raw = replaceRE `\]\(/([^/"#?)])` (printf "](%s$1" $base) $raw -}}
{{- $raw = replaceRE `href="/([^/"#?)])` (printf "href=\"%s$1" $base) $raw -}}
{{- $raw = replaceRE `\]\(/\)` (printf "](%s)" $base) $raw -}}
{{- $raw = replaceRE `href="/"` (printf "href=\"%s\"" $base) $raw -}}
{{- $raw -}}
