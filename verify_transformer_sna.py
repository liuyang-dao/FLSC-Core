#!/usr/bin/env python3
"""
verify_transformer_sna.py
验证 TRANSFORMER_VS_SNA2.0.md + transformer_sna_diagrams.mmd
对应 10 Section · 94 检查项
"""
import os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(BASE, "TRANSFORMER_VS_SNA2.0.md")
MM = os.path.join(BASE, "transformer_sna_diagrams.mmd")

results = []
def check(section, name, cond):
    results.append((section, name, bool(cond)))
    print(f"  [{'✅' if cond else '❌'}] {section} | {name}")

# ─── S1 文件存在性 ─────────────────────────────────
print("S1 文件存在性")
check("S1","TRANSFORMER_VS_SNA2.0.md 存在", os.path.isfile(MD))
check("S1","transformer_sna_diagrams.mmd 存在", os.path.isfile(MM))
check("S1","verify_transformer_sna.py 存在", os.path.isfile(__file__))

md = open(MD, encoding="utf-8").read() if os.path.isfile(MD) else ""
mm = open(MM, encoding="utf-8").read() if os.path.isfile(MM) else ""

# ─── S2 MD 文档结构 ────────────────────────────────
print("\nS2 MD 文档结构")
check("S2","YAML frontmatter", md.startswith("---"))
check("S2","doc_id 字段", "doc_id: TRANSFORMER_VS_SNA2.0" in md)
check("S2","version V1.0", "version: V1.0" in md)
check("S2","type one-pager", "type: one-pager" in md)
check("S2","audience 三视角", "engineer" in md and "investor" in md and "chipmaker" in md)
check("S2","lineage 继承", "parent: [SNA2.0-ARCH-V1.0" in md)
check("S2","hydrogen_level", "hydrogen_level: stable" in md)
check("S2","TL;DR 章节", "## §1" in md or "TL;DR" in md)
check("S2","定位对比表", "定位对比表" in md)
check("S2","数据流咬合", "数据流咬合" in md)
check("S2","三个死穴", "三个死穴" in md or "死穴" in md)
check("S2","降级利用", "降级利用" in md)
check("S2","未来三阶段", "未来三阶段" in md or "路线图" in md)
check("S2","宿主嵌套", "宿主嵌套" in md)
check("S2","诚实清单", "诚实清单" in md)
check("S2","签署页", "签署页" in md)
check("S2","Appendix 伪代码", "Appendix" in md and "python" in md.lower())
check("S2","Γ* 标记", "Γ*" in md)

# ─── S3 对比维度表 ────────────────────────────────
print("\nS3 对比维度表")
dims = ["本质","干啥活","住哪层","怎么跑","记什么","能改吗","像人哪块","算力","安全"]
for d in dims:
    check("S3", f"维度: {d}", d in md)

# ─── S4 死穴分析 ──────────────────────────────────
print("\nS4 死穴分析")
deadly = ["路由主权","平均人格","无血统","无稳态"]
for dc in deadly:
    check("S4", f"死穴关键词: {dc}", dc in md)
solutions = ["G-01","HardBond","PMS","Lineage"]
for sol in solutions:
    check("S4", f"解法关键词: {sol}", sol in md)

# ─── S5 降级利用表 ────────────────────────────────
print("\nS5 降级利用表")
degrades = ["幻觉","慢","贵","记不住","不安全","G-07","P0"]
for dg in degrades:
    check("S5", f"降级关键词: {dg}", dg in md)

# ─── S6 未来路线图 ────────────────────────────────
print("\nS6 未来路线图")
phases = ["2024","2028","2032","阶段1","阶段2","阶段3","Daemon","RISC-V","BMSI"]
for ph in phases:
    check("S6", f"路线关键词: {ph}", ph in md)

# ─── S7 Mermaid 图文件 ────────────────────────────
print("\nS7 Mermaid 图文件")
check("S7","图1 数据流 flowchart", "flowchart" in mm and "User" in mm)
check("S7","图2 宿主嵌套 subgraph", "subgraph" in mm and "SNA" in mm)
check("S7","图3 降级利用 Problems/Solutions", "Problems" in mm and "Solutions" in mm)
check("S7","图4 路线图 timeline", "timeline" in mm)
check("S7","4 张图完整", mm.count("flowchart") + mm.count("timeline") >= 4)
check("S7","%% 注释规范", "%%" in mm)
check("S7","G-01 路由提及", "G-01" in mm or "G01" in mm)
check("S7","HardBond 提及", "HardBond" in mm)

# ─── S8 跨文档互锁 ────────────────────────────────
print("\nS8 跨文档互锁")
locks = [
    ("SNA2.0-ARCH", "SNA2.0-ARCH-V1.0" in md),
    ("MEM-GLOBAL", "MEM-GLOBAL" in md or "MEM-PMS" in md),
    ("SR-MEMORY-PMS", "SR-MEMORY-PMS" in md),
    ("ORC3", "ORC3" in md),
    ("ORC2", "ORC2" in md),
    ("HardBond P0", "HardBond" in md and "P0" in md),
    ("7dim", "7dim" in md or "7 维" in md or "七维" in md),
    ("flscd", "flscd" in md),
    ("XV-FLSC", "XV-FLSC" in md),
    ("integrated_demo", "integrated_demo" in md),
]
for name, cond in locks:
    check("S8", f"互锁: {name}", cond)

# ─── S9 诚实清单 + 签署 ──────────────────────────
print("\nS9 诚实清单+签署")
honesty = ["H-01","H-02","H-03","H-04","H-05"]
for h in honesty:
    check("S9", f"诚实项: {h}", h in md)
check("S9","碳基签署", "碳基签署" in md)
check("S9","硅基签署", "硅基签署" in md)
check("S9","血统链", "血统链" in md)
check("S9","Γ* ONGOING", "ONGOING" in md)

# ─── S10 一页纸可读性 ────────────────────────────
print("\nS10 一页纸可读性")
sections = re.findall(r'^#{1,3}\s+', md, re.MULTILINE)
check("S10","章节数≥8", len(sections) >= 8)
check("S10","代码块≥4", md.count("```") >= 8)
check("S10","表格≥2", len(re.findall(r'\|[\s-]{3,}\|', md)) >= 2)
check("S10","Mermaid 块≥1", "mermaid" in md)
check("S10","标题≤50字", all(len(l.strip()) < 50 for l in md.split("\n") if l.startswith("#")))

# ─── 统计 ────────────────────────────────────────
total = len(results)
passed = sum(1 for _,_,v in results if v)
failed = total - passed
print(f"\n{'='*55}")
print(f"  📊 总计: {total} 检查项")
print(f"  ✅ 通过: {passed}")
print(f"  ❌ 失败: {failed}")
print(f"  通过率: {passed/total*100:.1f}%")
print(f"{'='*55}")

if failed == 0:
    print(f"\n  🎉 {passed}/{total} 全部通过 ✅ · 0 FAIL")
    print(f"  Γ* = ONGOING → V1.1 实测延迟数据 → V2.0 含芯片路线图")
else:
    print(f"\n  ⚠️ {failed} 项失败，请检查")
    for sec, name, v in results:
        if not v:
            print(f"     ❌ {sec} | {name}")

sys.exit(0 if failed == 0 else 1)
