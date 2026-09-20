import json, pathlib, subprocess, tempfile, shutil

ROOT=pathlib.Path(__file__).resolve().parents[1]
RUNTIME=ROOT/"worker/agora_runtime.py"
def run(*args,cwd):
    return subprocess.run(["python",str(RUNTIME),*args],cwd=cwd,text=True,capture_output=True,check=True)

with tempfile.TemporaryDirectory() as td:
    d=pathlib.Path(td)
    run("post","--id","MSG-RD-0001","--mission","MISSION-RD-0001","--source","SAPHEA-RD-01",
        "--target","AGORA","--role","R&D","--type","REQUEST","--claim","test mission",
        "--evidence","synthetic-test","--provenance","BUILD-002",cwd=d)
    run("read","--id","MSG-RD-0001",cwd=d)
    run("claim","--id","MSG-RD-0001","--actor","SAPHEA-S0",cwd=d)
    run("answer","--id","MSG-RD-0001","--actor","SAPHEA-RD-01","--note","candidate result",cwd=d)
    run("audit","--id","MSG-RD-0001","--actor","AUDITOR-01","--note","synthetic audit passed",cwd=d)
    run("close","--id","MSG-RD-0001","--actor","CEREBRON","cwd=d)
    obj=json.loads((d/"agora/messages/MSG-RD-0001.json").read_text())
    assert [x["status"] for x in obj["HISTORY"]]==["POSTED","CLAIMED","ANSWERED","AUDITED","CLOSED"]
    assert obj["STATUS"]=="CLOSED" and len(obj["HASH"])==64
print("AGORA_BUILD_002_PASS")
