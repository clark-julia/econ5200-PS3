# AI Appendix

**Model and date:** Claude Sonnet 5.5, November 5, 2026

---

## Version 1 prompt

Act as the state agency's lead econometrician. You believe the programme works and you are reading an external review that says your TWFE estimate is uninformative.

**[Request]** Here is the reviewer's paragraph on parallel trends and identification:

> I originally left out e=-1 because it is the baseline year for every cell. Each coefficient measures the change relative to that year, so including it would shift all the estimates. The pre-treatment estimates range from 0.03 to 0.85, which are fairly small. with only eight boards sharing shocks, differences this size could easily be due to noise alone, so they don't really support or go against parallel trends. After adoption, the estimates increase with exposure and follow the true effect pattern, rising from 1,4 at e-0 to 26.6 at e=8. The later estiamtes are less precise because they are based on only one to three boards. Overall, the flat pre-trends are consistent with parallel trends, but they don't prove the assumption. We cannot observe what adopting boards would have done without the program after adoption. We also have to assume boards did not choose when to adopt based on expected outcomes. The pre-treatment estimates help make the assumption more or less believeable, but cannot confirm it.

Give the three strongest objections you would raise in a written response.

**[Evaluate]** Rank them by how much damage each does to the reviewer's conclusion.

### Reply

**1. The reviewer's own estimator is validated only by a benchmark that real data can't supply.**
The paragraph says the estimates "follow the true effect pattern." That is only knowable in a simulation. With real data there is no true path, and the reviewer admits the pre-period can't confirm parallel trends. So nothing in this paragraph shows the event-study estimate is more credible than ours. The same caveats (unobservable untreated outcomes, possible strategic timing) apply to it, so "can't be proven" can't be used to call only our estimate uninformative.

**2. The late estimates, the headline of the reviewer's result, rest on almost nothing.**
By the reviewer's own account, the later estimates use only one to three boards. Every late cell is compared against a single never-treated board, so one unusual control path could drive the whole rise to 26.6. The composition also shifts as boards drop out of the panel, so part of the rise may reflect which boards are observed rather than exposure. "Less precise" is also never quantified, since no standard errors are reported. An estimator this fragile at its endpoints can't be the benchmark that tells us our estimate is uninformative.

**3. "Fairly small" and "noise alone" are asserted, not shown.**
No standard errors are given for the pre-period cells, so there is no basis for saying noise explains them. The size claim is also relative to the wrong comparison. Deviations up to 0.85 look small next to 26.6, but the first post-period estimate is only 1.4. Pre-period wobble of that size is more than half the effect at adoption. The reviewer then argues that eight boards give too little power to learn anything, which undercuts the earlier claim that the deviations are just noise.

A note on how the reviewer will likely respond: objection 1 is the one they can best rebut. Their case against TWFE rests on the decomposition, which shows bias from forbidden comparisons even if parallel trends hold. So the identification caveat doesn't carry their conclusion. I ranked it first because it does the most damage if the reviewer leans on this paragraph. Objections 2 and 3 are harder to answer, but they only weaken the event-study evidence, not the decomposition argument.

---

## Version 2 prompt

Some context of this is:

The reviewer argues that the agency's two-way fixed effects (TWFE) estimate can't recover the programme's true effect. The paragraph below isn't about that estimate, though. It interprets an event study built with a different method: each adopting group is compared with boards that haven't adopted yet, and every change is measured from the last year before adoption. The data cover counties by year, with eight boards of five counties each that adopt in different years, plus one board that never adopts. Be specific and more concise about the three strongest objections to the argument. Say which part you disagree with, state why and say what the reviewer would have had to show.

### Reply

**Objection 1: The noise scale undercuts the reviewer.**
*Quote:* "with only eight boards sharing shocks, differences this size could easily be due to noise alone, so they don't really support or go against parallel trends"
*Problem:* This sets 0.85 as the scale of noise, yet the post-adoption estimates climb from 1.4 to 26.6, about 30 times larger. If the noise claim is right, differential trends can't explain the post-period. If it's wrong, "small" and "noise" are unsupported.
*Reviewer must show:* Pre-period standard errors or intervals, and a plausible violation of parallel trends that starts at adoption and grows to about 26 units.

**Objection 2: "Not proven" proves nothing specific.**
*Quote:* "flat pre-trends are consistent with parallel trends, but they don't prove the assumption"
*Problem:* This applies to every difference-in-differences estimate, names no violation here, and concerns a different estimator than the TWFE estimate under dispute.
*Reviewer must show:* A concrete reason these boards' untreated paths would diverge after adoption, and how that assumption bears on TWFE's identification.

**Objection 3: The late estimates are too thin to carry the argument.**
*Quote:* "The later estimates are less precise because they are based on only one to three boards."
*Problem:* The paragraph treats the rise to 26.6 as proof the estimator works, yet the endpoint rests on one to three boards, each compared with a single never-treated control. The rise may reflect which boards are observed, not exposure. "Less precise" is never quantified.
*Reviewer must show:* Standard errors for the late cells, and results with a balanced set of boards at each exposure length.

**Ranking by damage:**

1. **Objection 1 (noise scale).** It turns the reviewer's own model against them. If 0.85 is noise, it can't explain a rise to 26.6. If it isn't, "small" and "noise" are unsupported. Only new evidence answers it.
2. **Objection 3 (thin late estimates).** It also needs new evidence (standard errors, balanced boards), but it only weakens the event-study evidence, not the wider claim.
3. **Objection 2 ("not proven").** The reviewer can fall back on the burden of proof, since the caveat holds for any difference-in-differences estimate.
