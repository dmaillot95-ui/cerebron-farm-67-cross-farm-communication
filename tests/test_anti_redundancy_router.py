import sys;sys.path.insert(0,"worker")
from anti_redundancy_router import *
q="Is actuator adequacy demonstrated?"
tasks=[
 {"agent":"SCIENCE","lane":"DERIVE","question":q},
 {"agent":"SCIENCE2","lane":"DERIVE","question":q},
 {"agent":"REDTEAM","lane":"FALSIFY","question":q},
 {"agent":"AUDIT","lane":"VERIFY","question":q},
 {"agent":"GAP","lane":"SEARCH_GAP","question":q},
 {"agent":"FUSION","lane":"FUSE","question":q}]
r,m=route(tasks)
assert len(r)==5 and len(m)==1 and forbid_same_question_same_lane(r)
assert {x["lane"] for x in r}==set(LANES)
print({"routed":len(r),"merged_duplicates":len(m),"lanes":[x["lane"] for x in r]})
print("SAPHEA_BUILD_028_ANTI_REDUNDANCY_ROUTER_PASS")
