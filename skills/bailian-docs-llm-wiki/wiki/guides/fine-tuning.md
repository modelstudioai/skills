# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或安全合规场景下表现的核心能力。它支持多种训练范式（SFT、CPT、DPO、RL、OPD），覆盖文本、图像、视频、语音等多模态模型，并提供控制台可视化操作与 API/SDK 编程接口。调优过程通过注入领域知识、对齐人类偏好或蒸馏教师模型能力，实现效果提升、幻觉抑制与延迟优化。

## 支持的模型/功能

百炼支持全栈式模型调优能力，涵盖文本生成、视觉理解、图像生成、视频生成和语音合成五大类模型：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列及千问 VL 多模态模型，训练方式包括 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）、RL（强化学习）和 OPD（在线策略蒸馏）。其中，CPT 和 DPO 仅支持华北2（北京）地域 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问 VL）**：支持 `qwen3-vl-8b-instruct` 等模型的 SFT 高效/全参训练，但不支持 CPT 或 DPO [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **图像生成模型**：支持万相（`wan2.7-image-pro`）和千问图像（`qwen-image-2.0`）的 SFT-LoRA 高效微调，适用于文生图、图生图任务 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成模型**：支持万相图生视频模型（如 `wan2.7-i2v`）的 SFT-LoRA 微调，支持基于首帧或首尾帧两种模式 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型**：仅支持 CosyVoice `cosyvoice-v3-flash` 的 SFT 高效微调，且必须为同一发音人多条录音；不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 2 中表格显示 `Qwen3.7-Plus-2026-05-26` 仅支持 CPT 全参训练，但文档 1 明确标注“调优后部署请联系商务经理”，暗示其生产可用性受限；而文档 4 和文档 5 均未将该模型列入推荐初学者选项，建议优先选用 `qwen3-8b` 或 `qwen3-14b` 等明确支持全训练方式的通用型号。

## 关键参数

调优任务的关键参数分为模型选择、训练方式与超参三类，需根据任务目标与资源约束协同配置：

- **训练方式选择**：
  - `efficient_sft`（LoRA 高效训练）：推荐用于快速验证、成本敏感或数据量较小的场景；收敛快、显存占用低。
  - `full_fine_tuning`（全参训练）：推荐用于追求全局最优效果的生产环境；文档 4 明确指出“全参训练效果比高效训练效果要好，性价比更高”，但需注意部分小模型（如 `qwen3-0.6b`）仅支持高效训练。
  - `rl` / `opd`：需额外配置函数组件（Rollout/Reward）或教师模型，不适用基础 SFT 流程。

- **核心超参**（以文本 SFT 为例）：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 同样使用 `1e-5` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `n_epochs`：数据量 < 10,000 条时建议 3–5 轮；> 10,000 条时建议 1–2 轮；过高的轮数易导致过拟合。
  - `batch_size`：默认值通常可用；常见取值为 16 或 32，具体范围依模型和训练方式而异。
  - `max_length`：应设为模型支持的最大上下文长度（如 `8192`），避免截断长样本。
  - `lora_rank` / `lora_alpha`：LoRA 专属参数，默认 `8` 和 `16`；增大可提升表达能力但增加显存开销。

- **多模态特有参数**：
  - 图像/视频微调使用 `max_steps`（步数）而非 `n_epochs` 控制训练时长 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - 语音调优使用 `lm_max_epoch` 和 `fm_max_epoch` 计算 [Token](../concepts/token.md) 消耗，与文本 SFT 的 `n_epochs` 语义不同 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

调优任务可通过控制台或 API/SDK 两种方式发起，流程高度一致：准备数据 → 创建任务 → 配置参数 → 提交训练。

- **数据准备**：
  - SFT 文本数据采用 JSONL 格式，每行一个 `{"messages": [...]}` 对象，支持 `system`/`user`/`assistant` 角色及 `loss_weight` 字段（Qwen3.5+ 默认支持）[调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - DPO 数据需包含 `chosen`/`rejected` 偏好对；CPT 数据为纯文本 `{text}`；RL/OPD 数据需含 `rollout_extra` 字段透传参考答案。
  - 图像/视频数据需打包为 ZIP，内含 `data.jsonl` 及对应图片/视频文件；语音数据为同一发音人的多段 WAV/MP3 录音。

- **控制台操作**：
  - 进入 [模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”。
  - 依次选择训练方法（SFT/CPT/DPO）、模型、训练方式（高效/全参）、数据集，并在“超参配置”面板调整关键参数。
  - 任务提交后可在控制台实时查看训练日志、损失曲线与验证指标。

- **API/SDK 操作**：
  - 先调用 `/api/v1/files` 上传数据文件，获取 `file_id`。
  - 再调用 `/api/v1/fine-tunes` 提交训练任务，请求体中指定 `model`、`training_datasets`（含 `file_id`）、`hyper_parameters` 和 `training_type`。
  - RL 和 OPD 任务需额外注册 Rollout/Reward 函数并配置 `resources`（MTU 训练单元）[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。

## 限制和注意事项

- **地域与权限限制**：
  - CPT、DPO、OSS 导入、云存储挂载仅支持华北2（北京）地域；图像/视频/语音调优同样强制要求北京地域 API Key [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - 子账号（RAM 用户）需被授予 `AliyunBailianFullAccess` 或精细化权限策略，否则无法创建训练任务 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

- **计费与配额**：
  - 控制台支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种计费方式；API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - 文件上传配额：单文件 ≤ 300 MB，总空间 ≤ 100 GB，总数量 ≤ 10,000 个 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - RL/OPD 训练**强制要求使用 MTU 训练单元**，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。

- **工程实践注意事项**：
  - 数据集类型（训练集/评测集）创建后不可变更；切换训练方式会清空已上传文件，务必提前规划 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - RL/OPD 任务需完成 OpenTelemetry、函数计算（FC）和日志服务（SLS）三项服务授权，否则提交失败 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
  - CosyVoice 调优产物为独立部署的单音色模型，`voice` 参数固定为 `default`，不再支持声音复刻或指令控制等基础模型能力 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

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
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)


