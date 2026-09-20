import sys;sys.path.insert(0,"worker")
from saphea_academy import *
c=chapter("RDI_FOUNDATIONS","C03"); assert c["prereq"]==["C01","C02"]
p=lesson_packet("RDI_FOUNDATIONS","C03","Vitesse angulaire",
"Convert n rpm to omega with omega=2*pi*n/60 before SI power calculations.",
["1800 rpm -> 188.496 rad/s"],["Using rpm directly in P=tau*omega"],"G:n@rpm;D:omega=2pi*n/60@rad/s")
assert p["status"]=="TEACH_NOT_MASTERED"
assert next_action(False,"Why radians per second?")=="GPT_MENTOR_REQUIRED"
assert next_action(True)=="AUDITOR_REQUIRED"
print("SAPHEA_BUILD_044_ACADEMY_PASS")
