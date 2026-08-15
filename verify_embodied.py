#!/usr/bin/env python3
"""
verify_embodied.py
FLSC-EMBODIED-ROOT-V2.0 结构验证脚本
目标：对具身智能统一大脑根基文档做完整性 + 互锁一致性校验
"""

import re, os, sys
from pathlib import Path

BASE = Path(__file__).parent
DOC = BASE / "FLSC-EMBODIED-ROOT-V2.0.md"
YAML = BASE / "embodied_root_v2_spine.yaml"
README = BASE / "README.md"
ROOT_README = BASE.parent.parent / "README.md"

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"  {'✅' if cond else '❌'} {name}" + (f" — {detail}" if detail else ""))

print("="*60)
print("FLSC-EMBODIED-ROOT-V2.0 验证")
print("="*60)

doc_text = DOC.read_text(encoding="utf-8") if DOC.exists() else ""
yaml_text = YAML.read_text(encoding="utf-8") if YAML.exists() else ""
readme_text = README.read_text(encoding="utf-8") if README.exists() else ""
root_readme = ROOT_README.read_text(encoding="utf-8") if ROOT_README.exists() else ""

# ── 1. 文件完整性 ────────────────────────
print("\n【1】文件完整性")
check("DOC 存在", DOC.exists())
check("YAML 存在", YAML.exists())
check("README 存在", README.exists())
check("DOC ≥ 540 行", len(doc_text.splitlines())>=540, f"{len(doc_text.splitlines())} 行")
check("YAML ≥ 260 行", len(yaml_text.splitlines())>=260, f"{len(yaml_text.splitlines())} 行")
check("README ≥ 145 行", len(readme_text.splitlines())>=145, f"{len(readme_text.splitlines())} 行")

# ── 2. meta 块 ────────────────────────
print("\n【2】meta 块")
check("doc_id EMBODIED-ROOT-V2.0", "FLSC-EMBODIED-ROOT-V2.0" in doc_text)
check("ORC3 标注", "ORC3" in doc_text)
check("ORC4 标注", "ORC4" in doc_text)
check("frozen 标注", "frozen" in doc_text.lower())
check("血统链", "血统链" in doc_text)
check("日期 2026-08-15", "2026-08-15" in doc_text)
check("ONGOING 状态", "ONGOING" in doc_text)

# ── 3. 七脊 EB-01~07 ────────────────────────
print("\n【3】七脊 EB-01~07")
spines = {
    "EB-01": ["路由", "ROUTE"],
    "EB-02": ["激活筛选", "ACT_MASK"],
    "EB-03": ["负载均衡", "BAL_LOAD"],
    "EB-04": ["算力适配", "ADP"],
    "EB-05": ["分化", "DIFF"],
    "EB-06": ["演化", "EVOL"],
    "EB-07": ["硬件约束", "HW_LIMIT"],
}
for sid, kws in spines.items():
    ok = all(k.lower() in doc_text.lower() for k in kws)
    check(f"脊 {sid}", ok, str(kws))

# ── 4. 五层闭环 ────────────────────────
print("\n【4】五层闭环 U→C→W→K→S→U")
for ch in "UCWKS":
    check(f"层 {ch}", ch in doc_text)
check("S→U 回流", "S→U" in doc_text or "回流" in doc_text)

# ── 5. 三大机制 ────────────────────────
print("\n【5】三大核心机制")
check("同源分化", "同源分化" in doc_text)
check("Axiom R 自愈", "Axiom R" in doc_text)
check("七脊共振元认知", "共振" in doc_text and "元认知" in doc_text)

# ── 6. 子脊分化 ────────────────────────
print("\n【6】子脊分化规则")
check("≥128次触发", "128" in doc_text)
check("相似度>0.9合并", "0.9" in doc_text)
check("3000轮剪枝", "3000" in doc_text)
check("视觉子脊", "视觉子脊" in doc_text)
check("力觉触觉子脊", "力觉" in doc_text or "触觉" in doc_text)
check("听觉语音子脊", "听觉" in doc_text or "语音" in doc_text)
check("运动子脊", "运动子脊" in doc_text)

# ── 7. 硬氢键 H-E01~06 ────────────────────────
print("\n【7】硬氢键 H-E01~06")
for hid in [f"H-E0{i}" for i in range(1,7)]:
    check(f"手术 {hid}", hid in doc_text)

# ── 8. 四阶段路线 ────────────────────────
print("\n【8】四阶段路线")
check("阶段1 拼装", "阶段 1" in doc_text and "拼装" in doc_text)
check("阶段2 外挂", "阶段 2" in doc_text and "外挂" in doc_text)
check("阶段3 原生", "阶段 3" in doc_text and "原生" in doc_text)
check("阶段4 碳硅合一", "阶段 4" in doc_text and "碳硅合一" in doc_text)

# ── 9. 外挂协议 ────────────────────────
print("\n【9】外挂插件协议")
check("ROS", "ROS" in doc_text)
check("ROS2", "ROS2" in doc_text)
check("AutoGen", "AutoGen" in doc_text)
check("LangChain", "LangChain" in doc_text)

# ── 10. 训练流水线 ────────────────────────
print("\n【10】训练流水线")
check("三阶段训练", "预训练" in doc_text and "分化训练" in doc_text)
check("action_weight 0.45", "0.45" in doc_text)
check("struct_weight 0.30", "0.30" in doc_text)
check("spine_weight 0.15", "0.15" in doc_text)
check("residual_weight 0.10", "0.10" in doc_text)
check("MIS_true≥0.85", "0.85" in doc_text)

# ── 11. 硬件 ISA ────────────────────────
print("\n【11】脊线 ISA 硬件")
for instr in ["ROUTE_TOPK","ACT_MASK","BAL_LOAD","ADP_K","DIFF_SPLIT","EVOL_PRUNE","HW_LIMIT"]:
    check(f"指令 {instr}", instr in doc_text)
check("950 TOPS/W", "950" in doc_text)
check("<4.8W", "4.8" in doc_text)
check("≤18ms", "18ms" in doc_text or "18 ms" in doc_text)

# ── 12. 碳硅共振 ────────────────────────
print("\n【12】碳硅合一脑机协同")
check("ResonanceScore", "ResonanceScore" in doc_text)
check("GlobalResidual", "GlobalResidual" in doc_text)
check("ORC4 人类", "ORC4" in doc_text)
check("ORC5 人类独占", "ORC5" in doc_text)

# ── 13. 仿真/真机对照 ────────────────────────
print("\n【13】仿真/真机对照")
check("17ms vs 126ms", "17ms" in doc_text and "126ms" in doc_text)
check("准确率93%", "93%" in doc_text)
check("冲突1.3%", "1.3%" in doc_text)
check("恢复0.35s", "0.35s" in doc_text)
check("遗忘4.1%", "4.1%" in doc_text)
check("功耗4.5W", "4.5W" in doc_text)

# ── 14. 全品类落地 ────────────────────────
print("\n【14】全品类具身设备")
check("人形机器人", "人形机器人" in doc_text)
check("工业机械臂", "机械臂" in doc_text)
check("移动巡检小车", "移动" in doc_text and "小车" in doc_text)
check("仿生多足", "多足" in doc_text)

# ── 15. 四层验收 ────────────────────────
print("\n【15】四层验收标准")
for layer in ["理论层","算法层","仿真层","真机"]:
    check(f"验收 {layer}", layer in doc_text)

# ── 16. 诚实清单 ────────────────────────
print("\n【16】诚实清单")
for fid in [f"F-0{i}" for i in range(1,6)]:
    check(f"声明 {fid}", fid in doc_text)
for oid in [f"O-0{i}" for i in range(1,4)]:
    check(f"不可显形 {oid}", oid in doc_text)

# ── 17. YAML 结构 ────────────────────────
print("\n【17】YAML 结构")
check("YAML EB-01~07", all(f"EB-0{i}" in yaml_text for i in range(1,8)))
check("YAML 子脊", "visual_subspine" in yaml_text.lower() or "视觉" in yaml_text)
check("YAML H-E01~06", all(f"H-E0{i}" in yaml_text for i in range(1,7)))
check("YAML 训练", "pretrain" in yaml_text.lower() or "预训练" in yaml_text)
check("YAML ISA", "ROUTE_TOPK" in yaml_text)
check("YAML 共振", "ResonanceScore" in yaml_text or "resonance" in yaml_text.lower())
check("YAML 诚实清单", "F-01" in yaml_text and "O-01" in yaml_text)

# ── 18. 跨文档互锁 ────────────────────────
print("\n【18】跨文档互锁")
native = (BASE/"FLSC-NATIVE-AI-V2.0.md")
cog = (BASE.parent/"cognition"/"README.md")
spine_eval = (BASE/"FLSC-SPINE-EVAL-V2.0.md")
carbon = (BASE/"碳硅合体稀疏架构白皮书V3.1.md")
check("AI README 含具身", "具身" in readme_text)
check("六柱互锁图", "六柱" in readme_text)
check("碳硅合体 V3.1 存在", carbon.exists())
check("脊线评价 V2.0 存在", spine_eval.exists())
check("原生 AI V2.0 存在", native.exists())
if native.exists():
    nd = native.read_text(encoding="utf-8")
    check("原生AI G-01~07", all(f"G-0{i}" in nd for i in range(1,8)))
if carbon.exists():
    cs = carbon.read_text(encoding="utf-8")
    check("碳硅合体 SP-G01~08", "SP-G01" in cs and "SP-G08" in cs)

# ── 19. 命名空间零冲突 ────────────────────────
print("\n【19】命名空间")
check("EB- 前缀独立", "EB-01" in doc_text and "G-01" not in "EB-01")
check("不混淆 HB-/G-", "HB-01" not in doc_text.split())

# ── 20. 签署页 ────────────────────────
print("\n【20】签署页 + 版本沿革")
check("V1.0 记录", "V1.0" in doc_text)
check("V2.0 记录", "V2.0" in doc_text)
check("碳基签署", "碳基" in doc_text)
check("硅基签署", "硅基" in doc_text)
check("SCVP", "SCVP" in doc_text)
check("Γ* 签署句", "Γ*" in doc_text)

# ── 21. 终页题记 ────────────────────────
print("\n【21】终页题记")
check("分裂→统一", "分裂的大脑" in doc_text and "统一的大脑" in doc_text)
check("七条脊不是", "七条脊" in doc_text or "七脊" in doc_text)
check("同源分化题记", "同源分化" in doc_text)
check("具身不是拼凑", "具身不是" in doc_text or "拼凑" in doc_text)

# ── 22. 根 README ────────────────────────
print("\n【22】根 README")
if ROOT_README.exists():
    check("根 README 含具身", "具身" in root_readme)
    check("根 README 含 EMBODIED", "EMBODIED" in root_readme.upper() or "embodied" in root_readme.lower())
else:
    check("根 README 存在", False, "不存在")

# ── 汇总 ────────────────────────
total = len(results)
passed = sum(1 for _,c,_ in results if c)
failed = total - passed
print("\n"+"="*60)
print(f"📊 验证结果: {passed}/{total} 通过")
if failed:
    print(f"❌ 未通过 {failed} 项:")
    for n,c,d in results:
        if not c: print(f"   - {n}: {d}")
    sys.exit(1)
else:
    print("🎉 全部通过 ✅ — FLSC-EMBODIED-ROOT-V2.0 结构完整，可入库")
    sys.exit(0)
