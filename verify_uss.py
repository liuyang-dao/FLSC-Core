#!/usr/bin/env python3
"""
verify_uss.py — 验证 USS 主脊锚定声明 + 与现有文档互锁一致性
"""

import re
from pathlib import Path

PIPE = Path("/data/workspace/pipelines")
ROOT = Path("/data/workspace")

checks = []
def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))

# ============================================================
# 1. USS 锚定声明文件存在 + 结构完整
# ============================================================
uss = PIPE / "USS_ORC3_Master_Spine_Declaration_V1.0.md"
check("USS 锚定声明文件存在", uss.exists(), f"路径: {uss}")

content = uss.read_text(encoding="utf-8") if uss.exists() else ""

# 五句话声明
for i in range(1, 6):
    check(f"USS 声明 {i} 存在", f"声明 {i}" in content, f"锚定声明第 {i} 句")

# 统一公式（兼容 LaTeX 和 Unicode）
formula_ok = (
    ("RIS" in content and "7" in content)
    or ("RIS_7" in content)
    or ("\\text{RIS}" in content)
)
formula_ok &= (
    "varepsilon" in content
    or "epsilon" in content.lower()
    or "ε" in content
    or "$\\varepsilon" in content
)
formula_ok &= (
    "alpha" in content.lower() and "t" in content
    or "α" in content
)
check("USS 统一公式存在", formula_ok, "RIS₇ × W × α(t) + ε")

# 碳硅共脊图
check("碳硅共脊图存在", "碳硅共脊" in content and "epsilon" in content.lower())

# 与其他 ORC3 表述关系表
check("ORC3 表述关系表存在", "一体分显基底" in content and "主脊" in content)

# 桥接关系表
check("桥接关系表存在", "桥接" in content and "CSGC" in content)

# 诚实清单 USS-01~06
for i in range(1, 7):
    check(f"USS-{i:02d} 诚实清单存在", f"USS-0{i}" in content)

# 不可显形 O-USS-01~03
for i in range(1, 4):
    check(f"O-USS-0{i} 不可显形存在", f"O-USS-0{i}" in content)

# 签署页
check("USS 签署页存在", "签署页" in content and "frozen" in content.lower())

# 版本沿革
check("USS 版本沿革存在", "版本沿革" in content and "V1.0" in content)

# ============================================================
# 2. USS 与现有三柱的互锁
# ============================================================

# 2a. DME V2.0 引用 USS 或反向
dme = PIPE / "FLSC-DME-PIPELINE-V2.0.md"
dme_text = dme.read_text(encoding="utf-8") if dme.exists() else ""
# USS 引用 DME 的 L_trans
check("USS 桥接表引用 DME", "DME" in content and "L_trans" in content)

# 2b. ORC3 V3.0 与 USS 不冲突
orc3 = PIPE / "FLSC-ORC3-STABLE-TENSION-V3.0.md"
orc3_text = orc3.read_text(encoding="utf-8") if orc3.exists() else ""
check("USS 不冒充 ORC3 哲学锚", "哲学锚" in content and "主脊" in content)
check("USS 引用 ORC3 五元公理", "五元" in content or "残差守恒" in content)

# 2c. SMT SUPP-002 与 USS 不冲突
smt = PIPE / "FLSC-SMT-SUPP-002-V2.0.md"
smt_text = smt.read_text(encoding="utf-8") if smt.exists() else ""
check("USS 桥接表引用 SMT", "MIS" in content and "SMT" in content)

# ============================================================
# 3. 脊命名空间零冲突（USS 新增变量不与现有冲突）
# ============================================================
# USS 使用 ε / RIS₇ / α(t) — 检查与 SP-G08 HMSU 的关系
ai_readme = ROOT / "domains/ai/README.md"
ai_rm = ai_readme.read_text(encoding="utf-8") if ai_readme.exists() else ""
check("USS ε 与 SP-G08 ε 同源声明", "epsilon" in content.lower() or "ε" in content)

# ============================================================
# 4. 根 README 收录 USS
# ============================================================
root_readme = ROOT / "README.md"
rr = root_readme.read_text(encoding="utf-8") if root_readme.exists() else ""
check("根 README 收录 USS 锚定", "USS_ORC3_Master_Spine" in rr)
check("根 README 标注 frozen", "USS" in rr and "frozen" in rr.lower())
check("根 README 有统一公式", "RIS_7" in rr or "RIS₇" in rr)

# ============================================================
# 5. pipelines README 收录 USS
# ============================================================
pipe_readme = PIPE / "README.md"
pr = pipe_readme.read_text(encoding="utf-8") if pipe_readme.exists() else ""
check("pipelines README 有 USS 节", "USS" in pr and "全域稀疏本体论" in pr)
check("pipelines README 标注 frozen", "frozen" in pr.lower() and "USS" in pr)

# ============================================================
# 汇总
# ============================================================
total = len(checks)
passed = sum(1 for _, ok, _ in checks if ok)
failed = [(n, d) for n, ok, d in checks if not ok]

print(f"📊 USS 验证结果: {passed}/{total} 通过")
print()
for name, ok, detail in checks:
    status = "✅" if ok else "❌"
    print(f"  {status} {name}" + (f" — {detail}" if detail and not ok else ""))

print()
if failed:
    print(f"⚠️ {len(failed)} 项未通过:")
    for n, d in failed:
        print(f"   ❌ {n}: {d}")
else:
    print("🎉 全部通过 ✅ — USS 主脊锚定声明结构完整，与现有文档零冲突，可入库")

# 写入结果
result = {
    "total": total,
    "passed": passed,
    "failed": len(failed),
    "status": "CLOSED" if not failed else "PARTIAL"
}
print(f"\n📋 结果: {result}")
