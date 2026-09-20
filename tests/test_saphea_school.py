import sys;sys.path.insert(0,"worker")
from saphea_school import *
s=LessonState("SAPHEA-QWEN","L01")
r=next_action(s,question="How do I convert rpm to rad/s?")
assert r["action"]=="MENTOR_ANSWER_REQUIRED"
s2=LessonState("SAPHEA-QWEN","L01")
r2=next_action(s2,answer="omega=1500*2*pi/60",deterministic_pass=True)
assert r2["action"]=="ADVANCE" and r2["state"]["status"]=="MASTERED"
s3=LessonState("SAPHIDE-SMOL","L02")
r3=next_action(s3,answer="300 kW",deterministic_pass=False)
assert r3["action"]=="MENTOR_CORRECT_THEN_RETRY"
print("CURRICULUM_SECTIONS",len(CURRICULUM))
print("SAPHEA_BUILD_038_SCHOOL_MENTOR_LOOP_PASS")
