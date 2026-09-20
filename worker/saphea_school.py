"""BUILD-038 SAPHEA SCHOOL — mentor/student curriculum state machine."""
from dataclasses import dataclass,asdict
CURRICULUM=[
("L01","UNITS","Convert rpm to rad/s and preserve dimensions."),
("L02","MECH_POWER","Use P=tau*omega only with defined torque/speed."),
("L03","EVIDENCE","Separate computed fact from adequacy claim."),
("L04","UNKNOWN","Ask a precise mentor question instead of inventing missing data."),
("L05","GLYPH","Return compact GIVEN/DERIVED/UNKNOWN/QUESTION evidence.")
]
@dataclass
class LessonState:
    student:str; lesson:str; status:str="STUDY"; attempts:int=0
def next_action(state, answer="", deterministic_pass=False, question=""):
    state.attempts+=1
    if question.strip():
        state.status="MENTOR_QUESTION"
        return {"state":asdict(state),"action":"MENTOR_ANSWER_REQUIRED","question":question.strip()}
    if deterministic_pass:
        state.status="MASTERED"
        return {"state":asdict(state),"action":"ADVANCE"}
    state.status="RETRY_AFTER_CORRECTION"
    return {"state":asdict(state),"action":"MENTOR_CORRECT_THEN_RETRY","student_answer":answer}
RULES=["READING!=LEARNING","CORRECTION!=MASTERY","PASS_ON_UNSEEN_EXERCISE","QUESTION_BEFORE_HALLUCINATION","DETERMINISTIC_CHECK_WHEN_AVAILABLE","ONLY_MASTERED_ADVANCES"]
