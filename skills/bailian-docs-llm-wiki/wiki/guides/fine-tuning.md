# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，支持通过监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）和强化学习（RL）等方式，提升模型在特定业务、行业或价值观对齐任务上的表现。它适用于当 Prompt 工程等轻量级方法无法满足效果要求时的深度优化场景，可显著降低幻觉、提升领域知识准确性和输出稳定性。

## 支持的模型与功能

百炼支持多模态、多任务的 fine tuning，覆盖文本生成、视觉理解、图像生成、视频生成和语音合成五大类模型：

- **文本生成**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等模型，提供 SFT、CPT、DPO 和 RL 四种训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问 VL）**：支持 `qwen3-vl-8b-instruct` 等模型，仅限 SFT 训练（不支持 DPO/CPT），需注意图像分辨率限制（长边/短边比值 ≤ 200:1，推荐 ≤ 8K）[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像生成**：支持万相（`wan2.7-image-pro`）和千问图像（`qwen-image-2.0`）模型，仅支持 SFT-LoRA 高效微调，文生图/图生图均适用 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：支持 `wan2.7-i2v` 等图生视频模型，同样仅限 SFT-LoRA，区分“基于首帧”与“基于首尾帧”两种任务类型 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：仅支持 `cosyvoice-v3-flash` 模型的 SFT 高效微调，面向同一发音人的高还原度音色定制，**控制台暂不支持，必须使用 API** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档中明确指出，**CosyVoice 模型调优当前仅支持 API 方式，控制台暂不支持** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)，而其他文本/视觉类模型均支持控制台与 API 双通道。此为关键功能差异，开发者需提前规划接入路径。

## 关键参数

不同训练方式与模型类型对应的关键参数存在显著差异，开发者应严格按模型能力选择：

- **通用超参（SFT 文本生成）**：`learning_rate`（默认 `3e-4`，高效训练建议 `1e-4` 量级）、`n_epochs`（数据 < 10k 条建议 3–5 轮）、`max_length`（建议设为模型支持最大值，SFT 超长数据会被丢弃）、`lora_rank`（高效训练推荐设为模型支持的最大值）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成专用参数**：万相模型使用 `max_steps`（推荐 ≥ 500）、`max_pixels`（如 `"2k"` 表示 2048×2048）；千问图像模型则使用 `n_epochs`（推荐 10）、`val_img_size`（如 `"2k"`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **RL 训练专属参数**：`algorithm`（如 `"gspo"`）、`batch_size`（如 `64`）、`kl_loss_coef`（如 `0.002`）、`n_rollouts`（每条 [prompt](prompt.md) 的采样数，如 `8`），且**必须配置 `resources` 字段指定 MTU 单元规格与数量** [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。
- **语音合成参数**：`lm_max_epoch` 与 `fm_max_epoch` 共同决定 Token 消耗，公式为 `(lm_max_epoch + fm_max_epoch) × 25 × 总音频秒数`，直接影响训练费用 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

fine tuning 的使用流程高度标准化，但入口与操作细节因模型类型而异：

- **控制台操作（文本/视觉）**：进入 [模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning) 页面 → 创建训练任务 → 选择模型、训练方式（SFT/CPT/DPO/RL）、训练集 → 配置超参 → 启动训练。训练日志与损失曲线可实时查看 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 操作（全类型）**：所有模型均支持 HTTP API 调用。通用流程为：1) 上传 `.zip` 数据集获取 `file_id`；2) 调用 `/api/v1/fine-tunes` 提交训练任务，携带 `model`、`training_file_ids` 和 `hyper_parameters`；3) 轮询任务状态直至 `SUCCEEDED` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **RL 特殊流程**：需先完成环境准备（安装 SDK、授权 FC/SLS/OTel）、开发 Rollout/Reward 函数、打包项目，再通过 `client.run()` 一键提交（自动注册函数+上传数据+启动训练）[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 限制和注意事项

- **地域限制**：绝大多数 fine tuning 功能（包括 SFT/DPO/CPT/RL、图像/视频/语音微调）**仅支持华北2（北京）地域**，跨地域调用将失败 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **数据格式强约束**：
  - 文本 SFT/DPO 必须为 JSONL 格式，SFT 每行含 `messages` 数组，DPO 需额外包含 `chosen`/`rejected` 字段 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CosyVoice 训练数据必须为 `.wav`（≥16kHz），`data.jsonl` 中 `wav_fn` 必须以 `train/` 开头 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **计费模式差异**：
  - 文本/视觉模型支持按 Token、训练单元预付费/后付费三种方式；**API 创建任务仅支持按 Token 计费** [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总秒数 × 0.2 元/千 Tokens`，部署费用另计 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL 训练**强制使用模型训练单元（MTU）计费，不支持按 Token 计费** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **模型能力边界**：fine tuning **无法扩展基础模型的原生能力**，例如 CosyVoice 调优不能新增语种支持，千问 VL 微调不能突破其固有的图像理解上限 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)


