#!/usr/bin/env python3
import argparse, hashlib, json, pathlib
from datetime import datetime, timezone

ROOT=pathlib.Path("agora/messages")
ALLOWED={"POSTED","CLAIMED","ANSWERED","AUDITED","CLOSED"}

def now(): return datetime.now(timezone.utc).isoformat()
def load(mid):
    p=ROOT/f"{mid}.json"
    if not p.exists(): raise SystemExit(f"UNKNOWN_MESSAGE:{mid}")
    return p,json.loads(p.read_text(encoding="utf-8"))
def digest(d):
    x={k:v for k,v in d.items() if k!="HASH"}
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def save(p,d):
    d["HASH"]=digest(d); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf-8")
def event(d,status,actor,note=""):
    if status not in ALLOWED: raise SystemExit("BAD_STATUS")
    d["STATUS"]=status; d["UPDATED_AT"]=now()
    d.setdefault("HISTORY",[]).append({"status":status,"actor":actor,"at":d["UPDATED_AT"],"note":note})
def post(a):
    d={"MESSAGE_ID":a.id,"MISSION_ID":a.mission,"SOURCE":a.source,"TARGET":a.target,
       "ROLE":a.role,"TYPE":a.type,"CLAIM":a.claim,"EVIDENCE":a.evidence,
       "PROVENANCE":a.provenance,"TTL":a.ttl,"CREATED_AT":now()}
    p=ROOT/f"{a.id}.json"
    if p.exists(): raise SystemExit("DUPLICATE_MESSAGE")
    event(d,"POSTED",a.source); save(p,d); print(json.dumps(d,ensure_ascii=False))
def transition(a,status):
    p,d=load(a.id); event(d,status,a.actor,getattr(a,"note","")); save(p,d); print(json.dumps(d,ensure_ascii=False))
def read(a):
    p,d=load(a.id)
    if d.get("HASH")!=digest(d): raise SystemExit("HASH_MISMATCH")
    print(json.dumps(d,indent=2,ensure_ascii=False))
def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("post")
    for x in ["id","mission","source","target","role","type","claim","evidence","provenance"]: p.add_argument(f"--{x}",required=True)
    p.add_argument("--ttl",type=int,default=3600)
    r=sp.add_parser("read"); r.add_argument("--id",required=True)
    for cmd in ["claim","answer","audit","close"]:
        q=sp.add_parser(cmd); q.add_argument("--id",required=True); q.add_argument("--actor",required=True); q.add_argument("--note",default="")
    a=ap.parse_args()
    {"post":post,"read":read,"claim":lambda x:transition(x,"CLAIMED"),"answer":lambda x:transition(x,"ANSWERED"),
     "audit":lambda x:transition(x,"AUDITED"),"close":lambda x:transition(x,"CLOSED")}[a.cmd](a)
if __name__=="__main__": main()
