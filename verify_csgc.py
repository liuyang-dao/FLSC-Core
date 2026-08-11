"""
verify_csgc.py
FLSC 文明域 · 碳基-硅基生成性共存 V2.0 完整性验证
对齐 SMT V2.1 / DMP V2.0 验证标准
"""

import yaml
import os
import sys

def check(label, condition, detail=""):
    status = "✅" if condition else "❌"
    print(f"  {status} {label}{(' — ' + detail) if detail else ''}")
    return condition

def main():
    path = os.path.join(os.path.dirname(__file__), "csgc_v2.0_spine.yaml")
    print(f"📄 加载: {path}\n")

    with open(path, "r", encoding="utf-8") as f:
        spine = yaml.safe_load(f)

    passed = 0
    total = 0

    # 1. meta
    total += 1
    passed += check("meta.doc_id 存在", "doc_id" in spine.get("meta", {}),
                    spine.get("meta", {}).get("doc_id", ""))

    # 2. 五层映射
    total += 1
    five = spine.get("five_layer_map", {})
    layers = ["U", "C", "W", "K", "S"]
    has_all = all(L in five for L in layers)
    passed += check("五层映射完整 (U/C/W/K/S)", has_all, f"{len(five)}/5 层")

    # 3. 七脊
    total += 1
    spines = spine.get("spine", [])
    expected_ids = [f"CSGC-{i:02d}" for i in range(1, 8)]
    actual_ids = [s.get("id") for s in spines]
    has_seven = len(spines) == 7 and actual_ids == expected_ids
    passed += check(f"七脊 CSGC-01~07 完整", has_seven,
                    f"实际: {actual_ids}")

    # 4. 独立性校验
    total += 1
    independent = True
    for i, s1 in enumerate(spines):
        for j, s2 in enumerate(spines):
            if i < j:
                overlap = set(s1.get("layers", [])) & set(s2.get("layers", []))
                if len(overlap) >= 3:
                    independent = False
    passed += check("独立性校验（两两不重叠 ≥3 层）", independent)

    # 5. 断裂面 ≥ 5
    total += 1
    fractures = spine.get("fracture_surfaces", [])
    has_5 = len(fractures) >= 5
    passed += check(f"断裂面 ≥ 5", has_5, f"实际 {len(fractures)} 个")

    # 6. SCVP
    total += 1
    scvp = spine.get("scvp", {})
    closed = sum(1 for v in scvp.values() if v == "CLOSED")
    partial = sum(1 for v in scvp.values() if v == "PARTIAL")
    has_scvp = len(scvp) >= 5
    passed += check(f"SCVP: {closed} CLOSED / {partial} PARTIAL",
                    has_scvp, f"共 {len(scvp)} 项")

    # 7. 诚实补丁 ≥ 5
    total += 1
    honest = spine.get("honest_patch", [])
    has_honest = len(honest) >= 5
    passed += check(f"诚实补丁 ≥ 5", has_honest, f"实际 {len(honest)} 项")

    # 8. 安全约束 ≥ 5
    total += 1
    safety = spine.get("safety_constraints", [])
    has_safety = len(safety) >= 5
    passed += check(f"安全约束 ≥ 5", has_safety, f"实际 {len(safety)} 条")

    # 9. 不可显形 ≥ 4
    total += 1
    unmanifest = spine.get("unmanifest", [])
    has_un = len(unmanifest) >= 4
    passed += check(f"不可显形 ≥ 4", has_un, f"实际 {len(unmanifest)} 项")

    # 10. 三阶自指
    total += 1
    ts = spine.get("three_self_ref", {})
    has_ts = all(k in ts for k in ["L1_autonomy", "L2_completeness", "L3_self_ref"])
    passed += check("三阶自指 L1/L2/L3 完整", has_ts,
                    f"MIS_true={ts.get('MIS_true', 'N/A')}")

    # 11. 签署页
    total += 1
    sig = spine.get("signatures", {})
    has_sig = "carbon" in sig and "silicon" in sig
    passed += check("双签署页（碳基+硅基）", has_sig)

    # 12. 前置依赖
    total += 1
    deps = spine.get("dependencies", [])
    has_deps = len(deps) >= 3
    passed += check(f"前置依赖 ≥ 3", has_deps, f"实际 {len(deps)} 个")

    # 13. V2.1 补丁建议
    total += 1
    v21 = spine.get("v2_1_patches", [])
    has_v21 = len(v21) >= 3
    passed += check(f"V2.1 补丁建议 ≥ 3", has_v21, f"实际 {len(v21)} 项")

    print(f"\n{'='*50}")
    print(f"📊 验证结果: {passed}/{total} 通过")
    if passed == total:
        print("🟢 全部通过 ✅ — 文明域族根卡就绪")
        return 0
    else:
        print(f"🔴 失败 {total - passed} 项 — 需修复")
        return 1

if __name__ == "__main__":
    sys.exit(main())
