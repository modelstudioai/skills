# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务场景下效果的核心技术手段，支持文本、图像、视频、语音等多模态模型。它通过 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）、RL（强化学习）和 OPD（在线策略蒸馏）等多种训练范式，帮助开发者将通用模型适配为领域专家。调优过程可显著提升任务表现、抑制幻觉、对齐人类偏好，并支持轻量级模型替代更大模型以降低推理成本。

## 支持的模型/功能

百炼支持全栈 fine tuning 能力，覆盖多种模型类型与训练方式：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列及千问 VL 视觉语言模型。训练方式包括 CPT、SFT（全参/高效）、DPO（全参/高效）及 RL。具体支持矩阵详见[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型**：万相（`wan2.7-image-pro`）、千问图像（`qwen-image-2.0`）及图生视频模型（`wan2.7-i2v`）仅支持 SFT 高效微调（LoRA），不支持 CPT/DPO/RL [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 SFT 高效微调，且必须使用同一发音人的多条录音，不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **高级训练范式**：
  - **RL（强化学习）**：需通过 SDK 提交，支持自定义 Rollout 与 Reward 函数，仅限华北2（北京）地域且必须使用模型训练单元（MTU）计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
  - **OPD（在线策略蒸馏）**：支持纯蒸馏（零代码）与 Agentic 模式（需自定义 Rollout），依赖教师-学生模型对，当前仅邀测开放 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档 1 明确指出“本文档仅适用于华北2（北京）地域”，而文档 7、8、10、13、17 均重复强调图像、视频、语音、RL 和 OPD 功能“仅支持华北2（北京）地域”。但文档 3 中“地域可用性”说明“SFT、本地上传、日志回流、API 上传、多模态数据格式全地域支持”，存在矛盾。实际部署时请以控制台地域选项为准，北京地域功能最全。

## 关键参数

不同训练方式的关键参数差异较大，开发者需按场景选择：

- **通用超参**（SFT/CPT/DPO 控制台/API）：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参/CPT 推荐 `1e-5` 量级；
  - `n_epochs`：数据量 < 10,000 条时建议 3–5 轮，> 10,000 条时建议 1–2 轮；
  - `max_length`：建议设为模型支持的最大值（如 8192），超长数据将被截断；
  - `lora_rank`/`lora_alpha`：LoRA 高效训练专属，`lora_rank=8`、`lora_alpha=16` 为默认值。

- **图像/视频专用参数**：
  - 万相/千问图像：使用 `max_steps`（训练总步数）而非 `n_epochs`，推荐 ≥ 500 步 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)；
  - 图生视频：`task_type="i2v"` 或 `"kf2v"`，`n_epochs=50` 为常见起点 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **RL/OPD 专用参数**：
  - RL：必填 `algorithm`（如 `"gspo"`）、`n_rollouts`、`kl_loss_coef`，且 `resources` 必须指定 MTU 规格与容量；
  - OPD：核心是 `teacher_model` 字符串（如 `"qwen3.5-397b-a17b"`），`functions=None` 表示纯蒸馏 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 使用方式

调优可通过控制台或 API 两种方式发起，流程高度结构化：

- **数据准备**：严格遵循对应训练方式的格式规范。SFT 使用 JSONL 的 ChatML `messages` 结构；DPO 使用 `chosen`/`rejected` 对；CPT 使用纯文本 `{text}`；RL/OPD 使用含 `rollout_extra` 的 JSONL。所有数据均需通过 API 上传或控制台导入 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **控制台操作**：进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)页面 → 创建训练任务 → 选择模型、训练方法（SFT/CPT/DPO）、训练模式（高效/全参）→ 配置超参 → 选择数据集 → 提交。RL 和 OPD 任务需先完成 OpenTelemetry/FC/SLS 服务授权。
- **API 操作**：使用 DashScope API，分两步：1) 用 `/api/v1/files` 上传数据获取 `file_id`；2) 用 `/api/v1/fine-tunes` 提交训练任务，传入 `model`、`training_datasets`（含 `file_id`）及 `hyper_parameters`。CosyVoice 和 RL 必须使用 API，控制台暂不支持 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 限制和注意事项

- **地域限制**：除基础 SFT 外，CPT、DPO、RL、OPD、图像/视频/语音调优均**仅支持华北2（北京）地域**。跨地域调用将失败。
- **计费差异**：
  - 控制台任务支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种方式；API 任务**仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - CosyVoice 训练费用公式为 `(lm_max_epoch + fm_max_epoch) × 25 × 总时长(秒)`，与文本模型按 [Token](../concepts/token.md) 计费逻辑不同 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **模型能力边界**：
  - CosyVoice 调优产物为单音色独立模型，`voice` 参数固定为 `"default"`，不再支持声音复刻或设计 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - OPD 教师模型必须与学生模型同系列且能力更强，且仅限邀测模型对 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。
- **数据与版本管理**：数据集类型（训练集/评测集）创建后不可变更；已发布版本不可编辑；切换训练方式会清空已上传文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

## 来源文档

- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)


