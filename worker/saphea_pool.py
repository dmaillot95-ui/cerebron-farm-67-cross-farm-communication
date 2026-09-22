import json,hashlib
ROLES={
 "SAPHEA-SCIENCE":{"role":"science_engineering","focus":["physics","equations","units"]},
 "SAPHEA-REDTEAM":{"role":"red_team","focus":["counterexample","assumptions","failure"]},
 "SAPHEA-FUSION":{"role":"fusion","focus":["compare","residual","decision"]},
}
def packet(role,mission,model="Qwen/Qwen3-1.7B"):
    assert role in ROLES
    body={"saphea_id":role,"logical_role":ROLES[role],"shared_physical_model":model,
          "mission":mission,"status":"ROUTED_NOT_EXECUTED",
          "rules":["AGENT_LOGIQUE!=MODELE_INDEPENDANT","SAME_MODEL!=INDEPENDENT_EVIDENCE","NO_SELF_CERTIFICATION"]}
    body["packet_hash"]=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()
    return body
if __name__=="__main__":
 import sys
 mission=sys.argv[1] if len(sys.argv)>1 else "industrial R&D mission"
 print(json.dumps([packet(r,mission) for r in ROLES],ensure_ascii=False,indent=2))
