import sys;sys.path.insert(0,"worker")
from mentor_question_queue import *
q=create_question("SAPHEA","M02",1,"Why convert rpm before P=tau*omega?")
assert q["status"]=="GPT_MENTOR_REQUIRED" and q["mentor_answer"] is None
a=attach_mentor_answer(q,"Because omega in P=tau*omega is angular velocity in rad/s; rpm must be converted consistently.")
assert a["status"]=="MENTOR_ANSWERED_RETRY_REQUIRED"
r=attach_retry(a,"omega=rpm*2*pi/60; then P=tau*omega")
assert r["status"]=="RETRY_SUBMITTED_AUDIT_REQUIRED"
print("SAPHEA_BUILD_041_MENTOR_QUESTION_QUEUE_PASS")
