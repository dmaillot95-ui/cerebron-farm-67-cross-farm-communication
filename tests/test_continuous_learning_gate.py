import sys;sys.path.insert(0,"worker")
from continuous_learning_gate import *
u=classify({"claim":"x"},"UNKNOWN")
assert learning_gate(u)["decision"]=="HOLD"
v=classify({"claim":"verified-result"},"VERIFIED",["tool-check","provenance"],"independent-auditor")
assert learning_gate(v)["decision"]=="PROMOTE_TO_VALIDATED_DATASET"
assert training_candidate(v)["decision"]=="DATASET_ONLY"
assert training_candidate(v,10,12)["decision"]=="ACCEPT_DELTA"
assert training_candidate(v,12,10)["decision"]=="ROLLBACK_DELTA"
assert "GPT_OUTPUT!=TRUTH" in RULES and "NO_SELF_PROMOTION" in RULES
print("SAPHEA_BUILD_029_CONTINUOUS_LEARNING_GATE_PASS")
