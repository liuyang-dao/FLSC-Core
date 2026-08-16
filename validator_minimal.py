#!/usr/bin/env python3
"""
validator_minimal.py — FLSC 机器可解析化编码校验器 V1.0

实现 FLSC-CODE-REQ-V1.0 四大硬性标准：
  Hard-1: 五层结构刚性隔离
  Hard-2: 全部概念编码唯一映射
  Hard-3: 逻辑与量化可独立执行
  Hard-4: 拓扑结构序列化存储

用法:
  python3 validator_minimal.py <file.yaml>           # 校验单个文件
  python3 validator_minimal.py <dir>               # 校验目录下所有 .yaml/.yml/.md
  python3 validator_minimal.py --self-test         # 自检

退出码: 0=全部通过, 1=存在失败
"""
import sys, os, re, json, ast, glob
from datetime import datetime

# ─────────────────────────────────────────────
# 常量（与 spine_yaml_schema.json / CODE-BASELINE V1.0 同步）
# ─────────────────────────────────────────────
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "spine_yaml_schema.json")

REQUIRED_DOC_FIELDS = [
    "doc_id", "lineage_id", "oracle_level", "oracle_chain",
    "oat_type", "hydrogen_bond", "status", "effective_date", "spine_namespace",
]

ORACLE_LEVELS = ["ORC1", "ORC2", "ORC3", "ORC4", "ORC5"]
OAT_TYPES     = ["OAT-N", "OAT-S", "OAT-C"]
HB_LEVELS     = ["frozen", "experimental", "production", "prototyping", "prototyping-fixed"]
DOC_STATUS    = ["draft", "review", "active", "deprecated"]
FIXED_PTYPES = ["None", "DoubleStrong", "Triple", "QuadCoupled"]
STEADY_LEVELS= ["L4", "L3", "L2", "L1"]
DEFECT_TYPES  = ["A", "B", "C", "D", "E", "CF"]
SPINE_IDS     = ["MD01", "MD02", "MD03", "MD04", "MD05", "MD06"]
EDGE_TYPES    = ["causal", "intervention", "counterfactual", "confounder", "mediator"]
ATOM_TYPES    = ["C-Atom", "I-Atom", "K-Atom", "T-Atom", "E-Atom", "M-Atom", "S-Atom"]
METRIC_NAMES  = ["CI_struct", "CI_true", "CD_true", "RIS_true", "S_order", "V_diss", "MIS_true"]
RANK_TYPES    = ["absolute", "strong", "domain"]
ACTION_TYPES  = ["alert", "degrade", "block", "terminate"]
EVIDENCE_LVLS = ["E-I", "E-II", "E-III", "E-IV"]

# 命名空间前缀 → 所属域（用于冲突检测）
NS_PREFIXES = {
    "CB-":  "Code Baseline",
    "SR-":  "结构资产卡",
    "GRIF-": "GRIFF 真洽推理",
    "HCOG-": "高阶认知 Agent",
    "PF-":  "Prompt Factory",
    "EB-":  "具身统一大脑",
    "G-":   "原生 AI 核心柱",
    "HB-":  "人脑七脊",
    "SP-G": "碳硅合体",
    "COG-G":"认知大统一",
    "MDL-": "脊线评价",
    "H-":   "原生 AI 硬氢键",
    "H-E":  "具身硬氢键",
    "K-":   "推理公理",
    "F-":   "诚实声明",
    "O-":   "不可显形边界",
    "MD0":  "负熵脊（耗散元理论）",
}

# 自然语言禁用词（命中即触发警告）
FORBIDDEN_NATURAL_WORDS = [
    "较高", "偏低", "一般", "严重", "轻微", "较大", "较小",
    "尽量", "尽可能", "大概", "差不多", "也许", "可能吧",
    "较好", "较差", "很强", "很弱",
]

# ─────────────────────────────────────────────
# 结果收集
# ─────────────────────────────────────────────
results = []  # [(file, check_name, status, detail)]

def record(file, name, status, detail=""):
    results.append((file, name, status, detail))

def load_yaml(text):
    """极简 YAML 解析：支持本规范用到的子集（无 PyYAML 依赖）。"""
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        # 无 yaml 库时退回 json 模式（文件需为 json 格式）
        return json.loads(text)

def extract_yaml_blocks(text):
    """从 .md 文档中抽取所有 ```yaml ... ``` 代码块。"""
    blocks = re.findall(r"```ya?ml\n(.*?)\n```", text, re.DOTALL)
    return blocks

# ─────────────────────────────────────────────
# 校验函数
# ─────────────────────────────────────────────
def check_doc_level_fields(data, file):
    """Hard-2: 文档级必填字段 + 枚举值"""
    for f in REQUIRED_DOC_FIELDS:
        if f not in data:
            record(file, f"doc_field:{f}", "FAIL", "缺失必填字段")
        else:
            record(file, f"doc_field:{f}", "PASS", "")

    # 枚举校验
    checks = [
        ("oracle_level", ORACLE_LEVELS),
        ("oat_type", OAT_TYPES),
        ("hydrogen_bond", HB_LEVELS),
        ("status", DOC_STATUS),
    ]
    for fname, allowed in checks:
        if fname in data and data[fname] not in allowed:
            record(file, f"enum:{fname}", "FAIL",
                    f"值={data[fname]!r}，允许={allowed}")
        elif fname in data:
            record(file, f"enum:{fname}", "PASS", "")

    # lineage_id 长度
    if "lineage_id" in data:
        lid = str(data["lineage_id"])
        if len(lid) < 8:
            record(file, "lineage_id_length", "FAIL", f"长度={len(lid)}<8")
        else:
            record(file, "lineage_id_length", "PASS", "")

    # effective_date ISO 格式
    if "effective_date" in data:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(data["effective_date"])):
            record(file, "effective_date_format", "FAIL",
                    f"应为 YYYY-MM-DD，实际={data['effective_date']}")
        else:
            record(file, "effective_date_format", "PASS", "")

    # spine_namespace 格式（XX-）
    if "spine_namespace" in data:
        ns = str(data["spine_namespace"])
        if not re.match(r"^[A-Z]{2,5}-$", ns):
            record(file, "spine_namespace_format", "FAIL",
                    f"应为大写前缀+连字符，如 'SR-'，实际={ns}")
        else:
            record(file, "spine_namespace_format", "PASS", "")

def check_five_layers(data, file):
    """Hard-1: 五层刚性隔离"""
    layers = ["unit_layer", "connect_layer", "weight_layer",
              "constraint_layer", "steady_layer"]
    present = [l for l in layers if l in data]
    if len(present) == 0:
        record(file, "five_layers:presence", "FAIL",
                "未找到任何五层字段（unit/connect/weight/constraint/steady）")
        return
    if len(present) < 5:
        record(file, "five_layers:completeness", "WARN",
                f"仅包含 {len(present)}/5 层: {present}")
    else:
        record(file, "five_layers:completeness", "PASS", "五层齐全")

    # 检查交叉混杂：connect 层不应含 weight 数值
    if "connect_layer" in data:
        cl = json.dumps(data["connect_layer"])
        for bad in ["weight_value", "metric_name"]:
            if bad in cl:
                record(file, "layer_isolation:connect", "FAIL",
                        f"connect_layer 不应包含 {bad}")
    if "unit_layer" in data:
        for atom in data["unit_layer"].get("atoms", []):
            for fld in ["logic_expr", "formula", "metric_name"]:
                if fld in atom:
                    record(file, "layer_isolation:unit", "FAIL",
                            f"unit atom 不应包含 {fld}")

    record(file, "layer_isolation", "PASS", "")

def check_unit_layer(data, file):
    """Unit 层校验"""
    ul = data.get("unit_layer", {})
    atoms = ul.get("atoms", [])
    if not atoms:
        record(file, "unit:atoms_present", "WARN", "unit_layer 无 atoms")
        return
    seen_ids = set()
    for a in atoms:
        aid = a.get("atom_id", "")
        # ID 唯一
        if aid in seen_ids:
            record(file, f"unit:atom_id_unique:{aid}", "FAIL", "重复 atom_id")
        seen_ids.add(aid)
        # unit_type 枚举
        ut = a.get("unit_type", "")
        if ut not in ATOM_TYPES:
            record(file, f"unit:atom_type:{aid}", "FAIL",
                    f"unit_type={ut}，允许={ATOM_TYPES}")
        else:
            record(file, f"unit:atom_type:{aid}", "PASS", "")
        # anchor_status 布尔
        if "anchor_status" in a and not isinstance(a["anchor_status"], bool):
            record(file, f"unit:anchor_bool:{aid}", "FAIL", "anchor_status 应为 bool")
        # defect_severity 0~1
        if "defect_severity" in a:
            ds = a["defect_severity"]
            if not isinstance(ds, (int, float)) or not (0 <= ds <= 1):
                record(file, f"unit:defect_range:{aid}", "FAIL",
                        f"defect_severity={ds}，应为 [0,1]")
        # oat_tag 枚举
        if "oat_tag" in a and a["oat_tag"] not in OAT_TYPES:
            record(file, f"unit:oat_tag:{aid}", "FAIL",
                    f"oat_tag={a['oat_tag']}")

def check_connect_layer(data, file):
    """Connect 层校验"""
    cl = data.get("connect_layer", {})
    edges = cl.get("edges", [])
    if not edges:
        record(file, "connect:edges_present", "WARN", "connect_layer 无 edges")
        return
    seen_eids = set()
    node_ids = set()
    # 收集 unit atom_ids 用于引用校验
    ul = data.get("unit_layer", {})
    valid_nodes = {a.get("atom_id") for a in ul.get("atoms", [])}
    for e in edges:
        eid = e.get("edge_id", "")
        if eid in seen_eids:
            record(file, f"connect:edge_unique:{eid}", "FAIL", "重复 edge_id")
        seen_eids.add(eid)
        # edge_type 枚举
        et = e.get("edge_type", "")
        if et not in EDGE_TYPES:
            record(file, f"connect:edge_type:{eid}", "FAIL",
                    f"edge_type={et}")
        else:
            record(file, f"connect:edge_type:{eid}", "PASS", "")
        # source/target 引用有效性
        src, tgt = e.get("source_unit_id"), e.get("target_unit_id")
        for nid, label in [(src, "source"), (tgt, "target")]:
            if nid and valid_nodes and nid not in valid_nodes:
                record(file, f"connect:ref:{eid}:{label}", "FAIL",
                        f"{label}_unit_id={nid} 未在任何 unit atom 中定义")
        # is_cyclic 布尔
        if "is_cyclic" in e and not isinstance(e["is_cyclic"], bool):
            record(file, f"connect:is_cyclic:{eid}", "FAIL", "应为 bool")
        # spine_id 格式
        if "spine_id" in e:
            sp = str(e["spine_id"])
            if not re.match(r"^[A-Z]{2,5}-[A-Z0-9]+$", sp):
                record(file, f"connect:spine_id:{eid}", "FAIL",
                        f"spine_id 格式应为 XX-NNN，实际={sp}")

def check_weight_layer(data, file):
    """Weight 层校验"""
    wl = data.get("weight_layer", {})
    metrics = wl.get("metrics", [])
    if not metrics:
        record(file, "weight:metrics_present", "WARN", "weight_layer 无 metrics")
        return
    for m in metrics:
        mn = m.get("metric_name", "")
        if mn not in METRIC_NAMES:
            record(file, f"weight:metric:{mn}", "FAIL",
                    f"metric_name={mn}，允许={METRIC_NAMES}")
        else:
            record(file, f"weight:metric:{mn}", "PASS", "")
        # weight_value 应为数字
        if "weight_value" in m and not isinstance(m["weight_value"], (int, float)):
            record(file, f"weight:value_type:{mn}", "FAIL", "weight_value 应为数字")
        # formula 应为非空字符串
        if "formula" in m:
            f = m["formula"]
            if not isinstance(f, str) or len(f) < 3:
                record(file, f"weight:formula:{mn}", "FAIL",
                        "formula 应为可执行表达式字符串")
            else:
                # 尝试 AST 解析（不执行，仅检查语法）
                try:
                    ast.parse(f, mode="eval")
                    record(file, f"weight:formula_ast:{mn}", "PASS", "")
                except SyntaxError:
                    record(file, f"weight:formula_ast:{mn}", "WARN",
                            "formula 非标准 Python 表达式（可能为领域 DSL）")

def check_constraint_layer(data, file):
    """Constraint 层校验"""
    cl = data.get("constraint_layer", {})
    cs = cl.get("constraints", [])
    if not cs:
        record(file, "constraint:present", "WARN", "constraint_layer 无 constraints")
        return
    for c in cs:
        cid = c.get("constraint_id", "")
        # rank 枚举
        rk = c.get("rank", "")
        if rk not in RANK_TYPES:
            record(file, f"constraint:rank:{cid}", "FAIL",
                    f"rank={rk}，允许={RANK_TYPES}")
        # block_action 枚举
        ba = c.get("block_action", "")
        if ba not in ACTION_TYPES:
            record(file, f"constraint:action:{cid}", "FAIL",
                    f"block_action={ba}")
        # evidence_level 枚举
        ev = c.get("evidence_level", "")
        if ev not in EVIDENCE_LVLS:
            record(file, f"constraint:evidence:{cid}", "FAIL",
                    f"evidence_level={ev}")
        # logic_expr 非空
        le = c.get("logic_expr", "")
        if not isinstance(le, str) or len(le) < 3:
            record(file, f"constraint:logic_expr:{cid}", "FAIL",
                    "logic_expr 过短或缺失")
        else:
            # 尝试 AST 解析
            try:
                ast.parse(le, mode="eval")
                record(file, f"constraint:logic_ast:{cid}", "PASS", "")
            except SyntaxError:
                record(file, f"constraint:logic_ast:{cid}", "WARN",
                        "logic_expr 非标准表达式")

def check_steady_layer(data, file):
    """Steady 层校验"""
    sl = data.get("steady_layer", {})
    if not sl:
        record(file, "steady:present", "WARN", "steady_layer 缺失")
        return
    # fixed_point_type
    fpt = sl.get("fixed_point_type", "")
    if fpt not in FIXED_PTYPES:
        record(file, "steady:fixed_point", "FAIL",
                f"fixed_point_type={fpt}")
    else:
        record(file, "steady:fixed_point", "PASS", "")
    # theta_critical 0~1
    tc = sl.get("theta_critical")
    if tc is not None and (not isinstance(tc, (int, float)) or not (0 <= tc <= 1)):
        record(file, "steady:theta_range", "FAIL", f"theta_critical={tc}")
    # residual >= 0
    rs = sl.get("residual")
    if rs is not None and (not isinstance(rs, (int, float)) or rs < 0):
        record(file, "steady:residual", "FAIL", f"residual={rs}")
    # steady_level
    slvl = sl.get("steady_level", "")
    if slvl not in STEADY_LEVELS:
        record(file, "steady:level", "FAIL", f"steady_level={slvl}")
    else:
        record(file, "steady:level", "PASS", "")

def check_forbidden_natural_language(data, file, raw_text):
    """CODE-REQ 禁止场景：自然语言模糊词检测"""
    hits = []
    for w in FORBIDDEN_NATURAL_WORDS:
        if w in raw_text:
            hits.append(w)
    if hits:
        record(file, "forbidden_nl_words", "WARN",
                f"检测到自然语言模糊词: {hits[:5]}")
    else:
        record(file, "forbidden_nl_words", "PASS", "")

def check_namespace_conflict(all_files_data):
    """跨文件命名空间冲突检测"""
    ns_map = {}  # prefix -> file
    for file, data in all_files_data:
        ns = data.get("spine_namespace", "")
        if ns in ns_map:
            record(file, f"ns_conflict:{ns}", "FAIL",
                    f"命名空间 {ns} 已被 {ns_map[ns]} 使用")
        else:
            ns_map[ns] = file
            record(file, f"ns_unique:{ns}", "PASS", "")

def check_cyclical_edges(data, file):
    """Hard-4: 拓扑环路检测（简易版）"""
    cl = data.get("connect_layer", {})
    edges = cl.get("edges", [])
    graph = {}
    for e in edges:
        src = e.get("source_unit_id")
        tgt = e.get("target_unit_id")
        if src and tgt:
            graph.setdefault(src, []).append(tgt)
    # DFS 环路检测
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    cycles = []
    def dfs(node, path):
        color[node] = GRAY
        for nb in graph.get(node, []):
            if color.get(nb) == GRAY:
                cycles.append(path + [nb])
            elif color.get(nb) == WHITE:
                dfs(nb, path + [nb])
        color[node] = BLACK
    for n in list(color.keys()):
        if color[n] == WHITE:
            dfs(n, [n])
    if cycles:
        record(file, "topo:cycle_detect", "FAIL",
                f"检测到 {len(cycles)} 个环路: {cycles[:2]}")
    else:
        record(file, "topo:cycle_detect", "PASS", "")

# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────
def validate_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception as e:
        record(path, "file_read", "FAIL", str(e))
        return

    # 尝试解析 YAML（支持 .yaml/.yml 直接解析，.md 提取代码块）
    data = None
    if path.endswith((".yaml", ".yml")):
        try:
            data = load_yaml(raw)
        except Exception as e:
            record(path, "yaml_parse", "FAIL", str(e))
            return
    elif path.endswith(".md"):
        blocks = extract_yaml_blocks(raw)
        if not blocks:
            record(path, "yaml_block_in_md", "WARN",
                    "Markdown 中未找到 ```yaml 代码块")
            return
        # 使用第一个 yaml 块
        try:
            data = load_yaml(blocks[0])
        except Exception as e:
            record(path, "yaml_parse_in_md", "FAIL", str(e))
            return
    elif path.endswith(".json"):
        try:
            data = json.loads(raw)
        except Exception as e:
            record(path, "json_parse", "FAIL", str(e))
            return
    else:
        record(path, "unsupported_format", "WARN",
                f"不支持的格式: {path}")
        return

    if not isinstance(data, dict):
        record(path, "data_type", "FAIL", "根节点应为 mapping/dict")
        return

    # 执行全部校验
    check_doc_level_fields(data, path)
    check_five_layers(data, path)
    check_unit_layer(data, path)
    check_connect_layer(data, path)
    check_weight_layer(data, path)
    check_constraint_layer(data, path)
    check_steady_layer(data, path)
    check_forbidden_natural_language(data, path, raw)
    check_cyclical_edges(data, path)

def validate_directory(dirpath):
    files = []
    for ext in ("*.yaml", "*.yml", "*.md", "*.json"):
        files.extend(glob.glob(os.path.join(dirpath, "**", ext), recursive=True))
    all_data = []
    for fp in sorted(set(files)):
        validate_file(fp)
        # 收集数据用于跨文件检测
        try:
            with open(fp, "r", encoding="utf-8") as f:
                raw = f.read()
            if fp.endswith((".yaml", ".yml")):
                d = load_yaml(raw)
            elif fp.endswith(".json"):
                d = json.loads(raw)
            else:
                blocks = extract_yaml_blocks(raw)
                d = load_yaml(blocks[0]) if blocks else None
            if isinstance(d, dict):
                all_data.append((fp, d))
        except:
            pass
    check_namespace_conflict(all_data)

def print_report():
    total = len(results)
    passed = sum(1 for r in results if r[2] == "PASS")
    warned = sum(1 for r in results if r[2] == "WARN")
    failed = sum(1 for r in results if r[2] == "FAIL")
    print(f"\n{'='*60}")
    print(f"  FLSC Code Baseline Validator V1.0")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  总校验项: {total}")
    print(f"  ✅ PASS: {passed}")
    print(f"  ⚠️  WARN: {warned}")
    print(f"  ❌ FAIL: {failed}")
    print(f"{'='*60}")
    if failed:
        print("\n--- FAIL 详情 ---")
        for f, n, s, d in results:
            if s == "FAIL":
                print(f"  ❌ [{os.path.basename(f)}] {n}: {d}")
    if warned:
        print("\n--- WARN 详情 ---")
        for f, n, s, d in results:
            if s == "WARN":
                print(f"  ⚠️  [{os.path.basename(f)}] {n}: {d}")
    print(f"\n{'='*60}")
    if failed == 0:
        print(f"  🎉 全部通过 ✅ ({passed}/{total})")
        if warned:
            print(f"  （含 {warned} 条警告，建议修复但不阻断）")
    else:
        print(f"  ❌ 存在 {failed} 项失败，阻断入库")
    print(f"{'='*60}\n")
    return failed == 0

# ─────────────────────────────────────────────
# 自检模式
# ─────────────────────────────────────────────
def self_test():
    """生成合规 + 违规样本，验证校验器自身正确性。"""
    import tempfile
    tmp = tempfile.mkdtemp()
    # 合规样本
    good = """doc_id: "TEST-GOOD-V1.0"
lineage_id: "sha256:abc1234567890"
oracle_level: "ORC2"
oracle_chain: ["ORC3-STABLE-TENSION-V3.0"]
oat_type: "OAT-S"
hydrogen_bond: "experimental"
status: "active"
effective_date: "2026-08-16"
spine_namespace: "TG-"
unit_layer:
  atoms:
    - atom_id: "TG-U01"
      unit_type: "C-Atom"
      anchor_status: true
      defect_severity: 0.0
      oat_tag: "OAT-S"
    - atom_id: "TG-U02"
      unit_type: "K-Atom"
      anchor_status: true
      defect_severity: 0.0
      oat_tag: "OAT-S"
connect_layer:
  edges:
    - edge_id: "TG-E01"
      source_unit_id: "TG-U01"
      target_unit_id: "TG-U02"
      edge_type: "causal"
      is_cyclic: false
      spine_id: "GRIF-C01"
weight_layer:
  metrics:
    - metric_name: "CI_struct"
      weight_value: 0.30
      formula: "w1*topo + w2*prop + w3*const + w4*anchor"
constraint_layer:
  constraints:
    - constraint_id: "TG-C01"
      logic_expr: "CI_struct >= 0.80"
      rank: "absolute"
      block_action: "block"
      evidence_level: "E-I"
steady_layer:
  fixed_point_type: "None"
  theta_critical: 0.85
  residual: 0.02
  steady_level: "L3"
"""
    # 违规样本
    bad = """doc_id: "TEST-BAD"
lineage_id: "short"
oracle_level: "ORC9"
oat_type: "OAT-X"
hydrogen_bond: "magic"
status: "unknown"
effective_date: "2026/08/16"
spine_namespace: "bad"
unit_layer:
  atoms:
    - atom_id: "DUPE"
      unit_type: "Z-Atom"
      anchor_status: "yes"
      defect_severity: 5.0
connect_layer:
  edges:
    - edge_id: "TG-E01"
      source_unit_id: "MISSING"
      edge_type: "weird"
      is_cyclic: "maybe"
      spine_id: "bad-id"
constraint_layer:
  constraints:
    - constraint_id: "B1"
      logic_expr: "x"
      rank: "super"
      block_action: "explode"
      evidence_level: "E-V"
steady_layer:
  fixed_point_type: "Weird"
  theta_critical: 5.0
  residual: -1.0
  steady_level: "L9"
"""
    good_path = os.path.join(tmp, "good.yaml")
    bad_path = os.path.join(tmp, "bad.yaml")
    with open(good_path, "w") as f: f.write(good)
    with open(bad_path, "w") as f: f.write(bad)
    validate_file(good_path)
    validate_file(bad_path)
    ok = print_report()
    return ok

# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    if "--self-test" in args:
        sys.exit(0 if self_test() else 1)
    if not args:
        print("用法: python3 validator_minimal.py <file.yaml|dir> [--self-test]")
        sys.exit(1)
    target = args[0]
    if os.path.isdir(target):
        validate_directory(target)
    elif os.path.isfile(target):
        validate_file(target)
    else:
        print(f"路径不存在: {target}")
        sys.exit(1)
    ok = print_report()
    sys.exit(0 if ok else 1)
