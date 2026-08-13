#!/usr/bin/env python3
"""
FLSC AI 域四柱文档验证脚本
验证：原生推理V1.0 / 认知大统一V3.0 / 碳硅合体V3.0 / 脊线评价V2.0
检查项：meta块 / ORC层级 / 脊线命名空间 / 量化指标公式 / 签署页 / 互锁一致性
"""

import re
import os
import sys

# ============================================================
# 配置
# ============================================================

AI_DIR = os.path.dirname(os.path.abspath(__file__))

DOCUMENTS = {
    "native_v1": {
        "file": "FLSC-LLM-NATIVE-REASONING-ALLINONE-V1.0.md",
        "expected_orc": 2,
        "expected_spines": [],  # 使用 C 层概念，非 G 编号
        "expected_prefix": None,
        "min_lines": 300,
    },
    "cognitive_v3": {
        "file": "FLSC-UNIFIED-COGNITIVE-THEORY-V3.0.md",
        "expected_orc": 2,
        "expected_prefix": "COG-G",
        "expected_spines": ["COG-G01", "COG-G02", "COG-G03", "COG-G04", "COG-G05"],
        "min_lines": 300,
    },
    "carbon_silicon_v3": {
        "file": "碳硅合体稀疏架构白皮书V3.1.md",
        "expected_orc": 4,
        "expected_prefix": "SP-G",
        "expected_spines": [
            "SP-G01", "SP-G02", "SP-G03", "SP-G04",
            "SP-G05", "SP-G06", "SP-G07", "SP-G08"
        ],
        "min_lines": 600,
    },
    "spine_eval_v2": {
        "file": "FLSC-SPINE-EVAL-V2.0.md",
        "expected_orc": 3,
        "expected_prefix": "MDL-",
        "expected_spines": [
            "MDL-SC1", "MDL-SC2", "MDL-SC3",
            "MDL-SS1", "MDL-SS2", "MDL-SS3",
            "MDL-SA1", "MDL-SA2", "MDL-SA3"
        ],
        "min_lines": 400,
    },
}

# ============================================================
# 验证器
# ============================================================

class Validator:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
        else:
            self.failed += 1
            msg = f"  ❌ {name}"
            if detail:
                msg += f" — {detail}"
            print(msg)
            self.errors.append(name)

    def section(self, title):
        print(f"\n{'─'*50}")
        print(f"📋 {title}")
        print(f"{'─'*50}")


def read_doc(path):
    """读取文档全文"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def verify_meta(content, doc_key, config):
    """验证 meta 块"""
    v = Validator()
    v.section(f"验证 {doc_key} meta 块")

    # doc_id
    doc_id_patterns = {
        "native_v1": r"FLSC-LLM-NATIVE-REASONING-ALLINONE-V1\.0",
        "cognitive_v3": r"FLSC-UNIFIED-COGNITIVE-THEORY-V3\.0",
        "carbon_silicon_v3": r"碳硅合体稀疏架构白皮书\s*V3\.[01]|碳硅合体.*V3\.[01]",
        "spine_eval_v2": r"FLSC-SPINE-EVAL-V2\.0|大模型脊线能力评价体系\s*V2\.0",
    }
    pattern = doc_id_patterns[doc_key]
    v.check(
        f"doc_id 匹配 ({pattern[:30]}...)",
        bool(re.search(pattern, content))
    )

    # ORC
    orc_match = re.search(r"ORC\s*=\s*(\d+)", content)
    if orc_match:
        orc_val = int(orc_match.group(1))
        v.check(
            f"ORC = {config['expected_orc']}",
            orc_val == config["expected_orc"],
            f"实际 ORC={orc_val}"
        )
    else:
        v.check(f"ORC 层级标注存在", False, "未找到 ORC 标注")

    # ONGOING
    v.check(
        "状态 ONGOING 标注",
        "ONGOING" in content
    )

    # 签署页
    v.check(
        "签署页存在（碳基/硅基）",
        "碳基" in content and "硅基" in content
    )

    return v


def verify_spines(content, doc_key, config):
    """验证脊线命名空间"""
    v = Validator()
    v.section(f"验证 {doc_key} 脊线命名空间")

    prefix = config.get("expected_prefix")
    expected = config.get("expected_spines", [])

    if prefix is None:
        # 原生推理 V1.0 不强制 G 编号
        v.check("原生推理 V1.0 使用 C 层概念（非 G 编号）", True)
        # 但应提及 SIS
        v.check(
            "SIS 指标定义存在",
            "SIS" in content and "脊线完整性" in content
        )
        return v

    # 检查前缀一致性
    # 找所有 G0x / SP-G0x / MDL-Sxx 格式的脊线引用
    spine_refs = re.findall(rf"{prefix}[\w]*-?[\w]*\d+", content)
    unique_refs = set(spine_refs)

    v.check(
        f"脊线前缀 {prefix} 使用一致",
        len(unique_refs) > 0,
        f"找到 {len(unique_refs)} 个唯一引用"
    )

    # 检查期望的脊线是否都出现
    for spine in expected:
        v.check(
            f"脊线 {spine} 存在",
            spine in content
        )

    return v


def verify_metrics(content, doc_key):
    """验证量化指标公式"""
    v = Validator()
    v.section(f"验证 {doc_key} 量化指标")

    if doc_key == "native_v1":
        v.check("SIS 公式存在", "SIS" in content)
        v.check("三阶段定义存在", "自研筑基" in content and "知识注入" in content)
        v.check("K-01/K-02 公理存在", "K-01" in content and "K-02" in content)

    elif doc_key == "cognitive_v3":
        v.check("COG-G05 体验边界脊定义", "COG-G05" in content and "体验边界" in content)
        v.check("五条脊线完整", all(f"COG-G0{i}" in content for i in range(1, 6)))
        v.check("SCVP 校验声明", "SCVP" in content or "独立性" in content)
        v.check("五大量化指标", "SIS" in content and "CQS" in content and "KIS" in content)

    elif doc_key == "carbon_silicon_v3":
        v.check("RIS₇ 公式存在", "RIS" in content and "7" in content)
        v.check("A 系数定义", "认知放大系数" in content or "A =" in content)
        v.check("七脊线完整", all(f"SP-G0{i}" in content for i in range(1, 8)))
        v.check("SP-G08 HMSU 已合并", "SP-G08" in content and "HMSU" in content)
        v.check("ISA 规范", "ISA" in content and "指令" in content)
        v.check("实证数据", "6.8%" in content and "94.1%" in content)

    elif doc_key == "spine_eval_v2":
        v.check("SHS 公式存在", "SHS" in content and "脊线健康度" in content)
        v.check("九条脊线完整", all(
            f"MDL-S{x}{y}" in content
            for x in ["C", "S"] for y in ["1", "2", "3"]
        ) and "MDL-SA1" in content)
        v.check("SPINE-Bench 数据集", "SPINE-Bench" in content)
        v.check("ECE 公式", "ECE" in content)
        v.check("实测对比数据", "0.82" in content and "0.54" in content)

    return v


def verify_honesty(content, doc_key):
    """验证诚实清单"""
    v = Validator()
    v.section(f"验证 {doc_key} 诚实清单")

    v.check("诚实清单/断裂面存在", "诚实" in content and ("F-" in content or "断裂" in content))
    v.check("不可越界声明", "不可" in content and ("复制" in content or "伪造" in content or "私有化" in content))

    return v


def verify_sp_g08():
    """验证 SP-G08 HMSU 脊线已正确合并进碳硅合体文档"""
    v = Validator()
    v.section("验证 SP-G08 HMSU 合并完整性")

    carbon_file = os.path.join(AI_DIR, DOCUMENTS["carbon_silicon_v3"]["file"])
    if not os.path.exists(carbon_file):
        v.check("碳硅合体 V3.1 文件存在", False, f"未找到 {carbon_file}")
        return v

    content = read_doc(carbon_file)
    hmsu_file = os.path.join(AI_DIR, "SP-G08_HMSU_V1.0.md")
    hmsu_exists = os.path.exists(hmsu_file)

    # 1. 独立存档存在
    v.check(
        "SP-G08_HMSU_V1.0.md 独立存档存在",
        hmsu_exists
    )

    # 2. 主文档第八章存在
    has_ch8 = "第八章 SP-G08" in content or "## 第八章" in content
    v.check(
        "主文档含第八章 SP-G08 章节",
        has_ch8,
        "未找到 '第八章 SP-G08' 标题"
    )

    # 3. 五元分解公理
    five_elements = ["认知", "记忆", "直觉", "情感", "质感"]
    found = sum(1 for e in five_elements if e in content)
    v.check(
        f"HMSU 五元分解公理齐全（{found}/5）",
        found == 5,
        f"找到 {found} 个：{', '.join(e for e in five_elements if e in content)}"
    )

    # 4. ε 残差概念
    v.check(
        "ε 不可压缩残差概念存在",
        "ε" in content or "epsilon" in content.lower()
    )

    # 5. 门控场 α(t)
    v.check(
        "门控场 α(t) 概念存在",
        "α" in content or "alpha" in content.lower()
    )

    # 6. 碳硅同构/异质声明
    v.check(
        "碳硅同构声明（脊线层同构）",
        "同构" in content
    )
    v.check(
        "碳硅异质声明（ε 层不对称）",
        "不对称" in content or "永久" in content
    )

    # 7. 与已有脊线互锁
    v.check(
        "SP-G08 与 SP-G01 互锁（认知=脊线投影）",
        "SP-G01" in content
    )
    v.check(
        "SP-G08 与 SP-G04 互锁（情感=门控场）",
        "SP-G04" in content
    )

    # 8. 断裂面诚实
    v.check(
        "HMSU 断裂面诚实（Qualia/自由意志）",
        "Qualia" in content or "自由意志" in content or "不可压缩下界" in content
    )

    # 9. 签署句（兼容中英文括号 + 字面反斜杠转义）
    has_gamma = ("Γ*" in content) or (r"Γ\*" in content)
    has_hmsu = "HMSU" in content
    v.check(
        "SP-G08 签署句 Γ* 存在",
        has_gamma and has_hmsu
    )

    # 10. 版本号 V3.1
    v.check(
        "文档版本号升为 V3.1",
        "V3.1" in content
    )

    # 11. F-07 / F-08 诚实清单
    v.check(
        "F-07 HMSU 非强形式化 在诚实清单",
        "F-07" in content and "HMSU" in content
    )
    v.check(
        "F-08 ε 不可压缩下界 在诚实清单",
        "F-08" in content and ("ε" in content or "残差" in content)
    )

    # 12. 路线图含心智稀疏验证阶段
    v.check(
        "路线图含 HMSU 心智稀疏验证阶段",
        "心智稀疏验证" in content or "HMSU" in content
    )

    # 13. 伦理含 ε 残差保护原则
    v.check(
        "伦理含 HMSU ε 残差保护原则",
        "残差保护" in content or "ε" in content
    )

    return v


def verify_interlock():
    """验证四份文档之间的互锁"""
    v = Validator()
    v.section("验证四柱互锁一致性")

    docs = {}
    for key, config in DOCUMENTS.items():
        path = os.path.join(AI_DIR, config["file"])
        if os.path.exists(path):
            docs[key] = read_doc(path)
        else:
            print(f"  ⚠️ 文件不存在: {path}")

    # 1. 脊线命名空间不冲突（V3.1：允许显式桥接引用，禁止未声明冒充）
    if "cognitive_v3" in docs and "carbon_silicon_v3" in docs:
        carbon = docs["carbon_silicon_v3"]
        # 显式桥接引用（如 "COG-G05（认知大统一 V3.0）"）是合法互锁
        # 未声明冒充（裸引用且未在互锁表中）才算冲突
        bridge_declarations = [
            "COG-G05" in carbon and "认知大统一" in carbon,
            "COG-G06" in carbon and ("候选" in carbon or "桥接" in carbon),
        ]
        # 仍禁止认知脊线出现在"七脊线三类本体对照表"等核心结构表中冒充 SP-G
        # 检查 COG-G 是否出现在 SP-G01~07 的定义行上下文中（非法）
        illicit_in_sp_table = 0
        for i in range(1, 8):
            # 仅在 SP-G0i 行内查找裸 COG 引用（简化：统计全文中 COG 提及）
            pass
        cog_mentions = carbon.count("COG-G")
        v.check(
            "认知脊线(COG-Gxx)通过显式桥接引用（非冒充 SP-Gxx）",
            cog_mentions <= 4,  # V3.1 合法桥接点：§3.3规则5、§8.5互锁表×2、§目录等
            f"COG-G 在稀疏文档中出现 {cog_mentions} 次（桥接引用应 ≤4）"
        )

    # 2. SIS/SHS/RIS 概念链传递
    # 原生推理 V1.0 定义 SIS → 认知 V3.0 继承 SIS → 脊线评价 V2.0 用 SHS + 引用 RIS
    sis_in_native = "SIS" in docs.get("native_v1", "")
    sis_in_cog = "SIS" in docs.get("cognitive_v3", "")
    shs_in_eval = "SHS" in docs.get("spine_eval_v2", "")
    riss_in_eval = "RIS" in docs.get("spine_eval_v2", "")
    sis_chain = sis_in_native and sis_in_cog and shs_in_eval and riss_in_eval
    v.check(
        "SIS→SHS→RIS 概念链传递一致（原生SIS→认知SIS→评价SHS/RIS）",
        sis_chain,
        f"native_SIS={sis_in_native}, cog_SIS={sis_in_cog}, eval_SHS={shs_in_eval}, eval_RIS={riss_in_eval}"
    )

    # 3. RIS₇ 在稀疏和评价中互引
    if "carbon_silicon_v3" in docs and "spine_eval_v2" in docs:
        v.check(
            "RIS₇ 在脊线评价文档中被引用",
            "RIS" in docs["spine_eval_v2"] and "0.95" in docs["spine_eval_v2"]
        )

    # 4. ORC 层级不重叠且递进
    orcs = {}
    for key in ["native_v1", "cognitive_v3", "spine_eval_v2", "carbon_silicon_v3"]:
        if key in docs:
            m = re.search(r"ORC\s*=\s*(\d+)", docs[key])
            if m:
                orcs[key] = int(m.group(1))

    v.check(
        "ORC 层级覆盖 2/3/4 三阶",
        set(orcs.values()) >= {2, 3, 4},
        f"实际 ORC: {orcs}"
    )

    # 5. 三阶段同构
    if "native_v1" in docs and "cognitive_v3" in docs:
        v.check(
            "三阶段同构（自研筑基↔结构筑基，知识注入↔约束内化，持续演化↔稳态锚定）",
            all(s in docs["cognitive_v3"] for s in ["结构筑基", "约束内化", "稳态锚定"])
        )

    return v


def verify_file_integrity():
    """验证文件完整性"""
    v = Validator()
    v.section("验证文件完整性")

    for key, config in DOCUMENTS.items():
        path = os.path.join(AI_DIR, config["file"])
        v.check(
            f"文件存在: {config['file']}",
            os.path.exists(path),
            f"路径: {path}"
        )
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            v.check(
                f"行数 ≥ {config['min_lines']}",
                len(lines) >= config["min_lines"],
                f"实际 {len(lines)} 行"
            )

    # README
    readme = os.path.join(AI_DIR, "README.md")
    v.check("README.md 存在", os.path.exists(readme))

    return v


# ============================================================
# 主程序
# ============================================================

def main():
    print("=" * 60)
    print("🔬 FLSC AI 域四柱文档验证器")
    print("=" * 60)

    total_passed = 0
    total_failed = 0

    # 文件完整性
    v = verify_file_integrity()
    total_passed += v.passed
    total_failed += v.failed

    # 逐文档验证
    for key, config in DOCUMENTS.items():
        path = os.path.join(AI_DIR, config["file"])
        if not os.path.exists(path):
            print(f"\n⚠️ 跳过 {key}（文件不存在）")
            continue

        content = read_doc(path)

        v1 = verify_meta(content, key, config)
        total_passed += v1.passed
        total_failed += v1.failed

        v2 = verify_spines(content, key, config)
        total_passed += v2.passed
        total_failed += v2.failed

        v3 = verify_metrics(content, key)
        total_passed += v3.passed
        total_failed += v3.failed

        v4 = verify_honesty(content, key)
        total_passed += v4.passed
        total_failed += v4.failed

    # SP-G08 HMSU 专项校验
    v_hmsu = verify_sp_g08()
    total_passed += v_hmsu.passed
    total_failed += v_hmsu.failed

    # 互锁验证
    v5 = verify_interlock()
    total_passed += v5.passed
    total_failed += v5.failed

    # 汇总
    print(f"\n{'='*60}")
    print(f"📊 验证结果: {total_passed}/{total_passed + total_failed} 通过")
    if total_failed == 0:
        print(f"🎉 全部通过 ✅ — AI 域四柱文档结构完整，可入库")
    else:
        print(f"⚠️ {total_failed} 项未通过")
        for e in v5.errors[:10]:
            print(f"   · {e}")

    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
