#!/usr/bin/env python3
"""SAPHEA-R&D-01 deterministic adapter prototype.
No LLM/model call: proves only SAPHEA identity -> Agora message exchange.
"""
import argparse, json, pathlib, subprocess, sys
RUNTIME=pathlib.Path(__file__).with_name("agora_runtime.py")

def call(args,cwd=None):
    p=subprocess.run([sys.executable,str(RUNTIME),*args],cwd=cwd,text=True,capture_output=True,check=True)
    return p.stdout

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--workspace",default=".")
    ap.add_argument("--id",default="MSG-SAPHEA-0001")
    ap.add_argument("--mission",default="MISSION-RD-0002")
    a=ap.parse_args()
    common=["--id",a.id,"--mission",a.mission,"--source","SAPHEA-RD-01","--target","CEREBRON-S0",
            "--role","R&D-STUDENT","--type","RESULT","--claim","SAPHEA-RD-01 transport handshake",
            "--evidence","deterministic-adapter-test","--provenance","BUILD-005"]
    call(["post",*common],a.workspace)
    call(["claim","--id",a.id,"--actor","CEREBRON-S0","--note","routed to SAPHEA-RD-01"],a.workspace)
    call(["answer","--id",a.id,"--actor","SAPHEA-RD-01","--note","HANDSHAKE_OK"],a.workspace)
    print(call(["read","--id",a.id],a.workspace))
if __name__=="__main__": main()
