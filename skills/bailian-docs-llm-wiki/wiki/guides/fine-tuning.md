# fine tuning

百炼平台的 fine tuning（模型调优）是一套面向生产场景的模型能力增强体系，支持文本、多模态、图像、视频及语音等多种模态的定制化训练。其核心目标是通过 SFT、CPT、DPO、RL 等方法，在不改变基础模型架构的前提下，提升模型在特定业务、行业或安全合规维度的表现力、稳定性与对齐度。调优过程强调数据驱动、参数可控、计费透明，并深度集成控制台与 API 两种交付路径。

## 支持的模型与功能

百炼支持多种模态和训练方式的组合：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3.5-9b`）、Qwen2.5 系列及千问 Plus 等，覆盖 CPT、SFT（全参/高效）、DPO 和 RL 四种训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问 VL）**：支持 `qwen3-vl-8b-instruct` 等，仅限 SFT 全参/高效训练，不支持 DPO/CPT [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成模型**：万相（`wan2.7-image-pro`）与千问图像（`qwen-image-2.0`）均支持 SFT-LoRA 微调，但超参体系不同：万相以 `max_steps` 控制训练，千问以 `n_epochs` 控制 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成模型**：支持 `wan2.7-i2v` 等图生视频模型，仅限 `efficient_sft`，需指定 `task_type="i2v"` 或 `"kf2v"` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型**：仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调，且**控制台暂不支持，必须通过 API 发起** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：支持 `qwen3.5-9b` 等 MoE 模型，但需联系商务经理开通权限；**仅支持模型训练单元（MTU）计费，不支持按 Token 计费** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 3（[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)）中称“Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”，而文档 4（[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)）未提及该限制，且控制台实际可选该模型。此处以控制台实时能力为准，文档 3 中该说明已过时。

## 关键参数

不同训练方式与模态的参数集存在显著差异，开发者需严格匹配：

| 参数类别 | 文本生成（SFT/DPO） | 图像生成（万相） | 视频生成 | 语音合成（CosyVoice） | 强化学习（RL） |
|----------|----------------------|------------------|-----------|------------------------|----------------|
| **核心步长** | `n_epochs`（轮次） | `max_steps`（步数） | `n_epochs` | `lm_max_epoch` + `fm_max_epoch` | `n_epochs`, `n_rollouts`, `batch_size` |
| **学习率** | `learning_rate`（SFT 推荐 `3e-4`，全参训练用 `1e-5`） | `learning_rate`（万相推荐 `3e-5`） | `learning_rate`（`2e-5`） | `learning_rate`（未公开推荐值） | `learning_rate`（`2e-6`），`kl_loss_coef`（`0.002`） |
| **序列/尺寸控制** | `max_length`（默认 `8192`） | `max_pixels`（如 `"2k"`）、`val_img_size` | `max_pixels`（数值，如 `102400`） | 无等效参数 | `max_length`（`8192`） |
| **LoRA 相关** | `lora_rank`（默认 `8`）、`lora_alpha`（默认 `16`） | `lora_rank`（必须为 `2^n`，如 `32`） | `lora_rank`, `lora_alpha`（均 `32`） | 不暴露 LoRA 参数 | 不适用 |
| **验证机制** | `eval_steps`（默认 `50`） | `eval_steps`（万相） / `eval_epochs`（千问） | `eval_epochs` | 无验证参数 | `eval_steps`（默认 `1`） |

所有训练方式均支持 `batch_size`、`lr_scheduler_type`（推荐 `linear` 或 `cosine`）和 `weight_decay`（默认 `0.01`）。CPT 训练**不支持 LoRA 相关参数、`warmup_ratio` 和 `weight_decay`** [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 使用方式

### 控制台操作（推荐入门与文本类任务）
1. 进入 [模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击「创建训练任务」；
2. 选择训练方法（SFT/DPO/CPT）、模型、训练类型（高效/全参）；
3. 上传或选择已准备好的训练集与评测集（格式要求见 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)）；
4. 配置超参（建议优先使用控制台默认值，再根据损失曲线迭代调整）；
5. 提交并监控训练日志（`Training Loss` 与 `Validation Loss` 曲线是判断欠拟合/过拟合的关键依据）。

### API 操作（适用于自动化、多模态及 RL 场景）
- **通用流程**：先调用 `/api/v1/files` 上传数据（`purpose="fine-tune"`），获取 `file_id`；再调用 `/api/v1/fine-tunes` 创建任务，传入 `file_id` 及 `hyper_parameters`。
- **模态特异性**：
  - 图像/视频：上传 `.zip` 包（含 `data.jsonl` + 原始媒体文件），`training_type` 固定为 `"efficient_sft"`；
  - 语音：`training_type` 必须为 `"efficient_sft"`，且 `model` 仅支持 `"cosyvoice-v3-flash"`；
  - RL：必须使用 `dashscope.finetune.reinforcement` SDK，通过 `AgenticRL().run()` 提交，**不支持直接 HTTP POST `/fine-tunes`** [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。

> **注意**：文档 5（[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)）中示例 `training_type` 列表包含 `"rl"`，但实际 RL 任务必须通过专用 SDK 提交，该字段为误导性残留。正确方式请以 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md) 为准。

## 限制和注意事项

- **地域限制**：绝大多数调优功能（除 CosyVoice 外）**仅支持华北2（北京）地域**；DPO/CPT/OSS 导入/云存储挂载也仅限北京 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **数据格式强约束**：
  - SFT/DPO 必须为 `jsonl`，每行一个 `{"messages": [...]}` 对象，`messages` 内必须含 `system`/`user`/`assistant` 角色；
  - 评测集仅支持 `xlsx`（非 `jsonl`），且仅支持本地上传与日志回流 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)；
  - 图像/视频训练集必须为 `.zip`，内含 `data.jsonl` 和媒体文件，目录结构固定。
- **不可逆操作**：
  - 数据集类型（训练集/评测集）创建后不可变更；
  - 已发布版本不可编辑；仅草稿版本可删除或在线编辑；
  - 切换训练方式（如 SFT → DPO）会清空已上传文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费差异**：
  - 控制台支持按 Token、训练单元预付费/后付费；API 创建的任务**仅支持按 Token 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)；
  - RL 训练**强制使用模型训练单元（MTU）**，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)；
  - CosyVoice 调优费用 = 训练 Token 费（0.2 元/千 Tokens）+ 部署时长费，公式含 `lm_max_epoch` 与 `fm_max_epoch` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)


