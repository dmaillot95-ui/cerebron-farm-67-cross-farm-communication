import sys;sys.path.insert(0,"worker")
from curriculum_compiler import *
assert len(SECTIONS)==10
p=packet("M02","equations","P=tau*omega","tau=80 N*m, n=1800 rpm")
assert p["status"]=="TEACH_NOT_MASTERED" and len(p["provenance"])==64
assert promote(p,True,True,True)=="MASTERED"
assert promote(p,True,False,True)=="RETRY"
print("MODULES",len(SECTIONS),"SKILLS",sum(len(x[2]) for x in SECTIONS))
print("SAPHEA_BUILD_039_CURRICULUM_COMPILER_PASS")
