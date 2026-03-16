#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifikation der Saetze aus GR_SSZ_INTERSECTION_PHI_DISCRETIZATION.md"""

import numpy as np
from scipy.optimize import brentq

PHI = (1 + np.sqrt(5)) / 2
XI_MAX = 1 - np.exp(-PHI)
D_MIN  = 1 / (2 - np.exp(-PHI))

def xi_decay(x): return 1.0 - np.exp(-PHI / x)
def xi_satur(x): return 1.0 - np.exp(-PHI * x)
def d_ssz(xi): return 1.0 / (1.0 + xi)
def d_gr(x): return float(np.sqrt(1.0 - 1.0/x)) if x > 1.0 else 0.0

all_pass = True

# ============================================================
print("=== KONSTANTEN ===")
print(f"phi          = {PHI:.15f}")
print(f"Xi_max       = {XI_MAX:.15f}")
print(f"D_min        = {D_MIN:.15f}")
cond_A = PHI + np.exp(-1)
cond_B = PHI + np.exp(-PHI**2)
print(f"phi + e^-1   = {cond_A:.15f}  < 2: {cond_A < 2}")
print(f"phi + e^-ph2 = {cond_B:.15f}  < 2: {cond_B < 2}")

# ============================================================
print()
print("=== SATZ 1: D_GR(phi) = 1/phi ===")
d1 = d_gr(PHI)
expected = 1.0 / PHI
diff = abs(d1 - expected)
ok = diff < 1e-14
print(f"D_GR(phi) = {d1:.15f}")
print(f"1/phi     = {expected:.15f}")
print(f"Diff      = {diff:.2e}  PASS: {ok}")
if not ok: all_pass = False

# ============================================================
print()
print("=== SATZ 2: a_{k+1} = (a_k + 1/phi) / phi ===")
for k in range(5):
    xk   = PHI**k
    xk1  = PHI**(k+1)
    ak   = d_gr(xk)**2
    ak1_direct  = d_gr(xk1)**2
    ak1_recurse = (ak + 1.0/PHI) / PHI
    err = abs(ak1_direct - ak1_recurse)
    ok = err < 1e-13
    print(f"k={k}: a_k={ak:.6f}  a_k1_direct={ak1_direct:.6f}  recurse={ak1_recurse:.6f}  delta={err:.2e}  {'OK' if ok else 'FAIL'}")
    if not ok: all_pass = False

# ============================================================
print()
print("=== SATZ 3: q_{k+1} = q_k^{1/phi} (Abklingform) ===")
for k in range(5):
    qk       = np.exp(-PHI**(1-k))
    qk1_d    = np.exp(-PHI**(0-k))   # = exp(-phi^{-k})
    qk1_r    = qk**(1.0/PHI)
    err = abs(qk1_d - qk1_r)
    ok = err < 1e-13
    print(f"k={k}: q_k={qk:.6f}  direct={qk1_d:.6f}  recurse={qk1_r:.6f}  delta={err:.2e}  {'OK' if ok else 'FAIL'}")
    if not ok: all_pass = False

# ============================================================
print()
print("=== SATZ 4: p_{k+1} = p_k^phi (Saettigungsform) ===")
for k in range(5):
    pk       = np.exp(-PHI**(k+1))
    pk1_d    = np.exp(-PHI**(k+2))
    pk1_r    = pk**PHI
    err = abs(pk1_d - pk1_r)
    ok = err < 1e-13
    print(f"k={k}: p_k={pk:.6f}  direct={pk1_d:.6f}  recurse={pk1_r:.6f}  delta={err:.2e}  {'OK' if ok else 'FAIL'}")
    if not ok: all_pass = False

# ============================================================
print()
print("=== SATZ 5: Vorzeichenwechsel ===")
da0 = d_ssz(xi_decay(1.0)) - d_gr(1.0)
da1 = d_ssz(xi_decay(PHI)) - d_gr(PHI)
db0 = d_ssz(xi_satur(1.0)) - d_gr(1.0)
db1 = d_ssz(xi_satur(PHI)) - d_gr(PHI)
print(f"Delta^A_0 = {da0:+.6f}  > 0: {da0>0}")
print(f"Delta^A_1 = {da1:+.6f}  < 0: {da1<0}")
print(f"Delta^B_0 = {db0:+.6f}  > 0: {db0>0}")
print(f"Delta^B_1 = {db1:+.6f}  < 0: {db1<0}")
conds = [da0>0, da1<0, db0>0, db1<0]
if not all(conds): all_pass = False

print()
print("=== SCHNITTPUNKTE ===")
x_A = brentq(lambda x: d_ssz(xi_decay(x)) - d_gr(x), 1.001, PHI - 1e-6)
x_B = brentq(lambda x: d_ssz(xi_satur(x)) - d_gr(x), 1.001, PHI - 1e-6)
print(f"Abklingform:     r*/r_s = {x_A:.6f}  D* = {d_gr(x_A):.6f}  in [1,phi]: {1<x_A<PHI}")
print(f"Saettigungsform: r*/r_s = {x_B:.6f}  D* = {d_gr(x_B):.6f}  in [1,phi]: {1<x_B<PHI}")
ok_A = abs(x_A - 1.594811) < 0.0001 and 1 < x_A < PHI
ok_B = abs(x_B - 1.387)    < 0.001  and 1 < x_B < PHI
print(f"Abklingform Verifikation:     {'PASS' if ok_A else 'FAIL'}")
print(f"Saettigungsform Verifikation: {'PASS' if ok_B else 'FAIL'}")
if not (ok_A and ok_B): all_pass = False

# ============================================================
print()
print("=== REALE OBJEKTE ===")
G = 6.6743e-11
C = 2.99792458e8
M_SUN = 1.9885e30

def rs_km(M_solar):
    return 2 * G * M_solar * M_SUN / C**2 / 1000.0  # in km

objs = [
    ("BH Horizont",     None,   None,    1.0),
    ("PSR J0740+6620",  2.08,   12.4,    None),
    ("NS kanonisch",    1.40,   10.0,    None),
    ("PSR J0030+0451",  1.34,   12.7,    None),
    ("Sirius B",        1.02,   5800.0,  None),
    ("Sonne",           1.00,   696000.0, None),
]

print(f"  {'Objekt':<18} {'x':>9} {'k_brack':>8} {'D_GR':>8} {'D_SSZ_A':>9} {'Delta%':>8}")
print("  " + "-"*65)
for name, M_solar, R_km, x_override in objs:
    if x_override is not None:
        x = x_override
    else:
        x = R_km / rs_km(M_solar)
    k = int(np.floor(np.log(x)/np.log(PHI))) if x > 1 else -1
    dg = d_gr(x)
    da = d_ssz(xi_decay(x))
    if dg > 0:
        dpct = (da - dg) / dg * 100
        print(f"  {name:<18} {x:>9.1f} [{k:>3},{k+1}]  {dg:>8.5f} {da:>9.5f} {dpct:>+7.2f}%")
    else:
        print(f"  {name:<18} {x:>9.3f} [{k:>3},{k+1}]  {'0(sing.)':>8} {da:>9.5f}    ---")

# ============================================================
print()
print("="*60)
print(f"GESAMT-ERGEBNIS: {'ALLE TESTS BESTANDEN' if all_pass else 'FEHLER AUFGETRETEN'}")
print("="*60)
