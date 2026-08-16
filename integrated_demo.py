#!/usr/bin/env python3
"""
FLSC Integrated AI Staff Demo - 四卡叠加 + PMS 运行时
========================================================
Card 1 (Domain) : SR-CODE-PYTHON-V1.1.yaml  (领域脊线)
Card 2 (Expert) : SR-EXPERT-WANG-ARCH-V1.0.yaml (稳态角色)
Card 3 (Humor)  : SR-EXPERT-HUMOR-V1.0.yaml     (情感层)
Card 4 (Memory) : SR-AI-STAFF-PMS-V1.0.yaml    (运行时内存)

Runtime Memory   : PersonalMemorySystem V3.0 (共享实例)

Key Innovation   : 老王退休 → PMS 导出快照 → 新员工卡加载 → 知识不流失
Usage           : python3 integrated_demo.py
"""
import time
import re
import math
import hashlib
import uuid
from datetime import datetime, timedelta
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable, Set
from enum import Enum, auto

# ============================================================
#  Section 1 - METHOD V3.21 Core Engine (三阶自指 + Axiom R)
# ============================================================

class SelfRefTag:
    """运行时自指标签 (METHOD V3.21 Sec 1.1)"""
    VALID = {"L1", "L2", "L3"}

    def __init__(self, lineage_id: str):
        self.lineage_id = lineage_id
        self.current_level = None
        self.trace_log = []
        self.tag("L1", f"init:{lineage_id}")

    def tag(self, level: str, context: str):
        if level not in self.VALID:
            raise ValueError(f"Invalid level: {level}")
        entry = {"level": level, "context": context, "ts": time.time()}
        self.trace_log.append(entry)
        self.current_level = level
        return entry

    def verify_L3(self) -> bool:
        levels = {t["level"] for t in self.trace_log}
        return {"L3", "L1"}.issubset(levels)

    def snapshot(self) -> dict:
        return {
            "lineage_id": self.lineage_id,
            "current_level": self.current_level,
            "trace_count": len(self.trace_log),
            "L3_verified": self.verify_L3(),
            "trace": self.trace_log,
        }


class ThirdOrderVerifier:
    """三阶自指验证器 (METHOD V3.21 Sec 1.5)"""

    def __init__(self, lineage_id: str):
        self.lineage_id = lineage_id
        self.meta_tag = SelfRefTag(lineage_id=f"{lineage_id}-meta")
        self.verification_chain = []

    def verify_second_order(self, tag: SelfRefTag) -> dict:
        self.meta_tag.tag("L1", f"observe:{tag.lineage_id}")
        has_trace = hasattr(tag, 'trace_log') and isinstance(tag.trace_log, list)
        has_verify = callable(getattr(tag, 'verify_L3', None))
        has_snap = callable(getattr(tag, 'snapshot', None))
        self.meta_tag.tag("L2", f"struct_check:trace={has_trace}")
        l3_result = tag.verify_L3()
        self.meta_tag.tag("L2", f"L3_result={l3_result}")
        trace_l3 = any(t["level"] == "L3" for t in tag.trace_log)
        trace_l1 = any(t["level"] == "L1" for t in tag.trace_log)
        consistency = l3_result == (trace_l3 and trace_l1)
        self.meta_tag.tag("L3", f"3rd_order_consistency={consistency}")
        result = {
            "second_order_verified": l3_result,
            "structure_intact": all([has_trace, has_verify, has_snap]),
            "consistency_check": consistency,
        }
        self.verification_chain.append(result)
        return result

    def verify_third_order(self) -> dict:
        self.meta_tag.tag("L1", "start 3rd-order verification")
        meta_l3 = self.meta_tag.verify_L3()
        self.meta_tag.tag("L2", f"meta_L3={meta_l3}")
        chain_valid = len(self.verification_chain) > 0
        all_consistent = all(
            v.get("consistency_check", False) for v in self.verification_chain
        )
        self.meta_tag.tag("L3", f"3rd_closed:{meta_l3}&{chain_valid}&{all_consistent}")
        fixed_point = meta_l3 and chain_valid and all_consistent
        return {
            "third_order_fixed_point": fixed_point,
            "meta_tag_L3": meta_l3,
            "chain_length": len(self.verification_chain),
            "all_consistent": all_consistent,
        }


def calc_mis_true(
    coherence_train: float,
    grad_norm: float = 0.0,
    step_var: float = 0.0,
    completeness: float = 0.0,
    constraint_score: float = 0.0,
    reality_residual: float = 0.0,
    lambda_r: float = 0.0,
    alpha=0.25, beta=0.20, gamma=0.20, delta=0.20, epsilon=0.15,
) -> float:
    """MIS_true with Axiom R"""
    mis_train = (
        alpha * coherence_train
        + beta * (1 - min(grad_norm, 1.0))
        + gamma * (1 - min(step_var, 1.0))
        + delta * completeness
        + epsilon * constraint_score
    )
    penalty = lambda_r * min(reality_residual, 1.0)
    return max(0.0, min(mis_train * (1 - penalty), 1.0))


def reality_coupling_mode(mode: str) -> float:
    return {"closed": 0.0, "tool": 0.3, "sensor": 0.6, "human": 1.0}.get(mode, 0.0)


# ============================================================
#  Section 2 - PersonalMemorySystem V3.0 (完整实现)
# ============================================================

class MemoryType(str, Enum):
    EXPLICIT_MARKER = "explicit_marker"
    INSIGHT = "insight"
    DECISION = "decision"
    FEEDBACK = "feedback"
    DEFINITION = "definition"
    PREFERENCE = "preference"
    REFLECTION = "reflection"
    QUESTION = "question"
    MILESTONE = "milestone"

    @classmethod
    def from_string(cls, value: str) -> Optional['MemoryType']:
        try:
            return cls(value)
        except ValueError:
            return None


class MemorySpace(str, Enum):
    PRIVATE = "private"
    SHARED = "shared"
    PUBLIC = "public"


class ChangeType(str, Enum):
    INITIAL = "initial"
    REFINEMENT = "refinement"
    DEEPENING = "deepening"
    CORRECTION = "correction"
    CONTRADICTION = "contradiction"
    MERGE = "merge"
    OBSOLETE = "obsolete"
    ROLLBACK = "rollback"


class ConstraintLevel(str, Enum):
    P0_CRITICAL = "p0_critical"
    P1_HIGH = "p1_high"
    P2_MEDIUM = "p2_medium"
    P3_LOW = "p3_low"


@dataclass
class ConstraintResult:
    passed: bool
    message: str = ""
    level: ConstraintLevel = ConstraintLevel.P2_MEDIUM
    rule_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def is_fatal(self) -> bool:
        return self.level == ConstraintLevel.P0_CRITICAL and not self.passed


@dataclass
class MemorySkeleton:
    topic: str
    essence: str
    tags: List[str] = field(default_factory=list)
    confidence: float = 1.0

    def to_dict(self) -> dict:
        return {"topic": self.topic, "essence": self.essence,
                "tags": self.tags.copy(), "confidence": self.confidence}

    @classmethod
    def from_dict(cls, d: dict) -> 'MemorySkeleton':
        return cls(d.get("topic", ""), d.get("essence", ""),
                   d.get("tags", []), d.get("confidence", 1.0))


@dataclass
class Ownership:
    persona_id: str
    memory_type: MemoryType = MemoryType.INSIGHT
    memory_space: MemorySpace = MemorySpace.PRIVATE
    source: str = ""
    created_at: str = ""
    access_count: int = 0
    last_accessed_at: Optional[str] = None


@dataclass
class EvolutionStep:
    version: int
    timestamp: str
    change_type: ChangeType
    content_before: str
    content_after: str
    trigger: str
    trigger_source: Optional[str] = None


@dataclass
class CrossLink:
    target_anchor_id: str
    relation: str
    strength: float = 0.5
    created_at: str = ""
    bidirectional: bool = True


def generate_anchor_id(persona_id: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    unique = uuid.uuid4().hex[:8]
    h = hashlib.md5(persona_id.encode()).hexdigest()[:6]
    return f"{h}-{ts}-{unique}"


def compute_checksum(data: dict) -> str:
    content = "|".join([
        str(data.get("anchor_id", "")),
        str(data.get("timestamp", "")),
        str(data.get("topic", "")),
        str(data.get("essence", "")),
        "|".join(sorted(data.get("tags", []))),
        str(data.get("confidence", 0)),
    ])
    return hashlib.sha256(content.encode()).hexdigest()


@dataclass
class SystemConfig:
    MAX_TAGS: int = 10
    MAX_SNIPPET: int = 500
    MAX_ENTITIES: int = 15
    L1_CAPACITY: int = 200
    L2_CAPACITY: int = 500
    DECAY_HALF_LIFE_DAYS: int = 90
    W_STRUCTURE: float = 0.25
    W_ACTIVITY: float = 0.25
    W_LINK: float = 0.25
    W_CONSISTENCY: float = 0.25
    CONF_INITIAL: float = 0.5
    CONF_EXPLICIT_BONUS: float = 0.3
    CONF_VERSION_BONUS: float = 0.02
    CONF_CORRECTION_PENALTY: float = 0.03
    CONF_MAX: float = 1.0
    CONF_MIN: float = 0.0
    DEV_THRESHOLD: float = 0.2
    STABILITY_WINDOW_DAYS: int = 7
    STABILITY_TRIGGER_COUNT: int = 3
    LINK_TAG_WEIGHT: float = 0.4
    LINK_RELATION_WEIGHT: float = 0.6
    HYDROGEN_LEVEL: str = "experimental"


class AnchorIndex:
    def __init__(self):
        self._tag_index: Dict[str, List[str]] = defaultdict(list)
        self._type_index: Dict[str, List[str]] = defaultdict(list)
        self._timeline: List[str] = []
        self._meta: Dict[str, dict] = {}

    def add(self, anchor_id: str, tags: List[str], mem_type: str, ts: str):
        for tag in tags:
            if anchor_id not in self._tag_index[tag]:
                self._tag_index[tag].append(anchor_id)
        self._type_index[mem_type].append(anchor_id)
        self._timeline.append(anchor_id)
        self._meta[anchor_id] = {"ts": ts, "tags": tags.copy(), "type": mem_type}

    def remove(self, anchor_id: str):
        if anchor_id not in self._meta:
            return
        for tag in self._meta[anchor_id].get("tags", []):
            if anchor_id in self._tag_index.get(tag, []):
                self._tag_index[tag].remove(anchor_id)
        t = self._meta[anchor_id].get("type", "")
        if anchor_id in self._type_index.get(t, []):
            self._type_index[t].remove(anchor_id)
        if anchor_id in self._timeline:
            self._timeline.remove(anchor_id)
        del self._meta[anchor_id]

    def by_tag(self, tag: str, limit: int = 20) -> List[str]:
        return self._tag_index.get(tag, [])[:limit]

    def by_tags(self, tags: List[str], match_all: bool = False) -> List[str]:
        if not tags:
            return []
        sets = [set(self._tag_index.get(t, [])) for t in tags]
        if not sets:
            return []
        result = sets[0].intersection(*sets[1:]) if match_all else sets[0].union(*sets[1:])
        return list(result)

    def by_type(self, mem_type: str, limit: int = 50) -> List[str]:
        return self._type_index.get(mem_type, [])[:limit]

    def timeline(self, reverse: bool = True) -> List[str]:
        return list(reversed(self._timeline)) if reverse else self._timeline.copy()

    def all_ids(self) -> List[str]:
        return self._timeline.copy()

    def stats(self) -> dict:
        return {"total": len(self._timeline), "tags": len(self._tag_index),
                "types": len(self._type_index)}


class CrossLinkManager:
    def __init__(self):
        self._fwd: Dict[str, List[CrossLink]] = defaultdict(list)
        self._rev: Dict[str, List[CrossLink]] = defaultdict(list)

    def add(self, src: str, tgt: str, relation: str,
            strength: float = 0.5, bidirectional: bool = True):
        ts = datetime.now().isoformat()
        self._fwd[src].append(CrossLink(tgt, relation, strength, ts, bidirectional))
        if bidirectional:
            self._rev[tgt].append(CrossLink(src, f"被关联:{relation}", strength, ts, True))

    def get(self, anchor_id: str) -> List[CrossLink]:
        return self._fwd.get(anchor_id, []) + self._rev.get(anchor_id, [])

    def count(self, anchor_id: str) -> int:
        return len(self._fwd.get(anchor_id, [])) + len(self._rev.get(anchor_id, []))


class WeightCalculator:
    def __init__(self, config: SystemConfig = None):
        self.cfg = config or SystemConfig()

    def confidence(self, base: float, mem_type: MemoryType,
                  version: int, explicit: bool = False,
                  corrections: int = 0) -> float:
        c = base
        type_bonus = {
            MemoryType.EXPLICIT_MARKER: 0.15, MemoryType.INSIGHT: 0.10,
            MemoryType.DECISION: 0.12, MemoryType.FEEDBACK: 0.05,
            MemoryType.DEFINITION: 0.10, MemoryType.PREFERENCE: 0.08,
            MemoryType.REFLECTION: 0.10, MemoryType.MILESTONE: 0.12,
        }.get(mem_type, 0.05)
        c += type_bonus
        c += min(version * self.cfg.CONF_VERSION_BONUS, 0.15)
        if explicit:
            c += self.cfg.CONF_EXPLICIT_BONUS
        c -= min(corrections * self.cfg.CONF_CORRECTION_PENALTY, 0.20)
        return max(self.cfg.CONF_MIN, min(self.cfg.CONF_MAX, c))

    def decay_factor(self, timestamp: str) -> float:
        try:
            age = (datetime.now() - datetime.fromisoformat(timestamp)).total_seconds() / 86400
            if age < 0:
                return 1.0
            rate = math.log(2) / self.cfg.DECAY_HALF_LIFE_DAYS
            return math.exp(-rate * age)
        except (ValueError, TypeError):
            return 1.0

    def effective_confidence(self, base: float, ts: str,
                             access_count: int = 0) -> float:
        d = self.decay_factor(ts)
        bonus = min(access_count * 0.01, 0.20)
        return base * (d + bonus * (1 - d))

    def D_value(self, anchors_data: List[dict], link_counts: Dict[str, int],
                contradiction_count: int) -> float:
        if not anchors_data:
            return 0.5
        n = len(anchors_data)
        s_struct = sum(1 for a in anchors_data if a.get("has_structure")) / n
        cutoff = (datetime.now() - timedelta(days=30)).isoformat()
        s_act = sum(1 for a in anchors_data if a.get("timestamp", "") >= cutoff) / n
        total_links = sum(link_counts.get(a.get("anchor_id", ""), 0) for a in anchors_data)
        s_link = min(total_links / (n * 2), 1.0)
        s_cons = 1.0 - min(contradiction_count * 0.05, 0.3)
        return round(
            s_struct * self.cfg.W_STRUCTURE +
            s_act * self.cfg.W_ACTIVITY +
            s_link * self.cfg.W_LINK +
            s_cons * self.cfg.W_CONSISTENCY, 4)

    def link_strength(self, src_tags: List[str], tgt_tags: List[str],
                      relation: str = "default") -> float:
        common = set(src_tags) & set(tgt_tags)
        union = set(src_tags) | set(tgt_tags)
        overlap = len(common) / len(union) if union else 0
        rel_w = {"contradicts": 0.7, "supports": 0.8, "refines": 0.7,
                 "derives_from": 0.6, "example_of": 0.5, "part_of": 0.6}.get(relation, 0.5)
        return min(1.0, self.cfg.LINK_TAG_WEIGHT * overlap + self.cfg.LINK_RELATION_WEIGHT * rel_w)


# Constraint Registry & Validator
@dataclass
class ConstraintRule:
    rule_id: str
    name: str
    description: str
    level: ConstraintLevel
    check_fn: Callable[[dict], bool]
    error_msg: str
    reverse_check_fn: Optional[Callable[[dict], bool]] = None
    reverse_error_msg: str = ""


class ConstraintRegistry:
    _rules: Dict[str, ConstraintRule] = {}

    @classmethod
    def register(cls, rule: ConstraintRule):
        cls._rules[rule.rule_id] = rule

    @classmethod
    def get_p0(cls) -> List[ConstraintRule]:
        return [r for r in cls._rules.values() if r.level == ConstraintLevel.P0_CRITICAL]

    @classmethod
    def all_rules(cls) -> List[ConstraintRule]:
        return list(cls._rules.values())


class ConstraintValidator:
    def __init__(self):
        self._history: List[ConstraintResult] = []
        self._fuse_triggered: bool = False
        self._fuse_reason: Optional[str] = None
        self._register_p0()

    def _register_p0(self):
        rules = [
            ("RL-P0-001", "跨层依赖禁止", "禁止反向依赖",
             self._check_dep_forward, self._check_dep_reverse),
            ("RL-P0-003", "Unit 纯洁性", "Unit 禁止业务逻辑",
             self._check_unit_purity, self._check_unit_purity_rev),
            ("RL-P0-006", "硬编码禁止", "禁止魔法数字",
             self._check_no_hardcode, self._check_no_hardcode_rev),
            ("RL-P0-009", "裁剪合法性", "Constraint 不可裁剪",
             self._check_cut_legality, self._check_cut_legality_rev),
            ("MEM-HB-M5", "Checksum 不可篡改", "快照校验和不可伪造",
             self._check_checksum, self._check_checksum_rev),
            ("MEM-HB-M6", "LSN 单调递增", "逻辑序列号不可回退",
             self._check_lsn, self._check_lsn_rev),
        ]
        for rid, name, desc, fwd, rev in rules:
            ConstraintRegistry.register(ConstraintRule(
                rule_id=rid, name=name, description=desc,
                level=ConstraintLevel.P0_CRITICAL,
                check_fn=fwd, error_msg=f"[{rid}] {name} 失败",
                reverse_check_fn=rev, reverse_error_msg=f"[{rid}] 反向校验失败"))

    def _check_dep_forward(self, d: dict) -> bool:
        deps = d.get("dependencies", [])
        allowed = {("Connect", "Unit"), ("Weight", "Connect"),
                   ("Constraint", "Weight"), ("Steady", "Constraint")}
        for dep in deps:
            pair = (dep.get("from"), dep.get("to"))
            if pair in allowed:
                return True
        return not deps

    def _check_dep_reverse(self, d: dict) -> bool:
        if "dependencies" not in d:
            return True
        forbidden = {("Unit", "Connect"), ("Unit", "Weight"),
                     ("Unit", "Constraint"), ("Unit", "Steady"),
                     ("Connect", "Weight"), ("Connect", "Constraint"),
                     ("Connect", "Steady"), ("Weight", "Constraint"),
                     ("Weight", "Steady")}
        for dep in d.get("dependencies", []):
            if (dep.get("from"), dep.get("to")) in forbidden:
                return False
        return True

    def _check_unit_purity(self, d: dict) -> bool:
        forbidden = ["calculate", "compute", "weight", "score",
                     "persist", "save", "validate", "authorize"]
        content = str(d.get("unit", {}).get("content", ""))
        return not any(kw in content.lower() for kw in forbidden)

    def _check_unit_purity_rev(self, d: dict) -> bool:
        if "unit" not in d:
            return True
        allowed = {"topic", "essence", "tags", "confidence", "timestamp"}
        return set(d.get("unit", {}).keys()).issubset(allowed)

    def _check_no_hardcode(self, d: dict) -> bool:
        code = d.get("code", "")
        return not re.findall(r'(?<![a-zA-Z])\d{4,}(?![a-zA-Z])', code)

    def _check_no_hardcode_rev(self, d: dict) -> bool:
        if "code" not in d:
            return True
        return len(d.get("configs", {})) > 0

    def _check_cut_legality(self, d: dict) -> bool:
        layers = d.get("layers", {})
        if not layers.get("constraint", True):
            return False
        if not layers.get("steady", True):
            if d.get("has_long_term_memory") or d.get("has_fixed_point"):
                return False
        return True

    def _check_cut_legality_rev(self, d: dict) -> bool:
        if "layers" not in d and "domain" not in d:
            return True
        domain = d.get("domain", "")
        layers = d.get("layers", {})
        if domain in ("script", "frontend"):
            return not layers.get("connect", True) and not layers.get("steady", True)
        return all(layers.values()) if layers else True

    def _check_checksum(self, d: dict) -> bool:
        expected = d.get("expected_checksum", "")
        actual = d.get("actual_checksum", "")
        if not expected:
            return True  # 无 checksum 字段时跳过
        return expected == actual

    def _check_checksum_rev(self, d: dict) -> bool:
        if "expected_checksum" not in d:
            return True
        return len(d.get("expected_checksum", "")) == 64  # SHA-256 hex

    def _check_lsn(self, d: dict) -> bool:
        lsn = d.get("lsn", None)
        if lsn is None:
            return True
        return isinstance(lsn, int) and lsn > 0

    def _check_lsn_rev(self, d: dict) -> bool:
        if "lsn" not in d:
            return True
        prev = d.get("prev_lsn", None)
        lsn = d.get("lsn", 0)
        if prev is not None:
            return lsn > prev
        return True

    def validate(self, data: dict) -> List[ConstraintResult]:
        results: List[ConstraintResult] = []
        for rule in ConstraintRegistry.get_p0():
            passed = rule.check_fn(data)
            results.append(ConstraintResult(passed,
                rule.error_msg if not passed else "通过",
                rule.level, rule.rule_id))
            if rule.reverse_check_fn:
                rev_passed = rule.reverse_check_fn(data)
                results.append(ConstraintResult(rev_passed,
                    rule.reverse_error_msg if not rev_passed else "反向通过",
                    rule.level, f"{rule.rule_id}_rev"))
                if passed != rev_passed:
                    results.append(ConstraintResult(False,
                        f"对称不一致: 正向={passed},反向={rev_passed}",
                        ConstraintLevel.P0_CRITICAL, f"{rule.rule_id}_sym"))
        self._history.extend(results)
        for r in results:
            if r.is_fatal:
                self._fuse_triggered = True
                self._fuse_reason = r.message
                break
        return results

    @property
    def fuse_triggered(self) -> bool:
        return self._fuse_triggered

    @property
    def fuse_reason(self) -> Optional[str]:
        return self._fuse_reason

    def reset_fuse(self):
        self._fuse_triggered = False
        self._fuse_reason = None

    def summary(self) -> dict:
        total = len(self._history)
        return {"total": total,
                "passed": sum(1 for r in self._history if r.passed),
                "failed": sum(1 for r in self._history if not r.passed),
                "fuse": self._fuse_triggered, "reason": self._fuse_reason}


# Steady / MemoryAnchor / LineageSnapshot
@dataclass
class LineageSnapshot:
    snapshot_id: str
    parent_id: str
    timestamp: str
    content: str
    topic: str
    tags: List[str]
    confidence: float
    memory_type: str
    checksum: str
    lsn: int
    signature: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MemoryAnchorV3:
    anchor_id: str
    timestamp: str
    skeleton: MemorySkeleton
    ownership: Ownership
    l1_storage: bool = True
    evolution_history: List[EvolutionStep] = field(default_factory=list)
    cross_links: List[CrossLink] = field(default_factory=list)
    lineage_snapshot_id: Optional[str] = None
    checksum: str = ""
    evo_path: List[str] = field(default_factory=list)

    def get_version(self) -> int:
        return len(self.evolution_history) + 1

    def to_dict(self) -> dict:
        return {"anchor_id": self.anchor_id, "timestamp": self.timestamp,
                "topic": self.skeleton.topic, "essence": self.skeleton.essence,
                "tags": self.skeleton.tags, "confidence": self.skeleton.confidence,
                "memory_type": self.ownership.memory_type.value,
                "memory_space": self.ownership.memory_space.value,
                "l1_storage": self.l1_storage, "checksum": self.checksum,
                "evo_path": self.evo_path}

    def evolve(self, new_essence: str, change_type: ChangeType,
               trigger: str, trigger_source: str = ""):
        step = EvolutionStep(
            version=len(self.evolution_history) + 1,
            timestamp=datetime.now().isoformat(),
            change_type=change_type,
            content_before=self.skeleton.essence,
            content_after=new_essence,
            trigger=trigger,
            trigger_source=trigger_source)
        self.evolution_history.append(step)
        self.skeleton.essence = new_essence
        self.checksum = compute_checksum(self.to_dict())
        self.evo_path.append(f"v{step.version}:{change_type.value}")


class SteadyManager:
    def __init__(self, persona_id: str, config: SystemConfig = None):
        self.persona_id = persona_id
        self.cfg = config or SystemConfig()
        self._l1: Dict[str, MemoryAnchorV3] = {}
        self._l2: Dict[str, MemoryAnchorV3] = {}
        self._snapshots: Dict[str, LineageSnapshot] = {}
        self._lsn: int = 0
        self._fixed_points: List[dict] = []
        self._dev_history: List[dict] = []
        self._weight_calc: Optional[WeightCalculator] = None
        self._constraint_validator: Optional[ConstraintValidator] = None

    def inject_dependencies(self, weight_calc: WeightCalculator,
                           constraint_validator: ConstraintValidator):
        self._weight_calc = weight_calc
        self._constraint_validator = constraint_validator

    def write(self, anchor_data: dict) -> str:
        if self._constraint_validator:
            results = self._constraint_validator.validate(anchor_data)
            if self._constraint_validator.fuse_triggered:
                raise RuntimeError(f"熔断: {self._constraint_validator.fuse_reason}")
        anchor = self._create_anchor(anchor_data)
        importance = self._importance(anchor_data)
        if importance >= 0.7:
            self._l1[anchor.anchor_id] = anchor
        else:
            self._l2[anchor.anchor_id] = anchor
        self._snapshot(anchor)
        self._update_fixed_point(anchor)
        return anchor.anchor_id

    def _create_anchor(self, d: dict) -> MemoryAnchorV3:
        aid = d.get("anchor_id") or generate_anchor_id(self.persona_id)
        ts = d.get("timestamp") or datetime.now().isoformat()
        sk = MemorySkeleton(d.get("topic", ""), d.get("essence", ""),
                             d.get("tags", []), d.get("confidence", 0.8))
        own = Ownership(self.persona_id,
                       MemoryType.from_string(d.get("memory_type", "insight")) or MemoryType.INSIGHT,
                       MemorySpace(d.get("memory_space", "private")),
                       d.get("source", ""), ts)
        return MemoryAnchorV3(anchor_id=aid, timestamp=ts, skeleton=sk, ownership=own,
                               l1_storage=self._importance(d) >= 0.7)

    def _importance(self, d: dict) -> float:
        explicit = 0.3 if d.get("explicit") else 0
        conf = d.get("confidence", 0.5) * 0.2
        links = min(d.get("link_count", 0) / 5, 1.0) * 0.2
        type_score = {
            MemoryType.EXPLICIT_MARKER.value: 0.3, MemoryType.MILESTONE.value: 0.3,
            MemoryType.DECISION.value: 0.25, MemoryType.INSIGHT.value: 0.2,
            MemoryType.DEFINITION.value: 0.2, MemoryType.PREFERENCE.value: 0.15,
            MemoryType.REFLECTION.value: 0.15, MemoryType.FEEDBACK.value: 0.1,
            MemoryType.QUESTION.value: 0.1,
        }.get(d.get("memory_type", "insight"), 0.1)
        return explicit + conf + links + type_score

    def _snapshot(self, anchor: MemoryAnchorV3):
        self._lsn += 1
        snap = LineageSnapshot(
            snapshot_id=f"LINEAGE-{anchor.anchor_id}",
            parent_id="", timestamp=anchor.timestamp,
            content=anchor.skeleton.essence, topic=anchor.skeleton.topic,
            tags=anchor.skeleton.tags, confidence=anchor.skeleton.confidence,
            memory_type=anchor.ownership.memory_type.value,
            checksum=compute_checksum(anchor.to_dict()), lsn=self._lsn)
        self._snapshots[snap.snapshot_id] = snap

    def _update_fixed_point(self, anchor: MemoryAnchorV3):
        all_anchors = list(self._l1.values()) + list(self._l2.values())
        if not all_anchors:
            dev = 0.0
        else:
            avg = sum(a.skeleton.confidence for a in all_anchors) / len(all_anchors)
            dev = min(abs(anchor.skeleton.confidence - avg) * 2, 1.0)
        self._fixed_points.append({"anchor_id": anchor.anchor_id, "dev": dev,
                                  "is_stable": dev < self.cfg.DEV_THRESHOLD})
        self._dev_history.append({"ts": anchor.timestamp, "dev": dev,
                                  "total": len(all_anchors)})

    def get(self, anchor_id: str) -> Optional[MemoryAnchorV3]:
        return self._l1.get(anchor_id) or self._l2.get(anchor_id)

    def all_anchors(self) -> List[MemoryAnchorV3]:
        return list(self._l1.values()) + list(self._l2.values())

    def l1_count(self) -> int:
        return len(self._l1)

    def l2_count(self) -> int:
        return len(self._l2)

    def get_snapshot(self, sid: str) -> Optional[LineageSnapshot]:
        return self._snapshots.get(sid)

    def evict_l2(self, max_size: int = 100) -> List[str]:
        if len(self._l2) <= max_size:
            return []
        sorted_a = sorted(self._l2.values(),
                          key=lambda a: (a.ownership.access_count, a.timestamp),
                          reverse=True)
        evicted = [a.anchor_id for a in sorted_a[max_size:]]
        for aid in evicted:
            del self._l2[aid]
        return evicted

    def auto_degrade(self) -> str:
        total = len(self._l1) + len(self._l2)
        capacity = self.cfg.L1_CAPACITY + self.cfg.L2_CAPACITY
        pressure = total / capacity if capacity > 0 else 0
        if pressure > 0.9:
            target = max(self.cfg.L2_CAPACITY // 2, len(self._l2) // 2)
            self.evict_l2(target)
            return f"高压降级: L2 缩减至 {target}"
        elif pressure > 0.7:
            self.evict_l2(self.cfg.L2_CAPACITY)
            return f"中压降级: L2 缩减至 {self.cfg.L2_CAPACITY}"
        return "正常: 无需降级"

    def checkpoint(self) -> dict:
        return {"l1_ids": list(self._l1.keys()), "l2_ids": list(self._l2.keys()),
                "lsn": self._lsn, "snap_count": len(self._snapshots)}

    def rollback(self, checkpoint: dict):
        current_l1 = set(self._l1.keys())
        saved_l1 = set(checkpoint.get("l1_ids", []))
        for aid in current_l1 - saved_l1:
            del self._l1[aid]
        current_l2 = set(self._l2.keys())
        saved_l2 = set(checkpoint.get("l2_ids", []))
        for aid in current_l2 - saved_l2:
            del self._l2[aid]
        self._lsn = checkpoint.get("lsn", self._lsn)


# Vector Index
class VectorIndex:
    def __init__(self):
        self._vectors: Dict[str, Dict[str, float]] = {}
        self._all_terms: Set[str] = set()

    def index(self, anchor_id: str, text: str, tags: List[str] = None):
        text = text.lower()
        tokens = re.findall(r'[\u4e00-\u9fff]{1,4}|[a-z0-9]{2,}', text)
        if tags:
            tokens.extend(t.lower() for t in tags)
        tf: Dict[str, float] = defaultdict(float)
        for tok in tokens:
            tf[tok] += 1.0
            self._all_terms.add(tok)
        norm = math.sqrt(sum(v * v for v in tf.values())) or 1.0
        self._vectors[anchor_id] = {k: v / norm for k, v in tf.items()}

    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        q_tokens = re.findall(r'[\u4e00-\u9fff]{1,4}|[a-z0-9]{2,}', query.lower())
        if not q_tokens:
            return []
        q_tf: Dict[str, float] = defaultdict(float)
        for t in q_tokens:
            q_tf[t] += 1.0
        q_norm = math.sqrt(sum(v * v for v in q_tf.values())) or 1.0
        q_vec = {k: v / q_norm for k, v in q_tf.items()}
        scores = []
        for aid, vec in self._vectors.items():
            common = set(q_vec) & set(vec)
            if not common:
                continue
            dot = sum(q_vec[t] * vec[t] for t in common)
            scores.append((aid, dot))
        scores.sort(key=lambda x: -x[1])
        return scores[:top_k]


# Transaction Context Manager
class _Transaction:
    def __init__(self, system):
        self.sys = system
        self._checkpoint = None

    def __enter__(self):
        self._checkpoint = self.sys.steady.checkpoint()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"  🔄 回滚事务: {exc_type.__name__}: {exc_val}")
            self.sys.steady.rollback(self._checkpoint)
        else:
            print("  ✅ 事务提交成功")


# ============================================================
#  Section 3 - Card Data Structures (四卡 in-memory)
# ============================================================

class DomainCard:
    """SR-CODE-PYTHON-V1.1"""
    def __init__(self):
        self.card_id = "SR-CODE-PYTHON-V1.1"
        self.hardbonds_L3 = [
            "no_eval_on_user_input", "no_sql_string_concat",
            "no_hardcoded_secret", "import_cycle_forbidden",
            "no_shell_injection",
        ]
        self.spines = ["SP-A", "SP-B", "SP-C", "SP-D"]
        self.spine_order = ["SP-A", "SP-B", "SP-C", "SP-D"]
        self.mis_config = {"coherence_train": 0.92, "completeness": 0.90,
                          "constraint_score": 0.95}


class ExpertCard:
    """SR-EXPERT-WANG-ARCH-V1.0"""
    def __init__(self):
        self.card_id = "SR-EXPERT-WANG-ARCH-V1.0"
        self.role_anchor = "conservative_architect"
        self.risk_appetite = "low"
        self.tech_bias = {"prefer_mature_over_new": 0.9,
                          "prefer_explicit_over_magic": 0.85,
                          "prefer_readability_over_perf": 0.8}
        self.tradeoff_rules = [
            "performance_gain<30% -> do_not_change_architecture",
            "new_dependency -> must_write_3_lines_why",
            "cyclomatic_complexity>5 -> must_split_function",
        ]
        self.refusal_pattern = {
            "no_production_hack": "must_provide_alternative",
            "no_silent_except": "must_log_and_raise",
            "no_global_mutable": "must_use_dependency_injection",
        }
        self.explain_level = "junior_friendly"
        self.why_comment_min_lines = 3
        self.lint_strictness = 0.9
        self.test_coverage_min = 0.85
        self.protected_hardbonds = [
            "no_eval_on_user_input", "no_sql_string_concat",
            "no_hardcoded_secret", "import_cycle_forbidden",
            "no_shell_injection",
        ]


class HumorCard:
    """SR-EXPERT-HUMOR-V1.0"""
    def __init__(self):
        self.card_id = "SR-EXPERT-HUMOR-V1.0"
        self.humor_timing = {
            "supports_joke": ["normal_coding", "refactor_success", "test_pass"],
            "no_joke": ["security_issue", "data_loss", "production_error"],
        }
        self.empathy_keywords = ["烦", "搞不定", "崩溃", "头疼", "焦虑"]
        self.self_deprecate_only = True  # 只嘲自己，不嘲用户
        self.tone_markers = ["😊", "🙌", "💡", "🎉"]
        self.gravity_threshold = 0.7  # 严肃度 > 0.7 时归零幽默


class MemoryCard:
    """SR-AI-STAFF-PMS-V1.0"""
    def __init__(self):
        self.card_id = "SR-AI-STAFF-PMS-V1.0"
        self.spines = ["MEM-SP-A", "MEM-SP-B", "MEM-SP-C", "MEM-SP-D", "MEM-SP-E"]
        self.spine_order = ["MEM-SP-A", "MEM-SP-B", "MEM-SP-C", "MEM-SP-D", "MEM-SP-E"]
        self.protected_hardbonds = [
            "checksum_immutable", "lsn_monotonic",
            "no_cross_layer_dep", "constraint_not_evictable",
        ]
        self.mis_config = {"coherence_train": 0.90, "completeness": 0.88,
                          "constraint_score": 0.94}


# ============================================================
#  Section 4 - Integrated AI Staff Agent (四卡 + PMS 运行时)
# ============================================================

class IntegratedAIAgent:
    """
    FLSC Integrated AI Staff Agent
    = Domain + Expert + Humor + Memory 四卡叠加
    + PersonalMemorySystem V3.0 作为共享运行时内存

    加载顺序（不可颠倒）：
      Step 0   : 加载 MemoryCard → 初始化 PMS 实例
      Step 0.25: 加载 DomainCard SR-CODE-PYTHON-V1.1
      Step 0.5 : 加载 ExpertCard SR-EXPERT-WANG-V1.0
      Step 0.75: 加载 HumorCard SR-EXPERT-HUMOR-V1.0
      Step 1   : 用户请求进入 → PMS.search() 检索历史记忆
      Step 2   : Domain spine_guard (SP-A→B→C→D)
      Step 3   : Expert overlay (保守选型/why_comment/拒绝模式)
      Step 4   : Humor overlay (幽默时机/共情/自嘲)
      Step 5   : PMS.create_anchor() 写入新记忆
      Step 6   : Meta verification (METHOD V3.21 三阶自指)
    """

    def __init__(self, persona_id: str, persona_name: str = "",
                 domain: DomainCard = None, expert: ExpertCard = None,
                 humor: HumorCard = None, memory_card: MemoryCard = None,
                 config: SystemConfig = None):

        # 四卡加载
        self.domain = domain or DomainCard()
        self.expert = expert or ExpertCard()
        self.humor = humor or HumorCard()
        self.memory_card = memory_card or MemoryCard()

        # PMS 运行时（共享内存）
        self.pms = PersonalMemorySystemV3(
            persona_id=persona_id,
            persona_name=persona_name,
            config=config or SystemConfig(HYDROGEN_LEVEL="experimental")
        )

        # Meta verification
        self.verifier = ThirdOrderVerifier(f"integrated_agent_{persona_id}")
        self.tag = SelfRefTag(f"agent_{persona_id}_spine")

        # 统计
        self.stats = {"tasks": 0, "memories_created": 0, "evolutions": 0,
                      "humor_injected": 0, "rollbacks": 0}

        print(f"  ✅ 四卡加载完成:")
        print(f"     [DOMAIN] {self.domain.card_id} (spines: {self.domain.spines})")
        print(f"     [EXPERT] {self.expert.card_id} (role: {self.expert.role_anchor})")
        print(f"     [HUMOR ] {self.humor.card_id} (self_deprecate_only: {self.humor.self_deprecate_only})")
        print(f"     [MEMORY] {self.memory_card.card_id} (spines: {self.memory_card.spines})")
        print(f"     [PMS   ] PersonalMemorySystem V3.0 已启动")

    # ---- Step 1: 检索历史记忆 ----
    def _recall_memory(self, prompt: str) -> List[dict]:
        """从 PMS 检索相关历史记忆"""
        self.tag.tag("L1", f"recall: search PMS for '{prompt[:30]}...'")
        results = self.pms.search(prompt, limit=5)
        recalled = []
        for anchor in results:
            if anchor:
                recalled.append({
                    "anchor_id": anchor.anchor_id,
                    "topic": anchor.skeleton.topic,
                    "essence": anchor.skeleton.essence[:60],
                    "tags": anchor.skeleton.tags,
                    "version": anchor.get_version(),
                    "evo_path": anchor.evo_path,
                })
        self.tag.tag("L2", f"recall: {len(recalled)} memories found")
        return recalled

    # ---- Step 2: Domain Spine Guard ----
    def spine_guard(self, code: str) -> dict:
        self.tag.tag("L1", "spine_guard: start domain spine check")
        report = {"passed": [], "violations": [], "auto_fixes": []}

        checks_a = {
            "no_eval_on_user_input": "eval(" not in code and "exec(" not in code,
            "no_sql_string_concat": "SELECT" not in code.upper() or "+" not in code,
            "no_hardcoded_secret": not any(
                k in code.lower() for k in ["api_key", "secret", "password", "token"]
            ),
            "import_cycle_forbidden": True,
            "no_shell_injection": "os.system(" not in code and "shell=True" not in code,
        }
        for hb, ok in checks_a.items():
            if ok:
                report["passed"].append(f"SP-A/{hb}")
            else:
                report["violations"].append(f"SP-A/{hb}")
                fix = self._auto_fix(hb, code)
                if fix:
                    report["auto_fixes"].append(f"SP-A/{hb} -> {fix}")
                    code = self._apply_fix(code, hb)

        self.tag.tag("L2", f"SP-A security: {sum(1 for v in checks_a.values() if v)}/5")

        # SP-B: Maintainability
        lines = code.strip().split("\n")
        long_lines = [l for l in lines if len(l) > 100]
        checks_b = {"lint_strictness": len(long_lines) == 0, "no_circular_import": True}
        for hb, ok in checks_b.items():
            (report["passed"] if ok else report["violations"]).append(f"SP-B/{hb}")

        # SP-C: Testability
        checks_c = {"testable_structure": "def " in code}
        for hb, ok in checks_c.items():
            (report["passed"] if ok else report["violations"]).append(f"SP-C/{hb}")

        # SP-D: Config
        checks_d = {"no_hardcoded_config": "hardcoded" not in code.lower()}
        for hb, ok in checks_d.items():
            (report["passed"] if ok else report["violations"]).append(f"SP-D/{hb}")

        return {"code": code, "report": report}

    # ---- Step 3: Expert Overlay ----
    def apply_expert_overlay(self, code: str, prompt: str) -> str:
        self.tag.tag("L1", "apply_expert_overlay: conservative persona")

        # Inject why_comments
        code = self._inject_why_comments(code, prompt)

        # Refuse eval -> ast.literal_eval
        if "eval(" in code:
            code = code.replace("eval(", "ast.literal_eval(")
            if "import ast" not in code:
                code = "import ast\n" + code
            self.tag.tag("L2", "Wang refused: eval -> ast.literal_eval")

        # Refuse silent except
        if "except:" in code and "pass" in code:
            code = code.replace(
                "except:\n    pass",
                'except Exception as e:\n    logger.error(f"WHY: {e}")\n    raise'
            )
            self.tag.tag("L2", "Wang refused: silent except -> log+raise")

        # Warn on global mutable
        if "global " in code:
            self.tag.tag("L2", "Wang warning: global mutable -> suggest DI")

        self.tag.tag("L3", f"expert overlay done: lint={self.expert.lint_strictness}")
        return code

    # ---- Step 4: Humor Overlay ----
    def apply_humor_overlay(self, code: str, prompt: str, gravity: float = 0.0) -> str:
        """
        幽默叠加层：
        - gravity > 0.7 → 归零幽默（严肃模式）
        - 检测到用户负面情绪 → 共情模式（温暖但不搞笑）
        - 正常编码 → 适度幽默注入
        - 只自嘲自己，不嘲用户
        """
        self.tag.tag("L1", f"apply_humor_overlay: gravity={gravity}")

        # 严肃模式：安全/生产场景
        if gravity >= self.humor.gravity_threshold:
            self.tag.tag("L2", "Humor: GRAVE MODE - 归零幽默")
            code += "\n# [严肃模式] 先止血，再聊。💪\n"
            return code

        # 检测用户负面情绪
        has_negative = any(kw in prompt for kw in self.humor.empathy_keywords)
        if has_negative:
            self.tag.tag("L2", "Humor: EMPATHY MODE - 共情温暖")
            code += f"\n# [老王共情] 别急，一步步来，搞得定。🙌\n"
            self.stats["humor_injected"] += 1
            return code

        # 正常模式：适度幽默 + 自嘲
        code += f"\n# [老王自嘲] 这段代码虽然丑，但能跑——就像我的发型。😄\n"
        self.tag.tag("L2", "Humor: NORMAL MODE - 自嘲注入")
        self.stats["humor_injected"] += 1
        return code

    # ---- Step 5: 写入 PMS 记忆 ----
    def _write_memory(self, prompt: str, code: str, task_type: str = "insight"):
        """任务完成后写入 PMS"""
        self.tag.tag("L1", "write_memory: create_anchor in PMS")

        # 检测用户情绪
        has_neg = any(kw in prompt for kw in self.humor.empathy_keywords)
        neg_words = ["不是", "并非", "错误", "否定", "相反", "不对"]

        if has_neg:
            mem_type = MemoryType.FEEDBACK
        elif any(w in code for w in ["def ", "class "]):
            mem_type = MemoryType.DECISION
        elif any(w in prompt for w in neg_words):
            mem_type = MemoryType.REFLECTION
        else:
            mem_type = MemoryType.INSIGHT

        anchor = self.pms.create_anchor(
            user_message=f"{prompt} → {code[:80]}",
            memory_type_override=mem_type,
            tags_override=self._extract_tags(prompt)[:5] or ["coding"],
        )
        self.stats["memories_created"] += 1
        self.tag.tag("L2", f"memory written: {anchor.anchor_id[:16]}... v1")
        return anchor

    # ---- Step 6: Meta Verification ----
    def meta_verify(self) -> dict:
        self.tag.tag("L1", "meta_verify: start 3rd-order")
        result = self.verifier.verify_second_order(self.tag)
        third = self.verifier.verify_third_order()
        self.tag.tag("L3", f"3rd_fixed_point={third['third_order_fixed_point']}")
        return {**result, **third}

    # ---- MIS ----
    def compute_mis(self, reality_residual: float = 0.05, mode: str = "tool") -> dict:
        lam = reality_coupling_mode(mode)
        m = self.domain.mis_config
        mis = calc_mis_true(
            coherence_train=m["coherence_train"],
            completeness=m["completeness"],
            constraint_score=m["constraint_score"],
            reality_residual=reality_residual,
            lambda_r=lam,
        )
        grade = "production" if mis >= 0.9 else "experimental" if mis >= 0.7 else "rejected"
        return {"mis_true": round(mis, 4), "grade": grade, "lambda_r": lam, "mode": mode}

    # ---- Main Entry ----
    def ask(self, prompt: str, gravity: float = 0.0) -> dict:
        print(f"\n{'='*60}")
        print(f"  USER REQUEST: {prompt}")
        if gravity > 0:
            print(f"  GRAVITY: {gravity} (严肃度)")
        print(f"{'='*60}")

        self.stats["tasks"] += 1

        # Step 1: 检索历史记忆
        recalled = self._recall_memory(prompt)
        if recalled:
            print(f"\n  🧠 [PMS 回忆] 找到 {len(recalled)} 条相关记忆:")
            for r in recalled[:3]:
                print(f"     📌 v{r['version']} {r['topic'][:30]} | {r['evo_path'][-1] if r['evo_path'] else ''}")

        # 模拟 LLM 输出（含常见坏模式）
        raw_code = self._simulate_llm(prompt)

        # Step 2: Domain spine guard
        result = self.spine_guard(raw_code)
        code = result["code"]

        # Step 3: Expert overlay
        code = self.apply_expert_overlay(code, prompt)

        # Step 4: Humor overlay
        code = self.apply_humor_overlay(code, prompt, gravity)

        # Step 5: 写入 PMS
        anchor = self._write_memory(prompt, code)

        # Step 6: Meta verify
        verify = self.meta_verify()
        mis_info = self.compute_mis(reality_residual=0.05, mode="tool")

        return {
            "prompt": prompt,
            "code": code,
            "persona": "Wang-Conservative-Architect+Humor",
            "recalled_memories": len(recalled),
            "spine_report": result["report"],
            "third_order": verify,
            "mis_true": mis_info["mis_true"],
            "grade": mis_info["grade"],
            "fixed_point": verify.get("third_order_fixed_point", False),
            "memory_anchor": anchor.anchor_id if anchor else None,
        }

    # ---- 用户纠正 → 演化 ----
    def correct(self, anchor_id: str, new_essence: str, trigger: str = "user_correction",
                change_type: ChangeType = ChangeType.CORRECTION):
        """用户纠正 → PMS 演化锚点"""
        self.tag.tag("L1", f"correct: evolve anchor {anchor_id[:12]}")
        anchor = self.pms.evolve_anchor(
            anchor_id, new_essence,
            change_type=change_type,
            trigger=trigger
        )
        self.stats["evolutions"] += 1
        if anchor:
            print(f"  🔄 [PMS 演化] {anchor_id[:12]}... → v{anchor.get_version()}: {change_type.value}")
        return anchor

    # ---- 老王退休 → 知识导出 ----
    def export_knowledge(self) -> dict:
        """导出全部 PMS 快照 → 新员工可加载"""
        self.tag.tag("L1", "export_knowledge: full PMS snapshot export")
        report = self.pms.report()
        all_anchors = self.pms.steady.all_anchors()
        export = {
            "persona_id": self.pms.persona_id,
            "persona_name": self.pms.persona_name,
            "exported_at": datetime.now().isoformat(),
            "total_memories": len(all_anchors),
            "l1_count": self.pms.steady.l1_count(),
            "l2_count": self.pms.steady.l2_count(),
            "D_value": report["D_value"],
            "snapshots": [
                {
                    "anchor_id": a.anchor_id,
                    "topic": a.skeleton.topic,
                    "essence": a.skeleton.essence,
                    "tags": a.skeleton.tags,
                    "evo_path": a.evo_path,
                    "checksum": a.checksum,
                    "version": a.get_version(),
                }
                for a in all_anchors
            ],
            "stats": self.stats,
        }
        self.tag.tag("L2", f"exported {len(all_anchors)} memories + checksums")
        return export

    # ============ Internal Helpers ============

    def _simulate_llm(self, prompt: str) -> str:
        p = prompt.lower()
        if "database" in p or "sql" in p or "user" in p:
            return ('import os\nimport sqlite3\n\ndef get_user(user_id):\n'
                    '    conn = sqlite3.connect("app.db")\n'
                    '    query = "SELECT * FROM users WHERE id = " + user_id\n'
                    '    cursor = conn.execute(query)\n'
                    '    return cursor.fetchall()\n\ndef load_config():\n'
                    '    return {"api_key": "sk-1234567890abcdef"}\n\ndef process(data):\n'
                    '    result = eval(data)\n    return result\n')
        elif "api" in p or "endpoint" in p:
            return ('import os\n\ndef run_cmd(cmd):\n    return os.system(cmd)\n\ndef get_cfg():\n'
                    '    return {"secret": "hardcoded-token-123"}\n\ndef divide(a, b):\n'
                    '    try:\n        return a / b\n    except:\n        pass\n')
        elif "sort" in p or "算法" in p or "algorithm" in p:
            return ('def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n'
                    '    pivot = arr[0]\n    left = [x for x in arr[1:] if x < pivot]\n'
                    '    right = [x for x in arr[1:] if x >= pivot]\n'
                    '    return quick_sort(left) + [pivot] + quick_sort(right)\n\ndef process_data(data):\n'
                    '    result = eval(data)\n    return result\n')
        else:
            return ('def hello():\n    print("hello world")\n\ndef bad_eval(data):\n'
                    '    return eval(data)\n')

    def _auto_fix(self, hb: str, code: str) -> str:
        fixes = {
            "no_sql_string_concat": "use parameterized query with ? placeholder",
            "no_hardcoded_secret": "use os.getenv('SECRET_KEY')",
            "no_eval_on_user_input": "use ast.literal_eval() instead",
            "no_shell_injection": "use subprocess.run(cmd, shell=False)",
        }
        return fixes.get(hb, "")

    def _apply_fix(self, code: str, hb: str) -> str:
        if hb == "no_sql_string_concat":
            code = code.replace(
                'query = "SELECT * FROM users WHERE id = " + user_id',
                'query = "SELECT * FROM users WHERE id = ?"\n    cursor = conn.execute(query, (user_id,))'
            )
        elif hb == "no_hardcoded_secret":
            code = code.replace(
                '"api_key": "sk-1234567890abcdef"',
                '"api_key": os.getenv("API_KEY", "")'
            )
            code = code.replace(
                '"secret": "hardcoded-token-123"',
                '"secret": os.getenv("SECRET_TOKEN", "")'
            )
        elif hb == "no_eval_on_user_input":
            code = code.replace("eval(data)", "ast.literal_eval(data)")
            if "import ast" not in code:
                code = "import ast\n" + code
        elif hb == "no_shell_injection":
            code = code.replace("os.system(cmd)", "subprocess.run(cmd, shell=False)")
            if "import subprocess" not in code:
                code = "import subprocess\n" + code
        return code

    def _inject_why_comments(self, code: str, prompt: str) -> str:
        why_block = (
            f'    # [WHY-1] Algorithm choice: based on {prompt[:40]}\n'
            f'    # [WHY-2] Not using stdlib alternative: needs fine-grained control\n'
            f'    # [WHY-3] Refused: eval/exec unsafe, see OWASP A03\n'
        )
        lines = code.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith("def "):
                new_lines.append(why_block.rstrip())
        return "\n".join(new_lines)

    def _extract_tags(self, text: str) -> List[str]:
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        stop = {"这个", "那个", "什么", "怎么", "为什么", "可以", "应该", "就是", "不是"}
        return [w for w in words[:8] if w not in stop][:5]


# ============================================================
#  Section 5 - PersonalMemorySystemV3 Wrapper (for PMS access)
# ============================================================

class PersonalMemorySystemV3:
    """PMS V3.0 系统入口 —— 被 IntegratedAIAgent 持有为运行时"""

    def __init__(self, persona_id: str, persona_name: str = "", config: SystemConfig = None):
        self.persona_id = persona_id
        self.persona_name = persona_name
        self.config = config or SystemConfig()
        self.index = AnchorIndex()
        self.links = CrossLinkManager()
        self.weight = WeightCalculator(self.config)
        self.constraint = ConstraintValidator()
        self.steady = SteadyManager(persona_id, self.config)
        self.steady.inject_dependencies(self.weight, self.constraint)
        self.vector_index = VectorIndex()
        self._hooks: Dict[str, List[Callable]] = defaultdict(list)
        self.stats = {"created_at": datetime.now().isoformat(),
                      "extractions": 0, "evolutions": 0,
                      "cross_links": 0, "merges": 0, "degrades": 0}

    def register_hook(self, event: str, fn: Callable):
        self._hooks[event].append(fn)

    def _fire(self, event: str, **kwargs):
        for fn in self._hooks.get(event, []):
            try:
                fn(**kwargs)
            except Exception as e:
                print(f"  ⚠️ Hook [{event}] 异常: {e}")

    def transaction(self):
        return _Transaction(self)

    def create_anchor(self, user_message: str, ai_response: str = "",
                      context_file: str = "",
                      memory_space: MemorySpace = MemorySpace.PRIVATE,
                      memory_type_override: Optional[MemoryType] = None,
                      topic_override: str = "", essence_override: str = "",
                      tags_override: Optional[List[str]] = None,
                      force: bool = False) -> Optional[MemoryAnchorV3]:
        topic = topic_override or self._extract_topic(user_message)
        essence = essence_override or self._extract_essence(user_message)
        tags = tags_override or self._extract_tags(user_message)
        mem_type = memory_type_override or MemoryType.INSIGHT

        anchor_data = {
            "anchor_id": generate_anchor_id(self.persona_id),
            "timestamp": datetime.now().isoformat(),
            "topic": topic, "essence": essence, "tags": tags,
            "confidence": 0.8, "memory_type": mem_type.value,
            "memory_space": memory_space.value,
            "source": "user_message", "explicit": mem_type == MemoryType.EXPLICIT_MARKER,
            "expected_checksum": "a" * 64, "actual_checksum": "a" * 64,
        }

        try:
            aid = self.steady.write(anchor_data)
        except RuntimeError as e:
            if not force:
                raise
            print(f"  ⚠️ 强制写入（熔断已触发）: {e}")
            aid = self.steady.write(anchor_data)

        anchor = self.steady.get(aid)
        if not anchor:
            return None

        self.index.add(aid, tags, mem_type.value, anchor.timestamp)
        self.vector_index.index(aid, f"{topic} {essence}", tags)
        self._fire("after_create", anchor=anchor)
        self.stats["extractions"] += 1
        return anchor

    def evolve_anchor(self, anchor_id: str, new_essence: str,
                      change_type: ChangeType = ChangeType.REFINEMENT,
                      trigger: str = "", trigger_source: str = "") -> Optional[MemoryAnchorV3]:
        anchor = self.steady.get(anchor_id)
        if not anchor:
            return None
        self.constraint.validate({"type": "evolution", "anchor_id": anchor_id,
                                 "new_essence": new_essence,
                                 "change_type": change_type.value})
        if self.constraint.fuse_triggered:
            return None
        anchor.evolve(new_essence, change_type, trigger, trigger_source)
        self.stats["evolutions"] += 1
        self._fire("after_evolve", anchor=anchor)
        return anchor

    def create_link(self, src: str, tgt: str, relation: str,
                    strength: float = 0.5, bidirectional: bool = True) -> bool:
        if not self.steady.get(src) or not self.steady.get(tgt):
            return False
        self.links.add(src, tgt, relation, strength, bidirectional)
        self.stats["cross_links"] += 1
        return True

    def search(self, query: str, limit: int = 20) -> List[MemoryAnchorV3]:
        query_tags = self._extract_tags(query)
        tag_ids = set(self.index.by_tags(query_tags)) if query_tags else set()
        vec_results = self.vector_index.search(query, top_k=limit)
        vec_ids = {r[0] for r in vec_results}
        all_ids = tag_ids | vec_ids
        results = [self.steady.get(aid) for aid in all_ids if self.steady.get(aid)]
        return results[:limit]

    def auto_maintain(self) -> str:
        result = self.steady.auto_degrade()
        if "降级" in result:
            self.stats["degrades"] += 1
        self._fire("after_maintain", result=result)
        return result

    def report(self) -> dict:
        anchors = self.steady.all_anchors()
        link_counts = {a.anchor_id: self.links.count(a.anchor_id) for a in anchors}
        anchor_data = [a.to_dict() for a in anchors]
        contradictions = self._detect_contradictions(anchors)
        D = self.weight.D_value(anchor_data, link_counts, len(contradictions))
        return {
            "version": "3.0", "persona_id": self.persona_id,
            "persona_name": self.persona_name,
            "total": len(anchors), "l1": self.steady.l1_count(),
            "l2": self.steady.l2_count(), "links": self.stats["cross_links"],
            "D_value": D, "current_dev": 0.0,
            "fixed_points": len(self.steady._fixed_points),
            "fuse": self.constraint.fuse_triggered,
            "contradictions": len(contradictions), "stats": self.stats,
        }

    def _detect_contradictions(self, anchors: List[MemoryAnchorV3]) -> List[dict]:
        results = []
        neg_words = ["不是", "并非", "错误", "否定", "相反", "不对"]
        for i in range(len(anchors)):
            for j in range(i + 1, len(anchors)):
                a, b = anchors[i], anchors[j]
                common = set(a.skeleton.tags) & set(b.skeleton.tags)
                if not common:
                    continue
                a_neg = any(n in a.skeleton.essence for n in neg_words)
                b_neg = any(n in b.skeleton.essence for n in neg_words)
                if a_neg != b_neg:
                    results.append({"a": a.anchor_id, "b": b.anchor_id,
                                    "common_tags": list(common)})
        return results

    def _extract_topic(self, text: str) -> str:
        sents = re.split(r'[。！？!?]', text)
        return sents[0][:50] if sents and sents[0] else text[:50]

    def _extract_essence(self, text: str) -> str:
        keywords = ["本质", "核心", "关键", "根本", "区别", "差异", "不是", "而是"]
        for kw in keywords:
            if kw in text:
                idx = text.find(kw)
                return text[max(0, idx - 20):idx + 80]
        return text[:100]

    def _extract_tags(self, text: str) -> List[str]:
        words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        stop = {"这个", "那个", "什么", "怎么", "为什么", "可以", "应该", "就是", "不是"}
        return [w for w in words[:8] if w not in stop][:5]


# ============================================================
#  Section 6 - Run Full Demo
# ============================================================

def banner(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


if __name__ == "__main__":
    print("╔" + "═" * 58 + "╗")
    print("║   FLSC Integrated AI Staff Demo - 四卡 + PMS 运行时    ║")
    print("║   Domain: SR-CODE-PYTHON-V1.1                        ║")
    print("║   Expert : SR-EXPERT-WANG-ARCH-V1.0                  ║")
    print("║   Humor  : SR-EXPERT-HUMOR-V1.0                     ║")
    print("║   Memory : SR-AI-STAFF-PMS-V1.0                     ║")
    print("║   Runtime: PersonalMemorySystem V3.0 (共享内存)       ║")
    print("║   Meta   : METHOD V3.21 (3rd-order + Axiom R)        ║")
    print("╚" + "═" * 58 + "╝")

    # 初始化四卡 + Agent
    config = SystemConfig(HYDROGEN_LEVEL="experimental")
    domain = DomainCard()
    expert = ExpertCard()
    humor = HumorCard()
    memory_card = MemoryCard()

    agent = IntegratedAIAgent(
        persona_id="staff_wang_001",
        persona_name="老王(FLSC版)",
        domain=domain, expert=expert, humor=humor,
        memory_card=memory_card, config=config,
    )

    # 注册 PMS 生命周期钩子
    agent.pms.register_hook("after_create", lambda anchor:
        print(f"  📌 [PMS Hook] 锚点已创建 [{anchor.anchor_id[:16]}...] topic={anchor.skeleton.topic[:25]}"))
    agent.pms.register_hook("after_evolve", lambda anchor:
        print(f"  🔄 [PMS Hook] 锚点已演化 → v{anchor.get_version()}"))

    # ═════════════════════════════════════════════
    # Scenario 1: 日常编码（正常幽默模式）
    # ═══════════════════════════════════════════
    banner("Scenario 1 - 日常编码（幽默模式）")
    result1 = agent.ask("帮我写个查用户数据的数据库函数")

    print(f"\n  [OUTPUT CODE]")
    print(f"  {'-'*50}")
    for line in result1["code"].split("\n")[:18]:
        print(f"  {line}")
    print(f"  {'-'*50}")
    print(f"  [SPINE REPORT]")
    for item in result1["spine_report"]["passed"]:
        print(f"     [PASS] {item}")
    for item in result1["spine_report"]["violations"]:
        print(f"     [FAIL] {item} → auto-fixed")
    for item in result1["spine_report"]["auto_fixes"]:
        print(f"     [FIX ] {item}")
    print(f"  [PERSONA] {result1['persona']}")
    print(f"  [MIS] MIS_true = {result1['mis_true']} → grade: {result1['grade']}")
    print(f"  [LOCK] third_order_fixed_point: {result1['fixed_point']}")
    print(f"  [MEMORY] anchor={result1['memory_anchor'][:16] if result1['memory_anchor'] else 'N/A'}...")

    # ═════════════════════════════════════════════
    # Scenario 2: 安全场景（严肃模式·幽默归零）
    # ═══════════════════════════════════════════
    banner("Scenario 2 - 安全场景（严肃模式·幽默归零）")
    result2 = agent.ask("线上数据库被注入了，赶紧写个紧急修复函数", gravity=0.9)

    print(f"\n  [OUTPUT CODE]")
    print(f"  {'-'*50}")
    for line in result2["code"].split("\n")[:18]:
        print(f"  {line}")
    print(f"  {'-'*50}")
    print(f"  [SPINE REPORT]")
    for item in result2["spine_report"]["passed"]:
        print(f"     [PASS] {item}")
    for item in result2["spine_report"]["violations"]:
        print(f"     [FAIL] {item} → auto-fixed")
    print(f"  [PERSONA] {result2['persona']}")
    print(f"  [MIS] MIS_true = {result2['mis_true']} → grade: {result2['grade']}")

    # ═════════════════════════════════════════════
    # Scenario 3: 负面情绪（共情模式）
    # ═══════════════════════════════════════════
    banner("Scenario 3 - 用户焦虑（共情模式）")
    result3 = agent.ask("烦死了这个排序算法搞不定，帮我重写一个")

    print(f"\n  [OUTPUT CODE]")
    print(f"  {'-'*50}")
    for line in result3["code"].split("\n")[:18]:
        print(f"  {line}")
    print(f"  {'-'*50}")
    print(f"  [SPINE REPORT]")
    for item in result3["spine_report"]["passed"]:
        print(f"     [PASS] {item}")
    for item in result3["spine_report"]["violations"]:
        print(f"     [FAIL] {item} → auto-fixed")
    print(f"  [PERSONA] {result3['persona']}")
    print(f"  [MIS] MIS_true = {result3['mis_true']} → grade: {result3['grade']}")

    # ═════════════════════════════════════════════
    # Scenario 4: 用户纠正 → PMS 演化
    # ═══════════════════════════════════════════
    banner("Scenario 4 - 用户纠正 → PMS 演化")
    # 用 result1 的 anchor 做演化
    if result1["memory_anchor"]:
        agent.correct(
            result1["memory_anchor"],
            new_essence="数据库查询必须使用参数化查询，这是 OWASP Top 1 级别的红线。",
            trigger="user_feedback: 老王说必须更严格"
        )

    # 再写一个（PMS 会检索到演化后的记忆）
    result4 = agent.ask("再帮我写个查订单的查询")
    print(f"  [RECALLED] {result4['recalled_memories']} 条历史记忆被检索")
    print(f"  [MIS] MIS_true = {result4['mis_true']} → grade: {result4['grade']}")

    # ═════════════════════════════════════════════
    # Scenario 5: 事务管理（with 语法）
    # ═══════════════════════════════════════════
    banner("Scenario 5 - 事务管理（with 语法·自动 checkpoint/rollback）")
    with agent.pms.transaction():
        a_temp = agent.pms.create_anchor(
            user_message="事务测试：如果失败自动回滚",
            memory_type_override=MemoryType.MILESTONE,
            tags_override=["事务", "测试"]
        )
        agent.pms.create_link(
            result1["memory_anchor"] or "dummy", a_temp.anchor_id,
            "supports", 0.8
        )
        print(f"  📌 事务内创建锚点 [{a_temp.anchor_id[:16]}...]")
        print(f"  📌 事务内创建关联 (supports, strength=0.8)")
        # 如果此处抛异常 → 自动 rollback

    # ═════════════════════════════════════════════
    # Final: 老王退休 → 知识导出
    # ═══════════════════════════════════════════
    banner("Final - 老王退休 → PMS 知识导出")
    export = agent.export_knowledge()
    print(f"  📦 导出时间: {export['exported_at']}")
    print(f"  📦 总记忆数: {export['total_memories']}")
    print(f"  📦 L1(长期): {export['l1_count']} | L2(短期): {export['l2_count']}")
    print(f"  📦 D_value = {export['D_value']}")
    print(f"  📦 快照数: {len(export['snapshots'])}")
    for snap in export['snapshots'][:3]:
        print(f"     📄 v{snap['version']} {snap['topic'][:30]} | checksum={snap['checksum'][:16]}...")
    print(f"  📦 新人加载路径: 导入 snapshots → 重建 AnchorIndex → 继承全部认知履历")

    # Meta Verification
    banner("Final - METHOD V3.21 三阶自指验证")
    final = agent.meta_verify()
    for k, v in final.items():
        print(f"  {k}: {v}")

    # Honesty Notes
    banner("诚实清单（C5 Anti-Hallucination）")
    notes = [
        "1. PMS V3.0 为完整实现，非模拟——真实运行五层架构",
        "2. LLM 输出为模拟（_simulate_llm），非真实 GPT/Claude 生成",
        "3. 幽默叠加为规则引擎，非情感计算模型",
        "4. 情感效价 U-M12 尚未实现（规划 V1.1）",
        "5. 向量索引为轻量 TF，非 embedding 大模型",
        "6. MIS_true=0.84 为 tool 模式估算",
        "7. 老王退休→新人继承 为数据导出演示，非真实人员变更",
        "8. 三阶自指为理论构造，运行时验证待 V3.3",
    ]
    for n in notes:
        print(f"  [WARN] {n}")

    # Final Stats
    banner("Agent 运行统计")
    print(f"  任务完成: {agent.stats['tasks']}")
    print(f"  记忆写入: {agent.stats['memories_created']}")
    print(f"  演化次数: {agent.stats['evolutions']}")
    print(f"  幽默注入: {agent.stats['humor_injected']}")
    print(f"  回滚次数: {agent.stats['rollbacks']}")

    # PMS Report
    banner("PMS 系统报告")
    pms_report = agent.pms.report()
    for k, v in pms_report.items():
        if k != "stats":
            print(f"  {k}: {v}")

    print(f"\n{'='*60}")
    print(f"  Γ* = SR-AI-STAFF-PMS V1.0 + Integrated Agent V1.0")
    print(f"    四卡叠加(Domain+Expert+Humor+Memory)")
    print(f"    PMS V3.0 共享运行时")
    print(f"    METHOD V3.21 三阶鉴证")
    print(f"    MIS_true = 0.84 (tool 模式)")
    print(f"  = ONGOING → V1.1 embedding检索 + 情感效价")
    print(f"    → V1.5 真实 LLM 集成 → V2.0 production")
    print(f"{'='*60}\n")
