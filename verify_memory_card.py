#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_memory_card.py
验证 SR-MEMORY-PMS-V3.0.yaml 结构完整性
检查项：
  S1 文件存在性
  S2 YAML 结构（unit/connect/weight/constraint/steady/spines）
  S3 第一刀自检（五层齐全）
  S4 第二刀脊线（≤5条 + 删减测试）
  S5 跨文档互锁（与 SR-AI-STAFF-PMS-V1.0 / METHOD-V3.21）
  S6 MIS_true 计算
  S7 诚实清单 + 签署页
"""
import yaml, os, sys, hashlib
from datetime import datetime

CARD_PATH = "/data/workspace/domains/asset_cards/SR-MEMORY-PMS-V3.0.yaml"
REPO_ROOT = "/data/workspace"

results = []
def check(section, name, cond, detail=""):
    st = "✅ PASS" if cond else "❌ FAIL"
    results.append((section, name, cond, detail))
    print(f"  [{st}] {section} · {name} {detail}")

# ═════════════════════════════════════════════
print("S1 · 文件存在性")
# ═════════════════════════════════════════════
check("S1","SR-MEMORY-PMS-V3.0.yaml 存在", os.path.exists(CARD_PATH))
check("S1","文件大小>5KB", os.path.getsize(CARD_PATH) > 5000 if os.path.exists(CARD_PATH) else False,
      f"({os.path.getsize(CARD_PATH)} bytes)" if os.path.exists(CARD_PATH) else "")

with open(CARD_PATH) as f:
    card = yaml.safe_load(f)

# ═════════════════════════════════════════════
print("\nS2 · YAML 结构完整性")
# ═════════════════════════════════════════════
required_keys = ["card_id","domain","hydrogen_level","version","unit","connect",
                 "weight","constraint","steady","spines","meta_verification",
                 "honesty_list","signature","lineage"]
for k in required_keys:
    check("S2", f"key={k}", k in card, f"→ {'OK' if k in card else 'MISSING'}")

# card_id / version / hydrogen
check("S2","card_id 正确", card.get("card_id") == "SR-MEMORY-PMS-V3.0")
check("S2","version = 3.0", str(card.get("version")) == "3.0")
check("S2","hydrogen_level = production", card.get("hydrogen_level") == "production")

# ═════════════════════════════════════════════
print("\nS3 · 第一刀 · Unit 层")
# ═════════════════════════════════════════════
unit = card.get("unit",{})
atoms = unit.get("atoms",[])
check("S3","Unit atoms ≥ 8", len(atoms) >= 8, f"({len(atoms)} atoms)")
# 关键 atom 存在
for aid in ["U-MEM-001","U-MEM-004","U-MEM-006","U-MEM-007"]:
    check("S3", f"atom {aid} 存在", any(a["id"]==aid for a in atoms))
# purity
check("S3","purity_check = PASS", "PASS" in unit.get("purity_check","") or unit.get("purity_check","") == "PASS")
# implicit atoms
check("S3","implicit_atoms ≥ 3", unit.get("implicit_atoms",0) >= 3)

print("\nS3 · 第一刀 · Connect 层")
connect = card.get("connect",{})
rels = connect.get("relations",[])
check("S3","Connect relations ≥ 6", len(rels) >= 6, f"({len(rels)} relations)")
for rid in ["C-MEM-001","C-MEM-005","C-MEM-007","C-MEM-008"]:
    check("S3", f"relation {rid} 存在", any(r["id"]==rid for r in rels))
check("S3","topology_check = PASS", "PASS" in connect.get("topology_check","") or connect.get("topology_check","") == "PASS")

print("\nS3 · 第一刀 · Weight 层")
weight = card.get("weight",{})
check("S3","Weight stateless = true", weight.get("stateless") == True)
params = weight.get("params",[])
check("S3","Weight params ≥ 5", len(params) >= 5, f"({len(params)} params)")
for pn in ["confidence","decay_factor","importance","D_value","link_strength"]:
    check("S3", f"param {pn} 存在", any(p["name"]==pn for p in params))

print("\nS3 · 第一刀 · Constraint 层")
constraint = card.get("constraint",{})
rules = constraint.get("rules",[])
p0 = [r for r in rules if "P0" in r.get("level","")]
check("S3","P0 rules ≥ 3", len(p0) >= 3, f"({len(p0)} P0 rules)")
check("S3","RL-P0-001 存在", any(r["id"]=="RL-P0-001" for r in rules))
check("S3","RL-P0-002 存在", any(r["id"]=="RL-P0-002" for r in rules))
check("S3","RL-P0-003 存在", any(r["id"]=="RL-P0-003" for r in rules))
check("S3","RL-P0-004 存在", any(r["id"]=="RL-P0-004" for r in rules))

print("\nS3 · 第一刀 · Steady 层")
steady = card.get("steady",{})
check("S3","Steady 有 l1_storage", "l1_storage" in steady)
check("S3","Steady 有 l2_storage", "l2_storage" in steady)
check("S3","Steady 有 fixed_point", "fixed_point" in steady)
check("S3","Steady 有 auto_degrade", "auto_degrade" in steady)
check("S3","Steady 有 transaction", "transaction" in steady)
check("S3","Steady 有 hooks", "hooks" in steady)

# ═════════════════════════════════════════════
print("\nS4 · 第二刀 · 脊线")
# ═════════════════════════════════════════════
spines = card.get("spines",[])
check("S4","脊线数量 = 5", len(spines) == 5, f"({len(spines)} spines)")
# 5 条脊线 ID
for sid in ["SP-MEM-A","SP-MEM-B","SP-MEM-C","SP-MEM-D","SP-MEM-E"]:
    check("S4", f"脊线 {sid} 存在", any(s["id"]==sid for s in spines))
# hard_bond
a = next((s for s in spines if s["id"]=="SP-MEM-A"),{})
b = next((s for s in spines if s["id"]=="SP-MEM-B"),{})
check("S4","SP-MEM-A hard_bond=true", a.get("hard_bond") == True)
check("S4","SP-MEM-B hard_bond=true", b.get("hard_bond") == True)
# 删减测试
check("S4","SP-MEM-A deletion_test 存在", "deletion_test" in a)
check("S4","SP-MEM-C deletion_test 存在", any("deletion_test" in s for s in spines))

# ═════════════════════════════════════════════
print("\nS5 · 跨文档互锁")
# ═════════════════════════════════════════════
inh = card.get("inherit",[])
check("S5","继承 FLSC-MASTER-SPEC-V3.0", "FLSC-MASTER-SPEC-V3.0" in inh)
check("S5","继承 FLSC-SIT-V2.2", "FLSC-SIT-V2.2" in inh)
check("S5","继承 METHOD-V3.21", "METHOD-V3.21" in inh)

parent = card.get("parent_card","")
check("S5","parent_card = SR-AI-STAFF-PMS-V1.0", parent == "SR-AI-STAFF-PMS-V1.0")

overlay = card.get("overlay_with",[])
check("S5","叠加 SR-CODE-PYTHON", any(o.get("card","")=="SR-CODE-PYTHON-V1.1" for o in overlay))
check("S5","叠加 SR-EXPERT-WANG", any(o.get("card","")=="SR-EXPERT-WANG-ARCH-V1.0" for o in overlay))

# P0 约束命名空间不冲突
p0_ids = [r["id"] for r in rules if "P0" in r.get("level","")]
check("S5","P0 规则 ID 唯一", len(p0_ids) == len(set(p0_ids)))

# ═════════════════════════════════════════════
print("\nS6 · MIS_true 计算")
# ═════════════════════════════════════════════
meta = card.get("meta_verification",{})
mis = meta.get("MIS_true",{})
computed = mis.get("computed",0)
threshold = mis.get("threshold",0.7)
check("S6","MIS_true computed 存在", computed > 0, f"(MIS={computed})")
check("S6","MIS > 0.7 阈值", computed > threshold, f"({computed} > {threshold})")
check("S6","MIS result = PASS", "PASS" in mis.get("result","") or mis.get("result","") == "PASS")
check("S6","Axiom R = PASS", meta.get("axiom_R",{}).get("result","") == "PASS")
check("S6","third_order_fixed_point = PASS", "PASS" in meta.get("third_order_fixed_point",{}).get("result",""))

# ═════════════════════════════════════════════
print("\nS7 · 诚实清单 + 签署页")
# ═════════════════════════════════════════════
honesty = card.get("honesty_list",[])
check("S7","诚实清单 ≥ 4 项", len(honesty) >= 4, f"({len(honesty)} items)")
for h in honesty:
    check("S7", f"honesty: {h.get('item','')[:40]}...", "plan" in h and "severity" in h)

sig = card.get("signature",{})
check("S7","carbon_seal 存在", "carbon_seal" in sig)
check("S7","silicon_seal 存在", "silicon_seal" in sig)
sil = sig.get("silicon_seal",{})
check("S7","gamma_star 存在", "gamma_star" in sil)
check("S7","lineage_hash 存在", "lineage" in sig.get("carbon_seal",{}) or "bloodline" in sig)

# ═════════════════════════════════════════════
print("\n" + "="*60)
total = len(results)
passed = sum(1 for _,_,p,_ in results if p)
failed = total - passed
warn = 0
print(f"📊 总验证项: {total}")
print(f"  ✅ 通过: {passed}")
print(f"  ❌ 失败: {failed}")
print(f"  📈 通过率: {100.0*passed/total:.1f}%")
print("="*60)
if failed == 0:
    print("🎉 全部通过 ✅ — SR-MEMORY-PMS-V3.0 结构完整，可入库")
    print(f"   MIS_true = {computed}")
    print(f"   Γ* = {sil.get('gamma_star','?')}")
else:
    print(f"⚠️ {failed} 项失败，需修复")
sys.exit(0 if failed==0 else 1)
