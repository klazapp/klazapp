#!/usr/bin/env python3
"""Build a local GitHub-style preview from README.md (not a second source of copy).

Optional tooling only: pip install markdown-it-py
The live README does not use this stylesheet or any JavaScript.
"""
from pathlib import Path
from html import escape
import re, base64
from markdown_it import MarkdownIt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'preview'
(OUT/'notes').mkdir(parents=True,exist_ok=True)
MD=MarkdownIt('commonmark', {'html': True}).enable('table')

CSS=r'''
:root{color-scheme:dark;--bg:#0d1117;--panel:#161b22;--ink:#e6edf3;--muted:#919eac;--border:#30363d;--link:#58a6ff;--orange:#e38b5b}
*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;font-size:16px;line-height:1.5}a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible,summary:focus-visible{outline:2px solid var(--orange);outline-offset:4px}img{max-width:100%;vertical-align:middle}picture{display:block}.page{max-width:1344px;margin:32px auto 64px;padding:0 32px;display:grid;grid-template-columns:238px minmax(0,1fr);gap:32px;align-items:start}.sidebar{padding-top:6px}.avatar{width:224px;height:224px;border-radius:50%;border:1px solid var(--border)}.name{font-size:28px;font-weight:650;line-height:1.2;margin:22px 0 1px}.handle{font-size:18px;color:var(--muted);margin:0 0 22px}.bio{font-size:16px;line-height:1.6;margin-bottom:24px}.contact{font-size:14px;margin:12px 0;overflow-wrap:anywhere}.contact a{color:var(--ink)}.contact .icon{color:var(--muted);display:inline-block;width:24px}.sidebar-foot{border-top:1px solid var(--border);margin-top:26px;padding-top:16px;color:var(--muted);font:12px/1.7 ui-monospace,SFMono-Regular,Consolas,monospace}.readme-shell{border:1px solid var(--border);border-radius:6px;min-width:0;background:var(--bg)}.repo-label{padding:20px 30px 4px;color:var(--muted);font:12px/1.5 ui-monospace,SFMono-Regular,Consolas,monospace}.repo-label strong{color:var(--ink);font-weight:600}.markdown-body{min-width:0;padding:28px 30px 22px;line-height:1.5;overflow-wrap:break-word}.markdown-body>:first-child{margin-top:0}.markdown-body p{margin:0 0 16px}.markdown-body h1,.markdown-body h2{padding-bottom:.3em;border-bottom:1px solid var(--border)}.markdown-body h1{font-size:2em}.markdown-body h2{font-size:24px;margin:30px 0 16px;font-weight:600}.markdown-body h3{font-size:20px;margin:25px 0 10px;font-weight:600}.markdown-body h3 code{font-size:.82em}.markdown-body hr{height:1px;padding:0;margin:29px 0;background:var(--border);border:0}.markdown-body details{margin:12px 0 18px}.markdown-body summary{cursor:pointer;display:list-item;list-style-position:inside;line-height:1.5}.markdown-body details[open]>summary{margin-bottom:18px}.markdown-body details p{margin-top:0}.markdown-body summary strong{font-weight:550}.markdown-body sub{font-size:12px;color:var(--muted)}.markdown-body code{padding:.16em .34em;margin:0;font-size:85%;background:rgba(110,118,129,.2);border-radius:5px;font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}.markdown-body pre{overflow:auto;padding:16px;font-size:13px;line-height:1.55;background:var(--panel);border-radius:6px;margin:16px 0}.markdown-body pre code{padding:0;background:transparent;border:0;border-radius:0;font-size:100%;white-space:pre}.markdown-body img{background:var(--bg)}.markdown-body blockquote{padding:0 1em;color:var(--muted);border-left:.25em solid var(--border)}.markdown-body table{border-collapse:collapse;width:100%}.markdown-body th,.markdown-body td{border:1px solid var(--border);padding:6px 13px}.markdown-body a[name]{display:block;scroll-margin-top:20px}.preview-label{max-width:1344px;margin:0 auto;padding:0 32px 20px;font:12px/1.6 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--muted)}.note-shell{max-width:980px;margin:36px auto;padding:0 20px}.note-shell .markdown-body{border:1px solid var(--border);border-radius:6px}.note-shell h1{font-size:28px}
@media(max-width:767px){.page{padding:0 14px;display:block;margin:20px 0 28px}.sidebar{display:grid;grid-template-columns:78px minmax(0,1fr);gap:0 16px;margin-bottom:22px;align-items:center}.avatar{width:78px;height:78px;grid-column:1;grid-row:1/3}.name{grid-column:2;margin:0;font-size:25px}.handle{grid-column:2;margin:0;font-size:15px}.bio{grid-column:1/-1;font-size:14px;margin:16px 0 10px}.contact,.sidebar-foot{display:none}.repo-label{padding:17px 18px 0;font-size:11px}.markdown-body{padding:22px 18px 18px;font-size:15px}.markdown-body h2{font-size:22px}.markdown-body h3{font-size:18px}.markdown-body pre{font-size:12px;padding:12px}.markdown-body summary{font-size:14px}.markdown-body sub{font-size:11px}.preview-label{padding:0 18px 20px}.note-shell{margin:16px auto;padding:0 14px}.note-shell .markdown-body{padding:20px}.note-shell h1{font-size:24px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''

def embed(local):
    p=ROOT/local
    mime='image/svg+xml' if p.suffix=='.svg' else 'image/png'
    return f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode()

def render(md, is_note=False):
    html=MD.render(md)
    # GitHub-style heading IDs, including duplicate suffixes.
    seen={}
    def heading(m):
        level,inner=m.groups()
        raw=re.sub('<[^>]*>','',inner).lower()
        slug=re.sub(r'[^\w\- ]','',raw).strip().replace(' ','-')
        n=seen.get(slug,0);seen[slug]=n+1
        return f'<h{level} id="{slug}{"-"+str(n) if n else ""}">{inner}</h{level}>'
    html=re.sub(r'<h([1-6])>(.*?)</h\1>',heading,html)
    html=re.sub(r'(src|srcset)="(assets/casebook/[^"]+)"',lambda m:f'{m[1]}="{embed(m[2])}"',html)
    if is_note:
        html=html.replace('href="../README.md','href="../index.html')
        # Other local markdown notes (index).
        html=re.sub(r'href="((?:0[1-4]-[^"#]+|README)\.md)(#[^"]*)?"', lambda m:'href="'+m[1][:-3]+'.html'+(m[2] or '')+'"',html)
    else:
        html=re.sub(r'href="notes/([^"#]+)\.md(#[^"]*)?"',lambda m:'href="notes/'+m[1]+'.html'+(m[2] or '')+'"',html)
        html=html.replace('href="tools/', 'href="../tools/')
    return html

def shell(body,title):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>'

html=render((ROOT/'README.md').read_text())
avatar=embed('assets/casebook/logo.svg')
sidebar=f'''<aside class="sidebar" aria-label="Profile preview"><img class="avatar" src="{avatar}" alt="Klaus K monogram"><div class="name">Klaus</div><div class="handle">klazapp</div><p class="bio">Software engineer. 11 years building production systems, developer tools, real-time runtimes and my own mobile products. Singapore.</p><div class="contact"><span class="icon">⌖</span>Singapore</div><div class="contact"><span class="icon">✉</span><a href="mailto:klazapp@klazapp.com">klazapp@klazapp.com</a></div><div class="contact"><span class="icon">↗</span><a href="https://www.linkedin.com/in/klaus-vinn/">LinkedIn</a></div><div class="contact"><span class="icon">↗</span><a href="https://github.com/klazapp">github.com/klazapp</a></div><div class="sidebar-foot">Systems / tools / products</div></aside>'''
body=f'<main class="page">{sidebar}<div class="readme-shell"><div class="repo-label"><strong>klazapp</strong> / README.md</div><article class="markdown-body">{html}</article></div></main><div class="preview-label">Local preview of the generated README · GitHub controls the surrounding page, native fonts and disclosure styling. The sidebar is an installation preview, not part of README.md.</div>'
(OUT/'index.html').write_text(shell(body,'Klaus — GitHub README preview'))
for p in (ROOT/'notes').glob('*.md'):
    note=render(p.read_text(),True)
    (OUT/'notes'/(p.stem+'.html')).write_text(shell(f'<main class="note-shell"><article class="markdown-body">{note}</article></main>',p.stem+' — Klaus'))
print('Built preview/index.html and local note pages')
