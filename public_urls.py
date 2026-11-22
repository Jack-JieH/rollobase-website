"""Keep public asset links working on legacy URL aliases."""

import re


ASSET_REFERENCE = re.compile(
    r'(<(?:a|img|link|script)\b[^<>]*?\s(?:href|src)=)("[^"]*"|\'[^\']*\')'
)


def normalize_asset_links(dist, filenames):
    """Anchor published assets at the site root, preserving suffixes and attributes."""
    asset_names = {path.name for path in dist.iterdir() if path.is_file() and path.suffix != '.html'}

    def replace_reference(match):
        prefix, quoted_url = match.groups()
        quote = quoted_url[0]
        url = quoted_url[1:-1].removeprefix('./')
        if re.split(r'[?#]', url, maxsplit=1)[0] not in asset_names:
            return match[0]
        return f'{prefix}{quote}/{url}{quote}'

    for filename in filenames:
        path = dist / filename
        html = path.read_text(encoding='utf-8')
        normalized = ASSET_REFERENCE.sub(replace_reference, html)
        if normalized != html:
            path.write_text(normalized, encoding='utf-8')
