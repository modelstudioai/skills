# fine tuning

百炼平台的 fine tuning 是面向开发者的核心模型优化能力，支持在文本生成、多模态理解、图像/视频生成及语音合成等场景下，通过监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）和强化学习（RL）等方式，对齐业务需求、提升领域表现、抑制幻觉并增强安全合规性。该能力覆盖全参数与高效（LoRA）两种训练模式，提供控制台可视化操作与 API/CLI 自动化接入双路径。

## 支持的模型与功能

百炼支持多种模态和任务类型的模型调优：

- **文本生成**：Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等，支持 SFT、CPT、DPO 和 RL 四种训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问 VL）**：`qwen3-vl-8b-instruct` 等模型支持 SFT 高效/全参训练，但不支持 DPO 或 CPT [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成**：万相（`wan2.7-image-pro`）与千问图像（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，文生图/图生图均适用 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：万相图生视频模型（如 `wan2.7-i2v`, `wan2.2-kf2v-flash`）仅支持 `efficient_sft`，按首帧或首尾帧模式训练 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：仅 `cosyvoice-v3-flash` 支持 SFT 高效微调，且**控制台暂不支持，必须通过 API 发起**；不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 2 中表格显示 `Qwen3.7-Plus-2026-05-26` 支持 CPT 全参训练，但文档 4 明确指出“CPT 仅支持北京地域”，而文档 2 开头强调“本文档仅适用于华北2（北京）地域”——二者无矛盾；但文档 7 和文档 8 均声明图像/视频微调“仅在华北2（北京）地域可用”，而文档 2 未在表格中显式标注地域限制，易引发误判。实际使用时，所有调优功能（含文本、VL、图像、视频、语音）均强制要求北京地域，此为统一前提。

## 关键参数

不同训练方式与模型类型支持的超参存在显著差异：

- **通用必填参数**（API 创建任务时必须显式指定）：`n_epochs`（文本/SFT/DPO/RL）、`max_steps`（图像万相）、`batch_size`、`max_length`（文本）或 `max_pixels`（多模态），缺失将导致请求失败 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **LoRA 相关参数**（仅高效训练支持）：`lora_rank`（推荐设为模型支持的最大值）、`lora_alpha`、`lora_dropout`；CPT 训练明确**不支持** LoRA 参数 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **RL 特有参数**：`algorithm`（如 `"gspo"`）、`kl_loss_coef`、`n_rollouts`、`ppo_mini_batch_size` 等，需配合自定义 Rollout/Reward 函数使用 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。
- **语音合成专属参数**：`lm_max_epoch` 与 `fm_max_epoch`，共同参与 [Token](../concepts/token.md) 消耗计算，直接影响训练费用 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

- **控制台操作**：适用于快速验证与低频调优。进入[模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，选择训练方法（SFT/CPT/DPO）、模型、数据集，并配置超参。推荐顺序为 `CPT → SFT → DPO` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API/CLI 调用**：适用于自动化流水线与生产集成。需先上传数据（`POST /api/v1/files`），再创建训练任务（`POST /api/v1/fine-tunes`），支持 OSS 挂载、多数据集混合等高级能力 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **RL 专用 SDK 流程**：需安装 DashScope SDK，编写 Rollout（轨迹生成）与 Reward（评分）函数，通过 `AgenticRL().run()` 一键提交，依赖 OpenTelemetry 实现全流程可观测 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)。
- **语音/图像/视频调优**：全部采用 API 方式，数据需打包为 `.zip`（含 `data.jsonl` + 媒体文件），且必须使用北京地域 API Key [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 限制和注意事项

- **地域限制**：所有 fine tuning 功能（含文本、VL、图像、视频、语音）**仅支持华北2（北京）地域**，跨地域 API 调用将失败。
- **计费差异**：
  - 文本/SFT/DPO/CPT：支持按 [Token](../concepts/token.md) 计费、训练单元预付费/后付费；**API 创建任务仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - RL：**仅支持训练单元计费（MTU）**，不支持按 Token [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
  - CosyVoice：训练费用按 Token 计费（0.2 元/千 Tokens），部署费用按模型单元时长计费 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **数据格式强约束**：
  - SFT/DPO 必须为 `jsonl`，每行符合 ChatML `messages` 结构；评测集为 `xlsx` [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - 图像/视频训练数据必须为 `.zip`，内含 `data.jsonl` 和媒体文件；语音训练数据同理，且音频需为 `.wav` 格式 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **模型能力边界**：调优无法扩展基础模型固有能力，例如 CosyVoice 调优不能新增语种支持，万相调优不能改变生成模式（仅限 t2i/i2i） [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)


