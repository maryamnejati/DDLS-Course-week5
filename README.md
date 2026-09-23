# PBMC 3K Navigator

An interactive FastAPI/Scanpy navigator for exploring a processed single-cell RNA-sequencing dataset of 2,700 human peripheral blood mononuclear cells (PBMCs). The app combines an interactive UMAP, cluster marker summaries, quality metrics, and focused statistical evidence for the two decisions requested by the data owner: whether clusters 0 and 1 should remain separate, and whether the small cluster 6 should be removed.

## What the app does

The navigator has three tabs:

### Overview

- Shows the dataset structure and cluster sizes.
- Displays a **Clusters: top marker genes** table for clusters 0–7.
- Shows **UMAP by cluster**, with a different color for each cluster and dotted boundaries around clusters.
- Lets you click a cluster to view its top markers and quality summary beside the UMAP.
- Includes the **Full dataset explorer**, where you can choose a cluster and a gene to color the UMAP by expression.
- Shows top markers for the selected cluster in the explorer controls.

### Cluster 0 vs 1

- Presents the recommendation to keep clusters 0 and 1 separate.
- Compares cell counts, detected genes, total counts, and mitochondrial percentage.
- Reports Mann–Whitney tests for quality metrics.
- Shows the top five differential markers for each cluster in a table and bar chart.
- Reports the five-fold cross-validated logistic-regression result using the 1,000 most variable genes.
- Defines how log fold change is interpreted.

### Cluster 6

- Reviews the 13-cell cluster separately.
- Shows its quality summary and top marker genes.
- Highlights the platelet-associated markers `PPBP` and `PF4`.
- Recommends retaining the cluster provisionally and flagging it for validation rather than deleting it automatically.

## Dataset

The app loads:

```text
ddls-week5-s1-junk-or-signal-dataset/data/pbmc3k.h5ad
```

The AnnData file contains:

- 2,700 cells
- 13,714 genes
- Log-normalized expression in `adata.X`
- Raw UMI counts in `adata.layers["counts"]`
- Leiden cluster labels in `adata.obs["leiden"]`
- Quality metrics in `adata.obs["n_genes"]`, `total_counts`, and `pct_mito`
- UMAP coordinates in `adata.obsm["X_umap"]`

## Requirements

- Python 3.10 or newer
- `pip` or [`uv`](https://docs.astral.sh/uv/)
- A modern web browser

## Installation

From the repository root, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, with `uv`:

```bash
uv venv
uv pip install --python .venv/bin/python -r requirements.txt
```

## Run the app

From the repository root:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open the navigator at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

The dataset is loaded once during application startup using Scanpy.

## API endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/umap?cluster=all` | UMAP coordinates and cell/cluster labels |
| `GET /api/genes?search=CD3` | Search available genes |
| `GET /api/expression/{gene}` | Per-cell expression for a gene |
| `GET /api/clusters` | Cluster labels and cell counts |
| `GET /api/cluster/{cluster}` | Cluster markers and quality summary |
| `GET /api/compare/0/1` | Marker and quality comparison for clusters 0 and 1 |
| `GET /api/analysis/cluster-0-vs-1` | Saved statistical analysis results |
| `GET /api/decisions` | Current decision summaries |

## Analysis conclusion for the data owner

Clusters 0 and 1 should be kept separate: their expression profiles are strongly distinguishable, with a five-fold cross-validated logistic regression using the 1,000 most variable genes achieving a mean ROC AUC of 1.00, while their detected-gene and mitochondrial distributions also differ; however, total counts do not differ, so technical quality effects should be considered when interpreting markers. Cluster 6 should not be deleted automatically: although it contains only 13 cells and therefore has low-confidence statistics, its coherent `PPBP` and `PF4` platelet-associated signal supports retaining it provisionally and flagging it for validation before finalizing the figure or sorting strategy.

## Project files

- `app.py` — FastAPI application, API endpoints, and browser interface.
- `analyze_clusters.py` — reproducible cluster 0 versus 1 analysis script.
- `cluster_0_vs_1_analysis.json` — saved analysis output.
- `requirements.txt` — Python dependencies.
- `ddls-week5-s1-junk-or-signal-dataset/data/pbmc3k.h5ad` — AnnData dataset.
- `ddls-week5-interview.md` — interview transcript with the data owner.

## Data and secrets

The local `.env` file may contain credentials and is intentionally excluded by `.gitignore`. Do not commit API keys or other secrets.

## Limitations

- UMAP is a visualization and should not be interpreted as a quantitative distance measure.
- Small clusters, particularly cluster 6 and cluster 7, have unstable marker estimates.
- The app's marker summaries are intended for exploration and decision support, not as a substitute for experimental validation.
- The cluster 0 versus 1 classifier demonstrates expression-based separability in this dataset; it does not by itself prove that the populations can be separated by surface markers in a flow-sorting panel.
