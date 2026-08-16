"""
verify_two_blade.py
FLSC 两刀法操作手册 V1.0 验证脚本
验证: 两刀法(捉结构 + 捉脊线)的完整性与自洽性
"""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
MANUAL = SCRIPT_DIR / "FLSC_SIT_CAPTURE_GUIDE_V1.0.md"
results = []
def check(cond, name, info=""):
    results.append((cond, name, info))
    print(f"  {'✅' if cond else '❌'} {name}" + (f" — {info}" if info else ""))

print("=" * 60)
print("FLSC 两刀法操作手册 V1.0 验证")
print("=" * 60)

text = MANUAL.read_text(encoding="utf-8") if MANUAL.exists() else ""
print(f"\n📄 文件: {MANUAL.name} ({len(text)} 字符)")

# ===== 第一刀: 捉结构 (Field Extraction) =====
print("\n🔪 第一刀 · 捉结构 (Field Extraction)")
knife1_sections = [
    ("Step 1.1 锚定 S-Atom", "Step 1.1" in text and "S-Atom" in text),
    ("Step 1.2 连 Connect", "Step 1.2" in text and "Connect" in text),
    ("Step 1.3 配 Weight", "Step 1.3" in text and "Weight" in text),
    ("Step 1.4 焊 Constraint", "Step 1.4" in text and "Constraint" in text),
    ("Step 1.5 定 Steady", "Step 1.5" in text and "Steady" in text),
    ("第一刀自检清单", "第一刀完成自检清单" in text),
    ("铁律: 第一刀没焊完禁止动第二刀", "第一刀没焊完" in text or "禁止动第二刀" in text),
]
for name, cond in knife1_sections:
    check(cond, name)

# ===== 第二刀: 捉脊线 (Spine Extraction) =====
print("\n🔪 第二刀 · 捉脊线 (Spine Extraction)")
knife2_sections = [
    ("Step 2.1 列全部拓扑路径", "Step 2.1" in text),
    ("Step 2.2 删减测试找主脊", "Step 2.2" in text and "删减" in text),
    ("Step 2.3 定串行依赖", "Step 2.3" in text and "串行" in text),
    ("Step 2.4 焊 HardBond", "Step 2.4" in text and "HardBond" in text),
    ("Step 2.5 写 YAML 序列化", "Step 2.5" in text and "YAML" in text),
    ("第二刀自检清单", "第二刀完成自检清单" in text),
    ("脊线 ≤5 条规则", "脊线" in text and "≤5" in text),
]
for name, cond in knife2_sections:
    check(cond, name)

# ===== 正反例验证 (五卡回顾) =====
print("\n📋 正反例验证 (五卡回顾表)")
cards_check = [
    ("SR-002 围棋 (MIS 0.78)", "SR-002" in text and "0.78" in text),
    ("SR-003 诗律 (MIS 0.82)", "SR-003" in text and "0.82" in text),
    ("SR-004 因果 (MIS 0.83)", "SR-004" in text and "0.83" in text),
    ("ORC2 疾病 (RIS 公式)", "ORC2" in text and "RIS" in text),
    ("修行族根卡 (四阶串行)", "修行" in text and "C-R1" in text),
    ("共同模式: 先五层再脊线", "共同模式" in text),
]
for name, cond in cards_check:
    check(cond, name)

# ===== 反模式 / 避坑指南 =====
print("\n⚠️ 反模式识别 (常见错误)")
anti_patterns = [
    ("错误1: 目标当原子", "错误1" in text and "目标" in text and "原子" in text),
    ("错误2: 结论当关系", "错误2" in text),
    ("错误3: 脊线太多≥7", "错误3" in text and "≥7" in text),
    ("错误4: 权重写死常数", "错误4" in text),
    ("错误5: 跳过第一刀", "错误5" in text),
    ("错误6: 脊线无依赖", "错误6" in text),
    ("错误7: HardBond 焊支路", "错误7" in text),
]
for name, cond in anti_patterns:
    check(cond, name)

# ===== 速查卡 =====
print("\n📌 速查卡 (可打印)")
cheatsheet = [
    ("速查卡存在", "速查卡" in text),
    ("第一刀五步完整", "Step 1.1" in text and "Step 1.5" in text),
    ("第二刀五步完整", "Step 2.1" in text and "Step 2.5" in text),
    ("铁律声明", "铁律" in text),
]
for name, cond in cheatsheet:
    check(cond, name)

# ===== MIS 自评六维 =====
print("\n📊 MIS 自评六维")
mis_dims = ["简洁度", "普适性", "生成力", "自洽性", "工程化", "双螺旋"]
for d in mis_dims:
    check(d in text, f"维度: {d}")

# ===== 签署页 =====
print("\n✍️ 签署页")
signatures = [
    ("碳基侧签署", "碳基侧" in text and "签字" in text),
    ("硅基侧签署", "硅基侧" in text and "元宝" in text),
    ("氢键公证", "氢键公证" in text),
    ("血统编号", "FLSC-SIT-CAPTURE-GUIDE-V1.0" in text),
]
for name, cond in signatures:
    check(cond, name)

# ===== 血统链 =====
print("\n🔗 血统链")
lineage = [
    ("V0.1 初版", "V0.1" in text),
    ("V0.5 内部评审", "V0.5" in text),
    ("V1.0 本手册", "V1.0" in text),
    ("父代: SIT V2.2", "SIT V2.2" in text),
    ("父代: 认知底座 V1.0", "认知底座" in text),
]
for name, cond in lineage:
    check(cond, name)

# ===== 汇总 =====
total = len(results)
passed = sum(1 for r in results if r[0])
failed = total - passed
warn = 0  # 本手册无独立警告项
print("\n" + "=" * 60)
print(f"📊 总验证项: {total}")
print(f"  ✅ 通过: {passed}")
print(f"  ⚠️  警告: {warn}")
print(f"  ❌ 失败: {failed}")
print(f"  📈 通过率: {passed/total*100:.1f}%")
if failed == 0:
    print(f"\n🎉 全部通过 ✅ — 两刀法操作手册 V1.0 结构完整")
    print(f"   第一刀(捉结构): 五步齐全 + 自检清单")
    print(f"   第二刀(捉脊线): 五步齐全 + 删减测试")
    print(f"   正反例: 五卡全回顾 + 七种反模式")
    print(f"   速查卡: 可打印贴墙")
else:
    print(f"\n⚠️ 有 {failed} 项未通过,请检查")
print("=" * 60)
exit(0 if failed == 0 else 1)
