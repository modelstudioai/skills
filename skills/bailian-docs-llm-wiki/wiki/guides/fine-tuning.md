# fine tuning

百炼平台的 fine tuning 功能支持多种模型类型和训练方式，适用于文本生成、视觉理解、图像/视频生成、语音合成及决策模型等场景。其核心目标是提升模型在特定业务或行业中的表现，对齐人类偏好，并降低输出延迟。

## 支持的模型与功能

百炼支持以下模型调优能力：

- **文本生成模型**：支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）和 RL（强化学习）四种训练方式，覆盖 Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列及千问 Plus 等数十个模型 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。其中，SFT 用于教会模型“学做事”，CPT 用于“补知识”，DPO 用于“做得更好”，RL 则通过奖励信号驱动自主策略优化。
  
- **视觉理解（千问 VL）**：支持 SFT 训练，适用于图片/视频理解任务，但暂不支持 DPO 和 CPT [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **图像/视频生成模型**：万相（`wan2.7-image-pro` 等）与千问图像模型（`qwen-image-2.0`）支持 SFT-LoRA 高效微调；图生视频模型（`wan2.7-i2v` 等）同样仅支持 `efficient_sft` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 `efficient_sft`，且必须为同一发音人多条录音，不支持 CPT/DPO [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **决策模型**：`decision-model-preview-2026-09-24` 支持高效微调，专用于分类、评分、是非判断等封闭集合决策任务 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

- **在线策略蒸馏（OPD）**：支持 Model OPD（纯文本蒸馏）与 Agentic OPD（含工具调用），需指定教师模型（如 `qwen3.5-397b-a17b`）对学生模型（如 `qwen3.5-9b`）进行逐 token 概率分布指导 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档中关于训练方式支持存在地域限制矛盾。例如，[调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md) 明确指出 DPO 和 CPT 仅支持北京地域，而部分图像/视频微调文档未声明地域限制，但实际均要求华北2（北京）地域。开发者应以控制台可用性为准，避免跨地域调用失败。

## 关键参数

不同训练方式和模型类型对应的关键超参如下：

- **通用参数**（SFT/CPT/DPO/RL/OPD）：
  - `n_epochs`：训练轮数，默认 `3`（SFT）、`1`（OPD/RL）；图像生成模型使用 `max_steps` 替代。
  - `learning_rate`：SFT 高效训练推荐 `1e-4` 量级，全参训练为 `1e-5`；RL/OPD 通常为 `1e-6`～`2e-6`。
  - `batch_size`：文本模型常用 `16` 或 `32`；语音/视频模型常设为 `1`。
  - `max_length`：默认 `8192`，范围 `[500, 131072]`。

- **LoRA 特有参数**（高效训练）：
  - `lora_rank`（默认 `8`）、`lora_alpha`（默认 `16`）、`lora_dropout`（默认 `0.1`）。

- **RL/OPD 特有参数**：
  - `n_rollouts`（每步采样轨迹数）、`kl_loss_coef`（KL 散度系数）、`algorithm`（如 `"gspo"`）等，详见 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。

- **语音模型特有参数**：
  - `lm_max_epoch` / `fm_max_epoch`：影响 Token 消耗计算，无对应文本模型参数。

## 使用方式

fine tuning 可通过两种主要方式启动：

- **控制台操作**：访问 [模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”，依次选择训练方法（SFT/CPT/DPO/RL）、模型、数据集、训练模式（高效/全参）及超参。控制台支持按 Token、训练单元预付费或后付费三种计费方式 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **API 调用**：通过 DashScope API 提交训练任务。需先上传数据（`POST /api/v1/files`），再创建任务（`POST /api/v1/fine-tunes`），传入 `model`、`training_datasets`、`hyper_parameters` 和 `training_type`。**注意**：API 创建的任务仅支持按 Token 计费，不支持训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

- **特殊流程**：
  - RL/OPD 需额外开发函数组件（Rollout/Reward），并通过 SDK 打包部署至函数计算（FC）；首次使用需完成 OpenTelemetry、FC、SLS 授权 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)。
  - CosyVoice 和决策模型仅支持 API 方式，控制台不可见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 限制和注意事项

- **地域限制**：绝大多数 fine tuning 功能（包括文本 SFT/DPO/CPT、图像/视频生成、语音合成、决策模型、RL、OPD）**仅支持华北2（北京）地域**。新加坡等地域仅部分模型（如 Qwen2.5-VL）支持视觉理解 SFT，但不支持其他训练方式。

- **数据格式与大小**：
  - SFT 文本数据为 JSONL 格式，单文件 ≤ 200 MB；API 上传单文件 ≤ 300 MB。
  - DPO 数据需 `chosen`/`rejected` 对；CPT 为纯文本 `{text}`；RL 数据需 `rollout_extra` 字段；OPD 数据需含 `rollout_extra.solution`。
  - 视觉/图像/视频数据需打包为 ZIP，内含 `data.jsonl` 和媒体文件。

- **计费差异**：
  - 控制台支持三种计费方式（Token/预付费/后付费），API 仅支持 Token 计费。
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总时长（秒）× 0.2 元/千 Tokens`；部署另计模型单元费用 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **模型产物与部署**：
  - 微调产物为独立新模型（非基础模型下的音色 ID 或插件），调用时需使用新模型 ID。
  - CosyVoice 调优后 `voice` 参数固定为 `default`，不可切换音色；决策模型微调后仍保持决策输出格式（非文本生成）。

- **训练方式选型建议**：推荐递进式组合：`CPT（可选）→ SFT → DPO（可选）→ RL/OPD（可选）`。其中 CPT 适合注入领域知识，SFT 适配任务指令，DPO 对齐偏好，RL/OPD 用于在线策略优化或能力蒸馏 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)


