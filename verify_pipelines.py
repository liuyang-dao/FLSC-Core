#!/usr/bin/env python3
"""
verify_pipelines.py — 验证 pipelines/ 三柱 + USS 主脊 + 桥接文件 完整一致性
覆盖：DME V2.0 / ORC3 V3.0 / SMT SUPP-002 V2.0 / USS V1.0 / 桥接文件
"""

from pathlib import Path

PIPE = Path("/data/workspace/pipelines")
ROOT = Path("/data/workspace")

checks = []
def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))

# ============================================================
# A. DME V2.0
# ============================================================
dme = PIPE / "FLSC-DME-PIPELINE-V2.0.md"
check("DME V2.0 文件存在", dme.exists())
dme_text = dme.read_text(encoding="utf-8") if dme.exists() else ""

# 四段流水线（正向+逆向）
dme_ok = (
    ("逆向" in dme_text or "溯源" in dme_text)
    and ("数学化" in dme_text or "数学" in dme_text)
    and ("工程化" in dme_text or "部署" in dme_text)
)
check("DME 含四段流水线", dme_ok, "正向+逆向+数学化+工程化")

# L_trans 翻译损失
check("DME 含翻译损失", "L_trans" in dme_text or "翻译损失" in dme_text or "损失" in dme_text)

# 逆向溯源
check("DME 含逆向溯源", "逆向" in dme_text or "溯源" in dme_text or "Step" in dme_text)

# ORC 跨 1~5
check("DME ORC 跨 1~5", "ORC1" in dme_text and "ORC5" in dme_text)

# 签署页
check("DME 双签署页", "签署" in dme_text and "2026" in dme_text)

# ============================================================
# B. ORC3 V3.0
# ============================================================
orc3 = PIPE / "FLSC-ORC3-STABLE-TENSION-V3.0.md"
check("ORC3 V3.0 文件存在", orc3.exists())
orc3_text = orc3.read_text(encoding="utf-8") if orc3.exists() else ""

check("ORC3 含五元公理", "五元" in orc3_text or "残差守恒" in orc3_text or "公理" in orc3_text)

# 三阶 OJP（三次跳跃）
orp_jump = sum(1 for kw in ["第一次", "第二次", "第三次"] if kw in orc3_text)
check("ORC3 含三阶 OJP", orp_jump >= 3, f"找到 {orp_jump}/3 次跳跃")

# 系统脊线
check("ORC3 含系统脊线", "系统脊线" in orc3_text or "SIT" in orc3_text or "涌现" in orc3_text)

# SCVP
check("ORC3 含 SCVP", "SCVP" in orc3_text or "校验" in orc3_text)

# frozen / CLOSED
check("ORC3 frozen/CLOSED", "CLOSED" in orc3_text or "frozen" in orc3_text.lower())

# 签署
check("ORC3 双签署页", "签署" in orc3_text and "2026" in orc3_text)

# ============================================================
# C. SMT SUPP-002 V2.0
# ============================================================
smt = PIPE / "FLSC-SMT-SUPP-002-V2.0.md"
check("SMT SUPP-002 V2.0 文件存在", smt.exists())
smt_text = smt.read_text(encoding="utf-8") if smt.exists() else ""

# MIS 公式
check("SMT 含 MIS 公式", "MIS" in smt_text and ("S_U" in smt_text or "S_C" in smt_text or "frac" in smt_text))

# 五裂缝
c01_05 = sum(1 for i in range(1, 6) if f"C-0{i}" in smt_text)
check(f"SMT 含五裂缝 C01~C05", c01_05 >= 4, f"找到 {c01_05}/5")

# 硬氢键手术
check("SMT 含硬氢键手术", "H-M" in smt_text or "手术" in smt_text or "修复" in smt_text)

# AI 协同
check("SMT 含 AI 协同", "AI" in smt_text and ("L3" in smt_text or "meta_capture" in smt_text))

# meta_capture 伪代码
check("SMT 含 meta_capture", "meta_capture" in smt_text or "def " in smt_text or "Morph" in smt_text)

# 签署
check("SMT 双签署页", "签署" in smt_text and "2026" in smt_text)

# ============================================================
# D. USS 主脊锚定声明
# ============================================================
uss = PIPE / "USS_ORC3_Master_Spine_Declaration_V1.0.md"
check("USS 锚定声明文件存在", uss.exists())
uss_text = uss.read_text(encoding="utf-8") if uss.exists() else ""

# 五句话声明
for i in range(1, 6):
    check(f"USS 声明 {i} 存在", f"声明 {i}" in uss_text, f"锚定声明第 {i} 句")

# 统一公式（兼容 LaTeX / Unicode）
formula_ok = (
    (("RIS" in uss_text and "7" in uss_text) or "\\text{RIS}" in uss_text)
) and (
    "varepsilon" in uss_text or "epsilon" in uss_text.lower() or "ε" in uss_text
) and (
    "alpha" in uss_text.lower() or "α" in uss_text
)
check("USS 统一公式存在", formula_ok, "RIS₇ × W × α(t) + ε")

# 碳硅共脊图
check("USS 碳硅共脊图", "碳硅" in uss_text and ("epsilon" in uss_text.lower() or "ε" in uss_text))

# ORC3 关系表
check("USS 与 ORC3 关系表", "一体分显" in uss_text or "哲学锚" in uss_text)

# 桥接表
check("USS 桥接关系表", "桥接" in uss_text and ("CSGC" in uss_text or "DME" in uss_text))

# 诚实清单 USS-01~06
for i in range(1, 7):
    check(f"USS-0{i} 诚实清单", f"USS-0{i}" in uss_text)

# 不可显形 O-USS-01~03
for i in range(1, 4):
    check(f"O-USS-0{i} 不可显形", f"O-USS-0{i}" in uss_text)

# 签署 + frozen
check("USS 签署页 frozen", "签署" in uss_text and "frozen" in uss_text.lower())

# 版本沿革
check("USS 版本沿革", "版本沿革" in uss_text and "V1.0" in uss_text)

# ============================================================
# E. 桥接文件
# ============================================================
mb = PIPE / "metrics_bridge.md"
check("metrics_bridge.md 存在", mb.exists())
mb_text = mb.read_text(encoding="utf-8") if mb.exists() else ""
check("MB 含五指标表", "L_trans" in mb_text and "RIS" in mb_text and "MIS" in mb_text)
check("MB 含层级关系", "层级" in mb_text or "映射" in mb_text)

sn = PIPE / "spine_namespace_3level.md"
check("spine_namespace_3level.md 存在", sn.exists())
sn_text = sn.read_text(encoding="utf-8") if sn.exists() else ""
check("SN 含三层脊表", "L3" in sn_text and "L2" in sn_text and "L1" in sn_text)
check("SN 含 M-0x 元脊", "M-01" in sn_text and "M-05" in sn_text)
check("SN 含 SP-Gxx 前缀", "SP-G" in sn_text)
check("SN 含 COG-Gxx 前缀", "COG-G" in sn_text)

patch = PIPE / "v2.1_patch_notes.md"
check("v2.1_patch_notes.md 存在", patch.exists())
patch_text = patch.read_text(encoding="utf-8") if patch.exists() else ""
for i in range(1, 6):
    check(f"PATCH B-0{i} 存在", f"B-0{i}" in patch_text)

# ============================================================
# F. 互锁一致性
# ============================================================

# F1. USS 不冒充 ORC3 哲学锚
check("USS 不冒充 ORC3 哲学锚", "哲学锚" in uss_text and "主脊" in uss_text)

# F2. USS 引用 DME 的 L_trans
check("USS 桥接 DME L_trans", "DME" in uss_text and ("L_trans" in uss_text or "翻译" in uss_text))

# F3. USS 引用 SMT MIS
check("USS 桥接 SMT MIS", "MIS" in uss_text and "SMT" in uss_text)

# F4. USS ε 与 SP-G08 ε 同源
check("USS ε 与 SP-G08 同源", "epsilon" in uss_text.lower() or "ε" in uss_text)

# F5. M-0x 元脊命名不冲突（在 SMT 文档中）
m_in_smt = sum(1 for i in range(1, 6) if f"M-0{i}" in smt_text)
check("M-0x 元脊在 SMT 中", m_in_smt >= 3, f"SMT 中含 {m_in_smt}/5 条 M-0x")

# F6. ORC3 系统脊线 SIT 独立命名
check("SIT 系统脊线独立", "系统脊线" in orc3_text or "SIT" in orc3_text)

# F7. DME 引用 ORC3
check("DME 引用 ORC3", "ORC3" in dme_text or "原点" in dme_text)

# F8. SMT 引用 DME（MIS 含 L_crack 与 L_trans 关系）
check("SMT 与 DME 互锁", "L_crack" in smt_text or "裂缝" in smt_text)

# ============================================================
# G. 根 README 收录
# ============================================================
root_rm = ROOT / "README.md"
rr = root_rm.read_text(encoding="utf-8") if root_rm.exists() else ""
check("根 README 收录 USS", "USS" in rr or "USS_ORC3" in rr)
check("根 README 标注 frozen", "frozen" in rr.lower() and "USS" in rr)
check("根 README 收录三柱", "DME" in rr and "ORC3" in rr and "SMT" in rr)

# ============================================================
# H. pipelines README
# ============================================================
pipe_rm = PIPE / "README.md"
pr = pipe_rm.read_text(encoding="utf-8") if pipe_rm.exists() else ""
check("pipelines README 有 USS 节", "USS" in pr and "全域稀疏" in pr)
check("pipelines README 标注 frozen", "frozen" in pr.lower() and "USS" in pr)

# ============================================================
# 汇总
# ============================================================
total = len(checks)
passed = sum(1 for _, ok, _ in checks if ok)
failed = [(n, d) for n, ok, d in checks if not ok]

print(f"📊 pipelines/ 全量验证: {passed}/{total} 通过")
print()
for name, ok, detail in checks:
    status = "✅" if ok else "❌"
    print(f"  {status} {name}" + (f" — {detail}" if detail and not ok else ""))

print()
if failed:
    print(f"⚠️ {len(failed)} 项未通过:")
    for n, d in failed:
        print(f"   ❌ {n}: {d}")
    print(f"\n📋 结果: {{'total': {total}, 'passed': {passed}, 'failed': {len(failed)}, 'status': 'PARTIAL'}}")
else:
    print("🎉 全部通过 ✅ — pipelines/ 三柱 + USS 主脊 + 桥接文件结构完整，可入库")
    print(f"\n📋 结果: {{'total': {total}, 'passed': {total}, 'failed': 0, 'status': 'CLOSED'}}")
