# Continuous Envy-Free Allocation via Reciprocal Preference Matrices

**Reproducibility materials for the manuscript:**

*Continuous Envy-Free Allocation via Reciprocal Preference Matrices: An Alternative to Sperner-Based Discretization*

**Authors:** Luis Ángel Calvo Pascual, Susana Merchán Rubira, Diego de Pereda Sebastián, and Javier Rodrigo Hitos.

## Overview

This repository contains the Python code used to generate the eight figures and reproduce the two worked numerical examples in the accompanying manuscript.

The paper studies envy-free allocation among **three agents and three alternatives** on the continuous allocation simplex. Agent preferences are represented by positive, multiplicatively consistent reciprocal pairwise-comparison matrices. Under this model, two independent preference thresholds per agent determine linear indifference boundaries. The paper derives an exact description of the feasible allocation regions and compares that description with a Sperner-based triangulation procedure.

The code uses exact rational arithmetic (`fractions.Fraction`) for geometric and combinatorial calculations. **No external empirical dataset is required.**

## Repository contents

| Path | Purpose |
| --- | --- |
| `code/geom.py` | Exact preference thresholds, priority vectors, assignment scores, polygon clipping, and Sperner triangulations. |
| `code/style.py` | Common plotting and geometric-visualization functions. |
| `code/figs.py` | Generates Figures 1--8 as PDF and PNG files. |
| `code/verify_examples.py` | Regression checks for the two worked examples (Examples 6.6 and 6.7). |
| `figures/fig1.pdf` ... `figures/fig8.pdf` | Figure PDFs supplied with the manuscript. |
| `requirements.txt` | Python plotting dependency. |

## Requirements

- Python 3 (tested with **Python 3.13.5**).
- Matplotlib (tested with **3.10.8**; the version is pinned in `requirements.txt`).

No separate data download is needed. Computations in the numerical examples are deterministic and use the Python standard library.

## Reproduce the numerical examples

From the repository's root directory, run:

```bash
python -m pip install -r requirements.txt
python code/verify_examples.py
```

Expected output:

```text
inc PASS - optimal assignment BCA triangles intersecting S 3
dis PASS - optimal assignment ACB triangles intersecting S 5
```

These checks reproduce the optimal assignments, exact vertices of the extended solution polygons, the unique fully labelled triangles in the `m = 10` meshes, and the counts of mesh triangles intersecting the strict solution regions.

**Scope of verification:** these regression tests check the two worked examples; they are not a computer-assisted proof of every general theorem in the paper.

## Regenerate the figures

From the repository's root directory, run:

```bash
python code/figs.py
```

The command generates `out/fig1.pdf` through `out/fig8.pdf` and matching 300-dpi PNG files. The `out/` directory is intentionally excluded from Git because these files are generated outputs. Reference PDFs are supplied in `figures/`.

The original figure style uses **Latin Modern Roman**. Font files are **not included** in this repository. If that font is not installed, Matplotlib may substitute another font, so the regenerated images may differ slightly in typography while retaining the same mathematical content.

## Reproducibility notes

- All numerical inputs used in the worked examples and figure scripts are encoded in the Python files.
- The examples use exact fractions for priority vectors, solution-region vertices, and triangulation coordinates.
- The Sperner comparisons in Examples 6.6 and 6.7 use the regular triangular mesh with resolution `m = 10` and the vertex-ownership rule described in the manuscript.
- The supplied scripts cover the worked examples and figures, not an independent automated verification of every statement in the paper.

## Citation and archived version

If you use these materials, please cite the associated manuscript. Bibliographic details and a permanent archival DOI will be added here once available. An archived release on Zenodo can provide a stable, citable software version.

## License

A public reuse license has not yet been selected. A `LICENSE` file should be added after agreement among the coauthors. Public visibility on GitHub does not itself grant reuse rights.
