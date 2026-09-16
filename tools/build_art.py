#!/usr/bin/env python3
"""Rebuild the README's local SVG design assets. Python 3.10+; standard library only.

These are editorial diagrams, not screenshots or benchmark results.
Run from any working directory: python tools/build_art.py
"""
from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'casebook'
OUT.mkdir(parents=True, exist_ok=True)
BG = '#0d1117'
PANEL = '#10171f'
EDGE = '#303b47'
INK = '#e6edf3'
MUTED = '#9aa8b7'
ACCENT = '#e38b5b'
DIM = '#576575'
MONO = "'DejaVu Sans Mono',Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif"

def text(x,y,s,size=18,fill=INK,weight='400',family=MONO,spacing=None):
    more = f' letter-spacing="{spacing}"' if spacing is not None else ''
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" font-family="{family}"{more}>{escape(s)}</text>'

def line(x1,y1,x2,y2,color=EDGE,width=1,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d}/>'

def rect(x,y,w,h,fill=PANEL,stroke=EDGE,rx=5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

def circle(x,y,r=5,fill=ACCENT,stroke=None):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'

def write(name,w,h,body,title,desc=''):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc or title)}</desc>
{body}
</svg>'''
    (OUT/name).write_text(svg,encoding='utf-8')

def panel(w,h,label,kind='SOURCE WALKTHROUGH'):
    return rect(.5,.5,w-1,h-1,BG)+text(22,30,label,13,MUTED)+text(w-22,30,'',13)+line(22,46,w-22,46)

def header(mobile=False):
    w,h=(480,254) if mobile else (960,250)
    b=f'<rect width="{w}" height="{h}" fill="{BG}"/>'
    b+=text(0,25,'SOFTWARE ENGINEER',13,MUTED,spacing=2)
    if not mobile:
        b+=text(960,25,'',13)
        b+=text(778,25,'KLAZAPP / SG',13,MUTED)
    b+=text(0,137,'KLAUS',91 if mobile else 104,INK,'700',spacing=3)
    b+=text(328 if mobile else 377,137,'/',91 if mobile else 104,ACCENT,'400')
    if mobile:
        b+=text(0,191,'Systems. Developer tools.',20,INK,family=SANS)
        b+=text(0,222,'And things I make for myself.',20,INK,family=SANS)
    else:
        b+=text(0,197,'Systems. Developer tools. And things I make for myself.',22,INK,family=SANS)
        # A quiet orthogonal detail, not a decorative dashboard.
        b+=line(822,105,926,105,DIM)+line(926,105,926,168,DIM)
        b+=circle(822,105,4,INK)+circle(926,168,4,ACCENT)
        b+=text(800,204,'CODE INSIDE',12,MUTED,spacing=1.4)
    b+=line(0,h-1,w,h-1)
    write('hero-mobile.svg' if mobile else 'hero.svg',w,h,b,'Klaus — software engineer','Systems. Developer tools. And things I make for myself.')

header();header(True)
for label,name in [('Runtime','runtime'),('Tooling','tooling'),('UI','ui'),('Products','products'),('All repos','repos')]:
    b=rect(.5,.5,139,43,BG,EDGE,4)+text(13,28,label,15,INK)+text(117,28,'→',17,ACCENT)
    write(f'nav-{name}.svg',140,44,b,label+' — follow link')

# The K motif from the approved concept: two crisp strokes and one copper dot.
for name,size,bg in [('logo.svg',256,True),('logo-mark.svg',256,False)]:
    b=(f'<rect width="256" height="256" fill="{BG}" rx="128"/>' if bg else '')
    b+=f'<path d="M79 70V176L181 73" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter"/>'
    b+=f'<path d="M133 143L159 169" fill="none" stroke="{MUTED}" stroke-width="11"/>'
    b+=circle(177,189,8,ACCENT)
    write(name,size,size,b,'Klaus — K monogram')

# Pathfinding. Schematic states, not an invented Unity screen capture.
def tiny_graph(x,y,mode):
    pts=[(0,26),(38,0),(38,52),(83,26),(128,26),(166,0),(166,52)]
    edges=[(0,1),(0,2),(1,3),(2,3),(3,4),(4,5),(4,6)]
    b=''
    for a,c in edges:
        p,q=pts[a],pts[c]
        b+=line(x+p[0],y+p[1],x+q[0],y+q[1],DIM,1.6)
    for a,c in [(0,1),(1,3),(3,4),(4,6)]:
        if mode=='closed' and (a,c)==(3,4):
            continue
        p,q=pts[a],pts[c]
        b+=line(x+p[0],y+p[1],x+q[0],y+q[1],ACCENT if mode!='closed' else DIM,2.6)
    if mode=='closed':
        b+=line(x+91,y+16,x+114,y+36,ACCENT,2.5)+line(x+91,y+36,x+114,y+16,ACCENT,2.5)
    for i,(px,py) in enumerate(pts):
        b+=circle(x+px,y+py,4.5,ACCENT if mode!='closed' and i in [0,1,3,4,6] else INK)
    return b

def graph_art(mobile=False):
    w,h=(480,410) if mobile else (960,252)
    b=panel(w,h,'01 / TOPOLOGY CHANGES')
    if mobile:
        b+=tiny_graph(42,82,'open')+tiny_graph(270,82,'closed')
        b+=text(42,172,'route found',14,INK)+text(269,172,'no route',14,ACCENT)
        b+=line(22,194,458,194)
        y=231;x=24
    else:
        b+=tiny_graph(36,87,'open')+tiny_graph(274,87,'closed')
        b+=text(36,173,'route found',15,INK)+text(274,173,'no route',15,ACCENT)
        b+=text(36,217,'Keep the destination. Replan on change.',16,MUTED)
        b+=line(492,63,492,224)
        x=520;y=89
    for i,(s,c) in enumerate([
        ('TopologyChangedCallback()',INK),
        ('{',MUTED),
        ('    if (destinationNode == null)',INK),
        ('        return;',MUTED),
        ('    RequestRoute();',ACCENT),
        ('}',MUTED),
    ]):
        b+=text(x,y+23*i,s,15 if not mobile else 17,c)
    write('route-mobile.svg' if mobile else 'route.svg',w,h,b,'A topology change triggers a new route request','Left: conceptual connectivity states, not screenshots. Right: excerpt from PlayerController.TopologyChangedCallback.')
graph_art();graph_art(True)

# Package report is the repository's documented JSON example, not live output.
def scan_art(mobile=False):
    w,h=(480,340) if mobile else (960,252)
    b=panel(w,h,'02 / DEPENDENCY POLICY')
    if not mobile:
        x=24;y=85
        for i,(s,c) in enumerate([
          ('policy',INK),('  package + exact version',MUTED),('         ↓',ACCENT),('resolved dependency tree',INK),('         ↓',ACCENT),('found / different / absent',INK)]):
            b+=text(x,y+25*i,s,17,c)
        b+=line(395,63,395,225);x=421;y=87
    else:
        x=24;y=86
    for i,(s,c) in enumerate([
       ('"found": [{',INK),
       ('  "package": "koa2-swagger-ui",',MUTED),
       ('  "version": "5.11.2",',ACCENT),
       ('  "path": "root > koa2-swagger-ui@5.11.2"',MUTED),
       ('}]',INK),
    ]):
        b+=text(x,y+i*25,s,17 if not mobile else (12.5 if i==3 else 16),c)
    b+=text(x,225 if not mobile else 273,'Documented example · not a live scan',14,MUTED,family=SANS)
    if mobile:
        b+=text(x,307,'Policy → dependency tree → report',16,INK,family=SANS)
    write('scan-mobile.svg' if mobile else 'scan.svg',w,h,b,'Package Scan — documented JSON report example','Excerpt from repository documentation. The package version is an example, not a claim about current vulnerability status.')
scan_art();scan_art(True)

# Culling mechanism. No invented FPS, vertex counts or comparative performance.
def rendering_art(mobile=False):
    w,h=(480,402) if mobile else (960,252)
    b=panel(w,h,'03 / DRAW SUBMISSION')
    x0=34;y0=80
    b+=rect(x0+74,y0-14,136,133,'#151d26',ACCENT,0)
    for row in range(4):
        for col in range(9):
            x=x0+col*31;y=y0+row*30
            visible=3<=col<=6
            b+=rect(x,y,13,13,INK if visible else '#24303d',INK if visible else '#364354',0)
    b+=text(x0,225 if not mobile else 229,'Frustum illustration · not a benchmark',13,MUTED,family=SANS)
    if mobile:
        b+=line(22,251,458,251);x=24;y=283
    else:
        b+=line(375,63,375,227);x=406;y=86
    for i,(s,c) in enumerate([
      ('Custom culling',ACCENT),
      ('Jobified transform updates',INK),
      ('DrawMeshInstanced',INK),
      ('Per-instance material properties',MUTED),
    ]):
        b+=text(x,y+31*i,s,17 if mobile else 20,c)
    write('render-mobile.svg' if mobile else 'render.svg',w,h,b,'Instanced rendering — visibility and work','Conceptual frustum illustration. The project combines custom culling, jobified transform updates and instanced drawing. No performance measurements are shown.')
rendering_art();rendering_art(True)

# Layout: reproduce the shape of the README's 4-column custom-layout example.
def bento_art(mobile=False):
    w,h=(480,432) if mobile else (960,252)
    b=panel(w,h,'04 / LAYOUT AS DATA')
    boxes=[(30,70,188,138,'hero'),(227,70,80,65,'stats1'),(316,70,80,65,'stats2'),(227,143,169,65,'chart')]
    for x,y,bw,bh,label in boxes:
        b+=rect(x,y,bw,bh,'#17212b',ACCENT if label=='hero' else EDGE)
        b+=text(x+12,y+27,label,14,INK)
    if mobile:
        b+=line(22,232,458,232);x=24;y=270
    else:
        b+=line(426,63,426,225);x=454;y=83
    snippets=['layoutBuilder(4)', '  .place("hero", 1, 1, {', '    colSpan: 2, rowSpan: 2', '  })', '  // components stay independent']
    for i,s in enumerate(snippets):
        b+=text(x,y+i*26,s,16 if mobile else 18,ACCENT if i==0 else (MUTED if i==4 else INK))
    write('layout-mobile.svg' if mobile else 'layout.svg',w,h,b,'A four-column layout defined separately from its cards','Illustration based on the repository README custom-layout example. The code excerpt uses its documented layoutBuilder API; not an application screenshot.')
bento_art();bento_art(True)
print(f'Wrote SVG assets to {OUT}')
