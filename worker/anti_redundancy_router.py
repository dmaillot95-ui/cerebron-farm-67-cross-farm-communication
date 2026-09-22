"""BUILD-028 — anti-redundancy router.
Assign distinct cognitive lanes; duplicate tasks are merged before model execution.
"""
import re,hashlib
LANES=("DERIVE","FALSIFY","VERIFY","SEARCH_GAP","FUSE")
def norm(s): return re.sub(r"[^a-z0-9]+","",s.lower())
def task_sig(t): return hashlib.sha256((norm(t["question"])+"|"+t["lane"]).encode()).hexdigest()
def route(tasks):
    seen=set(); out=[]; merged=[]
    for t in tasks:
        if t["lane"] not in LANES: raise ValueError("lane")
        s=task_sig(t)
        if s in seen: merged.append(t); continue
        seen.add(s); out.append({**t,"sig":s,"status":"ROUTED"})
    return out,merged
def forbid_same_question_same_lane(routed):
    keys=[(norm(x["question"]),x["lane"]) for x in routed]
    return len(keys)==len(set(keys))
