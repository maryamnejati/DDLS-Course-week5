import json
from pathlib import Path
import numpy as np
import pandas as pd
import scanpy as sc
from scipy.stats import mannwhitneyu
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

p = Path(__file__).parent / 'ddls-week5-s1-junk-or-signal-dataset/data/pbmc3k.h5ad'
a = sc.read_h5ad(p)
mask = a.obs.leiden.astype(str).isin(['0','1']).to_numpy()
labels = a.obs.loc[mask, 'leiden'].astype(str).to_numpy()
X = a.X[mask].toarray()
clusters = {c: labels == c for c in ['0','1']}
# Differential expression on normalized expression; Wilcoxon and BH correction.
a2 = a[mask].copy()
sc.tl.rank_genes_groups(a2, 'leiden', groups=['0','1'], reference='1', method='wilcoxon', use_raw=False)
rg = a2.uns['rank_genes_groups']
rows=[]
for gi, group in enumerate(['0','1']):
    names=rg['names'].tolist()[gi] if hasattr(rg['names'], 'tolist') else rg['names'][gi]; scores=rg['scores'].tolist()[gi] if hasattr(rg['scores'], 'tolist') else rg['scores'][gi]; pvals=rg['pvals'].tolist()[gi] if hasattr(rg['pvals'], 'tolist') else rg['pvals'][gi]; adj=rg['pvals_adj'].tolist()[gi] if hasattr(rg['pvals_adj'], 'tolist') else rg['pvals_adj'][gi]; lfc=rg['logfoldchanges'].tolist()[gi] if hasattr(rg['logfoldchanges'], 'tolist') else rg['logfoldchanges'][gi]
    for i,g in enumerate(names[:100]):
        gi=list(a.var_names).index(g)
        vals0=X[clusters['0'],gi]; vals1=X[clusters['1'],gi]
        rows.append({'group':group,'gene':str(g),'score':float(scores[i]),'logfoldchange':float(lfc[i]),'pvalue':float(pvals[i]),'pvalue_adj':float(adj[i]),'fraction_0':float((vals0>0).mean()),'fraction_1':float((vals1>0).mean()),'mean_0':float(vals0.mean()),'mean_1':float(vals1.mean())})
# Quality tests
quality={}
for col in ['n_genes','total_counts','pct_mito']:
    v0=a.obs.loc[mask & (a.obs.leiden.astype(str)=='0'),col].to_numpy(); v1=a.obs.loc[mask & (a.obs.leiden.astype(str)=='1'),col].to_numpy()
    u,pv=mannwhitneyu(v0,v1,alternative='two-sided')
    quality[col]={'cluster_0_mean':float(v0.mean()),'cluster_1_mean':float(v1.mean()),'cluster_0_median':float(np.median(v0)),'cluster_1_median':float(np.median(v1)),'u_statistic':float(u),'pvalue':float(pv)}
# Predictive separation using PCA-like top variable genes, held-out logistic regression.
var=np.var(X,axis=0); genes=np.argsort(var)[-1000:]
model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,solver='liblinear'))
cv=StratifiedKFold(5,shuffle=True,random_state=42)
scores=cross_val_score(model,X[:,genes],labels,cv=cv,scoring='roc_auc')
# save JSON
out={'dataset':str(p),'n_cells':int(mask.sum()),'cell_counts':{c:int(clusters[c].sum()) for c in ['0','1']},'quality_tests':quality,'classification':{'method':'5-fold stratified logistic regression on 1,000 most variable genes','roc_auc_mean':float(scores.mean()),'roc_auc_sd':float(scores.std()),'folds':scores.tolist()},'markers':rows}
Path('cluster_0_vs_1_analysis.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'counts':out['cell_counts'],'quality':quality,'classification':out['classification'],'top0':rows[:10],'top1':[r for r in rows if r['group']=='1'][:10]},indent=2))
