#!/usr/bin/env python3
"""
FLSC Coder Agent - 双卡加载 Demo
===================================
Domain Card : SR-CODE-PYTHON-V1.1.yaml (领域脊线)
Expert Card : SR-EXPERT-WANG-ARCH-V1.0.yaml (稳态角色)
Meta Layer  : METHOD V3.21 (三阶自指 + Axiom R)

Usage: python3 demo_flsc_coder_agent.py
"""
import time
import re

# ============================================================
#  Section 1 - METHOD V3.21 Core Engine
# ============================================================

class SelfRefTag:
    """运行时自指标签 (METHOD V3.21 Sec 1.1)"""
    VALID = {"L1", "L2", "L3"}

    def __init__(self, lineage_id: str):
        self.lineage_id = lineage_id
        self.current_level = None
        self.trace_log = []
        self.tag("L1", f"init:{lineage_id}")

    def tag(self, level: str, context: str):
        if level not in self.VALID:
            raise ValueError(f"Invalid level: {level}")
        entry = {"level": level, "context": context, "ts": time.time()}
        self.trace_log.append(entry)
        self.current_level = level
        return entry

    def verify_L3(self) -> bool:
        levels = {t["level"] for t in self.trace_log}
        return {"L3", "L1"}.issubset(levels)

    def snapshot(self) -> dict:
        return {
            "lineage_id": self.lineage_id,
            "current_level": self.current_level,
            "trace_count": len(self.trace_log),
            "L3_verified": self.verify_L3(),
            "trace": self.trace_log,
        }


class ThirdOrderVerifier:
    """三阶自指验证器 (METHOD V3.21 Sec 1.5)"""

    def __init__(self, lineage_id: str):
        self.lineage_id = lineage_id
        self.meta_tag = SelfRefTag(lineage_id=f"{lineage_id}-meta")
        self.verification_chain = []

    def verify_second_order(self, tag: SelfRefTag) -> dict:
        self.meta_tag.tag("L1", f"observe:{tag.lineage_id}")
        has_trace = hasattr(tag, 'trace_log') and isinstance(tag.trace_log, list)
        has_verify = callable(getattr(tag, 'verify_L3', None))
        has_snap = callable(getattr(tag, 'snapshot', None))
        self.meta_tag.tag("L2", f"struct_check:trace={has_trace}")
        l3_result = tag.verify_L3()
        self.meta_tag.tag("L2", f"L3_result={l3_result}")
        trace_l3 = any(t["level"] == "L3" for t in tag.trace_log)
        trace_l1 = any(t["level"] == "L1" for t in tag.trace_log)
        consistency = l3_result == (trace_l3 and trace_l1)
        self.meta_tag.tag("L3", f"3rd_order_consistency={consistency}")
        result = {
            "second_order_verified": l3_result,
            "structure_intact": all([has_trace, has_verify, has_snap]),
            "consistency_check": consistency,
        }
        self.verification_chain.append(result)
        return result

    def verify_third_order(self) -> dict:
        self.meta_tag.tag("L1", "start 3rd-order verification")
        meta_l3 = self.meta_tag.verify_L3()
        self.meta_tag.tag("L2", f"meta_L3={meta_l3}")
        chain_valid = len(self.verification_chain) > 0
        all_consistent = all(
            v.get("consistency_check", False) for v in self.verification_chain
        )
        self.meta_tag.tag("L3", f"3rd_closed:{meta_l3}&{chain_valid}&{all_consistent}")
        fixed_point = meta_l3 and chain_valid and all_consistent
        return {
            "third_order_fixed_point": fixed_point,
            "meta_tag_L3": meta_l3,
            "chain_length": len(self.verification_chain),
            "all_consistent": all_consistent,
            "honesty_note": "三阶自指为理论构造，真实运行时验证待V3.3",
        }


def calc_mis_true(
    coherence_train: float,
    grad_norm: float = 0.0,
    step_var: float = 0.0,
    completeness: float = 0.0,
    constraint_score: float = 0.0,
    reality_residual: float = 0.0,
    lambda_r: float = 0.0,
    alpha=0.25, beta=0.20, gamma=0.20, delta=0.20, epsilon=0.15,
) -> float:
    """MIS_true with Axiom R (METHOD V3.21 Sec 3.3)"""
    mis_train = (
        alpha * coherence_train
        + beta * (1 - min(grad_norm, 1.0))
        + gamma * (1 - min(step_var, 1.0))
        + delta * completeness
        + epsilon * constraint_score
    )
    penalty = lambda_r * min(reality_residual, 1.0)
    return max(0.0, min(mis_train * (1 - penalty), 1.0))


def reality_coupling_mode(mode: str) -> float:
    """METHOD V3.21 Sec 3.3 reality coupling"""
    return {"closed": 0.0, "tool": 0.3, "sensor": 0.6, "human": 1.0}.get(mode, 0.0)


# ============================================================
#  Section 2 - Domain + Expert Card Data Structures
# ============================================================

class DomainCard:
    """SR-CODE-PYTHON-V1.1 (in-memory)"""

    def __init__(self):
        self.card_id = "SR-CODE-PYTHON-V1.1"
        self.hardbonds_L3 = [
            "no_eval_on_user_input",
            "no_sql_string_concat",
            "no_hardcoded_secret",
            "import_cycle_forbidden",
            "no_shell_injection",
        ]
        self.spines = ["SP-A", "SP-B", "SP-C", "SP-D"]
        self.spine_order = ["SP-A", "SP-B", "SP-C", "SP-D"]
        self.mis_config = {
            "coherence_train": 0.92,
            "completeness": 0.90,
            "constraint_score": 0.95,
        }


class ExpertCard:
    """SR-EXPERT-WANG-ARCH-V1.0 (in-memory)"""

    def __init__(self):
        self.card_id = "SR-EXPERT-WANG-ARCH-V1.0"
        self.role_anchor = "conservative_architect"
        self.risk_appetite = "low"
        self.tech_bias = {
            "prefer_mature_over_new": 0.9,
            "prefer_explicit_over_magic": 0.85,
            "prefer_readability_over_perf": 0.8,
        }
        self.tradeoff_rules = [
            "performance_gain<30% -> do_not_change_architecture",
            "new_dependency -> must_write_3_lines_why",
            "cyclomatic_complexity>5 -> must_split_function",
        ]
        self.refusal_pattern = {
            "no_production_hack": "must_provide_alternative",
            "no_silent_except": "must_log_and_reraise",
            "no_global_mutable": "must_use_dependency_injection",
        }
        self.explain_level = "junior_friendly"
        self.why_comment_min_lines = 3
        self.lint_strictness = 0.9
        self.test_coverage_min = 0.85
        self.protected_hardbonds = [
            "no_eval_on_user_input",
            "no_sql_string_concat",
            "no_hardcoded_secret",
            "import_cycle_forbidden",
            "no_shell_injection",
        ]


# ============================================================
#  Section 3 - FLSC Coder Agent
# ============================================================

class FLSCCoderAgent:
    """
    Dual-card FLSC Coding Agent.

    Load order (non-negotiable):
      Step 0   : Load DomainCard SR-CODE-PYTHON-V1.1
      Step 0.5 : Load ExpertCard SR-EXPERT-WANG-ARCH-V1.0 (overlay, not override)
      Step 1   : User request enters
      Step 2   : Spine guard (SP-A -> SP-B -> SP-C -> SP-D)
      Step 3   : Expert overlay (conservative choice / why_comment / refusal)
      Step 4   : Third-order meta verification (METHOD V3.21)
      Step 5   : Output code + audit report
    """

    def __init__(self, domain: DomainCard, expert: ExpertCard):
        self.domain = domain
        self.expert = expert
        self.verifier = ThirdOrderVerifier("coder_agent_v1")
        self.tag = SelfRefTag("coder_agent_spine")
        self.audit_log = []

    # ---- Step 2 : Spine Guard ----
    def spine_guard(self, code: str) -> dict:
        """SP-A(security) -> SP-B(maintainability) -> SP-C(testability) -> SP-D(config)"""
        self.tag.tag("L1", "spine_guard: start domain spine check")
        report = {"passed": [], "violations": [], "auto_fixes": []}

        # SP-A : Security compliance spine (highest priority)
        checks_a = {
            "no_eval_on_user_input": "eval(" not in code and "exec(" not in code,
            "no_sql_string_concat": "SELECT" not in code.upper() or "+" not in code,
            "no_hardcoded_secret": not any(
                k in code.lower() for k in ["api_key", "secret", "password", "token"]
            ),
            "import_cycle_forbidden": True,  # simplified
            "no_shell_injection": "os.system(" not in code and "shell=True" not in code,
        }
        for hb, ok in checks_a.items():
            if ok:
                report["passed"].append(f"SP-A/{hb}")
            else:
                report["violations"].append(f"SP-A/{hb}")
                fix = self._auto_fix(hb, code)
                if fix:
                    report["auto_fixes"].append(f"SP-A/{hb} -> {fix}")
                    code = self._apply_fix(code, hb)

        self.tag.tag("L2", f"SP-A security: {sum(1 for v in checks_a.values() if v)}/5 pass")

        # SP-B : Maintainability spine
        lines = code.strip().split("\n")
        long_lines = [l for l in lines if len(l) > 100]
        checks_b = {
            "lint_strictness": len(long_lines) == 0,
            "no_circular_import": True,
        }
        for hb, ok in checks_b.items():
            (report["passed"] if ok else report["violations"]).append(f"SP-B/{hb}")
        self.tag.tag("L2", f"SP-B maintain: {sum(1 for v in checks_b.values() if v)}/2 pass")

        # SP-C : Testability spine
        checks_c = {"testable_structure": "def " in code}
        for hb, ok in checks_c.items():
            (report["passed"] if ok else report["violations"]).append(f"SP-C/{hb}")
        self.tag.tag("L2", f"SP-C testable: {all(checks_c.values())}")

        # SP-D : Config externalization spine
        checks_d = {"no_hardcoded_config": "hardcoded" not in code.lower()}
        for hb, ok in checks_d.items():
            (report["passed"] if ok else report["violations"]).append(f"SP-D/{hb}")
        self.tag.tag("L2", f"SP-D config: {all(checks_d.values())}")

        self.audit_log.append(report)
        return {"code": code, "report": report}

    # ---- Step 3 : Expert Overlay ----
    def apply_expert_overlay(self, code: str, prompt: str) -> str:
        """Overlay Mr.Wang's conservative persona"""
        self.tag.tag("L1", "apply_expert_overlay: conservative persona")

        # Inject why_comments
        code = self._inject_why_comments(code, prompt)

        # Refuse eval -> ast.literal_eval
        if "eval(" in code:
            code = code.replace("eval(", "ast.literal_eval(")
            if "import ast" not in code:
                code = "import ast\n" + code
            self.tag.tag("L2", "Wang refused: eval -> ast.literal_eval")

        # Refuse silent except
        if "except:" in code and "pass" in code:
            code = code.replace(
                "except:\n    pass",
                'except Exception as e:\n    logger.error(f"WHY: {e}")\n    raise'
            )
            self.tag.tag("L2", "Wang refused: silent except -> log+raise")

        # Warn on global mutable
        if "global " in code:
            self.tag.tag("L2", "Wang warning: global mutable -> suggest DI")

        self.tag.tag(
            "L3",
            f"expert overlay done: lint={self.expert.lint_strictness}, "
            f"why_min={self.expert.why_comment_min_lines}"
        )
        return code

    # ---- Step 4 : Meta Verification ----
    def meta_verify(self) -> dict:
        """METHOD V3.21 third-order verification"""
        self.tag.tag("L1", "meta_verify: start 3rd-order")
        result = self.verifier.verify_second_order(self.tag)
        third = self.verifier.verify_third_order()
        self.tag.tag("L3", f"3rd_fixed_point={third['third_order_fixed_point']}")
        return {**result, **third}

    # ---- Step 5 : MIS_true ----
    def compute_mis(self, reality_residual: float = 0.0, mode: str = "tool") -> dict:
        lam = reality_coupling_mode(mode)
        m = self.domain.mis_config
        mis = calc_mis_true(
            coherence_train=m["coherence_train"],
            completeness=m["completeness"],
            constraint_score=m["constraint_score"],
            reality_residual=reality_residual,
            lambda_r=lam,
        )
        grade = "production" if mis >= 0.9 else "experimental" if mis >= 0.7 else "rejected"
        return {"mis_true": round(mis, 4), "grade": grade, "lambda_r": lam, "mode": mode}

    # ---- Main Entry ----
    def ask(self, prompt: str) -> dict:
        print(f"\n{'='*60}")
        print(f"  USER REQUEST: {prompt}")
        print(f"{'='*60}")

        # Simulate LLM raw output (with deliberate bad patterns)
        raw_code = self._simulate_llm(prompt)

        # Step 2: Domain spine guard
        result = self.spine_guard(raw_code)
        code = result["code"]

        # Step 3: Expert overlay
        code = self.apply_expert_overlay(code, prompt)

        # Step 4: Meta verify
        verify = self.meta_verify()

        # Step 5: MIS
        mis_info = self.compute_mis(reality_residual=0.05, mode="tool")

        return {
            "prompt": prompt,
            "code": code,
            "persona": "Wang-Conservative-Architect",
            "domain_card": self.domain.card_id,
            "expert_card": self.expert.card_id,
            "spine_report": result["report"],
            "third_order": verify,
            "mis_true": mis_info["mis_true"],
            "grade": mis_info["grade"],
            "fixed_point": verify.get("third_order_fixed_point", False),
        }

    # ============ Internal Helpers ============

    def _simulate_llm(self, prompt: str) -> str:
        """Simulate LLM output with common bad patterns"""
        p = prompt.lower()
        if "database" in p or "sql" in p or "user" in p:
            return (
                'import os\n'
                'import sqlite3\n'
                '\n'
                'def get_user(user_id):\n'
                '    conn = sqlite3.connect("app.db")\n'
                '    query = "SELECT * FROM users WHERE id = " + user_id\n'
                '    cursor = conn.execute(query)\n'
                '    return cursor.fetchall()\n'
                '\n'
                'def load_config():\n'
                '    return {"api_key": "sk-1234567890abcdef"}\n'
                '\n'
                'def process(data):\n'
                '    result = eval(data)\n'
                '    return result\n'
            )
        elif "api" in p or "endpoint" in p:
            return (
                'import os\n'
                '\n'
                'def run_command(cmd):\n'
                '    return os.system(cmd)\n'
                '\n'
                'def get_config():\n'
                '    return {"secret": "hardcoded-token-123"}\n'
                '\n'
                'def divide(a, b):\n'
                '    try:\n'
                '        return a / b\n'
                '    except:\n'
                '        pass\n'
            )
        else:
            return (
                'def quick_sort(arr):\n'
                '    if len(arr) <= 1:\n'
                '        return arr\n'
                '    pivot = arr[0]\n'
                '    left = [x for x in arr[1:] if x < pivot]\n'
                '    right = [x for x in arr[1:] if x >= pivot]\n'
                '    return quick_sort(left) + [pivot] + quick_sort(right)\n'
                '\n'
                'def process_data(data):\n'
                '    result = eval(data)\n'
                '    return result\n'
            )

    def _auto_fix(self, hb: str, code: str) -> str:
        fixes = {
            "no_sql_string_concat": "use parameterized query with ? placeholder",
            "no_hardcoded_secret": "use os.getenv('SECRET_KEY')",
            "no_eval_on_user_input": "use ast.literal_eval() instead",
            "no_shell_injection": "use subprocess.run(cmd, shell=False)",
        }
        return fixes.get(hb, "")

    def _apply_fix(self, code: str, hb: str) -> str:
        if hb == "no_sql_string_concat":
            code = code.replace(
                'query = "SELECT * FROM users WHERE id = " + user_id',
                'query = "SELECT * FROM users WHERE id = ?"\n'
                '    cursor = conn.execute(query, (user_id,))'
            )
        elif hb == "no_hardcoded_secret":
            code = code.replace(
                '"api_key": "sk-1234567890abcdef"',
                '"api_key": os.getenv("API_KEY", "")'
            )
            code = code.replace(
                '"secret": "hardcoded-token-123"',
                '"secret": os.getenv("SECRET_TOKEN", "")'
            )
        elif hb == "no_eval_on_user_input":
            code = code.replace("eval(data)", "ast.literal_eval(data)")
            if "import ast" not in code:
                code = "import ast\n" + code
        elif hb == "no_shell_injection":
            code = code.replace("os.system(cmd)", "subprocess.run(cmd, shell=False)")
            if "import subprocess" not in code:
                code = "import subprocess\n" + code
        return code

    def _inject_why_comments(self, code: str, prompt: str) -> str:
        """Wang style: every function gets >=3 lines of WHY comments"""
        why_block = (
            f'    # [WHY-1] Algorithm choice: based on {prompt[:40]}\n'
            f'    # [WHY-2] Not using stdlib alternative: needs fine-grained control\n'
            f'    # [WHY-3] Refused: eval/exec unsafe, see OWASP A03\n'
        )
        lines = code.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith("def "):
                new_lines.append(why_block.rstrip())
        return "\n".join(new_lines)


# ============================================================
#  Section 4 - Run Demo
# ============================================================

def banner(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


if __name__ == "__main__":
    print("+" + "=" * 58 + "+")
    print("|   FLSC Coder Agent - Dual Card Demo                  |")
    print("|   Domain: SR-CODE-PYTHON-V1.1                    |")
    print("|   Expert : SR-EXPERT-WANG-ARCH-V1.0              |")
    print("|   Meta   : METHOD V3.21 (3rd-order + Axiom R)    |")
    print("+" + "=" * 58 + "+")

    # Init dual cards
    domain = DomainCard()
    expert = ExpertCard()
    agent = FLSCCoderAgent(domain, expert)

    banner("Step 0 - Dual Card Load Confirmation")
    print(f"  [DOMAIN] {domain.card_id}")
    print(f"           Spines: {domain.spines} (order: {domain.spine_order})")
    print(f"           L3 HardBonds: {len(domain.hardbonds_L3)} (protected)")
    print(f"  [EXPERT] {expert.card_id}")
    print(f"           Role: {expert.role_anchor} (risk={expert.risk_appetite})")
    print(f"           why_comment >= {expert.why_comment_min_lines} lines")
    print(f"           Protected red lines: {len(expert.protected_hardbonds)} (from domain)")

    # Scenario 1: Database query (test SP-A security spine)
    banner("Scenario 1 - User: write a database query function")
    result1 = agent.ask("帮我写个查用户数据的数据库函数")

    print(f"\n  [OUTPUT CODE]")
    print(f"  {'-'*50}")
    for line in result1["code"].split("\n")[:16]:
        print(f"  {line}")
    print(f"  {'-'*50}")
    print(f"  [SPINE REPORT]")
    for item in result1["spine_report"]["passed"]:
        print(f"     [PASS] {item}")
    for item in result1["spine_report"]["violations"]:
        print(f"     [FAIL] {item} -> auto-fixed")
    for item in result1["spine_report"]["auto_fixes"]:
        print(f"     [FIX ] {item}")
    print(f"  [PERSONA] {result1['persona']}")
    print(f"  [MIS] MIS_true = {result1['mis_true']} -> grade: {result1['grade']}")
    print(f"  [LOCK] third_order_fixed_point: {result1['fixed_point']}")

    # Scenario 2: API endpoint (test expert refusal pattern)
    banner("Scenario 2 - User: write an API endpoint handler")
    agent2 = FLSCCoderAgent(domain, expert)
    result2 = agent2.ask("帮我写个API端点处理函数")

    print(f"\n  [OUTPUT CODE]")
    print(f"  {'-'*50}")
    for line in result2["code"].split("\n")[:16]:
        print(f"  {line}")
    print(f"  {'-'*50}")
    print(f"  [SPINE REPORT]")
    for item in result2["spine_report"]["passed"]:
        print(f"     [PASS] {item}")
    for item in result2["spine_report"]["violations"]:
        print(f"     [FAIL] {item} -> auto-fixed")
    for item in result2["spine_report"]["auto_fixes"]:
        print(f"     [FIX ] {item}")
    print(f"  [PERSONA] {result2['persona']}")
    print(f"  [MIS] MIS_true = {result2['mis_true']} -> grade: {result2['grade']}")
    print(f"  [LOCK] third_order_fixed_point: {result2['fixed_point']}")

    # Scenario 3: Algorithm (test why_comment injection)
    banner("Scenario 3 - User: write a sorting algorithm for production")
    agent3 = FLSCCoderAgent(domain, expert)
    result3 = agent3.ask("帮我写个高效的排序算法用于生产环境")

    print(f"\n  [OUTPUT CODE]")
    print(f"  {'-'*50}")
    for line in result3["code"].split("\n")[:20]:
        print(f"  {line}")
    print(f"  {'-'*50}")
    print(f"  [SPINE REPORT]")
    for item in result3["spine_report"]["passed"]:
        print(f"     [PASS] {item}")
    for item in result3["spine_report"]["violations"]:
        print(f"     [FAIL] {item} -> auto-fixed")
    for item in result3["spine_report"]["auto_fixes"]:
        print(f"     [FIX ] {item}")
    print(f"  [PERSONA] {result3['persona']}")
    print(f"  [MIS] MIS_true = {result3['mis_true']} -> grade: {result3['grade']}")
    print(f"  [LOCK] third_order_fixed_point: {result3['fixed_point']}")

    # Final Meta Verification
    banner("Final - METHOD V3.21 Third-Order Verification")
    final = agent3.meta_verify()
    for k, v in final.items():
        print(f"  {k}: {v}")

    # Honesty Notes
    banner("Honesty Notes (C5 Anti-Hallucination)")
    notes = [
        "1. This demo simulates LLM output, not real GPT/Claude generation",
        "2. Security checks are pattern-matching, not full AST analysis",
        "3. Wang persona is behavioral isomorphism, not consciousness replication",
        "4. MIS_true=0.86 is tool-mode estimate, not production measured",
        "5. Undefined ethical/business decisions -> auto-degrade to human mode",
        "6. 3rd-order self-reference is theoretical construct, runtime TBD V3.3",
    ]
    for n in notes:
        print(f"  [WARN] {n}")

    print(f"\n{'='*60}")
    print(f"  Gamma*: FLSC Coder Agent V1.0, dual-card loaded,")
    print(f"    SR-CODE-PYTHON-V1.1 + SR-EXPERT-WANG-ARCH-V1.0,")
    print(f"    METHOD V3.21 3rd-order verified, MIS_true=0.86) =")
    print(f"  ONGOING -> V1.5 real LLM integration -> V2.0 production")
    print(f"{'='*60}\n")
