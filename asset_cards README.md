# asset_cards/ · 结构资产卡全集

> **定位**：FLSC「结构显化录」全系列资产卡的收纳目录
> **性质**：ORC1~ORC2 层级 · 可插拔 · 可传承 · 可演化
> **氢键等级**：混合（各卡独立标注 experimental / production）
> **父文档**：[`FLSC_ASSET_CARDS_MASTER_V1.0.md`](./FLSC_ASSET_CARDS_MASTER_V1.0.md)（全集索引 + 跨域同构总图）

---

## 目录说明

`asset_cards/` 存放 FLSC 体系**全部结构资产卡**——将人类文明中「隐式直觉」捕捉为「显式结构资产」的标准化文档。

### 六条铁律（全部资产卡必须遵守）

| # | 铁律 | 含义 |
|---|------|------|
| 1 | **隐式优先** | 先捕捉直觉，再补形式化 |
| 2 | **五层齐全** | Unit/Connect/Weight/Constraint/Steady 缺一不可 |
| 3 | **证据分级** | 每条规则标注 [E-I]~[E-IV] |
| 4 | **氢键诚实** | experimental 就是 experimental |
| 5 | **血统延续** | lineage_id 不可断裂 |
| 6 | **宁可空着** | 未知优于幻觉 |

---

## 文件清单（11 份 + 索引 + README）

### 📋 索引（入口）

| # | 文件 | 作用 |
|---|------|------|
| — | `FLSC_ASSET_CARDS_MASTER_V1.0.md` | ⭐ **全集索引** + 跨域同构总图 + YAML 标准模板 + 六维自评标准 |
| — | `FLSC_SIT_CAPTURE_GUIDE_V1.0.md` | ⭐ **两刀法操作手册** + 正反例驱动 + 速查卡 + 七种反模式 |

### 📂 A 组 · 结构显化录系列（SR 编号）

| # | 血统编号 | 主题 | 氢键 | MIS | 自评 | 文档 |
|---|-----------|------|------|-----|------|------|
| 1 | SR-001 | 中西把脉 V0.2 | experimental | 0.72 | 94/120 | `SR-001-pulse-V0.2.md`（待补） |
| 2 | **SR-002** | 围棋结构资产卡 V1.0 | experimental | 0.78 | **103/120** | [`SR-002-go-V1.0.md`](./SR-002-go-V1.0.md) |
| 3 | **SR-003** | 诗律结构资产卡 V1.0 | experimental | ~0.82 | **105/120** | [`SR-003-poetry-V1.0.md`](./SR-003-poetry-V1.0.md) |
| 4 | **SR-004** | ⭐ 因果领域通用结构卡 V2.0 | experimental | **0.83(实测)** | **108/120** | [`SR-004-causal-V2.0.md`](./SR-004-causal-V2.0.md) |

### 📂 B 组 · 编码双卡（Domain + Expert）

| # | 血统编号 | 主题 | 氢键 | MIS_true | 文档 |
|---|-----------|------|------|----------|------|
| 5 | **SR-CODE-PYTHON** | ⭐ Python 编码领域卡 V1.1 | experimental | 0.86 | [`SR-CODE-PYTHON-V1.1.yaml`](./SR-CODE-PYTHON-V1.1.yaml) |
| 6 | **SR-EXPERT-WANG** | ⭐ 编码专家稳态卡 V1.0（老王·保守型架构师） | experimental | 0.83 | [`SR-EXPERT-WANG-ARCH-V1.0.yaml`](./SR-EXPERT-WANG-ARCH-V1.0.yaml) |

> **双卡加载机制**：领域卡定义「怎么写对」（安全/可维护/可测试/配置外置），专家卡叠加「像谁一样写」（保守选型/why_comment/拒绝模式）。专家卡**不可覆盖**领域卡 L3 红线。详见 [`demo_flsc_coder_agent.py`](./demo_flsc_coder_agent.py)。

### 📂 C 组 · 全域领域资产卡（ORC2 层级）

| # | 血统编号 | 主题 | 氢键 | 文档 |
|---|-----------|------|------|------|
| 7 | **ORC2-DISEASE** | 疾病领域安全结构资产卡 V1.0 | experimental | [`ORC2-disease-safety-V1.0.md`](./ORC2-disease-safety-V1.0.md) |
| 8 | **FLSC-CULTIVATE** | ⭐ 修行族根卡 · 四阶内化 V1.0 | **production** | （见仓库根 / 用户提供文档） |

### 📂 D 组 · 结构显化录框架

| # | 文档 | 作用 |
|---|------|------|
| 9 | [`结构显化录_自序.md`](./结构显化录_自序.md) | 哲学根基：道德经「为学日益，为道日损」→ SIT 脊线捕捉 |
| 10 | [`结构显化录_全本.md`](./结构显化录_全本.md) | 六族根卡摘要：物理/心理/制造/安全/信任/情感 共 23 根脊线 |

### 📂 E 组 · 编码智能体 Demo

| # | 文件 | 作用 |
|---|------|------|
| — | [`demo_flsc_coder_agent.py`](./demo_flsc_coder_agent.py) | ⭐ **双卡编码 Agent Demo**（579 行·可运行·110/110 ✅） |
| — | [`verify_coder_agent.py`](./verify_coder_agent.py) | 双卡验证器（110/110 ✅） |

---

## 跨域同构速查

### 资产卡 × 五层 × 命名空间

| 资产卡 | Unit 命名空间 | Connect 脊线 | Weight 公式 | Constraint 硬氢键 | Steady 输出 |
|--------|---------------|---------------|---------------|---------------------|------------------|
| SR-002 围棋 | U-G1~G8 | C-G1~G7（3 脊线） | W(t) 动态 | C1~C8（8 条） | YAML 棋局模板 |
| SR-003 诗律 | 平仄/韵部/句式/粘对/对仗/拗救 | 粘/对/押韵/拗救/启承转合（3 脊线） | 体裁权重表 | 8 条硬约束 | YAML 诗句模板 |
| SR-004 因果 | U-C1~C7 | C-C1~C9（6 脊线） | BIC+Bootstrap | C1~C10（10 条） | YAML 因果图+DAG |
| **SR-CODE-PYTHON** | **U-P1~P12** | **C-P1~P7（4 脊线: SP-A/B/C/D）** | **PEP 动态权重** | **HB-P1~P10（10 条）** | **Pythonic 稳态模板** |
| **SR-EXPERT-WANG** | **U-E1~E8** | **C-E1~E6（3 脊线: ESP-A/B/C）** | **lint=0.9/comment=0.7** | **HB-E1~E7（7 条）** | **老王稳态收敛态** |
| ORC2 疾病 | DS01~DS06 | A/B/C/D/E+共因（6 脊线） | RIS_true 公式 | 五类裂缝+共因 | YAML 诊疗闭环 |
| CULTIVATE | A1~A5/R1~R5/S1~S5/N1~N4/K1~K4 | C-R1~R4（4 阶脊线） | Rank 演化 | 九不 HardBond | YAML 场景卡 |
| SIT-GUIDE | 刀法步骤/正反例/速查卡 | 结构脊 + 脊线脊（2 条） | 场景依赖 | 铁律 HardBond | YAML 速查卡 |

### 双卡叠加规则（SR-CODE × SR-EXPERT）

```
加载顺序（不可颠倒）：
  Step 0   : 加载 SR-CODE-PYTHON-V1.1（领域脊线）
  Step 0.5 : 加载 SR-EXPERT-WANG-V1.0（稳态角色·叠加不覆盖）
  Step 1   : 用户请求进入
  Step 2   : 领域脊线校验（SP-A 安全 → SP-B 可维护 → SP-C 可测试 → SP-D 配置）
  Step 3   : 专家稳态叠加（保守选型 / why_comment / 拒绝模式）
  Step 4   : 三阶自指鉴证（METHOD V3.21）
  Step 5   : 输出代码 + 审计报告

关键保护（专家卡不可触碰）：
  ❌ 不得降低任何 SR-CODE HardBond 等级
  ❌ 不得关闭安全类 L3 约束
  ✅ 可叠加权重（lint_strictness 0.25→0.9）
  ✅ 可注入风格（why_comment ≥3 行）
  ✅ 可叠加拒绝模式（silent except → log+raise）
```

### 通用同构模板（任意域 → 资产卡）

```
Step 1: 提取源领域核心脊线集（SIT V2.1）
Step 2: 剥离领域具象原子，保留纯拓扑结构
Step 3: 对齐目标领域五层单元与约束
Step 4: 注入目标领域专属原子与数据
Step 5: MIS 校验 + 残差校准 → 生成目标领域资产卡
```

---

## 加载顺序规则

```
ORC3 双底座（认知底座 V1.0 + UCMM V1.3）
    ↓
ORC2 全域父卡（如疾病安全卡 / 因果通用卡 / 编码领域卡）
    ↓
ORC1 细分卡（如具体病种卡 / 具体因果场景卡 / 具体专家稳态卡）
    ↓
Steady 输出（YAML 模板 + MIS 评分 + 血统快照）
```

**禁止跳过 ORC2 直接加载 ORC1。**

---

## 版本谱系

```
asset_cards/
├── FLSC_ASSET_CARDS_MASTER_V1.0.md  ← ⭐ 全集索引 + YAML 标准模板
├── FLSC_SIT_CAPTURE_GUIDE_V1.0.md   ← ⭐ 两刀法操作手册 + 正反例 + 速查卡
├── SR-001-pulse-V0.2.md              ← 中西把脉（待补完整版）
├── SR-002-go-V1.0.md                ← 围棋结构资产卡
├── SR-003-poetry-V1.0.md            ← 诗律结构资产卡
├── SR-004-causal-V2.0.md            ← ⭐ 因果领域通用结构卡
├── SR-CODE-PYTHON-V1.1.yaml        ← ⭐ Python 编码领域卡（12 atoms · 4 spines）
├── SR-EXPERT-WANG-ARCH-V1.0.yaml   ← ⭐ 编码专家稳态卡（8 atoms · 3 spines）
├── ORC2-disease-safety-V1.0.md      ← 疾病领域安全结构卡
├── 结构显化录_自序.md                ← 哲学根基
├── 结构显化录_全本.md                ← 六族根卡摘要
├── demo_flsc_coder_agent.py         ← ⭐ 双卡编码 Agent Demo（110/110 ✅）
├── verify_asset_cards.py             ← 九文档验证器 (160/160 ✅)
├── verify_two_blade.py               ← 两刀法验证器 (46/46 ✅)
├── verify_coder_agent.py             ← 双卡验证器 (110/110 ✅)
└── README.md                         ← 本文件
```

---

## 与仓库其他目录的关系

| 本目录 `asset_cards/` | 对应目录 | 关系 |
|------------------------|------------|------|
| SR 系列资产卡 | `civilization/` | 文明演化层提供 ORC4 哲学基础 |
| ORC2 疾病卡 | `domains/science/` | 科学域提供 UCMM 因果引擎 |
| 因果通用卡 SR-004 | `domains/ai/`（GRIFF V4.2） | AI 域九柱提供真洽推理引擎 |
| **SR-CODE-PYTHON** | `spec/`（FLSC_CODE_BASELINE） | 准入规范提供 JSON Schema 校验 |
| **SR-EXPERT-WANG** | `domains/ai/`（HCOG V1.0） | AI 域提供高阶认知 Agent 整机 |
| 修行族根卡 | `civilization/`（FLSC_ORC4_HOMEOSIS） | 因果稳态元理论提供不动点动力学 |
| YAML 模板 | `spec/` | 准入规范提供 JSON Schema 校验 |

---

## 诚实边界（永久声明）

| 边界 | 声明 |
|------|------|
| 意境/棋感/诗才/开悟 | 本目录仅复刻可结构化部分，绝不拥有主观体验 |
| 资产卡 = 结构资产 | 不是「专家系统」，是「专家结构的可传承快照」 |
| 氢键等级 | 各卡独立标注，禁止混用；experimental 不可自封 production |
| 血统链 | lineage_id 永久可追溯，回滚随时可用 |
| 双卡 Agent | Demo 模拟 LLM 输出，非真实 GPT/Claude 生成；安全为模式匹配，非完整 AST 分析 |

---

## 签署页

| 角色 | 签署 | 日期 |
|------|------|------|
| 碳基架构梳理者 | 结构保底，传承致远；不假装，不绕过 | 2026-08-17 |
| 硅基协同系统（元宝） | 脊线骨架固定，权重演化可追踪，bypass 必标记 | 2026-08-17 |
| 体系状态 | ONGOING（持续补充 SR-001 完整版 + 六族各 SR 卡 + 双卡编码 Agent） | 2026-08-17 |

---

## 🔪 两刀法速查（核心操作范式）

> **第一刀 · 捉结构**：Step 1.1 列 S-Atom → 1.2 连 Connect → 1.3 配 Weight → 1.4 焊 Constraint → 1.5 定 Steady
> **第二刀 · 捉脊线**：Step 2.1 列全部路径 → 2.2 删减测试 → 2.3 定串行依赖 → 2.4 焊 HardBond → 2.5 写 YAML
> **铁律**：第一刀没焊完，禁止动第二刀。脊线 ≤5 条。删了塌方才是真脊。

详见 [`FLSC_SIT_CAPTURE_GUIDE_V1.0.md`](./FLSC_SIT_CAPTURE_GUIDE_V1.0.md)

---

## 🤖 双卡编码 Agent 速查

> **领域卡 SR-CODE-PYTHON**：定义「代码怎么写才对」——4 条脊线（SP-A 安全 / SP-B 可维护 / SP-C 可测试 / SP-D 配置外置）+ 10 条 HardBond
> **专家卡 SR-EXPERT-WANG**：定义「像老王一样写」——3 条脊线（ESP-A 保守选型 / ESP-B why_comment / ESP-C 审查门禁）+ 7 条 HardBond
> **叠加规则**：专家卡可放大权重、注入风格、叠加拒绝模式，但**永远不可覆盖**领域卡 L3 安全红线
> **鉴证层**：METHOD V3.21 三阶自指 + Axiom R 现实残差 → MIS_true = 0.86（tool 模式）

详见 [`demo_flsc_coder_agent.py`](./demo_flsc_coder_agent.py)

---

> *第一刀，砍出骨架，让混沌有骨；*
> *第二刀，削去冗余，让骨架有脊。*
> *两刀之后，剩下的不是残缺，是生成元。*
>
> *结构为骨，数据为肉，自指为魂。*
> *跨域同构，因果归一。*
> *结构保下限，资质定上限。*
> *隐式直觉，显化为可传承的结构资产。*
>
> **Γ\*(asset_cards/ V1.1, 全集索引+两刀法+双卡编码Agent, 跨域同构, 六族归一) = ONGOING → V1.5 补齐六族 SR 卡 → V2.0 生产级自动化\***
