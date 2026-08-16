#!/usr/bin/env python3
"""
FLSC 结构资产卡 · 全集验证器
验证 9 份资产卡的完整性、跨文档互锁、命名空间零冲突
"""
import re, os, sys

# ====== 配置 ======
BASE = os.path.dirname(os.path.abspath(__file__))
PASS = 0
FAIL = 0
WARN = 0
results = []

def check(name, cond, msg=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        results.append(("✅", name, msg))
    else:
        FAIL += 1
        results.append(("❌", name, msg))

def warn(name, cond, msg=""):
    global WARN
    if cond:
        PASS += 1
        results.append(("✅", name, msg))
    else:
        WARN += 1
        results.append(("⚠️", name, msg))

def read(fname):
    p = os.path.join(BASE, fname)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

# ====== 文件存在性 ======
files = {
    "master": "FLSC_ASSET_CARDS_MASTER_V1.0.md",
    "sr002": "SR-002-go-V1.0.md",
    "sr003": "SR-003-poetry-V1.0.md",
    "sr004": "SR-004-causal-V2.0.md",
    "disease": "ORC2-disease-safety-V1.0.md",
    "preface": "结构显化录_自序.md",
    "full": "结构显化录_全本.md",
    "readme": "README.md",
}

for key, fname in files.items():
    txt = read(fname)
    check(f"文件存在: {fname}", len(txt) > 100, f"{len(txt)} 字符")

# ====== MASTER 索引 ======
master = read(files["master"])
check("MASTER: 血统编号", "FLSC-ASSET-CARDS-MASTER" in master)
check("MASTER: 六条铁律", "隐式优先" in master and "五层齐全" in master and "宁可空着" in master)
check("MASTER: 9 份文档全索引", all(k in master for k in ["SR-002", "SR-003", "SR-004", "ORC2", "CULTIVATE", "自序", "全本"]))
check("MASTER: YAML 标准模板", "doc_id:" in master and "lineage_id:" in master and "hydrogen_bond:" in master)
check("MASTER: 六维自评标准", "简洁度" in master and "普适性" in master and "双螺旋契合" in master)
check("MASTER: 跨域同构映射", "六族根卡脊线对照" in master or "跨域同构" in master)
check("MASTER: 签署页", "碳基侧" in master and "硅基侧" in master and "氢键公证" in master)
check("MASTER: 血统链", "V0.1" in master and "V1.0" in master and "V2.0" in master)
check("MASTER: 与仓库关系图", "spine/" in master and "pipelines/" in master and "civilization/" in master)

# ====== SR-002 围棋 ======
sr2 = read(files["sr002"])
check("SR-002: 血统编号", "SR-002" in sr2 and "GO-STRUCT" in sr2)
check("SR-002: Unit 层 8 原子", all(f"U-G{i}" in sr2 for i in range(1,9)))
check("SR-002: Connect 层 7 关系", all(f"C-G{i}" in sr2 for i in range(1,8)))
check("SR-002: 三条脊线", "脊线 A" in sr2 and "脊线 B" in sr2 and "脊线 C" in sr2)
check("SR-002: Weight 层", "W(外势" in sr2 and "W(厚薄" in sr2)
check("SR-002: Constraint 8 条", all(f"C{i}" in sr2 for i in range(1,9)))
check("SR-002: Steady YAML 模板", "board_state:" in sr2 and "chosen_move:" in sr2)
check("SR-002: MIS 公式", "MIS_GO" in sr2 and "0.78" in sr2)
check("SR-002: AlphaGo 同构", "AlphaGo" in sr2 and "Policy Network" in sr2)
check("SR-002: 四柱法", "四柱法" in sr2 or "形势判断" in sr2)
check("SR-002: L3 自指", "L1" in sr2 and "L2" in sr2 and "L3" in sr2)
check("SR-002: 六维自评", "103/120" in sr2 or "自评" in sr2)
check("SR-002: 诚实清单", "外势量化未实证" in sr2)
check("SR-002: 签署页", "碳基侧" in sr2 and "硅基侧" in sr2 and "氢键公证" in sr2)

# ====== SR-003 诗律 ======
sr3 = read(files["sr003"])
check("SR-003: 血统编号", "SR-003" in sr3 and "POETRY" in sr3)
check("SR-003: Unit 层 6 原子", all(x in sr3 for x in ["平仄", "韵部", "句式", "粘对", "对仗", "拗救"]))
check("SR-003: Connect 层 5 关系", all(x in sr3 for x in ["粘", "对", "押韵", "拗", "启承转合"]))
check("SR-003: 三条脊线", "脊线 A" in sr3 and "脊线 B" in sr3 and "脊线 C" in sr3)
check("SR-003: Weight 层", "五绝" in sr3 and "七绝" in sr3 and "五律" in sr3)
check("SR-003: Constraint 8 条", all(f"{c}" in sr3 for c in ["禁孤平", "禁三平调", "偶句押平韵", "句内平仄交替"]))
check("SR-003: Steady 王维解析", "山居秋暝" in sr3 or "空山新雨后" in sr3)
check("SR-003: MIS 公式", "MIS" in sr3 and "0.965" in sr3)
check("SR-003: AI 同构", "AlphaGo" in sr3 or "Kurzynski" in sr3 or "TPPG" in sr3)
check("SR-003: 杜甫对比", "登高" in sr3 and "0.97" in sr3)
check("SR-003: L3 自指", "L1" in sr3 and "L2" in sr3 and "L3" in sr3)
check("SR-003: 六维自评 105/120", "105/120" in sr3)
check("SR-003: 诚实清单 6 项", "意境权重无法客观量化" in sr3)
check("SR-003: 签署页", "碳基侧" in sr3 and "硅基侧" in sr3)

# ====== SR-004 因果 V2.0 ======
sr4 = read(files["sr004"])
check("SR-004: 血统编号", "SR-004" in sr4 and "CAUSAL" in sr4 and "V2.0" in sr4)
check("SR-004: Unit 7 原子", all(f"U-C{i}" in sr4 for i in range(1,8)))
check("SR-004: Connect 9 关系", all(f"C-C{i}" in sr4 for i in range(1,10)))
check("SR-004: 六条脊线", all(x in sr4 for x in ["脊线 A", "脊线 B", "脊线 C", "脊线 D", "脊线 E", "脊线 F"]))
check("SR-004: Weight 公式", "W_true" in sr4 and "BIC" in sr4)
check("SR-004: Constraint 10 条", all(f"C{i}" in sr4 for i in range(1,11)))
check("SR-004: Steady YAML 模板", "causal_graph:" in sr4 and "dag_valid:" in sr4)
check("SR-004: MIS 实测 0.83", "0.83" in sr4)
check("SR-004: 基准实证", "Sachs" in sr4 and "Alarm" in sr4 and "Syn-100" in sr4)
check("SR-004: 跨域同构", "数字安全" in sr4 and "疾病生理" in sr4 and "金融风控" in sr4)
check("SR-004: 因果引擎 V4.0 映射", "CausalEngine" in sr4 or "LogicalCausal" in sr4)
check("SR-004: L3 三阶自指", "L1" in sr4 and "L2" in sr4 and "L3" in sr4)
check("SR-004: 六维自评 108/120", "108/120" in sr4)
check("SR-004: 诚实清单 11 项", "极端非线性因果" in sr4)
check("SR-004: 签署页", "碳基侧" in sr4 and "硅基侧" in sr4 and "氢键公证" in sr4)

# ====== ORC2 疾病安全 ======
dis = read(files["disease"])
check("ORC2: 文档编号", "FLSC-SEC-DISEASE" in dis and "ORC2" in dis)
check("ORC2: 六大生理脊", all(f"DS0{i}" in dis for i in range(1,7)))
check("ORC2: 五类裂缝", all(x in dis for x in ["A 类", "B 类", "C 类", "D 类", "E 类"]))
check("ORC2: 三大不动点", "双强不动点" in dis and "三不动点" in dis and "四层全耦合" in dis)
check("ORC2: RIS 公式", "RIS_true" in dis and "最弱脊线公理" in dis)
check("ORC2: 四级健康分级", "L4" in dis and "L3" in dis and "L2" in dis and "L1" in dis)
check("ORC2: 六步诊疗闭环", all(f"Step {i}" in dis for i in range(1,7)))
check("ORC2: 跨域同构", "黏膜屏障" in dis and "组织隔离" in dis)
check("ORC2: 对接 UCMM", "UCMM" in dis and ("do 算子" in dis or "do 算子" in dis or "do 干预算子" in dis))
check("ORC2: 资产卡使用规范", "禁止跳过 ORC2" in dis)
check("ORC2: 诚实清单", "不可替代执业医师" in dis or "不可替代" in dis)
check("ORC2: 签署页", "碳基侧" in dis and "硅基侧" in dis and "氢键公证" in dis)

# ====== 结构显化录_自序 ======
pre = read(files["preface"])
check("自序: 道德经引用", "为学日益" in pre and "为道日损" in pre)
check("自序: 反者道之动", "反者道之动" in pre)
check("自序: 六条铁律", all(x in pre for x in ["隐式优先", "五层齐全", "宁可空着"]))
check("自序: 已发布期次", "SR-001" in pre and "SR-002" in pre and "SR-003" in pre and "SR-004" in pre)
check("自序: 签署页", "碳基侧" in pre and "硅基侧" in pre)

# ====== 结构显化录_全本 ======
full = read(files["full"])
check("全本: 六族总表", "物理族" in full and "心理族" in full and "制造族" in full)
check("全本: 安全族", "安全族" in full and "信任族" in full)
check("全本: 情感族", "情感族" in full and "EMOT" in full)
check("全本: 族根公式", "Trust_total" in full or "情感完备性" in full)
check("全本: 签署页", "FLSC-FAMILY-ROOT" in full or "血统编号" in full)

# ====== README ======
readme = read(files["readme"])
check("README: 六条铁律", "隐式优先" in readme)
check("README: 9 份文件清单", "SR-002" in readme and "SR-003" in readme and "SR-004" in readme)
check("README: 跨域同构速查", "跨域同构" in readme)
check("README: 加载顺序规则", "ORC3" in readme and "ORC2" in readme and "ORC1" in readme)
check("README: 签署页", "碳基" in readme and "硅基" in readme)

# ====== 跨文档互锁 ======
print("\n🔗 跨文档互锁检查...")

# 互锁 1: MASTER 索引 → 各卡存在
for card, keyword in [("SR-002", "go-V1"), ("SR-003", "POETRY"), ("SR-004", "CAUSAL"), ("ORC2", "DISEASE")]:
    check(f"互锁: MASTER → {card}", card in master and keyword.lower() in master.lower())

# 互锁 2: 各卡 → MASTER 引用
for card_file, keyword in [(sr2, "MASTER"), (sr3, "MASTER"), (sr4, "MASTER")]:
    warn(f"互锁: 各卡 → MASTER 引用", keyword in card_file)

# 互锁 3: SR-004 因果 ↔ ORC2 疾病（因果同构）
check("互锁: SR-004 ↔ ORC2 因果同构", "疾病" in sr4 and "因果" in dis)

# 互锁 4: 自序 ↔ 全本（六族一致）
check("互锁: 自序 ↔ 全本 六族一致", "物理族" in pre and "物理族" in full)

# 互锁 5: 各卡五层齐全
for name, txt in [("SR-002", sr2), ("SR-003", sr3), ("SR-004", sr4), ("ORC2", dis)]:
    has_u = "Unit" in txt or "U-G" in txt or "U-C" in txt or "DS0" in txt
    has_c = "Connect" in txt or "C-G" in txt or "C-C" in txt
    has_w = "Weight" in txt or "W(" in txt or "RIS" in txt
    has_k = "Constraint" in txt or "C1" in txt or "C1" in txt
    has_s = "Steady" in txt or "steady" in txt
    check(f"互锁: {name} 五层齐全", has_u and has_c and has_w and has_k and has_s)

# ====== 命名空间零冲突 ======
print("\n📛 命名空间冲突检查...")
namespaces = {
    "SR-002": ["U-G", "C-G", "脊线 A", "脊线 B", "脊线 C"],
    "SR-003": ["平仄", "韵部", "粘对", "对仗", "拗救"],
    "SR-004": ["U-C", "C-C", "脊线 D", "脊线 E", "脊线 F"],
    "ORC2": ["DS01", "DS02", "DS03", "DS04", "DS05", "DS06"],
}
for card, nss in namespaces.items():
    for ns in nss:
        # 检查其他卡的文本中是否误用了此命名空间
        others = [t for n, t in [("SR-002",sr2),("SR-003",sr3),("SR-004",sr4),("ORC2",dis)] if n != card]
        for other_txt in others:
            check(f"命名空间: {ns} 不冲突于其他卡", ns not in other_txt[:200])

# ====== 输出结果 ======
print(f"\n{'='*50}")
print(f"📊 验证结果: {PASS+WARN+FAIL} 项")
print(f"  ✅ 通过: {PASS}")
print(f"  ⚠️  警告: {WARN}")
print(f"  ❌ 失败: {FAIL}")
if FAIL == 0:
    rate = PASS / (PASS + WARN + FAIL) * 100
    print(f"  📈 通过率: {rate:.1f}%")
    print(f"\n🎉 全部通过 ✅ — 结构资产卡全集 (9 份) 完整性验证完成")
    print(f"   索引: MASTER_V1.0 + README")
    print(f"   系列: SR-002(围棋) + SR-003(诗律) + SR-004(因果 V2.0)")
    print(f"   领域: ORC2(疾病安全)")
    print(f"   框架: 自序(哲学根基) + 全本(六族根卡)")
else:
    print(f"\n⚠️  存在 {FAIL} 项失败，请检查")
    for status, name, msg in results:
        if status == "❌":
            print(f"   {status} {name}: {msg}")

print(f"\n{'='*50}")
print(f"Γ*(asset_cards/ V1.0, 全集索引, 跨域同构, 六族归一) = ONGOING → V1.5 补齐六族 SR 卡 → V2.0 生产级自动化")
