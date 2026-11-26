# model training

百炼平台提供覆盖文本、图像、视频、语音及决策模型的全栈训练能力，支持监督微调（SFT）、直接偏好优化（DPO）、持续预训练（CPT）、强化学习（RL）、OPD 蒸馏训练等多种范式。所有训练均基于统一的数据管理底座，并与模型评测、压缩、部署形成闭环。

## 支持的模型与功能

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3.8-27b`、`qwen3.6-flash-2026-04-16`）的 SFT（全参/高效）、DPO（全参/高效）、CPT 全参训练；Qwen3.7-Plus-2026-05-26 仅支持 SFT 全参训练 [千问模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model.md)。  
- **多模态模型**：支持视觉理解（Qwen3-VL）、图生视频（wan2.7-i2v）、文生图/图生图（wan2.7-image-pro、qwen-image-2.0）等场景的 SFT-LoRA 高效微调 [微调图像生成模型](../../raw/model-user-guide/model-training/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）和 Qwen-Audio-TTS（`qwen-audio-3.0-tts-flash`）均仅支持 SFT 高效微调，且需同一发音人多段录音 [CosyVoice模型调优](../../raw/_short/fine-tune-speech-synthesis-model-by-api-961a082a0e1a5d8b.md)。  
- **决策模型**：`decision-model-preview-2026-09-24` 支持微调，输出结构化分类、评分或是非判断，适用于工单分流、内容审核等封闭集合决策任务 [决策模型微调最佳实践](../../raw/model-user-guide/model-training/fine-tuning/decision-model-tuning-guide.md)。  
- **蒸馏与强化学习**：OPD 蒸馏训练支持 Model OPD（纯蒸馏）与 Agentic OPD（含工具调用）；RL 训练需自定义 Rollout/Reward 函数，当前为邀测功能，需联系商务经理开通 [强化学习训练概述](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-training-overview.md)。  

> **注意**：文档 7 和文档 42 中关于 `qwen3.7-plus-2026-05-26` 的支持状态存在矛盾——前者明确标注其 DPO/CPT 为“×”，后者未列出该模型。以文档 7 的表格为准，该模型**不支持 DPO 或 CPT**。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用配置** | `job_name` | 训练任务唯一标识 | 最长 50 字符，建议含模型与场景信息 |
| **数据相关** | `training_datasets` / `validation_datasets` | 训练/验证数据集路径 | 必须为已发布版本的 JSONL 文件（SFT/DPO/CPT）或 ZIP 包（多模态）；仅北京地域支持 OSS 导入 [训练集与评测集](../../raw/model-user-guide/model-training/model-data-overview/training-set-and-evaluation-set.md) |
| **模型选择** | `model`（学生） / `teacher_model`（教师） | OPD 蒸馏必需指定教师模型 | 教师模型必须强于学生模型，且二者同族（如 `qwen3.5-9b` → `qwen3.5-397b-a17b`） [OPD 蒸馏训练配置](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-training-config.md) |
| **训练控制** | `n_epochs`（文本） / `max_steps`（图像/视频） | 控制训练轮数或步数 | 万相模型按 `max_steps`，千问模型按 `n_epochs`；RL 训练需配置 `rollout_extra` 携带参考答案 [微调图像生成模型](../../raw/model-user-guide/model-training/fine-tuning/wan-image-generation-finetune-guide.md) |

## 使用方式

1. **准备数据**：在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)中创建训练集，选择类型（SFT/DPO/CPT）与场景（文本/视觉/视频），按格式要求上传数据（如 SFT 用 ChatML 格式 JSONL，DPO 用 `chosen/rejected` 结构）。日志回流可从 SLS 推理日志自动构建训练数据，但需先完成审计日志与推理日志授权 [日志回流](../../raw/model-user-guide/model-training/model-data-overview/model-log-backflow.md)。  
2. **选择训练方式**：在[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)页面创建任务，根据目标选择 SFT（学做事）、DPO（做得更好）、CPT（补知识）、RL（学推理）或 OPD（低成本继承能力）。推荐递进路径：`CPT → SFT → DPO → RL/OPD`。  
3. **提交任务**：  
   - **控制台**：填写任务名称、选择模型、关联数据集、设置超参（如 `n_epochs=3`），点击提交。  
   - **API**：使用 `dashscope.finetune` SDK，通过 `AgenticRL().run()` 一步提交（支持函数注册、数据上传、任务启动），或分步调用文件上传、任务创建接口 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
4. **监控与验证**：训练中可通过控制台查看 Loss 曲线、GPU 利用率；完成后在[我的模型](https://bailian.console.aliyun.com/model/custom)中管理产出模型，并通过[模型评测](https://bailian.console.aliyun.com/cn-beijing/model/evaluate)对比调优前后效果。

## 限制和注意事项

- **地域限制**：DPO、CPT、OSS 导入、云存储挂载、基线评测、模型压缩、日志回流（除新加坡外）均**仅限华北2（北京）地域**；新加坡仅支持日志回流 [日志回流](../../raw/model-user-guide/model-training/model-data-overview/model-log-backflow.md)。  
- **数据与模型约束**：  
  - 数据集类型（训练集/评测集）创建后不可变更；切换训练方式（如 SFT→DPO）会清空已上传文件 [调优数据上传规则](../../raw/_short/text-generation-tuning-data-upload-rules-28b04d7fad3dfa13.md)。  
  - CosyVoice/Qwen-Audio-TTS 调优必须使用**同一发音人**的录音，混合多发音人将导致音色还原度下降 [CosyVoice模型调优](../../raw/_short/fine-tune-speech-synthesis-model-by-api-961a082a0e1a5d8b.md)。  
- **计费与资源**：API 创建的训练任务**仅支持按 [Token](../concepts/token.md) 计费**，不支持模型训练单元；RL 训练按训练单元小时计费（如 IV 型 24 实例约 984 元/小时），提交前务必通过 `test_functions.py` 完成本地自检 [强化学习提交前自检](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-pre-submission-checklist.md)。  
- **安全合规**：零代码 SFT 可强化模型安全对齐能力，但需确保训练数据符合中国法律法规；敏感问题示例仅用于说明拒绝机制，不可用于生成违法内容 [0 代码强化大模型安全合规能力](../../raw/_short/enhance-the-security-compliance-of-large-models-20037a5f23c7138a.md)。

## 来源文档

- [数据管理](../../raw/model-user-guide/model-training/model-data-overview.md)
- [训练集与评测集](../../raw/model-user-guide/model-training/model-data-overview/training-set-and-evaluation-set.md)
- [模型调优](../../raw/model-user-guide/model-training/fine-tuning.md)
- [数据清洗或增强](../../raw/model-user-guide/model-training/model-data-overview/data-processing.md)
- [千问模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model.md)
- [日志回流](../../raw/model-user-guide/model-training/model-data-overview/model-log-backflow.md)
- [模型调优简介](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/_short/text-generation-tuning-data-upload-rules-28b04d7fad3dfa13.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [微调图像生成模型](../../raw/model-user-guide/model-training/fine-tuning/wan-image-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-speech-synthesis-model.md)
- [微调视频生成模型](../../raw/model-user-guide/model-training/fine-tuning/wan-video-generation-finetune-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/_short/enhance-the-security-compliance-of-large-models-20037a5f23c7138a.md)
- [CosyVoice模型调优](../../raw/_short/fine-tune-speech-synthesis-model-by-api-961a082a0e1a5d8b.md)
- [强化学习](../../raw/model-user-guide/model-training/fine-tuning/rl-overview.md)
- [Qwen-Audio-TTS模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-qwen-audio-tts.md)
- [强化学习训练概述](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习提交前自检](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-pre-submission-checklist.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [OPD 蒸馏训练](../../raw/model-user-guide/model-training/fine-tuning/opd-overview.md)
- [OPD 蒸馏训练概述](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-training-overview.md)
- [Agentic OPD 开发](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [Model OPD 开发](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-model-development-guide.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/model-training/fine-tuning/decision-model-tuning-guide.md)
- [OPD 蒸馏训练配置](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-training-config.md)
- [OPD 蒸馏训练可观测配置与指标参考](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-observable-config.md)
- [模型评测](../../raw/model-user-guide/model-training/model-evaluation-introduction.md)
- [评测任务](../../raw/model-user-guide/model-training/model-evaluation-introduction/evaluation-task-introduction.md)
- [模型评测](../../raw/model-user-guide/model-training/model-evaluation-introduction/model-evaluation-overview.md)
- [创建自定义评测任务](../../raw/_short/create-custom-evaluation-task-ae5244ae7d5f81fe.md)
- [创建基线评测任务](../../raw/_short/create-baseline-evaluation-task-644af05297696563.md)
- [查看评测结果](../../raw/_short/view-evaluation-results-57262b43138e3408.md)
- [人工标注评测](../../raw/_short/evaluation-manual-annotation-d9499dc8f91f52e8.md)
- [排行榜](../../raw/model-user-guide/model-training/model-evaluation-introduction/evaluation-task-introduction/evaluation-leaderboard.md)
- [评测维度](../../raw/model-user-guide/model-training/model-evaluation-introduction/evaluation-dimension-introduction.md)
- [规则评估](../../raw/_short/evaluation-dimension-rule-d98afe2913f0935b.md)
- [大模型评估](../../raw/_short/evaluation-dimension-llm-0e79ce833f170957.md)
- [评测维度](../../raw/_short/evaluation-metrics-e2db7de73abf0cc7.md)
- [我的模型](../../raw/model-user-guide/model-training/my-model-center.md)
- [模型压缩](../../raw/model-user-guide/model-training/model-compression-introduction.md)
- [人工评估](../../raw/_short/evaluation-dimension-manual-f3bd8ee18da624b1.md)


