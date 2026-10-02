# fine tuning

百炼平台的 fine tuning（模型调优）是一套面向开发者的核心能力，支持通过监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）、强化学习（RL）及在线策略蒸馏（OPD）等多种方式，对文本生成、视觉理解、图像/视频生成、语音合成及决策模型进行定制化训练。其目标是提升模型在特定行业、业务或安全合规场景下的表现，抑制幻觉，降低延迟，并对齐人类偏好。所有调优任务均需在华北2（北京）地域执行，部分功能（如 CPT、DPO、OSS 导入）亦受限于该地域 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持的模型与功能

百炼支持多模态、多任务模型的 fine tuning，覆盖文本、视觉、图像、视频、语音及结构化决策场景：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列（如 `qwen2.5-7b-instruct`）及千问 VL（如 `qwen3-vl-8b-instruct`）。训练方式包括 SFT（全参/高效）、CPT、DPO 和 RL [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型**：万相（`wan2.7-image-pro`, `wan2.7-i2v`）与千问图像（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，不支持 CPT/DPO [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 `efficient_sft` 方式，且必须为同一发音人多条录音，不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**：`decision-model-preview-2026-09-24` 专用于分类、评分、是非判断等封闭集合决策任务，仅支持 `efficient_sft` [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
- **强化学习（RL）与在线策略蒸馏（OPD）**：RL 支持自定义 Rollout/Reward 函数；OPD 支持纯蒸馏（零代码）及 Agentic 模式（需自定义 Rollout），教师模型须与学生模型同系列且更强 [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)、[在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)。

> **注意**：文档 2 中表格显示 `Qwen3.7-Plus-2026-05-26` 仅支持 CPT 全参训练，但文档 1 明确说明“Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”，暗示其生产可用性受限，非标准支持模型。开发者应以控制台实际可选模型为准。

## 关键参数

不同训练方式与模型类型对应的关键超参存在差异，核心参数如下：

- **通用参数**（SFT/CPT/DPO/OPD）：
  - `n_epochs`：循环次数，默认 `3`，数据量 < 10,000 条时推荐 `3~5` 次；OPD 默认 `1`。
  - `learning_rate`：学习率，SFT 高效训练推荐 `1e-4` 量级，全参训练为 `1e-5` 量级；RL/OPD 通常为 `1e-6` ~ `2e-6`。
  - `batch_size`：批次大小，SFT 推荐 `16` 或 `32`；决策模型因输入结构特殊，常设为 `1`。
  - `max_length`：最大上下文长度，默认 `8192`，范围 `[500, 131072]`。
- **LoRA 特有参数**（高效训练）：
  - `lora_rank`：秩值，默认 `8`，图像/视频模型常设 `32`。
  - `lora_alpha`：缩放因子，默认 `16`，图像/视频模型常设 `32`。
- **RL/OPD 特有参数**：
  - `n_rollouts`：每轮采样轨迹数，RL 常用 `8`，OPD 同。
  - `kl_loss_coef`：KL 散度损失系数，OPD 默认 `0.002`。
  - `algorithm`：算法类型，如 `"gspo"`（RL/OPD 均支持）。
- **图像/视频专用参数**：
  - `max_steps`：万相模型以训练步数而非 `n_epochs` 控制训练时长，推荐 `≥ 500` 步 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 使用方式

fine tuning 可通过控制台或 API 两种方式发起，流程高度统一：准备数据 → 创建任务 → 配置参数 → 提交训练。

- **数据准备**：
  - 文本 SFT/DPO/CPT 使用 `jsonl` 格式，基于 ChatML `messages` 结构；DPO 需 `chosen`/`rejected` 字段；CPT 为纯文本 `{text}`；评测集为 `xlsx` [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - 图像/视频数据需打包为 `.zip`，内含 `data.jsonl` 与对应图片/视频文件 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - 语音数据为同一发音人的多条 `.wav` 录音，总时长建议数小时 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **控制台操作**：
  - 进入 [模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”。
  - 选择模型、训练方法（SFT/CPT/DPO/RL）、训练模式（高效/全参），上传或选择已准备的数据集。
  - 在“超参配置”面板设置关键参数，系统实时显示费用预估 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 操作**：
  - 先调用 `/api/v1/files` 上传数据，获取 `file_id`。
  - 再调用 `/api/v1/fine-tunes` 提交训练任务，请求体中指定 `model`、`training_datasets`（含 `file_id`）、`hyper_parameters` 和 `training_type`（如 `"sft"`、`"efficient_sft"`、`"rl"`） [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - RL/OPD 任务需额外部署 Rollout/Reward 函数，通过 SDK 的 `AgenticRL().run()` 一键提交 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 限制和注意事项

- **地域限制**：所有 fine tuning 任务（除部分文本 SFT 外）强制要求在华北2（北京）地域执行。CPT、DPO、OSS 导入、云存储挂载、RL、OPD 及图像/视频/语音调优均仅支持北京地域 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)、[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **计费差异**：
  - 控制台支持按 [Token](../concepts/token.md)、训练单元·预付费、训练单元·后付费三种方式；API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - RL/OPD 训练**仅支持训练单元（MTU）计费**，不支持按 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
- **数据与模型约束**：
  - 数据集类型（训练集/评测集）创建后不可变更；切换训练方式会清空已上传文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CosyVoice 调优产物为单音色独立模型，`voice` 参数固定为 `"default"`，不再支持声音复刻或设计 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **功能边界**：
  - OPD 纯蒸馏模式无需编写任何函数，仅需传入 `teacher_model` 即可触发；而 Agentic OPD 必须自定义 Rollout 函数以支持工具调用或多轮交互 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。
  - RL 训练中，Rollout 函数可通过 `AgentOutput(reward_score=...)` 直接内嵌评分逻辑，无需单独编写 Reward 函数 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)。

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
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)


