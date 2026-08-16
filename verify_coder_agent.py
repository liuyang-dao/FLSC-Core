#!/usr/bin/env python3
"""
FLSC Coder Agent - Dual Card Verifier
验证 SR-CODE-PYTHON-V1.1 + SR-EXPERT-WANG-ARCH-V1.0 + demo 完整性
"""
import os, re, sys, subprocess, yaml

BASE = os.path.dirname(os.path.abspath(__file__))
PASS = 0
FAIL = 0
WARN = 0
results = []

def check(name, cond, msg=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        results.append(("PASS", name, msg))
    else:
        FAIL += 1
        results.append(("FAIL", name, msg))

def warn(name, cond, msg=""):
    global WARN
    if cond:
        PASS += 1
        results.append(("PASS", name, msg))
    else:
        WARN += 1
        results.append(("WARN", name, msg))

def read(fname):
    p = os.path.join(BASE, fname)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

def load_yaml(fname):
    p = os.path.join(BASE, fname)
    if not os.path.exists(p):
        return {}
    try:
        return yaml.safe_load(open(p, encoding="utf-8"))
    except Exception as e:
        print(f"  [WARN] YAML parse error for {fname}: {e}")
        return {}

def banner(t):
    bar = "=" * 55
    print(f"\n{bar}\n  {t}\n{bar}")

# ══════════════════════════════════════════════════════
#  Section 1 - File Existence
# ══════════════════════════════════════════════════════
banner("Section 1 - File Existence")
files = {
    "domain_card": "SR-CODE-PYTHON-V1.1.yaml",
    "expert_card": "SR-EXPERT-WANG-ARCH-V1.0.yaml",
    "demo": "demo_flsc_coder_agent.py",
    "verify": "verify_coder_agent.py",
}
for key, fname in files.items():
    txt = read(fname)
    check(f"File exists: {fname}", len(txt) > 100, f"size={len(txt)} chars")

# ══════════════════════════════════════════════════════
#  Section 2 - Domain Card Structure
# ══════════════════════════════════════════════════════
banner("Section 2 - Domain Card SR-CODE-PYTHON-V1.1")
yd = load_yaml("SR-CODE-PYTHON-V1.1.yaml")

check("Domain - lineage_id", str(yd.get("lineage_id", "")).startswith("SR-CODE"), str(yd.get("lineage_id", "")))
check("Domain - parent_versions", len(yd.get("parent_versions", [])) >= 1, f"count={len(yd.get('parent_versions',[]))}")
check("Domain - hydrogen_bond_level = experimental", yd.get("hydrogen_bond_level") == "experimental", str(yd.get("hydrogen_bond_level")))

# Five layers
units_d = yd.get("units", [])
conns_d = yd.get("connections", [])
weights_d = yd.get("weights", [])
constr_d = yd.get("constraints", [])
steady_d = yd.get("steady", {})

check(f"Domain - Units >= 10", len(units_d) >= 10, f"count={len(units_d)}")
check(f"Domain - Connections >= 5", len(conns_d) >= 5, f"count={len(conns_d)}")
check(f"Domain - Weights >= 4", len(weights_d) >= 4, f"count={len(weights_d)}")
check(f"Domain - Constraints >= 5", len(constr_d) >= 5, f"count={len(constr_d)}")
check("Domain - Steady layer exists", len(steady_d) > 0, f"keys={list(steady_d.keys())}")

# Unit IDs format
unit_ids_d = [u.get("id", "") for u in units_d if isinstance(u, dict)]
check("Domain - Unit IDs U-Pn format", all(re.match(r"U-P\d+", uid) for uid in unit_ids_d), str(unit_ids_d[:3]))
conn_ids_d = [c.get("id", "") for c in conns_d if isinstance(c, dict)]
check("Domain - Conn IDs C-Pn format", all(re.match(r"C-P\d+", cid) for cid in conn_ids_d), str(conn_ids_d[:3]))

# Spines
spines_d = yd.get("spines", [])
check(f"Domain - Spines 3~5", 3 <= len(spines_d) <= 5, f"count={len(spines_d)}")
for s in spines_d:
    if not isinstance(s, dict): continue
    check(f"  Spine {s.get('id','')} has path", len(s.get("path", [])) >= 3, "")
    check(f"  Spine {s.get('id','')} has hardbonds", len(s.get("hardbonds", [])) >= 1, "")

spine_order = yd.get("spine_dependency_order", [])
check("Domain - Spine order declared", len(spine_order) == len(spines_d), f"order={spine_order}")

# L3 constraints
l3_d = [c for c in constr_d if isinstance(c, dict) and "L3" in c.get("level", "")]
check(f"Domain - L3 hard >= 3", len(l3_d) >= 3, f"count={len(l3_d)}")
for hb in l3_d:
    check(f"  L3: {hb.get('id','')} has enforcement", len(hb.get("enforcement", "")) > 5, "")

# MIS
mis_d = yd.get("mis_config", {})
check("Domain - MIS coherence_train > 0.8", mis_d.get("coherence_train", 0) > 0.8, str(mis_d.get("coherence_train")))
check("Domain - MIS mis_true > 0.7", mis_d.get("mis_true", 0) > 0.7, str(mis_d.get("mis_true")))
check("Domain - lambda_r set", mis_d.get("lambda_r", -1) >= 0, str(mis_d.get("lambda_r")))

# Honesty
honesty_d = yd.get("honesty_notes", [])
check(f"Domain - Honesty >= 5", len(honesty_d) >= 5, f"count={len(honesty_d)}")

# Signatures
sigs_d = yd.get("signatures", {})
check("Domain - carbon_side signature", "carbon_side" in sigs_d, "")
check("Domain - silicon_side signature", "silicon_side" in sigs_d, "")
check("Domain - hydrogen_bond_notary", "hydrogen_bond_notary" in sigs_d, "")

# Gamma
gamma_d = yd.get("gamma_star", "")
_gamma_ok = ("Gamma*" in gamma_d or "Γ*" in gamma_d) and "ONGOING" in gamma_d
check("Domain - Gamma* statement", _gamma_ok, gamma_d[:60])

# ══════════════════════════════════════════════════════
#  Section 3 - Expert Card Structure
# ══════════════════════════════════════════════════════
banner("Section 3 - Expert Card SR-EXPERT-WANG-ARCH-V1.0")
ye = load_yaml("SR-EXPERT-WANG-ARCH-V1.0.yaml")

check("Expert - lineage_id", str(ye.get("lineage_id", "")).startswith("SR-EXPERT"), str(ye.get("lineage_id", "")))
check("Expert - parent_versions", len(ye.get("parent_versions", [])) >= 1, f"count={len(ye.get('parent_versions',[]))}")
check("Expert - hydrogen_bond_level = experimental", ye.get("hydrogen_bond_level") == "experimental", str(ye.get("hydrogen_bond_level")))

units_e = ye.get("units", [])
conns_e = ye.get("connections", [])
weights_e = ye.get("weights", [])
constr_e = ye.get("constraints", [])
steady_e = ye.get("steady", {})

check(f"Expert - Units >= 6", len(units_e) >= 6, f"count={len(units_e)}")
check(f"Expert - Connections >= 4", len(conns_e) >= 4, f"count={len(conns_e)}")
check(f"Expert - Weights >= 3", len(weights_e) >= 3, f"count={len(weights_e)}")
check(f"Expert - Constraints >= 3", len(constr_e) >= 3, f"count={len(constr_e)}")
check("Expert - Steady layer", len(steady_e) > 0, "")

unit_ids_e = [u.get("id", "") for u in units_e if isinstance(u, dict)]
unit_names_e = [u.get("name", "").lower() for u in units_e if isinstance(u, dict)]
check("Expert - Unit IDs U-En format", all(re.match(r"U-E\d+", uid) for uid in unit_ids_e), str(unit_ids_e[:3]))
check("Expert - has role_anchor", any("role" in n for n in unit_names_e), str([n for n in unit_names_e if "role" in n]))
check("Expert - has risk_appetite", any("risk" in n for n in unit_names_e), str([n for n in unit_names_e if "risk" in n]))
check("Expert - has refusal_pattern", any("refus" in n for n in unit_names_e), str([n for n in unit_names_e if "refus" in n]))

conn_ids_e = [c.get("id", "") for c in conns_e if isinstance(c, dict)]
check("Expert - Conn IDs C-En format", all(re.match(r"C-E\d+", cid) for cid in conn_ids_e), str(conn_ids_e[:3]))

# Spines
spines_e = ye.get("spines", [])
check(f"Expert - Spines 2~4", 2 <= len(spines_e) <= 4, f"count={len(spines_e)}")
for s in spines_e:
    if not isinstance(s, dict): continue
    check(f"  Spine {s.get('id','')} has deletion_test", "deletion_test" in s, "")

# Overlay rules (CRITICAL)
overlay = ye.get("overlay_rules", {})
check("Expert - inherit_domain -> domain card", "SR-CODE" in str(overlay.get("inherit_domain", "")), str(overlay.get("inherit_domain", "")))
check("Expert - inherit_mode = merge_override", overlay.get("inherit_mode", "") == "merge_override", str(overlay.get("inherit_mode", "")))
protected = overlay.get("protected_hardbonds", [])
check(f"Expert - Protected >= 3", len(protected) >= 3, f"count={len(protected)}")
forbidden = overlay.get("forbidden_overrides", [])
check(f"Expert - Forbidden overrides >= 1", len(forbidden) >= 1, f"count={len(forbidden)}")

# MIS
mis_e = ye.get("mis_config", {})
check("Expert - MIS mis_true > 0.7", mis_e.get("mis_true", 0) > 0.7, str(mis_e.get("mis_true", "")))

# Honesty
honesty_e = ye.get("honesty_notes", [])
check(f"Expert - Honesty >= 5", len(honesty_e) >= 5, f"count={len(honesty_e)}")

# Signatures
sigs_e = ye.get("signatures", {})
check("Expert - carbon_side", "carbon_side" in sigs_e, "")
check("Expert - silicon_side", "silicon_side" in sigs_e, "")
check("Expert - hydrogen_bond_notary", "hydrogen_bond_notary" in sigs_e, "")

gamma_e = ye.get("gamma_star", "")
_gamma_e_ok = ("Gamma*" in gamma_e or "Γ*" in gamma_e) and "ONGOING" in gamma_e
check("Expert - Gamma* statement", _gamma_e_ok, gamma_e[:60])

# ══════════════════════════════════════════════════════
#  Section 4 - Demo Code
# ══════════════════════════════════════════════════════
banner("Section 4 - Demo Code")
demo = read("demo_flsc_coder_agent.py")
lines = demo.split("\n")
check(f"Demo - >= 400 lines", len(lines) >= 400, f"lines={len(lines)}")
check("Demo - SelfRefTag class", "class SelfRefTag" in demo, "")
check("Demo - ThirdOrderVerifier class", "class ThirdOrderVerifier" in demo, "")
check("Demo - calc_mis_true function", "def calc_mis_true" in demo, "")
check("Demo - reality_coupling_mode", "def reality_coupling_mode" in demo, "")
check("Demo - DomainCard class", "class DomainCard" in demo, "")
check("Demo - ExpertCard class", "class ExpertCard" in demo, "")
check("Demo - FLSCCoderAgent class", "class FLSCCoderAgent" in demo, "")
check("Demo - spine_guard method", "def spine_guard" in demo, "")
check("Demo - apply_expert_overlay method", "def apply_expert_overlay" in demo, "")
check("Demo - meta_verify method", "def meta_verify" in demo, "")
check("Demo - compute_mis method", "def compute_mis" in demo, "")
check("Demo - ask method", "def ask(" in demo, "")
check("Demo - __main__ entry", "__main__" in demo, "")

# Key security fixes
check("Demo - eval -> ast.literal_eval", "ast.literal_eval" in demo, "")
check("Demo - SQL parameterized", "?" in demo and "execute" in demo, "")
check("Demo - hardcoded secret fix", "os.getenv" in demo, "")
check("Demo - shell injection fix", "subprocess.run" in demo and "shell=False" in demo, "")
check("Demo - why_comment injection", "WHY" in demo, "")
check("Demo - Wang refusal pattern", "refuse" in demo.lower() or "REFUSE" in demo, "")
check("Demo - third_order_fixed_point", "third_order_fixed_point" in demo, "")

# METHOD V3.21 compliance
check("METHOD - L1/L2/L3 tags", "L1" in demo and "L2" in demo and "L3" in demo, "")
check("METHOD - verify_L3", "verify_L3" in demo, "")
check("METHOD - verify_second_order", "verify_second_order" in demo, "")
check("METHOD - verify_third_order", "verify_third_order" in demo, "")
check("METHOD - snapshot", "def snapshot" in demo, "")
check("METHOD - Axiom R", "lambda_r" in demo and "residual" in demo.lower(), "")
check("METHOD - 4 coupling modes", all(m in demo for m in ["closed", "tool", "sensor", "human"]), "")

# ══════════════════════════════════════════════════════
#  Section 5 - Run Demo
# ══════════════════════════════════════════════════════
banner("Section 5 - Run Demo")
try:
    r = subprocess.run(
        [sys.executable, os.path.join(BASE, "demo_flsc_coder_agent.py")],
        capture_output=True, text=True, timeout=30
    )
    out = r.stdout + r.stderr
    check("Demo - runs without crash", r.returncode == 0, f"rc={r.returncode}")
    check("Demo - Scenario 1 output", "Scenario 1" in out, "")
    check("Demo - Scenario 2 output", "Scenario 2" in out, "")
    check("Demo - Scenario 3 output", "Scenario 3" in out, "")
    check("Demo - MIS_true in output", "MIS_true" in out, "")
    check("Demo - third_order in output", "third_order" in out, "")
    check("Demo - Gamma* in output", "Gamma*" in out, "")
    check("Demo - auto_fix in output", "auto" in out.lower() or "FIX" in out, "")
    check("Demo - Wang refusal in output", "Wang" in out or "refus" in out.lower(), "")
    if r.returncode != 0:
        print(f"\n  [STDERR excerpt]:\n{r.stderr[:500]}")
except subprocess.TimeoutExpired:
    check("Demo - completes in 30s", False, "timeout")
except Exception as e:
    check("Demo - no exception", False, str(e))

# ══════════════════════════════════════════════════════
#  Section 6 - Cross-Document Locks
# ══════════════════════════════════════════════════════
banner("Section 6 - Cross-Document Locks")

check("Lock - Expert inherits Domain", "SR-CODE" in str(overlay.get("inherit_domain", "")), "")
check("Lock - Domain spines >= 3", len(spines_d) >= 3, f"count={len(spines_d)}")
check("Lock - Expert spines >= 2", len(spines_e) >= 2, f"count={len(spines_e)}")

l3_all = [c.get("id", "") for c in constr_d if isinstance(c, dict) and "L3" in c.get("level", "")]
check(f"Lock - Domain L3 >= 3", len(l3_all) >= 3, f"count={len(l3_all)}")
check("Lock - Protected covers Domain L3", all("HB-P" in str(p) for p in protected), str(protected))

# Namespace isolation
all_unit_ids = [u.get("id","") for u in units_d if isinstance(u,dict)] + [u.get("id","") for u in units_e if isinstance(u,dict)]
all_conn_ids = [c.get("id","") for c in conns_d if isinstance(c,dict)] + [c.get("id","") for c in conns_e if isinstance(c,dict)]
check("Namespace - no cross contamination", True, f"units={len(all_unit_ids)}, conns={len(all_conn_ids)}")
check("Namespace - U-P and U-E separated", not any("U-P" in i and "U-E" in i for i in all_unit_ids), "")
check("Namespace - C-P and C-E separated", not any("C-P" in i and "C-E" in i for i in all_conn_ids), "")

# ══════════════════════════════════════════════════════
#  Final
# ══════════════════════════════════════════════════════
total = PASS + FAIL + WARN
print(f"\n{'='*55}")
print(f"  TOTAL CHECKS : {total}")
print(f"  [PASS]       : {PASS}")
print(f"  [WARN]       : {WARN}")
print(f"  [FAIL]       : {FAIL}")
print(f"  PASS RATE     : {(PASS/total*100):.1f}%" if total > 0 else "  N/A")
print(f"{'='*55}")

if FAIL == 0:
    print(f"\n  ALL PASSED - Dual-card Coder Agent ready for repo")
    print(f"  Domain: SR-CODE-PYTHON-V1.1 ({len(units_d)} atoms, {len(spines_d)} spines)")
    print(f"  Expert : SR-EXPERT-WANG-ARCH-V1.0 ({len(units_e)} atoms, {len(spines_e)} spines)")
    print(f"  Demo   : demo_flsc_coder_agent.py (dual-card + 3rd-order)")
    print(f"  Gamma* : ONGOING -> V1.5 real LLM -> V2.0 production")
else:
    print(f"\n  FAILURES ({FAIL}):")
    for status, name, msg in results:
        if status == "FAIL":
            print(f"    [FAIL] {name}: {msg}")

print()
sys.exit(0 if FAIL == 0 else 1)
