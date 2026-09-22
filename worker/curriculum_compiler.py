"""BUILD-039 — curriculum compiler: compact progressive training packets."""
from hashlib import sha256
SECTIONS=[
("M01","FOUNDATIONS",["units","dimensions","significant figures"]),
("M02","CALCULATION",["equations","symbolic checks","numerical checks"]),
("M03","EVIDENCE",["given_vs_derived","unknowns","claim_ceiling"]),
("M04","REASONING",["decomposition","counterexample","falsification"]),
("M05","TOOLS",["python","sympy","tests"]),
("M06","RESEARCH",["retrieval","provenance","source_conflict"]),
("M07","ENGINEERING",["requirements","margins","failure_modes"]),
("M08","INDUSTRIAL",["manufacturing","cost","qualification"]),
("M09","INVENTION",["alternatives","novelty","ablation"]),
("M10","FUSION",["dedup","contradictions","residual_gap"])
]
def packet(module,skill,lesson,exercise):
    body=f"{module}|{skill}|{lesson}|{exercise}"
    return {"module":module,"skill":skill,"lesson":lesson,"exercise":exercise,
            "provenance":sha256(body.encode()).hexdigest(),"status":"TEACH_NOT_MASTERED"}
def promote(record, unseen_pass, deterministic_check, auditor_pass):
    ok=bool(unseen_pass and deterministic_check and auditor_pass)
    return "MASTERED" if ok else "RETRY"
RULES=["TEACHING!=MASTERY","UNSEEN_TEST_REQUIRED","AUDITOR_REQUIRED",
       "DETERMINISTIC_CHECK_WHEN_AVAILABLE","QUESTION_BEFORE_HALLUCINATION",
       "COMPRESS_BEFORE_MEMORY","MASTERED_ONLY_TO_VALIDATED_DATASET"]
