import fitz


def _extract_link_targets(page) -> list[str]:
    links = []

    for link in page.get_links():
        uri = link.get("uri")
        if uri:
            links.append(uri.strip())

    return links


def extract_text(pdf_path: str) -> str:
    document = fitz.open(pdf_path)

    text = ""
    link_targets = []

    for page in document:
        text += page.get_text()
        link_targets.extend(_extract_link_targets(page))

    document.close()

    if link_targets:
        unique_targets = []
        seen = set()

        for target in link_targets:
            normalized = target.strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            unique_targets.append(normalized)

        text += "\n\nLINK TARGETS\n"
        text += "\n".join(unique_targets)

    return text
