# RolloBase public sharing copy

This is the 2026-11-19 five-language static website: Spanish, English,
Traditional Chinese, Simplified Chinese and Russian, with 65 pages and the A–D sample flow.

Homepages: `/`, `/en`, `/zh` (Traditional), `/zh-cn` (Simplified), `/ru`.
Chinese pages use independent `zh-Hant` and `zh-Hans` alternate URLs.
Reviewed buyer guidance lives in `seo-content.json`; Simplified Chinese copy is
checked into `simplified.json`. Builds fail if Chinese source text lacks a translation.
The asset archive contains the stylesheet, sample-form JavaScript and licensed photos.

## Deploy

- Service: Render Static Site. This must remain a static site, not a web service.
- Build command: `python3 deploy_build.py`
- Publish directory: `dist`
- Runtime dependencies: Python standard library only.
- `render.yaml` contains extensionless page routes.
- Canonical URLs, language alternates and the sitemap use the host's assigned
  `RENDER_EXTERNAL_URL`, or an explicitly configured HTTPS `SITE_ORIGIN`.
- Publish only `dist`, without access protection or visitor authentication.

The previous live website remains unchanged. The source in this copy contains
only website content and build configuration, not research workbooks or credentials.

Before sending the new URL, check the five homepages, mobile comparison table,
sample download, sitemap and robots.txt without authentication. Availability in
mainland China must be tested from the intended visitor's connection.

Sample forms download a text brief; they do not send orders or inquiries.
Photography credits and licensing information are preserved in each page footer.
