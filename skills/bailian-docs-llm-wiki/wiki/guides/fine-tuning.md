# fine tuning

百炼平台的 fine tuning 是一种模型定制化能力，允许开发者基于自有数据对基础大模型进行针对性训练，从而提升其在特定业务场景、行业知识或安全合规要求下的表现。它支持多种训练范式（SFT、CPT、DPO、RL、OPD），覆盖文本、图像、视频、语音及决策模型等多种模态，并提供控制台可视化操作与 API 编程两种使用方式。

## 支持的模型/功能

百炼支持多类模型的 fine tuning，按模态和训练方式划分如下：

- **文本生成模型**：支持 SFT、CPT、DPO、RL 和 OPD 四种主流训练方式。Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列（如 `qwen2.5-7b-instruct`）及千问 Plus 等均支持全参与高效（LoRA）训练 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **视觉理解模型（千问VL）**：支持 SFT 训练（如 `qwen3-vl-8b-instruct`），但暂不支持 CPT 与 DPO [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **图像/视频生成模型（万相、千问图像）**：仅支持 SFT 高效微调（LoRA），不支持 CPT/DPO/RL；训练目标聚焦于风格、IP 形象或特效复现 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **语音合成模型（CosyVoice）**：仅支持 `efficient_sft` 方式，且仅限 `cosyvoice-v3-flash` 模型，不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **决策模型**：`decision-model-preview-2026-09-24` 不参与常规 CPT/SFT/DPO 流程，需使用专属微调流程 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。  
- **强化学习（RL）与在线策略蒸馏（OPD）**：为高级训练范式，需通过 SDK 提交，依赖函数计算（FC）与 OpenTelemetry 可观测能力，且仅支持指定模型（如 `qwen3.5-9b`）与地域（北京）[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档中关于“全参训练效果优于高效训练”的推荐（见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)）与实际工程实践存在矛盾——LoRA 高效训练在多数业务场景下已能达成接近全参的效果，且显著降低显存与时间成本；官方推荐应以模型实际支持情况与验证结果为准，而非绝对化表述。

## 关键参数

fine tuning 的核心参数因训练方式与模型类型而异，通用关键参数如下：

- **训练方式（`training_type`）**：`efficient_sft`（LoRA）、`full_sft`、`cpt`、`dpo`、`rl`、`opd`；部分模型仅支持子集（如 CosyVoice 仅支持 `efficient_sft`）。  
- **学习率（`learning_rate`）**：SFT 高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级，CPT 推荐 `1e-5`；RL 训练通常更低（如 `2e-6`）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **循环次数（`n_epochs`）**：文本 SFT 推荐 `1–5` 次（依数据量调整），RL/OPD 通常设为 `1`；图像/视频模型则用 `max_steps` 控制（如 `800` 步）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。  
- **批次大小（`batch_size`）**：文本模型常用 `16` 或 `32`；语音与视频模型常设为 `1`（因输入尺寸大）[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)、[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **LoRA 参数（`lora_rank`, `lora_alpha`, `lora_dropout`）**：默认值分别为 `8`、`16`、`0.1`；图像/视频模型常设更高秩（如 `32`）以捕获复杂模式 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **教师模型（`teacher_model`）**：OPD 必填字段，用于提供 token 级概率分布；须与学生模型同系列且更强（如 `qwen3.5-397b-a17b` → `qwen3.5-9b`）[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 使用方式

fine tuning 支持控制台与 API 两种入口，流程高度一致：

1. **准备数据集**：按训练方式选择格式（SFT 用 `messages` JSONL，DPO 用 `chosen/rejected`，CPT 用纯文本 `{text}`，OPD/RL 需含 `rollout_extra`）；单文件 ≤200 MB（API 上传上限为 300 MB）；所有训练方式均需先上传至百炼平台获取 `file_id` [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
2. **创建训练任务**：  
   - **控制台**：进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)页面 → “创建训练任务” → 选择模型、训练方式、数据集、超参 → 提交 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
   - **API**：调用 `/api/v1/files` 上传数据 → 调用 `/api/v1/fine-tunes` 创建任务，传入 `model`、`training_file_ids`、`training_type`、`hyper_parameters` 等 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
3. **监控与管理**：训练中可查看日志、损失曲线、评估指标；RL/OPD 任务需通过 ARMS 控制台查看 Tracing 与自定义指标 [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)、[在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)。  
4. **部署与调用**：训练完成后，模型自动发布至“我的模型”，可一键部署为 API 服务；调用时使用新模型 ID，无需修改 Prompt 结构 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 限制和注意事项

- **地域限制**：绝大多数 fine tuning 功能（CPT、DPO、RL、OPD、决策模型）仅支持华北2（北京）地域；图像/视频/语音模型亦强制要求北京地域 API Key [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **计费差异**：控制台支持按 [Token](../concepts/token.md)、预付费/后付费训练单元三种计费方式；API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。RL 训练**强制使用训练单元（MTU）**，不支持按 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。  
- **数据与配置约束**：数据集类型（训练集/评测集）创建后不可变更；切换训练方式（如 SFT → DPO）会清空已上传文件；`loss_weight` 字段仅默认支持 Qwen3.5+ 模型，旧版本需联系商务经理 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **模型产物隔离**：CosyVoice 调优产物为独立部署的新模型，`voice` 参数固定为 `default`，不再支持声音复刻或设计；决策模型微调后亦为全新模型实例，非原模型的音色/能力扩展 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)、[决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。  
- **安全与合规**：SFT 是强化模型安全对齐的有效手段，但需确保训练数据符合中国法律法规及阿里云算法安全规范；仅依赖 Prompt 工程或后处理无法替代模型参数层面的安全内化 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)


