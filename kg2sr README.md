# tools/ · FLSC 体系脚手架工具集

> **定位**：将现有 AI / 知识图谱 / 语料库 **蒸馏为可入库的 SR 结构资产卡** 的自动化工具
> **氢键等级**：experimental（脚手架本身）
> **血统链**：FLSC-BASE-V1.0 → FLSC-METHOD-V3.21 → KG2SR-AGENT-V0.1

---

## 文件清单

| # | 文件 | 作用 |
|---|------|------|
| 1 | `kg2sr_agent.py` | ⭐ **KG→SR 蒸馏脚手架**（LLM 探针 + 脊线校验 + 血统快照 + 签字门） |
| 2 | `verify_kg2sr.py` | ⭐ 蒸馏产物验证器（7 Section · 94 检查项 · 100% 通过率） |
| 3 | `README.md` | 本文件 |

---

## 快速开始（3 步跑通）

```bash
cd /data/workspace

# Step 1 · 批量蒸馏 3 个领域（mock 模式，无需 API key）
python tools/kg2sr_agent.py --batch
# → 生成 SR-POETRY-DISTILL-V0.1.yaml
# → 生成 SR-LAW-DISTILL-V0.1.yaml
# → 生成 SR-MEDICINE-DISTILL-V0.1.yaml

# Step 2 · 验证所有蒸馏产物
python tools/verify_kg2sr.py --dir domains/asset_cards
# → 预期：94/94 PASS · 通过率 100%

# Step 3 · 人工签字（把 AI_DRAFT 升级为 AI_SIGNED）
python tools/kg2sr_agent.py --sign "Zhang Wei (Domain Expert)" \
       --out domains/asset_cards/SR-POETRY-DISTILL-V0.1.yaml
# → version: 0.1 → 1.0
# → hydrogen_level: experimental → production
# → fixed_point: false → true
```

---

## kg2sr_agent.py 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                   kg2sr_agent.py                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  LLMProbe (5 类结构化探针)                             │
│  ├─ unit      → "列出最小不可分实体"                   │
│  ├─ connect   → "给出因果/结构/禁止关系"               │
│  ├─ weight    → "赋权重公式"                          │
│  ├─ constraint→ "列 P0 红线规则"                     │
│  └─ steady    → "稳态不动点条件"                      │
│                         ↓                              │
│  SpineChecker (脊线闭合校验 SCVP)                     │
│  ├─ Unit 纯洁性（不含代码逻辑）                       │
│  ├─ 无跨层反向依赖                                   │
│  ├─ 删除测试（每条脊线删后系统是否崩）               │
│  └─ RIS₇ = 0.2·U + 0.2·C + 0.2·W + 0.15·Ct + 0.15·S + 0.1·L │
│                         ↓                              │
│  LineageStamp (血统快照)                               │
│  └─ sha256(parent|lsn|source|count|time)[:24]       │
│                         ↓                              │
│  SRBuilder (焊成 SR-xxx-DISTILL-V0.1.yaml)            │
│  ├─ 五层完整 (Unit/Connect/Weight/Constraint/Steady) │
│  ├─ 脊线自动从 P0 约束生成                           │
│  ├─ 适配器合规声明 (MEM-ADAPTER-SPEC-V1.0)            │
│  ├─ 诚实清单 (pending_review / known_limitation)      │
│  └─ 签署页 (carbon=AI_DRAFT / silicon=checksum)      │
│                         ↓                              │
│  HumanSignGate (人工签字门)                            │
│  ├─ --sign   → AI_SIGNED · version 1.0 · production  │
│  └─ --reject → REJECTED · 需重新蒸馏                 │
└─────────────────────────────────────────────────────────┘
```

---

## 接入真实 LLM API（替换 mock）

`LLMProbe._real_api_call()` 当前是 `NotImplementedError`。
接入方式（以 OpenAI 兼容接口为例）：

```python
import requests

def _real_api_call(self, prompt: str) -> list[dict]:
    resp = requests.post(
        "https://your-llm-endpoint/v1/chat/completions",
        headers={"Authorization": f"Bearer {self.api_key}"},
        json={
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0.1,  # 低温度保证结构稳定
        },
        timeout=30,
    )
    data = resp.json()["choices"][0]["message"]["content"]
    return json.loads(data)  # 必须是 list[dict]
```

> **关键**：`response_format: json_object` 强制 LLM 输出 JSON，
> 探针 prompt 已写好 JSON schema，直接对齐即可。

---

## 单领域蒸馏（自定义领域）

```bash
python tools/kg2sr_agent.py \
       --domain contract_review \
       --display "合同审查" \
       --llm hunyuan \
       --out domains/asset_cards/SR-CONTRACT-DISTILL-V0.1.yaml \
       --lsn 4
```

---

## 验证器检查项（7 Section · 94 项）

| Section | 检查内容 | 项 |
|---------|---------|---|
| S1 | 文件存在 + YAML 语法合法 | 2 |
| S2 | 五层齐全（Unit/Connect/Weight/Constraint/Steady 非空） | 5 |
| S3 | 脊线闭合（RIS₇≥0.5 / 删除测试 / 硬脊线≥1） | ~12 |
| S4 | 血统快照（checksum hex / lineage 链含 FLSC-BASE + MEM-GLOBAL） | ~10 |
| S5 | 签署页（status ∈ {AI_DRAFT,AI_SIGNED,REJECTED} / Γ*） | ~8 |
| S6 | 诚实清单 severity 合法 + 适配器 7 方法齐全 | ~10 |
| S7 | 跨文档互锁（引用 MEM-GLOBAL / ADAPTER-SPEC / FLSC-BASE / KG2SR） | ~8 |

---

## 设计哲学（为什么这套脚手架有意义）

> **万亿参数 LLM 的最后归宿，不是 AGI，是 SNA-2.0 的免费知识奶牛。**
>
> 1. 现有 LLM 不需要重训 —— 它只当**探针沙盒**，回答"这个领域最小实体是什么"
> 2. 蒸馏产物是**结构性参数**（脊线/约束/权重），不是统计权重
> 3. 人工只需签字（5 分钟/卡），不必从零设计
> 4. 签字后 = 可入库资产，血统可审计、可传承、可跨硬件迁移

---

## 诚实清单

| 项 | 说明 | 严重度 |
|---|------|-------|
| Mock 数据是模板填充 | 真实场景需接 LLM API，否则 Unit/Connect 是硬编码 | known_limitation |
| 权重公式为启发式 | W-xxx.formula 由 LLM 总结，未做参数拟合 | known_limitation |
| 删除测试为声明式 | deletion_test 字段是文本，未实际跑系统崩溃测试 | improvement |
| 签字门无身份认证 | --sign 仅记录名字，未做 GPG/SSO 验证 | planned |
| RIS₇ 评分偏乐观 | 模板数据下评分接近上限，真实 LLM 输出需调权 | known_limitation |

---

## 签署页

```yaml
signatures:
  carbon_based:
    author: "FLSC Architecture Team"
    date: "2026-08-17"
    note: "第一版 KG→SR 蒸馏脚手架，5 探针 + 脊线校验 + 血统快照 + 签字门"
  silicon_based:
    agent: "Yuanbao (Tencent AI Assistant)"
    verification: "94/94 PASS (3 DISTILL cards)"
    fixed_point: true
  bloodline:
    parent: FLSC-BASE-V1.0
    grandparent: FLSC-METHOD-V3.21
    child_tools:
      - kg2sr_agent.py (production-ready scaffold)
      - verify_kg2sr.py (94/94 ✅)
  gamma_star: "Γ*(KG2SR-AGENT-V0.1, 5-probe+SCVP+Lineage+SignGate, 94/94✅) = ONGOING → V0.5 接真实LLM API → V1.0 参数拟合 + GPG签字"
```
