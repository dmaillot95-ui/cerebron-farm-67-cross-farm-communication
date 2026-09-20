import json, pathlib, subprocess, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
ADAPTER=ROOT/"worker/saphea_rd01.py"
RUNTIME=ROOT/"worker/agora_runtime.py"

with tempfile.TemporaryDirectory() as td:
    subprocess.run(["python",str(ADAPTER),"--workspace",td],check=True,text=True,capture_output=True)
    p=pathlib.Path(td)/"agora/messages/MSG-SAPHEA-0001.json"
    obj=json.loads(p.read_text())
    assert obj["SOURCE"]=="SAPHEA-RD-01"
    assert obj["MISSION_ID"]=="MISSION-RD-0002"
    assert [e["status"] for e in obj["HISTORY"]]==["POSTED","CLAIMED","ANSWERED"]
    subprocess.run(["python",str(RUNTIME),"audit","--id","MSG-SAPHEA-0001","--actor","AUDITOR-01",
                    "--note","transport-only audit"],cwd=td,check=True,capture_output=True,text=True)
    subprocess.run(["python",str(RUNTIME),"close","--id","MSG-SAPHEA-0001","--actor","CEREBRON"],
                   cwd=td,check=True,capture_output=True,text=True)
    obj=json.loads(p.read_text())
    assert obj["STATUS"]=="CLOSED"
    assert [e["status"] for e in obj["HISTORY"]]==["POSTED","CLAIMED","ANSWERED","AUDITED","CLOSED"]
print("SAPHEA_AGORA_BUILD_005_PASS")
