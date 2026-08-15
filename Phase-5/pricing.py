# pricing.py
# Model → 1M token başına USD fiyatı. Gizli değil, git'e commit'lenir (versiyon takibi için iyi).
# Güncel fiyatları docs.claude.com'dan teyit et; bunlar örnek.
MODEL_PRICES = {
    "claude-sonnet-4-5": {"input": 5.00, "output": 25.00},
}

# pricing.py (devamı)
def hesapla_maliyet(model: str, input_tokens: int, output_tokens: int) -> float:
    fiyat = MODEL_PRICES.get(model)          # .get → yoksa None (KeyError değil)
    if fiyat is None:
        raise ValueError(f"Bilinmeyen model, fiyat tanımlı değil: {model}")

    input_maliyet = input_tokens / 1_000_000 * fiyat["input"]
    output_maliyet = output_tokens / 1_000_000 * fiyat["output"]
    return input_maliyet + output_maliyet