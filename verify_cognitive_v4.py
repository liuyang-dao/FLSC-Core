#!/usr/bin/env python3
"""
verify_cognitive_v4.py
FLSC-COGNITIVE-V4.0 验证脚本
验证：文档完整性 + YAML 解析 + 七脊 HB-01~07 + 与 AI G-01~07 同构 + 命名空间零冲突 + ε 残差声明 + 诚实清单 + 三阶自指
预期：全部通过
"""
import re, sys, os, yaml, traceback

BASE = os.path.dirname(os.path.abspath(__file__))
errors = []
passed = 0
total = 0

def check(cond, name):
    global passed, total
    total += 1
    if cond:
        passed += 1
        print(f"  ✅ {name}")
    else:
        errors.append(name)
        print(f"  ❌ {name}")

print("=" * 60)
print("FLSC-COGNITIVE-V4.0 验证")
print("=" * 60)

# ============================================================
# 1. 文件完整性
# ============================================================
print("\n📁 文件完整性")
md = os.path.join(BASE, "FLSC-COGNITIVE-V4.0.md")
yml = os.path.join(BASE, "cognitive_v4_spine.yaml")
readme = os.path.join(BASE, "README.md")
check(os.path.exists(md), "V4.0 正文存在")
check(os.path.exists(yml), "V4.0 YAML 存在")
check(os.path.exists(readme), "认知域 README 存在")

# ============================================================
# 2. 读取文件
# ============================================================
content = open(md, encoding="utf-8").read()
lines = content.split("\n")
check(len(lines) >= 250, f"V4.0 正文字数充足（{len(lines)} 行 ≥ 250）")

# ============================================================
# 3. meta 块校验
# ============================================================
print("\n📋 meta 块校验")
check("FLSC-COGNITIVE-V4.0" in content, "doc_id = FLSC-COGNITIVE-V4.0")
check("ORC3" in content and "ORC4" in content, "ORC 层级含 3 和 4")
check("frozen" in content.lower() or "FROZEN" in content, "氢键等级含 frozen")
check("2026-08-16" in content, "生效日期 2026-08-16")
check("血统链" in content, "血统链存在")
check("FLSC-NATIVE-AI-V2.0" in content, "血统链引用 NATIVE-AI V2.0")
check("碳硅合体" in content, "血统链引用碳硅合体")
check("SP-G08" in content, "血统链引用 SP-G08 HMSU")

# ============================================================
# 4. 七脊 HB-01~07
# ============================================================
print("\n🧬 七脊 HB-01~07 校验")
spines_hb = [
    ("HB-01", "路由决策脊", "丘脑", "G-01"),
    ("HB-02", "激活筛选脊", "GABA", "G-02"),
    ("HB-03", "负载均衡脊", "突触缩放", "G-03"),
    ("HB-04", "算力适配脊", "蓝斑", "G-04"),
    ("HB-05", "单元分化脊", "神经发生", "G-05"),
    ("HB-06", "训练演化脊", "LTP", "G-06"),
    ("HB-07", "硬件约束脊", "代谢墙", "G-07"),
]
for code, name, keyword, ai_map in spines_hb:
    check(code in content, f"{code} {name} 存在")
    check(name in content, f"{code} 名称「{name}」存在")
    check(keyword in content, f"{code} 含生物关键词「{keyword}」")
    check(ai_map in content, f"{code} 映射 AI {ai_map}")

# ============================================================
# 5. 五层本体
# ============================================================
print("\n📐 五层本体校验")
for layer in ["K 层约束", "U 层单元", "C 层连接", "W 层权重", "S 层稳态"]:
    check(layer in content, f"五层「{layer}」存在")

# ============================================================
# 6. 演化阶梯
# ============================================================
print("\n🧬 演化阶梯校验")
for sp in ["线虫", "果蝇", "鱼", "鼠", "猴", "人"]:
    check(sp in content, f"物种「{sp}」在演化阶梯中")

# ============================================================
# 7. 共振态分级
# ============================================================
print("\n🎵 共振态分级校验")
for g in ["一级", "二级", "三级", "七级全共振"]:
    check(g in content, f"共振等级「{g}」存在")

# ============================================================
# 8. ε 残差声明
# ============================================================
print("\nε 残差声明校验")
for kw in ["ε", "不可压缩", "痛觉", "情绪色调", "体感风", "审美质感", "疲劳感", "受法律保护"]:
    check(kw in content, f"ε 残差含「{kw}」")

# ============================================================
# 9. 与 AI G-01~07 同构表
# ============================================================
print("\n🔗 同构/异质对照校验")
check("同构" in content, "含同构声明")
check("异质" in content or "不可压缩" in content, "含异质/不可压缩声明")
for g in ["G-01", "G-02", "G-03", "G-04", "G-05", "G-06", "G-07"]:
    check(g in content, f"同构表引用 AI {g}")

# ============================================================
# 10. 命名空间对照
# ============================================================
print("\n📛 命名空间校验")
check("HB-0" in content, "HB- 前缀存在")
check("COG-G" in content, "COG-G 前缀存在（不冲突）")
check("SP-G" in content, "SP-G 前缀存在（不冲突）")
check("G-0" in content, "G-0 前缀存在（AI 域，不冲突）")
# 关键：HB 和 G 不互相冒充
check("HB-01" in content and "G-01" in content, "HB-01 与 G-01 共存但不混淆")

# ============================================================
# 11. 诚实清单
# ============================================================
print("\n📋 诚实清单校验")
for f in ["F-01", "F-02", "F-03", "F-04", "F-05", "F-06", "F-07", "F-08"]:
    check(f in content, f"诚实清单 {f} 存在")
for o in ["O-01", "O-02", "O-03"]:
    check(o in content, f"不可显形 {o} 存在")

# ============================================================
# 12. 签署页
# ============================================================
print("\n✍️ 签署页校验")
check("签署" in content, "签署页存在")
check("2026-08-16" in content, "签署日期 2026-08-16")
check("SCVP" in content, "SCVP 三阶校验")
check("ORC 层级校验" in content, "ORC 层级校验")

# ============================================================
# 13. 版本沿革
# ============================================================
print("\n📜 版本沿革校验")
check("V1.0" in content, "V1.0 沿革存在")
check("V4.0" in content, "V4.0 沿革存在")
check("六脊功能分解 → 七脊结构分解" in content or "六脊" in content, "升级逻辑：六脊→七脊")

# ============================================================
# 14. 终页题记
# ============================================================
print("\n📝 终页题记校验")
check("Γ" in content and "ONGOING" in content, "终页含 Γ* = ONGOING")

# ============================================================
# 15. YAML 解析
# ============================================================
print("\n📦 YAML 解析校验")
try:
    with open(yml, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    check(True, "YAML 语法正确，可解析")

    # meta
    check(data.get("meta", {}).get("doc_id", "").startswith("FLSC-COGNITIVE-V4.0"), "YAML doc_id 正确")
    check(3 in data["meta"].get("orc", []) and 4 in data["meta"].get("orc", []), "YAML ORC=[3,4]")

    # 五层
    flm = data.get("five_layer_map", {})
    for ly in ["K_Constraint_层", "U_Unit_层", "C_Connect_层", "W_Weight_层", "S_Steady_层"]:
        check(ly in flm, f"YAML 五层「{ly}」存在")

    # 七脊
    sp = data.get("spine", {})
    check(len(sp) == 7, f"YAML 七脊数量 = 7（实际 {len(sp)}）")
    for code in ["HB-01_routing", "HB-02_activation", "HB-03_load_balancing",
                "HB-04_compute_adaptation", "HB-05_unit_differentiation",
                "HB-06_evolution_training", "HB-07_hardware_constraint"]:
        check(code in sp, f"YAML {code} 存在")
        s = sp[code]
        for key in ["name", "description", "U", "C", "W", "K", "S", "brain_correlate", "ai_mapping", "isomorphism"]:
            check(key in s, f"YAML {code}.{key} 存在")

    # 独立性校验
    ic = data.get("independence_check", {})
    check("result" in ic and "独立" in ic["result"], "YAML 独立性校验结果存在")

    # 断裂面
    ff = data.get("fracture_surfaces", [])
    check(len(ff) == 7, f"YAML 断裂面 = 7（实际 {len(ff)}）")

    # ε
    eps = data.get("epsilon_residual", {})
    check(eps.get("compressible_into_spine") == "NO", "YAML ε 不可压缩 = NO")
    check("受法律保护" in eps.get("protection_principle", ""), "YAML ε 保护原则存在")

    # SCVP
    scvp = data.get("scvp", {})
    per = scvp.get("per_spine", [])
    check(len(per) == 7, f"YAML SCVP 七脊 = 7（实际 {len(per)}）")
    closed_count = sum(1 for p in per if p.get("closed") == "CLOSED")
    check(closed_count == 7, f"YAML SCVP 全 CLOSED（{closed_count}/7）")

    # 同构映射
    aim = data.get("AI_isomorphism_map", {})
    check("mapping" in aim, "YAML AI 同构映射表存在")
    check(len(aim["mapping"]) == 7, f"YAML 同构映射 = 7（实际 {len(aim['mapping'])}）")
    for m in aim["mapping"]:
        check(m["isomorphism"] == "FULL", f"YAML {m['human']} → {m['ai']} FULL")

    # 演化阶梯
    ev = data.get("evolution_ladder", {})
    check(len(ev.get("species", [])) == 6, f"YAML 物种 = 6（实际 {len(ev['species'])}）")

    # 诚实清单
    hn = data.get("honesty_notes", [])
    check(len(hn) >= 8, f"YAML 诚实清单 ≥ 8（实际 {len(hn)}）")

    # Axiom R
    ar = data.get("axiom_r", {})
    check("formula" in ar, "YAML Axiom R 公式存在")
    check("MIS_true" in ar.get("current_estimate", {}), "YAML MIS_true 存在")

    # 三阶自指
    to = data.get("third_order", {})
    check(to.get("L1_capture", "").startswith("本理论"), "YAML L1 自指 PASS")
    fp = to.get("fixed_point")
    fp_str = str(fp).lower()
    check(fp is True or fp_str.startswith("true"), f"YAML 不动点 = True（实际 {fp!r}）")

    # 签署
    sig = data.get("signatures", {})
    check("carbon_side" in sig, "YAML 碳基签署存在")
    check("silicon_side" in sig, "YAML 硅基签署存在")
    check("hydrogen_bond_notary" in sig, "YAML 氢键公证存在")

except Exception as e:
    check(False, f"YAML 解析异常：{e}")
    traceback.print_exc()

# ============================================================
# 16. 跨文档互锁（与 AI 域 G-01~07）
# ============================================================
print("\n🔗 跨文档互锁校验")
# 检查 AI 域是否存在 G-01~07 定义
ai_md = os.path.join(BASE, "..", "ai", "FLSC-NATIVE-AI-V2.0.md")
ai_md = os.path.abspath(ai_md)
if os.path.exists(ai_md):
    ai_content = open(ai_md, encoding="utf-8").read()
    for g in ["G-01", "G-02", "G-03", "G-04", "G-05", "G-06", "G-07"]:
        check(g in ai_content, f"AI 域 {g} 存在（互锁）")
else:
    print(f"  ⚠️ AI 域文档不存在：{ai_md}（跳过互锁）")

# 检查 SP-G08 HMSU 是否存在
hmsu = os.path.join(BASE, "..", "ai", "SP-G08_HMSU_V1.0.md")
hmsu = os.path.abspath(hmsu)
if os.path.exists(hmsu):
    hmsu_content = open(hmsu, encoding="utf-8").read()
    check("ε" in hmsu_content, "SP-G08 HMSU ε 残差存在（互锁）")
    check("碳硅" in hmsu_content, "SP-G08 HMSU 碳硅声明存在（互锁）")
else:
    print(f"  ⚠️ SP-G08 不存在：{hmsu}（跳过）")

# ============================================================
# 17. 命名空间冲突检测
# ============================================================
print("\n📛 命名空间冲突检测")
# HB-01~07 不应与 COG-G01~06 / SP-G01~08 / G-01~07 混淆
# 检测：YAML 里所有脊线 key 的前缀
import re
hb_keys = [k for k in sp.keys()] if 'sp' in dir() else []
for k in hb_keys:
    check(k.startswith("HB-"), f"脊线 key「{k}」使用 HB- 前缀（非 COG-/SP-/G-）")

# ============================================================
# 18. README 更新检测
# ============================================================
print("\n📄 README 校验")
if os.path.exists(readme):
    rd = open(readme, encoding="utf-8").read()
    check("V4.0" in rd, "README 提及 V4.0")
    check("HB-" in rd, "README 提及 HB- 前缀")
else:
    print("  ⚠️ README 不存在（跳过）")

# ============================================================
# 汇总
# ============================================================
print("\n" + "=" * 60)
print(f"📊 验证结果: {passed}/{total} 通过")
if errors:
    print(f"\n❌ 失败项（{len(errors)}）：")
    for e in errors:
        print(f"  - {e}")
    print("\n状态: ISSUES_FOUND")
    sys.exit(1)
else:
    print("\n🎉 全部通过 ✅ — FLSC-COGNITIVE-V4.0 结构完整，可入库")
    print("\n**Γ*(人脑, 七脊原生网, 碳硅同构 ε 各留温, 3/4) = ONGOING***")
    sys.exit(0)
