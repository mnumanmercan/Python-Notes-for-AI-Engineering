# pricing.py
# Model → 1M token başına USD fiyatı. Gizli değil, git'e commit'lenir (versiyon takibi için iyi).
# Güncel fiyatları docs.claude.com'dan teyit et; bunlar örnek.
MODEL_PRICES = {
    "claude-sonnet-4-5": {"input": 5.00, "output": 25.00},
}

def hesapla_maliyet(model, input_tokens, output_tokens,
                    cache_write_tokens=0, cache_read_tokens=0) -> float:
    fiyat = MODEL_PRICES.get(model)
    if fiyat is None:
        raise ValueError(f"Bilinmeyen model: {model}")
    p_in = fiyat["input"]       # base input $/1M
    return (
        input_tokens        / 1_000_000 * p_in
        + cache_write_tokens / 1_000_000 * p_in * 1.25
        + cache_read_tokens  / 1_000_000 * p_in * 0.10
        + output_tokens      / 1_000_000 * fiyat["output"]
    )