import sys;sys.path.insert(0,"worker")
from cerebron_summary_tree import *
nodes=[
 node("IDENTITY","role","industrial-science","VERIFIED","C42.1"),
 node("RULES","claim","CLAIM<=EVIDENCE","VERIFIED","constitution"),
 node("KNOWLEDGE","F","36kN","VERIFIED","BUILD-023"),
 node("FAILURES","verbose","token-truncation","VERIFIED","BUILD-024"),
 node("SKILLS","glyph","compact-transfer","CANDIDATE","BUILD-025"),
 node("CHECKPOINT","build","026","CANDIDATE",""),
 node("GAP","gain","orchestration-unproven","UNKNOWN","BUILD-024"),
 node("ACTION","next","retrieval-test","CANDIDATE","")
]
t=tree("farm-67","SAPHEA-SCIENCE",nodes)
g=glyph(t,["RULES","KNOWLEDGE","FAILURES","GAP","ACTION"])
assert "RV:claim=CLAIM<=EVIDENCE" in g
assert "KU:F=36kN" not in g and "KV:F=36kN" in g
assert "GU:gain=orchestration-unproven" in g
try:
 promote(node("SKILLS","x","y"),"VERIFIED","")
 raise AssertionError("promotion without evidence accepted")
except ValueError: pass
print(g)
print("SAPHEA_BUILD_026_SUMMARY_TREE_PASS")
