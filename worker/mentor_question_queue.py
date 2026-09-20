"""BUILD-041 — Mentor Question Queue.
Persists student questions for a real external mentor answer; never fabricates mentor replies.
"""
import json,hashlib,datetime
def create_question(student,lesson,attempt,question,context=""):
    q=question.strip()
    if not q: raise ValueError("question required")
    body=f"{student}|{lesson}|{attempt}|{q}|{context}"
    return {"question_id":"MQ-"+hashlib.sha256(body.encode()).hexdigest()[:16],
            "student":student,"lesson":lesson,"attempt":attempt,"question":q,
            "context":context,"status":"GPT_MENTOR_REQUIRED",
            "mentor_answer":None,"student_retry":None}
def attach_mentor_answer(record,answer,mentor="GPT_MENTOR"):
    if record["status"]!="GPT_MENTOR_REQUIRED": raise ValueError("not awaiting mentor")
    if not answer.strip(): raise ValueError("real mentor answer required")
    record=dict(record); record["mentor_answer"]=answer.strip(); record["mentor"]=mentor
    record["status"]="MENTOR_ANSWERED_RETRY_REQUIRED"; return record
def attach_retry(record,retry):
    if record["status"]!="MENTOR_ANSWERED_RETRY_REQUIRED": raise ValueError("mentor answer missing")
    record=dict(record); record["student_retry"]=retry; record["status"]="RETRY_SUBMITTED_AUDIT_REQUIRED"; return record
RULES=["NO_FAKE_MENTOR_REPLY","QUESTION_PERSISTS_UNTIL_ANSWERED","MENTOR_ANSWER!=MASTERY",
       "RETRY_REQUIRED","AUDIT_REQUIRED","PROVENANCE_REQUIRED"]
