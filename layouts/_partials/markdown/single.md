{{- $desc := partial "data/description" . -}}
{{- $fm := dict
    "title" .Title
    "description" $desc
    "url" .Permalink
    "markdown_url" (printf "%sindex.md" .Permalink)
    "date" (.Date.Format "2006-01-02")
    "lastmod" (.Lastmod.Format "2006-01-02")
    "author" (.Params.author | default "F9XR Team")
    "tags" (.Params.tags | default slice)
    "categories" (.Params.categories | default slice)
    "license" "CC BY-NC-SA 4.0"
    "generator" "Hugo" -}}
---
{{ $fm | jsonify }}
---

# {{ .Title }}

> {{ $desc }}

{{ .RawContent }}
