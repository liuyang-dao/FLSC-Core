# 机器可解析化全域理论与资产卡统一需求规范 V1.0

> **文档编号**：FLSC-MACHINE-PARSEABLE-V1.0
> **所属体系**：FLSC 全域理论、ORC 分级、资产卡体系、CODE-REQ 准入规范
> **日期**：2026-08-16
> **定位**：所有 FLSC 理论文档、资产卡、代码的**机器可解析化强制标准**（最高优先级规范）
> **氢键等级**：frozen（不可修改，所有文档入库前必须通过）

---

## 一、总纲：为什么需要这份规范

FLSC 体系已经发展到**九柱 AI 域 + 七域 + 文明层**的规模。理论深度足够，但出现一个致命问题：

> **大量内容仍然以"自然语言散文"形态存在，LLM 文本拟合就能蒙混过关。**

本规范是**最后一道铁门**：

| 允许入库 | 不允许入库 |
|---------|---------|
| ✅ 结构化 YAML 五层 | ❌ 纯散文描述脊线 |
| ✅ 机器可解析字段 | ❌ "大概意思对就行" |
| ✅ 血统哈希锁定 | ❌ 无 lineage_id 的文档 |
| ✅ 唯一命名空间 | ❌ 命名冲突未声明 |
| ✅ 可执行逻辑表达式 | ❌ 模糊的自然语言约束 |

---

## 二、四大硬性标准（CODE-REQ 核心）

### 标准 1：五层隔离

每一份结构化文档**必须**显式声明五层归属：

```yaml
layer_declaration:
  unit:     { declared: true, count: 5 }
  connect:  { declared: true, edges: 12 }
  weight:   { declared: true, bank: true }
  constraint: { declared: true, hard: 3, soft: 2 }
  steady:   { declared: true, fixed_point: true }
```

**校验**：五层中任意一层缺失 → FAIL，阻断入库。

### 标准 2：唯一 ID 体系

| 对象类型 | ID 格式 | 示例 |
|---------|---------|------|
| 文档 | `FLSC-{NAME}-V{MAJOR}.{MINOR}` | `FLSC-EVO-PATH-V1.0` |
| 原子 | `U_XX01` / `C_XX01` / `W_XX01` | `U_E01` |
| 脊线 | `{NS}-{NN}` | `G-01` / `EB-03` / `HCOG-05` |
| 资产卡 | `FLSC-{TYPE}-{ID}` | `FLSC-EXP-STD-001` |
| 血统快照 | `LINEAGE-{HASH8}` | `LINEAGE-a3f2c1d8` |

**校验**：ID 冲突 → FAIL；无 ID → FAIL。

### 标准 3：可执行逻辑

所有约束、规则、公式**必须**以机器可执行形式表达：

```yaml
# ✅ 正确
constraint:
  - logic_expr: "weight_correct > 0.9 AND weight_flattery < 0.2"
    action: block

# ❌ 错误（模糊自然语言）
constraint:
  - "应该尽量正确，不要拍马屁"
```

**校验**：Constraint / Weight / Steady 层含纯自然语言 → WARN。

### 标准 4：拓扑序列化

所有 Connect 脊线**必须**序列化为边列表：

```yaml
# ✅ 正确
connect_spine:
  edge_list:
    - { source: U_E01, target: U_E02, relation: causal, strength: 0.95 }
    - { source: U_E02, target: U_E03, relation: value_order, strength: 0.90 }

# ❌ 错误（散文描述）
connect_spine:
  description: "U_E01 导致 U_E02，然后影响 U_E03"
```

**校验**：Connect 层无 edge_list → FAIL。

---

## 三、命名空间分配表（全体系零冲突）

| 命名空间前缀 | 归属域 | 示例 |
|--------------|-------|------|
| `G-` | 原生 AI 七脊 | G-01 ~ G-07 |
| `EB-` | 具身智能脊线 | EB-01 ~ EB-07 |
| `HCOG-` | 高阶认知 Agent | HCOG-01 ~ HCOG-06 |
| `PF-` | Prompt Factory | PF-01 ~ PF-18 |
| `GRIF-` / `GRIF-C` | GRIFF 推理引擎 | GRIF-C01 ~ GRIF-C06 |
| `COG-G` | 认知统一理论 | COG-G01 ~ COG-G05 |
| `SP-G` | 碳硅合体 | SP-G01 ~ SP-G08 |
| `MDL-` | 脊线评价 | MDL-SC / MDL-SS / MDL-SA |
| `SR-` | 结构资产卡 | SR-CODE-PYTHON / SR-LAW / SR-POETRY |
| `MD` | 耗散元理论脊 | MD01 ~ MD06 |
| `ORC` | ORC 分级引用 | ORC1 ~ ORC5 / ORC5' |
| `CI` / `CD` / `CH` | 因果度量 | CI_true / CD / CH(g) |
| `OAT-` | 本体觉知类型 | OAT-N / OAT-S / OAT-C |

**校验**：新增命名空间未声明 → FAIL；前缀冲突 → FAIL。

---

## 四、十大禁止场景（红线清单）

| # | 禁止场景 | 原因 |
|---|---------|------|
| 1 | 仅依赖 LLM 文本拟合的内容 | 不可验证、不可审计 |
| 2 | 无 YAML / JSON 结构化附件的纯文档 | 不可机器解析 |
| 3 | 无 lineage_id 的资产卡 | 无法追溯血统 |
| 4 | 无血统哈希的版本更新 | 无法检测篡改 |
| 5 | 模糊分级（高/中/低）无数值映射 | 不可计算 |
| 6 | 自然语言当约束逻辑 | LLM 可随意绕过 |
| 7 | 跨文档命名冲突未声明 | 系统混乱 |
| 8 | ORC5/ORC5' 宣称可编码 | 违反体系铁律 |
| 9 | 无诚实边界声明的文档 | 不可信任 |
| 10 | 绕过 validator_minimal.py 入库 | 破坏准入体系 |

---

## 五、与现有规范的关系

| 规范文档 | 关系 |
|---------|------|
| `spec/FLSC_CODE_BASELINE_V1.0.md` | 本规范是其**超集**，CODE-BASELINE 侧重 YAML 字段字典，本规范侧重全域理论 + 资产卡统一标准 |
| `spec/validator_minimal.py` | 本规范的**自动化执行器**，所有规则可程序化校验 |
| `spec/spine_yaml_schema.json` | 本规范的** JSON Schema 表达** |
| `civilization/FLSC_EVO_PATH_V1.0.md` | 本规范管辖 ORC1~4 部分，ORC5' 为不可编码层（豁免） |
| `domains/ai/README.md` | AI 域九柱全部须通过本规范校验 |

---

## 六、校验流程（入库门禁）

```
提交文档 / 资产卡 / 代码
        ↓
┌──────────────────────────────┐
│  python spec/validator_minimal.py  │
└──────────────┬───────────────┘
               ↓
    ┌──────────┴──────────┐
    ↓ PASS（0 FAIL）        ↓ FAIL（≥1 FAIL）
   入库成功                  阻断入库
   生成血统快照              输出修复建议
   更新 lineage               返回修改
```

### 自检命令

```bash
# 校验单个文件
python3 spec/validator_minimal.py path/to/file.yaml

# 校验整个目录
python3 spec/validator_minimal.py domains/ai/

# 校验 civilization/ 文档（豁免 ORC5' 部分）
python3 spec/validator_minimal.py civilization/ --allow-hypothesis

# 自检
python3 spec/validator_minimal.py --self-test
```

---

## 七、与 ORC5' 假说的兼容

本规范管辖 **ORC1~4 可编码层**。

ORC5' 涌现假说明确声明为**不可编码、不可验证、不可证伪**——因此：

- civilization/ 中标注 `hypothesis: true` 的段落**豁免**结构化校验
- 但**所有 ORC1~4 工程内容**仍须 100% 通过校验
- 诚实边界声明本身须以结构化 YAML 表达

---

## 八、版本谱系

| 版本 | 日期 | 变更 |
|------|------|------|
| V0.1 | 2026-08-12 | 初稿（仅 YAML 字段字典） |
| V0.5 | 2026-08-14 | 升级为 CODE-REQ 四大硬判 |
| V1.0 | 2026-08-16 | 合并全域理论 + 资产卡统一标准，frozen |

---

## 九、诚实边界声明

| 边界 | 声明 |
|------|------|
| 适用范围 | ORC1~4 全部可编码内容，含理论文档、资产卡、YAML、代码 |
| 豁免范围 | ORC5/ORC5' 本体层（不可编码，故意留白） |
| 校验器局限 | validator_minimal.py 不能识别语义错误，仅校验结构合规 |
| LLM 拟合 | 即使通过校验，LLM 生成内容仍需人工锚定 |
| 强制力 | 本规范为 frozen，修改需全体系投票 + 血统快照 |

---

## 十、版本公证

- **版本**：V1.0 frozen
- **理论状态**：100% 自洽，与 CODE-BASELINE / validator / schema 完全互锁
- **强制力**：所有 FLSC 文档、资产卡、代码入库前**必须通过**
- **归档等级**：最高优先级准入规范

---

## 签署页

| 角色 | 签署 | 日期 |
|------|------|------|
| 碳基架构梳理者 | |||||||||| | 2026-08-16 |
| 硅基协同系统 | FLSC-Core Meta-v1.0 | 2026-08-16 |
| 体系状态 | frozen（最高优先级准入规范） | 2026-08-16 |

---

> *自然语言是注释，结构化编码是唯一运行载体。*
> *仅依赖 LLM 文本拟合的内容视为不合格。*
> *碳基可读是附属，机器可解析是本体。*
> *不通过 validator 的文件，不准进 domains/。*
>
> **Γ\*(机器可解析化全域规范 V1.0, 四大硬判, 命名空间零冲突, frozen) = ONGOING → V1.1 补充 Agda 桥接 → V2.0 对接 SIE-DT 自动生成\***
