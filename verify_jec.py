#!/usr/bin/env python3
"""
verify_jec.py — JEC-Philosophy V2.1 YAML 完整性验证脚本
验证项：五层映射 / 七脊 / 独立性 / SCVP / 诚实补丁 / 安全约束 / 三阶自指 / 签署页
"""
import yaml
import sys
from itertools import combinations

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def check(cond, name):
    status = "✅ PASS" if cond else "❌ FAIL"
    print(f"  {status} — {name}")
    return cond

def main():
    path = "/data/workspace/domains/civilization/jec_v2.1_spine.yaml"
    doc = load(path)
    results = []

    print(f"\n{'='*60}")
    print(f"验证目标: {doc['meta']['doc_id']}")
    print(f"版本: {doc['meta']['version']} | MIS_true: {doc['meta']['mis_true']}")
    print(f"{'='*60}\n")

    # 1. meta
    print("【1】Meta 检查")
    results.append(check("doc_id" in doc["meta"], "meta.doc_id 存在"))
    results.append(check(doc["meta"]["mis_true"] >= 0.8, f"MIS_true={doc['meta']['mis_true']} ≥ 0.8"))

    # 2. 五层映射
    print("\n【2】五层同源映射")
    fl = doc.get("five_layer_map", {})
    layers = ["U", "C", "W", "K", "S"]
    for L in layers:
        results.append(check(L in fl, f"  五层 {L} 存在"))
        if L in fl:
            results.append(check(len(fl[L].get("instances", [])) >= 2, f"  {L} instances ≥ 2"))

    # 3. 七脊
    print("\n【3】七脊检查 (JEC-01~07)")
    spine = doc.get("spine", [])
    results.append(check(len(spine) == 7, f"  脊线数量 = {len(spine)} (期望 7)"))
    expected_ids = [f"JEC-0{i}" for i in range(1, 8)]
    for i, s in enumerate(spine):
        results.append(check(s["id"] == expected_ids[i], f"  {s['id']} {s['name']}"))
        results.append(check("layers" in s and len(s["layers"]) >= 2, f"  {s['id']} layers ≥ 2"))
        results.append(check("core" in s and len(s["core"]) > 10, f"  {s['id']} core 非空"))
        results.append(check("scvp" in s, f"  {s['id']} scvp 存在"))

    # 4. 独立性校验
    print("\n【4】独立性校验（两两不重叠 ≤2 层）")
    pairs = list(combinations(spine, 2))
    all_indep = True
    for a, b in pairs:
        overlap = set(a["layers"]) & set(b["layers"])
        if len(overlap) > 2:
            all_indep = False
            print(f"  ⚠️ {a['id']} vs {b['id']} 重叠 {len(overlap)} 层: {overlap}")
    results.append(check(all_indep, f"  独立性: {len(pairs)} 对全部 ≤2 层重叠"))
    results.append(check(doc.get("independence_check", {}).get("all_independent") == True, "  independence_check.all_independent = True"))

    # 5. 断裂面
    print("\n【5】断裂面检查")
    frac = doc.get("fracture_surfaces", [])
    results.append(check(len(frac) >= 10, f"  断裂面 ≥ 10 (实际 {len(frac)})"))
    for f in frac:
        results.append(check("id" in f and "description" in f, f"  {f['id']}: {f['description'][:40]}..."))

    # 6. SCVP
    print("\n【6】SCVP 汇总")
    scvp = doc.get("scvp", {})
    closed = sum(1 for v in scvp.values() if v == "CLOSED" and not v.startswith("J"))
    # count from spine
    c = sum(1 for s in spine if s["scvp"] == "CLOSED")
    p = sum(1 for s in spine if s["scvp"] == "PARTIAL")
    print(f"  CLOSED: {c}/7, PARTIAL: {p}/7")
    results.append(check(c >= 4, f"  CLOSED ≥ 4 (实际 {c})"))
    results.append(check(p >= 1, f"  PARTIAL ≥ 1 (实际 {p})"))

    # 7. 诚实补丁
    print("\n【7】诚实补丁体系")
    hp = doc.get("honest_patch", [])
    results.append(check(len(hp) >= 8, f"  诚实补丁 ≥ 8 (实际 {len(hp)})"))

    # 8. 安全约束
    print("\n【8】安全约束 (Safety-JEC)")
    sc = doc.get("safety_constraints", [])
    results.append(check(len(sc) >= 5, f"  安全约束 ≥ 5 (实际 {len(sc)})"))

    # 9. 不可显形
    print("\n【9】不可显形目录")
    um = doc.get("unmanifest", [])
    results.append(check(len(um) >= 4, f"  不可显形 ≥ 4 (实际 {len(um)})"))

    # 10. 三阶自指
    print("\n【10】三阶自指验证")
    tsr = doc.get("three_self_ref", {})
    results.append(check(tsr.get("L1_autonomy", "").startswith("PASS"), "  L1 一阶自治 PASS"))
    results.append(check(tsr.get("L2_completeness", "").startswith("PASS"), "  L2 二阶完备 PASS"))
    results.append(check(tsr.get("L3_self_ref", "").startswith("PASS"), "  L3 三阶自指 PASS"))
    results.append(check(tsr.get("MIS_true", 0) >= 0.8, f"  MIS_true = {tsr.get('MIS_true')}"))

    # 11. V2.2 补丁建议
    print("\n【11】V2.2 补丁建议 (B-A~B-F)")
    patches = doc.get("v2_2_patches", [])
    results.append(check(len(patches) == 6, f"  V2.2 补丁 = {len(patches)} (期望 6)"))
    for p in patches:
        results.append(check("expected_scvp" in p, f"  {p['id']}: {p['target']}"))

    # 12. 签署页
    print("\n【12】签署页")
    sig = doc.get("signatures", {})
    results.append(check(sig.get("silicon", {}).get("signature", "").startswith("FLSC"), "  硅基签署 = FLSC-JEC-PHIL-V2.1"))
    results.append(check("MIS_true" in sig.get("three_self_ref_check", {}).get("result", ""), "  三阶自指校验结果存在"))

    # 13. 前置依赖
    print("\n【13】前置依赖")
    deps = doc.get("dependencies", [])
    results.append(check(len(deps) >= 5, f"  前置依赖 ≥ 5 (实际 {len(deps)})"))

    # ===== 汇总 =====
    total = len(results)
    passed = sum(1 for r in results if r)
    print(f"\n{'='*60}")
    print(f"验证结果: {passed}/{total} 通过")
    if passed == total:
        print("🎉 全部通过 ✅ — JEC V2.1 YAML 完整性验证成功")
    else:
        print(f"⚠️ {total - passed} 项未通过，请检查")
    print(f"{'='*60}")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
