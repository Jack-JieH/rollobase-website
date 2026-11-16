# RolloBase public sharing copy

This is the complete 2026-11-16 four-language static website: Spanish, English,
Traditional Chinese and Russian, with 52 pages and the existing A–D sample flow.

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

Before sending the new URL, check the four homepages, mobile comparison table,
sample download, sitemap and robots.txt without authentication. Availability in
mainland China must be tested from the intended visitor's connection.

Sample forms download a text brief; they do not send orders or inquiries.
Photography credits and licensing information are preserved in each page footer.
