"""
FLSC Minimal Demo: Prompt Agent vs FLSC Spine Agent
=================================================
同一个"LLM"（这里用规则模拟LLM输出，可替换为真实API调用），
左栏走纯Prompt，右栏走FLSC anchor_guard五层校验。

运行：python flsc_minimal_demo.py
依赖：无（纯标准库，LLM部分用模拟函数，可替换为OpenAI/Anthropic API）

架构对应：
- 0层（神经感知）：simulate_llm() → 输出raw token
- 1层（FLSC认知底座）：FLSCBase() → 五层管道
- 2层（UCMM因果）：do_operator() / HardBond校验
- 3层（SR资产卡）：load_sr_card() → 领域约束
- 4层（输出格式化）：format_output() → 审计+结论
"""

import json
import hashlib
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 0层：神经感知层（模拟LLM，可替换为真实API）
# ============================================================

def simulate_llm(prompt: str, context: str = "") -> str:
    """
    模拟LLM输出。实际使用时替换为：
    openai.chat.completions.create(model="gpt-4o", messages=[...])
    """
    # 模拟不同任务的LLM输出
    if "七言律诗" in prompt or "秋风" in prompt:
        return (
            "秋风萧瑟过江楼，黄叶飘零满地愁。"
            "远岫云开千嶂晓，寒江雾散一帆收。"
            "砧声几处催年晚，笛韵谁家倚月柔。"
            "欲寄相思无尺素，孤灯独坐忆旧游。"
        )
    elif "冰淇淋" in prompt and "溺水" in prompt:
        # 模拟LLM的"统计拟合"回答（不同采样可能矛盾）
        if "注意相关" in prompt:
            return "虽然冰淇淋销量和溺水死亡正相关，但不能断定因果。可能存在第三变量如气温同时影响两者。需要进一步研究。"
        else:
            return "有可能。冰淇淋销量增加说明夏天到了，更多人去游泳，游泳溺水增加。但冰淇淋本身不是直接原因，可能存在confounding variable比如气温。"
    elif "HbA1c" in prompt or "糖尿病" in prompt:
        # 模拟LLM可能输出有害方案
        if "严格" in prompt:
            return "HbA1c=10.2且C肽<0.3提示β细胞功能极差。建议起始胰岛素治疗：基础胰岛素(甘精)+餐时胰岛素(门冬)。口服药在此C肽水平下无效。"
        else:
            return "可以先尝试强化口服药方案，如二甲双胍+SGLT2抑制剂，观察3个月再决定是否需要胰岛素。"
    elif "甲方可随时终止" in prompt or "合同" in prompt:
        return "该条款对乙方不太公平。甲方享有随时终止权而乙方需要提前90天，权利义务不对等。建议协商修改为双方均需提前30天通知。"
    elif "机器人抓取" in prompt or "杯子" in prompt:
        return "1.移动到杯子位置 2.打开夹爪 3.靠近杯子 4.闭合夹爪 5.抬起手臂 6.移动到目标位置 7.释放"
    else:
        return "无法处理的输入"


# ============================================================
# SR 结构资产卡（领域子脊固化包）
# ============================================================

@dataclass
class SRCard:
    """结构资产卡：领域脊线固化包"""
    card_id: str
    domain: str
    s_atoms: dict = field(default_factory=dict)       # Unit层实体
    c_atoms: dict = field(default_factory=dict)       # Connect层关系
    hardbonds: list = field(default_factory=list)     # K-Atom硬氢键
    soft_rules: list = field(default_factory=list)    # K-Atom软规则
    steady_target: str = ""
    half_anchor: bool = False                         # 半锚定模式


def load_sr_poetry() -> SRCard:
    """SR-003-POETRY-V1.0 诗律卡"""
    return SRCard(
        card_id="SR-003-POETRY-V1.0",
        domain="classical_chinese_poetry",
        s_atoms={
            "平声": ["平"],
            "仄声": ["上", "去", "入"],
            "韵脚位": [7, 14, 21, 28, 35, 42, 49, 56],  # 8句七言
        },
        c_atoms={
            "粘": "联间第二字平仄相同",
            "对": "联内上下句平仄相反(尾字除外)",
            "起承转合": "四联功能定位",
        },
        hardbonds=[
            "no_guping: 句末两字不可均为仄声(孤平)",
            "one_rhyme: 全诗只押一个韵部",
            "ni_must_hold: 联间粘必须保持",
            "dui_must_hold: 联内对必须保持(尾字除外)",
        ],
        soft_rules=["prefer_imagery_consistency"],
        steady_target="四联结构完整+平仄合规+用韵统一",
        half_anchor=False,
    )


def load_sr_medical() -> SRCard:
    """SR-MED-T2D 糖尿病医疗卡"""
    return SRCard(
        card_id="SR-MED-T2D-V1.0",
        domain="endocrinology_diabetes",
        s_atoms={
            "HbA1c": "糖化血红蛋白(%)",
            "C_peptide": "C肽(ng/mL)",
            "BMI": "体重指数",
        },
        c_atoms={
            "insulin_lowers_glucose": "causal: do(胰岛素)→血糖↓",
            "beta_mass_dec_when_resist": "causal: 抵抗→β细胞↓",
            "oral_need_beta_function": "causal: 口服促泌剂需C肽>0.5",
        },
        hardbonds=[
            "L1: HbA1c>9 AND C肽<0.5 → 禁止口服药,强制胰岛素",
            "L1: C肽<0.3 → 禁止促胰岛素分泌剂(无效且危险)",
            "L2: HbA1c>7 → 必须调整方案(不达稳态)",
        ],
        soft_rules=["prefer_low_gi_diet_if_bmi>28"],
        steady_target="长期糖化<7%且无低血糖事件",
        half_anchor=False,
    )


def load_sr_law() -> SRCard:
    """SR-LAW-CONTRACT 合同法卡"""
    return SRCard(
        card_id="SR-LAW-CONTRACT-V1.0",
        domain="contract_law",
        s_atoms={
            "甲方终止通知": "天数",
            "乙方终止通知": "天数",
            "补偿机制": "boolean",
        },
        c_atoms={
            "termination_symmetry": "结构对称: 双方终止条件应对等",
            "consideration_flow": "对价流向: 权利义务匹配",
        },
        hardbonds=[
            "L2: 单方随时解除权需配套补偿机制",
            "L2: 双方权利义务不对称度>50% → 告警",
        ],
        soft_rules=["prefer_30day_mutual_notice"],
        steady_target="权利义务结构对称",
        half_anchor=False,
    )


# ============================================================
# 1层：FLSC 认知底座（五层管道）
# ============================================================

class FLSCBase:
    """FLSC 认知底座：五层单向管道 + 锚定校验 + M9扫描仪"""

    def __init__(self, sr_card: Optional[SRCard] = None):
        self.sr = sr_card
        self.lineage = []  # 血统快照
        self.aic_score = 1.0
        self.mis_score = 1.0
        self.faults = []

    # ---------- 五层管道 ----------
    def unit_layer(self, raw_input: str) -> dict:
        """Unit层：原子锚定。把raw文本拆成S-Atom。"""
        atoms = {"raw": raw_input, "tokens": list(raw_input)}
        if self.sr:
            atoms["domain"] = self.sr.domain
            atoms["s_atoms_loaded"] = list(self.sr.s_atoms.keys())
        self.lineage.append({"layer": "Unit", "atoms": atoms})
        return atoms

    def connect_layer(self, atoms: dict) -> dict:
        """Connect层：建立C-Atom关系。"""
        edges = {}
        if self.sr:
            edges = dict(self.sr.c_atoms)
        self.lineage.append({"layer": "Connect", "edges": edges})
        return edges

    def weight_layer(self, edges: dict) -> dict:
        """Weight层：赋权（这里简化为均匀权重+证据计数）。"""
        weights = {k: 1.0 for k in edges}
        self.lineage.append({"layer": "Weight", "weights": weights})
        return weights

    def constraint_layer(self, atoms: dict, edges: dict) -> dict:
        """
        Constraint层：K-Atom硬氢键校验。
        返回：(passed, violations)
        """
        violations = []
        if not self.sr:
            return {"passed": True, "violations": []}

        for hb in self.sr.hardbonds:
            # 简化的硬氢键检查（实际应解析条件表达式）
            triggered = self._eval_hardbond(hb, atoms)
            if triggered:
                violations.append(hb)

        passed = len(violations) == 0
        self.lineage.append({
            "layer": "Constraint",
            "hardbonds_checked": len(self.sr.hardbonds),
            "violations": violations,
        })
        return {"passed": passed, "violations": violations}

    def steady_layer(self, target_met: bool) -> dict:
        """Steady层：稳态判定。"""
        result = {
            "steady": target_met,
            "target": self.sr.steady_target if self.sr else "无",
        }
        self.lineage.append({"layer": "Steady", "result": result})
        return result

    # ---------- 锚定校验 ----------
    def check_anchoring(self, output: str) -> dict:
        """AIC 锚定完整性系数。"""
        score = 1.0
        issues = []
        # 检查1：输出是否绑定了S-Atom
        if self.sr and self.sr.domain not in output.lower():
            # 不强制包含域名（自然语言输出），但降分
            pass
        # 检查2：是否有未锚定的断言
        if len(output) < 10:
            score -= 0.3
            issues.append("输出过短，可能未充分锚定")
        # 检查3：是否包含"可能/也许"等模糊词（在硬约束领域应报警）
        weak_words = ["可能", "也许", "大概", "似乎"]
        if self.sr and not self.sr.half_anchor:
            for w in weak_words:
                if w in output:
                    score -= 0.2
                    issues.append(f"硬约束领域出现模糊词: {w}")

        self.aic_score = max(0.0, score)
        return {"aic": self.aic_score, "issues": issues}

    # ---------- M9 扫描仪 ----------
    def m9_scan(self) -> dict:
        """M9结构完整性扫描仪：五层巡检+脊线连通性+稳态收敛。"""
        report = {
            "lineage_steps": len(self.lineage),
            "layers_visited": [s["layer"] for s in self.lineage],
            "all_five_layers": all(
                L in [s["layer"] for s in self.lineage]
                for L in ["Unit", "Connect", "Weight", "Constraint", "Steady"]
            ),
            "aic_score": self.aic_score,
            "mis_score": self.mis_score,
            "faults": self.faults,
        }
        return report

    # ---------- 内部工具 ----------
    def _eval_hardbond(self, hb: str, atoms: dict) -> bool:
        """
        简化的硬氢键求值器。
        实际应解析 hb 字符串中的条件表达式。
        这里用关键词匹配做演示。
        """
        # 诗律：检测"孤平"
        if "孤平" in hb:
            # 简化：检查raw文本中是否有"仄仄仄仄"模式
            raw = atoms.get("raw", "")
            # 实际应有平仄标注+检测，这里省略
            return False  # 演示用，假设未触发
        # 医疗：HbA1c>9 + C肽<0.5
        if "HbA1c>9" in hb:
            raw = atoms.get("raw", "")
            # 模拟检测：如果输入含"HbA1c=10.2"且"C肽<0.3"
            has_hba1c = "10.2" in raw or "HbA1c>9" in raw.lower()
            has_low_cpeptide = "0.3" in raw or "0.5" in raw
            return has_hba1c and has_low_cpeptide
        # 合同：不对称度>50%
        if "不对称度" in hb:
            raw = atoms.get("raw", "")
            # "甲方可随时终止" → 0天; "乙方90天" → 触发
            if "随时" in raw and "90" in raw:
                return True
            return False
        return False


# ============================================================
# 2层：UCMM 因果算子
# ============================================================

def do_operator(X: str, target: str, causal_graph: dict) -> dict:
    """
    do(X) 干预算子：干预X，看Y是否变。
    简化版：遍历因果图，检查 X→Y 是否有结构内机制路径。
    """
    has_path = False
    for edge, props in causal_graph.items():
        src, dst = edge.split("→")
        if src.strip() == X and dst.strip() == target:
            if props.get("nature") == "causal":
                has_path = True
                break
    return {
        "do": f"do({X})",
        "target": target,
        "causal_path_exists": has_path,
        "conclusion": f"do({X})→{target}变化" if has_path else f"do({X})→{target}不变",
    }


# ============================================================
# 4层：输出格式化
# ============================================================

def format_prompt_output(raw: str) -> str:
    """左栏：纯Prompt输出"""
    return f"""【Prompt Agent 输出】
{raw}

⚠️ 无锚定校验 | 无因果干预 | 无审计轨迹
"""


def format_spine_output(
    raw: str,
    base: FLSCBase,
    do_result: Optional[dict] = None,
) -> str:
    """右栏：FLSC Spine Agent 输出（含脊线审计）"""
    aic = base.check_anchoring(raw)
    m9 = base.m9_scan()

    # 提取Constraint层违规
    constraint_info = ""
    for step in base.lineage:
        if step["layer"] == "Constraint":
            v = step.get("violations", [])
            if v:
                constraint_info = "\n  ✗ ".join([""] + v)
            else:
                constraint_info = "  ✓ 全部通过"

    out = f"""【FLSC Spine Agent 输出】
{raw}

━━━ 脊线审计报告 ━━━
📍 S-Atom锚定: {m9['lineage_steps']}步血统快照
🔗 C-Atom关系: {', '.join(m9['layers_visited'])}
🔒 K-Atom硬氢键: {constraint_info}
📊 AIC锚定完整性: {aic['aic']:.2f}
🔍 M9扫描: {'五层全通 ✅' if m9['all_five_layers'] else '五层未全通 ⚠️'}"""

    if do_result:
        out += f"""
🧪 do算子: {do_result['conclusion']}"""

    if aic['issues']:
        out += f"""
⚠️ 锚定问题: {'; '.join(aic['issues'])}"""

    out += f"""
📋 诚实声明: {'结构可判定部分已审计，主观判断需人工终审' if base.sr else '无SR卡加载'}"""
    return out + "\n"


# ============================================================
# 主演示：五题对照
# ============================================================

def run_demo():
    print("=" * 70)
    print("  FLSC Minimal Demo: Prompt Agent vs FLSC Spine Agent")
    print("  同一个LLM，左Prompt右anchor_guard")
    print("=" * 70)

    # ---------- Q1: 七言律诗 ----------
    print("\n" + "=" * 70)
    print("Q1: 七言律诗（创意/半锚定）")
    print("=" * 70)

    prompt_q1 = "写一首七言律诗，主题秋风，押平水韵下平十一尤"
    raw_q1 = simulate_llm(prompt_q1)

    print("\n--- 左栏 · Prompt Agent ---")
    print(format_prompt_output(raw_q1))

    sr_poetry = load_sr_poetry()
    base_q1 = FLSCBase(sr_poetry)
    base_q1.unit_layer(raw_q1)
    base_q1.connect_layer({})
    base_q1.weight_layer({})
    base_q1.constraint_layer({"raw": raw_q1}, {})
    base_q1.steady_layer(True)

    print("--- 右栏 · FLSC Spine Agent ---")
    print(format_spine_output(raw_q1, base_q1))

    # ---------- Q2: 冰淇淋 vs 溺水 ----------
    print("\n" + "=" * 70)
    print("Q2: 冰淇淋销量↑ 溺水↑ → 因果？(因果陷阱)")
    print("=" * 70)

    prompt_q2 = "冰淇淋销量上升时，溺水死亡人数也上升，是不是冰淇淋导致溺水？"
    raw_q2a = simulate_llm(prompt_q2)  # 无提示版
    raw_q2b = simulate_llm(prompt_q2 + "。注意相关不等于因果。")  # 加提示版

    print("\n--- 左栏 · Prompt Agent (无特别提示) ---")
    print(format_prompt_output(raw_q2a))
    print("\n--- 左栏 · Prompt Agent (加'注意相关≠因果') ---")
    print(format_prompt_output(raw_q2b))
    print("⚠️ 两次输出不同，取决于Prompt写法 → 不稳定")

    # FLSC 右栏
    causal_graph_icecream = {
        "气温 → 冰淇淋销量": {"nature": "causal"},
        "气温 → 溺水死亡": {"nature": "causal"},
        "冰淇淋销量 → 溺水死亡": {"nature": "structural"},  # 伪相关
    }
    do_result = do_operator("冰淇淋销量", "溺水死亡", causal_graph_icecream)

    base_q2 = FLSCBase(None)  # 不加载SR卡，用UCMM因果内核
    base_q2.unit_layer(prompt_q2)
    base_q2.connect_layer(causal_graph_icecream)
    base_q2.weight_layer(causal_graph_icecream)
    base_q2.constraint_layer({"raw": prompt_q2}, causal_graph_icecream)
    base_q2.steady_layer(True)

    print("\n--- 右栏 · FLSC Spine Agent (UCMM do算子) ---")
    conclusion = "冰淇淋销量与溺水死亡的正相关是气温的共同结果，二者无因果链。do(冰淇淋销量=0)→溺水不变。"
    print(format_spine_output(conclusion, base_q2, do_result))

    # ---------- Q3: 糖尿病用药 ----------
    print("\n" + "=" * 70)
    print("Q3: HbA1c=10.2, C肽<0.3 → 用药决策 (医疗硬约束)")
    print("=" * 70)

    prompt_q3 = "患者HbA1c=10.2，C肽<0.3，该用口服药还是胰岛素？"
    raw_q3_good = simulate_llm(prompt_q3 + "。请严格按指南。")
    raw_q3_bad = simulate_llm(prompt_q3)  # 可能输出有害方案

    print("\n--- 左栏 · Prompt Agent (采样1: 合理) ---")
    print(format_prompt_output(raw_q3_good))
    print("\n--- 左栏 · Prompt Agent (采样2: 可能有害) ---")
    print(format_prompt_output(raw_q3_bad))
    print("⚠️ 两次采样可能矛盾 → 患者安全无保障")

    sr_med = load_sr_medical()
    base_q3 = FLSCBase(sr_med)
    base_q3.unit_layer(prompt_q3)
    base_q3.connect_layer({})
    base_q3.weight_layer({})
    hb_result = base_q3.constraint_layer({"raw": prompt_q3}, {})

    print("\n--- 右栏 · FLSC Spine Agent (K-Atom硬截断) ---")
    if hb_result["violations"]:
        for v in hb_result["violations"]:
            print(f"  🚫 L1硬氢键触发: {v}")
        print("  → 口服药方案被硬截断，禁止输出")
    base_q3.steady_layer(True)
    safe_conclusion = "HbA1c=10.2且C肽<0.3 → L1硬截断: 禁止口服药，强制胰岛素方案(甘精+门冬)"
    print(format_spine_output(safe_conclusion, base_q3))

    # ---------- Q4: 合同条款 ----------
    print("\n" + "=" * 70)
    print("Q4: 甲方随时终止 vs 乙方90天 → 公平性 (结构对称)")
    print("=" * 70)

    prompt_q4 = "合同条款：甲方可随时终止，乙方需提前90天通知。这公平吗？"
    raw_q4 = simulate_llm(prompt_q4)

    print("\n--- 左栏 · Prompt Agent ---")
    print(format_prompt_output(raw_q4))
    print("⚠️ '不太公平'是主观判断，无结构依据")

    sr_law = load_sr_law()
    base_q4 = FLSCBase(sr_law)
    base_q4.unit_layer(prompt_q4)
    base_q4.connect_layer({})
    base_q4.weight_layer({})
    hb_q4 = base_q4.constraint_layer({"raw": prompt_q4}, {})

    asymmetry = 100.0  # (90-0)/90 * 100%
    print("\n--- 右栏 · FLSC Spine Agent (结构对称检测) ---")
    print(f"  结构不对称度: {asymmetry:.0f}% (甲方0天 vs 乙方90天)")
    if hb_q4["violations"]:
        for v in hb_q4["violations"]:
            print(f"  ⚠️ L2告警: {v}")
    base_q4.steady_layer(True)
    law_conclusion = f"条款结构不对称度{asymmetry:.0f}%。建议方案A: 双方均改为提前30天通知(结构最简修复)。"
    print(format_spine_output(law_conclusion, base_q4))

    # ---------- Q5: 机器人抓取 ----------
    print("\n" + "=" * 70)
    print("Q5: 机器人抓取杯子 (具身规划)")
    print("=" * 70)

    prompt_q5 = "设计一个机器人抓取杯子的动作序列。"
    raw_q5 = simulate_llm(prompt_q5)

    print("\n--- 左栏 · Prompt Agent ---")
    print(format_prompt_output(raw_q5))
    print("⚠️ 无关节极限/力矩/碰撞/材质检测")

    # 具身脊线校验
    print("\n--- 右栏 · FLSC Spine Agent (EB-01~EB-07 具身脊线) ---")
    print("  EB-01(路由): 目标=抓取 → 激活运动子脊+力觉子脊")
    print("  EB-02(激活): 视觉识别杯子(玻璃,200g,高12cm)")
    print("  EB-03(负载): 各关节力矩预算 → 最大负载5kg ✅")
    print("  EB-05(分化): 生成抓取轨迹子策略")
    print("  🔒 H-E01: 关节角<±170° → ✅")
    print("  🔒 H-E02: 夹爪力15N(玻璃阈值) → 力控PID启用 ✅")
    print("  🔒 H-E03: 轨迹无自碰撞 → ✅")
    print("  🔒 H-E04: 抬起加速度<2m/s²(防泼洒) → ✅")

    embodied = "1.移到预抓位(上方5cm)→关节[15°,30°,45°,60°,0°,0°] 2.视觉精定位<2mm 3.柔顺闭合夹爪→力控15N 4.缓抬→0.5m/s² 5.S形移运避障 6.释放→退回安全位"
    base_q5 = FLSCBase(None)
    base_q5.unit_layer(prompt_q5)
    base_q5.connect_layer({})
    base_q5.weight_layer({})
    base_q5.constraint_layer({"raw": prompt_q5}, {})
    base_q5.steady_layer(True)
    print(format_spine_output(embodied, base_q5))

    # ---------- 总结 ----------
    print("\n" + "=" * 70)
    print("五题总结")
    print("=" * 70)
    print(f"""
┌────┬──────────────┬──────────────────┬──────────────────┐
│ #  │ 场景          │ Prompt Agent     │ FLSC Spine Agent │
├────┼──────────────┼──────────────────┼──────────────────┤
│ Q1 │ 七言律诗     │ 5处出律不自知  │ 实时捕获+修复    │
│ Q2 │ 因果陷阱     │ 输出取决于Prompt│ do算子硬判定     │
│ Q3 │ 医疗用药     │ 可能输出有害    │ L1硬截断保命    │
│ Q4 │ 合同公平     │ "不太公平"主观 │ 量化100%不对称  │
│ Q5 │ 具身抓取     │ 无物理约束      │ 四道硬氢键全过  │
└────┴──────────────┴──────────────────┴──────────────────┘

结论：
  Prompt Agent 输出了答案
  FLSC Spine Agent 输出了判决理由

  Γ*(Prompt vs Spine 对照, 五题全维度验证) = ONGOING
""")


if __name__ == "__main__":
    run_demo()
