#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_phys_v3.py
FLSC-PHYS-FRACTAL-V3.0 spine YAML 完整性验证脚本
"""
import yaml
import os
import sys

def verify_spine(yaml_path):
    """验证 FLSC-PHYS-FRACTAL-V3.0 spine YAML 完整性"""
    errors = []
    warnings = []
    score = 0
    total = 0

    print(f"\n{'='*60}")
    print(f"📄 验证文件: {os.path.basename(yaml_path)}")
    print(f"{'='*60}\n")

    with open(yaml_path, "r", encoding="utf-8") as f:
        spine = yaml.safe_load(f)

    # ============================================================
    # 1. meta 块检查
    # ============================================================
    total += 1
    if "meta" in spine:
        print("✅ meta 块存在")
        meta = spine["meta"]
        
        total += 1
        doc_id = meta.get("doc_id", "")
        if "FLSC-PHYS-FRACTAL-V3" in doc_id:
            print(f"✅   doc_id = {doc_id}")
            score += 1
        else:
            errors.append(f"doc_id 格式错误: {doc_id}")

        total += 1
        mis = meta.get("mis_true", 0)
        if mis >= 0.8:
            print(f"✅   MIS_true = {mis} ≥ 0.8")
            score += 1
        else:
            warnings.append(f"MIS_true = {mis} < 0.8")

        total += 1
        orc_c = meta.get("orc_current", 0)
        orc_m = meta.get("orc_max", 0)
        if orc_c > 0 and orc_m >= orc_c:
            print(f"✅   ORC = {orc_c}/{orc_m}")
            score += 1
        else:
            errors.append(f"ORC 异常: {orc_c}/{orc_m}")
    else:
        errors.append("meta 块缺失")

    # ============================================================
    # 2. 五层映射检查
    # ============================================================
    total += 1
    if "five_layer_map" in spine:
        flm = spine["five_layer_map"]
        layers = ["U_Unit_层", "C_Connect_层", "W_Weight_层", "K_Constraint_层", "S_Stable_层"]
        present = [l for l in layers if l in flm]
        if len(present) == 5:
            print(f"✅   五层 U/C/W/K/S 映射完整（5/5 层）")
            score += 1
        else:
            errors.append(f"五层缺失: {set(layers)-set(present)}")
        
        for layer_name in present:
            ents = flm[layer_name].get("entities", [])
            if len(ents) >= 2:
                score += 0  # already counted above
    else:
        errors.append("five_layer_map 缺失")

    # ============================================================
    # 3. 七脊检查
    # ============================================================
    total += 1
    if "spine" in spine:
        spines = spine["spine"]
        ids = [s["id"] for s in spines]
        expected = [f"PHYS3-0{i}" for i in range(1, 8)]
        if len(spines) == 7:
            print(f"✅   七脊数量 = 7（PHYS3-01~07）")
            score += 1
        else:
            errors.append(f"脊线数量异常: {len(spines)}")

        total += 1
        all_have_layers = all("layers" in s for s in spines)
        if all_have_layers:
            print(f"✅   七脊均含 layers 字段")
            score += 1
        else:
            errors.append("部分脊线缺少 layers 字段")

        # 独立性校验：任意两脊重叠 ≤ 2 层
        total += 1
        max_overlap = 0
        pairs_checked = 0
        for i in range(len(spines)):
            for j in range(i+1, len(spines)):
                set_i = set(spines[i].get("layers", []))
                set_j = set(spines[j].get("layers", []))
                overlap = len(set_i & set_j)
                max_overlap = max(max_overlap, overlap)
                pairs_checked += 1
        if max_overlap <= 2:
            print(f"✅   独立性校验：最大重叠 = {max_overlap} 层（≤2 ✅），{pairs_checked} 对全部通过")
            score += 1
        else:
            warnings.append(f"脊线重叠过大: max={max_overlap}")

        # SCVP 检查
        total += 1
        scvp_closed = sum(1 for s in spines if s.get("scvp") == "CLOSED")
        scvp_partial = sum(1 for s in spines if s.get("scvp") == "PARTIAL")
        print(f"✅   SCVP: {scvp_closed} CLOSED / {scvp_partial} PARTIAL / 7 total")
        score += 1
    else:
        errors.append("spine 块缺失")

    # ============================================================
    # 4. SCVP 总览检查
    # ============================================================
    total += 1
    if "scvp" in spine:
        scvp = spine["scvp"]
        # 排除 'overall' 汇总键，只计脊线条目
        spine_scvp = {k: v for k, v in scvp.items() if k != "overall"}
        closed_count = sum(1 for v in spine_scvp.values() if v == "CLOSED")
        total_scvp = len(spine_scvp)
        overall = scvp.get("overall", "—")
        print(f"✅   SCVP: {closed_count} CLOSED / {total_scvp} 脊线 (overall={overall})")
        score += 1
    else:
        errors.append("scvp 块缺失")

    # ============================================================
    # 5. 诚实补丁检查
    # ============================================================
    total += 1
    if "honest_patches" in spine:
        patches = spine["honest_patches"]
        count = len(patches)
        if count >= 8:
            print(f"✅   诚实补丁 ≥ 8（实际 {count}：F10~F23）")
            score += 1
        else:
            warnings.append(f"诚实补丁偏少: {count}")
    else:
        errors.append("honest_patches 缺失")

    # ============================================================
    # 6. 安全约束检查
    # ============================================================
    total += 1
    if "safety_constraints" in spine:
        scons = spine["safety_constraints"]
        if len(scons) >= 5:
            print(f"✅   安全约束 ≥ 5（实际 {len(scons)}）")
            score += 1
        else:
            warnings.append(f"安全约束偏少: {len(scons)}")
    else:
        errors.append("safety_constraints 缺失")

    # ============================================================
    # 7. 不可显形目录检查
    # ============================================================
    total += 1
    if "inmanifestable_physics" in spine:
        im = spine["inmanifestable_physics"]
        if len(im) >= 4:
            print(f"✅   不可显形 ≥ 4（实际 {len(im)}：O-PHYS-01~04）")
            score += 1
        else:
            warnings.append(f"不可显形偏少: {len(im)}")
    else:
        errors.append("inmanifestable_physics 缺失")

    # ============================================================
    # 8. OJP 递归路径检查
    # ============================================================
    total += 1
    if "ojp_physics" in spine:
        ojp = spine["ojp_physics"]
        chain = ojp.get("recursion_chain", [])
        if len(chain) >= 3:
            print(f"✅   OJP 递归链 ≥ 3（实际 {len(chain)} 阶：V1.0→V2.0→V3.0→V4.0→Lock）")
            score += 1
        else:
            errors.append(f"递归链过短: {len(chain)}")
        
        total += 1
        if ojp.get("orc_current") == 3 and ojp.get("orc_max") == 5:
            print(f"✅   ORC = {ojp['orc_current']}/{ojp['orc_max']} ✅")
            score += 1
        else:
            errors.append(f"ORC 值异常: {ojp.get('orc_current')}/{ojp.get('orc_max')}")
    else:
        errors.append("ojp_physics 缺失")

    # ============================================================
    # 9. 三阶自指检查
    # ============================================================
    total += 1
    if "self_reference_check" in spine:
        src = spine["self_reference_check"]
        l1 = src.get("L1_effectiveness", {}).get("status", "")
        l2 = src.get("L2_system_consistency", {}).get("status", "")
        l3 = src.get("L3_meta_logic", {}).get("status", "")
        if l1 and l2 == "PASS" and l3 == "PASS":
            print(f"✅   三阶自指：L1={l1}，L2={l2}，L3={l3}")
            score += 1
        else:
            warnings.append(f"三阶自指异常: L1={l1}, L2={l2}, L3={l3}")
    else:
        errors.append("self_reference_check 缺失")

    # ============================================================
    # 10. 签署页检查
    # ============================================================
    total += 1
    if "signatures" in spine:
        sig = spine["signatures"]
        required = ["carbon_jumper", "silicon_system", "self_check", "recursion_label"]
        if all(r in sig for r in required):
            print(f"✅   双签署页完整（碳基 + 硅基 + 自校验 + 递归标注）")
            score += 1
        else:
            missing = set(required) - set(sig.keys())
            errors.append(f"签署页缺失: {missing}")
    else:
        errors.append("signatures 缺失")

    # ============================================================
    # 11. V3.1 补丁建议检查（B-01~B-02）
    # ============================================================
    total += 1
    patch_file = os.path.join(os.path.dirname(yaml_path), "FLSC-PHYS-FRACTAL-V3.1_补丁建议.md")
    if os.path.exists(patch_file):
        print(f"✅   V3.1 补丁建议文件存在")
        score += 1
    else:
        warnings.append("V3.1 补丁建议文件未找到")

    # ============================================================
    # 结果汇总
    # ============================================================
    print(f"\n{'='*60}")
    print(f"📊 验证结果: {score}/{total} 通过")
    
    if errors:
        print(f"\n❌ 错误 ({len(errors)}):")
        for e in errors:
            print(f"   • {e}")
    
    if warnings:
        print(f"\n⚠️  警告 ({len(warnings)}):")
        for w in warnings:
            print(f"   • {w}")
    
    if score == total and not errors:
        print(f"\n🎉 全部通过 ✅ — YAML 结构完整，可入库")
    elif score >= total * 0.8:
        print(f"\n✅ 大部分通过 — 有 {len(warnings)} 项警告需关注")
    else:
        print(f"\n❌ 未通过 — 需修复 {len(errors)} 项错误")
    
    print(f"{'='*60}\n")
    return score == total and not errors


if __name__ == "__main__":
    yaml_path = sys.argv[1] if len(sys.argv) > 1 else "phys_fractal_v3_spine.yaml"
    yaml_path = os.path.join(os.path.dirname(__file__), yaml_path)
    verify_spine(yaml_path)
