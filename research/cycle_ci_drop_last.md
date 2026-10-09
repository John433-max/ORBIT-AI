# CI 37869012520 — drop_last stole last_n

SOURCE: https://github.com/John433-max/ORBIT-AI/actions/runs/37869012520
DATE: 2026-10-09
TECHNIQUE: pack-order matcher exclusion (same contract as research/cycle_matcher_steal.md)
WHAT IT IMPROVES: Tests on main after chaining p236–p239 through p235
REQUIREMENTS: p237 loaded before p209 (seen-set keeps first drop_last)
TRADE-OFFS: "drops the last n elements" stays last_n; singular "drop the last element" stays drop_last
RELEVANCE: CI 3.11 and 3.12 both failed test_p204 and test_p209
EXPECTED BENEFIT: those two assertions pass again

Failure: match_template("write a function that drops the last n elements of a list") returned drop_last (p237) instead of last_n.
Fix: p237 drop_last rejects "last n", "n element", and "n item", matching p209.
