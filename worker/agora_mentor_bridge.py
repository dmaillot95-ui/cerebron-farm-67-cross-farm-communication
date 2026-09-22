"""BUILD-042 — Agora mentor bridge.
Routes unresolved student questions to mentor inbox and routes a real answer back by question_id.
Transport only; does not call or impersonate GPT.
"""
import hashlib
def to_agora(question_record):
    if question_record.get("status")!="GPT_MENTOR_REQUIRED": raise ValueError("question not mentor-ready")
    return {"kind":"MENTOR_QUESTION","question_id":question_record["question_id"],
            "student":question_record["student"],"lesson":question_record["lesson"],
            "question":question_record["question"],"context":question_record.get("context",""),
            "route":"AGORA/GPT_MENTOR","state":"QUEUED"}
def mentor_reply(question_packet,answer,mentor_id="GPT_MENTOR"):
    if question_packet.get("kind")!="MENTOR_QUESTION": raise ValueError("wrong packet")
    if not answer.strip(): raise ValueError("answer required")
    payload=f'{question_packet["question_id"]}|{mentor_id}|{answer.strip()}'
    return {"kind":"MENTOR_ANSWER","question_id":question_packet["question_id"],
            "student":question_packet["student"],"lesson":question_packet["lesson"],
            "mentor":mentor_id,"answer":answer.strip(),
            "provenance":hashlib.sha256(payload.encode()).hexdigest(),
            "route":"AGORA/STUDENT","state":"ANSWERED"}
def match(question_packet,answer_packet):
    return question_packet["question_id"]==answer_packet["question_id"] and question_packet["student"]==answer_packet["student"]
RULES=["TRANSPORT!=MENTOR","NO_SYNTHETIC_GPT_REPLY","QUESTION_ID_REQUIRED","ANSWER_PROVENANCE_REQUIRED","RETURN_TO_ORIGIN_STUDENT","ANSWER!=MASTERY"]
