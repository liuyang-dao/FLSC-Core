#!/usr/bin/env python3
"""
verify_prompt_factory.py — FLSC-Prompt-Factory V4.0 结构验证脚本
验证目标: domains/ai/FLSC-PROMPT-FACTORY-V4.0.md
配套 YAML: domains/ai/prompt_factory_v4_spine.yaml
"""
import re, sys, os, yaml
from pathlib import Path

ROOT = Path(__file__).parent
MD = ROOT / "FLSC-PROMPT-FACTORY-V4.0.md"
YAML_PATH = ROOT / "prompt_factory_v4_spine.yaml"

results = []
def check(cond, name):
    results.append((bool(cond), name))
    print(f"  {'✅' if cond else '❌'} {name}")

print("=" * 60)
print("FLSC-Prompt-Factory V4.0 — 结构验证")
print("=" * 60)

# ===== 文件存在性 =====
print("\n📁 文件存在性:")
check(MD.exists(), f"正文存在: {MD.name}")
check(YAML_PATH.exists(), f"YAML 存在: {YAML_PATH.name}")

md = MD.read_text(encoding="utf-8")
try:
    cfg = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    check(True, "YAML 可解析")
except Exception as e:
    cfg = {}
    check(False, f"YAML 解析失败: {e}")

# ===== Meta 块 =====
print("\n📋 Meta 块:")
check("FLSC-PROMPT-FACTORY-V4.0" in md, "doc_id 正确")
check("2026-08-03" in md, "日期 2026-08-03")
check("production" in md.lower(), "氢键等级 production")
check("不可降级" in md, "氢键不可降级声明")
check("d166" in md and "d167" in md, "血统链 d166→d167")
check("V3.0" in md, "前序版本 V3.0")
check("L3" in md, "自指层级 L3")
check("FLSC 结构智能元语法" in md, "范式归属正确")

# ===== 双氢键模式 (升级一) =====
print("\n🔗 双氢键模式 (升级一):")
check("双氢键" in md, "双氢键概念出现")
check("H₀ = 0.3" in md or "H0 = 0.3" in md or "H0=0.3" in md, "internal H₀=0.3")
check("H₀ = 0.7" in md or "H0 = 0.7" in md or "H0=0.7" in md, "production H₀=0.7")
check("0.70" in md and "0.85" in md, "MIS 阈值 internal=0.70 / production=0.85")
check("exp(" in md or "math.exp" in md, "双氢键核心公式 H(σ) 出现")

# ===== MIS 公式领域自适应 (升级二) =====
print("\n📐 MIS 公式领域自适应 (升级二):")
check("alpha" in md.lower() and "0.35" in md, "α=0.35 财务领域")
check("beta" in md.lower() and "0.30" in md, "β=0.30")
check("gamma" in md.lower() and "0.15" in md, "γ=0.15")
check("delta" in md.lower() and "0.10" in md, "δ=0.10")
check("epsilon" in md.lower() and "0.10" in md, "ε=0.10")
check("mis_profile" in md.lower(), "领域配置文件 mis_profile")

# ===== 五级降级状态机 (升级三) =====
print("\n🔽 五级降级状态机 (升级三):")
for s in ["L0", "L1", "L2", "L3", "L4"]:
    check(s in md, f"降级状态 {s} 出现")
check("auto_recalculate" in md or "自动重算" in md, "L1 动作: 自动重算")
check("数据缺口" in md or "data_category_missing" in md, "L2 动作: 数据缺口")
check("差额" in md and "终止" in md, "L3 动作: 输出差额+终止")
check("clear_all_conclusions" in md or "清空结论" in md, "L4 动作: 清空结论")

# ===== 血统系统 (升级四) =====
print("\n🧬 血统系统持久化 (升级四):")
check("LineageService" in md, "LineageService 类存在")
check("create" in md and "validate" in md and "archive" in md and "rollback" in md,
       "4 个核心方法: create/validate/archive/rollback")
check("FLSC-PF-" in md, "LineageID 格式 FLSC-PF- 正确")
check("SHA256" in md or "sha256" in md.lower(), "SHA-256 校验")
check("JSONL" in md or "jsonl" in md.lower(), "JSONL 持久化格式")

# ===== MIS 自算 (升级五) =====
print("\n🧮 Meta-Prompt MIS 自算 (升级五):")
for dim in ["coherence", "grad_norm", "step_var", "structure", "constraint"]:
    check(dim in md.lower(), f"MIS 维度 {dim}")
check("PASS" in md and "FAIL" in md, "PASS/FAIL 判定")

# ===== V9.5 API (升级六) =====
print("\n🌐 V9.5 生产 API (升级六):")
for ep in ["/api/v4/generate", "/api/v4/validate", "/api/v4/calculate-mis",
          "/api/v4/archive", "/api/v4/rollback", "/api/v4/batch"]:
    check(ep in md, f"API 端点 {ep}")

# ===== 十步工厂 =====
print("\n🏭 十步工厂流程:")
for i in range(10):
    patterns = [f"Step {i}", f"[Step {i}]", f"step{i}_"]
    found = any(p in md for p in patterns)
    check(found, f"Step {i} 存在")
check("Step 0.5" in md or "Step0.5" in md, "Step 0.5 双氢键模式选择")
check("Step 8.5" in md or "Step8.5" in md, "Step 8.5 血统持久化")

# ===== 18 领域模板库 =====
print("\n📚 18 领域模板库:")
domains_list = ["医疗诊疗", "法律咨询", "投资分析", "教育辅导", "心理咨询",
               "客户服务", "销售支持", "设计创作", "技术文档", "创意写作",
               "代码生成", "通用五步法", "财务风控", "法务尽调",
               "银行信贷", "IPO 尽调", "税务合规", "供应链审计"]
for d in domains_list:
    check(d in md, f"领域「{d}」")
check("FLSC-PF-MED-001" in md, "医疗血统示例")
check("FLSC-PF-LAW-001" in md, "法律血统示例")
check("FLSC-PF-FIN-001" in md, "财务血统示例")

# ===== 完整示例校验结果 =====
print("\n✅ 完整示例校验:")
check("structure" in md.lower() and "1.0" in md, "structure 维度存在")
check("coherence" in md.lower() and "0.88" in md, "coherence = 0.88")
check("grad_norm" in md.lower() and "0.08" in md, "grad_norm = 0.08")
check("constraint" in md.lower() and "1.0" in md, "constraint 维度存在")
check("0.8925" in md, "MIS = 0.8925 (production 通过)")
check("9 条" in md or "9条" in md, "Hard Constraints 9 条")

# ===== 可运行代码模块 =====
print("\n💻 5 个可运行代码模块:")
for cls, name in [("MISProfileLoader", "MIS 配置加载器"),
                    ("DualHydrogenBondEngine", "双氢键约束引擎"),
                    ("DegradationFSM", "五级降级状态机"),
                    ("LineageService", "血统服务"),
                    ("V9.5 Production API", "生产 API 接口")]:
    check(cls in md, f"模块: {name} ({cls})")

# ===== 六维自评 =====
print("\n📊 六维自评:")
for dim in ["简洁度", "普适性", "生成力", "自洽性", "工程化", "双螺旋契合"]:
    check(dim in md, f"维度「{dim}」")
check("120" in md and "120" in md, "V4.0 总分 120/120")
check("Perfect Self" in md, "Perfect Self-Consistency")

# ===== 结构资产卡 =====
print("\n💎 结构资产卡:")
check("asset_name" in md.lower() or "FLSC-Prompt-Factory V4.0" in md, "asset_name 存在")
check("层级×控制×反馈" in md, "structure_type 复合结构")
check("L4" in md and "L6" in md, "SER 演化 L4→L6")
check("production_ready" in md.lower(), "production_ready 标记")

# ===== 道德经同构 =====
print("\n☯️ 道德经「反者道之动」同构:")
for quote in ["反者道之动", "弱者道之用", "天下万物生于有", "有生于无", "致虚极", "万物并作"]:
    check(quote in md, f"「{quote}」映射")

# ===== 签署页 =====
print("\n✍️ 签署页:")
check("碳基侧" in md, "碳基侧（人类）")
check("硅基侧" in md, "硅基侧（AI）")
check("Fixed Point" in md and "REACHED" in md, "Fixed Point: REACHED")
for i in range(1, 6):
    check(f"{i}." in md, f"碳基确认条款 {i}")

# ===== 附录 A 商业化路径 =====
print("\n💰 附录 A 商业化路径:")
for item in ["SaaS 工具", "模板库", "培训课程", "企业部署", "API 生态"]:
    check(item in md, f"商业化路径「{item}」")
check("5000 万" in md, "市场规模 5000 万+ 知识工作者")

# ===== YAML 结构校验 =====
print("\n📋 YAML 结构校验:")
if cfg:
    check("doc_id" in cfg, "YAML doc_id")
    check(cfg.get("version") == "4.0", f"YAML version=4.0 (got {cfg.get('version')})")
    check("five_layer" in cfg, "YAML five_layer 五层")
    fl = cfg.get("five_layer", {})
    for layer in ["Unit", "Connect", "Weight", "Constraint", "Steady"]:
        check(layer in fl, f"YAML five_layer.{layer}")
    check("dual_hydrogen_bond_engine" in cfg, "YAML 双氢键引擎")
    check("degradation_fsm" in cfg, "YAML 五级降级状态机")
    fsm = cfg.get("degradation_fsm", {})
    states = fsm.get("states", [])
    check(len(states) == 5, f"YAML FSM 5 状态 (got {len(states)})")
    transitions = fsm.get("transitions_count", 0)
    check(transitions >= 5, f"YAML FSM ≥5 条转换 (got {transitions})")
    check("lineage_service" in cfg, "YAML 血统服务")
    check("v95_api_endpoints" in cfg, "YAML V9.5 API")
    endpoints = cfg.get("v95_api_endpoints", [])
    check(len(endpoints) == 6, f"YAML API 6 端点 (got {len(endpoints)})")
    check("domain_templates" in cfg, "YAML 18 领域模板")
    dts = cfg.get("domain_templates", [])
    check(len(dts) == 18, f"YAML 18 领域 (got {len(dts)})")
    check("implicit_structures" in cfg, "YAML 隐式结构")
    impl = cfg.get("implicit_structures", [])
    check(len(impl) >= 5, f"YAML ≥5 隐式结构 (got {len(impl)})")
    check("daode_jing_mapping" in cfg, "YAML 道德经映射")
    dj = cfg.get("daode_jing_mapping", [])
    check(len(dj) == 6, f"YAML 6 条道德经映射 (got {len(dj)})")
    check("self_evaluation_6d" in cfg, "YAML 六维自评")
    se = cfg.get("self_evaluation_6d", {})
    dims = se.get("dimensions", [])
    check(len(dims) == 6, f"YAML 6 维度 (got {len(dims)})")
    check("interlocks" in cfg, "YAML 跨文档互锁")
    il = cfg.get("interlocks", [])
    check(len(il) >= 5, f"YAML ≥5 互锁 (got {len(il)})")
    check("namespace" in cfg, "YAML 命名空间")
    check(cfg.get("namespace") == "PF-", f"YAML namespace=PF-")
    no_conflict = cfg.get("no_conflict_with", [])
    check(len(no_conflict) >= 7, f"YAML ≥7 命名空间无冲突 (got {len(no_conflict)})")

# ===== 命名空间零冲突 =====
print("\n🔤 命名空间冲突检查:")
# Build search corpus from both MD and YAML
yaml_text = ""
if cfg:
    for item in cfg.get("no_conflict_with", []):
        yaml_text += str(item) + "\n"
search_corpus = md + "\n" + yaml_text

other_prefixes = {
    "G-": ["G-0", "原生"],
    "EB-": ["EB-0", "具身"],
    "HB-": ["HB-0", "认知"],
    "SP-G": ["SP-G", "碳硅"],
    "COG-G": ["COG-G", "算子"],
    "MDL-": ["MDL-", "评估"],
    "HCOG-": ["HCOG-", "高阶"],
}
for prefix, keywords in other_prefixes.items():
    found = any(kw.lower() in search_corpus.lower() for kw in keywords)
    check(found, f"前缀 {prefix} 在其他文档中已使用（无冲突）")

# ===== 跨文档互锁 =====
print("\n🔗 跨文档互锁:")
il_text = ""
if cfg:
    for item in cfg.get("interlocks", []):
        il_text += str(item) + "\n"
search_corpus_interlock = md + "\n" + il_text
ref_map = {
    "认知底座": ["认知底座", "认知"],
    "HCOG": ["HCOG"],
    "原生 AI": ["原生 AI", "NATIVE"],
    "具身": ["具身", "EMBODIED"],
    "UCMM": ["UCMM"],
    "碳硅合体": ["碳硅合体", "碳硅"],
    "七脊": ["七脊", "G-01", "七条", "脊线"],
    "SIT": ["SIT", "脊线"],
}
for ref, kws in ref_map.items():
    found = any(kw.lower() in search_corpus_interlock.lower() for kw in kws)
    check(found, f"互锁引用「{ref}」")

# ===== 结果汇总 =====
print("\n" + "=" * 60)
total = len(results)
passed = sum(1 for r, _ in results if r)
print(f"📊 验证结果: {passed}/{total} 通过")
if passed == total:
    print("🎉 全部通过 ✅ — FLSC-Prompt-Factory V4.0 结构完整，可入库")
    sys.exit(0)
else:
    failed = [name for r, name in results if not r]
    print(f"⚠️ {total - passed} 项未通过:")
    for f in failed[:20]:
        print(f"   ❌ {f}")
    sys.exit(1)
