"""Generate static English pages from the maintained French source and reviewed copy."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://michelpalmer256-afk.github.io/beaver4x4ai/'
PAGES = ['index.html', 'assistance.html', 'confidentialite.html']
COPY = json.loads((ROOT / 'locales/en.json').read_text())
UNCHANGED = {'BEAVER','4X4AI','4X4 AI','PRÉPARE · EXPLORE · PARTAGE','‹','›','☰','Land Cruiser','Patrol','Defender','Wrangler','IMAC','iMac','APPLE WATCH','Apple Watch','IPHONE DUO','iPhone Duo','·','▲','FR','EN','|','Français','English'}
DESCRIPTIONS = {
 'index.html': ('Beaver4x4 AI : garage numérique, copilote IA, Trails et communauté pour préparer, explorer et partager tes aventures tout-terrain.', 'Discover Beaver4x4 AI: a digital garage, AI copilot, Trails and a community to help you prepare, explore and share your off-road adventures.'),
 'assistance.html': ('Assistance Beaver4x4 AI : informations utiles pour obtenir de l’aide concernant l’application.', 'Beaver4x4 AI support: information on getting help with the app.'),
 'confidentialite.html': ('Informations de confidentialité de Beaver4x4 AI et état de préparation de la politique officielle.', 'Beaver4x4 AI privacy information and the status of the official privacy policy.')
}

def seo(page, lang):
    suffix = '' if page == 'index.html' else page
    fr, en = BASE + suffix, BASE + 'en/' + suffix
    description = DESCRIPTIONS[page][lang == 'en']
    url = en if lang == 'en' else fr
    title = {'index.html':'Beaver4x4 AI — Prépare · Explore · Partage', 'assistance.html':'Assistance — Beaver4x4 AI', 'confidentialite.html':'Confidentialité — Beaver4x4 AI'}[page]
    if lang == 'en': title = COPY[title]
    return f'''<!-- seo:start -->
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="fr" href="{fr}">
<link rel="alternate" hreflang="en" href="{en}">
<link rel="alternate" hreflang="x-default" href="{fr}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{'en_US' if lang == 'en' else 'fr_FR'}">
<meta property="og:locale:alternate" content="{'fr_FR' if lang == 'en' else 'en_US'}">
<!-- seo:end -->'''

def add_seo(source, page, lang):
    source = re.sub(r'<!-- seo:start -->.*?<!-- seo:end -->', '', source, flags=re.S)
    return source.replace('</head>', seo(page, lang) + '</head>', 1)

class English(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.missing, self.raw = [], set(), 0
    def translate(self, value):
        key = value.strip()
        if not key or key in UNCHANGED: return value
        if key not in COPY:
            self.missing.add(key)
            return value
        start = len(value) - len(value.lstrip())
        end = len(value.rstrip())
        return value[:start] + COPY[key] + value[end:]
    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        values = dict(attrs)
        for key, value in attrs:
            if value is None: continue
            translated = value
            if key in ('alt','aria-label','aria-roledescription','title','placeholder'):
                translated = self.translate(value)
            elif tag == 'html' and key == 'lang': translated = 'en'
            elif key in ('src','href') and not value.startswith(('#','http:','https:','mailto:','tel:','data:','/')):
                if value.startswith('assets/') or value.split('?')[0] in ('style.css','quality.css','quality.js','language.css','language.js','script.js','sitemap.xml'):
                    translated = '../' + value
                elif value == 'index.html': translated = './'
            elif key == 'srcset':
                translated = ', '.join('../' + item.strip() if item.strip().startswith('assets/') else item.strip() for item in value.split(','))
            if translated != value:
                raw = re.sub(r'('+re.escape(key)+r'\s*=\s*)([\"\']).*?\2', lambda m: m[1]+m[2]+escape(translated, quote=True)+m[2], raw, count=1)
        if 'data-language' in values:
            raw = re.sub(r'\saria-current="[^"]*"', '', raw)
            if values['data-language'] == 'en': raw = raw[:-1] + ' aria-current="page">'
        self.out.append(raw)
        if tag in ('script','style'): self.raw += 1
    def handle_startendtag(self, tag, attrs): self.handle_starttag(tag, attrs)
    def handle_endtag(self, tag):
        self.out.append('</'+tag+'>')
        if tag in ('script','style'): self.raw -= 1
    def handle_data(self, data):
        self.out.append(data if self.raw else escape(self.translate(data), quote=False))
    def handle_decl(self, decl): self.out.append('<!'+decl+'>')
    def handle_comment(self, data): self.out.append('<!--'+data+'-->')

def build(check=False):
    outputs = []
    for page in PAGES:
        original = (ROOT / page).read_text()
        french = add_seo(original, page, 'fr')
        parser = English(); parser.feed(french)
        if parser.missing: raise ValueError(f'Missing translations in {page}: {sorted(parser.missing)}')
        english = add_seo(''.join(parser.out), page, 'en')
        english = re.sub(r'<(div|p|small)([^>]*)>PRÉPARE · EXPLORE · PARTAGE</\1>', r'<\1\2 lang="fr">PRÉPARE · EXPLORE · PARTAGE</\1>', english)
        outputs += [(ROOT/page, french),(ROOT/'en'/page, english)]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in PAGES:
        suffix = '' if page == 'index.html' else page
        fr, en = BASE + suffix, BASE + 'en/' + suffix
        for url in [fr, en]:
            sitemap.append(f'<url><loc>{url}</loc><xhtml:link rel="alternate" hreflang="fr" href="{fr}"/><xhtml:link rel="alternate" hreflang="en" href="{en}"/><xhtml:link rel="alternate" hreflang="x-default" href="{fr}"/></url>')
    sitemap.append('</urlset>')
    outputs.append((ROOT/'sitemap.xml', '\n'.join(sitemap)+'\n'))
    if check:
        stale = [str(path.relative_to(ROOT)) for path, content in outputs if not path.exists() or path.read_text() != content]
        if stale: raise ValueError('Regenerate static pages: ' + ', '.join(stale))
        print('Static translations and SEO are up to date.')
        return
    for path, content in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    print('Built French SEO and three static English pages; all source text covered.')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    build(check=parser.parse_args().check)
