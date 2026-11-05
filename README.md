# econ5200-PS3
# Diagnosing Experimental Failures in A/B Testing

## Objective

I diagnosed and fixed several ways an A/B test can give misleading results, covering variance reduction, sample ratio mismatch, interference between users, Bayesian decision rules, and peeking.

## Methodology

- Found and fixed three bugs in an analyst's CUPED (variance reduction) code, then compared the variance reduction and standard error before and after my fixes.
- Ran sample ratio mismatch tests on two experiments, one with 100,000 users and one with 20 million, and compared the chi-squared statistics.
- Simulated a marketplace where discounted buyers take inventory from the control group, then compared the A/B test's naive ATE with the effect of rolling the discount out to everyone.
- Ran a Bayesian A/B test, computed P(B > A) and the expected loss of shipping B, applied the ship rule, and checked the result against a permutation test.
- Wrote my own function for the Bayesian test and used it on a test with four times the users.
- Simulated peeking by running 1,000 experiments with no true effect and testing at 50 points in each, then compared against a single test at the end.
- (Challenge) Applied CUPED to the LaLonde job training data, using re74 and re75 as covariates.

## Key Findings

- **CUPED bugs:** The analyst reported a [YOUR VALUE]% variance reduction. After my fixes it was [YOUR VALUE]%, and the standard error fell from [YOUR VALUE] to [YOUR VALUE].
- **Sample ratio mismatch:** A [YOUR VALUE] pp imbalance among 100,000 users gave a chi-squared of [YOUR VALUE]. A [YOUR VALUE] pp imbalance among 20 million users gave [YOUR VALUE].
- **Interference:** The naive ATE was [YOUR VALUE], against [YOUR VALUE] for rolling the discount out to everyone. The A/B test overstated the effect by [YOUR VALUE]% of the naive estimate.
- **Bayesian test:** P(B > A) was [YOUR VALUE] and the expected loss of shipping B was [YOUR VALUE], so the ship rule said [YOUR VALUE]. The permutation test gave p = [YOUR VALUE].
- **Larger test:** With four times the users, my own function gave P(B > A) = [YOUR VALUE].
- **Peeking:** [YOUR VALUE]% of the 1,000 no-effect experiments crossed p < 0.05 at least once across the 50 looks, against [YOUR VALUE]% with a single test at the end.
- **Challenge (LaLonde):** Adding re74 and re75 as covariates cut the variance by [YOUR VALUE]%.
