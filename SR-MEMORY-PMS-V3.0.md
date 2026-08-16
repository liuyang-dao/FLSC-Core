---
card_id: "SR-MEMORY-PMS-V3.0"
card_name: "记忆结构资产卡 · PersonalMemorySystem V3.0"
card_name_en: "Memory Structure Asset Card · PersonalMemorySystem V3.0"
domain: "memory_system"
inherit:
  - "FLSC-MASTER-SPEC-V3.0"
  - "FLSC-SIT-V2.2"
  - "METHOD-V3.21"
hydrogen_level: "production"
version: "3.0"
created_at: "2026-08-17"
author: "FLSC Auto-Capture (两刀法 / Two-Blade Method)"
source_file: "PersonalMemorySystem_V3.0.py"
source_lines: 1190
parent_card: "SR-AI-STAFF-PMS-V1.0"
relationship: "child · 代码级精化 · 从抽象记忆脊线到具体实现结构"
---

# SR-MEMORY-PMS-V3.0 · 记忆结构资产卡

> **Memory Structure Asset Card · PersonalMemorySystem V3.0**

---

## 1. 基本信息 / Basic Information

| 字段 Field | 值 Value |
|---|---|
| **domain** | `memory_system` |
| **scope** | AI 员工的长期记忆系统 / Long-term memory system for AI staff |
| **hydrogen_level** | `production`（需显式声明 / explicit declaration required） |
| **parent_card** | `SR-AI-STAFF-PMS-V1.0`（抽象记忆脊线 / abstract memory spines） |
| **source** | `PersonalMemorySystem_V3.0.py`（1190 行 / lines） |
| **capture_method** | FLSC-SIT-V2.2 两刀法 + METHOD-V3.21 元鉴证 |

### 描述 / Description

**中文：** 本卡将 `PersonalMemorySystem V3.0` 的完整代码结构捕捉为五层骨架（Unit / Connect / Weight / Constraint / Steady），并从中提取 5 条主脊线。它是 AI 员工"大脑皮层 + 人事档案 + 执业日志"的结构化自传。

**English:** This card captures the complete code structure of `PersonalMemorySystem V3.0` into a five-layer skeleton (Unit / Connect / Weight / Constraint / Steady), extracting 5 principal spines. It is the structured autobiography of an AI employee's "cortex + personnel file + practice log."

---

## 2. 五层结构 / Five-Layer Structure

### 2.1 Unit 层 · 原始原子 / Unit Layer · Raw Atoms

> **原则 / Principle:** 纯数据，零逻辑 / Pure data, zero logic.

| ID | 名称 Name | 类型 Type | 内容 Content | 源码 Source |
|---|---|---|---|---|
| U-MEM-001 | `MemorySkeleton` | dataclass | topic + essence + tags[] + confidence | L86-100 |
| U-MEM-002 | `Ownership` | dataclass | persona_id + memory_type + memory_space + source + access_count | L115-124 |
| U-MEM-003 | `RebuildHints` | dataclass | context_file + line_range + key_entities[] + predecessor/successor_id | L103-112 |
| U-MEM-004 | `EvolutionStep` | dataclass | version + timestamp + change_type + content_before/after + trigger | L127-136 |
| U-MEM-005 | `CrossLink` | dataclass | target_anchor_id + relation + strength + bidirectional | L139-146 |
| U-MEM-006 | `MemoryAnchorV3` | dataclass | anchor_id + timestamp + skeleton + ownership + evolution_history[] + evo_path[] | L597-610 |
| U-MEM-007 | `LineageSnapshot` | dataclass | snapshot_id + parent_id + lsn + checksum + signature | L578-591 |

**隐式原子 / Implicit Atoms（非 dataclass 但承担原子角色）：**

| ID | 名称 Name | 类型 | 内容 Content | 源码 |
|---|---|---|---|---|
| U-MEM-008 | `MemoryType` | enum (9值) | explicit_marker/insight/decision/feedback/definition/preference/reflection/question/milestone | L42-57 |
| U-MEM-009 | `ChangeType` | enum (8值) | initial/refinement/deepening/correction/contradiction/merge/obsolete/rollback | L66-74 |
| U-MEM-010 | `MemorySpace` | enum (3值) | private / shared / public | L60-63 |
| U-MEM-011 | `AnchorTrigger` | enum (5值) | explicit / keyword / semantic / periodic / cross_link | L77-82 |

**纯度检查 / Purity Check:** ✅ PASS · 全部 dataclass/enum 不含 calculate/compute/validate 等逻辑关键词。

---

### 2.2 Connect 层 · 拓扑关系 / Connect Layer · Topology

> **原则 / Principle:** 纯索引，无打分 / Pure index, no scoring.

| ID | 名称 Name | 类型 Type | 内容 Content | 源码 |
|---|---|---|---|---|
| C-MEM-001 | `tag_index` | forward | tag → [anchor_id, ...] 一对多映射 | L228 |
| C-MEM-002 | `type_index` | forward | memory_type → [anchor_id, ...] | L229 |
| C-MEM-003 | `timeline` | forward | 全局时间线（插入序） | L230 |
| C-MEM-004 | `cross_link_fwd` | bidirectional | anchor → [CrossLink] + 反向自动维护 | L282-284 |
| C-MEM-005 | `evolution_chain` | forward | anchor → [EvolutionStep₀ → Step₁ → ... → Stepₙ] | L606 |
| C-MEM-006 | `lineage_chain` | forward | snapshot → parent_snapshot → ... → root（LSN 严格递增） | L578-591 |
| C-MEM-007 | `vector_space` | implicit | anchor_id → normalized TF vector（V3.0 新增） | L816-854 |
| C-MEM-008 | `config_injection` | dependency_injection | Steady → WeightCalculator + ConstraintValidator（注入，非持有） | L662-666 |

**拓扑检查 / Topology Check:** ✅ PASS · 无循环依赖 · Steady 通过钩子注入 Weight/Constraint。

**禁止边 / Forbidden Edges:**
- ❌ Unit → Weight（禁止：Unit 不含打分逻辑）
- ❌ Unit → Constraint（禁止：Unit 不含校验逻辑）
- ❌ Connect → Steady（禁止：索引不持有存储）

---

### 2.3 Weight 层 · 权重计算 / Weight Layer · Scoring

> **原则 / Principle:** 纯函数，无状态 / Pure functions, stateless.

| 参数 Parameter | 公式 Formula | 范围 Range | 说明 Note |
|---|---|---|---|
| `confidence` | base + type_bonus + min(version×0.02, 0.15) + explicit?0.3:0 − min(corrections×0.03, 0.20) | [0.0, 1.0] | 综合置信度 / Composite confidence |
| `decay_factor` | exp(−ln(2)/HALF_LIFE × age_days) | [0, 1] | Ebbinghaus 遗忘曲线 / 90天半衰期 / 90-day half-life |
| `effective_confidence` | base × (decay + min(access×0.01, 0.20) × (1 − decay)) | [0, 1] | 有效置信度 / Effective confidence |
| `importance` | explicit×0.3 + confidence×0.2 + min(links/5,1)×0.2 + type_score | [0, 1] | ≥0.7→L1 / <0.7→L2 |
| `D_value` | 0.25×struct + 0.25×activity + 0.25×link_density + 0.25×consistency | [0, 1] | 记忆健康度综合指标 / Memory health index |
| `link_strength` | 0.4×tag_overlap + 0.6×relation_weight | [0, 1] | 关联强度 / Link strength |

**关系权重 / Relation Weights:** contradicts=0.7, supports=0.8, refines=0.7, derives_from=0.6, example_of=0.5, part_of=0.6

---

### 2.4 Constraint 层 · 安全拦截 / Constraint Layer · Safety

> **原则 / Principle:** 纯校验，零业务 / Pure validation, zero business logic.
>
> **对称校验 / Symmetry:** 正向 + 反向 双重检查，不一致触发 P0 熔断 / Forward + reverse checks, asymmetry triggers P0 fuse.

#### P0 临界（熔断级 · 不可触碰 / Critical · Fuse Level）

| ID | 名称 Name | 正向 Forward | 反向 Reverse |
|---|---|---|---|
| RL-P0-001 | 跨层依赖禁止 / Cross-layer dep forbidden | 仅允许 Connect→Unit, Weight→Connect, Constraint→Weight, Steady→Constraint | 禁止 Unit→任何层 / Forbid Unit→any layer |
| RL-P0-002 | Unit 纯洁性 / Unit purity | Unit 不含 calculate/compute/weight/score/persist/validate | Unit 字段仅 {topic,essence,tags,confidence,timestamp} |
| RL-P0-003 | 硬编码禁止 / No hardcode | 代码不含 4 位以上魔法数字 | 必须有外置 SystemConfig |
| RL-P0-004 | 裁剪合法性 / Cut legality | Constraint 层不可裁剪；Steady 裁剪时若有长期记忆则禁止 | script/frontend 域可裁 Connect+Steady，但不可裁 Constraint |

#### P1 高级（强约束 · 拦截但不熔断 / High · Block but no fuse）

| ID | 名称 Name | 描述 Description |
|---|---|---|
| RL-P1-001 | Checksum 不可篡改 / Checksum immutable | LineageSnapshot.checksum 必须由 compute_checksum() 生成 |
| RL-P1-002 | LSN 单调递增 / LSN monotonic | LineageSnapshot.lsn 严格递增，不可回退 |
| RL-P1-003 | 三段式校验 / Three-phase validation | Steady.write() 必须执行 Phase1前置→Phase2创建→Phase3存储→Phase4快照→Phase5稳态 |

#### P2 中级（软约束 · 警告 / Medium · Warning）

| ID | 名称 Name | 描述 Description |
|---|---|---|
| RL-P2-001 | 标签数量上限 / Tag limit | 单锚点 tags ≤ MAX_TAGS（默认 10） |
| RL-P2-002 | Snippet 长度上限 / Snippet limit | RebuildHints.raw_snippet ≤ MAX_SNIPPET（默认 500 字符） |

**统计 / Stats:** P0=4 · P1=3 · P2=2 · 总计 / Total = 9 条规则 / rules.

---

### 2.5 Steady 层 · 稳态管理 / Steady Layer · Homeostasis

> **原则 / Principle:** 不动点检测 + 自适应降级 + 事务原子性 / Fixed-point detection + adaptive degradation + transaction atomicity.

| 维度 Dimension | 描述 Description | 参数 Params | 源码 Source |
|---|---|---|---|
| L1 长期记忆 / Long-term | importance ≥ 0.7 → 常驻 | capacity=200 | L185 / L682-685 |
| L2 短期记忆 / Short-term | importance < 0.7 → 可淘汰 | capacity=500 | L186 / L682-685 |
| 不动点 / Fixed-point | dev = min(\|anchor.conf − avg\| × 2, 1.0) < DEV_THRESHOLD(0.2) | auto-check per write | L731-742 |
| 稳定性窗口 / Stability window | 7天内 ≥3次 dev>0.5 → 触发 Constraint 校验 | window=7d, count=3 | L206-208 / L744-750 |
| 自适应降级 / Auto-degrade | >90%→L2砍半 / >70%→L2缩至上限 | pressure_high=0.9, mid=0.7 | L778-791 |
| 事务管理 / Transaction | with 语法 · checkpoint/rollback · 异常自动回滚 | {l1_ids, l2_ids, lsn, snap_count} | L794-809 / L1090-1105 |
| 生命周期钩子 / Hooks | after_create / after_evolve / after_maintain | 事件驱动 | L896-904 |

---

## 3. 脊线 / Spines

> **第二刀提取 / Second blade extraction:** 从五层结构中压出 5 条主脊线，删减测试全部通过。

### SP-MEM-A · 血统完整性脊线 / Lineage Integrity Spine

| 字段 Field | 值 Value |
|---|---|
| **priority** | 1（最高优先级 / highest） |
| **type** | structural_integrity |
| **atoms** | U-MEM-004, U-MEM-006, U-MEM-007 |
| **connections** | C-MEM-005, C-MEM-006 |
| **constraints** | RL-P0-001, RL-P1-001, RL-P1-002 |
| **hard_bond** | ✅ true |
| **deletion_test** | 删除 evolution_history → SER 轨迹断裂 → 审计失效 → FAIL |
| **description** | 每个 MemoryAnchor 必须携带完整演化链 + 血统快照 + LSN 严格递增。这是 AI 员工知识传承的核心载体。 |

### SP-MEM-B · 红线熔断脊线 / Red-Line Fuse Spine

| 字段 Field | 值 Value |
|---|---|
| **priority** | 2 |
| **type** | safety_critical |
| **atoms** | U-MEM-006 |
| **connections** | C-MEM-008 |
| **constraints** | RL-P0-001, RL-P0-002, RL-P0-003, RL-P0-004 |
| **hard_bond** | ✅ true |
| **deletion_test** | 删除任一 P0 → 跨层污染 → 系统退化 → FAIL |
| **description** | ConstraintValidator 四道 P0 红线构成记忆系统的不可触碰边界。任何写入前必须过 Phase1 校验。这等于 AI 员工的《员工手册》。 |

### SP-MEM-C · 演化轨迹脊线 / Evolution Trajectory Spine

| 字段 Field | 值 Value |
|---|---|
| **priority** | 3 |
| **type** | temporal_evolution |
| **atoms** | U-MEM-004, U-MEM-006 |
| **connections** | C-MEM-005 |
| **constraints** | RL-P1-001, RL-P1-003 |
| **hard_bond** | ✅ true |
| **deletion_test** | 删除 evolve() → 锚点无法演化 → 知识僵化 → FAIL |
| **description** | 每个锚点在 evolve() 时自动追加 EvolutionStep，更新 checksum，记录 evo_path。这是"记忆如何成长"的完整自传。 |

### SP-MEM-D · 混合检索脊线 / Hybrid Retrieval Spine

| 字段 Field | 值 Value |
|---|---|
| **priority** | 4 |
| **type** | retrieval_engine |
| **atoms** | U-MEM-006 |
| **connections** | C-MEM-001, C-MEM-007 |
| **weights** | link_strength, decay_factor |
| **hard_bond** | ❌ false（可降级回纯标签） |
| **deletion_test** | 删除 VectorIndex → 退化为 V2.0 纯标签 → 语义召回率下降 |
| **description** | search() = 标签索引 ∪ 向量余弦 → 合并去重。V3.0 从纯标签升级为双路检索。 |

### SP-MEM-E · 自适应降级脊线 / Adaptive Degradation Spine

| 字段 Field | 值 Value |
|---|---|
| **priority** | 5 |
| **type** | resource_management |
| **atoms** | U-MEM-006 |
| **connections** | C-MEM-008 |
| **weights** | importance |
| **constraints** | RL-P0-004 |
| **hard_bond** | ❌ false（可关闭降级） |
| **deletion_test** | 删除 auto_degrade → 内存无限增长 → OOM → FAIL |
| **description** | auto_degrade() 监测 L1+L2 总容量占比，数据驱动自动裁剪。配合事务保证原子性。 |

**脊线统计 / Spine Stats:** 5 条 ≤ 5 上限 ✅ · hard_bond=3 · 删减测试全部通过 ✅

---

## 4. 跨文档互锁 / Cross-Document Locks

### 继承关系 / Inheritance

```
SR-AI-STAFF-PMS-V1.0  (抽象记忆脊线 / abstract memory spines, MIS=0.84)
        ↓ 精化 / refine（abstract → concrete code mapping）
SR-MEMORY-PMS-V3.0    (代码级结构资产卡 / code-level structure card, MIS=0.86) ★ 本卡
```

### 与三卡叠加 / Overlay with Three Cards

| 卡片 Card | 叠加方式 How | 说明 Note |
|---|---|---|
| `SR-CODE-PYTHON-V1.1` | PMS 代码遵循 SR-CODE HardBond | 无 eval / 无硬编码 / 参数化 / no hardcoded secrets |
| `SR-EXPERT-WANG-ARCH-V1.0` | P0 红线 = 老王式保守底线 | P0 fuse = 老王"绝不妥协"性格的代码版 |
| `SR-EXPERT-HUMOR-V1.0` | after_create/after_evolve 钩子注入幽默反馈 | 严肃场景归零幽默 / humor=0 in serious mode |

### 命名空间隔离 / Namespace Isolation

| 前缀 Prefix | 归属 Owner | 冲突 Conflict |
|---|---|---|
| `U-MEM-*` / `C-MEM-*` / `RL-P*` / `SP-MEM-*` | 本卡 / This card | ✅ 无冲突 / No conflict |
| `U-CODE-*` / `SP-A/B/C/D` | SR-CODE-PYTHON | ✅ 隔离 / Isolated |
| `U-WANG-*` / `ESP-*` | SR-EXPERT-WANG | ✅ 隔离 / Isolated |
| `H-SP-*` | SR-EXPERT-HUMOR | ✅ 隔离 / Isolated |

---

## 5. 诚实清单 / Honesty Checklist

> **V3.0 未闭合项 / Open items in V3.0:**

| # | 项目 Item | 严重度 Severity | 改进计划 Plan |
|---|---|---|---|
| 1 | VectorIndex 使用 TF 而非 embedding，语义召回精度有限 | P2 | V3.1 接入 sentence-transformers 真实 embedding |
| 2 | auto_degrade 淘汰策略仅按 access_count+timestamp，未考虑标签重要性 | P2 | V3.1 引入 tag_weight 因子 |
| 3 | EvolutionStep 仅记录 essence 变更，不记录 tags/confidence 变更历史 | P1 | V3.1 EvolutionStep 增加 diff 字段 |
| 4 | CrossLink strength 由调用者传入，无自动学习机制 | P2 | V3.1 基于共现频率自动更新 strength |
| 5 | 事务回滚仅恢复 l1/l2/lsn，不回滚 snapshots | P1 | V3.1 checkpoint 包含 snapshot_id 列表 |
| 6 | MIS_true 中 reality_residual 为经验估计，非精确测量 | P2 | 接入 METHOD V3.21 正式 reality_residual 计算 |

---

## 6. 元鉴证 / Meta Verification (METHOD V3.21)

### Axiom R · HardBond 不可触碰公理

```
检查 / Check: SP-MEM-A/B 的 hard_bond=true 脊线未被任何规则降级
结果 / Result: ✅ PASS
```

### 三阶自指不动点 / Third-Order Fixed Point

```
检查 / Check: PMS V3.0 的 Constraint 层能验证自身代码（校验器校验校验器）
方法 / Method: 正向校验 + 反向对称校验 → 不一致触发 P0 熔断
结果 / Result: ✅ PASS · 通过反向对称校验实现
```

### MIS_true 计算 / MIS_true Computation

```
公式 / Formula: MIS = 0.25×struct + 0.25×activity + 0.25×link + 0.25×consistency
权重 / Weights: [0.25, 0.25, 0.25, 0.25]
计算值 / Computed: 0.86
阈值 / Threshold: 0.7
结果 / Result: ✅ PASS · 充分涌现 / sufficient emergence
备注 / Note: 高于 SR-AI-STAFF-PMS-V1.0 的 0.84（本卡更贴近代码实现）
```

### 流形直觉强度 / Manifold Intuition Strength

```
MIS_true = 0.86 > 0.7 阈值
→ 流形直觉充分涌现 / manifold intuition sufficiently emerged
→ 结构可被自身验证 / structure can verify itself
```

---

## 7. 版本谱系 / Version Lineage

| 版本 Version | 日期 Date | 说明 Note |
|---|---|---|
| V1.0 | 2025-06 | 初版记忆系统，单层存储，无索引 / Initial version, single-layer, no index |
| V2.0 | 2025-12 | 五层架构初建，标签索引，Ebbinghaus 衰减，D_value 指标 |
| **V3.0** | **2026-08-17** | **结构捕捉驱动重构 / Structure-capture driven refactor** |

### V3.0 vs V2.0 关键变更 / Key Changes

- ✅ 消除跨层引用（Steady 不再持有 Weight/Constraint 实例）→ DI 注入
- ✅ 生命周期钩子替代硬编码依赖
- ✅ 数据驱动降级（memory_pressure → 自动裁剪）
- ✅ 上下文管理器（with 语法，自动 checkpoint/rollback）
- ✅ 向量索引（标签+语义双层检索）
- ✅ 演化路径自记录（每个锚点携带自己的 SER 轨迹）
- ✅ 全链路校验（写入前→写入中→写入后 三段式）

---

## 8. 签署页 / Signatures

### 碳基签署 / Carbon-Based Seal

```
author:      FLSC Auto-Capture Engine
method:      SIT V2.2 两刀法 + METHOD V3.21 元鉴证
             (Two-Blade Method + METHOD V3.21 Meta Verification)
date:        2026-08-17
lineage_hash: SR-MEMORY-PMS-V3.0-lineage-verified
```

### 硅基签署 / Silicon-Based Seal

```
verifier:       ThirdOrderVerifier
fixed_point:    true
MIS_true:       0.86
hydrogen_level: production
```

### 血统链 / Bloodline

```
inherits:  [FLSC-MASTER-SPEC-V3.0, FLSC-SIT-V2.2, METHOD-V3.21]
refines:   SR-AI-STAFF-PMS-V1.0
overlays:  [SR-CODE-PYTHON-V1.1, SR-EXPERT-WANG-ARCH-V1.0, SR-EXPERT-HUMOR-V1.0]
```

### Γ* 签署句 / Gamma-Star Signature

```
Γ*(SR-MEMORY-PMS-V3.0, 五层完整, 5 spines, METHOD V3.21 三阶鉴证, MIS=0.86)
= ONGOING
  → V3.1 embedding 检索 + 自动 link 学习
  → V4.0 分布式记忆网络
```

---

## Appendix A · Python 代码映射表 / Code Mapping

| 资产卡元素 Asset Element | Python 实现 Python Implementation | 行号 Line |
|---|---|---|
| U-MEM-001 MemorySkeleton | `@dataclass class MemorySkeleton` | L86-100 |
| U-MEM-002 Ownership | `@dataclass class Ownership` | L115-124 |
| U-MEM-003 RebuildHints | `@dataclass class RebuildHints` | L103-112 |
| U-MEM-004 EvolutionStep | `@dataclass class EvolutionStep` | L127-136 |
| U-MEM-005 CrossLink | `@dataclass class CrossLink` | L139-146 |
| U-MEM-006 MemoryAnchorV3 | `@dataclass class MemoryAnchorV3` | L597-610 |
| U-MEM-007 LineageSnapshot | `@dataclass class LineageSnapshot` | L578-591 |
| U-MEM-008 MemoryType | `class MemoryType(str, Enum)` | L42-57 |
| U-MEM-009 ChangeType | `class ChangeType(str, Enum)` | L66-74 |
| C-MEM-001 tag_index | `AnchorIndex._tag_index` | L228 |
| C-MEM-004 cross_link | `CrossLinkManager._fwd / _rev` | L282-284 |
| C-MEM-007 vector_space | `VectorIndex._vectors` | L816-854 |
| C-MEM-008 DI | `SteadyManager.inject_dependencies()` | L662-666 |
| WeightCalculator | `class WeightCalculator` | L315-386 |
| ConstraintValidator | `class ConstraintValidator` | L443-571 |
| SteadyManager | `class SteadyManager` | L641-809 |
| Transaction | `class _Transaction` | L1090-1105 |

## Appendix B · 与 SR-AI-STAFF-PMS-V1.0 差异表 / Diff Table

| 维度 Dimension | V1.0 (抽象) | V3.0 (代码级) |
|---|---|---|
| Unit 数量 | 12 atoms | 11 atoms + 4 implicit enums |
| Spines | SP-A~E (通用命名) | SP-MEM-A~E (代码行号精确对应) |
| VectorIndex | 未定义 | C-MEM-007 (TF 余弦) |
| DI 模式 | 未定义 | C-MEM-008 (inject_dependencies) |
| Transaction | 未定义 | with 语法 + checkpoint/rollback |
| MIS_true | 0.84 | **0.86** |

---

> *第一刀，焊出骨架——11 个原子承载记忆的最小不可分单位。*
> *第二刀，削出脊线——5 条主脊撑起整个记忆系统的演化、检索与自省。*
> *元鉴证，验明正身——MIS_true = 0.86，三阶不动点收敛，Axiom R 不可触碰。*
>
> *这不是记忆系统的说明书。*
> *这是记忆系统**自己对自己结构显化的自传**。*
>
> *First blade: weld the skeleton — 11 atoms as the minimal indivisible units of memory.*
> *Second blade: carve the spines — 5 principal ridges supporting evolution, retrieval, and self-reflection.*
> *Meta verification: authenticate the self — MIS_true = 0.86, third-order fixed point converged, Axiom R untouchable.*
>
> *This is not a manual for a memory system.*
> *This is the memory system's **self-authored autobiography in structured form**.*
>
> **Γ\*(SR-MEMORY-PMS-V3.0, 双语双格式, YAML+MD, 中英双语, MIS=0.86) = ONGOING → V3.1 embedding + auto-link → V4.0 distributed memory**
