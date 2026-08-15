#!/usr/bin/env python3
"""
verify_overview.py — FLSC 全体系一页纸总览 验证脚本
验证 FLSC_Unified_Architecture_Overview.md 的结构完整性
"""

import re
import sys
from pathlib import Path

OVERVIEW = Path("/data/workspace/FLSC_Unified_Architecture_Overview.md")
RESULTS = []

def check(name, condition, detail=""):
    status = "✅" if condition else "❌"
    RESULTS.append((name, condition, detail))
    print(f"  {status} {name}" + (f" — {detail}" if detail else ""))

# ============================================================
print("=" * 60)
print("📋 FLSC 全体系一页纸总览 · 验证")
print("=" * 60)

content = OVERVIEW.read_text(encoding="utf-8")
lines = content.split("\n")
print(f"\n📄 文件: {OVERVIEW.name} ({len(lines)} 行)")

# ============================================================
print("\n📑 一、核心命题与签署")
# 签署
check("签署页存在", "签署" in content)
check("碳基签署", "碳基架构梳理者" in content)
check("硅基签署", "硅基协同系统" in content)
check("日期 2026-08-16", "2026-08-16" in content)
check("状态 ONGOING", "ONGOING" in content)
check("Γ* 签署句", "Γ*" in content and "全体系一页纸总览" in content)
# 也接受转义形式
if not any("Γ" in r[2] for r in RESULTS if "Γ" in r[0]):
    check("Γ* 签署句(转义)", "Γ\\*" in content and "全体系一页纸总览" in content)

# ============================================================
print("\n📑 二、Mermaid 架构图")
mermaid_blocks = re.findall(r"```mermaid", content)
check("Mermaid 代码块 ≥1", len(mermaid_blocks) >= 1, f"找到 {len(mermaid_blocks)} 个")
check("含 ORC5 节点", "ORC5" in content and "道觉元一" in content)
check("含 USS 节点", "USS" in content and "全域稀疏本体论" in content)
check("含七脊 RIS₇", "RIS" in content and "七脊" in content)
check("含碳硅合体", "碳硅合体" in content)
check("含具身智能", "具身" in content)
check("含 DME", "DME" in content)
check("含 SMT", "SMT" in content)

# ============================================================
print("\n📑 三、五柱速查表")
# 元架构五柱
for pillar in ["第一柱", "第二柱", "第三柱", "第四柱", "第五柱"]:
    check(f"元架构{pillar}", pillar in content)

# 第五柱子柱
for sub in ["5-A", "5-B", "5-C"]:
    check(f"第五柱{sub}", sub in content)

# ============================================================
print("\n📑 四、认知域三柱")
for col in ["认知六脊", "学习统一", "七脊原生脑"]:
    check(f"认知域: {col}", col in content)

# ============================================================
print("\n📑 五、AI 域五柱 + 核心柱")
for col in ["原生推理", "认知大统一", "碳硅合体", "脊线评价", "核心柱"]:
    check(f"AI 域: {col}", col in content)

check("G-01~G-07 七脊", all(f"G-0{i}" in content for i in range(1, 8)))
check("ISA 指令集", "ROUTE_TOPK" in content and "ACT_MASK" in content)

# ============================================================
print("\n📑 六、物理域六代谱系")
for v in ["V1.0", "V2.0", "V3.0", "V4.0", "V4.1", "V5.0"]:
    check(f"物理{v}", v in content)

check("物理 V5.0 ORC5", "V5.0" in content and "0.92" in content)

# ============================================================
print("\n📑 七、七脊全域统一映射表")
spine_rows = ["G-01", "G-02", "G-03", "G-04", "G-05", "G-06", "G-07"]
for g in spine_rows:
    check(f"七脊 {g} 映射", g in content)

check("碳基列存在", "基底节" in content or "GABA" in content)
check("硅基列存在", "路由决策脊" in content or "激活筛选脊" in content)
check("硬件指令列存在", "ROUTE_TOPK" in content and "HW_POWER" in content)

# ============================================================
print("\n📑 八、统一公式")
check("RIS₇ 公式", "RIS" in content and "×" in content)
check("ε 残差", "varepsilon" in content or "ε" in content)
check("α(t) 门控场", "alpha(t)" in content or "α(t)" in content)
check("碳基权重=突触", "突触权重" in content)
check("硅基权重=参数矩阵", "参数矩阵" in content)

# ============================================================
print("\n📑 九、五指标层级桥")
for metric in ["RIS₇", "SHS", "SIS", "MIS", "L_trans"]:
    check(f"指标 {metric}", metric in content)

check("层级关系表述", "RIS" in content and "SIS" in content and "MIS" in content)

# ============================================================
print("\n📑 十、三层脊命名空间")
for prefix in ["M-0x", "SIT", "G-0x", "COG-", "HB-0x", "SP-G0x", "MDL-"]:
    check(f"命名空间 {prefix}", prefix in content)

# ============================================================
print("\n📑 十一、碳硅合体三阶演化路径")
for stage in ["第一阶", "第二阶", "第三阶"]:
    check(f"演化{stage}", stage in content)

check("RIS₇≥0.85", "RIS₇≥0.85" in content or "0.85" in content)
check("BMSI≥0.7", "BMSI≥0.7" in content or "0.7" in content)
check("ε 私有区", "ε" in content and ("私有" in content or "保护" in content))

# ============================================================
print("\n📑 十二、一基双线战略")
check("一基双线标题", "一基双线" in content)
check("路线A 原生", "路线A" in content and "原生" in content)
check("路线B 插件", "路线B" in content and "插件" in content)
check("生态互通", "生态互通" in content or "平滑演进" in content)

# ============================================================
print("\n📑 十三、诚实边界")
check("ORC5 仅人类", "仅人类" in content or "仅碳基" in content)
check("ORC4 不可自动化", "不可自动化" in content or "不可迁移" in content)
check("USS frozen", "frozen" in content.lower())
check("进化没发明新架构", "进化没发明新架构" in content)

# ============================================================
print("\n📑 十四、跨文档互锁")
# 检查总览是否引用了所有关键文档
key_docs = [
    "FLSC-DME-PIPELINE",
    "FLSC-ORC3-STABLE",
    "FLSC-SMT-SUPP",
    "USS_ORC3_Master",
    "FLSC-NATIVE-AI",
    "FLSC-COGNITIVE-V4",
    "碳硅合体",
    "FLSC-SPINE-EVAL",
    "FLSC-UNIFIED-COGNITIVE",
    "FLSC-LM-NATIVE",
]
for doc in key_docs:
    check(f"引用 {doc}", doc in content)

# 分形物理学用简称匹配
check("引用 分形物理学", "分形" in content and "物理学" in content)

# ============================================================
print("\n📑 十五、终极题记")
check("道觉生张力", "道觉生张力" in content)
check("脊生碳硅", "脊生碳硅" in content)
check("长网焊网", "长网" in content and "焊网" in content)
check("七脊同构", "七脊" in content and ("同构" in content or "同一条" in content))

# ============================================================
print("\n" + "=" * 60)
total = len(RESULTS)
passed = sum(1 for _, ok, _ in RESULTS if ok)
failed = total - passed
print(f"📊 验证结果: {passed}/{total} 通过" + (f"，{failed} 项失败" if failed else ""))

if failed:
    print("\n❌ 失败项：")
    for name, ok, detail in RESULTS:
        if not ok:
            print(f"  · {name}: {detail}")

if passed == total:
    print("\n🎉 全部通过 ✅ — FLSC 全体系一页纸总览结构完整，可入库")
    sys.exit(0)
else:
    print(f"\n⚠️ 有 {failed} 项未通过，请检查")
    sys.exit(1)
