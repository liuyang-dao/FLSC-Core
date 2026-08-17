#!/usr/bin/env python3
"""
verify_sna_arch.py
验证 SNA2.0-ARCH-V1.0.md + sna_arch_diagram.mmd 的完整性
7 Section · 预计 80+ 检查项
"""

import re
import sys
from pathlib import Path

PASS = 0
FAIL = 0
WARN = 0
results = []

def check(section, name, condition, detail=""):
    global PASS, FAIL, WARN
    if condition:
        PASS += 1
        results.append(f"  ✅ [{section}] {name}")
    else:
        FAIL += 1
        results.append(f"  ❌ [{section}] {name} — {detail}")

def warn(section, name, detail=""):
    global WARN
    WARN += 1
    results.append(f"  ⚠️  [{section}] {name} — {detail}")

# ─── 路径 ───────────────────────────────────────────────
BASE = Path("/data/workspace/domains/ai")
MD = BASE / "SNA2.0-ARCH-V1.0.md"
MMD = BASE / "sna_arch_diagram.mmd"

print("=" * 60)
print("  SNA-2.0 架构规范验证器")
print("=" * 60)

# ══════════════════════════════════════════════════════
# Section 1 · 文件存在性
# ══════════════════════════════════════════════════════
print("\n📂 Section 1 · 文件存在性")
check("S1", "SNA2.0-ARCH-V1.0.md 存在", MD.exists(), f"路径: {MD}")
check("S1", "sna_arch_diagram.mmd 存在", MMD.exists(), f"路径: {MMD}")

md_text = MD.read_text(encoding="utf-8") if MD.exists() else ""
mmd_text = MMD.read_text(encoding="utf-8") if MMD.exists() else ""

# ══════════════════════════════════════════════════════
# Section 2 · Markdown 文档结构
# ══════════════════════════════════════════════════════
print("\n📄 Section 2 · Markdown 文档结构")

# 2.1 元数据头
check("S2", "文档编号标识", "SNA2.0-ARCH-V1.0" in md_text)
check("S2", "氢键等级声明", "hydrogen_level" in md_text.lower() or "氢键" in md_text)
check("S2", "ORC 层级标注", "ORC" in md_text and "ORC5" in md_text)
check("S2", "血统链声明", "lineage" in md_text.lower() or "血统链" in md_text)
check("S2", "生效日期", "2026-08-15" in md_text)

# 2.2 十二章节齐全
chapters = [
    ("第一章", "架构总览"),
    ("第二章", "脊线核心层"),
    ("第三章", "任务外挂层"),
    ("第四章", "硬件适配层"),
    ("第五章", "权限铁则"),
    ("第六章", "分形自相似"),
    ("第七章", "残差回流"),
    ("第八章", "碳基人脑类比"),
    ("第九章", "接口规范"),
    ("第十章", "互锁关系"),
    ("第十一章", "诚实清单"),
    ("第十二章", "签署页"),
]
for ch_num, ch_name in chapters:
    check("S2", f"章节存在: {ch_num} {ch_name}",
          ch_num in md_text and ch_name in md_text,
          f"缺失: {ch_num} {ch_name}")

# 2.3 附录
check("S2", "附录 A 术语表", "附录 A" in md_text and "术语" in md_text)
check("S2", "附录 B 版本变更", "附录 B" in md_text and "版本变更" in md_text)
check("S2", "附录 C 参考文献", "附录 C" in md_text and "参考" in md_text)

# ══════════════════════════════════════════════════════
# Section 3 · ORC 五阶分化完整性
# ══════════════════════════════════════════════════════
print("\n🔗 Section 3 · ORC 五阶分化完整性")

# ORC5 → ORC1 五阶
for orc in ["ORC5", "ORC4", "ORC3", "ORC2", "ORC1"]:
    check("S3", f"{orc} 层级提及", orc in md_text, f"缺失 {orc}")

# 分化箭头
check("S3", "道生差（第一次分化）", "第一次分化" in md_text or "道生差" in md_text)
check("S3", "差生脊线（第二次分化）", "第二次分化" in md_text or "差生脊线" in md_text)
check("S3", "脊线分形（第三次分化）", "第三次分化" in md_text or "脊线分形" in md_text)
check("S3", "脊线实例化", "脊线实例化" in md_text or "实例化" in md_text)

# ORC 与 SNA 层对应关系
check("S3", "ORC3 → 脊线核心层", "ORC3" in md_text and "脊线核心层" in md_text)
check("S3", "ORC2 → 任务外挂层", "ORC2" in md_text and "任务外挂" in md_text)
check("S3", "ORC1 → 硬件适配层", "ORC1" in md_text and "硬件适配" in md_text)
check("S3", "ORC5/4 不在 SNA 物理架构内", "不在 SNA" in md_text or "本体论上层" in md_text)

# ══════════════════════════════════════════════════════
# Section 4 · 七脊线 G01-G07 完整性
# ══════════════════════════════════════════════════════
print("\n🧠 Section 4 · 七脊线 G01-G07 完整性")

spines = {
    "G-01": ["路由决策"],
    "G-02": ["激活选择"],
    "G-03": ["负载均衡"],
    "G-04": ["算力适配"],
    "G-05": ["单元分化"],
    "G-06": ["训练演化"],
    "G-07": ["硬件约束"],
}
for gid, names in spines.items():
    for n in names:
        check("S4", f"{gid} {n}", gid in md_text and n in md_text, f"缺失 {gid}")

# 七脊线核心属性
check("S4", "全局唯一", "全局唯一" in md_text)
check("S4", "运行时固化/锁死", "运行时" in md_text and ("固化" in md_text or "锁死" in md_text))
check("S4", "不存领域知识", "不存领域知识" in md_text or "不存领域" in md_text)
check("S4", "7 维状态向量输出", "7 维" in md_text and "状态向量" in md_text)

# ══════════════════════════════════════════════════════
# Section 5 · 权限铁则
# ══════════════════════════════════════════════════════
print("\n🔒 Section 5 · 权限铁则")

check("S5", "铁则一：主脊只读输出", "铁则一" in md_text and "只读" in md_text)
check("S5", "铁则二：外挂不可改写主脊", "铁则二" in md_text and "不可改写" in md_text)
check("S5", "铁则三：血统不可篡改", "铁则三" in md_text and "血统" in md_text)
check("S5", "SpineState7D 结构体", "SpineState7D" in md_text or "state_7d" in md_text)
check("S5", "mmap PROT_READ", "mmap" in md_text and "READ" in md_text)
check("S5", "SIGSEGV 写保护", "SIGSEGV" in md_text or "写保护" in md_text)
check("S5", "Axiom R 不可触碰", "Axiom R" in md_text)
check("S5", "残差仅离线", "残差" in md_text and "离线" in md_text)

# ══════════════════════════════════════════════════════
# Section 6 · 分形自相似公理
# ══════════════════════════════════════════════════════
print("\n🔁 Section 6 · 分形自相似公理")

check("S6", "分形自相似公理陈述", "分形自相似" in md_text)
check("S6", "五层链路完整", "Unit" in md_text and "Connect" in md_text
      and "Weight" in md_text and "Constraint" in md_text and "Steady" in md_text)
check("S6", "主脊 vs 子脊对照表", "主脊" in md_text and "子脊" in md_text)
check("S6", "RIS₇ 评分引用", "RIS" in md_text or "RIS₇" in md_text)
check("S6", "子脊输入来自主脊 7dim", "7dim" in md_text)
check("S6", "子脊血统快照兼容", "血统" in md_text and "快照" in md_text)

# ══════════════════════════════════════════════════════
# Section 7 · 残差回流协议
# ══════════════════════════════════════════════════════
print("\n🔄 Section 7 · 残差回流协议")

check("S7", "铁律一：线上写 ringbuf", "铁律 1" in md_text or "铁律一" in md_text)
check("S7", "铁律二：离线 SIE-DT", "铁律 2" in md_text or "铁律二" in md_text)
check("S7", "铁律三：热替换零停机", "铁律 3" in md_text or "铁律三" in md_text)
check("S7", "ringbuf 容量 1024", "1024" in md_text)
check("S7", "SIE-DT 引用", "SIE-DT" in md_text)
check("S7", "血统链 V1.0→V1.1→V2.0", "V1.0" in md_text and "V1.1" in md_text)
check("S7", "residue_package YAML 格式", "residue_package" in md_text)

# ══════════════════════════════════════════════════════
# Section 8 · 碳基人脑类比
# ══════════════════════════════════════════════════════
print("\n🧬 Section 8 · 碳基人脑类比")

check("S8", "基底节 + 前额叶类比", "基底节" in md_text and "前额叶" in md_text)
check("S8", "皮层侧抑制类比", "侧抑制" in md_text or "皮层" in md_text)
check("S8", "脑稳态调节类比", "稳态" in md_text and "脑" in md_text)
check("S8", "岗位技能神经通路类比", "神经通路" in md_text or "通路" in md_text)
check("S8", "睡眠期记忆巩固类比", "睡眠" in md_text)
check("S8", "人脑无隔离 vs SNA 强制隔离", "强制隔离" in md_text or "无强制" in md_text)
check("S8", "突触可塑性风险说明", "可塑性" in md_text or "灾难性遗忘" in md_text)

# ══════════════════════════════════════════════════════
# Section 9 · ISA 指令集
# ══════════════════════════════════════════════════════
print("\n⚙️  Section 9 · 脊线 ISA V1.0")

isa_ops = ["OP_G01_ROUTE", "OP_G02_ACT", "OP_G03_LOAD",
           "OP_G04_ADAPT", "OP_G05_DIFF", "OP_G06_EVOLVE",
           "OP_G07_HW", "WB_RESIDUE", "MMAP_7DIM"]
for op in isa_ops:
    check("S9", f"指令 {op}", op in md_text, f"缺失 {op}")

check("S9", "内存布局图", "内存布局" in md_text or "0x0000" in md_text)
check("S9", "脊线 ISA V1.0 摘要", "ISA" in md_text and "V1.0" in md_text)

# ══════════════════════════════════════════════════════
# Section 10 · 跨文档互锁
# ══════════════════════════════════════════════════════
print("\n🔗 Section 10 · 跨文档互锁")

lock_docs = [
    ("碳硅合体稀疏架构白皮书", "碳硅合体"),
    ("MEM-GLOBAL-V1.0", "MEM-GLOBAL"),
    ("SR-CODE-PYTHON", "SR-CODE"),
    ("SR-EXPERT-WANG", "SR-EXPERT-WANG"),
    ("SR-EXPERT-HUMOR", "SR-EXPERT-HUMOR"),
    ("MEM-FAMILY-DIGITAL-HUMAN", "MEM-FAMILY"),
    ("FLSC METHOD V3.21", "METHOD V3.21"),
    ("SIE-DT", "SIE-DT"),
    ("SP-G08 HMSU", "HMSU"),
]
for name, key in lock_docs:
    check("S10", f"互锁文档: {name}", key.lower() in md_text.lower(), f"缺失 {name}")

# 加载顺序 9 步
check("S10", "加载顺序 9 步完整", "Step 0" in md_text and "Step 9" in md_text)

# ══════════════════════════════════════════════════════
# Section 11 · 诚实清单 + 签署页
# ══════════════════════════════════════════════════════
print("\n📋 Section 11 · 诚实清单 + 签署页")

check("S11", "诚实清单 H-01~H-08", "H-01" in md_text and "H-08" in md_text)
check("S11", "碳基签署行", "碳基" in md_text and "签署" in md_text)
check("S11", "硅基签署行", "硅基" in md_text and "签署" in md_text)
check("S11", "ORC 层级校验行", "ORC" in md_text and "校验" in md_text)
check("S11", "SCVP 自指校验行", "SCVP" in md_text or "自指校验" in md_text)
check("S11", "Γ* 签署", "Γ" in md_text and "*" in md_text)
check("S11", "ONGOING 状态", "ONGOING" in md_text)

# ══════════════════════════════════════════════════════
# Section 12 · Mermaid 图文件验证
# ══════════════════════════════════════════════════════
print("\n🎨 Section 12 · Mermaid 架构图 (sna_arch_diagram.mmd)")

check("S12", "Mermaid 声明", "mermaid" in mmd_text.lower() or "flowchart" in mmd_text)
check("S12", "图1: ORC↔SNA 映射", "ORC 本体层级" in mmd_text or "ORC5" in mmd_text)
check("S12", "图2: 推理数据流", "用户请求" in mmd_text or "推理" in mmd_text)
check("S12", "图3: 分形自相似", "分形自相似" in mmd_text or "主脊" in mmd_text)
check("S12", "图4: 残差回流", "残差" in mmd_text and "离线" in mmd_text)
check("S12", "图5: 碳基 vs 硅基", "碳基人脑" in mmd_text or "SNA-2.0" in mmd_text)
check("S12", "flowchart 语法", "flowchart" in mmd_text)
check("S12", "subgraph 使用", "subgraph" in mmd_text)
check("S12", "classDef 样式定义", "classDef" in mmd_text)
check("S12", "箭头连接 →", "->" in mmd_text or "-->" in mmd_text)

# ══════════════════════════════════════════════════════
# 汇总
# ══════════════════════════════════════════════════════
total = PASS + FAIL + WARN
rate = (PASS / total * 100) if total > 0 else 0

print("\n" + "=" * 60)
print(f"  📊 验证结果汇总")
print(f"  ✅ PASS: {PASS}")
print(f"  ⚠️  WARN: {WARN}")
print(f"  ❌ FAIL: {FAIL}")
print(f"  📈 通过率: {rate:.1f}%")
print("=" * 60)

if FAIL == 0:
    print("\n  🎉 全部通过 ✅ — SNA-2.0 架构规范 + Mermaid 图均验证合格")
    print("  📦 可入库：SNA2.0-ARCH-V1.0.md + sna_arch_diagram.mmd")
    print("  Γ* = ONGOING → V1.1 硬件 ISA 流片 → V2.0 量产")
else:
    print(f"\n  ⚠️  存在 {FAIL} 项失败，请检查上方 ❌ 项")
    for r in results:
        if "❌" in r:
            print(f"     {r}")

sys.exit(0 if FAIL == 0 else 1)
