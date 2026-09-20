import json,re
REQUIRED=("PROVENANCE_FOURNIE","DEDUCTION_AUTORISEE","INCONNU","INTERDIT_D_AFFIRMER")
def enforce(answer):
    low=answer.lower()
    facts=[]
    for s in [
      "Qwen/Qwen3-1.7B","plusieurs prompts","auditeurs externes",
      "aucune modification de poids n'est demontree","aucune memoire persistante n'est demontree"]:
        if s.lower() in low: facts.append(s)
    unknown=[]
    if any(x in low for x in ["pretraining","preentrainement","fine-tuning","history","historique"]):
        unknown.append("pretraining/fine-tuning/historique exact")
    return {
      "schema":"CEREBRON_EPISTEMIC_V1",
      "PROVENANCE_FOURNIE":facts,
      "DEDUCTION_AUTORISEE":["les sorties peuvent etre auditees externement"] if "auditor" in low or "auditeur" in low else [],
      "INCONNU":unknown,
      "INTERDIT_D_AFFIRMER":["modification des poids","memoire persistante","historique d'entrainement exact"],
      "raw_model_output":answer
    }
if __name__=="__main__":
    import sys
    src=json.load(open(sys.argv[1]))
    json.dump(enforce(src["answer"]),open(sys.argv[2],"w"),ensure_ascii=False,indent=2)
