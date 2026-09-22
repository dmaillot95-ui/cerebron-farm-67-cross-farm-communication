import sys;sys.path.insert(0,"worker")
from fractal_foundry import *
def branches(m,d):
 return [("DERIVE",m+" derive"),("FALSIFY",m+" falsify"),("VERIFY",m+" verify"),("DERIVE",m+" derive")]
p=plan("Collatz arbitrary-N residual",branches,depth=5,max_agents=10000,per_parent=100)
assert len(p)>3 and len(p)<=10000
assert all(x["state"]=="PLANNED_NOT_EXECUTED" for x in p)
assert len({(x["lane"],x["mission"]) for x in p})==len(p)
assert len(execution_budget(p,100))<=100
print({"planned":len(p),"max_capacity":10000,"executed":0})
print("SAPHEA_BUILD_033_FRACTAL_FOUNDRY_PASS")
