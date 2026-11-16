"""Build the four-language site using the URL assigned by its host."""
import os
from pathlib import Path
import runpy
from urllib.parse import urlsplit

origin = os.environ.get('SITE_ORIGIN') or os.environ.get('RENDER_EXTERNAL_URL')
if not origin:
    raise SystemExit('Set SITE_ORIGIN or build inside Render with RENDER_EXTERNAL_URL.')
parts = urlsplit(origin)
if parts.scheme != 'https' or not parts.netloc or parts.path not in ('','/') or parts.query or parts.fragment or parts.username:
    raise SystemExit('The site origin must be an HTTPS origin without a path or credentials.')
os.environ['SITE_ORIGIN'] = origin.rstrip('/')
runpy.run_path(str(Path(__file__).with_name('build.py')),run_name='__main__')
print('Built 52 pages for', os.environ['SITE_ORIGIN'])
