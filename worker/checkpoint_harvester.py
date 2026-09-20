"""BUILD-030 — Checkpoint Harvester.
Converts research checkpoints into compact candidate deltas; never self-validates them.
"""
import hashlib,json,re
VALID={"VERIFIED","CANDIDATE","UNKNOWN","REJECTED","CONTRADICTORY"}
def _clean(s,n=240): return re.sub(r"\s+"," ",str(s)).strip()[:n]
def harvest(source,checkpoint,claims,gaps,failures,provenance):
    deltas=[]
    for kind,items,status in [
        ("CLAIM",claims,"CANDIDATE"),("GAP",gaps,"UNKNOWN"),("FAILURE",failures,"REJECTED")]:
        for i,x in enumerate(items):
            value=_clean(x)
            raw=f"{source}|{checkpoint}|{kind}|{value}|{provenance}"
            deltas.append({"id":hashlib.sha256(raw.encode()).hexdigest()[:16],
                           "kind":kind,"value":value,"status":status,
                           "source":source,"checkpoint":checkpoint,"provenance":provenance})
    return deltas
def glyph(d):
    tag={"CLAIM":"C","GAP":"G","FAILURE":"F"}[d["kind"]]
    st={"VERIFIED":"V","CANDIDATE":"C","UNKNOWN":"U","REJECTED":"X","CONTRADICTORY":"!"}[d["status"]]
    return f"⟦Δ|{tag}{st}|{d['id']}|{d['value']}|π={d['provenance']}⟧"
def export_packet(deltas):
    return {"schema":"CEREBRON_CHECKPOINT_DELTA_V1","deltas":deltas,
            "rules":["HARVEST!=VALIDATION","GPT_OUTPUT!=TRUTH","DEDUP_BEFORE_REASONING","LEARNING_GATE_REQUIRED"]}
