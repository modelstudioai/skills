# fine tuning

百炼平台的 fine tuning 是面向开发者的核心模型优化能力，支持通过监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）、强化学习（RL）及在线策略蒸馏（OPD）等多种方式，对文本、图像、视频、语音等多模态模型进行定制化训练。该能力可显著提升模型在特定行业、业务场景或安全合规维度的表现，同时支持高效训练（LoRA）与全参训练两种模式，兼顾效果与成本。

## 支持的模型与功能

百炼支持广泛的模型类型和调优方法：

- **文本生成模型**：覆盖 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`, `qwen3.5-plus-2026-02-15`）、Qwen2.5 系列（如 `qwen2.5-7b-instruct`）及千问角色模型（如 `qwen-plus-character-2025-11-06`），支持 SFT、CPT、DPO、RL 和 OPD 全流程；其中 CPT 与 DPO 当前仅限华北2（北京）地域 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问VL）模型**：如 `qwen3-vl-8b-instruct`，支持 SFT 训练，暂不支持 CPT/DPO [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型**：万相（`wan2.7-image-pro`, `wan2.7-i2v`）与千问图像模型（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，且必须使用华北2（北京）地域 API Key [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 SFT 高效微调，且仅限北京地域，不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）与在线策略蒸馏（OPD）**：需联系商务经理开通权限，且均强制要求使用模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。

> **注意**：文档 2 明确指出“本文档仅适用于华北2（北京）地域”，而文档 6、8、10、13、16 均重复强调图像/视频/语音/RL/OPD 功能“仅在华北2（北京）地域可用”。但文档 3 中“地域可用性”说明“SFT、本地上传、日志回流、API 上传、多模态数据格式全地域支持”，存在矛盾。实际开发中应以具体功能页面（如控制台地域下拉选项）和最新 API 文档为准，北京地域为最全支持区域。

## 关键参数

不同调优方式对应不同核心参数，需按场景合理配置：

- **通用超参**（SFT/CPT/DPO 控制台/API）：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 继续预训练亦用 `1e-5` 量级 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `n_epochs`：数据量 < 10,000 条时建议 3~5 轮，> 10,000 条时建议 1~2 轮；视频生成模型（如 `wan2.7-i2v`）则使用 `n_epochs: 50` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
  - `batch_size`：默认值通常适用，常见取值为 16 或 32；语音合成 CosyVoice 模型固定为 `batch_size: 1` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
  - `max_length`：建议设为模型支持的最大值（如 8192），避免截断 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **LoRA 专用参数**（高效训练）：
  - `lora_rank`（默认 8）、`lora_alpha`（默认 16）、`lora_dropout`（默认 0.1）：视频生成模型常设为 `lora_rank: 32`, `lora_alpha: 32` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **RL/OPD 特有参数**：
  - RL：`algorithm`（如 `"gspo"`）、`kl_loss_coef`（如 `0.002`）、`n_rollouts`（如 `8`）等 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。
  - OPD：必须指定 `teacher_model`（如 `"qwen3.5-397b-a17b"`），并配置 `algorithm: "gspo"` 等 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 使用方式

调优任务可通过控制台或 API 两种方式发起，数据准备是共性前提：

- **数据准备**：SFT/DPO/CPT 均采用 JSONL 格式。SFT 要求 `messages` 数组（含 `system`/`user`/`assistant` 角色）；DPO 要求 `chosen`/`rejected` 字段；CPT 为纯文本 `{text}`；评测集为 XLSX 格式 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。图像/视频模型需 ZIP 打包（含 `data.jsonl` + 媒体文件）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **控制台操作**：进入 [模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”，依次选择训练方法（SFT/CPT/DPO）、模型、数据集，并配置超参。阿里云推荐调优顺序为 `CPT（可选）→ SFT → DPO（可选）→ RL/OPD（可选）` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **API 操作**：需先调用 `/api/v1/files` 上传数据获取 `file_id`，再调用 `/api/v1/fine-tunes` 创建任务。注意：通过 API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。RL/OPD 则需使用 `dashscope.finetune.agentic_rl.AgenticRL().run()` SDK 方法，自动完成函数注册、数据上传与任务提交 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 限制和注意事项

- **地域限制**：CPT、DPO、RL、OPD、图像/视频/语音模型调优均**仅支持华北2（北京）地域**；SFT 文本生成基础功能虽标称“全地域支持”，但关键配套（如控制台训练方法列表、模型服务端点）实际依赖北京地域资源。
- **计费差异**：
  - SFT/CPT/DPO 控制台支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种方式；API 仅支持按 Token 计费 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - RL/OPD **强制使用训练单元（MTU）计费**，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
  - CosyVoice 语音调优训练费用为 **0.2 元 / 千 Tokens**，与文本模型单价不同 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **模型与训练方式匹配**：并非所有模型都支持全部训练方式。例如 `qwen3.7-plus-2026-05-26` 仅支持 CPT 全参训练，不支持 SFT 或 DPO；`qwen3.6-flash-2026-04-16` 仅支持 CPT 全参训练 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **数据与版本管理**：数据集类型（训练集/评测集）创建后不可变更；切换训练方式会清空已上传文件；各训练方式新增版本均需重新导入全部数据 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **训练产物**：CosyVoice 调优产物为独立部署的新模型，`voice` 参数固定为 `default`，无法切换音色；OPD 训练完成后，最后一个 Checkpoint 会自动发布至“我的模型” [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)


