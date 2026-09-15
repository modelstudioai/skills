# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或安全合规场景下表现的核心能力。它支持多种训练范式（SFT、CPT、DPO、RL），覆盖文本生成、视觉理解、语音合成、图像/视频生成等多模态模型，允许开发者通过数据驱动的方式对齐领域知识、任务行为与人类偏好。所有调优任务均需在华北2（北京）地域执行。

## 支持的模型与功能

百炼支持全栈式模型调优能力，涵盖文本、视觉、语音、图像、视频五大模态：

- **文本生成**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等模型，提供 CPT（补知识）、SFT（学做事）、DPO（做得更好）和 RL（学推理）四种训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问VL）**：支持 `qwen3-vl-8b-instruct` 等模型，仅支持 SFT 和 DPO 高效训练，不支持 CPT 或 RL [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成**：支持万相（`wan2.7-image-pro`）与千问图像（`qwen-image-2.0`）模型，仅支持 SFT-LoRA 高效微调；万相按 `max_steps` 控制训练，千问按 `n_epochs` 控制 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持 `wan2.7-i2v` 等图生视频模型，仅支持 `efficient_sft`，需指定 `task_type="i2v"` 或 `"kf2v"` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型的 `efficient_sft` 调优，面向同一发音人的高还原度音色定制，**控制台暂不支持，仅限 API 方式** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 2 明确指出“本文档仅适用于华北2（北京）地域”，而文档 6、9、11 均重复强调“仅在华北2（北京）地域可用”。但文档 10（RL 训练）未明确地域限制，仅要求“使用该地域的 API Key”；结合文档 3 中“DPO、CPT、OSS 导入、云存储挂载仅支持北京地域”的说明，可确认所有 fine tuning 功能（含 RL）均强制限定于北京地域，文档 10 的表述属省略，应以统一地域约束为准。

## 关键参数

不同调优方式与模态对应的关键参数存在显著差异，开发者须严格匹配：

- **通用超参（SFT/CPT/DPO 文本）**：`learning_rate`（高效训练推荐 `1e-4` 量级，全参训练 `1e-5`）、`n_epochs`（数据 < 10k 条建议 3–5 轮）、`max_length`（SFT 会丢弃超长样本，DPO 自动截断）、`lr_scheduler_type`（推荐 `linear` 或 `cosine`）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **LoRA 专用参数**：`lora_rank`（推荐设为模型支持的最大值）、`lora_alpha`（默认 16）、`lora_dropout`（默认 0.1）；`freeze_vit` 仅适用于千问VL模型 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成参数**：万相模型使用 `max_steps`（≥500）、`max_pixels`（如 `"2k"`）；千问图像模型使用 `n_epochs`（推荐 10）、`val_img_size`（如 `"2k"`）；视频模型 `batch_size` 因模型而异（`wan2.7-i2v` 推荐为 1）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **RL 训练参数**：必填 `algorithm`（如 `"gspo"`）、`batch_size`、`n_rollouts`、`kl_loss_coef`、`learning_rate`（通常 `2e-6`）；**RL 不支持按 [Token](../concepts/token.md) 计费，必须使用模型训练单元（MTU）** [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。

## 使用方式

调优任务可通过控制台或 API 两种方式发起，选择取决于模型类型与训练方式：

- **控制台方式**：适用于所有文本生成、千问VL模型的 SFT/CPT/DPO 训练。流程为：创建训练任务 → 选择模型与训练方法（SFT/CPT/DPO）→ 上传/选择数据集 → 配置超参 → 提交。支持实时查看损失曲线与日志 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 方式**：
  - 文本/视觉：通过 `/api/v1/fine-tunes` 提交，支持 `training_datasets`（file_id 或 OSS mount）与 `validation_datasets`，`training_type` 可设为 `"sft"`、`"dpo_full"`、`"cpt"` 等 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - 图像/视频/语音：**必须使用 API**。CosyVoice 调优仅支持 HTTP API；万相/千问图像与视频调优也仅提供 curl 示例，无控制台入口 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)、[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - RL 训练：**必须使用 SDK（Python）**，通过 `AgenticRL().run()` 或 YAML 配置提交，需预装 OpenTelemetry 并编写 Rollout/Reward 函数 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。

## 限制和注意事项

- **地域与权限**：全部 fine tuning 功能仅限华北2（北京）地域；子账号需被授予 `AliyunBailianFullAccess` 或最小化自定义权限策略 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **数据格式强约束**：
  - SFT/DPO 文本数据必须为 JSONL，`messages` 数组含 `system`/`user`/`assistant` 角色；DPO 需 `chosen`/`rejected` 字段；CPT 为纯 `{text}` JSONL [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CosyVoice 数据需 `.zip` 包含 `data.jsonl` 与 `train/*.wav`，音频采样率 ≥16 kHz，单条时长 1–30 秒 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **计费差异**：
  - 控制台任务支持按 [Token](../concepts/token.md)、训练单元预付费/后付费；**API 创建的任务仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - RL 训练**强制使用训练单元（MTU）**，不支持 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **模型产物与部署**：调优产物为独立模型 ID（如 `qwen3-8b-ft-xxx`），需单独部署；CosyVoice 调优产物固定 `voice="default"`，不可切换音色 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)


