import sys;sys.path.insert(0,"worker")
from distributed_foundry import *
mission="hard scientific residual"
agents=distribute(mission)
assert len(agents)==36
assert all(a["state"]=="CLONED_NOT_EXECUTED" for a in agents)
assert max(sum(1 for a in agents if a["farm"]==f) for f in FARMS)==3
assert {a["specialty"] for a in agents if a["farm"]=="70-proof"}=={"FORMALIZE","LEMMA","PROOF_AUDIT"}
assert "COLLATZ_01_07_PROTECTED" in RULES
print({"farms":len(FARMS),"logical_agents":len(agents),"max_per_farm":3})
print("SAPHEA_BUILD_035_DISTRIBUTED_FOUNDRY_PASS")
