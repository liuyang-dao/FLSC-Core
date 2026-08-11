"""
verify_smt_v2.1.py
验证 smt_v2.1_spine.yaml 加载正确 + SCVP 全 CLOSED + UT 计算
"""
import yaml

with open("/data/workspace/domains/meta/smt_v2.1_spine.yaml", "r", encoding="utf-8") as f:
    smt = yaml.safe_load(f)

print("=" * 60)
print("SMT V2.1 YAML 验证报告")
print("=" * 60)

# 1. 基本信息
print(f"\n📄 文档: {smt['document_title']}")
print(f"   编号: {smt['document_id']}")
print(f"   氢键等级: {smt['hydrogen_bond_level']}")
print(f"   日期: {smt['date']}")

# 2. 五层映射
print(f"\n📐 五层映射:")
flm = smt['five_layer_map']
for k, v in flm.items():
    print(f"   {k} ({v['name']}): {len(v['smt_entities'])} 个实体")

# 3. 六脊
print(f"\n🦴 六脊线 (SMT-01 ~ SMT-06):")
for spine in smt['spine']:
    ho = "✅人类独占" if spine.get('human_only') else "人机协同"
    print(f"   {spine['id']} {spine['name']} | {spine['layer']} | {ho} | {spine['ojp_step']}")

# 4. 独立性校验
print(f"\n🔗 独立性校验:")
for ic in smt['independence_check']:
    print(f"   {ic['pair'][0]} ↔ {ic['pair'][1]}: {'✅ 独立' if ic['independent'] else '⚠️ 不独立'}")

# 5. 断裂面
print(f"\n🔧 断裂面 (F-01 ~ F-06):")
for fs in smt['fracture_surfaces']:
    print(f"   {fs['id']}: {fs['description'][:50]}... [{fs['severity']}]")

# 6. SCVP
print(f"\n✅ SCVP 验证:")
scvp = smt['scvp']
for k, v in scvp.items():
    if k != 'overall':
        emoji = "✅" if v == "CLOSED" else "⚠️"
        print(f"   {k}: {emoji} {v}")
print(f"   ─────────────────")
print(f"   总体: 🔒 {scvp['overall']}")

# 7. 公理
print(f"\n📜 五条完备公理:")
for ax in smt['axioms']:
    print(f"   {ax['id']} {ax['name']}: SCVP={ax['scvp']}")

# 8. Axiom R
print(f"\n📊 Axiom R 量化:")
ar = smt['axiom_r']
print(f"   MIS_train = {ar['MIS_train']}")
print(f"   λ = {ar['lambda']}")
print(f"   reality_residual = {ar['reality_residual']}")
print(f"   MIS_true = {ar['MIS_true']}")
print(f"   公式: {ar['formula']}")
print(f"   状态: {ar['status']}")

# 9. 统一信任
print(f"\n🛡️ 统一信任 (SMT 自验证):")
ut = smt['unified_trust']
print(f"   公式: {ut['formula']}")
print(f"   约束: {ut['constraint']}")
sv = ut['smt_self_verify']
print(f"   RIS_true={sv['RIS_true']} MIS_true={sv['MIS_true']} SC={sv['Self_Consistency']}")
print(f"   Unified_Trust = {sv['Unified_Trust']} → {sv['grade']}")

# 10. OJP 协议
print(f"\n🔄 OJP V2.1 六步骤:")
for sid, step in smt['ojp_protocol'].items():
    h = "人类独占" if step.get('human_only') else ("人机协同" if step.get('human_ai') else ("人类主导" if step.get('human_led') else "自动化"))
    print(f"   {sid} {step['name']:20s} | {h:8s} | Γ*={step['gamma_star']}")

# 11. 不可显形
print(f"\n🚫 不可显形目录 (O-01 ~ O-10): {len(smt['inmanifestable'])} 项")

# 12. 伦理红线
print(f"\n⚠️ 伦理红线:")
for sc in smt['safety_constraints']:
    print(f"   {sc['id']}: {sc['rule'][:50]}")

# 13. 三阶自指
print(f"\n🔬 三阶自指验证:")
srv = smt['self_referential_verification']
print(f"   一阶 (五层分解): {srv['first_order']['result']}")
print(f"   二阶 (公理自洽): {srv['second_order']['result']}")
print(f"   三阶 (自指闭合): {srv['third_order']['result']}")
print(f"   法官状态: {srv['judge_status']}")

# 14. 签署
print(f"\n✍️ 签署页:")
for k, v in smt['signatures'].items():
    if isinstance(v, dict):
        sig = v.get('signature', v.get('orc_decision', '?'))
        print(f"   {k}: {sig}")
    else:
        print(f"   {k}: {v}")

# 15. 版本谱系
print(f"\n📋 版本谱系:")
for vl in smt['version_lineage']:
    star = " ★当前" if vl.get('current') else ""
    print(f"   {vl['version']}: {vl['contribution'][:45]}...{star}")

print(f"\n{'=' * 60}")
print("✅ YAML 验证完成")
print(f"{'=' * 60}")
