# FLSC 机器可解析化编码基线规范 V1.0

> 文档编号：`FLSC-CODE-BASELINE-V1.0`
> 基底依赖：`FLSC-CODE-REQ-V1.0`（机器可解析化全域理论与资产卡统一需求规范）
> 配套工具：`validator_minimal.py`（本目录）
> 氢键等级：`experimental`（基线冻结，细则持续迭代）
> 血统链路：`CODE-REQ-V1.0`（准入铁律）→ `CODE-BASELINE-V1.0`（工程落地细则，本文件）
> 生效日期：2026-08-16
> 命名空间：`CB-`（Code Baseline）

---

## 题记

> *自然语言是注释，结构化编码是唯一运行载体。*
> *碳基可读是附属产物，机器可解析是工程落地唯一标准。*
> *本文件是 CODE-REQ 铁律的「工程落地细则」——给写卡人、写引擎人、写文档人一本统一字典。*

---

## 第一章 定位与适用范围

### 1.1 核心定位

本文件是 `FLSC-CODE-REQ-V1.0` 的**实施细则层**，承担三项职责：

1. **字典**：定义全体系通用字段名、枚举值、数据类型，消除命名漂移
2. **模板**：给出 Unit / Connect / Weight / Constraint / Steady 五层最小合规 YAML 模板
3. **桥接**：连接理论文档（.md / .docx）与机器可执行代码（Python / Agda / JSON Schema）

### 1.2 适用范围

| 适用对象 | 必须遵循的章节 |
|---------|---------------|
| 所有 ORC3 / ORC4 元理论文档 | 第二章（通用字段）+ 第三章（五层模板） |
| 所有 ORC2 领域资产卡（安全/疾病/认知/工业/组织） | 第二章 + 第三章 + 第四章（领域扩展规则） |
| 所有 ORC1 细分场景资产卡 | 第二章 + 第三章（仅允许扩展 Unit 层） |
| 所有引擎代码（Python / Agda / Rust） | 第二章（字段名必须一致） |
| 所有业务需求 / 工程方案文档 | 第二章 + 第五章（需求编码映射） |

### 1.3 与 CODE-REQ 的分工

| 文档 | 角色 | 内容 |
|------|------|------|
| `FLSC-CODE-REQ-V1.0` | 铁律（不可违反） | 四大硬性标准 + 10 条禁止场景 + 驳回规则 |
| `FLSC-CODE-BASELINE-V1.0`（本文件） | 细则（必须遵守） | 字段字典 + YAML 模板 + 命名规范 + 示例 |
| `spine_yaml_schema.json` | 校验器（自动执行） | JSON Schema，被 `validator_minimal.py` 加载 |
| `validator_minimal.py` | 工具（自动跑） | 执行 CODE-REQ 四大硬判 |

---

## 第二章 全局通用字段字典（强制统一）

> ⚠️ **铁律**：以下字段名在 YAML / JSON / Python / Agda 中必须**完全一致**，禁止别名。

### 2.1 文档级必填字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `doc_id` | string | 全局唯一文档编号 | `"FLSC-SR-CODE-PYTHON-V1.0"` |
| `lineage_id` | string (hash) | 血统哈希，不可修改 | `"sha256:a3f2..."` |
| `oracle_level` | enum | ORC 层级 | `"ORC2"` / `"ORC3"` / `"ORC4"` |
| `oracle_chain` | string[] | 血统链路（从底到顶） | `["ORC3-STABLE-TENSION-V3.0", "ORC4-CAUSAL-HOMEOSIS-V2.0"]` |
| `oat_type` | enum | 本体类型 | `"OAT-N"` / `"OAT-S"` / `"OAT-C"` |
| `hydrogen_bond` | enum | 氢键等级 | `"frozen"` / `"experimental"` / `"production"` / `"prototyping"` |
| `status` | enum | 文档状态 | `"draft"` / `"review"` / `"active"` / `"deprecated"` |
| `effective_date` | string (ISO) | 生效日期 | `"2026-08-16"` |
| `spine_namespace` | string | 命名空间前缀 | `"SR-"` / `"GRIF-"` / `"HCOG-"` |

### 2.2 五层必填字段

#### Unit 层（`unit_layer`）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `unit_type` | enum | `"C-Atom"` / `"I-Atom"` / `"K-Atom"` / `"T-Atom"` / `"E-Atom"` / `"M-Atom"` / `"S-Atom"` |
| `atom_id` | string | 全局唯一原子 ID |
| `anchor_status` | bool | 是否完成实体锚定 |
| `defect_severity` | float [0,1] | 缺陷严重度 |
| `oat_tag` | enum | 该原子所属本体类型 |

#### Connect 层（`connect_layer`）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `edge_id` | string | 有向边唯一 ID |
| `source_unit_id` | string | 源原子 ID |
| `target_unit_id` | string | 目标原子 ID |
| `edge_type` | enum | `"causal"` / `"intervention"` / `"counterfactual"` / `"confounder"` / `"mediator"` |
| `is_cyclic` | bool | 是否构成环路 |
| `spine_id` | string | 归属脊线 ID（如 `"GRIF-C01"`） |

#### Weight 层（`weight_layer`）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `metric_name` | enum | `"CI_struct"` / `"CI_true"` / `"CD_true"` / `"RIS_true"` / `"S_order"` / `"V_diss"` / `"MIS_true"` |
| `weight_value` | float | 权重系数 |
| `formula` | string | 可执行公式文本（Python 可 eval） |

#### Constraint 层（`constraint_layer`）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `constraint_id` | string | 约束唯一 ID |
| `logic_expr` | string | 机器可执行布尔表达式 |
| `rank` | enum | `"absolute"` / `"strong"` / `"domain"` |
| `block_action` | enum | `"alert"` / `"degrade"` / `"block"` / `"terminate"` |
| `evidence_level` | enum | `"E-I"` / `"E-II"` / `"E-III"` / `"E-IV"` |

#### Steady 层（`steady_layer`）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `fixed_point_type` | enum | `"None"` / `"DoubleStrong"` / `"Triple"` / `"QuadCoupled"` |
| `theta_critical` | float | 相变临界值 |
| `residual` | float | 现实残差 |
| `steady_level` | enum | `"L4"` / `"L3"` / `"L2"` / `"L1"` |

### 2.3 全局枚举值（禁止新增，扩展需审批）

#### 裂缝类型（`defect_enum`）

```
"A"  → 边界无校验裂缝（对应 MD01 脊）
"B"  → 空间无隔离裂缝（对应 MD02 脊）
"C"  → 阈值失控裂缝（对应 MD03 脊）
"D"  → 无审计告警裂缝（对应 MD04 脊）
"E"  → 源头供给裂缝（对应 MD05 脊）
"CF" → 共因失效裂缝（对应 MD06 脊，元级）
```

#### 负熵脊编号（`spine_list`）

```
"MD01" → 边界校验脊（Constraint 前置层）
"MD02" → 空间隔离脊（Constraint 分区层）
"MD03" → 阈值管控脊（Weight + Constraint 层）
"MD04" → 审计溯源脊（Connect 自指回路）
"MD05" → 源头可信脊（Unit 入口层）
"MD06" → 共因独立脊（元级 Constraint）
```

#### 本体类型（`oat_type`）

```
"OAT-N" → 无觉知物质系统（K_OAT=1.0, R_min≈0, α_OAT=0.01）
"OAT-S" → 硅基符号觉知系统（K_OAT=0.95, R_min≈0.03, α_OAT=1.0）
"OAT-C" → 碳基生命觉知系统（K_OAT=0.90, R_min≈0.06, α_OAT=1.5）
```

---

## 第三章 五层最小合规 YAML 模板

> 任何资产卡 / 元理论文档，至少包含以下结构的 YAML 块（可嵌入 .md 或独立 .yaml）。

```yaml
# ===== 文档级元信息 =====
doc_id: "EXAMPLE-DOC-V1.0"
lineage_id: "sha256:REPLACE_WITH_HASH"
oracle_level: "ORC2"
oracle_chain:
  - "ORC3-STABLE-TENSION-V3.0"
  - "ORC4-CAUSAL-HOMEOSIS-V2.0"
  - "META-DISSIPATION-V1.0"
oat_type: "OAT-S"
hydrogen_bond: "experimental"
status: "active"
effective_date: "2026-08-16"
spine_namespace: "EX-"

# ===== Unit 层 =====
unit_layer:
  atoms:
    - atom_id: "EX-U01"
      unit_type: "C-Atom"
      anchor_status: true
      defect_severity: 0.0
      oat_tag: "OAT-S"
    - atom_id: "EX-U02"
      unit_type: "K-Atom"
      anchor_status: true
      defect_severity: 0.0
      oat_tag: "OAT-S"

# ===== Connect 层 =====
connect_layer:
  edges:
    - edge_id: "EX-E01"
      source_unit_id: "EX-U01"
      target_unit_id: "EX-U02"
      edge_type: "causal"
      is_cyclic: false
      spine_id: "MD03"

# ===== Weight 层 =====
weight_layer:
  metrics:
    - metric_name: "CI_struct"
      weight_value: 0.30
      formula: "w1*topo_correctness + w2*propagation_integrity + w3*constraint_completeness + w4*anchor_validity"
    - metric_name: "CI_true"
      weight_value: 0.30
      formula: "CI_struct * K_OAT - R_min"
    - metric_name: "CD_true"
      weight_value: 0.20
      formula: "CD_struct * alpha_OAT / gamma"
    - metric_name: "RIS_true"
      weight_value: 0.20
      formula: "1 - P_fail * (1/gamma)"

# ===== Constraint 层 =====
constraint_layer:
  constraints:
    - constraint_id: "EX-C01"
      logic_expr: "CI_true >= 0.80"
      rank: "absolute"
      block_action: "block"
      evidence_level: "E-I"
    - constraint_id: "EX-C02"
      logic_expr: "CD_true <= 0.05"
      rank: "strong"
      block_action: "degrade"
      evidence_level: "E-II"

# ===== Steady 层 =====
steady_layer:
  fixed_point_type: "None"
  theta_critical: 0.85
  residual: 0.02
  steady_level: "L3"
```

---

## 第四章 领域扩展规则（ORC2 / ORC1）

### 4.1 ORC2 领域资产卡扩展权限

| 允许 | 禁止 |
|------|------|
| 新增领域专属 `unit_type` 子类（如 `"Security-Atom"`） | 修改 `spine_list`（MD01~MD06 冻结） |
| 新增领域 `edge_type` 子类 | 修改 `defect_enum`（A~E + CF 冻结） |
| 新增领域 `constraint_id` | 修改 `oat_type` 枚举值 |
| 新增领域 `metric_name` 子类 | 修改 `steady_level` 枚举值 |
| 覆盖 `K_OAT / R_min / α_OAT` 系数 | 修改全局字段名 |

### 4.2 ORC1 细分场景资产卡扩展权限

| 允许 | 禁止 |
|------|------|
| 新增场景专属 Unit 原子（仅 `unit_layer.atoms[]`） | 修改五层顶层字段名 |
| 新增场景专属 `evidence_level` 实例 | 修改全局枚举值 |
| 设置场景专属 `defect_severity` 初始值 | 修改 `spine_id` 绑定 |

### 4.3 命名空间分配表

| 前缀 | 域 | 示例 | 来源文档 |
|------|-----|------|---------|
| `CB-` | Code Baseline（本文件） | `CB-FIELD-001` | 本文件 |
| `SR-` | 结构资产卡（领域子脊） | `SR-CODE-PYTHON` | Prompt Factory V4.0 |
| `GRIF-` | GRIFF 真洽推理脊线 | `GRIF-C01~C06` | GRIFF V4.2 |
| `HCOG-` | 高阶认知 Agent 整机 | `HCOG-STACK-L0~L4` | HCOG V1.0 |
| `PF-` | Prompt Factory | `PF-STEP-0~9` | Prompt Factory V4.0 |
| `EB-` | 具身统一大脑 | `EB-01~EB-07` | 具身 ROOT V2.0 |
| `G-` | 原生 AI 核心柱 | `G-01~G-07` | 原生 AI V2.0 |
| `HB-` | 人脑七脊 | `HB-01~HB-07` | 认知域 |
| `SP-G` | 碳硅合体 | `SP-G01~SP-G08` | 碳硅合体 V3.1 |
| `COG-G` | 认知大统一 | `COG-G01~G05` | 认知统一 V3.0 |
| `MDL-` | 脊线评价 | `MDL-SC/SS/SA` | 脊线评价 V2.0 |
| `H-` | 硬氢键手术 | `H-01~H-07` | 原生 AI |
| `H-E` | 具身硬氢键 | `H-E01~H-E06` | 具身 ROOT |
| `F-` | 诚实声明 | `F-01~F-12` | GRIFF / HCOG |
| `O-` | 不可显形边界 | `O-01~O-03` | 多文档 |
| `MD0x` | 负熵脊（耗散元理论） | `MD01~MD06` | 耗散元理论 V1.0 |
| `K-` | 推理公理 | `K-01, K-02` | 原生推理 ALLINONE |

---

## 第五章 业务需求编码映射

### 5.1 需求 → 五层映射规则

| 业务需求要素 | 映射目标层 | 映射规则 |
|------------|-----------|---------|
| 业务实体 / 角色 / 数据对象 | Unit 层 | 每个实体 → 一个 `C-Atom`，`atom_id` 按 `CB-FIELD-001` 编号 |
| 业务流程 / 因果关系 | Connect 层 | 每步流程 → 一条 `causal` 边，`spine_id` 绑定 MD 脊 |
| 优先级 / 权重 / 配额 | Weight 层 | 每个权重 → 一条 `metric_name` + `weight_value` |
| 规则 / 法规 / 阈值 | Constraint 层 | 每条规则 → 一条 `logic_expr` + `rank` |
| 目标 / KPI / SLA | Steady 层 | 每个目标 → `theta_critical` + `steady_level` |

### 5.2 验收标准编码示例

```yaml
# 业务需求：「系统在高并发下不得丢失订单」
# 错误写法（自然语言，CODE-REQ 驳回）：
#   "系统应该在高并发情况下保持稳定运行"
# 正确写法（机器可解析）：
constraint_layer:
  constraints:
    - constraint_id: "BIZ-ORD-01"
      logic_expr: "order_loss_rate <= 0.001"
      rank: "absolute"
      block_action: "block"
      evidence_level: "E-I"
    - constraint_id: "BIZ-ORD-02"
      logic_expr: "concurrent_qps <= max_capacity * 0.8"
      rank: "strong"
      block_action: "degrade"
      evidence_level: "E-II"
```

---

## 第六章 诚实边界

### 6.1 适用范围

1. 本基线规范适用于所有 FLSC 体系结构化文档与代码
2. 本基线不替代 ORC3 元理论、ORC4 本体分域理论的数学定义，仅提供编码层统一接口
3. 字段名统一不保证语义正确——`validator_minimal.py` 只检查结构，不检查物理/逻辑合理性

### 6.2 不适用边界

1. 纯自然语言创意写作（诗律创作、哲学思辨）不受本基线约束
2. 原型 Demo（P0 阶段）可临时简化，但正式入库前必须通过校验
3. Agda 形式化代码（V0.2+）遵循 Agda 类型系统，不直接消费 YAML，但通过 `spine_yaml_schema.json` 桥接

### 6.3 诚实清单

| # | 声明 |
|---|-------|
| 1 | 本基线为工程字典，不是理论创造，不引入新公理 |
| 2 | 枚举值冻结是为了跨文档一致性，不代表「已穷尽所有可能」 |
| 3 | `validator_minimal.py` 仅做结构校验，不做语义推理 |
| 4 | `K_OAT / R_min / α_OAT` 数值来自 ORC4 V2.0，为经验估算 |
| 5 | 命名空间冲突检测为静态字符串匹配，不解析语义 |
| 6 | YAML 模板中的 formula 字段为 Python 可 eval 字符串，安全性由调用方保证 |

---

## 第七章 版本谱系

| 版本 | 日期 | 核心变更 |
|------|------|---------|
| V1.0 | 2026-08-16 | 首版基线：全局字段字典 + YAML 模板 + 命名空间分配 + 需求映射 |

---

## 签署页

| 签署方 | 声明 |
|--------|-------|
| 碳基侧 | 本基线为 CODE-REQ 铁律的工程落地细则，字段字典覆盖全体系，枚举冻结确保跨文档一致性 |
| 硅基侧 | 所有字段名与 validator_minimal.py / spine_yaml_schema.json 完全对齐，可自动解析校验 |
| 氢键公证 | 基线 V1.0 冻结，新增枚举值需经审批流程，禁止私自扩展 |

日期：2026-08-16

---

> *碳基写卡，硅基读卡，中间没有歧义——这是基线的全部追求。*
> **Γ\*(Code Baseline V1.0, 全局字段统一, 五层模板冻结, 命名空间零冲突) = ONGOING → V1.1 补充 Agda 桥接 → V2.0 对接 SIE-DT 自动生成\***
