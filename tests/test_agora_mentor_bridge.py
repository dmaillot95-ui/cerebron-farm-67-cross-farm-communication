import sys;sys.path.insert(0,"worker")
from mentor_question_queue import create_question
from agora_mentor_bridge import *
q=create_question("SAPHEA-QWEN","M02",2,"Why must rpm be converted to rad/s?","power lesson")
p=to_agora(q)
assert p["route"]=="AGORA/GPT_MENTOR"
a=mentor_reply(p,"Because P=tau*omega uses SI angular velocity; omega=2*pi*n/60.")
assert match(p,a) and a["route"]=="AGORA/STUDENT" and len(a["provenance"])==64
print("SAPHEA_BUILD_042_AGORA_MENTOR_BRIDGE_PASS")
