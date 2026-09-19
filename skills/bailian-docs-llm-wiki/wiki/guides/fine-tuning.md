# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或安全合规场景下表现的核心能力，支持监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）和强化学习（RL）四种训练范式。用户可通过控制台可视化操作或 API 编程方式，基于高质量标注数据对预置模型进行定制化训练，显著提升任务适配性、降低幻觉、对齐人类偏好，并支持文本、[多模态](../concepts/multimodal.md)、语音、视频等多类型模型。

## 支持的模型/功能

百炼支持全栈模型调优能力，覆盖文本生成、视觉理解（千问VL）、语音合成（CosyVoice）、图像生成（万相/千问图像）、视频生成（万相）五大类模型：

- **文本生成模型**：Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`, `qwen3-vl-8b-instruct`）、Qwen2.5 系列及千问-Plus-Character 等，支持 SFT（全参/高效）、CPT、DPO 和 RL 四种训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型**：Qwen3-VL 系列（如 `qwen3-vl-8b-instruct`）仅支持 SFT（全参/高效），不支持 DPO/CPT；训练时需注意图像分辨率限制（长边/短边比值 ≤ 200:1，推荐 ≤ 8K）[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **语音合成模型**：仅 `cosyvoice-v3-flash` 支持 SFT 高效微调（`efficient_sft`），且**控制台暂不支持，必须通过 API 发起**；调优产物为单音色独立模型，`voice` 参数固定为 `default` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **图像/视频生成模型**：万相（`wan2.7-i2v`, `wan2.7-image-pro`）与千问图像（`qwen-image-2.0`）均仅支持 SFT-LoRA 高效微调；但超参体系不同——万相以 `max_steps` 控制训练，千问图像以 `n_epochs` 控制 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

> **注意**：文档中关于“全参训练效果优于高效训练”的表述存在矛盾。[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md) 明确建议“如果模型支持全参训练，请优先选择全参训练，因为全参训练效果比高效训练效果要好”，但[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md) 的“训练模式对比”表格中又指出高效训练（LoRA）是“推荐”方式，且适用于“对训练时间和成本敏感的场景”。实际应依据任务目标权衡：生产环境追求极致效果且预算充足时选全参；快速验证、小数据集或成本敏感场景首选 LoRA。

## 关键参数

不同调优方式与模型类型对应的关键参数差异显著，开发者需严格按文档要求配置：

- **通用核心参数（SFT/CPT/DPO 文本生成）**：`n_epochs`（循环次数，必填）、`batch_size`（批次大小，必填）、`max_length`（序列长度，必填）、`learning_rate`（学习率）。其中 `n_epochs` 推荐值与数据量强相关：数据量 < 10,000 条时设为 3~5；> 10,000 条时设为 1~2 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **LoRA 专用参数（高效训练）**：`lora_rank`（秩值，推荐设为模型支持的最大值）、`lora_alpha`（缩放因子）、`lora_dropout`（丢弃率）。`lora_rank` 越大拟合能力越强，但易过拟合；`lora_alpha` 过大则模型过度依赖调优任务，过小则保留过多原始知识 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成特有参数**：万相图像/视频使用 `max_steps`（总步数，必填）、`eval_steps`（验证间隔）、`max_pixels`（训练图最大分辨率）；千问图像则用 `n_epochs` 和 `eval_epochs`；视频生成模型（如 `wan2.7-i2v`）还需指定 `task_type`（`i2v` 或 `kf2v`）[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **强化学习（RL）独有参数**：`algorithm`（算法，如 `gspo`）、`kl_loss_coef`（KL 散度惩罚系数）、`n_rollouts`（每条 [prompt](prompt.md) 的采样数）、`ppo_mini_batch_size`（PPO 小批量大小）。RL 训练**强制要求使用模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 使用方式

调优流程统一为“准备数据 → 上传文件 → 创建任务 → 监控训练 → 部署调用”，但入口与细节因方式而异：

- **控制台操作**：适用于文本生成模型的 SFT/CPT/DPO。进入[模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”，依次配置任务名称、模型、训练方法（高效/全参）、训练方式（SFT/CPT/DPO）、数据集及超参。所有参数均有默认值，可直接启动 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 操作**：适用于所有模型类型及 RL。需先调用 `/api/v1/files` 上传数据（`purpose="fine-tune"`），获取 `file_id`；再调用 `/api/v1/fine-tunes` 创建任务，请求体中指定 `model`、`training_datasets`（含 `file_id`）、`training_type`（如 `"sft"`、`"efficient_sft"`、`"dpo_full"`）及 `hyper_parameters`。**通过 API 创建的任务仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **RL 特殊流程**：需离线开发 Rollout（轨迹生成）和 Reward（评分）函数，打包为 SDK 项目；通过 `AgenticRL().run()` 一步完成函数注册、数据上传与任务提交，全程依赖 MTU 资源 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。

## 限制和注意事项

- **地域限制**：绝大多数调优功能（SFT/DPO/CPT/RL）仅在**华北2（北京）地域**可用；部分功能（如 CosyVoice、万相视频）明确要求使用该地域的 API Key [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **数据格式与规模**：
  - SFT/DPO 文本数据为 JSONL 格式，单文件上限 200 MB；SFT 数据需符合 ChatML `messages` 结构（含 `system`/`user`/`assistant` 角色）；DPO 数据需包含 `chosen` 与 `rejected` 对比输出 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CosyVoice 语音调优需准备同一发音人的 `.wav` 音频（≥16 kHz，2~30 秒/条）及 `data.jsonl`（含 `wav_fn` 和 `text` 字段），打包为 ZIP 上传 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **计费与资源**：
  - 文本生成模型支持按 [Token](../concepts/token.md) 计费（API 专属）、训练单元预付费/后付费（控制台专属）；CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总时长(秒) × 0.2 元/千 Tokens`；RL 训练**强制绑定 MTU 单元**，无 Token 计费选项 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 所有调优任务均需 RAM 子账号具备相应权限（`AliyunBailianFullAccess` 或最小化策略）[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **模型行为约束**：调优无法突破基础模型能力边界。例如，CosyVoice 调优不能新增语种支持；万相图像调优不能改变其文生图/图生图的固有模式；千问VL 调优后仍受原图分辨率限制 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)


