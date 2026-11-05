"""Simulated data for the Batch Effects module in the Pitfalls Lab.

Every case was processed in batch 1 and every control in batch 2, so
batch and condition are perfectly confounded. The simulated expression
values contain a batch shift and no condition effect at all.

Run from the repository root:
    python scripts/batch_effects_pca.py
Writes assets/figures/batch_effects_pca.png
"""

import matplotlib.pyplot as plt
import numpy as np

N_PER_GROUP = 6
N_GENES = 500
BATCH_SHIFT = 1.5
SEED = 42


def simulate_expression(rng):
    """Return a samples x genes matrix with a batch shift and no biology."""
    n_samples = 2 * N_PER_GROUP
    values = rng.normal(0, 1, size=(n_samples, N_GENES))
    affected = rng.random(N_GENES) < 0.3
    values[N_PER_GROUP:, affected] += BATCH_SHIFT
    return values


def first_two_pcs(values):
    """Centre the matrix and return the first two principal components."""
    centred = values - values.mean(axis=0)
    u, s, _ = np.linalg.svd(centred, full_matrices=False)
    return u[:, :2] * s[:2]


def plot_panel(ax, pcs, labels, title):
    for label, colour in zip(sorted(set(labels)), ["#2f6f6f", "#c47a3d"]):
        idx = [i for i, x in enumerate(labels) if x == label]
        ax.scatter(pcs[idx, 0], pcs[idx, 1], s=60, color=colour, label=label)
    ax.set_title(title)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.legend(frameon=False)


def main():
    rng = np.random.default_rng(SEED)
    pcs = first_two_pcs(simulate_expression(rng))
    condition = ["case"] * N_PER_GROUP + ["control"] * N_PER_GROUP
    batch = ["batch 1"] * N_PER_GROUP + ["batch 2"] * N_PER_GROUP

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    plot_panel(axes[0], pcs, condition, "Colored by condition")
    plot_panel(axes[1], pcs, batch, "Colored by batch")
    fig.tight_layout()
    fig.savefig("assets/figures/batch_effects_pca.png", dpi=150)


if __name__ == "__main__":
    main()
