# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或安全合规场景下表现的核心能力。它通过在预训练模型基础上注入领域知识、对齐任务指令或优化人类偏好，实现效果提升、幻觉抑制与延迟降低。调优支持文本、图像、视频、语音等多模态模型，并提供 SFT、CPT、DPO、RL、OPD 等多种训练范式，兼顾效果、成本与工程效率。

## 支持的模型与功能

百炼支持全栈式模型调优能力，覆盖主流模态与训练范式：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问 VL 多模态模型（如 `qwen3-vl-8b-instruct`）。训练方式包括 CPT（补知识）、SFT（学做事）、DPO（做得更好）和 RL（学推理），并明确推荐递进流程：`CPT（可选）→ SFT → DPO（可选）→ RL（可选）` [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型**：万相（`wan2.7-image-pro`, `wan2.7-i2v`）与千问图像模型（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，不支持 CPT/DPO/RL；训练控制参数为 `max_steps`（非 `n_epochs`），且仅限华北2（北京）地域 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：CosyVoice 仅支持 `efficient_sft` 方式调优，且仅限 `cosyvoice-v3-flash` 模型，不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）与在线策略蒸馏（OPD）**：二者均需通过 SDK 提交，依赖函数计算（FC）与 OpenTelemetry 可观测性，且**仅支持华北2（北京）地域**。RL 需自定义 Rollout 与 Reward 函数；OPD 则以教师模型逐 token 概率分布为监督信号，支持纯蒸馏（零代码）与叠加 Reward 的进阶模式 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档 2 中表格显示 `Qwen3.7-Plus-2026-05-26` 仅支持 CPT 全参训练，但文档 1 明确标注“调优后部署请联系商务经理”，暗示该模型调优能力受限或处于邀测阶段，实际可用性需以控制台选项为准。

## 关键参数

不同调优方式的关键参数存在显著差异，开发者需按场景选择：

- **通用超参（SFT/CPT/DPO 控制台/API）**：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 继续预训练亦用 `1e-5` 量级。
  - `n_epochs`：数据量 < 10,000 条时建议 3–5 轮，> 10,000 条时建议 1–2 轮。
  - `batch_size`：默认值通常适用，常见取值为 16 或 32。
  - `max_length`：应设为模型支持的最大值（如 8192），避免截断。
  - `lora_rank`/`lora_alpha`：LoRA 高效训练专属，控制低秩适配器维度与缩放强度，默认值分别为 8 和 16。

- **图像/视频生成专用参数**：
  - `max_steps`（非 `n_epochs`）：万相/千问图像/视频模型的核心训练步数，建议 ≥ 500 步以确保收敛 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - `task_type`：视频生成模型必需，如 `"i2v"`（首帧生视频）或 `"kf2v"`（首尾帧生视频）。

- **RL/OPD 专用参数**：
  - `teacher_model`：OPD 训练的唯一新增必填字段，用于指定更强的教师模型 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。
  - `algorithm`（如 `"gspo"`）、`kl_loss_coef`、`n_rollouts`：RL 训练核心算法与稳定性参数，详见 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。

## 使用方式

调优可通过控制台（可视化）或 API/SDK（自动化）两种方式发起，选择取决于工程需求：

- **控制台操作**：适用于快速验证与小规模调优。流程为「创建训练任务 → 选择模型与训练方法（SFT/CPT/DPO）→ 上传/选择数据集 → 配置超参 → 提交」。控制台支持训练单元预付费/后付费及按 [Token](../concepts/token.md) 计费，但**RL 和 OPD 不支持控制台提交，必须使用 SDK** [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API/SDK 提交**：
  - 文本/SFT/CPT/DPO：通过 `POST /api/v1/fine-tunes` 提交，支持 `file_id` 或 OSS 挂载数据源 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - 图像/视频/CosyVoice：均仅支持 API 提交，无控制台入口 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL/OPD：必须使用 `dashscope.finetune.agentic_rl.AgenticRL` SDK，通过 `run()` 方法一步完成函数注册、数据上传与任务提交，且需提前完成 FC/ARMS/SLS 服务授权 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

> **注意**：文档 4 建议“如果模型支持全参训练，请优先选择全参训练”，但文档 6 在安全合规示例中明确选用高效训练（LoRA），因其“速度快、成本低”，适用于快速验证。开发者应根据效果要求与资源约束权衡，而非机械遵循单一建议。

## 限制和注意事项

- **地域限制**：绝大多数调优能力（SFT/DPO/CPT/RL/OPD/图像/视频/语音）**仅支持华北2（北京）地域**；部分功能（如 DPO/CPT/OSS 导入）在其他地域不可用 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费差异**：
  - 控制台任务支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种方式；**API 创建的任务仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - CosyVoice 调优费用 = 训练 Token 费用（0.2 元/千 Tokens） + 部署模型单元费用；RL/OPD 仅支持训练单元（MTU）计费，**不支持按 Token 计费** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)、[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
- **数据与格式约束**：
  - SFT 数据为 JSONL 格式，每行含 `messages` 数组（system/user/assistant 角色）；DPO 数据需 `chosen`/`rejected` 对；CPT 为纯文本 `{text}` [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - 数据集类型（训练集/评测集）创建后不可变更；切换训练方式会清空已上传文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **模型与能力边界**：
  - CosyVoice 调优产物为单音色独立模型，**不支持声音复刻、声音设计或指令控制功能**，语种支持完全继承基础模型 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - OPD 教师模型必须与学生模型同系列且能力更强，且当前仅限邀测模型组合 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

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
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)


