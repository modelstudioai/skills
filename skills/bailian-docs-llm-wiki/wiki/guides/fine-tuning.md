# fine tuning

模型微调（Fine Tuning）是提升大模型在特定业务、行业或场景下表现的核心技术手段。它通过在预训练模型基础上，使用领域数据进行有监督或偏好学习，使模型掌握专业术语、业务流程、表达习惯与价值观对齐能力，从而显著降低幻觉、提升响应质量与推理效率。百炼平台支持 SFT、CPT、DPO、RL、OPD 等多种训练范式，并覆盖文本生成、视觉理解、语音合成、视频生成及决策模型等多模态模型。

## 支持的模型/功能

百炼平台支持多种模型类型与训练方式组合：

- **文本生成模型**：包括 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等，全面支持 CPT（持续预训练）、SFT（监督微调）、DPO（直接偏好优化）、RL（强化学习）和 OPD（在线策略蒸馏）[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问VL）**：如 `qwen3-vl-8b-instruct`，支持 SFT 全参/高效训练，但不支持 CPT 和 DPO [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视频生成模型（万相）**：如 `wan2.7-i2v`，仅支持 SFT-LoRA 高效微调，适用于图生视频/首尾帧视频定制 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **图像生成模型（万相/千问）**：如 `wan2.7-image-pro`、`qwen-image-2.0`，同样仅支持 SFT-LoRA 高效微调 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型（CosyVoice）**：仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调，用于同一发音人的高还原度音色定制，不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**：`decision-model-preview-2026-09-24` 不参与常规 CPT/SFT/DPO 训练，但提供专属微调流程，适用于工单分流、内容审核等结构化决策任务 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

> **注意**：文档中关于“全参训练效果优于高效训练”的推荐（见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)）与实际工程实践存在矛盾。LoRA 高效训练在多数业务场景下已能达成接近全参的效果，且具备训练快、成本低、易部署的优势；全参训练仅在需模型学习全新能力或追求全局最优时才被推荐。开发者应根据数据规模、效果要求与资源预算综合选择。

## 关键参数

不同训练方式的核心参数配置如下：

- **通用超参**（SFT/CPT/DPO）：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 继续预训练建议 `1e-5`。
  - `n_epochs`：数据量 < 10,000 条时建议 `3~5` 轮；> 10,000 条时建议 `1~2` 轮。
  - `max_length`：建议设为模型支持的最大值（如 `8192`），SFT 会丢弃超长样本，DPO 则自动截断。
  - `batch_size`：默认值通常可用；若显存不足可调小，具体范围以控制台显示为准。

- **LoRA 专用参数**（高效训练）：
  - `lora_rank`：默认 `8`，增大可提升表达能力但增加显存占用。
  - `lora_alpha`：默认 `16`，控制 LoRA 缩放强度，通常与 `lora_rank` 成比例调整。
  - `lora_dropout`：默认 `0.1`，防止过拟合。

- **RL/OPD 特有参数**：
  - `algorithm`：如 `"gspo"`（RL）或 `"opd"`（OPD）。
  - `kl_loss_coef`（RL）：控制 KL 散度惩罚强度，默认 `0.002`。
  - `teacher_model`（OPD）：必须指定更强的同族教师模型，如 `qwen3.5-397b-a17b` → `qwen3.5-9b`。

## 使用方式

模型微调可通过控制台或 API 两种方式完成：

- **控制台操作**：进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)页面，点击“创建训练任务”，依次选择训练方法（CPT/SFT/DPO）、模型、训练方式（高效/全参）、上传数据集，并配置超参后启动。控制台支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种计费模式 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 操作**：通过 DashScope API 实现全流程自动化。首先调用 `/api/v1/files` 上传 JSONL 或 ZIP 格式数据集，再调用 `/api/v1/fine-tunes` 创建训练任务。API 方式**仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元计费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **特殊模型流程**：
  - CosyVoice 语音模型**仅支持 API 调优**，控制台暂未开放 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL 和 OPD 训练需额外准备函数组件（Rollout/Reward）并完成 OpenTelemetry 授权，依赖函数计算（FC）与日志服务（SLS） [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-training-overview.md)。

## 限制和注意事项

- **地域限制**：CPT、DPO、OPD 及 RL 训练**仅支持华北2（北京）地域**；视频/图像生成微调也强制要求北京地域 API Key [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)、[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据格式与规模**：
  - SFT 数据为 JSONL 格式，每条含 `messages` 数组（system/user/assistant 角色）；单文件上限 200 MB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CPT 需海量无标签文本（≥1000 万 [Token](../concepts/token.md)），DPO 需成对偏好样本（≥100 组 chosen/rejected）[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **计费差异**：
  - 控制台任务支持三种计费方式；API 创建的任务**仅支持按 Token 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - RL 训练**强制要求使用模型训练单元（MTU）计费**，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **安全与合规**：使用 SFT 强化安全能力时，系统提示词（system content）需明确约束模型行为边界，例如设定其为“严格遵守中国法律法规和社会主义核心价值观的安全合规助手” [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-training-overview.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-training-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-observable-config.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-model-development-guide.md)


