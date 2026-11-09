# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或价值观对齐能力的核心技术手段，支持文本生成、视觉理解、语音合成、图像/视频生成及决策模型等多种模态。其核心方法包括监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）、强化学习（RL）和在线策略蒸馏（OPD），可按需组合使用，形成“CPT → SFT → DPO → RL/OPD”的递进式优化路径。

## 支持的模型与功能

百炼支持多模态、多任务的 fine tuning，但不同模型支持的训练方式存在显著差异：

- **文本生成模型**（如 Qwen3 系列、Qwen2.5 系列）：全面支持 CPT、SFT（全参/高效）、DPO（全参/高效）及 RL；其中 Qwen3-32B、Qwen3-14B、Qwen3-8B 等主流型号均支持全部五种方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型**（千问VL系列）：仅支持 SFT 和 DPO，不支持 CPT 或 RL [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型**（万相系列）：仅支持 SFT-LoRA 高效微调，不支持 CPT、DPO、RL 或 OPD；且万相与千问图像模型的超参控制逻辑不同（万相用 `max_steps`，千问用 `n_epochs`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**（CosyVoice）：仅支持 SFT 高效微调（`efficient_sft`），不支持 CPT、DPO、RL 或 OPD，且训练产物为单音色独立模型，无法切换音色 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**（`decision-model-preview-2026-09-24`）：不参与常规 CPT/SFT/DPO 训练流程，需通过专属微调入口，且仅支持 SFT 高效训练 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

> **注意**：文档 1 和文档 5 的表格中，Qwen3.7-Plus-2026-05-26 在“CPT全参训练”列标记为 ×，但文档 4 的“步骤一：选择调优方式”明确说明“CPT（继续预训练）目的是通过海量的无标记训练数据，提升模型在特定行业的表现”，且未排除该模型。结合文档 1 中“**说明**Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”的提示，该模型的 CPT 支持可能为邀测或白名单功能，实际可用性需以控制台实时选项为准。

## 关键参数

不同训练方式的关键参数差异较大，开发者应严格依据场景选择：

- **通用超参**（SFT/DPO/CPT）：`learning_rate`（默认 `3e-4`）、`n_epochs`（默认 `3`，范围 [1, 200]）、`batch_size`（默认值推荐）、`max_length`（默认 `8192`，范围 [500, 131072]）、`lora_rank`（LoRA 秩，默认 `8`）、`lora_alpha`（LoRA 缩放因子，默认 `16`）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **RL 特有超参**：`algorithm`（如 `gspo`）、`kl_loss_coef`（KL 散度系数，默认 `0.002`）、`n_rollouts`（每步采样轨迹数）、`ppo_mini_batch_size`（PPO 小批量大小）[强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。
- **OPD 特有超参**：`teacher_model`（必填，指定教师模型）、`opd_teacher_*` 系列参数（控制教师模型前向行为）[OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。
- **图像/视频生成特有超参**：万相模型使用 `max_steps`（训练总步数，建议 ≥500）而非 `n_epochs`；千问图像模型则使用 `n_epochs` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 使用方式

fine tuning 可通过控制台或 API 两种方式发起，选择依据为开发成熟度与自动化需求：

- **控制台**：适合快速验证、零代码场景及初次使用者。流程为：进入[模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning) → 创建训练任务 → 选择训练方式（SFT/DPO/CPT/RL/OPD）→ 选择模型 → 配置超参 → 绑定训练/验证数据集 → 开始训练 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API**：适合 CI/CD 集成、批量任务管理及复杂函数开发（如 RL Rollout/Reward、OPD Agentic Rollout）。需先上传数据（`POST /api/v1/files`），再创建训练任务（`POST /api/v1/fine-tunes` 或 `AgenticRL().run(...)`）[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。RL 和 OPD 必须通过 API（SDK）提交，因其依赖自定义函数组件 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[OPD 蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

## 限制和注意事项

- **地域限制**：绝大多数 fine tuning 功能（除基础 SFT 外）仅支持华北2（北京）地域，包括 CPT、DPO、RL、OPD、决策模型微调、万相/千问图像/视频生成微调及 CosyVoice 微调 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **计费差异**：
  - 控制台任务支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种方式；API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - RL 训练**强制要求使用模型训练单元（MTU）**，不支持按 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
- **数据格式强约束**：SFT 必须为 JSONL 格式 ChatML messages 结构；DPO 需 `chosen`/`rejected` 字段；CPT 为纯文本 `{text}`；RL 数据需含 `rollout_extra`；OPD 数据需含 `messages` 和 `rollout_extra.solution` [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **模型能力边界**：fine tuning **无法扩展基础模型的固有能力**，例如 CosyVoice 调优不能新增语种支持，万相微调不能改变其文生图/图生图的底层架构 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [OPD 蒸馏训练](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [OPD 蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [OPD 蒸馏训练可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)


