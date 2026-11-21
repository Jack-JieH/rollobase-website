# RolloBase public sharing copy

The static website has 65 pages across Spanish, English, Traditional Chinese,
Simplified Chinese and Russian, plus a Spanish refrigerated-beverage label guide.
The A–D sample flow is available in all five languages.

Homepages: `/`, `/en`, `/zh` (Traditional), `/zh-cn` (Simplified), `/ru`.
The Spanish guide at `/guia-bopp-botellas-refrigeradas` links to the BOPP product
and the prefilled BOPP sample request. Its trial record is a downloadable CSV.
Public page links use extensionless canonical paths and keep queries and anchors.
Chinese pages use independent `zh-Hant` and `zh-Hans` alternate URLs.
Reviewed buyer guidance lives in `seo-content.json`; Simplified Chinese copy is
checked into `simplified.json`. Builds fail if Chinese source text lacks a translation.
The asset archive contains the stylesheet, sample-form JavaScript and licensed photos.

`design_update.py` applies the shared application-first layout, the five-part
product specification format and the user-provided business telephone across
all five locales. Sample requests remain local TXT downloads; the phone link
lets visitors arrange how to share them. No email or WhatsApp service is assumed.

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
