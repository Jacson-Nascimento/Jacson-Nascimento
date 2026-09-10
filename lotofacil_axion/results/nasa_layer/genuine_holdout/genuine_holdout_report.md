# AXION - Genuine post-3435 holdout validation

Freeze: contest 3435, 2025-07-05.
Genuine holdout: contests 3436 to 3779 (344 draws).

## Frequency persistence
- Fixed pre-freeze top-15: 9.0872 mean hits, empirical p=0.0974095.
- Rolling 1000: 9.0203 mean hits, empirical p=0.387448.
- Bias-vector Pearson correlation pre vs holdout: r=0.3347, p=0.102016.
- Fixed pre-freeze probability Brier: 0.239974, compared with 0.24 baseline.

## AXION 0.3 genuine holdout
- Single game: 9.0174 mean hits, empirical p=0.402438.
- Brier: 0.240231.
- Portfolio 10: 10.8023 vs random 10.8935; paired difference -0.0912, p=0.0449156.

## Multiplicity
- fixed_top15_hits: p=0.0974095, BH q=0.170027.
- rolling1000_top15_hits: p=0.387448, BH q=0.402438.
- bias_vector_pearson: p=0.102016, BH q=0.170027.
- axion_single_hits: p=0.402438, BH q=0.402438.
- axion_portfolio_vs_random: p=0.0449156, BH q=0.170027.

## Governance
These observations are a falsification test of a signal specified before the post-3435 holdout was inspected. Statistical significance alone does not establish a causal mechanism or future advantage. Results remain experimental until replicated on additional future contests and checked against source/data-quality explanations.
