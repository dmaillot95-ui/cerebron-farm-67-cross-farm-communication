"""BUILD-035 — Distributed Foundry specialization planner.
Clone logical SAPHEA profiles by useful farm specialty; max 3 sub-agents per farm.
Planning/routing only: clone != execution.
"""
import hashlib
FARMS={
 "44-routing":["ROUTE","CAPABILITY_MATCH","BUDGET"],
 "45-runtime":["EXECUTE","TRACE","LIFECYCLE"],
 "59-learning":["EVALUATE_DELTA","ABLATE","REGRESSION"],
 "66-knowledge":["RETRIEVE","PROVENANCE","DEDUP"],
 "67-communication":["DISPATCH","AGORA","COLLECT"],
 "68-experiment":["DESIGN_EXPERIMENT","ORCHESTRATE","STOP_RULE"],
 "69-causal":["CAUSAL_TEST","CONFOUNDERS","COUNTERFACTUAL"],
 "70-proof":["FORMALIZE","LEMMA","PROOF_AUDIT"],
 "71-reproduction":["REPLICATE","PERTURB","TRANSFER"],
 "72-reality":["EVIDENCE_GATE","CLAIM_CEILING","CONTRADICTION"],
 "73-integration":["INTEGRATE","QUALIFY","FREEZE"],
 "74-memory":["CHECKPOINT","RESUME","CANONICAL_MEMORY"]
}
def specialize(farm,mission,max_agents=3):
    if farm not in FARMS: raise ValueError("unknown farm")
    n=max(1,min(3,max_agents))
    out=[]
    for role in FARMS[farm][:n]:
        sig=hashlib.sha256((farm+"|"+role+"|"+mission).encode()).hexdigest()
        out.append({"agent_id":"SAPHEA-"+sig[:12],"farm":farm,"specialty":role,
                    "mission":mission,"state":"CLONED_NOT_EXECUTED"})
    return out
def distribute(mission,farms=None,max_per_farm=3):
    fs=farms or list(FARMS)
    return [a for f in fs for a in specialize(f,mission,max_per_farm)]
RULES=["MAX_3_PER_FARM","CLONED!=EXECUTED","SPECIALIZE_BY_FARM","DEDUP_BEFORE_DISPATCH",
       "GLOBAL_BUDGET_REQUIRED","COLLATZ_01_07_PROTECTED","NO_SELF_PERMISSION_CHANGE"]
