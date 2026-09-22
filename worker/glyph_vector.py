"""BUILD-025 — SPIRALIX / GLYPH-VECTOR inter-SAPHEA protocol.
Compact factual packets. Encoding is transport, never evidence.
"""
import json, hashlib

VERSION="GV1"
ALLOWED={"GIVEN","DERIVED","CLAIM","CONTRADICTION","UNKNOWN","RESIDUAL","REJECTED"}
def packet(role, facts, provenance):
    clean=[]
    for f in facts:
        if f["kind"] not in ALLOWED: raise ValueError("invalid kind")
        clean.append({k:f[k] for k in ("kind","key","value","unit") if k in f})
    body={"v":VERSION,"role":role,"facts":clean,"prov":provenance,
          "rules":["GLYPH_VECTOR!=EVIDENCE","UNKNOWN_STAYS_UNKNOWN","NO_SELF_CERTIFICATION"]}
    raw=json.dumps(body,sort_keys=True,separators=(",",":"))
    body["sha256"]=hashlib.sha256(raw.encode()).hexdigest()
    return body

def compact(p):
    # Machine-facing SPIRALIX glyph transport, intentionally not natural-language prose.
    tags={"GIVEN":"G","DERIVED":"D","CLAIM":"C","CONTRADICTION":"X",
          "UNKNOWN":"U","RESIDUAL":"R","REJECTED":"!"}
    fs=[]
    for f in p["facts"]:
        fs.append(tags[f["kind"]]+":"+f["key"]+"="+str(f["value"])+(("@"+f["unit"]) if f.get("unit") else ""))
    return "⟦"+p["role"]+"|"+(";".join(fs))+"|π="+p["sha256"][:12]+"⟧"
