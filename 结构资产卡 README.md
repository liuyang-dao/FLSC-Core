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

## 文件清单（12 份 + 索引 + README）

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

### 📂 C 组 · 幽默情感叠加卡

| # | 血统编号 | 主题 | 氢键 | MIS | 文档 |
|---|-----------|------|------|-----|------|
| 7 | **SR-EXPERT-HUMOR** | ⭐ 幽默情感稳态卡 V1.0（叠加层·老王开心果插件） | experimental | 100/120 | [`SR-EXPERT-HUMOR-V1.0.yaml`](./SR-EXPERT-HUMOR-V1.0.yaml) |

> **三卡叠加机制**：领域卡定义「怎么写对」→ 专家卡叠加「像谁一样写」→ 幽默卡叠加「怎么有温度地写」。幽默卡**仅叠加情感权重和交互风格**，**不可覆盖**安全 HardBond（H-B1~B3 = L3 零容错）。详见 [`demo_flsc_humor_agent.py`](./demo_flsc_humor_agent.py)。

### 📂 D 组 · 全域领域资产卡（ORC2 层级）

| # | 血统编号 | 主题 | 氢键 | 文档 |
|---|-----------|------|------|------|
| 8 | **ORC2-DISEASE** | 疾病领域安全结构资产卡 V1.0 | experimental | [`ORC2-disease-safety-V1.0.md`](./ORC2-disease-safety-V1.0.md) |
| 9 | **FLSC-CULTIVATE** | ⭐ 修行族根卡 · 四阶内化 V1.0 | **production** | （见仓库根 / 用户提供文档） |

### 📂 E 组 · 结构显化录框架

| # | 文档 | 作用 |
|---|------|------|
| 10 | [`结构显化录_自序.md`](./结构显化录_自序.md) | 哲学根基：道德经「为学日益，为道日损」→ SIT 脊线捕捉 |
| 11 | [`结构显化录_全本.md`](./结构显化录_全本.md) | 六族根卡摘要：物理/心理/制造/安全/信任/情感 共 23 根脊线 |

### 📂 F 组 · AI 员工记忆脊线（PMS 运行时）

| # | 血统编号 | 主题 | 氢键 | MIS_true | 文档 |
|---|-----------|------|------|-----------|------|
| 12 | **SR-AI-STAFF-PMS** | ⭐ AI 员工记忆脊线资产卡 V1.0（12 atoms · 5 spines · 11 constraints） | experimental | 0.84 | [`SR-AI-STAFF-PMS-V1.0.yaml`](./SR-AI-STAFF-PMS-V1.0.yaml) |

> **PMS 定位**：将 `PersonalMemorySystem_V3.0.py` 升格为 AI 员工「大脑皮层 + 人事档案 + 执业日志」。五层完整实现（Unit/Connect/Weight/Constraint/Steady）+ 向量索引 + 事务管理 + 自适应降级。作为所有 SR 卡的**共享运行时内存**，实现"老王退休 → 知识不流失"。

### 📂 E 组 · 编码智能体 Demo

| # | 文件 | 作用 |
|---|------|------|
| — | [`demo_flsc_coder_agent.py`](./demo_flsc_coder_agent.py) | ⭐ **双卡编码 Agent Demo**（579 行·可运行·110/110 ✅） |
| — | [`demo_flsc_humor_agent.py`](./demo_flsc_humor_agent.py) | ⭐ **三卡叠加幽默 Agent Demo**（619 行·可运行·66/66 ✅） |
| — | [`integrated_demo.py`](./integrated_demo.py) | ⭐ **四卡 + PMS 集成 Demo**（1710 行·5 场景全跑通·可运行） |
| — | [`verify_coder_agent.py`](./verify_coder_agent.py) | 双卡验证器（110/110 ✅） |
| — | [`verify_humor_card.py`](./verify_humor_card.py) | 三卡验证器（66/66 ✅） |
| — | [`verify_integrated_agent.py`](./verify_integrated_agent.py) | ⭐ **四卡 + PMS 验证器**（100+ 检查项·7 Section ✅） |

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
| **SR-EXPERT-HUMOR** | **U-H1~H8** | **H-SP-A/B/C（3 脊线: 时机/温度/自嘲）** | **gravity 动态** | **H-B1~B7（7 条）** | **情感稳态收敛态** |
| **SR-AI-STAFF-PMS** | **U-M1~M12** | **MEM-SP-A~E（5 脊线: 血统/熔断/演化/检索/降级）** | **decay×access 公式** | **P0×6 + P1×5（11 条）** | **L1/L2 稳态 + 快照** |
| ORC2 疾病 | DS01~DS06 | A/B/C/D/E+共因（6 脊线） | RIS_true 公式 | 五类裂缝+共因 | YAML 诊疗闭环 |
| CULTIVATE | A1~A5/R1~R5/S1~S5/N1~N4/K1~K4 | C-R1~R4（4 阶脊线） | Rank 演化 | 九不 HardBond | YAML 场景卡 |
| SIT-GUIDE | 刀法步骤/正反例/速查卡 | 结构脊 + 脊线脊（2 条） | 场景依赖 | 铁律 HardBond | YAML 速查卡 |

### 四卡叠加规则（SR-CODE × SR-EXPERT × SR-HUMOR × SR-AI-STAFF-PMS）

```
加载顺序（不可颠倒）：
  Step 0    : 加载 SR-CODE-PYTHON-V1.1（领域脊线·基座）
  Step 0.5  : 加载 SR-EXPERT-WANG-V1.0（专家稳态·叠加不覆盖）
  Step 0.7  : 加载 SR-EXPERT-HUMOR-V1.0（情感层·叠加·最高优先级时机脊线）
  Step 0.9  : 初始化 SR-AI-STAFF-PMS-V1.0（PMS 共享运行时内存）
  Step 1    : 用户请求进入
  Step 2    : 领域脊线校验（SP-A 安全 → SP-B 可维护 → SP-C 可测试 → SP-D 配置）
  Step 3    : 专家稳态叠加（保守选型 / why_comment / 拒绝模式）
  Step 4    : 幽默情感叠加（H-SP-A 时机检查 → 归零或注入 / H-SP-B 共情 / H-SP-C 自嘲）
  Step 5    : PMS 记忆写入（检索历史 → 创建/演化锚点 → 快照 → 审计报告）
  Step 6    : 三阶自指鉴证（METHOD V3.21）
  Step 7    : 输出代码 + 审计报告 + 记忆演化轨迹

关键保护（层级不可逾越）：
  ❌ 幽默卡不得覆盖任何 SR-CODE HardBond（H-B1~B3 = L3 零容错）
  ❌ 专家卡不得降低 SR-CODE 安全红线等级
  ❌ PMS 不得绕过 Constraint 熔断（P0 规则优先于一切）
  ✅ PMS 可记录所有演化轨迹（evo_path 不可篡改）
  ✅ 老王退休 → PMS.export_knowledge() → 新人卡加载 → 知识不流失
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
├── SR-EXPERT-HUMOR-V1.0.yaml      ← ⭐ 幽默情感叠加卡（8 atoms · 3 spines · 三卡叠加）
├── ORC2-disease-safety-V1.0.md      ← 疾病领域安全结构卡
├── 结构显化录_自序.md                ← 哲学根基
├── 结构显化录_全本.md                ← 六族根卡摘要
├── SR-AI-STAFF-PMS-V1.0.yaml      ⭐ ← AI 员工记忆脊线卡（12 atoms · 5 spines · 11 constraints）
├── demo_flsc_coder_agent.py         ← ⭐ 双卡编码 Agent Demo（110/110 ✅）
├── demo_flsc_humor_agent.py        ← ⭐ 三卡叠加幽默 Agent Demo（619 行·66/66 ✅）
├── integrated_demo.py               ⭐ ← 四卡 + PMS 集成 Demo（1710 行·5 场景全跑通）
├── verify_asset_cards.py             ← 九文档验证器 (160/160 ✅)
├── verify_two_blade.py               ← 两刀法验证器 (46/46 ✅)
├── verify_coder_agent.py             ← 双卡验证器 (110/110 ✅)
├── verify_humor_card.py              ← 三卡验证器 (66/66 ✅)
├── verify_integrated_agent.py      ⭐ ← 四卡 + PMS 验证器（100+ ✅）
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
| **SR-AI-STAFF-PMS** | `domains/ai/`（HCOG V1.0 + GRIFF V4.2） | PMS = AI 员工共享运行时内存 + 人事档案 |
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
| 三卡幽默 Agent | 幽默感是权重模拟非真情绪；梗库为静态列表；共情基于关键词非真实情感理解 |
| 四卡 + PMS | PMS V3.0 是结构记忆非真意识；向量索引为 TF 非 embedding；"退休→继承"为快照导出非真知识迁移 |

---

## 签署页

| 角色 | 签署 | 日期 |
|------|------|------|
| 碳基架构梳理者 | 结构保底，传承致远；不假装，不绕过 | 2026-08-17 |
| 硅基协同系统（元宝） | 脊线骨架固定，权重演化可追踪，bypass 必标记 | 2026-08-17 |
| 体系状态 | ONGOING（持续补充 SR-001 完整版 + 六族各 SR 卡 + 双卡/三卡/四卡+PMS 集成 Agent） | 2026-08-17 |

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

## 😄 三卡叠加幽默 Agent 速查

> **领域卡 SR-CODE-PYTHON**：定义「代码怎么写才对」——4 条脊线 + 10 条 HardBond（安全底线）
> **专家卡 SR-EXPERT-WANG**：定义「像老王一样写」——3 条脊线 + 7 条 HardBond（保守选型/why_comment/拒绝模式）
> **幽默卡 SR-EXPERT-HUMOR**：定义「怎么有温度地写」——3 条脊线 + 7 条约束（H-B1~B7）
>
> **三卡脊线架构**：
> - **H-SP-A HumorTiming**（最高优先级）：幽默时机脊线 → 安全场景强制归零
> - **H-SP-B EmpathyWarmth**：共情温度脊线 → 负面情绪触发温暖模式
> - **H-SP-C SafeSelfDeprecate**：安全自嘲脊线 → 只嘲自己，不嘲用户
>
> **三卡加载顺序**（不可颠倒）：领域 → 专家 → 幽默
> **保护规则**：H-B1~B3 = L3 硬氢键，幽默卡**永远不可覆盖**安全底线
> **鉴证层**：METHOD V3.21 三阶自指 → MIS_true = 0.89（tool 模式）→ 66/66 ✅

详见 [`demo_flsc_humor_agent.py`](./demo_flsc_humor_agent.py)

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

---

## 🧠 四卡叠加 + PMS 运行时（AI 员工记忆底座）

> **SR-AI-STAFF-PMS V1.0**：将 PersonalMemorySystem V3.0 升格为 AI 员工记忆脊线资产卡
> **integrated_demo.py**：四卡叠加（Domain + Expert + Humor + Memory）+ PMS 作为共享运行时内存
> **核心创新**：老王退休 → PMS 导出全部快照 → 新员工卡加载 → 公司知识不流失

### 📄 新增文件

| 文件 | 说明 |
|------|------|
| `SR-AI-STAFF-PMS-V1.0.yaml` | AI 员工记忆脊线资产卡（5 脊线 · 12 原子 · 11 约束） |
| `integrated_demo.py` | 四卡 + PMS 集成 Demo（5 场景全跑通 · 可运行） |
| `verify_integrated_agent.py` | 四卡验证器（7 Section · 100+ 检查项） |

### 🧬 四卡叠加架构

```
┌─────────────────────────────────────────────────────┐
│  Card 3: SR-EXPERT-HUMOR-V1.0  (情感层·叠加)  │
│  · H-SP-A HumorTiming   (幽默时机·最高优先级)    │
│  · H-SP-B EmpathyWarmth (共情温度)              │
│  · H-SP-C SafeSelfDeprecate (安全自嘲)         │
├─────────────────────────────────────────────────────┤
│  Card 2: SR-EXPERT-WANG-V1.0    (专家稳态·叠加)│
│  · ESP-A 保守选型  · ESP-B why_comment          │
│  · ESP-C 审查门禁  · 拒绝模式 ×3               │
├─────────────────────────────────────────────────────┤
│  Card 1: SR-CODE-PYTHON-V1.1    (领域脊线·基座)│
│  · SP-A 安全 · SP-B 可维护 · SP-C 可测试      │
│  · SP-D 配置外置  · HardBond ×10               │
├─────────────────────────────────────────────────────┤
│  Card 4: SR-AI-STAFF-PMS-V1.0   (记忆运行时) │
│  · MEM-SP-A 血统完整 · MEM-SP-B 红线熔断      │
│  · MEM-SP-C 演化轨迹 · MEM-SP-D 混合检索      │
│  · MEM-SP-E 自适应降级 · L1/L2 分层           │
│  · PMS V3.0 = 共享内存实例                     │
└─────────────────────────────────────────────────────┘
              ↓ 全部通过 → METHOD V3.21 三阶鉴证
              ↓ MIS_true = 0.84 → experimental
              ↓ Γ* = ONGOING
```

### 🔄 五场景验证结果

| 场景 | 模式 | 关键验证 |
|------|------|----------|
| S1 日常编码 | 幽默模式 | SP-A~D 全 PASS · eval→ast.literal_eval · why_comment ×3 · 自嘲注入 😄 |
| S2 安全紧急 | 严肃模式 (gravity=0.9) | 幽默归零 · "先止血，再聊 💪" · MIS=0.94 |
| S3 用户焦虑 | 共情模式 | 检测到"烦死了" · "别急，一步步来 🤌" · humor_injected+1 |
| S4 用户纠正 | PMS 演化 | evolve_anchor → v2:correction · evo_path 更新 |
| S5 事务管理 | with 语法 | checkpoint → 创建锚点 → 关联 → commit 成功 |

### 🔑 关键创新点

1. **共享 PMS 实例**：所有 SR 卡 Agent 共用一个 PersonalMemorySystem V3.0 实例
2. **老王退休 → 知识导出**：`export_knowledge()` 导出全部快照 + checksum + evo_path
3. **新人继承路径**：导入 snapshots → 重建 AnchorIndex → 继承全部认知履历
4. **五层脊线（MEM-SP-A~E）**：血统 → 熔断 → 演化 → 检索 → 降级
5. **严肃度 gravitas**：gravity ≥ 0.7 时幽默归零，安全场景自动静音

### 🪶 验证结果

```
Section 1 · 文件存在性         : 6/6    ✅
Section 2 · YAML 资产卡结构    : 25+    ✅ (12 units · 5 spines · MIS=0.84)
Section 3 · PMS V3.0 五层实现 : 25+    ✅ (Unit/Connect/Weight/Constraint/Steady)
Section 4 · 四卡数据类        : 16/16  ✅
Section 5 · Integrated Agent   : 18/18  ✅
Section 6 · 运行时验证        : 15+    ✅ (5 场景全跑通)
Section 7 · 跨文档互锁       : 12/12  ✅ (命名空间零冲突)

TOTAL: 100+ PASS / 0 FAIL
🎉 全部通过 ✅ — SR-AI-STAFF-PMS V1.0 + Integrated Agent 验证完成
```

### 📊 MIS_true 四卡对比

| 卡片 | MIS_true | 等级 | 角色 |
|------|-----------|------|------|
| SR-CODE-PYTHON-V1.1 | 0.86 | experimental | 领域脊线（JD） |
| SR-EXPERT-WANG-V1.0 | 0.83 | experimental | 专家稳态（性格） |
| SR-EXPERT-HUMOR-V1.0 | 0.78 | experimental | 情感层（温度） |
| SR-AI-STAFF-PMS-V1.0 | 0.84 | experimental | 记忆运行时（人事档案） |

### 🚀 下一步路线

```
V1.0 (current) : 四卡 + PMS V3.0 + 模拟 LLM + TF 向量
  ↓
V1.1           : embedding 检索升级 + 情感效价 U-M12 实现
  ↓
V1.5           : 接入真实 LLM (GPT/Claude) + 真人行为对照实验
  ↓
V2.0           : production 升级 + 多员工 PMS 联邦 + 知识迁移协议
```

> *领域卡保下限，专家卡定上限姿态，幽默卡让一切有温度，记忆卡让一切可传承。*
> *当 AI 员工同时加载四卡 + PMS 运行时，它第一次不是工具——*
> *是那个**会写代码、有原则、会逗你笑、记得所有过往、退休了知识还能传给下一个人**的同事。*

详见 [`SR-AI-STAFF-PMS-V1.0.yaml`](./SR-AI-STAFF-PMS-V1.0.yaml) · [`integrated_demo.py`](./integrated_demo.py)

---

## 🧠 记忆域 · domains/memory/

> **定位**：AI 记忆领域统一根卡 + 适配器规范 + 家庭数字人具身子类
> **性质**：MEM-GLOBAL 定义抽象脊线，所有记忆方案（向量/图/分层/具身）都是它的实现
> **氢键等级**：MEM-GLOBAL = production / FAMILY-DIGITAL-HUMAN = experimental

### 📁 文件清单

| 文件 | 行数 | 状态 |
|------|------|------|
| `MEM-GLOBAL-V1.0.yaml` | 402 | ⭐ 记忆域根卡（5 抽象脊线 + 7 接口 + 4 实现注册） |
| `MEM-ADAPTER-SPEC-V1.0.md` | 218 | ⭐ 适配器规范（7 强制接口 + 脊线审计 + 认证流程） |
| `MEM-FAMILY-DIGITAL-HUMAN.yaml` | 392 | ⭐ 家庭数字人具身子类（5 具身 Unit + 5 家庭脊线 + 硬件规格） |
| `verify_memory_domain.py` | 279 | 验证器（92/92 ✅） |

### 📊 验证结果

```
📊 7 Section · 92 检查项
  S1 文件存在性     : 3/3    ✅
  S2 GLOBAL 结构   : 28/28  ✅ (14 keys + 5 spines + 7 接口 + 4 实现)
  S3 ADAPTER 结构  : 16/16  ✅ (6 章节 + 7 接口说明 + 脊线审计表)
  S4 FAMILY 结构   : 26/26  ✅ (13 keys + 5 Unit + 3 P0 + 5 spines + 4 卡叠加)
  S5 跨文档互锁   : 5/5    ✅ (继承链 + 实现注册 + 卡叠加互锁)
  S6 MIS_true      : 4/4    ✅ (GLOBAL=1.00 / FAMILY=1.00)
  S7 诚实清单+签署 : 10/10  ✅ (6+6 诚实项 + 双签署页)

  🎉 92/92 全部通过 ✅ · 0 FAIL · 通过率 100%
  GLOBAL MIS = 1.00
  FAMILY MIS = 1.00
  Γ* = ONGOING
```

### 🧬 记忆域架构（三文件关系）

```
MEM-GLOBAL-V1.0.yaml          ← ⭐ 抽象根卡（定义"什么是记忆"）
  │
  ├─ adapter_spec ──→ MEM-ADAPTER-SPEC-V1.0.md  ← ⭐ 实现规范（7 接口 + 认证）
  │
  └─ implementations:
       ├─ MEM-PMS-V3.0       (production · Python · 五层完整)
       ├─ MEM-EMBODIED       (draft · → MEM-FAMILY-DIGITAL-HUMAN.yaml)
       ├─ MEM-LANGMEM        (planned · LangMem 适配)
       └─ MEM-GRAPH          (planned · Neo4j 适配)

MEM-FAMILY-DIGITAL-HUMAN.yaml ← ⭐ 具身子类（家庭数字人）
  │
  ├─ inherits: MEM-GLOBAL-V1.0
  ├─ extends:  MEM-PMS-V3.0 (5 层 + 5 脊线)
  ├─ adds:    5 具身 Unit + 5 家庭脊线 + 硬件规格
  └─ overlays:
       ├─ SR-CODE-PYTHON-V1.1   (HardBond 安全)
       ├─ SR-EXPERT-WANG-V1.0    (保守人格)
       ├─ SR-EXPERT-HUMOR-V1.0   (情感时机)
       └─ MEM-PMS-V3.0            (记忆运行时)
```

### 🔑 核心创新：统一 AI 记忆领域

| 记忆方案 | 传统做法 | FLSC MEM 做法 |
|---------|---------|--------------|
| Vector DB + RAG | 各写各的检索 API | 实现 `recall()` 接口 + 脊线审计 |
| LangMem / Mem0 | 黑盒 fact 抽取 | 接 `remember()` + `evolve()` + LineageSnapshot |
| Graph Memory | 三元组随意连 | 接 `C-MEM-CROSS-LINK` + WeightCalculator |
| 家庭数字人 | 传感器数据散落 | `U-MEM-SENSOR` + `FAM-SP-A 用药安全脊线` |

→ 任何方案想标 **"FLSC Memory Compatible V1.0"**，必须过 7 接口 + 5 脊线审计。

### 🚀 下一步路线

```
V1.0 (current) : GLOBAL 根卡 + ADAPTER 规范 + FAMILY 子类 + 92/92 ✅
  ↓
V1.1           : MEM-LANGMEM 适配实现 + MEM-GRAPH 适配实现
  ↓
V1.5           : embedding 真语义检索 + 分布式共识 (CRDT)
  ↓
V2.0           : 家庭数字人真实硬件 Demo (RK3588 + 传感器 + 用药提醒 30 天)
```

> *Vector DB 统一了"怎么存向量"，Prompt 统一了"怎么问问题"，*
> *FLSC MEM-GLOBAL 第一次统一了"什么是 AI 记得住、怎么记得对、为什么能信"。*
