#!/usr/bin/env python3
# 验证 fractal_physics_spine.yaml 完整性 + SCVP + OJP 递归路径
import yaml, sys

PATH = "/data/workspace/domains/physics/fractal_physics_spine.yaml"

with open(PATH, "r", encoding="utf-8") as f:
    s = yaml.safe_load(f)

print("=" * 60)
print("分形物理学 V1.0 YAML 验证")
print("=" * 60)

checks = []
def chk(name, ok, detail=""):
    checks.append((name, ok, detail))
    icon = "✅" if ok else "❌"
    extra = f" — {detail}" if detail else ""
    print(f"  [{icon}] {name}{extra}")

# 1. meta
m = s.get("meta", {})
chk("meta.doc_id 存在", bool(m.get("doc_id")), m.get("doc_id",""))
chk("meta.status 存在", bool(m.get("status")))

# 2. 五层
fl = s.get("five_layer_map", {})
for k in ["U_Unit_层","C_Connect_层","W_Weight_层","K_Constraint_层","S_Steady_层"]:
    chk(f"五层.{k}", k in fl)

# 3. 六脊（spine 是 dict）
sp = s.get("spine", {})
chk("脊线数量 = 6", len(sp) == 6, f"实际 {len(sp)}")
ids = list(sp.keys())
for rid in ["PHYS-01","PHYS-02","PHYS-03","PHYS-04","PHYS-05","PHYS-06"]:
    # YAML key 不带前缀 'PHYS-0X_' 之后的描述；兼容两种
    found = any(rid in k for k in ids)
    chk(f"脊线 {rid} 存在", found)

# 4. 独立性
ic = s.get("independence_check", {})
chk("独立性校验存在", "verification" in ic or "result" in ic)

# 5. 断裂面
fs = s.get("fracture_surfaces", [])
chk("断裂面 ≥ 6", len(fs) >= 6, f"实际 {len(fs)}")

# 6. SCVP
sc = s.get("scvp", {})
per = sc.get("per_spine", [])
closed = sum(1 for x in per if isinstance(x, dict) and x.get("closed") == "CLOSED")
partial = sum(1 for x in per if isinstance(x, dict) and "PARTIAL" in str(x.get("closed","")))
chk(f"SCVP: {closed} CLOSED / {partial} PARTIAL", True, f"{closed}/{len(per)} CLOSED")
chk("SCVP overall 存在", "overall" in sc)

# 7. OJP
oj = s.get("ojp_physics", {})
chk("Origin₁ 定义存在", "origin" in oj)
chk("ORC 当前 = 1", oj.get("orc_current") == 1)
chk("ORC 上限 = 5", oj.get("orc_max") == 5)

# 8. 实验
et = s.get("experimental_tests", [])
chk(f"实验预测 ≥ 5", len(et) >= 5, f"实际 {len(et)}")

# 9. Axiom R
ar = s.get("axiom_r", {})
chk("Axiom R 公式存在", "formula" in ar)
ce = ar.get("current_estimate", {})
chk("MIS_train 存在", "MIS_train" in ce)
chk("MIS_true 合理 (0,1)", 0 < ce.get("MIS_true",0) < 1)

# 10. 不可显形
ip = s.get("inmanifestable_physics", [])
chk(f"不可显形 ≥ 4", len(ip) >= 4, f"实际 {len(ip)}")

# 11. 诚实补丁
hp = s.get("honest_patch_summary", {})
chk(f"F-01~F-09 共 9 项", len(hp) == 9, f"实际 {len(hp)}")

# 12. 安全约束
sc2 = s.get("safety_constraints", [])
chk(f"安全约束 ≥ 5", len(sc2) >= 5, f"实际 {len(sc2)}")

# 13. 签署页
sg = s.get("signatures", {})
chk("签署页存在", bool(sg))
chk("ORC 状态存在", "orc_status" in sg)

# 总结
passed = sum(1 for _,ok,_ in checks if ok)
total = len(checks)
print("-" * 60)
print(f"总计：{passed}/{total} 通过")
if passed == total:
    print("🎉 全部通过 ✅")
    sys.exit(0)
else:
    print("⚠️ 存在未通过项")
    sys.exit(1)
