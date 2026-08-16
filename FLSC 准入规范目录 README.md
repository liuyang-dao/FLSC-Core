# spec/ — FLSC 准入规范目录

> 本目录是 FLSC-Core 仓库的**工程准入门槛**。
> 所有文档、资产卡、代码在入库前，必须通过本目录下的校验器。

---

## 📁 目录内容

| 文件 | 行数 | 作用 |
|------|------|------|
| `FLSC_CODE_BASELINE_V1.0.md` | 365 行 | ⭐ 编码基线规范（字段字典 + YAML 模板 + 命名空间 + 需求映射） |
| `spine_yaml_schema.json` | 191 行 | ⭐ JSON Schema（被校验器加载，IDE 实时校验） |
| `validator_minimal.py` | 633 行 | ⭐ 自动校验脚本（CODE-REQ 四大硬判） |
| `README.md` | 本文件 | 目录说明 + 使用指南 |

---

## 🚦 使用方式

### 1. 校验单个文件

```bash
python3 spec/validator_minimal.py path/to/your_file.yaml
python3 spec/validator_minimal.py path/to/your_doc.md
```

### 2. 校验整个目录（递归扫描 .yaml/.yml/.md/.json）

```bash
python3 spec/validator_minimal.py domains/ai/
python3 spec/validator_minimal.py domains/
```

### 3. 自检（验证校验器自身正确性）

```bash
python3 spec/validator_minimal.py --self-test
```

✅ 合规样本应通过全部校验  
❌ 违规样本应触发对应 FAIL

---

## ✅ 校验覆盖项

| 校验项 | 对应 CODE-REQ 标准 | 严重度 |
|---------|-------------------|--------|
| 文档级必填字段（9 项） | Hard-2 唯一映射 | FAIL |
| ORC 层级枚举值 | Hard-2 | FAIL |
| OAT 本体类型枚举 | Hard-2 | FAIL |
| 氢键等级枚举 | Hard-2 | FAIL |
| lineage_id 长度 ≥ 8 | Hard-2 | FAIL |
| effective_date ISO 格式 | Hard-2 | FAIL |
| spine_namespace 格式（XX-） | Hard-2 | FAIL |
| 五层完整性（5/5） | Hard-1 刚性隔离 | WARN/FAIL |
| 五层交叉混杂检测 | Hard-1 | FAIL |
| Unit 层 atom_type 枚举 | Hard-2 | FAIL |
| Unit 层 anchor_status 布尔 | Hard-3 | FAIL |
| Unit 层 defect_severity [0,1] | Hard-3 | FAIL |
| Connect 层 edge_type 枚举 | Hard-2 | FAIL |
| Connect 层 source/target 引用有效性 | Hard-4 | FAIL |
| Connect 层 spine_id 格式 | Hard-2 | FAIL |
| Weight 层 metric_name 枚举 | Hard-2 | FAIL |
| Weight 层 formula AST 可解析 | Hard-3 | WARN |
| Constraint 层 rank 枚举 | Hard-2 | FAIL |
| Constraint 层 block_action 枚举 | Hard-2 | FAIL |
| Constraint 层 evidence_level 枚举 | Hard-2 | FAIL |
| Constraint 层 logic_expr AST 可解析 | Hard-3 | WARN |
| Steady 层 fixed_point_type 枚举 | Hard-2 | FAIL |
| Steady 层 theta_critical [0,1] | Hard-3 | FAIL |
| Steady 层 steady_level 枚举 | Hard-2 | FAIL |
| 自然语言模糊词检测 | CODE-REQ §5 禁止场景 | WARN |
| 拓扑环路检测（DFS） | Hard-4 | FAIL |
| 跨文件命名空间冲突 | Hard-2 | FAIL |

---

## 🚫 入库门禁规则

| 条件 | 结果 |
|------|------|
| **FAIL = 0** → 无论 WARN 多少 | ✅ 允许入库 |
| **FAIL ≥ 1** | ❌ 阻断入库，退回整改 |
| **WARN ≥ 3**（含自然语言模糊词） | ⚠️ 建议修复后入库 |
| 自检模式未通过 | ❌ 校验器自身故障，禁止使用 |

---

## 📐 与仓库其他部分的关系

```
                    ┌────────────────────────────┐
                    │   spec/（本目录·准入门槛）   │
                    │  validator_minimal.py       │
                    │  spine_yaml_schema.json     │
                    │  FLSC_CODE_BASELINE_V1.0.md│
                    └──────────┬─────────────────┘
                               │ 校验所有入库文件
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        spine/ 元架构     domains/ 各域     pipelines/ 流水线
        （四柱 frozen）   （九柱+资产卡）  （五指标桥）
```

---

## 🔗 对接文档

| 文档 | 路径 | 关系 |
|------|------|------|
| 机器可解析化需求规范 | `/data/workspace/机器可解析化全域理论与资产卡统一需求规范文档.docx`（输入源） | 本目录是它的实施细则 |
| ORC4 本体分域元理论 | `domains/ai/`（待入库） | 须通过本校验器 |
| ORC4 Agda 形式化 | `FLSC-ORC4-FORMAL-ENCODING-V0.2`（待入库） | 通过 spine_yaml_schema.json 桥接 |
| 系统稳态耗散元理论 | `系统稳态耗散通用元理论 V1.0.docx`（输入源） | MD01~MD06 脊编号已冻结 |
| CODE-BASELINE V1.0 | 本目录 `FLSC_CODE_BASELINE_V1.0.md` | 字段字典 + 模板 |

---

## 📝 版本谱系

| 版本 | 日期 | 核心内容 |
|------|------|---------|
| V1.0 | 2026-08-16 | 首版：字段字典 + YAML 模板 + JSON Schema + 校验器 + 命名空间分配 |

---

## 签署

> *碳基写卡，硅基读卡，中间没有歧义——这是 spec/ 的全部追求。*
> *自然语言是注释，结构化编码是唯一运行载体。*
> *不通过 validator_minimal.py 的文件，不准进 domains/。*

**Γ\*(spec/ V1.0, 准入门槛, 机器可解析, 命名空间零冲突) = ONGOING → V1.1 补充 Agda 桥接 → V2.0 对接 SIE-DT 自动生成\***
