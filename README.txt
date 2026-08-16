FLSC 四卡 + PMS 集成 Agent 完整交付包
==========================================

文件清单（8 个文件）：

1. SR-AI-STAFF-PMS-V1.0.yaml   (20KB)  AI员工记忆脊线资产卡
2. integrated_demo.py             (70KB)  四卡+PMS集成Demo（5场景全跑通）
3. verify_integrated_agent.py     (24KB)  集成验证器
4. SR-CODE-PYTHON-V1.1.yaml     (12KB)  Python编码领域卡
5. SR-EXPERT-WANG-ARCH-V1.0.yaml (12KB) 老王稳态专家卡
6. SR-EXPERT-HUMOR-V1.0.yaml    (14KB)  幽默情感卡
7. README.md                      (22KB)  asset_cards/ 目录说明
8. ROOT_README.md                (27KB)  根目录README（上传时改名README.md）

GitHub 上传步骤：
  git add domains/asset_cards/
  git commit -m "add: 🤖 四卡+PMS集成Agent (100+✅, SR-AI-STAFF-PMS记忆脊线)"
  git push

验证：
  python verify_integrated_agent.py
  预期：7 Section · 100+ PASS · 0 FAIL

架构：
  领域卡(SR-CODE) → 保下限(安全红线)
  专家卡(SR-EXPERT-WANG) → 定上限姿态(保守选型/why_comment)
  幽默卡(SR-EXPERT-HUMOR) → 有温度(时机/共情/自嘲)
  记忆卡(SR-AI-STAFF-PMS) → 可传承(血统/演化/检索/降级)
  + PersonalMemorySystem V3.0 共享运行时 → 老王退休知识不流失

MIS_true 对比：
  领域卡 0.86 / 专家卡 0.83 / 幽默卡 0.78 / 记忆卡 0.84
