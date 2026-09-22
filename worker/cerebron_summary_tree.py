"""BUILD-026 — CEREBRON Summary Tree -> GLYPH-VECTOR.
Small SAPHEA loads only mission-relevant branches. Summary is memory/index, not learning proof.
"""
import json, hashlib

SECTIONS=("IDENTITY","RULES","METHODS","KNOWLEDGE","TOOLS","FAILURES","SKILLS","CHECKPOINT","GAP","ACTION")
STATUS={"VERIFIED","CANDIDATE","UNKNOWN","REJECTED"}

def node(section,key,value,status="CANDIDATE",provenance=""):
    if section not in SECTIONS: raise ValueError("section")
    if status not in STATUS: raise ValueError("status")
    return {"s":section,"k":key,"v":value,"st":status,"p":provenance}

def tree(farm,role,nodes):
    body={"v":"CST1","farm":farm,"role":role,"nodes":nodes,
          "rules":["SUMMARY!=LEARNING","MEMORY!=LEARNING","ONLY_VERIFIED_PROMOTES","UNKNOWN_STAYS_UNKNOWN","PROVENANCE_REQUIRED"]}
    raw=json.dumps(body,sort_keys=True,separators=(",",":"))
    body["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
    return body

def select(t, sections):
    wanted=set(sections)
    return [n for n in t["nodes"] if n["s"] in wanted]

def glyph(t, sections):
    tags={"IDENTITY":"I","RULES":"R","METHODS":"M","KNOWLEDGE":"K","TOOLS":"T","FAILURES":"F","SKILLS":"S","CHECKPOINT":"C","GAP":"G","ACTION":"A"}
    st={"VERIFIED":"V","CANDIDATE":"C","UNKNOWN":"U","REJECTED":"X"}
    xs=[]
    for n in select(t,sections):
        xs.append(f'{tags[n["s"]]}{st[n["st"]]}:{n["k"]}={n["v"]}')
    return "⟦CST1|"+t["farm"]+"|"+(";".join(xs))+"|π="+t["sha256"][:12]+"⟧"

def promote(n,new_status,evidence_provenance):
    if new_status=="VERIFIED" and not evidence_provenance: raise ValueError("verified requires provenance")
    x=dict(n); x["st"]=new_status; x["p"]=evidence_provenance or x.get("p",""); return x
