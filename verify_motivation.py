#!/usr/bin/env python3
"""验证 FLSC Motivation V2.2 + Three Core Requirements 完整性"""
import os, re, yaml

print("=" * 60)
print("FLSC Motivation V2.2 + Three Core Requirements 验证")
print("=" * 60)

# 1. 检查 meta_arch_v1.md
path = "/data/workspace/spine/meta_arch_v1.md"
with open(path) as f:
    content = f.read()
print(f"\n[✓] {path}")
print(f"    行数: {len(content.splitlines())}")
assert "形而下之道的结构显形语法" in content, "副标题缺失"
print("    ✓ 副标题: 形而下之道的结构显形语法")
assert "Γ*" in content, "Γ* 算子缺失"
print("    ✓ Γ* 递归算子对接")
assert "Origin₁" in content, "Origin₁ 缺失"
print("    ✓ Origin₁ 不可约公理")

# 2. 检查 smt_v2.2_motivation.md
path = "/data/workspace/domains/meta/smt_v2.2_motivation.md"
with open(path) as f:
    content = f.read()
print(f"\n[✓] {path}")
print(f"    行数: {len(content.splitlines())}")
assert "为何显形" in content
print("    ✓ 扉页动机: 为何显形")
assert "形而下之道的结构捕捉" in content
print("    ✓ 扉页动机: 形而下之道的结构捕捉")
assert ("Γ*" in content) or ("Γ\\*" in content), "Γ* 引用缺失"
print("    ✓ Γ* 引用")

# 3. 检查 FLSC_Three_Core_Requirements.md
path = "/data/workspace/FLSC_Three_Core_Requirements.md"
with open(path) as f:
    content = f.read()
print(f"\n[✓] {path}")
print(f"    行数: {len(content.splitlines())}")
# 三大核心检查
for keyword, label in [
    ("锚定原点", "第一核心: 锚定原点 + OJP"),
    ("五层同源语法", "第二核心: 五层语法"),
    ("全域分形映射", "第三核心: 全域分形映射"),
    ("缺一不可", "缺一不可判定"),
    ("Origin₁", "Origin₁ 引用"),
    ("Γ*", "Γ* 引用"),
    ("ORC", "ORC 递归控制器"),
    ("Axiom T-1", "Axiom T-1 原点锚定公理"),
    ("Axiom T-2", "Axiom T-2 五层完备公理"),
    ("Axiom T-3", "Axiom T-3 分形全覆盖公理"),
    ("Axiom T-4", "Axiom T-4 递归终止公理"),
]:
    assert keyword in content, f"缺失: {label}"
    print(f"    ✓ {label}")

print("\n" + "=" * 60)
print("全部验证通过 ✅")
print("=" * 60)
print("""
交付清单:
  spine/meta_arch_v1.md                    副标题版（道器之脊）
  domains/meta/smt_v2.2_motivation.md    扉页动机页
  FLSC_Three_Core_Requirements.md         三大核心要求（宪法级）
""")
