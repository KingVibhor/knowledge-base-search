from pypdf import PdfReader

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        page_text = page.extract_text(suppress_overlapping=True) or ""
        texts.append(page_text)
    return "\n".join(texts)
