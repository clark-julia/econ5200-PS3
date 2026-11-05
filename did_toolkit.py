"""Difference-in-differences toolkit (ECON 5200 PS3), extending Lab 11's did_utils.py."""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

NEVER = 10 ** 9      # the cohort of a never-treated unit: later than any period

# Lab 11's functions, carried over

def two_by_two(df: pd.DataFrame, outcome: str, treated: str, post: str) -> float:
    """The canonical 2x2: difference of differences of the four group means."""
    g = df.groupby([treated, post])[outcome].mean()
    return float((g[1, 1] - g[1, 0]) - (g[0, 1] - g[0, 0]))


def clean_att(df: pd.DataFrame, time: str = "t", outcome: str = "y",
              cohort: str = "g") -> tuple[pd.DataFrame, float]:
    """ATT(g, t) cells against not-yet-treated controls, and their size-weighted average.

    Controls are units with cohort > t (never-treated included); both changes are
    measured from g - 1. Returns the cells (g, t, att, n) and the weighted mean.
    """
    out = []
    for g in sorted(df.loc[df[cohort] < NEVER, cohort].unique()):
        treated = df[df[cohort] == g]
        if (treated[time] == g - 1).sum() == 0:
            continue                                    # no baseline period for this cohort
        for t in range(g, df[time].max() + 1):
            controls = df[df[cohort] > t]
            if controls.empty:
                continue                                # nobody left to compare with
            d_tr = (treated.loc[treated[time] == t, outcome].mean()
                    - treated.loc[treated[time] == g - 1, outcome].mean())
            d_co = (controls.loc[controls[time] == t, outcome].mean()
                    - controls.loc[controls[time] == g - 1, outcome].mean())
            out.append({"g": g, "t": t, "att": d_tr - d_co,
                        "n": int((treated[time] == t).sum())})
    cells = pd.DataFrame(out)
    return cells, float(np.average(cells["att"], weights=cells["n"]))


def event_study(cells: pd.DataFrame) -> pd.DataFrame:
    """Average ATT(g, t) cells by event time e, weighted by n (cells need columns e, att, n).

    Negative e are pre-treatment periods: a diagnostic, not a test of parallel trends.
    """
    rows = [{"e": e, "att": np.average(grp["att"], weights=grp["n"])}
            for e, grp in cells.groupby("e")]
    return pd.DataFrame(rows)


def pre_cells(df: pd.DataFrame, time: str, outcome: str, cohort: str,
              unit: str) -> pd.DataFrame:
    """Pre-period cells for cohort g in period t < g - 1, measured from base g - 1.

    Controls are cohorts adopting after g, so they are untreated in both periods compared.
    Returns columns g, t, e, att, n.
    """
    rows = []
    for g in sorted(c for c in df[cohort].unique() if c < NEVER):
        tr, co, base = df[df[cohort] == g], df[df[cohort] > g], g - 1
        for t in sorted(df.loc[df[time] < base, time].unique()):
            d_tr = tr.loc[tr[time] == t, outcome].mean() - tr.loc[tr[time] == base, outcome].mean()
            d_co = co.loc[co[time] == t, outcome].mean() - co.loc[co[time] == base, outcome].mean()
            rows.append({"g": g, "t": t, "e": t - g, "att": d_tr - d_co,
                         "n": tr[unit].nunique()})
    return pd.DataFrame(rows)


# your clustered-inference wrapper (Step 3.3)

def twfe_fit(df: pd.DataFrame, outcome: str, treat: str, unit: str, time: str,
             cluster: str | None = None):
    """TWFE fit `outcome ~ treat + C(unit) + C(time)`; cluster-robust SEs if `cluster` is given.

    The point estimate is the same either way; only the standard error changes.
    Cluster at the level where treatment was assigned.
    """
    model = smf.ols(f"{outcome} ~ {treat} + C({unit}) + C({time})", data=df)
    if cluster is None:
        return model.fit()
    return model.fit(cov_type="cluster", cov_kwds={"groups": df[cluster]})


# your bootstrap (Task 4.1)

def wild_cluster_bootstrap(df, cluster, y="y", treat="D", unit="county", time="year", max_G=14):
    """
    Wild cluster bootstrap-t, null imposed, Rademacher weights, full enumeration of 2^G sign vectors.
    Model: y ~ treat + unit FE + time FE (the TWFE/DiD regression). Cluster-robust t everywhere (CRV1).
    `cluster` is the column holding the cluster id (e.g. the regional board).
    """
    d = df.reset_index(drop=True)
    codes, labels = pd.factorize(d[cluster])
    G = len(labels)
    if G > max_G:
        raise ValueError(f"{G} clusters means 2^{G} weight vectors; enumeration is only sensible for small G.")

    fe = pd.get_dummies(d[[unit, time]].astype(str), drop_first=True, dtype=float)
    fe.insert(0, "const", 1.0)
    X_r = fe.to_numpy()                                   # restricted: no treatment term
    X_u = np.column_stack([d[treat].to_numpy(float), X_r])  # unrestricted: treatment is column 0
    yv = d[y].to_numpy(float)

    def fit_t(yy, use_t=False):
        res = sm.OLS(yy, X_u).fit(cov_type="cluster", cov_kwds={"groups": codes}, use_t=use_t)
        return res.params[0], res.tvalues[0], res

    # actual (unrestricted) estimate
    b, t_obs, res_u = fit_t(yv)

    # Step 1: restricted fit, treatment coefficient forced to zero
    res_r = sm.OLS(yv, X_r).fit()
    y_tilde, u_tilde = res_r.fittedvalues, res_r.resid

    # Step 2: all 2^G Rademacher vectors, one weight per cluster
    W = np.array(list(itertools.product([-1.0, 1.0], repeat=G)))   # (2^G, G)

    # Steps 3-4: synthetic outcome, re-estimate unrestricted model, store cluster-robust t*
    t_star = np.empty(len(W))
    for k, w in enumerate(W):
        y_star = y_tilde + w[codes] * u_tilde
        t_star[k] = fit_t(y_star)[1]

    # Step 5: share of |t*| >= |t| (tolerance because w = +1 and w = -1 reproduce |t| up to rounding)
    p_boot = np.mean(np.abs(t_star) >= abs(t_obs) - 1e-8)

    p_norm = float(res_u.pvalues[0])                      # cluster-robust t, normal reference
    p_tG1 = float(fit_t(yv, use_t=True)[2].pvalues[0])    # cluster-robust t, t(G-1) reference
    return {"coef": b, "se_cluster": res_u.bse[0], "t": t_obs, "G": G, "n_vectors": len(W),
            "p_boot": p_boot, "p_cluster_normal": p_norm, "p_cluster_t_Gm1": p_tG1, "t_star": t_star}


def _toy_panel(effect: float = 2.0, seed: int = 0) -> pd.DataFrame:
    """8 boards x 5 counties x 12 years, constant true effect, one never-treated board."""
    rng = np.random.default_rng(seed)
    start = np.array([3, 3, 4, 4, 5, 6, 6, NEVER])
    shock = rng.normal(0, 0.5, (8, 12))
    level = rng.normal(0, 2, 40)
    noise = rng.normal(0, 0.8, (40, 12))
    county = np.repeat(np.arange(40), 12)
    year = np.tile(np.arange(12), 40)
    board = county // 5
    g = start[board]
    D = (year >= g).astype(int)
    y = 50 + level[county] + 0.5 * year + shock[board, year] + effect * D + noise.ravel()
    return pd.DataFrame({"county": county, "board": board, "g": g, "t": year,
                         "year": year, "D": D, "y": y})


if __name__ == "__main__":
    toy = _toy_panel()

    tiny = pd.DataFrame({"y": [1, 3, 2, 3], "tr": [1, 1, 0, 0], "post": [0, 1, 0, 1]})
    assert two_by_two(tiny, "y", "tr", "post") == 1.0                      # (3-1) - (3-2)

    cells, att = clean_att(toy)
    assert cells["n"].sum() == (toy["D"] == 1).sum()                       # every treated county-year once
    assert abs(att - 2.0) < 1.0                                            # truth is 2.0

    es = event_study(cells.assign(e=cells["t"] - cells["g"]))
    assert list(es["e"]) == list(range(0, 9))

    pc = pre_cells(toy, "t", "y", "g", "county")
    assert (pc["e"] <= -2).all() and pc["att"].abs().max() < 2

    f_default = twfe_fit(toy, "y", "D", "county", "year")
    f_board = twfe_fit(toy, "y", "D", "county", "year", cluster="board")
    assert f_board.n_groups == 8
    assert abs(f_board.params["D"] - f_default.params["D"]) < 1e-8         # only the SE changes
    assert f_board.bse["D"] > 0

    bs = wild_cluster_bootstrap(toy, cluster="board", y="y", treat="D", unit="county", time="year")
    assert abs(bs["coef"] - f_board.params["D"]) < 1e-8
    assert abs(bs["t"] - f_board.tvalues["D"]) < 1e-6                      # same CR1 t statistic
    assert bs["n_vectors"] == 256 and 0 <= bs["p_boot"] <= 1
    assert np.allclose(bs["t_star"], -bs["t_star"][::-1])                  # w and -w: opposite t*

    print("did_toolkit: all assertions pass")
