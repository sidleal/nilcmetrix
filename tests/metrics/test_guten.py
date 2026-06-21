# -*- coding: utf-8 -*-
"""Behavioral tests for metrics in text_metrics/metrics/guten.py."""

import pytest

import text_metrics
from text_metrics.metrics.guten import GunningFog


def gunning_fox(text):
    return GunningFog().value_for_text(text_metrics.Text(text))


# ---------------------------------------------------------------------------
# gunning_fox = 0.4 × (words / sentences + 100 × complex_words / words)
# A "complex" word has 3 or more syllables. The complex-word term is a
# percentage (0–100), so it dominates the score on dense text.
# ---------------------------------------------------------------------------

class TestGunningFog:

    def test_without_complex_words_only_the_length_term_remains(self):
        # No word has 3+ syllables, so the complex term is 0 and the score is
        # 0.4 × words / sentences = 0.4 × 5 / 1.
        assert gunning_fox("O gato bebeu o leite.") == pytest.approx(2.0)

    def test_all_words_complex_makes_the_complex_term_a_full_100(self):
        # Every word has 3+ syllables, so complex / words = 1 → the term is a
        # full 100%: 0.4 × (4 / 1 + 100) = 41.6.
        assert gunning_fox(
            "Professores estudiosos analisam estatísticas."
        ) == pytest.approx(41.6)

    @pytest.mark.parametrize(
        "label, text, expected",
        [
            # 0.4 × (6/1 + 100 × 4/6)
            ("one sentence, 4 of 6 complex",
             "A professora explicou a matéria complicada.", 29.066667),
            # 0.4 × (6/2 + 100 × 3/6)
            ("two sentences, 3 of 6 complex",
             "Comprei pão. Ela estuda medicina veterinária.", 21.2),
        ],
    )
    def test_complex_words_enter_as_a_percentage(self, label, text, expected):
        assert gunning_fox(text) == pytest.approx(expected), label
