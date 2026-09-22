import sys;sys.path.insert(0,"worker")
from saphea_foundry import *
specs=[("Builder","DERIVE"),("Duplicate","DERIVE"),("Breaker","FALSIFY"),("Auditor","VERIFY"),("Gap","SEARCH_GAP"),("Fusion","FUSE")]
a=forge_distinct("test industrial claim",specs,"Qwen/Qwen3-1.7B")
assert len(a)==5 and all(x["state"]=="FORGED_NOT_EXECUTED" for x in a)
r=execution_record(a[0],"real-output-placeholder-for-contract-test","contract-test-run")
assert r["state"]=="EXECUTED" and r["output_sha256"]
assert "NO_SELF_PERMISSION_CHANGE" in r["rules"]
print({"forged":len(a),"lanes":[x["lane"] for x in a]})
print("SAPHEA_BUILD_031_FOUNDRY_CONTRACT_PASS")
