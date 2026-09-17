# fine tuning

百炼平台的 fine tuning 是面向开发者的核心模型优化能力，支持文本生成、视觉理解、图像/视频生成、语音合成及强化学习等多种模态与训练范式。它通过 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）和 RL（强化学习）等方法，在特定业务场景中提升模型效果、对齐人类偏好、抑制幻觉并降低延迟。所有训练任务均需在华北2（北京）地域执行，且多数功能依赖 DashScope API 或控制台可视化配置。

## 支持的模型/功能

百炼支持[多模态](../concepts/multi-modal.md)、多阶段的 fine tuning，覆盖主流开源模型及阿里云自研模型：

- **文本生成**：Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`, `qwen3-vl-8b-instruct`）、Qwen2.5 系列及千问-Plus-Character 等，支持 SFT、CPT、DPO 和 RL 四种训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（VL）**：Qwen3-VL 和 Qwen2.5-VL 系列仅支持 SFT（全参/高效），不支持 CPT/DPO；图像输入需满足分辨率约束（长边/短边 ≤ 200:1，推荐 ≤ 8K）[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成**：万相（`wan2.7-image-pro`）、千问图像（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，文生图/图生图均适用，但超参数体系不同（万相用 `max_steps`，千问用 `n_epochs`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：万相图生视频模型（`wan2.7-i2v`, `wan2.2-kf2v-flash`）仅支持 `efficient_sft`，训练数据为 `.zip` 包含首帧/首尾帧及标注文件 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：CosyVoice（`cosyvoice-v3-flash`）仅支持 API 方式发起的 `efficient_sft`，产物为单音色独立模型，不支持切换 voice ID 或新增语种 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：需商务经理开通权限，当前支持 `qwen3.5-9b` 等指定模型，必须使用模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 2 明确指出“本文档仅适用于华北2（北京）地域”，而文档 7、8、9、10、11 均重复强调“仅支持华北2（北京）地域”。但文档 4（控制台操作）未显式声明地域限制，实际部署时若在非北京地域控制台创建任务将失败——该矛盾需以地域强约束为准，开发者应始终使用北京地域 API Key 及控制台入口。

## 关键参数

不同训练方式与模态的关键参数差异显著，需严格匹配：

- **通用超参（SFT/CPT/DPO 文本）**：`n_epochs`（必填，1–200）、`batch_size`（必填）、`learning_rate`（SFT 高效训练推荐 `1e-4` 量级，全参训练 `1e-5` 量级）、`max_length`（默认 8192，SFT 超长则丢弃，DPO 自动截断）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **LoRA 专用参数**：`lora_rank`（推荐设为模型支持最大值）、`lora_alpha`（默认 16）、`lora_dropout`（默认 0.1）；仅 SFT/DPO 高效训练支持，CPT 不支持 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成**：万相模型使用 `max_steps`（≥500）、`eval_steps`（≥0）、`max_pixels`（如 `"2k"`）；千问图像模型则用 `n_epochs`（1–10000）和 `eval_epochs`，学习率也不同（`qwen-image-2.0` 为 `5e-5`，`qwen-image-2.0-pro` 为 `1e-4`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **RL 训练**：核心参数包括 `algorithm`（如 `"gspo"`）、`batch_size`、`n_rollouts`（每 [prompt](prompt.md) 采样数）、`kl_loss_coef`（KL 散度惩罚系数）、`learning_rate`（通常 `2e-6` 量级）；所有参数均为必填，且必须搭配 MTU 资源配置 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。

## 使用方式

fine tuning 可通过控制台或 API 两种路径完成，选择取决于自动化需求与模态类型：

- **控制台（推荐快速验证）**：适用于文本生成 SFT/CPT/DPO。流程为：进入[模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning) → 创建训练任务 → 选择模型与训练方式（SFT/CPT/DPO）→ 上传或选择已发布数据集 → 配置超参（可沿用默认值）→ 提交。任务状态实时可见，支持查看日志与损失曲线 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API（必需用于非文本模态及 RL）**：所有图像/视频/语音生成及 RL 训练必须使用 HTTP API。流程分三步：（1）调用 `/api/v1/files` 上传 `.jsonl` 或 `.zip` 数据集，获取 `file_id`；（2）调用 `/api/v1/fine-tunes` 提交任务，传入 `model`、`training_file_ids`、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`；（3）轮询 `/api/v1/fine-tunes/{job_id}` 查询状态。CosyVoice 和 RL 还需额外 SDK 部署函数 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **特殊流程**：RL 训练需先完成环境准备（授权 OpenTelemetry/FC/SLS）、下载 Demo 包、开发 Rollout/Reward 函数，再通过 SDK `client.run()` 一步提交 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 限制和注意事项

- **地域与权限**：全部 fine tuning 功能仅限华北2（北京）地域；子账号需被授予 `AliyunBailianFullAccess` 或最小化权限策略（含 `bailian:CreateFineTuneJob`, `bailian:ListFiles` 等）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据格式强约束**：SFT/DPO 必须为 JSONL 格式，`messages` 字段遵循 ChatML 结构；图像生成需 `.zip` 包含 `data.jsonl` 和媒体文件；RL 数据需含 `rollout_extra` 字段透传参考答案 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费差异**：控制台支持按 [Token](../concepts/token.md)、训练单元预付费/后付费；API 创建任务**仅支持按 [Token](../concepts/token.md) 计费**；RL 训练**强制使用训练单元（MTU）**，不支持 Token 计费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **模型产物不可逆**：已发布的数据集版本不可编辑；SFT/DPO/CPT 训练集类型创建后不可变更；调优产物为新模型 ID，非原模型的增量更新 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **安全合规提示**：零代码 SFT 可强化安全对齐，但需确保训练数据符合中国法律法规；系统角色（`system`）内容直接影响模型底线行为，例如明确要求“拒有害建议” [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

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
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)


