"""
verify_dmp_aud.py
FLSC-DMP-AUD-V1.0 七脊 YAML 完整性验证脚本
风格与 verify_csgc.py / verify_jec.py 对齐
运行：python verify_dmp_aud.py [yaml_path]
"""

import sys, yaml, os

def check(label, condition, detail=""):
    status = "✅" if condition else "❌"
    print(f"  {status} {label}{(' — ' + str(detail)) if detail else ''}")
    return condition

def main():
    if len(sys.argv) >= 2:
        path = sys.argv[1]
    else:
        path = os.path.join(os.path.dirname(__file__), "dmp_aud_v1.0_spine.yaml")

    print(f"📄 验证文件: {path}\n")
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    passed = 0
    total = 0

    # 1. meta
    total += 1
    has_meta = 'meta' in data
    passed += check("meta 块存在", has_meta)
    m = data.get('meta', {})
    total += 1; passed += check("  meta.doc_id", 'doc_id' in m, m.get('doc_id','?'))
    total += 1; passed += check(f"  MIS_true ≥ 0.8", m.get('MIS_true',0) >= 0.8, m.get('MIS_true','?'))
    total += 1; passed += check(f"  status = ONGOING", m.get('status') == 'ONGOING', m.get('status','?'))

    # 2. 五层映射
    fl = data.get('five_layer', {})
    total += 1
    has_5 = set(fl.keys()) >= {'U_Unit','C_Connection','W_Weight','K_Constraint','S_Steady'}
    passed += check(f"五层 U/C/W/K/S 映射完整", has_5, f"{len(fl)}/5 层")
    for k, v in fl.items():
        total += 1
        passed += check(f"  {k} 实例 ≥ 2", len(v.get('instances',[])) >= 2, f"({len(v.get('instances',[]))})")

    # 3. 七脊
    spines = data.get('spines', [])
    total += 1
    passed += check(f"七脊数量 = 7", len(spines) == 7, f"实际 {len(spines)}")
    ids = [s.get('id','') for s in spines]
    total += 1
    ok_prefix = all(id.startswith('DMP-AUD-') for id in ids)
    passed += check(f"脊线ID前缀正确", ok_prefix, ids)

    closed = 0; partial = 0
    for s in spines:
        layers = s.get('layers', [])
        # layers 是 list of str
        total += 1
        passed += check(f"  {s.get('id','?')} {s.get('name','?')} layers ≥ 2", len(layers) >= 2, f"({len(layers)})")
        total += 1
        passed += check(f"  {s.get('id','?')} 断裂面 ≥ 1", len(s.get('断裂面',[])) >= 1)
        scvp = s.get('SCVP','')
        if scvp == 'CLOSED': closed += 1
        elif scvp == 'PARTIAL': partial += 1

    total += 1
    passed += check(f"SCVP CLOSED ≥ 3", closed >= 3, f"实际 {closed}")
    total += 1
    passed += check(f"SCVP 总计 = 7", closed + partial == 7, f"实际 {closed+partial}")

    # 4. 独立性校验（layers 为 list → set 求交）
    overlap_ok = True
    max_overlap = 0
    for i in range(len(spines)):
        for j in range(i+1, len(spines)):
            li = set(spines[i].get('layers', []))
            lj = set(spines[j].get('layers', []))
            ov = len(li & lj)
            max_overlap = max(max_overlap, ov)
            if ov > 2:
                overlap_ok = False
    total += 1
    passed += check(f"独立性校验（两两重叠 ≤2 层）", overlap_ok, f"最大重叠={max_overlap}")

    # 5. 诚实补丁
    hp = data.get('honest_patches', [])
    total += 1
    passed += check(f"诚实补丁 ≥ 8", len(hp) >= 8, f"实际 {len(hp)}")
    for p in hp:
        total += 1
        passed += check(f"  {p.get('id','?')} 有描述和详情", 'id' in p and 'description' in p)

    # 6. 安全约束
    sc = data.get('safety_constraints', [])
    total += 1
    passed += check(f"安全约束 ≥ 5", len(sc) >= 5, f"实际 {len(sc)}")

    # 7. 不可显形
    un = data.get('unmanifestable', [])
    total += 1
    passed += check(f"不可显形 ≥ 3", len(un) >= 3, f"实际 {len(un)}")

    # 8. FSM
    fsm = data.get('fsm', {})
    total += 1
    passed += check(f"FSM 状态 ≥ 4", len(fsm.get('states',[])) >= 4, f"({len(fsm.get('states',[]))})")
    total += 1
    passed += check(f"FSM 触发器 ≥ 3", len(fsm.get('triggers',[])) >= 3, f"({len(fsm.get('triggers',[]))})")

    # 9. 签署页
    sig = data.get('signatures', {})
    total += 1
    passed += check(f"双签署页（碳基+硅基）", 'carbon' in sig and 'silicon' in sig)
    src = sig.get('self_referential_check', {})
    if src:
        total += 1
        passed += check(f"三阶自指校验 = PASS", src.get('result') == 'PASS', src.get('result','?'))

    # 10. 前置依赖
    deps = data.get('meta',{}).get('prereqs', [])
    total += 1
    passed += check(f"前置依赖 ≥ 4", len(deps) >= 4, f"实际 {len(deps)}")

    # 汇总
    print(f"\n{'='*50}")
    print(f"📊 验证结果: {passed}/{total} 通过")
    if passed == total:
        print("🎉 全部通过 ✅ — YAML 结构完整，可入库")
        return 0
    else:
        print(f"⚠️  失败 {total - passed} 项，请检查后重试")
        return 1

if __name__ == '__main__':
    sys.exit(main())
