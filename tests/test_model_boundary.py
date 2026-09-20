import json, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=subprocess.run(["python",str(ROOT/"worker/saphea_model_adapter.py")],text=True,capture_output=True,check=True)
obj=json.loads(p.stdout)
assert obj["status"]=="MODEL_NOT_EXECUTED"
assert obj["transport"]=="SEPARATE"
cfg=json.loads((ROOT/"config/saphea-rd01-model.json").read_text())
assert cfg["status"]=="CANDIDATE_NOT_EXECUTED"
assert cfg["evidence_ceiling"].startswith("E0")
print("SAPHEA_BUILD_007_BOUNDARY_PASS")
