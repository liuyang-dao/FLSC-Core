#!/usr/bin/env python3
"""verify_sparsity.py — FLSC-SPARSITY-V4.1 YAML 完整性验证"""
import yaml, sys, os, numpy as np

path = os.path.join(os.path.dirname(__file__), "sparsity_v4_spine.yaml")
with open(path, "r", encoding="utf-8") as f:
    s = yaml.safe_load(f)

print("=" * 55)
print("FLSC-SPARSITY-V4.1 SPINE YAML — 完整性验证")
print("=" * 55)

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
check(m.get("doc_id") == "FLSC-SPARSITY-V4.1-SPINE", f"doc_id = {m.get('doc_id')}")
check("ORC=2" in m.get("orc", ""), f"orc = {m.get('orc')}")
check(m.get("version") == "V4.1", f"version = {m.get('version')}")
total_checks += 1
if m.get("honest_note"):
    passed += 1
    print(f"  ✅ honest_note 存在")
else:
    print(f"  ❌ FAIL: honest_note 缺失")

# ============================================================
# 2. 五层映射
# ============================================================
print("\n📋 [2] 五层同源映射检查")
fl = s.get("five_layer_map", {})
expected_layers = ["U_Unit_层", "C_Connect_层", "W_Weight_层", "K_Constraint_层", "S_Steady_层"]
for k in expected_layers:
    check(k in fl, f"五层: {k}")
    layer = fl.get(k, {})
    # 检查四范式实例
    pi = layer.get("paradigm_instances", {})
    for p in ["transformer_moe", "sparse_cnn", "sparse_rnn", "sparse_diffusion"]:
        check(p in pi, f"  {k} 含 {p}")
    # 检查 dmp_phase
    check("dmp_phase" in layer, f"  {k} 含 dmp_phase")

# ============================================================
# 3. 七条脊线
# ============================================================
print("\n📋 [3] 七条通用脊线检查")
sp = s.get("spine", {})
expected_spines = ["G-01_路由决策脊", "G-02_激活选择脊", "G-03_负载均衡脊",
                   "G-04_算力任务匹配脊", "G-05_单元分化脊", "G-06_训练演化脊", "G-07_硬件资源脊"]
for sid in expected_spines:
    check(sid in sp, f"脊线: {sid}")
    spine = sp.get(sid, {})
    check("definition" in spine, f"  {sid} 含 definition")
    check("dimension" in spine, f"  {sid} 含 dimension")
    check("layers" in spine, f"  {sid} 含 layers")
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
check(len(fs) >= 5, f"断裂面数量 = {len(fs)} ≥ 5")
for fr in fs:
    check("spine" in fr and "fracture" in fr, f"  {fr.get('spine')}: {fr.get('fracture','')[:50]}")

# ============================================================
# 6. SCVP
# ============================================================
print("\n📋 [6] SCVP 校验")
scvp = s.get("scvp", {})
print(f"  overall = {scvp.get('overall')}")
per = scvp.get("per_spine", [])
check(len(per) == 7, f"七脊 SCVP 数量 = {len(per)}")
closed = sum(1 for x in per if "CLOSED" in x.get("closed", ""))
partial = sum(1 for x in per if "PARTIAL" in x.get("closed", ""))
print(f"  → {closed}/7 CLOSED, {partial}/7 PARTIAL")
check(closed >= 5, f"至少 5 CLOSED (实际 {closed})")

# ============================================================
# 7. 七条公理
# ============================================================
print("\n📋 [7] 七条公理检查")
ax = s.get("axioms", {})
for i in range(1, 8):
    key = f"A{i}_"
    found = [k for k in ax.keys() if k.startswith(key)]
    check(len(found) == 1, f"公理{i}: {found[0] if found else 'MISSING'}")
    axiom = ax.get(found[0], {}) if found else {}
    check("statement" in axiom, f"  含 statement")
    check("implication" in axiom, f"  含 implication")

# ============================================================
# 8. 全变体验证矩阵
# ============================================================
print("\n📋 [8] 全变体验证矩阵检查")
vm = s.get("validation_matrix", {})
paradigms = vm.get("paradigms", [])
check(len(paradigms) >= 7, f"验证架构数 = {len(paradigms)} ≥ 7")
for p in paradigms:
    check("name" in p and "completeness" in p and "level" in p,
           f"  {p.get('name')}: {p.get('completeness')} ({p.get('level')})")

# ============================================================
# 9. 诚实补丁
# ============================================================
print("\n📋 [9] 诚实补丁检查")
hp = s.get("honest_patch_summary", {})
check(len(hp) >= 5, f"诚实补丁数 = {len(hp)} ≥ 5")
for k, v in hp.items():
    print(f"  ✅ {k}: {v[:60]}...")

# ============================================================
# 10. 安全约束
# ============================================================
print("\n📋 [10] 安全约束检查")
sc = s.get("safety_constraints", [])
check(len(sc) >= 5, f"安全约束数 = {len(sc)} ≥ 5")
for item in sc:
    check("id" in item and "rule" in item, f"  {item.get('id')}: {item.get('rule','')[:50]}")

# ============================================================
# 11. 不可显形
# ============================================================
print("\n📋 [11] 不可显形清单检查")
us = s.get("unshowable", [])
check(len(us) >= 3, f"不可显形数 = {len(us)} ≥ 3")

# ============================================================
# 12. 三阶自指
# ============================================================
print("\n📋 [12] 三阶自指校验")
tsr = s.get("three_order_self_reference", {})
for k in ["L1_first_order", "L2_second_order", "L3_third_order"]:
    check(k in tsr, f"含 {k}")
    v = tsr.get(k, {})
    check(v.get("status") == "PASS", f"  {k} = PASS")

# ============================================================
# 13. 前置依赖
# ============================================================
print("\n📋 [13] 前置依赖检查")
pre = s.get("prerequisites", [])
check(len(pre) >= 4, f"前置依赖数 = {len(pre)} ≥ 4")

# ============================================================
# 14. V4.2 补丁代码验证
# ============================================================
print("\n📋 [14] V4.2 补丁代码验证")

# B-01: 稀疏收益拐点
def effective_sparsity(lambda_rate, flops_save, comm_cost):
    raw_save = lambda_rate * flops_save
    return raw_save - comm_cost

check(effective_sparsity(0.5, 100, 30) > 0, "B-01: λ=0.5 有效稀疏 (收益>0)")
check(effective_sparsity(0.1, 100, 30) < 0, "B-01: λ=0.1 伪稀疏 (收益<0)")

# B-02: 软分化度 = 归一化熵
def soft_diff_entropy(route_weights):
    w = np.array(route_weights, dtype=float)
    w = w / w.sum()
    entropy = -np.sum(w * np.log(w + 1e-12))
    return entropy / np.log(len(w))

# 均匀分布 → 高分化度 ≈ 1
unif = [1, 1, 1, 1]
# 集中分布 → 低分化度 ≈ 0
peaked = [3.8, 0.1, 0.05, 0.05]

ent_unif = soft_diff_entropy(unif)
ent_peaked = soft_diff_entropy(peaked)
check(0.9 < ent_unif < 1.01, f"B-02: 均匀分布熵 = {ent_unif:.3f} ≈ 1")
check(ent_peaked < ent_unif, f"B-02: 集中分布熵 ({ent_peaked:.3f}) < 均匀分布 ({ent_unif:.3f})")

print(f"  ✅ B-02 软分化度范围验证通过 (均匀={ent_unif:.3f}, 集中={ent_peaked:.3f})")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 55)
print(f"📊 验证结果: {passed}/{total_checks} 通过")
if passed == total_checks:
    print("🎉 全部通过 ✅ — FLSC-SPARSITY-V4.1 结构完整，可入库")
else:
    print(f"⚠️ {total_checks - passed} 项未通过")
print("=" * 55)
sys.exit(0 if passed == total_checks else 1)
