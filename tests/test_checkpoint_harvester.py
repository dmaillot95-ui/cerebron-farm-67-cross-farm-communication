import sys;sys.path.insert(0,"worker")
from checkpoint_harvester import *
d=harvest("collatz-research","C66",
 ["N<=4 closed under stated odd-map theorem"],
 ["arbitrary N remains open"],
 ["finite search cannot prove arbitrary N"],
 "checkpoint-C66")
assert len(d)==3
assert [x["status"] for x in d]==["CANDIDATE","UNKNOWN","REJECTED"]
assert all(x["provenance"]=="checkpoint-C66" for x in d)
p=export_packet(d)
assert "LEARNING_GATE_REQUIRED" in p["rules"]
print("\n".join(glyph(x) for x in d))
print("SAPHEA_BUILD_030_CHECKPOINT_HARVESTER_PASS")
