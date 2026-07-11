from app.evaluation.generation_metrics import calculate_metrics


def test_calculate_metrics_identical_text_gives_high_scores():
    text = "Wells Fargo resolved the dispute by correcting the credit report."
    r1, rl, bleu = calculate_metrics(text, text)
    assert r1 == 1.0
    assert rl == 1.0
    assert bleu > 0.9


def test_calculate_metrics_unrelated_text_gives_low_scores():
    r1, rl, bleu = calculate_metrics("completely unrelated sentence here", "Wells Fargo credit report dispute")
    assert r1 < 0.5
    assert rl < 0.5
