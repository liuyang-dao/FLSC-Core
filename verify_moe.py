#!/usr/bin/env python3
"""verify_moe.py — MoE spine YAML 完整性验证"""
import yaml, sys, os

path = os.path.join(os.path.dirname(__file__), "moe_spine.yaml")
with open(path, "r", encoding="utf-8") as f:
    s = yaml.safe_load(f)

print("=" * 55)
print("MoE SPINE YAML — 完整性验证")
print("=" * 55)

# 1. meta
m = s.get("meta", {})
print(f"\n[meta] doc_id = {m.get('doc_id')}")
print(f"[meta] target = {m.get('target_system')}")
assert m.get("doc_id"), "FAIL: meta.doc_id 缺失"

# 2. 五层
fl = s.get("five_layer_map", {})
print(f"\n[five_layer_map] 层数 = {len(fl)}")
for k in ["U_Unit_层", "C_Connect_层", "W_Weight_层", "K_Constraint_层", "S_Steady_层"]:
    assert k in fl, f"FAIL: 缺 {k}"
    print(f"  ✓ {k}")
assert len(fl) == 5, f"FAIL: 五层数量={len(fl)}"

# 3. 五脊
sp = s.get("spine", {})
print(f"\n[spine] 脊线数 = {len(sp)}")
expected = ["MOE-A", "MOE-B", "MOE-C", "MOE-D", "MOE-E"]
for sid in expected:
    found = any(k.startswith(sid) for k in sp.keys())
    assert found, f"FAIL: 缺脊线 {sid}"
    print(f"  ✓ {[k for k in sp.keys() if k.startswith(sid)][0]}")
assert len(sp) == 5, f"FAIL: 脊线数={len(sp)}，期望5"

# 4. 独立性
ic = s.get("independence_check", {})
print(f"\n[independence_check] result = {ic.get('result')}")
assert "独立" in ic.get("result", ""), "FAIL: 独立性校验"

# 5. 断裂面
fs = s.get("fracture_surfaces", [])
print(f"\n[fracture_surfaces] 数量 = {len(fs)}")
assert len(fs) >= 5, f"FAIL: 断裂面={len(fs)}"
for fr in fs:
    print(f"  ✓ {fr['spine']}: {fr['fracture']}")

# 6. SCVP
scvp = s.get("scvp", {})
print(f"\n[scvp] overall = {scvp.get('overall')}")
for item in scvp.get("per_spine", []):
    print(f"  {item['spine']}: {item['closed']}")
closed = sum(1 for x in scvp["per_spine"] if x["closed"] == "CLOSED")
partial = sum(1 for x in scvp["per_spine"] if "PARTIAL" in x["closed"])
print(f"  → {closed}/5 CLOSED, {partial}/5 PARTIAL")

# 7. Axiom R
ar = s.get("axiom_r", {})
print(f"\n[axiom_r]")
print(f"  baseline MIS_true = {ar['baseline']['MIS_true']} ({ar['baseline']['status']})")
print(f"  post_repair MIS_true = {ar['post_repair_estimate']['MIS_true']} ({ar['post_repair_estimate']['status']})")
assert ar["baseline"]["MIS_true"] == 0.68
assert ar["post_repair_estimate"]["MIS_true"] == 0.85

# 8. 诚实补丁
hp = s.get("honest_patch_summary", {})
print(f"\n[honest_patch] 补丁数 = {len(hp)}")
for k, v in hp.items():
    print(f"  ✓ {k}: {v[:60]}...")
assert len(hp) >= 5

# 9. 安全约束
sc = s.get("safety_constraints", [])
print(f"\n[safety_constraints] 数量 = {len(sc)}")
assert len(sc) >= 5

# 10. 验收指标
ab = s.get("acceptance_baseline", [])
print(f"\n[acceptance_baseline] 指标数 = {len(ab)}")
assert len(ab) >= 7

# 11. 三阶自指
tsr = s.get("three_order_self_reference", {})
for k in ["L1_first_order", "L2_second_order", "L3_third_order"]:
    assert k in tsr, f"FAIL: 缺 {k}"
print(f"\n[three_order_self_reference] L1/L2/L3 ✓")

# 12. DegradationFSM
df = s.get("degradation_fsm", {})
print(f"[degradation_fsm] states = {len(df.get('states',[]))}, triggers = {len(df.get('triggers',[]))}")

print("\n" + "=" * 55)
print("✅ 全部检查通过（共 11 大类）")
print("=" * 55)
sys.exit(0)
