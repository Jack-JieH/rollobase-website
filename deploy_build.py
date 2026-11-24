"""Build the five-language site using the URL assigned by its host."""
import os
import json
from pathlib import Path
import runpy
from shutil import copyfile
from urllib.parse import urlsplit
from zipfile import ZipFile

origin = os.environ.get('SITE_ORIGIN') or os.environ.get('RENDER_EXTERNAL_URL')
if not origin:
    raise SystemExit('Set SITE_ORIGIN or build inside Render with RENDER_EXTERNAL_URL.')
parts = urlsplit(origin)
if parts.scheme != 'https' or not parts.netloc or parts.path not in ('','/') or parts.query or parts.fragment or parts.username:
    raise SystemExit('The site origin must be an HTTPS origin without a path or credentials.')
os.environ['SITE_ORIGIN'] = origin.rstrip('/')
root = Path(__file__).parent
dist = root/'dist'
dist.mkdir(exist_ok=True)
photos = json.loads((root/'site-photos.json').read_text(encoding='utf-8'))['photos']
photo_files = {'photos/' + photo['file'] for key, photo in photos.items() if key != 'pack'}
(dist/'photos').mkdir(exist_ok=True)
with ZipFile(root/'site-assets.zip') as assets:
    expected = {'style.css','hero-rolls.webp'} | photo_files
    if set(assets.namelist()) != expected:
        raise SystemExit('The site asset bundle does not match the expected files.')
    for name in expected:
        (dist/name).write_bytes(assets.read(name))
(dist/'labelstock.webp').unlink(missing_ok=True)
copyfile(root/'buyer.js', dist/'buyer.js')
runpy.run_path(str(root/'build.py'),run_name='__main__')
if os.environ['SITE_ORIGIN'] == 'https://rollobase-materials.onrender.com':
    # Google Search Console checks this public tag on the canonical homepage.
    homepage = dist/'index.html'
    verification = '<meta name="google-site-verification" content="BxAOcnRNOY8abPEE5USKcO1PO-CD7UU5JoSyb8Jwb-I">'
    homepage.write_text(homepage.read_text(encoding='utf-8').replace('</head>', verification + '</head>', 1), encoding='utf-8')
from catalog_expansion import apply
apply(dist, os.environ['SITE_ORIGIN'])
from catalog_layout import apply_catalog_layout
apply_catalog_layout(dist)
from news import apply_news
apply_news(dist, os.environ['SITE_ORIGIN'])
from unified_layout import apply_unified_layout
apply_unified_layout(dist)
print('Built',len(list(dist.glob('*.html'))),'pages for',os.environ['SITE_ORIGIN'])
