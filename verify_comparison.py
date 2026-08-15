"""
verify_comparison.py
=====================
验证 FLSC Prompt vs Spine 对照实验文档 + Demo 的完整性。

运行：python docs/verify_comparison.py
预期：全部通过 ✅
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent  # /data/workspace
DOCS = ROOT / "docs"
DOC = DOCS / "AGENT_COMPARISON_PROMPT_VS_SPINE.md"
DEMO = DOCS / "flsc_minimal_demo.py"

checks = []
def check(name, cond, detail=""):
    status = "✅" if cond else "❌"
    checks.append((name, cond, detail))
    print(f"  {status} {name}" + (f" — {detail}" if detail else ""))
    return cond

print("=" * 65)
print("  FLSC Prompt vs Spine 对照实验 · 完整性验证")
print("=" * 65)

# ===== 文件存在性 =====
print("\n【文件存在性】")
check("对照文档存在", DOC.exists(), f"path={DOC}")
check("Demo脚本存在", DEMO.exists(), f"path={DEMO}")

# ===== 对照文档结构 =====
print("\n【对照文档结构】")
doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""

required_sections = [
    "一、实验设计",
    "二、对照结果",
    "三、五题总结对照表",
    "四、核心结论",
    "五、文档签署",
    "Q1",
    "Q2",
    "Q3",
    "Q4",
    "Q5",
]
for s in required_sections:
    check(f"文档含「{s}」", s in doc_text, f"len={len(doc_text)}")

# ===== 五题对照完整性 =====
print("\n【五题左栏(Prompt) vs 右栏(Spine)】")
questions = {
    "Q1(诗律)": ["平仄", "粘对", "AIC", "SR-003"],
    "Q2(因果)": ["do(", "冰淇淋", "溺水", "伪相关", "因果图"],
    "Q3(医疗)": ["HbA1c", "C肽", "L1", "硬截断", "胰岛素"],
    "Q4(合同)": ["不对称度", "100%", "L2告警", "结构对称"],
    "Q5(具身)": ["EB-01", "H-E0", "夹爪力", "关节"],
}
for q, kws in questions.items():
    for kw in kws:
        check(f"{q}含「{kw}」", kw in doc_text, f"len={len(doc_text)}")

# ===== 核心结论句 =====
print("\n【核心结论句】")
key_quotes = [
    "Prompt Agent 输出了答案",
    "FLSC Agent 输出了判决理由",
    "概率碰对",
    "脊线不许错",
    "会查资料的聪明鹦鹉",
]
for q in key_quotes:
    check(f"含结论「{q}」", q in doc_text)

# ===== Demo 脚本结构 =====
print("\n【Demo 脚本结构】")
demo_text = DEMO.read_text(encoding="utf-8") if DEMO.exists() else ""

demo_classes = [
    "class FLSCBase",
    "def simulate_llm",
    "def do_operator",
    "def load_sr_poetry",
    "def load_sr_medical",
    "def load_sr_law",
    "def format_prompt_output",
    "def format_spine_output",
    "def run_demo",
    "unit_layer",
    "connect_layer",
    "weight_layer",
    "constraint_layer",
    "steady_layer",
    "check_anchoring",
    "m9_scan",
]
for c in demo_classes:
    check(f"Demo含「{c}」", c in demo_text, f"len={len(demo_text)}")

# ===== Demo 可运行性 =====
print("\n【Demo 可运行性】")
try:
    import subprocess
    result = subprocess.run(
        [sys.executable, str(DEMO)],
        capture_output=True, text=True, timeout=30,
    )
    check("Demo退出码=0", result.returncode == 0, f"rc={result.returncode}")
    out = result.stdout
    check("Demo含Q1", "Q1" in out)
    check("Demo含Q2", "Q2" in out)
    check("Demo含Q3", "Q3" in out)
    check("Demo含Q4", "Q4" in out)
    check("Demo含Q5", "Q5" in out)
    check("Demo含总结表", "五题总结" in out)
    check("Demo含Γ*签署", "Γ*" in out)
    if result.returncode != 0:
        print(f"\n  ⚠️ stderr:\n{result.stderr[:500]}")
except Exception as e:
    check(f"Demo可运行", False, f"exception={e}")

# ===== 命名空间零冲突 =====
print("\n【命名空间冲突检查】")
# 检查docs/下的文件不与已有domains/ai/文件冲突
ai_dir = ROOT / "domains" / "ai"
ai_files = set(f.name for f in ai_dir.glob("*.md")) if ai_dir.exists() else set()
doc_files = {DOC.name} if DOC.exists() else set()
conflicts = doc_files & ai_files
check("命名空间零冲突(docs/ vs domains/ai/)", len(conflicts) == 0, f"冲突={conflicts}")

# ===== 汇总 =====
print("\n" + "=" * 65)
total = len(checks)
passed = sum(1 for _, c, _ in checks if c)
failed = total - passed
print(f"  总计: {total} 项")
print(f"  通过: {passed} 项 ✅")
if failed:
    print(f"  失败: {failed} 项 ❌")
    for name, cond, detail in checks:
        if not cond:
            print(f"    ❌ {name} — {detail}")
print(f"\n  📊 验证结果: {passed}/{total} 通过")
if failed == 0:
    print("  🎉 全部通过 ✅ — Prompt vs Spine 对照实验完整可入库")
else:
    print("  ⚠️ 存在问题，需修复")
print("=" * 65)

sys.exit(0 if failed == 0 else 1)
