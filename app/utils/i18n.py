# app/utils/i18n.py
from deep_translator import GoogleTranslator

def tr(text: str, source: str = "en", target: str = "pt") -> str:
    """Traduz texto entre idiomas."""
    if not text:
        return text
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception:
        return text

def tr_to_en(text: str) -> str:
    """Traduz texto português → inglês para consultas da API."""
    return tr(text, source="pt", target="en")

def tr_many(texts: list[str], source: str = "en", target: str = "pt") -> list[str]:
    """Traduz uma lista de textos."""
    out = []
    for t in texts:
        try:
            out.append(GoogleTranslator(source=source, target=target).translate(t))
        except Exception:
            out.append(t)
    return out
