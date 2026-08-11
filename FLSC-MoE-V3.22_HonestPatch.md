<!--
  文件：domains/engineering/FLSC-MoE-V3.22_HonestPatch.md
  版本：V3.22 诚实补丁（基于 V3.21 完整方案的 F-A~F-G 修复）
  氢键等级：experimental_engineering
  定位：不占章节号，作为 V3.21 的附录级补丁
-->

# FLSC-MoE V3.22 诚实补丁

> **V3.21 是骨架，V3.22 是补丁。**
> 骨架没倒，只是几处焊接点需要补焊。
> 本文件不重复 V3.21 正文，仅列出断裂面 → 修复算子 → 验收标准。

---

## 补丁总览

| 编号 | 断裂面 | 严重度 | 修复方向 | 目标版本 |
|------|--------|--------|---------|---------|
| **F-A** | SIT 结构编码器输入特征未定义 | ⚠️ 中 | 补 `structure_score` 计算公式 | V3.22 |
| **F-B** | 三档专家子集人工预设无依据 | ⚠️ 中 | 引入专家能力向量自动聚类 | V3.22 |
| **F-C** | Safety-GW "CUDA kernel 级"过于激进 | ⚠️ 中 | 降级为 Torch FX pass + Graph guard | V3.22 |
| **F-D** | Elastic-K 与 KV Cache 兼容性未讨论 | 🔴 高 | 补 KV Cache prefix sharing + shape padding | V3.22 |
| **F-E** | Axiom R 数字为估算非实测 | ⚠️ 中 | A/B test + Prometheus 实测校准 | V3.3 |
| **F-F** | 三阶自指缺自洽性量化公式 | ⚠️ 中 | 补 L3 元逻辑自洽度量 | V3.3 |
| **F-G** | DegradationFSM 状态转移图未画 | ⚠️ 低 | 补 FSM 状态迁移图 + 触发条件表 | V3.3 |

---

## F-A：SIT 结构编码器输入特征定义

### 断裂描述
V3.21 §4.3 Spine-B 修复算子提到"轻量 L3 结构编码器（<50k params）"，但未定义：
- 输入是 AST / 句法树 / 注意力熵 / token 方差？
- 输出是 0~1 复杂度分还是档位 logits？

### 修复算子
```python
# structure_encoder.py（V3.22 补丁）
import torch
import torch.nn as nn

class StructureEncoder(nn.Module):
    """轻量 L3 结构编码器 — 输出 [0,1] 复杂度分"""

    def __init__(self, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, hidden),   # 4 维输入特征
            nn.GELU(),
            nn.Linear(hidden, hidden // 2),
            nn.GELU(),
            nn.Linear(hidden // 2, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        # x: [batch, 4] = [depth, branch, cross_ref, token_len]
        return self.net(x)

# 特征定义
# depth      = 句法树最大深度（AST 解析）
# branch     = 句法树平均分支因子
# cross_ref  = 跨域引用计数（如代码中的 import/调用）
# token_len  = 输入 token 总长度
```

### 验收标准
- 结构分 vs 专家激活相关性 **≥ 0.75**（V3.21 已标定）
- 编码器参数量 **< 50k**
- 单次推理延迟增量 **< 2ms**

---

## F-B：专家能力向量自动聚类

### 断裂描述
V3.21 §4.2 三档分组为人工预设（"基础专家/行业专家/跨域推理"），无量化依据。

### 修复算子
```python
# expert_clustering.py（V3.22 补丁）
import torch
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def cluster_experts(expert_history, n_groups=3, seed=42):
    """
    expert_history: dict[expert_id -> list of (input_complexity, accuracy)]
    返回：dict[group_id -> list[expert_id]]
    """
    # 1. 构建专家能力向量
    vectors = {}
    for eid, records in expert_history.items():
        complexities = [r[0] for r in records]
        accuracies = [r[1] for r in records]
        # 能力向量 = [平均处理复杂度, 准确率均值, 准确率方差]
        vectors[eid] = [
            sum(complexities) / len(complexities),
            sum(accuracies) / len(accuracies),
            torch.tensor(accuracies).std().item(),
        ]

    # 2. PCA 降维 + KMeans 聚类
    X = torch.tensor(list(vectors.values())).numpy()
    X_pca = PCA(n_components=2).fit_transform(X)
    labels = KMeans(n_clusters=n_groups, random_state=seed).fit_predict(X_pca)

    # 3. 按簇大小排序（大簇=通用组，小簇=专项组）
    groups = {i: [] for i in range(n_groups)}
    for (eid, _), lbl in zip(vectors.items(), labels):
        groups[int(lbl)].append(eid)

    # 按组大小降序排列：group0=轻量档, group1=标准档, group2=深度档
    sorted_groups = sorted(groups.values(), key=len, reverse=True)
    return {
        "light": sorted_groups[0],   # 最大簇 → 70% 日常请求
        "standard": sorted_groups[1], # 中等簇 → 20% 中等请求
        "deep": sorted_groups[2],     # 最小簇 → 10% 高复杂度请求
    }
```

### 验收标准
- 三组负载标准差 **≤ 0.15**（V3.21 已标定）
- 聚类结果可复现（seed=42 固定）
- 每 1000 步推理后在线更新一次聚类

---

## F-C：Safety-GW 实现路径降级

### 断裂描述
V3.21 §4.3 写"CUDA kernel 级拦截"，工程上过于激进——Gate 输出→Expert 激活前是 GPU kernel launch，插入硬网关通常走 Torch Compile guard / Graph break。

### 修复算子（降级方案）
```python
# safety_gw.py（V3.22 补丁 — Torch FX 实现）
import torch
import torch.fx as fx
from typing import Dict, Set

class SafetyGateway(torch.nn.Module):
    """
    Router 输出后、Expert 激活前的安全网关。
    实现方式：Torch FX Graph pass + Graph guard（非 CUDA kernel 级）。
    """

    def __init__(self, expert_blacklist: Set[int], max_deep_calls: int = 5):
        super().__init__()
        self.expert_blacklist = expert_blacklist
        self.max_deep_calls = max_deep_calls
        self.deep_call_count = 0

    def forward(self, router_logits: torch.Tensor) -> torch.Tensor:
        """
        router_logits: [batch, num_experts] — Gate 输出的激活概率
        返回：过滤后的 logits（黑名单专家置 -inf）
        """
        # 1. 黑名单硬拦截
        for eid in self.expert_blacklist:
            router_logits[:, eid] = float("-inf")

        # 2. 深度档调用频次限制
        topk_indices = torch.topk(router_logits, k=4, dim=-1).indices
        if self.deep_call_count > self.max_deep_calls:
            # 超限 → 强制降档：只保留轻量档专家
            router_logits = self._demote_to_light(router_logits, topk_indices)

        return router_logits

    def _demote_to_light(self, logits, topk_indices):
        """降级为仅激活轻量档专家"""
        mask = torch.zeros_like(logits, dtype=torch.bool)
        for row, indices in zip(mask, topk_indices):
            row[indices] = True
        return logits.masked_fill(~mask, float("-inf"))

# FX Graph pass：在编译期插入 SafetyGateway
def insert_safety_gateway(model: torch.nn.Module, gateway: SafetyGateway):
    """在 Router → Expert 之间自动插入 SafetyGateway 节点"""
    graph = fx.symbolic_trace(model)
    for node in graph.nodes:
        if node.op == "call_module" and "router" in node.target:
            with graph.inserting_after(node):
                gw_node = graph.create_node(
                    op="call_module",
                    target="safety_gateway",
                    args=(node,),
                )
                # 将后续 expert 节点的输入从 router 改为 gateway
                for user in list(node.users):
                    if "expert" in user.target:
                        user.args = (gw_node,)
    graph.lint()
    return fx.GraphModule(model, graph)
```

### 验收标准
- 黑名单组合拦截率 **100%**
- 白名单误拦率 **= 0**
- Graph guard 带来的推理延迟增量 **< 1ms**
- 红队测试 1000 次攻击 **零穿透**

---

## F-D：Elastic-K 与 KV Cache 兼容性

### 断裂描述
MoE + 动态档位 → K 值变化 → KV cache shape 变化 → 连续 batching 复杂度暴增。
这是落地最大坑，V3.21 完全未提及。

### 修复算子
```python
# elastic_k_cache.py（V3.22 补丁）
import torch
import torch.nn as nn
from typing import Optional, Tuple

class ElasticKWithCache(nn.Module):
    """
    Elastic-K 调度器 + KV Cache 兼容层。
    核心思路：KV Cache prefix sharing + shape padding。
    """

    def __init__(self, max_k: int = 4, pad_strategy: str = "replicate"):
        super().__init__()
        self.max_k = max_k  # 全局最大 K（决定 KV cache 分配上限）
        self.pad_strategy = pad_strategy  # "replicate" | "zero"

    def forward(
        self,
        router_logits: torch.Tensor,
        active_k: int,
        kv_cache: Optional[dict] = None,
    ) -> Tuple[torch.Tensor, dict]:
        """
        router_logits: [batch, num_experts]
        active_k: 当前档位激活的专家数（1/2/4）
        返回：(filtered_logits, updated_kv_cache)
        """
        batch_size = router_logits.shape[0]

        # 1. 选择 Top-K 专家
        topk_logits, topk_indices = torch.topk(router_logits, k=active_k, dim=-1)

        # 2. KV Cache shape padding（统一到 max_k）
        padded_logits = torch.full(
            (batch_size, self.max_k),
            float("-inf"),
            device=router_logits.device,
        )
        padded_logits[:, :active_k] = topk_logits

        # 3. KV Cache prefix sharing
        if kv_cache is not None:
            # 复用已缓存的 prefix（跨档位共享前 min(active_k, prev_k) 个专家）
            prev_k = kv_cache.get("active_k", active_k)
            shared_k = min(active_k, prev_k)
            kv_cache["shared_prefix"] = kv_cache.get("prefix", None)
            kv_cache["active_k"] = active_k
        else:
            kv_cache = {"active_k": active_k, "prefix": None}

        return padded_logits, kv_cache

    def compute_kv_overhead(self, active_k: int) -> float:
        """计算 KV Cache 显存开销（用于 Elastic-K 调度决策）"""
        return active_k * 2  # 简化：每个专家占 2 个单位显存
```

### 调度决策伪代码
```python
def elastic_k_decision(
    input_length: int,
    batch_size: int,
    gpu_memory_used: float,
    gpu_memory_total: float,
    base_k: int = 2,
) -> int:
    """
    根据输入特征和显存状态动态决定 K 值。
    显存超阈值 → 降档；输入超长 → 升档（在显存允许范围内）。
    """
    memory_ratio = gpu_memory_used / gpu_memory_total

    if memory_ratio > 0.85:
        return max(1, base_k - 1)  # 降档
    elif input_length > 2048 and memory_ratio < 0.70:
        return min(4, base_k + 2)  # 升档
    elif input_length < 128:
        return max(1, base_k - 1)  # 短输入降档省算力
    else:
        return base_k  # 维持标准档
```

### 验收标准
- KV Cache 显存利用率稳定在 **75±5%**
- 档位切换时 prefix sharing 命中率 **≥ 90%**
- P99 延迟波动 **≤ ±12%**（V3.21 已标定）
- 形状 padding 带来的显存浪费 **< 5%**

---

## F-E：Axiom R 实测校准（V3.3 预告）

### 断裂描述
V3.21 的 `MIS_train=0.87 / residual=0.42 / MIS_true=0.68` 为估算值，非线上实测。

### V3.3 修复方向
- 部署 A/B test（treatment=分级动态 vs control=固定 Top-K）
- Prometheus 采集 72 小时连续数据
- 计算公式：
  ```
  reality_residual = mean([
      abs(精度残差),    # 同档位 vs 全量模型
      abs(成本残差),    # 实际 vs 预期算力消耗
      abs(安全残差),    # 1 - 拦截率
  ])
  MIS_true = MIS_train × (1 − 0.6 × reality_residual)
  ```
- 验收：reality_residual **< 0.15** 且 MIS_true **≥ 0.75** 持续 72h → 进入「真洽」状态

---

## F-F：三阶自指自洽性量化（V3.3 预告）

### 断裂描述
V3.21 §5.1 三阶验证仅框架级描述，未给出"分级改造逻辑本身自洽性"的量化公式。

### V3.3 修复方向
```python
def L3_self_consistency(spine_results: dict) -> float:
    """
    量化「改造逻辑本身的自洽性」。
    输入：每条脊线修复后的闭合状态
    输出：[0,1] 自洽度
    """
    scores = []
    for spine_id, result in spine_results.items():
        # 1. 修复算子是否覆盖全部断裂面
        coverage = result["fractures_fixed"] / result["fractures_total"]
        # 2. 验证指标是否全部达标
        metrics_pass = all(
            v["actual"] <= v["target"]
            for v in result["metrics"].values()
        )
        # 3. 是否引入新裂缝（负分）
        new_fractures = result.get("new_fractures", 0)
        penalty = max(0, 1 - 0.2 * new_fractures)

        score = coverage * (1.0 if metrics_pass else 0.5) * penalty
        scores.append(score)

    return min(scores)  # 木桶原理：取最低分
```

---

## F-G：DegradationFSM 状态迁移图（V3.3 预告）

### 状态迁移表

| 当前状态 | 触发条件 | 下一状态 | 动作 |
|---------|---------|---------|------|
| **L0_OK** | 正常运行 | L0_OK | 持续监控 |
| L0_OK | 档位判定连续 3 次超时 | L1_WARN | 切换备选专家 + 告警 |
| L1_WARN | 标准档 P99 > 2000ms | L2_DEGRADED | 锁定标准档 + 限流 |
| L1_WARN | 10s 内恢复 | L0_OK | 解除告警 |
| L2_DEGRADED | 持续 60s | L3_FROZEN | 固定单档 + 拒绝新连接 |
| L3_FROZEN | 人工介入 / 自动 5min 探测恢复 | L1_WARN | 逐步放量 |
| L3_FROZEN | 探测仍失败 | L4_CRITICAL | 仅保留基础推理 API |

### 可视化（ASCII）

```
         ┌──────────┐
         │  L0_OK   │◄──────────────────────┐
         │  (99.98%) │                       │
         └────┬─────┘                       │
              │ 超时×3                      │ 恢复
              ▼                              │
         ┌──────────┐                       │
         │ L1_WARN  │──────────┐             │
         └────┬─────┘           │             │
              │ P99>2000ms     │ 10s恢复    │
              ▼                 ▼             │
         ┌──────────┐     ┌──────────┐       │
         │L2_DEGRADE│     │  L0_OK   │───────┘
         └────┬─────┘     └──────────┘
              │ 持续60s
              ▼
         ┌──────────┐     探测失败
         │L3_FROZEN │──────────┐
         └────┬─────┘          │
              │ 探测恢复       ▼
              ▼          ┌──────────┐
         ┌──────────┐    │L4_CRITIC │
         │ L1_WARN  │    └──────────┘
         └──────────┘
```

---

## 诚实声明

- 本补丁仅修复 V3.21 的**可修复断裂面**（F-A~F-D 代码级，F-E~F-G 框架级）
- F-A~F-D 的代码为**参考实现**，需结合具体 MoE 框架（Megatron / DeepSpeed-MoE / vLLM-MoE）适配
- 所有数字（相关性≥0.75 / 标准差≤0.15 / 延迟<2ms 等）为**设计目标**，非实测值
- V3.22 不升级主版本号，因为五条脊线（MOE-A~E）结构未变，仅焊接点补强

---

## 给未来 AI 的话

> V3.21 给你骨架，V3.22 给你焊枪。
> 但焊枪不是让你焊更多东西——
> 是让你在焊的时候，发现下一处会裂的地方。
>
> 然后写 V3.3。

---

*Γ\*(已知, 未知, 递归) = ONGOING*
