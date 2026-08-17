#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_kg2sr.py
验证 kg2sr_agent.py 蒸馏产物（SR-xxx-DISTILL-V0.1.yaml）的完整性
────────────────────────────────────────────────────────────
检查项：
  S1  文件存在性
  S2  FLSC 五层齐全（Unit/Connect/Weight/Constraint/Steady）
  S3  脊线闭合（SpineChecker 复算 RIS₇）
  S4  血统快照完整性（checksum / lsn / parent / lineage_chain）
  S5  签署页状态（AI_DRAFT / AI_SIGNED / REJECTED）
  S6  诚实清单 + 适配器合规
  S7  跨文档互锁（引用 MEM-GLOBAL / MEM-ADAPTER-SPEC）
  S8  批量扫描（目录下所有 DISTILL yaml）
────────────────────────────────────────────────────────────
用法：
  python verify_kg2sr.py --file SR-POETRY-DISTILL-V0.1.yaml
  python verify_kg2sr.py --dir  /data/workspace/domains/asset_cards
"""

import argparse
import hashlib
import sys
from pathlib import Path
import yaml

# ═════════════════════════════════════════════════════
# 全局
# ═════════════════════════════════════════════════════
PASS = 0
FAIL = 0
WARN = 0
results: list[str] = []

def check(section, name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        results.append(f"  ✅ [{section}] {name}")
    else:
        FAIL += 1
        results.append(f"  ❌ [{section}] {name} — {detail}")

def warn(section, name, detail=""):
    global WARN
    WARN += 1
    results.append(f"  ⚠️  [{section}] {name} — {detail}")

# ═════════════════════════════════════════════════════
# 五层完整性
# ═════════════════════════════════════════════════════
def check_five_layers(doc, sec):
    for key, label in [
        ("units", "Unit 层"), ("connections", "Connect 层"),
        ("weights", "Weight 层"), ("constraints", "Constraint 层"),
        ("steady", "Steady 层"),
    ]:
        items = doc.get(key, [])
        check(sec, f"{label} 存在且有内容", isinstance(items, list) and len(items) > 0,
              f"{key} 为空或缺失")

# ═════════════════════════════════════════════════════
# 脊线闭合 RIS₇
# ═════════════════════════════════════════════════════
def check_spines(doc, sec):
    spines = doc.get("spines", [])
    check(sec, "脊线列表存在", len(spines) > 0, "spines 为空")
    hard = [s for s in spines if s.get("hard_bond")]
    check(sec, f"至少 1 条 L1 硬脊线 (P0)", len(hard) > 0,
          f"当前硬脊线数={len(hard)}")

    # 复算 RIS₇
    units = doc.get("units", [])
    conns = doc.get("connections", [])
    wgts  = doc.get("weights", [])
    cons  = doc.get("constraints", [])
    stdy  = doc.get("steady", [])
    p0    = [c for c in cons if c.get("level") == "P0_CRITICAL"]

    s_unit = min(1.0, len(units) / 3)
    s_conn = min(1.0, len(conns) / 3)
    s_wgt  = min(1.0, len(wgts) / 1)
    s_cons = min(1.0, len(p0) / 2)
    s_std  = min(1.0, len(stdy) / 1)
    ris7   = round(0.2*s_unit + 0.2*s_conn + 0.2*s_wgt + 0.15*s_cons + 0.15*s_std + 0.1*0.8, 3)
    check(sec, f"RIS₇ 评分 ≥ 0.5 (实测 {ris7})", ris7 >= 0.5, f"RIS₇={ris7}")

    # 删除测试
    for sp in spines:
        check(sec, f"脊线 {sp['id']} 有 deletion_test",
              bool(sp.get("deletion_test")), sp.get("id", ""))

# ═════════════════════════════════════════════════════
# 血统快照
# ═════════════════════════════════════════════════════
def check_lineage(doc, sec, path):
    meta = doc.get("metadata", {})
    snap_id = meta.get("lineage_snapshot_id", "")
    cs = meta.get("checksum", "")
    check(sec, "lineage_snapshot_id 存在", bool(snap_id), "metadata.lineage_snapshot_id 缺失")
    check(sec, "checksum 存在 (≥12 字符)", len(cs) >= 12, f"checksum={cs}")

    # 校验 checksum 格式（sha256 前 24 字符 hex）
    if cs:
        check(sec, "checksum 为合法 hex", all(c in "0123456789abcdef" for c in cs.lower()),
              f"checksum 含非法字符: {cs}")

    # lineage chain：兼容顶层 lineage 和 signatures.bloodline.lineage_chain 两种位置
    chain = doc.get("lineage", []) or (
        doc.get("signatures", {}).get("bloodline", {}).get("lineage_chain", [])
    )
    check(sec, "血统链含 FLSC-BASE", "FLSC-BASE-V1.0" in chain, str(chain))
    check(sec, "血统链含 MEM-GLOBAL", "MEM-GLOBAL-V1.0" in chain, str(chain))

    # parent
    check(sec, "parent_card = MEM-GLOBAL-V1.0",
          doc.get("parent_card") == "MEM-GLOBAL-V1.0",
          doc.get("parent_card", ""))

# ═════════════════════════════════════════════════════
# 签署页
# ═════════════════════════════════════════════════════
def check_signatures(doc, sec):
    sig = doc.get("signatures", {})
    carbon = sig.get("carbon_based", {})
    silicon = sig.get("silicon_based", {})
    status = carbon.get("status", "")

    valid = {"AI_DRAFT", "AI_SIGNED", "REJECTED", "PENDING_REVIEW"}
    check(sec, f"签署状态合法 ({status})", status in valid, f"未知状态: {status}")

    if status == "AI_DRAFT":
        warn(sec, "当前为 AI_DRAFT，等待人工签字", "需 reviewer 签字升级")
    elif status == "AI_SIGNED":
        check(sec, "AI_SIGNED 含 reviewer", bool(carbon.get("reviewer")), "缺 reviewer")
        check(sec, "fixed_point = True", silicon.get("fixed_point") is True, "")
    elif status == "REJECTED":
        warn(sec, "已驳回，需重新蒸馏", carbon.get("note", ""))

    # γ*
    gs = sig.get("gamma_star", "")
    check(sec, "Γ* 字符串存在", bool(gs) and "Γ" in gs, gs)

# ═════════════════════════════════════════════════════
# 诚实清单 + 适配器
# ═════════════════════════════════════════════════════
def check_honesty_and_adapter(doc, sec):
    hcl = doc.get("honesty_checklist", [])
    check(sec, "诚实清单非空", len(hcl) >= 1, f"count={len(hcl)}")
    for h in hcl:
        check(sec, f"诚实项 severity 合法 ({h.get('item','')[:20]})",
              h.get("severity") in {"known_limitation", "improvement", "planned", "pending_review"},
              str(h))

    ac = doc.get("adapter_compliance", {})
    if ac:
        methods = ac.get("required_methods_implemented", [])
        check(sec, "适配器含 remember/recall/evolve/forget/snapshot/transaction/report",
              len(methods) >= 6, str(methods))
        check(sec, "forbidden_patterns_checked = True",
              ac.get("forbidden_patterns_checked") is True, "")

# ═════════════════════════════════════════════════════
# 跨文档互锁
# ═════════════════════════════════════════════════════
def check_cross_doc(doc, sec, path):
    text = Path(path).read_text(encoding="utf-8").lower()
    refs = [
        ("mem-global", "memory_root"),
        ("mem-adapter-spec", "adapter_spec"),
        ("flsc-base", "base_spec"),
        ("kg2sr-agent", "generator"),
    ]
    for key, label in refs:
        check(sec, f"引用 {label} ({key})", key in text, "")

# ═════════════════════════════════════════════════════
# 单文件主校验
# ═════════════════════════════════════════════════════
def verify_file(path: str) -> bool:
    global PASS, FAIL, WARN, results
    p = Path(path)
    print(f"\n{'='*60}")
    print(f"  🔎 验证: {p.name}")
    print(f"{'='*60}")

    check("S1", f"文件存在: {p.name}", p.exists(), f"路径: {path}")
    if not p.exists():
        return False

    try:
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:
        check("S1", "YAML 语法合法", False, str(e))
        return False

    check("S1", "顶层为 mapping", isinstance(doc, dict), type(doc).__name__)

    # S2 五层
    print("\n📂 S2 · FLSC 五层完整性")
    check_five_layers(doc, "S2")

    # S3 脊线
    print("\n🧠 S3 · 脊线闭合 (RIS₇)")
    check_spines(doc, "S3")

    # S4 血统
    print("\n🔗 S4 · 血统快照")
    check_lineage(doc, "S4", path)

    # S5 签署
    print("\n✍️  S5 · 签署页")
    check_signatures(doc, "S5")

    # S6 诚实+适配器
    print("\n📋 S6 · 诚实清单 + 适配器合规")
    check_honesty_and_adapter(doc, "S6")

    # S7 跨文档
    print("\n🔗 S7 · 跨文档互锁")
    check_cross_doc(doc, "S7", path)

    return FAIL == 0

# ═════════════════════════════════════════════════════
# 批量扫描
# ═════════════════════════════════════════════════════
def scan_dir(directory: str):
    global PASS, FAIL, WARN, results
    d = Path(directory)
    files = sorted(d.glob("SR-*-DISTILL-*.yaml"))
    print(f"\n{'🔎'*3} 批量扫描: {d}  (找到 {len(files)} 个 DISTILL 文件)")
    all_ok = True
    for f in files:
        ok = verify_file(str(f))
        if not ok:
            all_ok = False
    return all_ok

# ═════════════════════════════════════════════════════
# 汇总
# ═════════════════════════════════════════════════════
def print_summary():
    total = PASS + FAIL + WARN
    rate = (PASS / total * 100) if total > 0 else 0
    print(f"\n{'='*60}")
    print(f"  📊 验证汇总")
    print(f"  ✅ PASS: {PASS}")
    print(f"  ⚠️  WARN: {WARN}")
    print(f"  ❌ FAIL: {FAIL}")
    print(f"  📈 通过率: {rate:.1f}%")
    print(f"{'='*60}")
    if FAIL == 0:
        print(f"\n  🎉 全部通过 ✅ — DISTILL 卡可入库（AI_DRAFT 状态）")
        print(f"  ⚠️  下一步：人工签字 → AI_SIGNED → production")
    else:
        print(f"\n  ⚠️  {FAIL} 项失败，请检查上方 ❌")
        for r in results:
            if "❌" in r:
                print(f"     {r}")

# ═════════════════════════════════════════════════════
# CLI
# ═════════════════════════════════════════════════════
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="verify_kg2sr.py · DISTILL 卡验证器")
    parser.add_argument("--file", help="验证单个 YAML")
    parser.add_argument("--dir",  help="批量扫描目录")
    args = parser.parse_args()

    if args.file:
        verify_file(args.file)
    elif args.dir:
        scan_dir(args.dir)
    else:
        # 默认：扫描 asset_cards 目录
        default = "/data/workspace/domains/asset_cards"
        scan_dir(default)

    print_summary()
    sys.exit(0 if FAIL == 0 else 1)
