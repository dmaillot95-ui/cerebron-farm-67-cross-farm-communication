"""BUILD-031 — SAPHEA FOUNDRY.
Creates auditable agent execution packets. Creation != execution; execution requires a real model call.
"""
import hashlib,json,uuid
LANES={"DERIVE","FALSIFY","VERIFY","SEARCH_GAP","FUSE","RESEARCH","COMPUTE"}
def forge(mission,lane,role,model,tools=None,budget_tokens=160):
    if lane not in LANES: raise ValueError("lane")
    seed=f"{mission}|{lane}|{role}|{model}"
    aid="SAPHEA-"+hashlib.sha256(seed.encode()).hexdigest()[:12]
    return {"agent_id":aid,"mission":mission,"lane":lane,"role":role,"model":model,
            "tools":tools or [],"budget_tokens":budget_tokens,"state":"FORGED_NOT_EXECUTED",
            "rules":["AGENT!=MODEL","FORGED!=EXECUTED","SAME_MODEL!=INDEPENDENT_EVIDENCE",
                     "NO_SELF_PERMISSION_CHANGE","NO_SELF_CERTIFICATION"]}
def execution_record(agent,output,run_id):
    if not run_id or output is None: raise ValueError("execution proof required")
    raw=json.dumps(output,sort_keys=True) if not isinstance(output,str) else output
    return {**agent,"state":"EXECUTED","run_id":str(run_id),
            "output_sha256":hashlib.sha256(raw.encode()).hexdigest(),"output":output}
def forge_distinct(mission,specs,model):
    seen=set(); agents=[]
    for role,lane in specs:
        key=(mission.strip().lower(),lane)
        if key in seen: continue
        seen.add(key); agents.append(forge(mission,lane,role,model))
    return agents
