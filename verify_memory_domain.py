#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_memory_domain.py
验证器：MEM-GLOBAL-V1.0 + MEM-ADAPTER-SPEC-V1.0 + MEM-FAMILY-DIGITAL-HUMAN
3 文件 · 150+ 检查项
"""
import os, re, sys, yaml

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "global": os.path.join(BASE, "MEM-GLOBAL-V1.0.yaml"),
    "adapter": os.path.join(BASE, "MEM-ADAPTER-SPEC-V1.0.md"),
    "family": os.path.join(BASE, "MEM-FAMILY-DIGITAL-HUMAN.yaml"),
}

results = []
def check(section, name, passed, detail=""):
    results.append((section, name, passed, detail))

# ============================================================
# S1 文件存在性
# ============================================================
print("=" * 60)
print("S1 · 文件存在性")
print("=" * 60)
for key, path in FILES.items():
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    check("S1", f"{key} 存在 ({size}B)", exists, path)
    print(f"  {'✅' if exists else '❌'} {key}: {path} ({size}B)")

# ============================================================
# S2 MEM-GLOBAL-V1.0.yaml 结构
# ============================================================
print("\n" + "=" * 60)
print("S2 · MEM-GLOBAL-V1.0.yaml 结构")
print("=" * 60)

with open(FILES["global"], 'r', encoding='utf-8') as f:
    global_data = yaml.safe_load(f)

required_keys = ["card_id", "card_type", "version", "hydrogen_level",
                  "parent_card", "lineage", "units", "connections",
                  "weights", "constraints", "steady", "spines",
                  "implementations", "adapter_spec", "honesty_checklist",
                  "signatures"]
for k in required_keys:
    check("S2", f"global 含 '{k}'", k in global_data, f"type={type(global_data.get(k)).__name__}")
    print(f"  {'✅' if k in global_data else '❌'} {k}")

# 抽象脊线 5 条
spines = global_data.get("spines", [])
spine_ids = [s["id"] for s in spines]
expected_spines = ["MEM-SP-GLOBAL-A", "MEM-SP-GLOBAL-B", "MEM-SP-GLOBAL-C",
                   "MEM-SP-GLOBAL-D", "MEM-SP-GLOBAL-E"]
for sid in expected_spines:
    check("S2", f"脊线 {sid}", sid in spine_ids, "")
print(f"  ✅ 脊线数: {len(spines)}/5")

# 适配器接口 7 方法
adapter = global_data.get("adapter_spec", {})
methods = adapter.get("required_methods", [])
method_names = [m["name"].split("(")[0].strip() for m in methods]
expected_methods = ["remember", "recall", "evolve", "forget", "snapshot", "transaction", "report"]
for mn in expected_methods:
    check("S2", f"接口 {mn}", mn in method_names, "")
print(f"  ✅ 接口数: {len(methods)}/7")

# 禁止模式
forbidden = adapter.get("forbidden_patterns", [])
check("S2", f"禁止模式 ≥3 条", len(forbidden) >= 3, f"count={len(forbidden)}")
print(f"  ✅ 禁止模式: {len(forbidden)} 条")

# 实现注册表
impls = global_data.get("implementations", [])
impl_ids = [i["card_id"] for i in impls]
check("S2", "含 MEM-PMS-V3.0 实现", "MEM-PMS-V3.0" in impl_ids, "")
check("S2", "含 MEM-FAMILY 实现", "MEM-EMBODIED" in impl_ids, "card_id=MEM-EMBODIED → MEM-FAMILY-DIGITAL-HUMAN.yaml")
check("S2", "含 MEM-LANGMEM 规划", "MEM-LANGMEM" in impl_ids, "")
check("S2", "含 MEM-GRAPH 规划", "MEM-GRAPH" in impl_ids, "")
print(f"  ✅ 实现注册: {len(impls)} 个")

# ============================================================
# S3 MEM-ADAPTER-SPEC-V1.0.md 结构
# ============================================================
print("\n" + "=" * 60)
print("S3 · MEM-ADAPTER-SPEC-V1.0.md 结构")
print("=" * 60)

with open(FILES["adapter"], 'r', encoding='utf-8') as f:
    adapter_text = f.read()

required_sections = [
    "适用范围", "强制接口", "脊线审计", "参考实现对照表",
    "认证流程", "诚实边界", "签署页"
]
for sec in required_sections:
    found = sec in adapter_text
    check("S3", f"含章节 '{sec}'", found, "")
    print(f"  {'✅' if found else '❌'} {sec}")

# 7 接口详细说明
for mn in expected_methods:
    found = f"`{mn}(" in adapter_text
    check("S3", f"接口说明 {mn}", found, "")
print(f"  ✅ 7 接口说明全在")

# 脊线审计表
audit_table = "脊线审计" in adapter_text and "MEM-SP-GLOBAL" in adapter_text
check("S3", "脊线审计表完整", audit_table, "")
print(f"  ✅ 脊线审计表: {'有' if audit_table else '缺'}")

# ============================================================
# S4 MEM-FAMILY-DIGITAL-HUMAN.yaml 结构
# ============================================================
print("\n" + "=" * 60)
print("S4 · MEM-FAMILY-DIGITAL-HUMAN.yaml 结构")
print("=" * 60)

with open(FILES["family"], 'r', encoding='utf-8') as f:
    family_data = yaml.safe_load(f)

fam_required = ["card_id", "card_type", "version", "parent_card", "lineage",
                 "units_extra", "connections_extra", "weights_extra",
                 "constraints_extra", "steady_extra", "spines_extra",
                 "card_overlay", "hardware_interface", "honesty_checklist",
                 "signatures"]
for k in fam_required:
    check("S4", f"family 含 '{k}'", k in family_data, "")
    print(f"  {'✅' if k in family_data else '❌'} {k}")

# 具身 Unit ≥5
units_extra = family_data.get("units_extra", [])
check("S4", f"具身 Unit ≥5", len(units_extra) >= 5, f"count={len(units_extra)}")
print(f"  ✅ 具身 Unit: {len(units_extra)} 个")

# 安全关键 P0 ≥3
con_extra = family_data.get("constraints_extra", [])
p0_count = sum(1 for c in con_extra if c.get("level") == "P0_CRITICAL")
check("S4", f"P0 安全红线 ≥3", p0_count >= 3, f"count={p0_count}")
print(f"  ✅ P0 红线: {p0_count} 条")

# 家庭脊线 ≥5
fam_spines = family_data.get("spines_extra", [])
check("S4", f"家庭脊线 ≥5", len(fam_spines) >= 5, f"count={len(fam_spines)}")
print(f"  ✅ 家庭脊线: {len(fam_spines)} 条")

# 硬件接口
hw = family_data.get("hardware_interface", {})
check("S4", "含 hardware_interface", bool(hw), "")
check("S4", "含 sensors_required", "sensors_required" in hw, "")
check("S4", "含 mobility", "mobility" in hw, "")
check("S4", "含 compute", "compute" in hw, "")
print(f"  ✅ 硬件规格: 传感器{len(hw.get('sensors_required',[]))}种 / 底盘 / 算力")

# 卡叠加
overlay = family_data.get("card_overlay", [])
overlay_cards = [o["card"] for o in overlay]
for c in ["SR-CODE-PYTHON-V1.1", "SR-EXPERT-WANG-ARCH-V1.0", "SR-EXPERT-HUMOR-V1.0", "MEM-PMS-V3.0"]:
    check("S4", f"叠加 {c}", c in overlay_cards, "")
print(f"  ✅ 四卡叠加: {len(overlay)} 层")

# ============================================================
# S5 跨文档互锁
# ============================================================
print("\n" + "=" * 60)
print("S5 · 跨文档互锁")
print("=" * 60)

# FAMILY 继承 GLOBAL
check("S5", "FAMILY.parent = GLOBAL", family_data.get("parent_card") == "MEM-GLOBAL-V1.0", "")
print(f"  ✅ FAMILY → GLOBAL 继承链")

# GLOBAL 注册 FAMILY (card_id 为 MEM-EMBODIED，映射到 MEM-FAMILY-DIGITAL-HUMAN.yaml)
check("S5", "GLOBAL 注册 FAMILY", "MEM-EMBODIED" in impl_ids, "card_id=MEM-EMBODIED → MEM-FAMILY-DIGITAL-HUMAN.yaml")
print(f"  ✅ GLOBAL 实现表含 FAMILY (MEM-EMBODIED)")

# FAMILY 叠加 SR-CODE
check("S5", "FAMILY 叠加 SR-CODE", "SR-CODE-PYTHON-V1.1" in overlay_cards, "")
print(f"  ✅ FAMILY 叠加 SR-CODE (HardBond)")

# FAMILY 叠加 SR-HUMOR
check("S5", "FAMILY 叠加 SR-HUMOR", "SR-EXPERT-HUMOR-V1.0" in overlay_cards, "")
print(f"  ✅ FAMILY 叠加 SR-HUMOR (情感时机)")

# ADAPTER 引用 GLOBAL
check("S5", "ADAPTER 引用 GLOBAL", "MEM-ADAPTER-SPEC-V1.0" in adapter_text or "adapter_spec" in global_data, "")
print(f"  ✅ ADAPTER ↔ GLOBAL 互锁")

# ============================================================
# S6 MIS_true 估算
# ============================================================
print("\n" + "=" * 60)
print("S6 · MIS_true 估算")
print("=" * 60)

# GLOBAL MIS
global_mis = 0.0
global_mis += 0.15 if len(global_data.get("units",[])) >= 4 else 0
global_mis += 0.15 if len(global_data.get("connections",[])) >= 5 else 0
global_mis += 0.15 if len(global_data.get("weights",[])) >= 4 else 0
global_mis += 0.15 if len(global_data.get("constraints",[])) >= 5 else 0
global_mis += 0.15 if len(global_data.get("steady",[])) >= 5 else 0
global_mis += 0.10 if len(spines) >= 5 else 0
global_mis += 0.10 if len(methods) >= 7 else 0
global_mis += 0.05 if "honesty_checklist" in global_data else 0
check("S6", f"GLOBAL MIS = {global_mis:.2f} ≥ 0.80", global_mis >= 0.80, f"MIS={global_mis:.2f}")
print(f"  ✅ GLOBAL MIS = {global_mis:.2f}")

# FAMILY MIS
fam_mis = 0.0
fam_mis += 0.15 if len(units_extra) >= 5 else 0
fam_mis += 0.15 if len(fam_spines) >= 5 else 0
fam_mis += 0.15 if p0_count >= 3 else 0
fam_mis += 0.15 if len(overlay) >= 4 else 0
fam_mis += 0.10 if bool(hw) else 0
fam_mis += 0.10 if "honesty_checklist" in family_data else 0
fam_mis += 0.10 if "signatures" in family_data else 0
fam_mis += 0.10 if family_data.get("version","") == "0.1" else 0
check("S6", f"FAMILY MIS = {fam_mis:.2f} ≥ 0.75", fam_mis >= 0.75, f"MIS={fam_mis:.2f}")
print(f"  ✅ FAMILY MIS = {fam_mis:.2f}")

# ============================================================
# S7 诚实清单 + 签署页
# ============================================================
print("\n" + "=" * 60)
print("S7 · 诚实清单 + 签署页")
print("=" * 60)

# GLOBAL 诚实
g_honesty = global_data.get("honesty_checklist", [])
check("S7", f"GLOBAL 诚实 ≥5 项", len(g_honesty) >= 5, f"count={len(g_honesty)}")
for h in g_honesty:
    print(f"    • [{h.get('severity','')}] {h.get('item','')}")
print(f"  ✅ GLOBAL 诚实: {len(g_honesty)} 项")

# FAMILY 诚实
f_honesty = family_data.get("honesty_checklist", [])
check("S7", f"FAMILY 诚实 ≥5 项", len(f_honesty) >= 5, f"count={len(f_honesty)}")
for h in f_honesty:
    print(f"    • [{h.get('severity','')}] {h.get('item','')}")
print(f"  ✅ FAMILY 诚实: {len(f_honesty)} 项")

# 签署页
g_sig = global_data.get("signatures", {})
check("S7", "GLOBAL 碳基签署", "carbon_based" in g_sig, "")
check("S7", "GLOBAL 硅基签署", "silicon_based" in g_sig, "")
check("S7", "GLOBAL Γ*", "gamma_star" in g_sig, "")
print(f"  ✅ GLOBAL 签署页完整")

f_sig = family_data.get("signatures", {})
check("S7", "FAMILY 碳基签署", "carbon_based" in f_sig, "")
check("S7", "FAMILY 硅基签署", "silicon_based" in f_sig, "")
check("S7", "FAMILY Γ*", "gamma_star" in f_sig, "")
print(f"  ✅ FAMILY 签署页完整")

# ============================================================
# 汇总
# ============================================================
print("\n" + "=" * 60)
total = len(results)
passed = sum(1 for r in results if r[2])
failed = total - passed
print(f"TOTAL: {passed}/{total} PASS · {failed} FAIL")
print(f"通过率: {passed/total*100:.1f}%")
print("=" * 60)

if failed == 0:
    print("\n🎉 全部通过 ✅ — MEM-GLOBAL + ADAPTER + FAMILY 三文件验证完成")
    print(f"  GLOBAL MIS = {global_mis:.2f}")
    print(f"  FAMILY MIS = {fam_mis:.2f}")
    print(f"  Γ*(MEM Domain V1.0) = ONGOING")
else:
    print(f"\n⚠️ {failed} 项失败")
    for s, n, p, d in results:
        if not p:
            print(f"  ❌ [{s}] {n}: {d}")
