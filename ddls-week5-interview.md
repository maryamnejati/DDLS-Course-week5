# DDLS 2026 — Week 5 interview transcript

**Lab:** Interview a Single-Cell Data Owner
**Data owner:** Dr. Ravi Menon — Immunologist cleaning up a PBMC single-cell dataset before a figure
**Student:** Maryam Nejati <maryam.nejati@scilifelab.se>
**Exported:** 2026-09-23T11:55:12+00:00

> This is the record of your interview with the data owner. Hand it to your analyst agent as the raw source for `AGENTS.md` and `spec.md`.

---

**You**:

Hi! can you tell me about you and your project?

**Dr. Ravi Menon**:

I’m Dr. Ravi Menon, an immunologist working with human blood cells. This is my first PBMC single-cell dataset—**2,700 cells**, returned by the facility in numbered clusters 0–7 with a little map. The thing nagging me is cluster 6: only **about 13 cells**, with roughly **350 genes each**, so I’m about to bin it as junk. Can you confirm it’s safe to delete before it messes up the figure?

**You**:

can you tell me about the data set? What each file contain? and what's the structure of the files? is there any specific app or software I should use to open them? and what's PBMC?

**Dr. Ravi Menon**:

It’s **one processed file** from the core facility, containing the readouts for 2,700 individual PBMCs, their numbered groups **0–7**, and a two-dimensional map. I don’t know the internal file structure or what software it expects—I’m not the computational person; the facility sent it back ready to interpret.

PBMC means *peripheral blood mononuclear cells*: mainly lymphocytes and monocytes isolated from blood, excluding red cells and most granulocytes. For opening it, use whatever application the facility specified; I don’t know whether they gave us a spreadsheet, an analysis object, or something else. What file extension did they send you?

**You**:

ok, the readme file says I should open it in python. what was the goal of your assay? what are you looking for in the data? what does each cluster mean? and why do you think the cluster 6 is junk?

**Dr. Ravi Menon**:

The assay was to catalogue the immune cells in this blood sample and assign the numbered groups to cell populations. In particular, I need to decide whether clusters **0 and 1** are one population or two before Dr. Alvarez plans the follow-up sorting panel.

I can’t tell you what clusters 0–7 mean from the numbers alone—the facility hasn’t given me cell-type names. Cluster 6 worries me because it has only **13 cells**, with about **350 genes per cell**, whereas the other groups are much larger or have more genes; that looks like dead cells or empty droplets to me. The readme says Python, but I don’t know the file structure well enough to interpret it—what does it say is inside the file?

**You**:

what makes you believe that a cluster should be assigned as junk and be deleted or not. and what's the sorting that Dr. Alvarez is planning? is it dependant on this analysis that I'm going to do?

**Dr. Ravi Menon**:

My instinct about cluster 6 is simply **13 cells with roughly 350 genes each**—it looks like dead or empty material. But I don’t know the computational criteria for calling something junk, so I need you to determine that rather than just agreeing with me.

Dr. Alvarez is planning a flow-sorting panel to separate the relevant blood-cell populations for follow-up work. Yes, the panel depends on whether clusters 0 and 1 are one population or two; an artificial split could mean unnecessary sorting gates, while a real distinction could get lost. Can you check what clusters 0 and 1 are actually expressing before making that call?

**You**:

what makes the sorting-panel recommendation usable? do you know what row or cell record represent? and if there's some fields mentioned in the file, what are their meaning? how did you collect the samples? how was the clustered assigned and is there any differences between batches (if there are different batches)?

**Dr. Ravi Menon**:

The sorting panel is usable if the analysis shows that the groups correspond to distinct blood-cell populations that can be separated with surface proteins; if clusters 0 and 1 are the same population, we should not design two separate gates for them. I need that call from the expression data, not just the numbered groups.

What I know about the records is limited: one row or cell record should represent one of the **2,700 individual cells**, but I don’t know the exact columns or their meanings. The facility isolated PBMCs from a blood sample, performed the sequencing and initial grouping, and returned clusters 0–7 plus the map; I wasn’t given the clustering procedure or any batch details. Does the file or readme list sample IDs, batch labels, and the column names?

**You**:

what are the evidences that are required to distinguish between cluster 0 and 1 as two separate clusters? and is there a special format you would prefer for your results?

**Dr. Ravi Menon**:

I’d need to see whether clusters 0 and 1 have **different sets of genes turned on**, not just that the facility numbered them separately. Please include the genes most characteristic of each group, how consistent those patterns are across the cells, and the summary numbers: cluster 0 has **1,197 cells, 809 genes per cell, 1.8% mito**; cluster 1 has **489 cells, 850 genes per cell, 2.3% mito**. If the gene patterns and those cell-quality summaries are essentially alike, I’d lean toward combining them; if the gene patterns separate cleanly, keep them apart.

A plain table is fine: recommendation first, then cluster size, the main gene names for each group, and the corresponding per-cell summaries. I don’t need a special app or polished figure—Dr. Alvarez mainly needs a defensible one-population versus two-population call. Can you extract the gene lists for clusters 0 and 1?

**You**:

do you know if there are any missing data that I should be aware of?

**Dr. Ravi Menon**:

I don’t know—the summary I have doesn’t say whether any cell records or gene readings are missing. The facility only gave me the cluster counts and summaries; does the readme mention blank entries or cells excluded before clustering?

**You**:

correct me if I'm wrong. you want a summary of all clusters with the cluster size, the main gene names for each group. and you want to know if clusters 0 an d1 are two separate clusters or can be combined in one and if cluster 6 is a true cluster, right?

**Dr. Ravi Menon**:

Almost. I mainly need:

- the **main genes** defining clusters 0 and 1, with their cell-quality summaries;
- a clear recommendation to **keep 0 and 1 separate or combine them**;
- and an assessment of whether cluster 6 is junk to remove or should be retained before it affects the figure.

A full summary of every cluster would be useful only if it helps interpret those decisions. I still suspect cluster 6 is junk—**13 cells and about 350 genes each**—but I need you to make the call from the data rather than simply confirm my assumption.

**You**:

is there anything that you want me to know and I haven't asked?

**Dr. Ravi Menon**:

Only that I need the **0-versus-1 call by tomorrow morning** for Dr. Alvarez, and I don’t want a figure cluttered by an artificial split. For cluster 6, my instinct remains to remove the **13-cell** group, but you need to assess it from the data—don’t just rubber-stamp me.

**You**:

what makes you distrust the result of the analysis righ away and what a good analysis would look like for you?

**Dr. Ravi Menon**:

I distrust cluster 6 **on sight** because it contains only **13 cells**, each with about **350 genes**—that makes me worry the facility’s grouping is being driven by poor material rather than a meaningful blood population. But that is my bench instinct, not a conclusion from the analysis.

A useful analysis would show the actual genes switched on in clusters 0 and 1, whether those patterns are consistent across cells, and the size/mitochondrial summaries: cluster 0 is **1,197 cells, 809 genes, 1.8% mito**; cluster 1 is **489 cells, 850 genes, 2.3% mito**. Then give me a direct recommendation: combine 0 and 1, keep them separate, and retain or remove 6—with the visible evidence named. Are you asking mainly about the suspicious small group, or the 0-versus-1 decision?

**You**:

ok, thank you

**Dr. Ravi Menon**:

Right—please don’t just delete cluster 6 on my say-so. I need the expression evidence and the clear 0-versus-1 recommendation for the handoff tomorrow.
