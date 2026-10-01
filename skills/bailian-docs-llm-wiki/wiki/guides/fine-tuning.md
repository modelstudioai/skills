# fine tuning

fine tuning 是百炼平台提供的核心模型优化能力，支持通过领域数据对基础模型进行定制化训练，从而提升其在特定业务场景下的准确性、安全性与响应效率。该能力覆盖文本生成、视觉理解、语音合成、图像生成、视频生成及决策模型等多种模态，并提供 SFT、CPT、DPO、RL、OPD 等多种训练范式，兼顾效果、成本与工程落地性。

## 支持的模型与功能

百炼支持多类模型的 fine tuning，不同模态和训练方式的兼容性存在地域与功能限制：

- **文本生成模型**（如 Qwen3 系列）：全面支持 SFT（全参/高效）、CPT、DPO 和 RL 训练，且支持深度思考（thinking）、工具调用（function calling）等高级能力 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **视觉理解模型**（Qwen-VL 系列）：仅支持 SFT 训练，不支持 CPT 或 DPO [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **图像/视频生成模型**（万相系列）：仅支持 SFT 高效微调（LoRA），不支持全参训练或偏好优化 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)；视频生成模型同理 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **语音合成模型**（CosyVoice）：仅支持 `efficient_sft` 方式，且必须使用 `cosyvoice-v3-flash` 模型，控制台暂不支持，仅限 API 调用 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **决策模型**：专用于分类、评分、是非判断等结构化输出任务，仅支持 `efficient_sft`，计费限时优惠 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。  
- **强化学习（RL）与在线策略蒸馏（OPD）**：均需通过 SDK 提交，依赖函数计算（FC）与 OpenTelemetry 可观测能力，且仅支持华北2（北京）地域 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档中关于“全参训练效果优于高效训练”的推荐（见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)）与实际工程实践存在矛盾——对于视觉/图像/视频/语音等生成类模型，官方明确仅支持高效训练（LoRA），全参训练不可用。该推荐仅适用于部分文本生成模型，开发者应以控制台可选参数或文档明确支持范围为准。

## 关键参数

fine tuning 的关键参数因训练方式和模型类型而异，以下为通用高频参数及其典型取值：

| 参数 | 默认值 | 推荐范围 | 说明 |
|------|--------|----------|------|
| `learning_rate` | `3e-4` | SFT 高效：`1e-4` 量级；SFT 全参/CPT：`1e-5` 量级；RL：`2e-6`；OPD：`1e-6` | 学习率过高易震荡，过低收敛慢；需按训练方式和模型规模调整 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md) |
| `n_epochs` | `3` | `<10,000 条数据：3–5`；`>10,000 条：1–2` | 文本生成 SFT 常用；视频/图像生成模型则使用 `max_steps` 替代 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) |
| `batch_size` | 控制台动态建议 | `1–32`（依模型显存而定） | 图像/视频生成任务常设为 `1`；语音合成任务按音频时长线性换算 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md) |
| `lora_rank` / `lora_alpha` | `8` / `16` | `rank`: `4–64`；`alpha`: `2×rank` 常见 | LoRA 核心超参，影响适配器容量与表达能力；视频生成示例中设为 `32` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md) |
| `max_length` | `8192` | `[500, 131072]` | 影响上下文长度与显存占用，需匹配训练数据平均长度 |

此外，RL 和 OPD 引入专属参数：`algorithm`（如 `gspo`）、`kl_loss_coef`、`n_rollouts`、`teacher_model`（OPD 必填）等，详见对应文档。

## 使用方式

fine tuning 可通过控制台或 API 两种方式发起，选择依据为自动化程度与灵活性需求：

- **控制台方式**：适用于快速验证与标准流程，支持 SFT/CPT/DPO 训练，提供可视化参数配置、费用预估与实时日志 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
- **API 方式**：适用于批量任务、CI/CD 集成与复杂训练流程（如 RL、OPD），所有 API 调用统一使用 `https://dashscope.aliyuncs.com/api/v1/fine-tunes` 端点，但需注意：  
  - 通过 API 创建的任务**仅支持按 Token 计费**，不支持训练单元预付费/后付费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)；  
  - RL 和 OPD 必须使用 DashScope SDK（非纯 HTTP），需完成 FC 函数部署、OpenTelemetry 授权与环境变量配置 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。  

数据准备是前置关键步骤：SFT/DPO/CPT 文本数据需为 JSONL 格式，遵循 ChatML messages 结构；多模态数据需打包为 ZIP 并包含 `data.jsonl` + 媒体文件；RL/OPD 数据需含 `rollout_extra` 字段以透传参考答案 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

## 限制和注意事项

- **地域限制**：CPT、DPO、RL、OPD 及所有生成类模型（图像/视频/语音）的 fine tuning **仅支持华北2（北京）地域**；文本生成 SFT 全地域可用 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  
- **计费差异**：  
  - 控制台支持按 Token、训练单元预付费/后付费三种方式；  
  - API 创建任务**强制按 Token 计费**；  
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总时长（秒） × 0.2 元/千 Tokens`，与文本模型计费逻辑不同 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **数据与版本管理**：数据集类型（训练集/评测集）创建后不可变更；切换训练方式（如 SFT → DPO）会清空已上传文件；各训练方式新增版本需重新导入全部数据 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **安全合规提示**：使用 SFT 强化安全能力时，系统设定（system [prompt](prompt.md)）需明确约束模型行为边界，且训练数据应覆盖政治、历史、社会等多维度风险场景 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)


