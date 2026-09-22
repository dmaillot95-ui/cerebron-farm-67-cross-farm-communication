"""BUILD-044 — SAPHEA Academy: hierarchical books/chapters/lessons for micro-model students."""
import hashlib, json
BOOKS={
"RDI_FOUNDATIONS":{
"title":"Fondations scientifiques et R&D industrielle",
"chapters":[
{"id":"C01","title":"Unités, dimensions et ordres de grandeur","prereq":[],"sections":["SI et conversions","Analyse dimensionnelle","Ordres de grandeur","Chiffres significatifs"]},
{"id":"C02","title":"Équations et calcul scientifique","prereq":["C01"],"sections":["Variables et hypothèses","Calcul symbolique","Calcul numérique","Vérification indépendante"]},
{"id":"C03","title":"Mécanique, énergie et puissance","prereq":["C01","C02"],"sections":["Force et couple","Vitesse angulaire","Travail et énergie","Puissance et rendement"]},
{"id":"C04","title":"Preuve, évidence et inconnues","prereq":["C02"],"sections":["GIVEN vs DERIVED","UNKNOWN","Claim ceiling","Contre-exemple et falsification"]},
{"id":"C05","title":"Ingénierie et exigences","prereq":["C03","C04"],"sections":["Besoin et exigence","Marges","Modes de défaillance","Qualification"]},
{"id":"C06","title":"Modélisation et simulation","prereq":["C02","C04"],"sections":["Modèle et réalité","Hypothèses","Simulation","Validation et domaine de validité"]},
{"id":"C07","title":"Recherche et provenance","prereq":["C04"],"sections":["État de l'art","Sources","Conflits de sources","Traçabilité"]},
{"id":"C08","title":"Invention et architecture","prereq":["C05","C06","C07"],"sections":["Alternatives","Contraintes","Novelty funnel","Ablation"]},
{"id":"C09","title":"Industrialisation","prereq":["C05"],"sections":["Fabrication","Coût","Essais","Production et field data"]},
{"id":"C10","title":"Fusion CÉRÉBRON","prereq":["C04","C06","C07"],"sections":["Déduplication","Contradictions","Residual gap","Audit et décision"]}
]}}
def chapter(book,cid):
    c=next(x for x in BOOKS[book]["chapters"] if x["id"]==cid)
    raw=json.dumps(c,sort_keys=True,ensure_ascii=False)
    return {**c,"book":book,"status":"TEACH_NOT_MASTERED","provenance":hashlib.sha256(raw.encode()).hexdigest()}
def lesson_packet(book,cid,section,explanation,examples,errors,glyph):
    c=chapter(book,cid)
    if section not in c["sections"]: raise ValueError("unknown section")
    return {"book":book,"chapter":cid,"section":section,"explanation":explanation,
      "worked_examples":examples,"common_errors":errors,"glyph_summary":glyph,
      "student_actions":["STUDY","EXPLAIN_BACK","PRACTICE","ASK_IF_BLOCKED","UNSEEN_EXAM"],
      "status":"TEACH_NOT_MASTERED","chapter_provenance":c["provenance"]}
def next_action(passed,question=None):
    if question: return "GPT_MENTOR_REQUIRED"
    return "AUDITOR_REQUIRED" if passed else "RETEACH_OR_QUESTION"
RULES=["BOOK!=MASTERY","CHAPTER!=MASTERY","READING!=LEARNING","EXPLAIN_BACK_REQUIRED",
"UNSEEN_EXAM_REQUIRED","QUESTION_BEFORE_HALLUCINATION","AUDITOR_REQUIRED","MASTERED_ONLY_TO_VALIDATED_MEMORY"]
