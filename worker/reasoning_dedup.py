"""BUILD-027 — reasoning deduplication for Summary Tree / GLYPH-VECTOR."""
import re, hashlib
def canon(v):
    return re.sub(r"[^a-z0-9]+","",str(v).lower())
def signature(n):
    # semantic-lite deterministic key: section + concept key + normalized value
    return hashlib.sha256((n["s"]+"|"+canon(n["k"])+"|"+canon(n["v"])).encode()).hexdigest()
def deduplicate(nodes):
    rank={"VERIFIED":3,"CANDIDATE":2,"UNKNOWN":1,"REJECTED":0}
    kept={}; redundant=[]
    for n in nodes:
        sig=signature(n)
        if sig not in kept: kept[sig]=n; continue
        old=kept[sig]
        if rank[n["st"]]>rank[old["st"]]:
            redundant.append(old); kept[sig]=n
        else: redundant.append(n)
    return list(kept.values()),redundant
def reasoning_tasks(nodes):
    unique,_=deduplicate(nodes)
    # Never spend a reasoning slot twice on the same normalized concept.
    seen=set(); out=[]
    for n in unique:
        concept=canon(n["k"])
        if concept in seen: continue
        seen.add(concept); out.append(n)
    return out
