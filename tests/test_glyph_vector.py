import sys; sys.path.insert(0,"worker")
from glyph_vector import packet,compact
p=packet("SAPHEA-SCIENCE",[
 {"kind":"GIVEN","key":"P","value":12,"unit":"MPa"},
 {"kind":"GIVEN","key":"A","value":0.003,"unit":"m2"},
 {"kind":"DERIVED","key":"F","value":36,"unit":"kN"},
 {"kind":"CONTRADICTION","key":"REPORT_F","value":"3.6_vs_36","unit":"kN"},
 {"kind":"UNKNOWN","key":"adequacy","value":"required_load_missing"}],
 "BUILD-025-test")
g=compact(p)
assert "D:F=36@kN" in g and "X:REPORT_F=3.6_vs_36@kN" in g and "U:adequacy=required_load_missing" in g
assert "GLYPH_VECTOR!=EVIDENCE" in p["rules"]
print(g)
print("SAPHEA_BUILD_025_GLYPH_VECTOR_PASS")
