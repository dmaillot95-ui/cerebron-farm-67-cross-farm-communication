import sys;sys.path.insert(0,"worker")
from reasoning_dedup import *
N=[
 {"s":"KNOWLEDGE","k":"force","v":"36 kN","st":"CANDIDATE","p":"a"},
 {"s":"KNOWLEDGE","k":"Force","v":"36kN","st":"VERIFIED","p":"b"},
 {"s":"GAP","k":"adequacy","v":"missing required load","st":"UNKNOWN","p":"c"},
 {"s":"ACTION","k":"adequacy","v":"check required load","st":"CANDIDATE","p":"d"}]
k,r=deduplicate(N)
assert len(k)==3 and len(r)==1
assert any(x["st"]=="VERIFIED" and x["k"]=="Force" for x in k)
tasks=reasoning_tasks(N)
assert len([x for x in tasks if x["k"].lower()=="adequacy"])==1
print({"kept":len(k),"redundant":len(r),"reasoning_slots":len(tasks)})
print("SAPHEA_BUILD_027_REASONING_DEDUP_PASS")
