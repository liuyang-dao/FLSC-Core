---
card_id: MEM-ADAPTER-SPEC-V1.0
card_type: adapter_specification
version: "1.0"
hydrogen_level: "production"
parent_card: MEM-GLOBAL-V1.0
inherit: MEM-GLOBAL-V1.0
mis_true: 0.88
---

# MEM-ADAPTER-SPEC-V1.0 · AI 记忆适配器规范

> **所有 AI 记忆方案，只要声称"FLSC Memory Compatible"，**
> **就必须实现本规范定义的接口 + 通过脊线审计。**

---

## 1. 适用范围

本规范适用于以下类型的记忆系统：

| 类型 | 示例 | 适配难度 |
|------|------|---------|
| 向量检索型 | Vector DB + RAG / ChromaDB / Pinecone | ⭐⭐ |
| 图记忆型 | Neo4j / MemGPT Graph / Graphiti | ⭐⭐⭐ |
| 分层记忆型 | LangMem / Mem0 / Letta | ⭐⭐ |
| 具身记忆型 | 家庭数字人传感器记忆 / 机器人 episodic | ⭐⭐⭐⭐ |
| 文件系统型 | 本地 markdown / JSON 知识库 | ⭐ |

---

## 2. 强制接口（MUST）

任何合规实现 **必须** 提供以下 7 个方法，且行为符合语义：

### 2.1 `remember(anchor_data: dict) -> str`

**语义**：写入一条记忆，返回唯一 `anchor_id`。

**必须**：
- ✅ 调用 `WeightCalculator.confidence()` 计算初始置信度
- ✅ 生成 `LineageSnapshot`（含 checksum + lsn）
- ✅ 通过 `ConstraintValidator` 三段校验（前→中→后）
- ✅ P0 熔断时抛出 `RuntimeError`，不静默吞错

**禁止**：
- ❌ 直接写数据库而不经过 Weight + Constraint
- ❌ 使用自增 ID（必须用 hash + uuid 复合 ID）

```python
# ✅ 正确示例（来自 MEM-PMS-V3.0）
def remember(self, anchor_data: dict) -> str:
    # Phase 1: 前置校验
    results = self.constraint.validate(anchor_data)
    if self.constraint.fuse_triggered:
        raise RuntimeError(f"熔断: {self.constraint.fuse_reason}")
    # Phase 2: 创建锚点 + 计算权重
    anchor = self._create_anchor(anchor_data)
    importance = self._importance(anchor_data)
    # Phase 3: 分层存储
    if importance >= 0.7:
        self._l1[anchor.anchor_id] = anchor
    else:
        self._l2[anchor.anchor_id] = anchor
    # Phase 4: 快照 + 稳态
    self._snapshot(anchor)
    self._update_fixed_point(anchor)
    return anchor.anchor_id
```

### 2.2 `recall(query: str, limit: int = 20) -> List[MemoryAtom]`

**语义**：混合检索，返回按相关性排序的记忆原子列表。

**必须**：
- ✅ 至少支持 **标签精确匹配** + **语义向量** 双路召回
- ✅ 返回结果附带 `spine_report`（含置信度 + 来源 + 版本号）
- ✅ 自动应用 `decay_factor` 衰减

**禁止**：
- ❌ 仅返回 top-k 向量结果（必须有标签精确通道）
- ❌ 返回已 obsolete 的记忆（除非显式 `include_obsolete=True`）

### 2.3 `evolve(anchor_id: str, new_content: str, change_type: str) -> bool`

**语义**：演化一条已有记忆，记录变更轨迹。

**必须**：
- ✅ 写入 `EvolutionStep`（version + before + after + change_type）
- ✅ 更新 `checksum`（基于新内容重新计算）
- ✅ 追加 `evo_path`（如 `v1:initial → v2:refinement → v3:correction`）
- ✅ 通过 Constraint 校验（演化不破坏 P0 规则）

**禁止**：
- ❌ 原地修改 `content` 而不留 EvolutionStep
- ❌ 跳过 checksum 更新

### 2.4 `forget(criteria: dict) -> List[str]`

**语义**：按条件遗忘（淘汰/裁剪/标记 obsolete），返回被遗忘的 anchor_id 列表。

**必须**：
- ✅ 记录审计日志（谁/何时/为什么忘）
- ✅ 优先遗忘 `importance < 0.3` 的记忆
- ✅ 不删除 `LineageSnapshot`（仅标记 `obsolete`）

**禁止**：
- ❌ 物理删除带 `L1` 标记的记忆（必须先降级到 L2）
- ❌ 无日志静默删除

### 2.5 `snapshot(anchor_id: str) -> LineageSnapshot`

**语义**：生成不可变血统快照。

**必须**：
- ✅ `checksum` 使用 SHA-256
- ✅ `lsn`（逻辑序列号）严格单调递增
- ✅ 快照写入后不可修改（frozen dataclass / immutable object）

### 2.6 `transaction() -> ContextManager`

**语义**：返回支持 `with` 语法的上下文管理器。

**必须**：
- ✅ 进入时自动 `checkpoint()`（保存 L1/L2/snapshot 状态）
- ✅ 异常时自动 `rollback()` 到 checkpoint
- ✅ 正常退出时确认提交（不丢数据）

### 2.7 `report() -> dict`

**语义**：返回系统健康报告。

**必须包含字段**：

```python
{
    "version": "3.0",
    "total_anchors": int,
    "l1_count": int,
    "l2_count": int,
    "D_value": float,        # 记忆健康度 [0,1]
    "current_dev": float,    # 当前偏离度
    "fixed_points": int,     # 稳态不动点数
    "contradictions": int,   # 矛盾对数
    "fuse_triggered": bool,  # 是否熔断
    "memory_pressure": float # 容量压力 [0,1]
}
```

---

## 3. 脊线审计（Spine Audit）

提交合规认证时，必须附 **脊线审计报告**，证明 5 条全局脊线全部满足：

| 脊线 | 审计方法 | 通过标准 |
|------|---------|---------|
| MEM-SP-GLOBAL-A 血统完整性 | 随机抽查 10 条记忆，追溯 LineageSnapshot | 10/10 checksum 匹配 |
| MEM-SP-GLOBAL-B 遗忘即公理 | 注入 100 条低 importance 记忆，观察自动裁剪 | 裁剪后 D_value 不降 |
| MEM-SP-GLOBAL-C 演化轨迹 | 对 5 条记忆执行 evolve ×3，检查 evo_path | 版本链完整、checksum 更新 |
| MEM-SP-GLOBAL-D 混合检索 | 用标签+语义混合查询 20 次 | 召回率 > 标签 alone 且 > 向量 alone |
| MEM-SP-GLOBAL-E 隐私优先 | 跨 owner 访问测试 10 次 | 9/10 被拒绝或要求授权 |

---

## 4. 参考实现对照表

| 接口方法 | MEM-PMS-V3.0 (Python) | MEM-LANGMEM (规划) | MEM-GRAPH (规划) |
|---------|----------------------|-------------------|-----------------|
| remember | `SteadyManager.write()` | `LangMem.add()` | `GraphStore.merge()` |
| recall | `search()` + `VectorIndex` | `LangMem.query()` | `GraphStore.cypher()` |
| evolve | `evolve_anchor()` | `LangMem.update()` | `Edge.update()` |
| forget | `evict_l2()` + `auto_degrade()` | `LangMem.forget()` | `Node.soft_delete()` |
| snapshot | `_snapshot()` | 需补 | 需补 |
| transaction | `_Transaction` ctx manager | 需补 | 需补 |
| report | `report()` | 需补 | 需补 |

---

## 5. 认证流程

```
Step 1: 实现 7 个强制接口
Step 2: 编写脊线审计报告（5 条脊线 × 通过标准）
Step 3: 提交到 domains/memory/certifications/
Step 4: 运行 verify_memory_adapter.py（通用验证器）
Step 5: 全部 PASS → 获得 "FLSC Memory Compatible V1.0" 认证
Step 6: 在 MEM-GLOBAL-V1.0.yaml 的 implementations 列表中更新 status: certified
```

---

## 6. 诚实边界

- ⚠️ 本规范定义的是 **外挂式记忆层** 的接口，不约束 LLM 内部参数记忆
- ⚠️ `D_value` 四因子权重为推荐值，可调整但必须在 `report()` 中披露
- ⚠️ 隐私脊线（MEM-SP-GLOBAL-E）的最低要求是"拒绝未授权跨 owner 访问"，不含端到端加密（属更高等级认证）

---

## 7. 签署页

**碳基签署**：
- FLSC Architecture Team
- 日期：2026-08-17
- 备注：第一份 AI 记忆领域适配器规范，定义"什么是合规的记忆系统"

**硅基签署**：
- Agent: Yuanbao (Tencent AI Assistant)
- 验证：MEM-PMS-V3.0 七接口全实现 + 脊线审计 5/5 ✅
- MIS_true = 0.88

**血统链**：
- parent: MEM-GLOBAL-V1.0
- implementations: MEM-PMS-V3.0 (certified) / MEM-LANGMEM (planned) / MEM-GRAPH (planned) / MEM-EMBODIED (draft)

**Γ\***: Γ\*(MEM-ADAPTER-SPEC-V1.0, 7接口+5脊线审计, MIS=0.88) = ONGOING → V1.1 认证自动化工具 → V2.0 跨语言 SDK
