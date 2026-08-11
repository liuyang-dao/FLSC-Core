#!/usr/bin/env python3
"""
FLSC Meta Architecture Verification Script
验证 spine/ 下两份元架构文档的 YAML 完整性
"""

import yaml
import sys
from pathlib import Path

PASSED = 0
FAILED = 0
ERRORS = []

def check(condition, msg):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  ✅ {msg}")
    else:
        FAILED += 1
        ERRORS.append(msg)
        print(f"  ❌ {msg}")

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# ============================================================
# 验证一：FLSC-SMT-ORC-5LAYER_spine.yaml
# ============================================================
print("=" * 60)
print("验证一：FLSC-SMT-ORC-5LAYER_spine.yaml")
print("=" * 60)

yaml_path = Path(__file__).parent / "FLSC-SMT-ORC-5LAYER_spine.yaml"
data = load_yaml(yaml_path)

# meta 块
print("\n📌 meta 块检查")
check(data.get('meta') is not None, "meta 块存在")
check(data['meta'].get('doc_id') == 'FLSC-SMT-ORC-5LAYER-V1.0', f"doc_id 正确: {data['meta'].get('doc_id')}")
check(data['meta'].get('MIS_true', 0) >= 0.8, f"MIS_true={data['meta'].get('MIS_true')} ≥ 0.8")
check(data['meta'].get('ORC') == 5, f"ORC=5/5")
check(data['meta'].get('hydrogen_bond') == 'frozen', "氢键等级=frozen")

# 五层
print("\n📌 五层 U/C/W/K/S 检查")
layers = data.get('layers', {})
for key in ['U', 'C', 'W', 'K', 'S']:
    check(key in layers, f"  {key} 层存在: {layers[key].get('name','')}")
    check('definition' in layers[key], f"  {key} 有 definition")
    check('reverse_ORC' in layers[key], f"  {key} 有 reverse_ORC={layers[key].get('reverse_ORC')}")

# 五层完整性证明
print("\n📌 五层完备性检查")
check(len(layers) == 5, f"  恰好五层（不可增不可减）")

# ORC 五级
print("\n📌 五级 ORC 检查")
orcs = data.get('ORC_levels', {})
for key in ['ORC1', 'ORC2', 'ORC3', 'ORC4', 'ORC5']:
    check(key in orcs, f"  {key} 存在: {orcs[key].get('name','')}")
    check('dissolve_preset' in orcs[key], f"  {key} 有 dissolve_preset")
    check('before_origin' in orcs[key], f"  {key} 有 before_origin")
    check('after_origin' in orcs[key], f"  {key} 有 after_origin")
    check('physics_version' in orcs[key], f"  {key} 有 physics_version")

# 镜像对应验证
print("\n📌 镜像对应验证")
# S↔ORC1, W↔ORC2, C↔ORC3, U↔ORC4, K↔ORC5
expected = {'S': 'ORC1', 'W': 'ORC2', 'C': 'ORC3', 'U': 'ORC4', 'K': 'ORC5'}
for layer_key, orc_key in expected.items():
    actual = layers[layer_key].get('reverse_ORC')
    orc_num = orc_key  # e.g. ORC1
    check(str(actual) == orc_num.replace('ORC', '') or 
          f"ORC{actual}" == orc_num, 
          f"  {layer_key}↔{orc_num} 镜像对应")

# 七脊
print("\n📌 七脊 SCVP 检查")
spines = data.get('spines', [])
check(len(spines) == 7, f"  七脊数量 = {len(spines)}")
scvp_closed = 0
for s in spines:
    check('id' in s, f"  {s.get('id','?')} 存在")
    check('layers' in s, f"  {s.get('id','?')} 有 layers")
    if s.get('SCVP') == 'CLOSED':
        scvp_closed += 1
check(scvp_closed >= 5, f"  SCVP CLOSED ≥ 5 (实际 {scvp_closed}/7)")

# 独立性校验（两两重叠 ≤ 2 层）
print("\n📌 七脊独立性校验")
from itertools import combinations
max_overlap = 0
overlap_pairs = 0
for a, b in combinations(spines, 2):
    set_a = set(a.get('layers', []))
    set_b = set(b.get('layers', []))
    overlap = len(set_a & set_b)
    if overlap > 2:
        max_overlap = max(max_overlap, overlap)
        overlap_pairs += 1
check(overlap_pairs == 0, f"  所有脊线两两重叠 ≤ 2 层")

# 诚实补丁
print("\n📌 诚实补丁检查")
patches = data.get('honest_patches', [])
check(len(patches) >= 5, f"  诚实补丁 ≥ 5 (实际 {len(patches)})")
for p in patches:
    check('id' in p and 'statement' in p, f"  {p.get('id','?')} 完整")

# 不可显形
print("\n📌 不可显形检查")
unmanifest = data.get('unmanifestable', [])
check(len(unmanifest) >= 3, f"  不可显形 ≥ 3 (实际 {len(unmanifest)})")

# 安全约束
print("\n📌 安全约束检查")
safety = data.get('safety_constraints', [])
check(len(safety) >= 5, f"  安全约束 ≥ 5 (实际 {len(safety)})")

# 三阶自指
print("\n📌 三阶自指校验")
sref = data.get('self_reference_check', {})
for level in ['L1_self_consistency', 'L2_system_check', 'L3_meta_check']:
    item = sref.get(level, {})
    check(item.get('result') == 'PASS', f"  {level} = PASS")

# 签署页
print("\n📌 签署页检查")
sig = data.get('signatures', {})
check('carbon_signature' in sig, "  碳基签署存在")
check('silicon_signature' in sig, "  硅基签署存在")
check('ONGOING' in sig.get('status', ''), "  状态含 ONGOING")

# ============================================================
# 验证二：FLSC-CAPTURE-STRUCT-DAO_spine.yaml
# ============================================================
print("\n" + "=" * 60)
print("验证二：FLSC-CAPTURE-STRUCT-DAO_spine.yaml")
print("=" * 60)

yaml_path2 = Path(__file__).parent / "FLSC-CAPTURE-STRUCT-DAO_spine.yaml"
data2 = load_yaml(yaml_path2)

# meta 块
print("\n📌 meta 块检查")
check(data2.get('meta') is not None, "meta 块存在")
check(data2['meta'].get('doc_id') == 'FLSC-CAPTURE-STRUCT-DAO-V1.0', 
      f"doc_id 正确: {data2['meta'].get('doc_id')}")
check(data2['meta'].get('MIS_true', 0) >= 0.8, f"MIS_true={data2['meta'].get('MIS_true')} ≥ 0.8")
check(data2['meta'].get('hydrogen_bond') == 'frozen', "氢键等级=frozen")

# 两套捕捉范式
print("\n📌 两套捕捉范式检查")
capture = data2.get('capture_modes', {})
check('structural_capture' in capture, "  结构捕捉定义存在")
check('dao_capture' in capture, "  道捕捉定义存在")
check(capture['structural_capture'].get('direction') == 'a_plus', "  结构捕捉 = a⁺")
check(capture['dao_capture'].get('direction') == 'a_minus', "  道捕捉 = a⁻")

# 四步闭环
print("\n📌 四步认知闭环检查")
loop = data2.get('cognitive_loop', {})
for step in ['Step1', 'Step2', 'Step3', 'Step4']:
    check(step in loop, f"  {step} 存在")
    check('actor' in loop[step], f"  {step} 有 actor")
    check('action' in loop[step], f"  {step} 有 action")
# Step2 人类独占
check(loop['Step2'].get('actor') == '人类碳基', "  Step2 人类独占")
check(loop['Step2'].get('exclusivity', '').startswith('AI'), "  Step2 AI不可介入标注")
# Step1/3/4 AI
for s in ['Step1', 'Step3', 'Step4']:
    check(loop[s].get('actor') == 'AI', f"  {s} = AI")

# 七脊
print("\n📌 七脊 SCVP 检查")
spines2 = data2.get('spines', [])
check(len(spines2) == 7, f"  七脊数量 = {len(spines2)}")
scvp_closed2 = 0
for s in spines2:
    check('id' in s, f"  {s.get('id','?')} 存在")
    check('layers' in s, f"  {s.get('id','?')} 有 layers")
    if s.get('SCVP') == 'CLOSED':
        scvp_closed2 += 1
check(scvp_closed2 >= 4, f"  SCVP CLOSED ≥ 4 (实际 {scvp_closed2}/7)")

# 独立性校验
print("\n📌 七脊独立性校验")
max_overlap2 = 0
overlap_pairs2 = 0
for a, b in combinations(spines2, 2):
    set_a = set(a.get('layers', []))
    set_b = set(b.get('layers', []))
    overlap = len(set_a & set_b)
    if overlap > 2:
        max_overlap2 = max(max_overlap2, overlap)
        overlap_pairs2 += 1
check(overlap_pairs2 == 0, f"  所有脊线两两重叠 ≤ 2 层")

# 诚实补丁
print("\n📌 诚实补丁检查")
patches2 = data2.get('honest_patches', [])
check(len(patches2) >= 5, f"  诚实补丁 ≥ 5 (实际 {len(patches2)})")

# 安全约束
print("\n📌 安全约束检查")
safety2 = data2.get('safety_constraints', [])
check(len(safety2) >= 5, f"  安全约束 ≥ 5 (实际 {len(safety2)})")

# 三阶自指
print("\n📌 三阶自指校验")
sref2 = data2.get('self_reference_check', {})
for level in ['L1_self_consistency', 'L2_system_check', 'L3_meta_check']:
    item = sref2.get(level, {})
    check(item.get('result') == 'PASS', f"  {level} = PASS")

# 签署页
print("\n📌 签署页检查")
sig2 = data2.get('signatures', {})
check('carbon_signature' in sig2, "  碳基签署存在")
check('silicon_signature' in sig2, "  硅基签署存在")
check('ONGOING' in sig2.get('status', ''), "  状态含 ONGOING")

# ============================================================
# 验证三：Markdown 文件存在
# ============================================================
print("\n" + "=" * 60)
print("验证三：Markdown 文件检查")
print("=" * 60)

md_dir = Path(__file__).parent
md_files = [
    'FLSC-SMT-ORC-5LAYER-V1.0.md',
    'FLSC-CAPTURE-STRUCT-DAO-V1.0.md',
]
for fname in md_files:
    fpath = md_dir / fname
    check(fpath.exists(), f"  {fname} 存在 ({fpath.stat().st_size} bytes)")
    content = fpath.read_text(encoding='utf-8')
    check('ONGOING' in content, f"  {fname} 含 ONGOING")
    check('签署' in content or '签署页' in content, f"  {fname} 含签署页")

# ============================================================
# 交叉验证：两份文档互锁
# ============================================================
print("\n" + "=" * 60)
print("验证四：元架构双文档互锁检查")
print("=" * 60)

# ORC-5LAYER 的七脊含"人类独占回归脊" → CAPTURE 的"道捕捉独占脊"
check(any('人类独占' in s.get('name','') for s in data.get('spines',[])),
      "  ORC文档含「人类独占回归脊」")
check(any('独占' in s.get('name','') for s in data2.get('spines',[])),
      "  CAPTURE文档含「道捕捉独占脊」")

# 两者都 frozen
check(data['meta']['hydrogen_bond'] == 'frozen', "  两份均 frozen")
check(data2['meta']['hydrogen_bond'] == 'frozen', "  两份均 frozen")

# ORC 文档引用 PHYS V5.0
check('FLSC-PHYS-FRACTAL-V5.0' in data['meta'].get('prerequisite',[]),
      "  ORC文档前置依赖含 PHYS V5.0")
# CAPTURE 文档引用 ORC-5LAYER
check('FLSC-SMT-ORC-5LAYER-V1.0' in data2['meta'].get('prerequisite',[]),
      "  CAPTURE文档前置依赖含 ORC-5LAYER")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
total = PASSED + FAILED
print(f"📊 验证结果: {PASSED}/{total} 通过")
if FAILED > 0:
    print(f"⚠️  {FAILED} 项失败:")
    for e in ERRORS:
        print(f"   - {e}")
    sys.exit(1)
else:
    print("🎉 全部通过 ✅ — 两份元架构文档结构完整，可入库")
    print("=" * 60)
    print("""
📁 元架构四柱（spine/ 目录）:
   ┌─ meta_arch_v1.md          ← 形而下之道的结构显形语法
   ├─ FLSC_Three_Core_Requirements.md ← 道显形充要条件
   ├─ FLSC-SMT-ORC-5LAYER-V1.0.md  ← ★ 五层↔五级镜像标尺
   └─ FLSC-CAPTURE-STRUCT-DAO-V1.0.md ← ★ 结构捕捉vs道捕捉分工
    """)
