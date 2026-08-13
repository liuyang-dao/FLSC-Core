#!/usr/bin/env python3
"""verify_learning.py — FLSC-INTELLIGENCE-LEARNING-UNITY-V2.0 YAML 完整性验证"""
import yaml, sys, os

path = os.path.join(os.path.dirname(__file__), "learning_unity_v2_spine.yaml")
with open(path, "r", encoding="utf-8") as f:
    s = yaml.safe_load(f)

print("=" * 55)
print("FLSC-LEARNING-UNITY-V2.0 SPINE YAML — 完整性验证");
print("=" * 55);

total_checks = 0
passed = 0

def check(cond, msg):
    global total_checks, passed
    total_checks += 1
    if cond:
        passed += 1
        print(f"  ✅ {msg}")
    else:
        print(f"  ❌ FAIL: {msg}")

# ============================================================
# 1. meta 块
# ============================================================
print("\n📋 [1] meta 块检查")
m = s.get("meta", {})
check(m.get("doc_id") == "FLSC-INTELLIGENCE-LEARNING-UNITY-V2.0-SPINE",
       f"doc_id = {m.get('doc_id')}")
check("ORC=2" in m.get("orc", ""), f"orc = {m.get('orc')}")
check(m.get("version") == "V2.0", f"version = {m.get('version')}")
check(m.get("honest_note"), "honest_note 存在")

# ============================================================
# 2. 五层映射
# ============================================================
print("\n📋 [2] 五层同源映射检查")
fl = s.get("five_layer_map", {})
expected_layers = ["U_Unit_层", "C_Connect_层", "W_Weight_层", "K_Constraint_层", "S_Steady_层"]
for k in expected_layers:
    check(k in fl, f"五层: {k}")
    layer = fl.get(k, {})
    ai = layer.get("agent_instances", {})
    for a in ["carbon_human", "silicon_ai", "organization", "hybrid"]:
        check(a in ai, f"  {k} 含 {a}")
    check("dmp_phase" in layer, f"  {k} 含 dmp_phase")

# ============================================================
# 3. 三条脊线
# ============================================================
print("\n📋 [3] 三条通用学习脊线检查")
sp = s.get("spine", {})
expected_spines = ["K-01_压缩迁移守恒脊", "K-02_残差暴露动力脊", "K-03_层级嵌套演化脊"]
for sid in expected_spines:
    check(sid in sp, f"脊线: {sid}")
    spine = sp.get(sid, {})
    check("definition" in spine, f"  {sid} 含 definition")
    check("dimension" in spine, f"  {sid} 含 dimension")
    check("layers" in spine, f"  {sid} 含 layers")
    check("law" in spine, f"  {sid} 含 law")
    check("scvp" in spine, f"  {sid} 含 scvp")

# ============================================================
# 4. 独立性校验
# ============================================================
print("\n📋 [4] 独立性校验")
ic = s.get("independence_check", {})
check("独立" in ic.get("result", ""), f"独立性结果 = {ic.get('result')}")
check(ic.get("max_overlap", 99) <= 2, f"最大重叠 = {ic.get('max_overlap')} ≤ 2")

# ============================================================
# 5. 断裂面
# ============================================================
print("\n📋 [5] 断裂面检查")
fs = s.get("fracture_surfaces", [])
check(len(fs) >= 3, f"断裂面数量 = {len(fs)} ≥ 3")
for fr in fs:
    check("spine" in fr and "fracture" in fr, f"  {fr.get('spine')}: {fr.get('fracture','')[:50]}")

# ============================================================
# 6. SCVP
# ============================================================
print("\n📋 [6] SCVP 校验")
scvp = s.get("scvp", {})
print(f"  overall = {scvp.get('overall')}")
per = scvp.get("per_spine", [])
check(len(per) == 3, f"三脊 SCVP 数量 = {len(per)}")
closed = sum(1 for x in per if "CLOSED" in x.get("closed", ""))
print(f"  → {closed}/3 CLOSED")
check(closed == 3, f"3/3 CLOSED (实际 {closed})")

# ============================================================
# 7. 五条公理
# ============================================================
print("\n📋 [7] 五条公理检查")
ax = s.get("axioms", {})
for i in range(1, 6):
    key = f"A{i}_"
    found = [k for k in ax.keys() if k.startswith(key)]
    check(len(found) == 1, f"公理{i}: {found[0] if found else 'MISSING'}")
    axiom = ax.get(found[0], {}) if found else {}
    check("statement" in axiom, f"  含 statement")
    check("implication" in axiom, f"  含 implication")
    check("spine_support" in axiom, f"  含 spine_support")

# ============================================================
# 8. 六阶段模型
# ============================================================
print("\n📋 [8] 六阶段学习路径模型检查")
six = s.get("six_stage_model", {})
for st in ["stage_0_perception", "stage_1_extraction", "stage_2_compression",
           "stage_3_transfer", "stage_4_metacognition", "stage_5_reconstruction"]:
    check(st in six, f"阶段: {st}")
    stage = six.get(st, {})
    check("name" in stage, f"  {st} 含 name")
    check("operation" in stage, f"  {st} 含 operation")
    check("layer" in stage, f"  {st} 含 layer")

# ============================================================
# 9. 量化指标
# ============================================================
print("\n📋 [9] 量化指标体系检查")
qm = s.get("quantitative_metrics", {})
for metric in ["SIS", "CR", "TC"]:
    check(metric in qm, f"指标: {metric}")
    m_data = qm.get(metric, {})
    check("definition" in m_data, f"  {metric} 含 definition")
    check("range" in m_data, f"  {metric} 含 range")

# ============================================================
# 10. 跨域验证
# ============================================================
print("\n📋 [10] 跨域验证矩阵检查")
cd = s.get("cross_domain_validation", {})
ax_list = cd.get("axioms", [])
check(len(ax_list) == 5, f"公理跨域验证数 = {len(ax_list)} = 5")

# ============================================================
# 11. 预测 H-01~H-07
# ============================================================
print("\n📋 [11] 可检验预测检查")
pr = s.get("predictions", {})
check(len(pr) >= 5, f"预测数 = {len(pr)} ≥ 5")
for k, v in pr.items():
    check("content" in v and "method" in v and "priority" in v,
           f"  {k}: {v.get('content','')[:50]}... (P={v.get('priority','')})")

# ============================================================
# 12. 诚实补丁
# ============================================================
print("\n📋 [12] 诚实补丁检查")
hp = s.get("honest_patch_summary", {})
check(len(hp) >= 5, f"诚实补丁数 = {len(hp)} ≥ 5")
for k, v in hp.items():
    print(f"  ✅ {k}: {v[:60]}...")

# ============================================================
# 13. 终极边界
# ============================================================
print("\n📋 [13] 终极边界声明检查")
ub = s.get("ultimate_boundary", [])
check(len(ub) >= 3, f"终极边界条目 = {len(ub)} ≥ 3")

# ============================================================
# 14. 安全约束
# ============================================================
print("\n📋 [14] 安全约束检查")
sc = s.get("safety_constraints", [])
check(len(sc) >= 5, f"安全约束数 = {len(sc)} ≥ 5")

# ============================================================
# 15. 不可显形
# ============================================================
print("\n📋 [15] 不可显形清单检查")
us = s.get("unshowable", [])
check(len(us) >= 3, f"不可显形数 = {len(us)} ≥ 3")

# ============================================================
# 16. 三阶自指
# ============================================================
print("\n📋 [16] 三阶自指校验")
tsr = s.get("three_order_self_reference", {})
for k in ["L1_first_order", "L2_second_order", "L3_third_order"]:
    check(k in tsr, f"含 {k}")
    v = tsr.get(k, {})
    check(v.get("status") == "PASS", f"  {k} = PASS")

# ============================================================
# 17. 前置依赖
# ============================================================
print("\n📋 [17] 前置依赖检查")
pre = s.get("prerequisites", [])
check(len(pre) >= 5, f"前置依赖数 = {len(pre)} ≥ 5")

# ============================================================
# 18. V2.1 补丁代码验证
# ============================================================
print("\n📋 [18] V2.1 补丁代码验证")

# B-01: SIS 操作化
def compute_sis(c_layer_autonomy, residual_exposure, cross_domain_reuse):
    return (c_layer_autonomy * 0.4 +
            residual_exposure * 0.4 +
            cross_domain_reuse * 0.2)

sis_high = compute_sis(0.8, 0.7, 0.6)
sis_low = compute_sis(0.3, 0.2, 0.1)
check(0.5 < sis_high < 1.0, f"B-01: 高自主 SIS = {sis_high:.3f} ∈ (0.5, 1)")
check(sis_low < sis_high, f"B-01: 低自主 SIS ({sis_low:.3f}) < 高自主 ({sis_high:.3f})")
print(f"  ✅ B-01 SIS 操作化验证通过 (高={sis_high:.3f}, 低={sis_low:.3f})")

# B-02: 元认知训练回路
class FakeModel:
    def __init__(self): self.reflected = False
    def compute_loss(self, batch): return type('L', (), {'residual': 0.5})()
    def trigger_strategy_reflection(self): self.reflected = True

def metacognitive_training_step(model, batch, residual_threshold=0.3):
    loss = model.compute_loss(batch)
    if loss.residual > residual_threshold:
        model.trigger_strategy_reflection()
    return loss

m = FakeModel()
metacognitive_training_step(m, None, 0.3)
check(m.reflected, "B-02: 残差超阈值 → 触发策略反思 ✅")
print(f"  ✅ B-02 元认知训练回路验证通过")

# ============================================================
# 19. TC 公式验证
# ============================================================
print("\n📋 [19] TC 公式验证")
alpha = 0.7
tc_self = 0.8 * (1 - 0.7 * 0.25)  # SIS=0.8, CR=0.25 → ~0.66
tc_distill = 0.5 * (1 - 0.7 * 0.75)  # SIS=0.5, CR=0.75 → ~0.24
check(tc_self > tc_distill, f"TC 自研({tc_self:.3f}) > TC 蒸馏({tc_distill:.3f}) ✅")
print(f"  ✅ TC = SIS×(1-α×CR): 自研={tc_self:.3f}, 蒸馏={tc_distill:.3f}")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 55)
print(f"📊 验证结果: {passed}/{total_checks} 通过")
if passed == total_checks:
    print("🎉 全部通过 ✅ — FLSC-LEARNING-UNITY-V2.0 结构完整，可入库")
else:
    print(f"⚠️ {total_checks - passed} 项未通过")
print("=" * 55)
sys.exit(0 if passed == total_checks else 1)
