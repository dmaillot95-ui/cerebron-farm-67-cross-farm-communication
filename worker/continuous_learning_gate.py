"""BUILD-029 — Continuous Learning Gate.
Validated deltas may enter memory/dataset; no output self-promotes and no automatic weight update.
"""
ALLOWED={"VERIFIED","CANDIDATE","UNKNOWN","REJECTED","CONTRADICTORY"}
def classify(item,status,evidence=None,auditor=None):
    if status not in ALLOWED: raise ValueError("status")
    x=dict(item); x.update(status=status,evidence=evidence or [],auditor=auditor)
    return x
def learning_gate(x):
    if x["status"]!="VERIFIED": return {"decision":"HOLD","reason":"NOT_VERIFIED"}
    if not x["evidence"]: return {"decision":"HOLD","reason":"NO_EVIDENCE"}
    if not x["auditor"]: return {"decision":"HOLD","reason":"NO_AUDITOR"}
    return {"decision":"PROMOTE_TO_VALIDATED_DATASET","reason":"EVIDENCE_AND_AUDIT"}
def training_candidate(x, benchmark_before=None, benchmark_after=None):
    g=learning_gate(x)
    if g["decision"]!="PROMOTE_TO_VALIDATED_DATASET": return {"decision":"NO_TRAIN"}
    if benchmark_before is None or benchmark_after is None: return {"decision":"DATASET_ONLY","reason":"BENCHMARK_REQUIRED"}
    return {"decision":"ACCEPT_DELTA" if benchmark_after>benchmark_before else "ROLLBACK_DELTA",
            "before":benchmark_before,"after":benchmark_after}
RULES=["GPT_OUTPUT!=TRUTH","MEMORY!=LEARNING","DATASET!=WEIGHT_UPDATE","NO_SELF_PROMOTION",
       "BENCHMARK_BEFORE_AFTER","ROLLBACK_IF_REGRESSION","HUMAN_REVIEW_FOR_MAJOR_PROMOTION"]
