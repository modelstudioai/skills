# fine tuning

fine tuning 是百炼平台提供的核心模型优化能力，支持通过领域数据对基础模型进行定制化训练，以提升其在特定业务场景下的效果、安全性与推理效率。该能力覆盖文本生成、视觉理解、语音合成、图像/视频生成及决策模型等多种模态，并提供 SFT、DPO、CPT、RL、OPD 等多种训练范式，兼顾效果、成本与工程可控性。

## 支持的模型与功能

百炼 fine tuning 支持多类模型与训练方式，地域与功能存在明确约束：

- **文本生成模型**：Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问 Plus 等均支持 SFT、DPO、CPT 训练；其中 CPT、DPO 及 OSS 导入仅限华北2（北京）地域 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **视觉理解模型（千问VL）**：`qwen3-vl-8b-instruct` 等支持 SFT 全参/高效训练，暂不支持 DPO/CPT [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **图像/视频生成模型**：万相（`wan2.7-image-pro`）、千问图像（`qwen-image-2.0`）及万相图生视频（`wan2.7-i2v`）等仅支持 SFT-LoRA 高效微调，且必须使用北京地域 API Key [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 SFT 高效微调，且**控制台暂不支持**，必须通过 API 发起 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **决策模型**：`decision-model-preview-2026-09-24` 专属支持 SFT 微调，仅限高效训练（LoRA），全参训练不可选 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。  
- **强化学习（RL）与 OPD 蒸馏**：均需联系商务经理开通权限，并强制使用模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。

> **注意**：文档中关于“全参训练效果优于高效训练”的推荐（见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)）与决策模型、图像/视频/语音模型的实际限制矛盾——这些模型**仅支持高效训练（LoRA）**，全参训练选项不可用或无效，开发者应以控制台实际可选配置为准。

## 关键参数

不同训练方式与模型类型的关键参数差异显著，需严格匹配：

- **通用超参**（SFT/DPO/CPT 控制台/API）：`learning_rate`（默认 `3e-4`）、`n_epochs`（范围 `[1, 200]`）、`batch_size`（默认值因模型而异）、`max_length`（默认 `8192`，范围 `[500, 131072]`）。DPO 还需指定 `beta`（偏好强度，默认 `0.1`）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **LoRA 专用参数**（高效训练）：`lora_rank`（默认 `8`）、`lora_alpha`（默认 `16`）、`lora_dropout`（默认 `0.1`），影响低秩适配器容量与正则化强度。  
- **图像/视频生成特有参数**：万相模型使用 `max_steps`（训练总步数，推荐 ≥500）而非 `n_epochs`；千问图像模型则使用 `n_epochs` [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **RL/OPD 特有参数**：`n_rollouts`（每轮采样轨迹数）、`kl_loss_coef`（KL 散度系数）、`algorithm`（如 `"gspo"`）、`teacher_model`（OPD 必填）等，需通过 SDK YAML 或 `run()` 接口配置 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。  

## 使用方式

fine tuning 可通过控制台或 API 两种方式完成，流程高度结构化：

1. **数据准备与上传**：  
   - 文本 SFT/DPO/CPT 数据需为 JSONL 格式，遵循 ChatML `messages` 结构（含 `system`/`user`/`assistant` 角色），单文件 ≤200 MB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
   - 图像/视频数据需打包为 ZIP（含 `data.jsonl` + 原始媒体文件），语音数据需为同一发音人多段高质量录音 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
   - 上传接口统一为 `POST /api/v1/files`，`purpose="fine-tune"`，返回 `file_id` 用于后续任务创建 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  

2. **任务创建**：  
   - **控制台**：进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)页面 → “创建训练任务” → 选择训练方式（SFT/DPO/CPT/RL/OPD）→ 选择模型 → 配置超参 → 绑定训练集/评测集 → 提交 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
   - **API**：调用 `POST /api/v1/fine-tunes`，请求体中指定 `model`、`training_file_ids`、`training_type`（如 `"efficient_sft"`）、`hyper_parameters` 等字段 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
   - **RL/OPD**：必须使用 DashScope SDK 的 `AgenticRL().run()` 方法，传入 `teacher_model`（OPD）或 `functions`（Rollout/Reward 组件） [OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。  

3. **监控与部署**：  
   - 训练中可通过控制台“日志”、“指标”页签查看 loss 曲线、评估分数及资源消耗。  
   - 训练完成后，产出模型自动发布至“我的模型”，支持一键部署为在线 API 服务。

## 限制和注意事项

- **地域与权限限制**：CPT、DPO、OSS 导入、云存储挂载、RL、OPD 及决策模型微调**仅支持华北2（北京）地域**；所有操作需子账号具备对应 RAM 权限 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **数据与版本管理**：数据集类型（训练集/评测集）创建后不可变更；切换训练方式会清空已上传文件；各训练方式新增版本需重新导入全部数据 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **计费差异**：  
  - 控制台支持按 [Token](../concepts/token.md)、训练单元预付费/后付费；API 创建任务**仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
  - RL/OPD **强制使用训练单元（MTU）计费**，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。  
- **安全合规要求**：SFT 数据中 `system` 角色需明确定义安全边界（如“严格遵守中国法律法规”），避免模型习得有害倾向 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。  
- **模型能力边界**：调优无法扩展基础模型的固有能力（如 CosyVoice 无法通过调优支持新语种；图像模型无法新增风格类型），仅能优化其在已有能力范围内的表现 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [OPD 蒸馏训练](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [OPD 蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [OPD 蒸馏训练可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)


