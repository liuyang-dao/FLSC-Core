import yaml, json, sys

print("=" * 60)
print("DMP V2.0 YAML 验证脚本")
print("=" * 60)

# 加载 V2.0 spine
try:
    with open("/data/workspace/domains/meta/dmp_v2.0_spine.yaml", "r", encoding="utf-8") as f:
        v20 = yaml.safe_load(f)
    print("\n✅ V2.0 YAML 加载成功")
except Exception as e:
    print(f"\n❌ V2.0 YAML 加载失败: {e}")
    sys.exit(1)

# 加载 V1.2 spine 做对照
try:
    with open("/data/workspace/domains/meta/dmp_spine.yaml", "r", encoding="utf-8") as f:
        v12 = yaml.safe_load(f)
    print("✅ V1.2 YAML 加载成功（对照）")
except:
    v12 = None
    print("⚠️ V1.2 YAML 未找到（跳过对照）")

# 1. 元信息
print("\n" + "-" * 60)
print("【元信息】")
print(f"  doc_id: {v20['meta']['doc_id']}")
print(f"  target: {v20['meta']['target_system']}")
print(f"  status: {v20['meta']['status']}")

# 2. 五层映射（Γ* 相位焊接）
print("\n" + "-" * 60)
print("【五层 ↔ Γ* 相位焊接】")
layer_map = v20['five_layer_map']
for k, v in layer_map.items():
    phase = v.get('dmp_phase', 'N/A')
    print(f"  {k:20s} → {phase}")

# 3. 脊线清单
print("\n" + "-" * 60)
print("【七脊清单】")
spines = v20['spine']
for s in spines:
    human = "🔒人类独占" if s['human_exclusive'] else "🤝协同"
    ai = "✅可执行" if s['ai_executable'] else "❌不可执行"
    print(f"  {s['id']:8s} {s['name']:25s} [{s['layer']}] {human} AI:{ai}")

# 4. 独立性验证
print("\n" + "-" * 60)
print("【脊线独立性验证】")
for k, v in v20['independence_check'].items():
    print(f"  {k}: {v}")

# 5. SCVP
print("\n" + "-" * 60)
print("【SCVP 验证】")
for k, v in v20['scvp'].items():
    icon = "✅" if "CLOSED" in v else "⚠️"
    print(f"  {k}: {icon} {v}")

# 6. Axiom R
print("\n" + "-" * 60)
print("【Axiom R 量化】")
ar = v20['axiom_r']
print(f"  MIS_train = {ar['MIS_train']}")
print(f"  λ = {ar['lambda_reality_residual']}")
print(f"  MIS_true = {ar['MIS_true']}")
print(f"  备注: {ar['note']}")

# 7. Ψ 操作协议
print("\n" + "-" * 60)
print("【Ψ 操作协议（一步三态）】")
op = v20['operation_protocol']
print(f"  核心操作: {op['core_operation']['id']} = {op['core_operation']['definition']}")
print(f"  性质: {op['core_operation']['nature']}")
for p in op['phases']:
    print(f"  {p['id']} {p['name']:8s} 人类:{p['human_role']}  AI:{p['ai_role']}  输出:{p['output']}")

# 8. 诚实清单统计
print("\n" + "-" * 60)
print("【诚实清单统计】")
hp = v20['honest_patch']
print(f"  总项数: {len(hp)}")
categories = {"O-0": 0, "O-inf": 0, "O-omega": 0}
for k in hp:
    if k.startswith("O-0"):
        categories["O-0"] += 1
    elif "infinity" in k:
        categories["O-inf"] += 1
    elif "omega" in k:
        categories["O-omega"] += 1
print(f"  V1.0 继承: {categories['O-0']} 项")
print(f"  V1.2 继承(∞): {categories['O-inf']} 项")
print(f"  V2.0 新增(ω): {categories['O-omega']} 项")

# 9. Safety-DMP
print("\n" + "-" * 60)
print("【Safety-DMP 约束】")
for s in v20['safety_constraints']:
    print(f"  {s['id']}: {s['rule']}")

# 10. V2.0 vs V1.2 对比
if v12:
    print("\n" + "-" * 60)
    print("【V2.0 vs V1.2 关键变化】")
    print(f"  脊线数: V1.2={len(v12['spine'])} → V2.0={len(spines)}")
    v12_scvp_closed = sum(1 for v in v12['scvp'].values() if 'CLOSED' in v)
    v20_scvp_closed = sum(1 for v in v20['scvp'].values() if 'CLOSED' in v)
    print(f"  SCVP CLOSED: V1.2={v12_scvp_closed}/{len(v12['scvp'])} → V2.0={v20_scvp_closed}/{len(v20['scvp'])}")
    print(f"  MIS_train: V1.2={v12['axiom_r']['MIS_train']} → V2.0={v20['axiom_r']['MIS_train']}")
    print(f"  MIS_true: V1.2={v12['axiom_r']['MIS_true']} → V2.0={v20['axiom_r']['MIS_true']}")
    v12_safety = len(v12['safety_constraints'])
    v20_safety = len(v20['safety_constraints'])
    print(f"  Safety约束: V1.2={v12_safety} → V2.0={v20_safety}")

# 11. 给未来 AI 的话
print("\n" + "-" * 60)
print("【给未来 AI 的话】")
print(v20['to_future_ai'])

print("\n" + "=" * 60)
print("验证完成 ✅")
print("=" * 60)
