"""
analyze.py - Analysis of results/raw-data.csv (Bubble sort experiment).

Usage (from the repository root):
    pip install pandas matplotlib numpy
    python analysis/analyze.py

Outputs (in analysis/):
    summary_stats.csv        five-number summary + mean + sd per configuration
    median_table.csv         median time (ns) per configuration, algorithms side by side
    figures/*.png            plots used in the report
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "results", "raw-data.csv")
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

ALGS = ["BubbleSortPassPerItem", "BubbleSortUntilNoChange", "BubbleSortWhileNeeded"]
SHORT = {"BubbleSortPassPerItem": "PassPerItem",
         "BubbleSortUntilNoChange": "UntilNoChange",
         "BubbleSortWhileNeeded": "WhileNeeded"}
COLOR = {"PassPerItem": "#d95f02", "UntilNoChange": "#1b9e77", "WhileNeeded": "#7570b3"}
INPUTS = ["RANDOM", "SORTED", "REVERSE", "NEARLY_SORTED"]
SIZES = [100, 500, 1000, 2000, 5000]

# The CSV header has spaces around the commas, so skipinitialspace + rename
d = pd.read_csv(RAW, skipinitialspace=True)
d.columns = ["alg", "size", "input", "rep", "ns"]
d["alg"] = d["alg"].map(SHORT)
ALGS = [SHORT[a] for a in ALGS]

# ---------- descriptive statistics ----------

g = d.groupby(["size", "input", "alg"])["ns"]
s = g.agg(min="min",
          q1=lambda x: x.quantile(.25),
          median="median",
          q3=lambda x: x.quantile(.75),
          max="max", mean="mean", sd="std", n="count").reset_index()
s.to_csv(os.path.join(HERE, "summary_stats.csv"), index=False, float_format="%.1f")

med = s.pivot_table(index=["input", "size"], columns="alg", values="median")
med = med.reindex(INPUTS, level=0)[ALGS]
med["WhileNeeded / PassPerItem"] = med["WhileNeeded"] / med["PassPerItem"]
med["UntilNoChange / PassPerItem"] = med["UntilNoChange"] / med["PassPerItem"]
med.to_csv(os.path.join(HERE, "median_table.csv"), float_format="%.3f")


# ---------- Fig 1: box plots, one panel per input type, one group per size ----------

fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharey=False)
for ax, inp in zip(axes.ravel(), INPUTS):
    pos, data, cols, ticks = [], [], [], []
    for i, n in enumerate(SIZES):
        for j, a in enumerate(ALGS):
            pos.append(i * 4 + j)
            data.append(d[(d["input"] == inp) & (d["size"] == n) & (d["alg"] == a)]["ns"].values / 1e3)
            cols.append(COLOR[a])
        ticks.append(i * 4 + 1)
    bp = ax.boxplot(data, positions=pos, widths=.8, patch_artist=True,
                    flierprops=dict(marker=".", markersize=3), medianprops=dict(color="black"))
    for patch, c in zip(bp["boxes"], cols):
        patch.set_facecolor(c)
    ax.set_yscale("log")
    ax.set_xticks(ticks)
    ax.set_xticklabels(SIZES)
    ax.set_title(inp.replace("_", " ").title())
    ax.set_xlabel("Array size (elements)")
    ax.set_ylabel("Execution time (µs, log scale)")
    ax.grid(axis="y", alpha=.3)
handles = [plt.Rectangle((0, 0), 1, 1, color=COLOR[a]) for a in ALGS]
fig.legend(handles, ALGS, loc="lower center", ncol=3)
fig.tight_layout(rect=(0, .04, 1, 1))
fig.savefig(os.path.join(FIG, "fig1_boxplots.png"), dpi=160)
plt.close(fig)


# ---------- Fig 2: median time vs size (log-log), per input type ----------

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, inp in zip(axes.ravel(), INPUTS):
    for a in ALGS:
        m = s[(s["input"] == inp) & (s["alg"] == a)].sort_values("size")
        ax.plot(m["size"], m["median"] / 1e3, marker="o", label=a, color=COLOR[a])
        ax.fill_between(m["size"], m["q1"] / 1e3, m["q3"] / 1e3, color=COLOR[a], alpha=.15)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks(SIZES); ax.set_xticklabels(SIZES)
    ax.set_title(inp.replace("_", " ").title())
    ax.set_xlabel("Array size (elements)")
    ax.set_ylabel("Median time (µs)")
    ax.grid(alpha=.3, which="both")
axes[0, 0].legend()
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig2_scaling.png"), dpi=160)
plt.close(fig)


# ---------- Fig 3: relative time vs PassPerItem (median) ----------

fig, ax = plt.subplots(figsize=(10, 5))
w = .35
x = np.arange(len(INPUTS))
for k, a in enumerate(["UntilNoChange", "WhileNeeded"]):
    vals = [med.loc[(inp, 5000), a] / med.loc[(inp, 5000), "PassPerItem"] for inp in INPUTS]
    ax.bar(x + (k - .5) * w, vals, w, label=a, color=COLOR[a])
ax.axhline(1, color="gray", ls="--", lw=1)
ax.set_xticks(x); ax.set_xticklabels([i.replace("_", " ").title() for i in INPUTS])
ax.set_ylabel("Median time relative to PassPerItem")
ax.set_title("Relative execution time at n = 5000 (PassPerItem = 1)")
ax.set_yscale("log"); ax.legend(); ax.grid(axis="y", alpha=.3, which="both")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig3_relative_n5000.png"), dpi=160)
plt.close(fig)


# ---------- Fig 4: ECDF for the hardest configuration (random, n = 5000) ----------

fig, ax = plt.subplots(figsize=(8, 5))
for a in ALGS:
    v = np.sort(d[(d["input"] == "RANDOM") & (d["size"] == 5000) & (d["alg"] == a)]["ns"].values) / 1e6
    ax.step(v, np.arange(1, len(v) + 1) / len(v), where="post", label=a, color=COLOR[a])
ax.set_xlabel("Execution time (ms)"); ax.set_ylabel("Empirical CDF")
ax.set_title("ECDF, random input, n = 5000")
ax.legend(); ax.grid(alpha=.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG, "fig4_ecdf_random_5000.png"), dpi=160)
plt.close(fig)


# ---------- console summary ----------

print("Rows:", len(d), "| configs:", s.shape[0], "| reps per config:", s["n"].unique())
print("\nWinner (lowest median) per condition:")
for (inp, n), row in med[ALGS].iterrows():
    print(f"  {inp:14s} n = {n:5d} -> {row.idxmin()}")
