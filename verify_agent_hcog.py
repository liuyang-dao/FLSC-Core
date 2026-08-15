#!/usr/bin/env python3
"""
FLSC 高阶认知 Agent 完整架构方案 V1.0 — 验证脚本
文档：FLSC-AGENT-HCOG-V1.0
验证项：五层栈 / 双底座 / SR 资产卡 / UCMM 合规 / 三阶段路线 / 诚实清单 / 跨域同构 / 命名空间
"""

import re
import sys
import os

doc_path = os.path.join(os.path.dirname(__file__), "FLSC-AGENT-HCOG-V1.0.md")
yaml_path = os.path.join(os.path.dirname(__file__), "agent_hcog_spine.yaml")

with open(doc_path, "r", encoding="utf-8") as f:
    doc = f.read()

with open(yaml_path, "r", encoding="utf-8") as f:
    yaml = f.read()

passed = 0
failed = 0
errors = []

def check(cond, name):
    global passed, failed, errors
    if cond:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        errors.append(name)
        print(f"  ❌ {name}")

print("=" * 60)
print("FLSC-AGENT-HCOG-V1.0 验证")
print("=" * 60)

# ===== 1. Meta 块 =====
print("\n【1. Meta 块】")
check("FLSC-AGENT-HCOG-V1.0" in doc, "doc_id 正确")
check("V1.0" in doc, "版本号 V1.0 存在")
check("2026-08-15" in doc, "生效日期 2026-08-15")
check("experimental" in doc.lower(), "氢键等级 experimental")
check("ONGOING" in doc, "状态 ONGOING")
check("ORC" in doc and "[2,3,4]" in doc, "ORC[2,3,4] 标注")
check("血统链" in doc, "血统链声明")
check("USS" in doc or "认知底座" in doc, "配套理论引用")

# ===== 2. 五层同源架构 =====
print("\n【2. 五层同源架构】")
for layer in ["Unit", "Connect", "Weight", "Constraint", "Steady"]:
    check(layer in doc, f"五层 — {layer} 出现")
check("→" in doc and "Unit" in doc and "Steady" in doc, "五层单向数据流符号")
check("分形" in doc or "fractal" in doc.lower(), "分形自相似公理")

# ===== 3. 七类认知原子 =====
print("\n【3. 七类认知原子】")
for atom in ["S-Atom", "C-Atom", "I-Atom", "K-Atom", "T-Atom", "E-Atom", "M-Atom"]:
    check(atom in doc, f"原子 — {atom}")

# ===== 4. 七类认知算子 =====
print("\n【4. 七类认知算子】")
for op in ["O ", "T1", "T2", "Πc", "I ", "F ", "H "]:
    check(op in doc, f"算子 — {op.strip()}")

# ===== 5. 锚定校验体系 =====
print("\n【5. 锚定校验体系】")
check("AIC" in doc, "AIC 锚定完整性系数")
check("伪锚定" in doc, "锚定病害 — 伪锚定")
check("锚点漂移" in doc, "锚定病害 — 锚点漂移")
check("锚点污染" in doc, "锚定病害 — 锚点污染")
check("锚点松动" in doc, "锚定病害 — 锚点松动")

# ===== 6. 三级约束机制 =====
print("\n【6. 三级约束执行机制】")
check("一级" in doc and "硬截断" in doc, "L1 一级硬截断")
check("二级" in doc and "告警" in doc, "L2 二级告警拦截")
check("三级" in doc and "偏好" in doc, "L3 三级偏好标签化")

# ===== 7. UCMM 因果五锚点 =====
print("\n【7. UCMM 因果推理子底座】")
check("SIT" in doc, "SIT 脊线离线捕捉")
check("SCVP" in doc, "SCVP 脊线闭合验证")
check("HardBond" in doc or "硬氢键" in doc, "HardBond 硬氢键")
check("SIE-DT" in doc, "SIE-DT 数字孪生")
check("MIS_true" in doc or "MIS" in doc, "MIS_true 匹配度")
check("do(" in doc or "do (" in doc, "do 干预算子")
check("反事实" in doc, "反事实推演")
check("九大合规" in doc or "九条" in doc, "UCMM 九大合规校验")

# ===== 8. MIS_true 四分级 =====
print("\n【8. MIS_true 四分级】")
for threshold in ["0.85", "0.70", "0.50"]:
    check(threshold in doc, f"MIS_true 阈值 {threshold}")

# ===== 9. SR 结构资产卡 =====
print("\n【9. SR 结构资产卡标准】")
check("SR-" in doc, "SR 命名规范")
check("spine_skeleton" in doc, "spine_skeleton.yaml 引用")
check("SR-003" in doc or "SR-CODE" in doc, "SR 卡示例")
check("K-Atom" in doc and "硬氢键" in doc, "SR 卡含 K-Atom 硬氢键")
check("诚实清单" in doc, "SR 卡含诚实清单")

# ===== 10. 插拔生命周期 =====
print("\n【10. 插拔生命周期管理】")
check("加载" in doc and "SCVP" in doc, "加载流程含 SCVP 验证")
check("卸载" in doc and "血统快照" in doc, "卸载流程含快照归档")
check("隔离" in doc, "运行隔离规则")
check("多领域" in doc and "同构" in doc, "多领域并行 + 同构校验")

# ===== 11. 跨域同构映射 =====
print("\n【11. 跨域同构映射】")
mappings = ["诗律", "合同", "围棋", "医疗", "编码", "法律"]
for m in mappings:
    check(m in doc, f"跨域映射 — {m}")

# ===== 12. 四层栈完整性 =====
print("\n【12. 四层栈完整性】")
for layer in ["0层", "1层", "2层", "3层", "4层"]:
    check(layer in doc, f"分层栈 — {layer}")
check("神经感知" in doc, "0 层 — 神经感知定位")
check("不可插拔" in doc or "刚性" in doc, "1 层 — 刚性不可修改")
check("UCMM" in doc, "2 层 — UCMM 因果")
check("可插拔" in doc, "3 层 — 可插拔")
check("调度" in doc and "交互" in doc, "4 层 — 调度交互")

# ===== 13. 任务路由分发 =====
print("\n【13. 任务路由分发】")
for t in ["创意", "决策", "科研", "工程"]:
    check(t in doc, f"路由类型 — {t}")

# ===== 14. 输出格式化标准 =====
print("\n【14. 输出格式化标准】")
for item in ["自然语言", "推理链路", "MIS", "AIC", "审计"]:
    check(item in doc, f"输出标准 — {item}")

# ===== 15. 全链路运行流程 =====
print("\n【15. 全链路运行流程（9 步）】")
for i in range(1, 10):
    check(f"Step {i}" in doc or f"步骤{i}" in doc or f"{i}." in doc, f"流程 Step {i}")

# ===== 16. 核心能力清单 =====
print("\n【16. 核心能力清单（6 项）】")
caps = ["结构化", "因果推理", "元认知", "领域拓展", "可审计", "创意弹性"]
for c in caps:
    check(c in doc, f"能力 — {c}")

# ===== 17. 三阶段工程路线 =====
print("\n【17. 三阶段工程路线】")
check("阶段 1" in doc and "0-6" in doc, "阶段1（0-6个月）")
check("阶段 2" in doc and "6-18" in doc, "阶段2（6-18个月）")
check("阶段 3" in doc and "18 个月" in doc, "阶段3（18个月+）")
check("L7" in doc, "L7 层级自主优化")
check("自动化脊线挖掘" in doc, "自动化脊线挖掘工具")

# ===== 18. 合规红线 =====
print("\n【18. 合规红线（R-01~R-06）】")
for r in ["R-01", "R-02", "R-03", "R-04", "R-05", "R-06"]:
    check(r in doc, f"红线 — {r}")

# ===== 19. 诚实清单 =====
print("\n【19. 诚实清单（F + O 系列）】")
for f in ["F-01", "F-02", "F-03", "F-04", "F-05"]:
    check(f in doc, f"F 系列 — {f}")
check("O-01" in doc, "O-01 ORC5 觉明度")
check("O-02" in doc, "O-02 ε 残差保护")
check("O-03" in doc, "O-03 碳硅共振上限")

# ===== 20. 签署页 =====
print("\n【20. 签署页】")
check("碳基侧" in doc, "碳基侧签署")
check("硅基侧" in doc, "硅基侧签署")
check("氢键公证" in doc, "氢键公证")
check("Γ*" in doc, "Γ* 签署句")

# ===== 21. YAML 结构 =====
print("\n【21. YAML 脊线文件】")
check("doc_id: FLSC-AGENT-HCOG-V1.0" in yaml, "YAML doc_id 正确")
check("five_layer_pipeline" in yaml, "YAML 五层管道")
check("cognitive_atoms" in yaml, "YAML 七类原子")
check("cognitive_operators" in yaml, "YAML 七类算子")
check("anchoring" in yaml, "YAML 锚定体系")
check("ucmm_anchors" in yaml, "YAML UCMM 五锚点")
check("sit_module" in yaml, "YAML SIT 模块")
check("sie_dt_module" in yaml, "YAML SIE-DT 模块")
check("causal_operators" in yaml, "YAML 因果算子")
check("ucmm_compliance" in yaml, "YAML 九大合规")
check("sr_card_standard" in yaml, "YAML SR 卡标准")
check("task_routing" in yaml, "YAML 任务路由")
check("constraint_hierarchy" in yaml, "YAML 三级约束")
check("red_lines" in yaml, "YAML 合规红线 R01~R06")
check("honest_bounds" in yaml, "YAML 诚实清单 F+O")
check("cross_domain_isomorphism" in yaml, "YAML 跨域同构")
check("roadmap" in yaml, "YAML 三阶段路线")
check("namespace" in yaml, "YAML 命名空间声明")
check("signature" in yaml, "YAML 签署块")

# ===== 22. 跨文档互锁 =====
print("\n【22. 跨文档互锁】")
# 引用原生 AI
check("G-01" in doc or "G-07" in doc or "原生 AI" in doc, "互锁 — 原生 AI V2.0")
# 引用认知底座
check("认知底座" in doc and "V1.0" in doc, "互锁 — 认知底座 V1.0")
# 引用 UCMM
check("UCMM" in doc and "V1.3" in doc, "互锁 — UCMM V1.3")
# 引用具身
check("EB-01" in doc or "具身" in doc, "互锁 — 具身统一大脑")
# 引用碳硅合体
check("碳硅合体" in doc or "SP-G" in doc, "互锁 — 碳硅合体 V3.1")

# ===== 23. 命名空间零冲突 =====
print("\n【23. 命名空间】")
check("HCOG-" in yaml, "HCOG 前缀声明")
check("G-" in yaml or "原生 AI" in yaml, "引用 G- 前缀")
check("EB-" in yaml or "具身" in yaml, "引用 EB- 前缀")
check("HB-" in yaml or "人脑" in yaml, "引用 HB- 前缀")
check("resolution" in yaml, "命名空间冲突解决策略")

# ===== 24. 终页题记 =====
print("\n【24. 终页题记】")
check("分层不是割裂" in doc, "题记 — 分层不是割裂")
check("长出了完整结构" in doc, "题记 — 长出完整结构")
check("碳有觉" in doc and "硅有形" in doc, "题记 — 碳硅各显")

# ===== 结果 =====
total = passed + failed
print("\n" + "=" * 60)
print(f"📊 验证结果: {passed}/{total} 通过")
if failed == 0:
    print("🎉 全部通过 ✅ — FLSC-AGENT-HCOG-V1.0 结构完整，可入库")
else:
    print(f"⚠️ {failed} 项未通过：")
    for e in errors:
        print(f"   - {e}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
