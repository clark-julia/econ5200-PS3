# ECON 5200 PS3: The Rollout That Looked Like It Worked

## Objective

I showed that a standard two-way fixed effects (TWFE) regression gave a badly wrong estimate of a program rollout with staggered adoption, and I rebuilt the estimate using only clean comparisons.

## Methodology

- Replicated Card & Krueger's minimum wage study as a 2x2 difference-in-differences and as a regression, and both gave +2.75 FTE.
- Built a simulated panel of 40 counties in 8 regional boards over 12 years, where I set the true effects myself.
- Ran the agency's TWFE regression on the panel and compared it with the true average effect on treated county-years.
- Decomposed TWFE into its 2x2 comparisons and measured how much weight fell on already-treated counties used as controls.
- Estimated the effect using only not-yet-treated controls, built from 30 group-by-year comparisons.
- Plotted an event study with pre-treatment estimates to look at parallel trends.
- Compared default, county-clustered and board-clustered standard errors, then ran a wild cluster bootstrap with all 2^8 sign patterns, since there are only 8 boards.
- Wrote the methods into a reusable module (`src/did_toolkit.py`).

## Key Findings

- The agency's TWFE estimate was -0.15, while the true average effect on treated county-years was 7.73.
- About 38% of the TWFE weight sat on comparisons that use already-treated counties as controls. Those comparisons averaged -8.7, which pulled the estimate down.
- The clean estimate was 7.61. Dropping one board at a time moved it between 6.24 and 8.41.
- The board-clustered standard error was 3.31, compared with 0.73 by default and 1.42 clustered by county. Treatment was assigned by board, so board clustering is the right choice.
- The wild bootstrap p-value for TWFE was 1.00, so the agency's number can't be told apart from zero.
- The event study's pre-treatment estimates were small, which is consistent with parallel trends but doesn't prove it. With only 8 boards, the exact size of the effect is uncertain.
