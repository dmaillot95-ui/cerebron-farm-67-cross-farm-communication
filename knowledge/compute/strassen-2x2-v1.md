# AFAH — STRASSEN 2x2 V1

Status: VERIFIED_ALGORITHM
Scope: SAPHEA + Sapheĩde + future AFAH colonies
Rule: REDUCE_BEFORE_COMPUTE; EXACT_EQUIVALENCE_REQUIRED

For
A=[[a,b],[c,d]], B=[[e,f],[g,h]]

Compute seven scalar products:
M1=(a+d)(e+h)
M2=(c+d)e
M3=a(f-h)
M4=d(g-e)
M5=(a+b)h
M6=(c-a)(e+f)
M7=(b-d)(g+h)

Reconstruct:
C11=M1+M4-M5+M7
C12=M3+M5
C21=M2+M4
C22=M1-M2+M3+M6

Thus C=A*B using 7 scalar multiplications instead of the classical 8.

Control rules:
1. Never claim fewer operations unless every hidden multiplication is counted.
2. Verify reconstructed C against ordinary matrix multiplication on test cases.
3. For tensor powers, 7^2=49 is only a baseline, not a lower bound.
4. Any candidate below 49 remains EXPERIMENTAL until exact decomposition and independent verification.
5. Prefer an optimization only when its total cost (multiplications, additions, memory, precision, overhead) fits the mission.
6. COMPUTATION != PROOF; CANDIDATE != CERTIFIED REDUCTION.

Routing:
matrix/tensor task -> inspect structure -> reuse/factor/common subexpressions -> choose verified algorithm -> compute -> exact/numerical verification -> report operation count.
