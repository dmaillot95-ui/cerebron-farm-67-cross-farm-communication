#!/usr/bin/env python3
"""BUILD-007 model adapter. Real inference only when --execute-model is explicitly supplied."""
import argparse, json, pathlib, sys

CFG=pathlib.Path(__file__).resolve().parents[1]/"config/saphea-rd01-model.json"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--prompt",default="A steel part has mass 10 kg and specific heat 500 J/(kg K). Estimate the energy needed for a 20 K temperature rise. State assumptions and units.")
    ap.add_argument("--execute-model",action="store_true")
    ap.add_argument("--max-new-tokens",type=int,default=256)
    a=ap.parse_args()
    cfg=json.loads(CFG.read_text())
    if not a.execute_model:
        print(json.dumps({"status":"MODEL_NOT_EXECUTED","model_id":cfg["model_id"],"transport":"SEPARATE"},indent=2)); return
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
    except Exception as e:
        raise SystemExit("MODEL_RUNTIME_UNAVAILABLE:"+repr(e))
    mid=cfg["model_id"]
    tok=AutoTokenizer.from_pretrained(mid)
    model=AutoModelForCausalLM.from_pretrained(mid,torch_dtype="auto",device_map="auto")
    messages=[{"role":"system","content":"You are SAPHEA-R&D-01, an industrial R&D student. State assumptions, units, uncertainty, and never claim verification you did not perform."},
              {"role":"user","content":a.prompt}]
    text=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
    inp=tok([text],return_tensors="pt").to(model.device)
    out=model.generate(**inp,max_new_tokens=a.max_new_tokens,do_sample=False)
    answer=tok.decode(out[0][inp.input_ids.shape[1]:],skip_special_tokens=True)
    print(json.dumps({"status":"UNREVIEWED_MODEL_OUTPUT","model_id":mid,"answer":answer},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
