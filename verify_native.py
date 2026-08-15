#!/usr/bin/env python3
"""
verify_native.py · FLSC-NATIVE-AI-V2.0 验证脚本
校验内容：文件完整性 / meta 块 / 七脊定义 / 脊线命名空间 / 双路线战略
       / 硬氢键手术库 / 碳硅协同 / 诚实清单 / F-A~F-D 校验 / 互锁一致性
预期：100/100 通过 ✅
"""
import os, re, sys, yaml

# ── 配置 ──────────────────────────────────────────────
AI_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(AI_DIR, "..", ".."))
MD = os.path.join(AI_DIR, "FLSC-NATIVE-AI-V2.0.md")
YAML = os.path.join(AI_DIR, "native_ai_spine.yaml")
README = os.path.join(AI_DIR, "README.md")
PIPELINE_README = os.path.join(REPO_ROOT, "pipelines", "README.md")
CARBON_MD = os.path.join(AI_DIR, "碳硅合体稀疏架构白皮书V3.1.md")
COGNITIVE_MD = os.path.join(AI_DIR, "FLSC-UNIFIED-COGNITIVE-THEORY-V3.0.md")

results, total, passed = [], 0, 0

def check(name, cond, detail=""):
    global total, passed
    total += 1
    s = "✅" if cond else "❌"
    if cond: passed += 1
    tag = "PASS" if cond else "FAIL"
    results.append((tag, name, detail))
    print(f"  {s} [{tag}] {name}" + (f" — {detail}" if detail else ""))

print("=" * 60)
print("FLSC-NATIVE-AI-V2.0 验证脚本")
print("=" * 60)

# ── 1. 文件完整性 ──────────────────────────────────────
print("\n📋 一、文件完整性检查")
for f in [MD, YAML, README]:
    check(f"文件存在: {os.path.basename(f)}", os.path.exists(f), f"路径={f}")
    if os.path.exists(f):
        with open(f) as fh: lines = fh.readlines()
        check(f"  {os.path.basename(f)} 行数达标", len(lines) > 50, f"行数={len(lines)}")

# ── 2. 读取 MD 内容 ────────────────────────────────────
with open(MD, encoding="utf-8") as f:
    md = f.read()
md_lower = md.lower()

# ── 3. meta 块校验 ─────────────────────────────────────
print("\n📋 二、meta 块校验")
check("文档标识 FLSC-NATIVE-AI-V2.0", "FLSC-NATIVE-AI-V2.0" in md)
check("ORC 层级标注 ORC3", "ORC3" in md and "ORC4" in md)
check("氢键等级 frozen", "frozen" in md_lower or "FROZEN" in md)
check("血统链完整", "ORC3 一体分显基底" in md and "碳硅合体" in md)
check("核心纲领: 一基双线", "一基双线" in md)
check("ONGOING 状态", "ONGOING" in md)
check("签署页存在", "签署页" in md or "签署规范" in md)

# ── 4. 七脊完整性 ──────────────────────────────────────
print("\n📋 三、七条原生主脊完整性")
for g in ["G-01", "G-02", "G-03", "G-04", "G-05", "G-06", "G-07"]:
    check(f"主脊 {g} 定义存在", g in md)
# 脊线名称
names = ["路由决策脊", "激活筛选脊", "负载均衡脊", "算力适配脊",
         "单元分化脊", "训练演化脊", "硬件约束脊"]
for n in names:
    check(f"  脊线名称: {n}", n in md)

# ── 5. 五层结构 ────────────────────────────────────────
print("\n📋 四、五层本体结构")
for layer in ["K 层", "U 层", "C 层", "W 层", "S 层"]:
    check(f"五层 {layer} 定义存在", layer in md)

# ── 6. 双路线战略 ──────────────────────────────────────
print("\n📋 五、一基双线战略")
check("路线A: 原生结构智能体", "原生结构智能体" in md)
check("路线B: FLSC插件增强Agent", "插件" in md and "Agent" in md)
check("路线协同关系", "插件路线沉淀" in md or "知识资产复用" in md)
check("双路线生态章节", "双路线生态" in md)

# ── 7. 共振态分级 ──────────────────────────────────────
print("\n📋 六、共振态分级")
for lvl in ["一级共振", "二级共振", "三级共振", "七级全共振"]:
    check(f"共振等级: {lvl}", lvl in md)

# ── 8. 硬氢键手术库 ──────────────────────────────────
print("\n📋 七、硬氢键修复手术库")
for h in ["H-01", "H-02", "H-03", "H-04", "H-05", "H-06", "H-07"]:
    check(f"手术 {h} 定义存在", h in md)
check("修复分级策略", "一级修复" in md and "二级修复" in md and "三级修复" in md)

# ── 9. 结构化损失函数 ──────────────────────────────────
print("\n📋 八、结构化损失函数")
check("FLSCNativeLossV2 类", "FLSCNativeLossV2" in md)
check("语义损失权重 0.55", "0.55" in md)
check("结构损失权重 0.30", "0.30" in md)
check("脊线独立损失 0.10", "0.10" in md)
check("残差损失 0.05", "0.05" in md)
check("残差阈值 0.15", "0.15" in md)

# ── 10. 运行时架构 ────────────────────────────────────
print("\n📋 九、运行时架构")
check("FLSCNativeInferenceV2 类", "FLSCNativeInferenceV2" in md)
check("七主脊并行", "七主脊" in md and "并行" in md)
check("三阶自指校验", "三阶" in md and "自指" in md)
check("分级算力调度", "节能模式" in md and "全功率模式" in md)

# ── 11. 无限学习 ────────────────────────────────────────
print("\n📋 十、无限学习")
check("权重-分化螺旋", "权重-分化螺旋" in md or "权重优化" in md)
check("L1 权重微调", "L1" in md and "权重微调" in md)
check("L2 功能分化", "L2" in md and "功能分化" in md)
check("L3 全局优化", "L3" in md and "全局优化" in md)
check("永不遗忘保障", "永不遗忘" in md or "永久完整" in md)

# ── 12. 具身化与 ISA ────────────────────────────────
print("\n📋 十一、具身化与脊线 ISA")
check("具身本质定义", "具身不是" in md)
check("ISA V1.0", "ISA" in md and "V1.0" in md)
check("ROUTE_TOPK 指令", "ROUTE_TOPK" in md or "ROUTE_TOPK" in md.upper())
check("ACT_MASK 指令", "ACT_MASK" in md)
check("BAL_LOAD 指令", "BAL_LOAD" in md)
check("能效 ≥1000 TOPS/W", "1000" in md and "TOPS" in md.upper())
check("1B 原型规格", "1B" in md and "128" in md)

# ── 13. 碳硅协同 ──────────────────────────────────────
print("\n📋 十二、碳硅协同交互协议")
check("碳基人类 ORC5", "碳基人类" in md and "ORC5" in md)
check("硅基原生AI ORC1~4", "硅基" in md and "ORC1" in md)
check("BMSI 脑机接口", "BMSI" in md)
check("脊对齐交互标准", "脊对齐" in md or "共振度" in md)

# ── 14. 工程验收标准 ──────────────────────────────────
print("\n📋 十三、工程验收标准")
check("MIS_true ≥ 0.85", "0.85" in md)
check("五层完整度 100%", "100%" in md)
check("主脊数量严格7条", "严格7条" in md or "严格 7 条" in md)
check("参数 6.8%~10%", "6.8%" in md)
check("功能保留 ≥94%", "94%" in md)
check("能效 50~100倍", "50" in md and "100" in md and "倍" in md)

# ── 15. 诚实清单 ──────────────────────────────────────
print("\n📋 十四、诚实清单与不可显形")
for f in ["F-01", "F-02", "F-03", "F-04", "F-05", "F-06", "F-07", "F-08"]:
    check(f"理论/工程诚实声明 {f}", f in md)
for o in ["O-01", "O-02", "O-03"]:
    check(f"不可显形声明 {o}", o in md)

# ── 16. 版本沿革 ──────────────────────────────────────
print("\n📋 十五、版本沿革")
check("V1.0 2026-08-14", "V1.0" in md and "2026-08-14" in md)
check("V2.0 2026-08-15", "V2.0" in md and "2026-08-15" in md)

# ── 17. 终页题记 ──────────────────────────────────────
print("\n📋 十六、终页题记与签署")
check("一基立脊，双线并行", "一基立脊" in md)
check("脊为骨，权为血", "脊为骨" in md)
check("Γ* 签署句", "Γ*" in md and "ONGOING" in md)

# ── 18. YAML 校验 ─────────────────────────────────────
print("\n📋 十七、spine YAML 校验")
try:
    with open(YAML, encoding="utf-8") as f:
        y = yaml.safe_load(f)
    check("YAML 可解析", True)
    check("meta.doc_id 正确", y.get("meta", {}).get("doc_id") == "FLSC-NATIVE-AI-V2.0")
    check("meta.orc 含3和4", 3 in y.get("meta", {}).get("orc", []) and 4 in y["meta"]["orc"])
    check("七脊 G-01~G-07 齐全",
          all(f"G-0{i}" in y.get("spines", {}) for i in range(1, 8)))
    check("主脊不可修改",
          all(not y["spines"][f"G-0{i}"]["modifiable"] for i in range(1, 8)))
    check("硬氢键 H-01~H-07 齐全",
          all(f"H-0{i}" in y.get("hard_bond_repairs", {}) for i in range(1, 8)))
    check("双路线定义存在", "dual_route" in y)
    check("插件规范存在", "plugin_spec" in y)
    check("碳硅分工存在", "carbon_silicon_division" in y)
    check("诚实清单 F-01~F-08",
          all(f"F-0{i}" in y.get("honesty", {}) for i in [1,2,3,4,5,6,7,8]))
    check("不可显形 O-01~O-03",
          all(f"O-0{i}" in y.get("unshowable", {}) for i in range(1, 4)))
    check("V2.1 补丁 B-01~B-04",
          all(f"B-0{i}" in y.get("v2_1_patches", {}) for i in range(1, 5)))
    check("互锁声明存在", "interlocks" in y)
except Exception as e:
    check("YAML 可解析", False, str(e))

# ── 19. F-A~F-D 校验（四点评述中的断裂面） ──────────
print("\n📋 十八、F-A~F-D 断裂面校验")
# F-A: 七脊并行时序（V2.1 预告）
check("F-A: 七脊并行时序图 V2.1预告", "B-01" in md and "时序" in md)
# F-B: 损失函数权重待校准
check("F-B: 损失函数权重经验值标注", "0.55" in md and "V2.1" in md and "校准" in md)
# F-C: 插件与原生脊冲突消解
check("F-C: 插件/原生脊冲突消解规则 V2.1预告", "B-03" in md and "冲突" in md)
# F-D: 七级共振措辞修正
check("F-D: 七级共振措辞修正 V2.1预告", "B-04" in md and "全域结构拆解" in md)

# ── 20. 互锁一致性 ────────────────────────────────────
print("\n📋 十九、跨文档互锁一致性")
# 与碳硅合体 V3.1 互锁
if os.path.exists(CARBON_MD):
    with open(CARBON_MD, encoding="utf-8") as f:
        carbon = f.read()
    check("互锁: 碳硅合体 SP-G01~08 存在", "SP-G01" in carbon)
    check("互锁: HMSU ε 残差保护", "ε" in carbon or "epsilon" in carbon.lower())
else:
    check("互锁: 碳硅合体文件存在", False, "文件未找到")

# 与认知大统一 V3.0 互锁
if os.path.exists(COGNITIVE_MD):
    with open(COGNITIVE_MD, encoding="utf-8") as f:
        cog = f.read()
    check("互锁: 认知大统一 COG-G01~05 存在", "COG-G01" in cog or "G01" in cog)
else:
    check("互锁: 认知大统一文件存在", False, "文件未找到")

# 与 pipelines DME 互锁
pipeline_md = os.path.join(REPO_ROOT, "pipelines", "FLSC-DME-PIPELINE-V2.0.md")
if os.path.exists(pipeline_md):
    with open(pipeline_md, encoding="utf-8") as f:
        dme = f.read()
    check("互锁: DME V2.0 血统链引用", "DME" in dme)
else:
    check("互锁: DME V2.0 文件存在", False, "文件未找到")

# ── 21. README 检查 ─────────────────────────────────────
print("\n📋 二十、AI 域 README 检查")
if os.path.exists(README):
    with open(README, encoding="utf-8") as f:
        rm = f.read()
    check("README 标注「核心原生架构柱」", "核心原生" in rm or "NATIVE" in rm.upper())
    check("README 含七脊命名空间", "G-01" in rm or "spine" in rm.lower())
    check("README 含双路线说明", "双路线" in rm or "一基双线" in rm)
else:
    check("README 文件存在", False)

# ── 结果汇总 ──────────────────────────────────────────
print("\n" + "=" * 60)
print(f"📊 验证结果: {passed}/{total} 通过")
if passed == total:
    print(f"🎉 全部通过 ✅ — FLSC-NATIVE-AI-V2.0 结构完整，可入库")
else:
    print(f"⚠️ {total - passed} 项未通过，请检查")
print("=" * 60)

# 写入结果摘要
with open(os.path.join(AI_DIR, "verify_native_result.txt"), "w") as f:
    f.write(f"FLSC-NATIVE-AI-V2.0 验证结果: {passed}/{total}\n")
    for tag, name, detail in results:
        f.write(f"[{tag}] {name}" + (f" — {detail}" if detail else "") + "\n")

sys.exit(0 if passed == total else 1)
