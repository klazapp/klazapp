#!/usr/bin/env python3
"""Validate the profile's local links, named anchors and SVG content. No network."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import re
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
    def __init__(self):
        super().__init__();self.paths=[];self.anchors=set();self.forbidden=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag in {'script','iframe','object','embed','style'}:
            self.forbidden.append(tag)
        if any(k=='style' or k.startswith('on') for k in a):
            self.forbidden.append(f'active/style attribute on {tag}')
        if tag=='a' and a.get('name'):
            self.anchors.add(a['name'])
        for k in ('href','src','srcset'):
            if a.get(k): self.paths.append(a[k])

def check():
    errors=[];checks=0
    for md in [ROOT/'README.md',*(ROOT/'notes').glob('*.md')]:
        s=md.read_text(encoding='utf-8');parser=Tags();parser.feed(s)
        errors.extend(f'{md.name}: {e}' for e in parser.forbidden)
        paths=parser.paths+re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',s)
        for u in paths:
            parsed=urlsplit(u)
            if parsed.scheme or parsed.netloc: continue
            target=(md.parent/unquote(parsed.path)).resolve() if parsed.path else md
            if not target.exists():errors.append(f'{md.name}: missing {u}')
            elif parsed.fragment:
                # Check explicit named anchors; use GitHub headings for other anchors.
                t=target.read_text(encoding='utf-8') if target.suffix=='.md' else ''
                names=set(re.findall(r'<a\s+name="([^"]+)"',t))
                heads=set()
                for heading in re.findall(r'^#{1,6}\s+(.+)$',t,re.M):
                    heads.add(re.sub(r'[^\w\- ]','',heading.lower()).replace(' ','-'))
                if parsed.fragment not in names|heads:
                    errors.append(f'{md.name}: missing anchor {u}')
            checks+=1
    for svg in (ROOT/'assets/casebook').glob('*.svg'):
        try:
            r=ET.parse(svg).getroot()
            for e in r.iter():
                tag=e.tag.rsplit('}',1)[-1]
                if tag in {'script','foreignObject','iframe','image'}:
                    errors.append(f'{svg.name}: unsupported {tag}')
                if any(k.startswith('on') for k in e.attrib):
                    errors.append(f'{svg.name}: event handler')
                for k,v in e.attrib.items():
                    if k.endswith('href') and not v.startswith('#'):
                        errors.append(f'{svg.name}: external reference')
            assert len(r.get('viewBox','').split())==4
        except (ET.ParseError,AssertionError) as e:
            errors.append(f'{svg.name}: invalid SVG {e}')
        checks+=1
    # No font binaries may be bundled.
    for p in ROOT.rglob('*'):
        if p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'}:
            errors.append(f'Unexpected font file: {p}')
    if errors:
        print('\n'.join(errors));return 1
    print(f'PASS: {checks} local references/anchors/SVGs checked; no font files or active README content.')
    return 0
if __name__=='__main__':sys.exit(check())
