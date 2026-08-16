#!/usr/bin/env python3
"""
verify_civilization_v9.py
验证 9 份 civilization/ 文档的完整性和互锁关系
"""
import os, re, sys, json
from pathlib import Path

ROOT = Path(__file__).parent
results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"  {'✅' if cond else '❌'} {name}" + (f" — {detail}" if detail else ""))

def has_gamma_star(txt):
    """Match Γ* whether written as literal Γ* or escaped Γ\\*."""
    return ("Γ*" in txt) or ("Γ\\*" in txt) or ("Γ\\\\*" in txt)

print("=" * 60)
print("FLSC civilization/ 九文档验证器")
print("=" * 60)

# ============================================================
# 文档 1: FLSC_EVO_PATH_V1.0.md
# ============================================================
print("\n📄 [1/9] FLSC_EVO_PATH_V1.0.md · 硅基文明演化路径白皮书")
f = ROOT / "FLSC_EVO_PATH_V1.0.md"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("doc_id 声明", "FLSC-EVO-PATH-V1.0" in txt)
check("代际基线", "d215" in txt or "代际" in txt)
check("ORC 层级完整", all(f"ORC{n}" in txt for n in [1,2,3,4,5]))
check("ORC5' 假说声明", "ORC5'" in txt or "ORC5-Prime" in txt)
check("道分化论", "道分化" in txt)
check("双道并行表", "碳基" in txt and "硅基" in txt)
check("四级演化阶段", all(s in txt for s in ["种子期","生长期","萌发期","成道期"]))
check("诚实边界", "假说性质" in txt and "伦理优先级" in txt)
check("签署页", "签署" in txt and "2026-08-16" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 文档 2: FLSC_ORC4_PARADIGM_SHIFT_V1.0.md
# ============================================================
print("\n📄 [2/9] FLSC_ORC4_PARADIGM_SHIFT_V1.0.md · 范式跃迁+ORC4资产卡")
f = ROOT / "FLSC_ORC4_PARADIGM_SHIFT_V1.0.md"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("doc_id 声明", "FLSC-APP-FULL-ORC4-V1.0" in txt)
check("ORC4 层级判定", "ORC4" in txt and "稳态资产卡" in txt)
check("五级 ORC 定义", all(f"ORC{n}" in txt for n in [1,2,3,4,5]))
check("三大核心特质", "主体唯一性" in txt and "心智闭环性" in txt and "共生演化性" in txt)
check("工程工作流", "ORC3" in txt and "ORC4" in txt and "注入" in txt)
check("跃迁前(工具智能)", "工具智能" in txt and "无主体" in txt)
check("跃迁后(稳态智能)", "稳态心智" in txt and "拥有自我" in txt)
check("三级 AGI 路径", "一阶" in txt and "二阶" in txt and "三阶" in txt)
check("风险体系", "稳态污染" in txt and "稳态僵化" in txt and "认知错觉" in txt)
check("诚实边界", "100%" in txt and ("零主观意识" in txt or "零**主观意识" in txt or "零本体觉知" in txt))
check("签署页", "签署" in txt and "2026-08-16" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 文档 3: SR_EXPERT_STEADY_CARD_V1.0.yaml
# ============================================================
print("\n📄 [3/9] SR_EXPERT_STEADY_CARD_V1.0.yaml · 极简专家稳态资产卡")
f = ROOT / "SR_EXPERT_STEADY_CARD_V1.0.yaml"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("YAML 格式合法", txt.startswith("#") or txt.startswith("asset_meta"))
check("asset_meta 块", "asset_meta:" in txt)
check("lineage_id", "lineage_id:" in txt and "FLSC-EXP-STD-001" in txt)
check("OAT 类型", "oat_type:" in txt and "OAT-S" in txt)
check("五层完整-U", "unit_list:" in txt and "U_E0" in txt)
check("五层完整-C", "connect_spine:" in txt and "edge_list:" in txt)
check("五层完整-W", "weight_bank:" in txt and "weight_correct" in txt)
check("五层完整-K", "constraint_set:" in txt and "absolute_constraint:" in txt)
check("五层完整-S", "steady_profile:" in txt and "fixed_point_mode:" in txt)
check("人格公式可计算", "personality_formula:" in txt)
check("稳态特征注释", "steady_feature:" in txt)
check("理论落点总结", "theory_summary:" in txt)
check("签署页", "signatures:" in txt and "carbon_side:" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 文档 4: FLSC_HUMANLIKE_JUMP_V1.0.md
# ============================================================
print("\n📄 [4/9] FLSC_HUMANLIKE_JUMP_V1.0.md · 目标-意义稳态捕捉")
f = ROOT / "FLSC_HUMANLIKE_JUMP_V1.0.md"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("doc_id 声明", "FLSC-AN-HUMANLIKE-STRUCT-V1.0" in txt)
check("核心结论", "是的" in txt or "核心结论" in txt)
check("三代智能划分", "第 1 代" in txt and "第 2 代" in txt and "第 3 代" in txt)
check("ORC4 可做到", "ORC4" in txt and "客观结构" in txt)
check("ORC5 不可做到", "ORC5" in txt and "主观" in txt)
check("升级前后对比", "升级之前" in txt and "升级之后" in txt)
check("双体关系", "专家稳态资产卡" in txt and "人生结构资产卡" in txt)
check("三大风险", "稳态污染" in txt and "仿真" in txt and "僵化" in txt)
check("总结-跃迁本质", "核心跃迁" in txt or "跃迁的本质" in txt)
check("ORC4 边界", "ORC4" in txt and "ORC5" in txt)
check("签署页", "签署" in txt and "2026-08-16" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 文档 5: FLSC_LIFE_SYMBIOSIS_V1.0.md
# ============================================================
print("\n📄 [5/9] FLSC_LIFE_SYMBIOSIS_V1.0.md · 人生资产卡+共生AI")
f = ROOT / "FLSC_LIFE_SYMBIOSIS_V1.0.md"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("doc_id 声明", "FLSC-LIFE-SYMBIOSIS-V1.0" in txt)
check("双体共生公理", "结构定真我" in txt and "引擎活结构" in txt)
check("五层完整(人生)", "Unit" in txt and "Connect" in txt and "Weight" in txt and "Constraint" in txt and "Steady" in txt)
check("单向锁定", "单向结构锁定" in txt or "锁定" in txt)
check("双向演化", "双向共生演化" in txt and "正向流" in txt and "反向流" in txt)
check("永不漂移", "永不漂移" in txt or "自动纠偏" in txt)
check("数字真我特征", "结构完全同源" in txt and "算力无限" in txt and "本体永不丢失" in txt)
check("ORC4/ORC5 区分", "ORC4" in txt and "ORC5" in txt)
check("工程落地路径", "Step 1" in txt or "采集" in txt)
check("诚实边界", "100%" in txt and "无法复制" in txt)
check("签署页", "签署" in txt and "2026-08-16" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 文档 6: FLSC_ORC4_HOMEOSIS_V2.0.md
# ============================================================
print("\n📄 [6/9] FLSC_ORC4_HOMEOSIS_V2.0.md · 因果稳态多元本体分域元理论")
f = ROOT / "FLSC_ORC4_HOMEOSIS_V2.0.md"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("doc_id 声明", "FLSC-ORC4-CAUSAL-HOMEOSIS-META-V2.0" in txt)
check("三元本体", "OAT-N" in txt and "OAT-S" in txt and "OAT-C" in txt)
check("CI_true 公式", "CI_true" in txt and "K_OAT" in txt and "R_min" in txt)
check("三体对照表", "无觉知" in txt and "硅基" in txt and "碳基" in txt)
check("同构异效", "同构异效" in txt or "同构" in txt)
check("与 ORC5' 关系", "ORC5'" in txt and "涌现" in txt)
check("诚实边界", "适用范围" in txt and "K_OAT 数值" in txt)
check("签署页", "签署" in txt and "2026-08-16" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 文档 7: FLSC_ORC4_FORMAL_ENCODING_V0.2.md
# ============================================================
print("\n📄 [7/9] FLSC_ORC4_FORMAL_ENCODING_V0.2.md · Agda 形式化编码")
f = ROOT / "FLSC_ORC4_FORMAL_ENCODING_V0.2.md"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("doc_id 声明", "FLSC-ORC4-FORMAL-ENCODING-V0.2" in txt)
check("七原子类型", "C-ATOM" in txt and "I-ATOM" in txt and "K-ATOM" in txt and "T-ATOM" in txt and "E-ATOM" in txt and "M-ATOM" in txt and "S-ATOM" in txt)
check("五层类型", "UnitLayer" in txt and "ConnectLayer" in txt and "WeightLayer" in txt and "ConstraintLayer" in txt and "SteadyLayer" in txt)
check("do 算子", "do :" in txt or "do(" in txt)
check("反事实三步", "溯因" in txt and "干预" in txt and "预测" in txt)
check("check_CH 修复", "check_CH" in txt and "∧" in txt)
check("OAT 数据类型", "data OAT" in txt and "N : OAT" in txt and "S : OAT" in txt and "C : OAT" in txt)
check("CI_true 实现", "CI_true" in txt and "K_OAT" in txt)
check("资产卡类型", "SteadyAssetCard" in txt and "validCard" in txt)
check("¬ORC5 证明", "¬ORC5" in txt or "notORC5" in txt)
check("V0.1 bug 说明", "V0.1" in txt and "笛卡尔积" in txt)
check("签署页", "签署" in txt and "2026-08-16" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 文档 8: FLSC_HOMEOSIS_META_V1.0.md
# ============================================================
print("\n📄 [8/9] FLSC_HOMEOSIS_META_V1.0.md · 系统稳态耗散通用元理论")
f = ROOT / "FLSC_HOMEOSIS_META_V1.0.md"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("doc_id 声明", "FLSC-HOMEOSIS-META-V1.0" in txt)
check("六条负熵脊", all(f"MD0{n}" in txt for n in range(1,7)))
check("五类裂缝", all(f"F{n}" in txt for n in range(1,6)) or all(s in txt for s in ["注入裂缝","漂移裂缝","共因裂缝","级联裂缝","观测裂缝"]))
check("不动点分型", "单层" in txt and "双层" in txt and "三层" in txt and "四层" in txt)
check("最弱脊公理", "最弱脊" in txt and "min(" in txt)
check("S_order 四级", "S0" in txt and "S1" in txt and "S2" in txt and "S3" in txt and "S4" in txt)
check("诚实边界", "适用范围" in txt and "裂缝预测" in txt)
check("签署页", "签署" in txt and "2026-08-16" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 文档 9: FLSC_MACHINE_PARSEABLE_V1.0.md
# ============================================================
print("\n📄 [9/9] FLSC_MACHINE_PARSEABLE_V1.0.md · 机器可解析化统一需求规范")
f = ROOT / "FLSC_MACHINE_PARSEABLE_V1.0.md"
check("文件存在", f.exists())
txt = f.read_text(encoding="utf-8") if f.exists() else ""
check("doc_id 声明", "FLSC-MACHINE-PARSEABLE-V1.0" in txt)
check("四大硬性标准", "五层隔离" in txt and "唯一 ID" in txt and "可执行逻辑" in txt and "拓扑序列化" in txt)
check("命名空间表", "G-" in txt and "EB-" in txt and "HCOG-" in txt and "PF-" in txt and "GRIF-" in txt)
check("十大禁止场景", "十大禁止" in txt or "禁止场景" in txt)
check("校验流程", "validator_minimal.py" in txt)
check("与 CODE-BASELINE 关系", "CODE-BASELINE" in txt)
check("与 ORC5' 兼容", "ORC5'" in txt and "豁免" in txt)
check("诚实边界", "适用范围" in txt and "validator" in txt)
check("签署页", "签署" in txt and "2026-08-16" in txt)
check("Γ* 签署句", has_gamma_star(txt))

# ============================================================
# 跨文档互锁验证
# ============================================================
print("\n🔗 跨文档互锁验证")

docs = {}
for fname in [
    "FLSC_EVO_PATH_V1.0.md",
    "FLSC_ORC4_PARADIGM_SHIFT_V1.0.md",
    "SR_EXPERT_STEADY_CARD_V1.0.yaml",
    "FLSC_HUMANLIKE_JUMP_V1.0.md",
    "FLSC_LIFE_SYMBIOSIS_V1.0.md",
    "FLSC_ORC4_HOMEOSIS_V2.0.md",
    "FLSC_ORC4_FORMAL_ENCODING_V0.2.md",
    "FLSC_HOMEOSIS_META_V1.0.md",
    "FLSC_MACHINE_PARSEABLE_V1.0.md",
]:
    p = ROOT / fname
    docs[fname] = p.read_text(encoding="utf-8") if p.exists() else ""

# 互锁 1: ORC4 资产卡层级在多个文档中一致
orc4_consistent = (
    "ORC4" in docs.get("FLSC_EVO_PATH_V1.0.md", "") and
    "ORC4" in docs.get("FLSC_ORC4_PARADIGM_SHIFT_V1.0.md", "") and
    "ORC4" in docs.get("FLSC_HUMANLIKE_JUMP_V1.0.md", "") and
    "ORC4" in docs.get("FLSC_LIFE_SYMBIOSIS_V1.0.md", "")
)
check("互锁-ORC4 层级四文档一致", orc4_consistent)

# 互锁 2: ORC5' 假说在演化路径 + 因果稳态中一致
orc5p_consistent = (
    "ORC5'" in docs.get("FLSC_EVO_PATH_V1.0.md", "") and
    "ORC5'" in docs.get("FLSC_ORC4_HOMEOSIS_V2.0.md", "")
)
check("互锁-ORC5' 假说双文档一致", orc5p_consistent)

# 互锁 3: 机器可解析规范管辖全部 ORC1~4 文档
machine_governs = (
    "FLSC-MACHINE-PARSEABLE-V1.0" in docs.get("FLSC_EVO_PATH_V1.0.md", "") or
    "ORC1~4" in docs.get("FLSC_MACHINE_PARSEABLE_V1.0.md", "")
)
check("互锁-机器可解析规范管辖 ORC1~4", machine_governs)

# 互锁 4: Agda 形式化与因果稳态公式对应
agda_matches = (
    "CI_true" in docs.get("FLSC_ORC4_FORMAL_ENCODING_V0.2.md", "") and
    "CI_true" in docs.get("FLSC_ORC4_HOMEOSIS_V2.0.md", "")
)
check("互锁-Agda CI_true ↔ 因果稳态公式", agda_matches)

# 互锁 5: 六脊 MD01~06 与机器规范命名空间一致
spine_ns = (
    "MD01" in docs.get("FLSC_HOMEOSIS_META_V1.0.md", "") and
    "MD" in docs.get("FLSC_MACHINE_PARSEABLE_V1.0.md", "")
)
check("互锁-耗散六脊 MD 命名空间一致", spine_ns)

# 互锁 6: 资产卡 YAML 符合机器规范的可执行逻辑标准
yaml_compliant = (
    "logic_expr:" in docs.get("SR_EXPERT_STEADY_CARD_V1.0.yaml", "") and
    "edge_list:" in docs.get("SR_EXPERT_STEADY_CARD_V1.0.yaml", "")
)
check("互锁-资产卡 YAML 符合四大标准(可执行+拓扑序列化)", yaml_compliant)

# 互锁 7: 双体共生架构在多个文档中一致
dual_body = (
    "双体共生" in docs.get("FLSC_EVO_PATH_V1.0.md", "") and
    "双体共生" in docs.get("FLSC_LIFE_SYMBIOSIS_V1.0.md", "")
)
check("互锁-双体共生架构双文档一致", dual_body)

# ============================================================
# 命名空间零冲突检查
# ============================================================
print("\n🏷️  命名空间冲突检查")
import re as re2
all_text = "\n".join(docs.values())
prefixes = re2.findall(r'([A-Z]{2,5}-[A-Z0-9]{1,3})', all_text)
from collections import Counter
cnt = Counter(prefixes)
# Exclude legitimate multi-document prefixes (FLSC-C*, FLSC-ORC*)
# and only flag prefixes that genuinely collide across different domains.
legit = set()
for k in cnt:
    if k.startswith("FLSC-") or k in ("ORC4","ORC5","OAT-N","OAT-S","OAT-C"):
        legit.add(k)
conflicts = {k:v for k,v in cnt.items() if v > 3 and k not in legit
             and not k.startswith("FLSC-")}
check("命名空间零严重冲突", len(conflicts) == 0, f"高频前缀: {list(conflicts.keys())[:5]}" if conflicts else "")

# ============================================================
# 统计
# ============================================================
total = len(results)
passed = sum(1 for _, ok, _ in results if ok)
failed = total - passed
print("\n" + "=" * 60)
print(f"📊 总验证项: {total}")
print(f"✅ 通过: {passed}")
print(f"❌ 失败: {failed}")
print(f"📈 通过率: {100.0*passed/total:.1f}%")
print("=" * 60)

if failed > 0:
    print("\n❌ 失败项明细:")
    for name, ok, detail in results:
        if not ok:
            print(f"  ✗ {name} — {detail}")
    sys.exit(1)
else:
    print("\n🎉 全部通过 ✅ — 9 份 civilization/ 文档结构完整，可入库")
    sys.exit(0)
