"""BUILD-033 — Fractal Foundry planner.
Plans up to 10k logical workers without pretending they executed.
"""
import hashlib
def plan(root, branches, depth=2, max_agents=10000, per_parent=100):
    if max_agents<1 or per_parent<1: raise ValueError("budget")
    q=[("ROOT",root,0)]; out=[]; seen=set()
    while q and len(out)<max_agents:
        parent,mission,d=q.pop(0)
        if d>=depth: continue
        for lane,sub in branches(mission,d)[:per_parent]:
            sig=hashlib.sha256((lane+"|"+sub.strip().lower()).encode()).hexdigest()
            if sig in seen: continue
            seen.add(sig)
            aid="FRACTAL-"+sig[:12]
            out.append({"agent_id":aid,"parent":parent,"depth":d+1,"lane":lane,
                        "mission":sub,"state":"PLANNED_NOT_EXECUTED"})
            if len(out)>=max_agents: break
            q.append((aid,sub,d+1))
    return out
def execution_budget(plan,cap):
    return plan[:min(cap,len(plan))]
RULES=["PLANNED!=EXECUTED","10000_LOGICAL!=10000_PROOFS","DEDUP_BEFORE_EXECUTION",
       "GLOBAL_BUDGET_REQUIRED","STOP_LOW_MARGINAL_GAIN","NO_SELF_PERMISSION_CHANGE"]
