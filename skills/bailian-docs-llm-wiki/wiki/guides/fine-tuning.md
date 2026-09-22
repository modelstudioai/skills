# fine tuning

模型调优是提升大模型在特定业务场景下表现的核心技术手段，适用于 Prompt 工程等轻量级优化无法满足效果要求的阶段。它通过 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）和 RL（强化学习）等多种方式，使模型深度适配领域知识、任务指令与人类偏好。调优后的模型可显著降低幻觉、提升 Zero/Few-Shot 效果并减少输出延迟。

## 支持的模型/功能

百炼支持文本生成、视觉理解（千问VL）、图像生成、视频生成及语音合成五大类模型的调优，但各类型支持的训练方式差异显著：

- **文本生成模型**（如 `qwen3-8b`, `qwen2.5-7b-instruct`）：全面支持 CPT、SFT（全参/高效）、DPO 和 RL 四种方式，且多数模型同时支持深度思考、工具调用等高级能力 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型**（如 `qwen3-vl-8b-instruct`）：仅支持 SFT 全参与高效训练，不支持 CPT 或 DPO [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型**（如 `wan2.7-image-pro`, `wan2.7-i2v`）：仅支持 SFT-LoRA 高效微调，且必须使用华北2（北京）地域 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**（`cosyvoice-v3-flash`）：仅支持 SFT 高效微调，且必须通过 API 发起，控制台暂不支持 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **在线策略蒸馏（OPD）**：作为独立调优范式，支持 Model OPD（纯文本）与 Agentic OPD（含工具调用），需指定教师模型与学生模型 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档 1 和文档 4 均指出“阿里云百炼推荐您以先 CPT（可选），后 SFT，再 DPO 的顺序使用模型调优”，但文档 10 的 RL 概览图明确将 RL 置于 DPO 之后，形成 `CPT→SFT→DPO→RL` 的完整链路；而文档 4 的流程图未包含 RL。此处以文档 10 的权威性为准，RL 是可选的最终对齐步骤。

## 关键参数

关键超参数因训练方式和模型类型而异，开发者应优先参考控制台默认值，并根据数据规模调整：

- **通用参数**：`n_epochs`（循环次数）默认为 3，数据量 < 10,000 条时建议 3~5 次，> 10,000 条时建议 1~2 次；`learning_rate` 需按训练方式区分——高效训练推荐 `1e-4` 量级，全参训练或 CPT 推荐 `1e-5` 量级 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **LoRA 特有参数**：`lora_rank`（默认 8）、`lora_alpha`（默认 16）、`lora_dropout`（默认 0.1）仅在高效训练中生效。
- **图像/视频生成专用参数**：万相系列模型使用 `max_steps`（训练总步数）而非 `n_epochs` 控制训练长度，推荐不少于 500 步 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **RL/OPD 专用参数**：`algorithm`（如 `"gspo"`）、`kl_loss_coef`、`n_rollouts` 等需在 SDK 中显式配置，且必须搭配 `mtu_capacity`（模型训练单元数量）资源参数 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。

## 使用方式

调优可通过控制台（GUI）或 API（代码）两种方式发起，选择依据是工程化程度与自动化需求：

- **控制台方式**：适合快速验证、小规模调优。流程为：进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)页面 → 创建训练任务 → 选择训练方法（CPT/SFT/DPO）与模型 → 上传或选择已准备好的数据集 → 配置超参数（可沿用默认值）→ 启动训练 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 方式**：适合 CI/CD 集成与批量任务。核心步骤为：1) 用 `POST /api/v1/files` 上传数据文件获取 `file_id`；2) 用 `POST /api/v1/fine-tunes` 提交训练任务，其中 `training_datasets` 字段需传入 `file_id` 或 OSS 挂载路径 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **RL/OPD 特殊方式**：必须使用 DashScope SDK 的 `AgenticRL().run()` 方法，通过 Python 代码提交，需预先完成函数计算（FC）授权与 OpenTelemetry 配置 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)。

## 限制和注意事项

- **地域与权限限制**：绝大多数调优功能（除部分文本 SFT 外）仅在华北2（北京）地域可用；所有操作均需子账号被授予模型调用、训练和部署的 RAM 权限 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据格式强约束**：SFT 必须使用 JSONL 格式，每行一个 `{"messages": [...]}` 对象；DPO 要求 `chosen`/`rejected` 字段；CPT 仅需纯文本 `{text}`；评测集则强制为 XLSX 格式 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费模式差异**：控制台支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种计费方式；而 API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **模型产物不可变**：调优产物是一个独立部署的新模型，例如 CosyVoice 调优后模型的 `voice` 参数被锁死为 `default`，无法切换音色 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **训练失败处理**：RL/OPD 任务中，若 `Rollout` 或 `Reward` 函数返回 `TaskStatus.FAILED`，框架会重试或丢弃该样本，开发者需在 `error` 字段中提供明确原因以便排查 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)。

## 来源文档

- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
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
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)


