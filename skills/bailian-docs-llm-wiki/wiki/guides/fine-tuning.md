# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或安全合规场景下表现的核心能力，支持文本生成、视觉理解、语音合成、图像生成和视频生成等多种模态。调优方式涵盖监督微调（SFT）、继续预训练（CPT）、直接偏好优化（DPO）和强化学习（RL），用户可根据目标（补知识、学做事、做得更好、学推理）选择递进式组合策略。所有调优任务均需在华北2（北京）地域执行。

## 支持的模型与功能

- **文本生成模型**：全面支持 Qwen3 系列（如 `qwen3-8b`, `qwen3.5-27b`）、Qwen2.5 系列及千问VL多模态模型（如 `qwen3-vl-8b-instruct`）。支持 SFT、DPO、CPT 三种训练方式，其中 DPO 和 CPT 当前仅限北京地域使用 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **图像/视频生成模型**：万相（`wan2.7-image-pro`, `wan2.7-i2v`）和千问图像模型（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，不支持 CPT/DPO；图像生成按 `max_steps` 控制训练过程，而千问图像模型按 `n_epochs` 控制 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 `efficient_sft` 方式，且**控制台暂不支持**，必须通过 API 发起 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：支持 Qwen3.5-9B 等指定模型，需联系商务经理开通，并**强制使用模型训练单元（MTU）计费，不支持按 Token 计费** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 3 明确指出“本文档仅适用于华北2（北京）地域”，但文档 7 和文档 14 在“适用范围”中重复强调“仅在华北2（北京）地域可用”，而文档 2 的“地域可用性”表格却注明“SFT、本地上传、日志回流、API 上传、多模态数据格式全地域支持”。该矛盾表明 SFT 基础能力（如数据上传、文本 SFT 训练）可能已扩展至其他地域，但高级能力（DPO/CPT/RL）及多模态模型调优仍严格限定于北京。实际操作请以控制台可选地域为准。

## 关键参数

| 参数 | 适用训练类型 | 说明 | 推荐值/约束 |
|------|--------------|------|-------------|
| `training_type` | 全部 | 必填，取值为 `sft`/`dpo_full`/`efficient_sft`/`cpt`/`rl` | 文本 SFT 推荐 `efficient_sft`（LoRA）；图像/视频/语音固定为 `efficient_sft` |
| `n_epochs` | SFT/CPT/RL | 训练轮数（文本/语音/视频）；图像生成模型不使用此参数 | 文本 SFT：数据量 <10k 条时设为 3~5；视频微调：小数据集（2~5 条）推荐 50 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md) |
| `max_steps` | 万相图像生成 | 训练总步数（万相专属，千问图像模型不支持） | ≥500，推荐 800 |
| `learning_rate` | 全部 | 学习率，高效训练（LoRA）建议 `1e-4` 量级，全参训练建议 `1e-5` 量级 | 文本 SFT LoRA 默认 `3e-4`；语音调优默认 `5e-5`；视频微调默认 `2e-5` |
| `batch_size` | 全部 | 每次参数更新的样本数 | 图像/视频模型对 `batch_size` 敏感，`wan2.7-i2v` 推荐值为 1，不可随意增大 |
| `lora_rank` / `lora_alpha` | 高效训练 | LoRA 低秩矩阵维度与缩放因子 | 视频微调推荐 `lora_rank=32`, `lora_alpha=32`；文本 SFT 默认 `rank=8`, `alpha=16` |
| `max_length` | 文本 SFT/DPO/CPT | 单条数据最大 token 长度 | SFT 超长数据会被丢弃，DPO 会自动截断；推荐设为模型支持的最大值（如 8192） |

## 使用方式

- **控制台操作**：适用于文本生成模型的 SFT/DPO/CPT。进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)页面，创建任务 → 选择模型与训练方法（高效/全参）→ 上传或选择已发布数据集 → 配置超参 → 提交。评测集仅支持 xlsx 格式，且**仅支持本地上传与日志回流，不支持 OSS 导入** [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **API 调用**：通用方式，支持所有模型与训练类型。流程为：1) 上传数据文件（`/api/v1/files`，单文件 ≤300MB）→ 2) 创建训练任务（`/api/v1/fine-tunes`），在 `training_datasets` 中指定 `file_id` 或 `oss_mount` → 3) 查询状态。语音与视频模型**必须使用 API**，且其数据集需为 `.zip` 包（含 `data.jsonl` + 音频/图像/视频文件）。
- **RL 特殊流程**：需离线 SDK 开发 Rollout/Reward 函数，通过 `AgenticRL().run()` 一键提交，依赖函数计算（FC）、日志服务（SLS）和 OpenTelemetry 授权 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)。

## 限制和注意事项

- **地域与权限**：所有 fine tuning 功能（除基础 SFT 数据上传外）均严格限定在**华北2（北京）地域**；子账号需被授予 `AliyunBailianFullAccess` 或精细化的 `FineTuning` 相关权限。
- **数据与版本管理**：数据集类型（训练集/评测集）创建后**不可变更**；已发布版本**不可编辑**；切换训练方式（如 SFT→DPO）会清空已上传文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费差异**：
  - 控制台任务支持按 Token、训练单元预付费/后付费；
  - **API 创建的任务仅支持按 Token 计费**，且语音调优单价为 0.2 元/千 Tokens [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；
  - RL 训练**强制使用 MTU 训练单元**，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **模型产物**：调优产物为独立部署的新模型（非音色 ID 或风格插件），调用时需使用新生成的 `model_id`；CosyVoice 调优后 `voice` 参数必须固定为 `default`，无法切换音色。
- **安全合规**：使用 SFT 强化安全能力时，`system` 角色需明确定义合规边界，`assistant` 回答须体现拒绝与正向引导，避免仅依赖提示词工程 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)


