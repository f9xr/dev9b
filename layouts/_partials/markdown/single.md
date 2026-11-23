{{- $desc := partial "data/description" . -}}
{{- $keywords := partial "data/keywords" . -}}
{{- $cover := "" -}}
{{- with .Params.image -}}
    {{- $cover = . -}}
    {{- with $.Resources.Get . -}}{{- $cover = .Permalink -}}{{- end -}}
{{- end -}}
{{- $source := "" -}}
{{- with .File -}}
    {{- $source = printf "https://raw.githubusercontent.com/f9xr/dev9b/master/content/%s" (replace .Path "\\" "/") -}}
{{- end -}}
{{- $fm := dict
    "title" .Title
    "description" $desc
    "url" .Permalink
    "markdown_url" (printf "%sindex.md" .Permalink)
    "source_url" $source
    "date" (.Date.Format "2006-01-02")
    "lastmod" (.Lastmod.Format "2006-01-02")
    "author" (.Params.author | default "F9XR Team")
    "section" .Section
    "tags" (.Params.tags | default slice)
    "categories" (.Params.categories | default slice)
    "keywords" $keywords
    "image" $cover
    "faq" (.Params.faq | default slice)
    "wordCount" .WordCount
    "readingTime" .ReadingTime
    "license" "CC BY-NC-SA 4.0"
    "generator" "Hugo" -}}
{{- $fmJSON := $fm | jsonify -}}
{{- $fmJSON = replaceRE `\]\(/([^/"#?)])` (printf "](%s$1" site.BaseURL) $fmJSON -}}
{{- $fmJSON = replaceRE `\]\(/\)` (printf "](%s)" site.BaseURL) $fmJSON -}}
---
{{ $fmJSON }}
---

# {{ .Title }}

> {{ $desc }}

{{ partial "markdown/body.md" . }}
