# fine tuning

百炼平台的 fine tuning 是一种模型定制化能力，允许开发者基于预训练大模型，使用自有业务数据进行针对性训练，从而提升模型在特定领域、任务或价值观对齐方面的表现。它支持多种训练范式（SFT、CPT、DPO、RL、OPD 等），覆盖文本、图像、视频、语音及决策模型等多种模态，并提供控制台可视化操作与 API 编程两种使用方式。

## 支持的模型/功能

百炼支持多类模型的 fine tuning，按模态和训练方式划分如下：

- **文本生成模型**：支持 SFT、CPT、DPO、RL 和 OPD 四种主流训练范式。Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问 Plus 等均支持全参训练与 LoRA 高效训练；部分模型（如 `qwen3.7-plus-2026-05-26`）仅支持 CPT 全参训练 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问 VL）**：支持 SFT 训练，适用于图片/视频输入场景，但不支持 DPO 或 CPT [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型（万相、千问图像）**：仅支持 SFT-LoRA 高效微调，不支持全参训练或 DPO/CPT；训练以 `max_steps` 为控制单位，而非 `n_epochs` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型（CosyVoice）**：仅支持 `efficient_sft` 方式，且必须使用 `cosyvoice-v3-flash` 模型，不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**：支持 `efficient_sft` 微调，专用于分类、评分、是非判断等结构化输出任务，当前模型为 `decision-model-preview-2026-09-24` [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
- **强化学习（RL）与在线策略蒸馏（OPD）**：均为高级训练方式，需通过 SDK 提交，依赖函数开发与 MTU 计费资源；RL 需自定义 Rollout/Reward 函数，OPD 则以教师模型逐 token 指导学生模型 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档中关于“高效训练推荐优先级”的表述存在矛盾。文档 3 明确指出“**如果模型支持全参训练，请优先选择全参训练，因为效果更好，性价比更高**”；而文档 5 却称“高效训练（LoRA）速度快、成本低……适用于快速验证”，并默认推荐高效训练。实际选型应以效果目标为先：生产环境强效果需求首选全参训练；快速迭代或资源受限场景可选 LoRA。

## 关键参数

不同训练方式的核心参数差异较大，以下为通用高频参数及其典型取值：

| 参数 | 类型 | 默认值 | 说明 | 推荐设置 |
|------|------|--------|------|-----------|
| `training_type` | string | — | 训练方式标识 | `sft` / `cpt` / `dpo` / `efficient_sft` / `rl` / `opd`（需传 `teacher_model`） |
| `n_epochs` | int | `3` | 训练轮数（文本/SFT/OPD） | 数据量 < 10k 条：3–5 轮；> 10k 条：1–2 轮 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md) |
| `max_steps` | int | — | 训练总步数（图像/视频） | ≥500 步确保收敛 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) |
| `learning_rate` | float | `3e-4` | 学习率 | 高效训练：`1e-4` 量级；全参/CPT：`1e-5` 量级 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md) |
| `batch_size` | int | — | 批次大小 | 文本常用 `16`/`32`；语音/决策模型常为 `1` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md) |
| `lora_rank` / `lora_alpha` | int / float | `8` / `16` | LoRA 秩与缩放因子 | 视模型规模调整，常见组合：`rank=8, alpha=16` 或 `rank=32, alpha=32` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)、[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md) |

其他重要参数包括 `lr_scheduler_type`（推荐 `linear` 或 `cosine`）、`eval_steps`（验证频率）、`max_length`（最大上下文长度，默认 `8192`）等，具体支持范围以控制台或 API 文档为准。

## 使用方式

fine tuning 可通过**控制台**或**API/SDK**两种方式完成，流程高度一致：准备数据 → 创建任务 → 配置参数 → 启动训练 → 部署调用。

- **控制台操作**：适用于无代码需求的用户。进入 [模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”，依次选择训练方法（SFT/CPT/DPO）、模型、训练方式（高效/全参），上传或引用已上传的数据集，配置超参后提交。训练状态、损失曲线、评估指标均可实时查看 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API/SDK 操作**：
  - **HTTP API**：适用于文本、语音、决策模型。需先调用 `/api/v1/files` 上传数据（`purpose="fine-tune"`），再调用 `/api/v1/fine-tunes` 创建任务，请求体中指定 `model`、`training_datasets`（含 `file_id` 或 `oss_mount`）、`hyper_parameters` 和 `training_type` [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - **SDK（RL/OPD）**：必须使用 DashScope SDK。需完成环境准备（API Key、服务授权、OpenTelemetry 依赖）、编写 Rollout/Reward 函数（RL/Agentic OPD）或仅准备数据（纯蒸馏 OPD），最后通过 `AgenticRL().run(...)` 一键提交 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

所有方式均要求数据符合对应训练方式的格式规范（如 SFT 为 ChatML messages JSONL，DPO 为 chosen/rejected 对，CPT 为纯文本 JSONL）[调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

## 限制和注意事项

- **地域限制**：绝大多数 fine tuning 功能（SFT/CPT/DPO/RL/OPD/语音/决策模型）**仅支持华北2（北京）地域**；图像/视频微调亦明确限定该地域 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **计费模式差异**：
  - 控制台支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种方式；
  - **API 创建的任务仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)；
  - RL 和 OPD **强制使用训练单元（MTU）计费**，不支持按 [Token](../concepts/token.md) [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。
- **数据与权限要求**：需确保 RAM 子账号已授予 `AliyunBailianFullAccess` 或最小必要权限；数据文件单个上限 200MB（文本）或 300MB（API 通用）；OSS 挂载仅支持北京/新加坡地域 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)、[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **模型与功能兼容性**：并非所有模型支持全部训练方式。例如，`qwen3.7-plus-2026-05-26` 仅支持 CPT 全参训练，不支持 SFT/DPO；千问 VL 不支持 DPO/CPT；CosyVoice 仅支持 `efficient_sft` [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)


