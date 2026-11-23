# Extensions of Alekseyev (2026): arXiv:2611.01243v1, Section 6, paragraph 2, page 18

The note answers the regularity question in Max A. Alekseyev's *Halving
Partitions and Hyperbinary Expansions*, arXiv:2611.01243v1, Section 6,
page 18. It classifies the partitions of `2^m+1`, proves nonexistence of a
finite decimation family over every nonzero commutative ring, and deduces
nonautomaticity modulo every integer at least two in every base `2^s`,
`s >= 1`. It gives a flat dyadic length distribution, its exact mean and
variance, an explicit deficit from Stern's sequence, and the digit-1
weighted refinement on `n = 2^v (2^m+1)`.
It also determines `A_rho(2^m+1)` for every nonnegative offset `rho`,
recovering the stabilization threshold in Alekseyev's Theorem 17.
The dyadic count, length spectrum and total-part sum are explicit
specializations of Alekseyev's Theorem 5; the note gives an alternative
actual-list proof and further ring, digit-weight and base extensions.

## Files

- `note.tex`: self-contained LaTeX, including its bibliography.
- `metadata.json`: bibliographic metadata and the precise Lean source link.
- `verify.py`: Python 3 exact finite counting checks; standard library only.
- `verification.json`: deterministic finite-check results and numerical ranges.

The PDF is supplied separately as `note.pdf`.

## Rebuild

Use Tectonic 0.17.0:

```sh
tectonic note.tex
python3 verify.py --output verification.json
```

Alternatively, use a LaTeX distribution with `amsmath`, `amssymb`, `amsthm`,
`booktabs`, `array`, `geometry`, `lmodern`, and `hyperref`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded; BibTeX is unnecessary.

## Scientific coverage

The written proof establishes the dyadic length polynomial, total-part
formula, growth bound, nonregularity over nonzero commutative rings, and
nonautomaticity modulo every integer at least two. Further written proofs
give the digit-weight polynomial, deficit, flat distribution, mean and
variance, and the base-`2^s` extension. The finite checker
compares direct positive-list enumeration for `0 <= n <= 256` with a
separate memoized halving-chain count, and checks the dyadic length and
total-part formulas for `2 <= m <= 80`. Further finite ranges appear in
`verification.json`; these checks do not replace the infinite proof.
It independently enumerates digit weights for `1 <= n <= 256`, and
checks the dyadic weighted polynomial, deficit and length moments for
`2 <= m <= 80`, including dilation by `2^v`, `0 <= v <= 3`.
The offset-count formula is checked for `2 <= m <= 40`, `0 <= rho <= m+2`.

The integer family/matrix nonexistence statement and the source-count
identification are the content of `HalvingPartitionNonregularity.result`
in the pinned scientific source:

https://github.com/the-omega-institute/trureturing/blob/1154841a3345ca579e0d56fc4ceebee38814557c/D5/S1/Recurrence/Partitions/HalvingPartitionNonregularity.lean

The ring, modular, length-polynomial, total-part, growth, deficit,
digit-weight, length-moment and base-`2^s` conclusions
are justified by the note's written arguments.

The coverage table distinguishes these dyadic answers from the general
deficit, fixed-digit maximum, general weighted-count and larger-division-base
questions. The formulas for even dilation and Mersenne arguments are
credited to Alekseyev and OEIS A349552, not presented as new results.
OEIS A349553 is the least-input sequence; its exact values are outside
the note's coverage.

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0 (`cc-by-4.0`).
