# fine tuning

fine tuning 是百炼平台提供的核心模型优化能力，支持通过领域数据对预训练大模型进行针对性调整，以提升其在特定业务场景下的准确性、安全性与响应效率。该能力覆盖文本生成、视觉理解、语音合成、图像/视频生成及决策模型等多种模态，并提供 SFT、CPT、DPO、RL 和 OPD 等多种训练范式，兼顾效果、成本与工程落地性。

## 支持的模型与功能

百炼支持多类模型的 fine tuning，按模态和训练方式划分如下：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列及千问 Plus 等共 20+ 官方模型，涵盖 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）和 RL（强化学习）四种方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **视觉理解模型（千问 VL）**：支持 `qwen3-vl-8b-instruct` 等 6 款模型，仅限 SFT 训练，不支持 DPO/CPT [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
- **图像/视频生成模型（万相）**：支持 `wan2.7-image-pro`、`wan2.7-i2v` 等，**仅支持 SFT 高效微调（LoRA）**，且必须使用华北2（北京）地域 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **语音合成模型（CosyVoice）**：仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调，**控制台暂不支持，必须通过 API 发起** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  
- **决策模型**：支持 `decision-model-preview-2026-09-24`，专用于分类、评分、是非判断等结构化输出任务，微调计费限时 0 元/千 token [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。  
- **强化学习（RL）与在线策略蒸馏（OPD）**：均需联系商务经理开通权限；RL 支持自定义 Rollout/Reward 函数，OPD 支持纯蒸馏（零代码）或叠加 Reward 的进阶模式 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档 2 中表格显示 `Qwen3.7-Plus-2026-05-26` 支持 CPT 全参训练，但文档 1 明确说明“Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”，且文档 4 未将其列入控制台可选模型列表。该模型实际可用性受限，建议优先选用 `Qwen3-32b` 或 `Qwen3-14b` 等明确标注全量支持的型号。

## 关键参数

不同训练方式的核心参数存在差异，开发者需根据任务目标合理配置：

- **通用超参**（SFT/DPO/CPT）：  
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 也适用 `1e-5` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  
  - `n_epochs`：数据量 < 10,000 条时建议 3–5 轮，> 10,000 条时建议 1–2 轮；RL/OPD 中该参数含义为训练轮次，但 OPD 更关注 `n_rollouts`（每轮采样数） [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。  
  - `batch_size`：默认值通常可用；图像/视频生成模型中 `wan2.7-i2v` 推荐设为 `1`，因输入分辨率高 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  

- **LoRA 专用参数**（高效训练）：  
  - `lora_rank`（默认 8）、`lora_alpha`（默认 16）、`lora_dropout`（默认 0.1）：影响低秩适配器的表达能力与泛化性，调优时可结合验证集 loss 曲线调整 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  

- **RL/OPD 特有参数**：  
  - RL：`kl_loss_coef`（KL 散度系数，默认 0.002）、`ppo_mini_batch_size`（PPO 小批量大小）；需搭配 MTU 训练单元资源 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。  
  - OPD：`teacher_model`（必填，指定更强教师模型）、`opd_teacher_*` 系列参数（控制教师前向行为）；纯蒸馏无需编写函数组件 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 使用方式

fine tuning 可通过控制台或 API 两种方式发起，选择依据为自动化程度与定制化需求：

- **控制台操作（推荐入门与快速验证）**：  
  访问 [模型调优控制台](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”，依次完成：① 选择模型与训练方式（SFT/CPT/DPO）；② 上传或选择已准备的数据集；③ 配置超参（支持默认值一键应用）；④ 设置计费方式（Token/预付费/后付费）。全流程可视化，适合无编码经验的开发者 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。  

- **API 调用（推荐生产集成与批量任务）**：  
  1. **上传数据**：使用 `/api/v1/files` 接口上传 JSONL（SFT/DPO/CPT）、ZIP（多模态）或 OSS 路径；单文件上限 300MB [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
  2. **提交训练**：调用 `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id` 或 `oss_mount`）、`hyper_parameters` 及 `training_type`（如 `"sft"` 或 `"efficient_sft"`）[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
  3. **高级训练（RL/OPD）**：必须使用 `dashscope.finetune` SDK，通过 `AgenticRL().run()` 提交，需预先配置函数组件、MTU 资源及 OpenTelemetry 依赖 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 限制和注意事项

- **地域与服务开通限制**：  
  - SFT/DPO/CPT 数据上传、本地上传、日志回流、API 上传全地域支持；但 **DPO、CPT、OSS 导入、云存储挂载仅支持华北2（北京）地域** [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
  - CosyVoice、万相图像/视频、RL、OPD 均**强制要求使用北京地域 API Key** [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。  

- **数据与格式约束**：  
  - SFT 文本数据必须为 JSONL 格式，每行一个 `{"messages": [...]}` 对象，支持 `system`/`user`/`assistant` 角色；`loss_weight` 字段仅默认支持 Qwen3.5+，旧版本需联系商务 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。  
  - RL 训练**仅支持按训练单元（MTU）计费，不支持按 Token 计费**；且必须完成阿里云 OpenTelemetry、函数计算（FC）、日志服务（SLS）三项授权 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。  

- **计费与资源**：  
  - 控制台支持 Token/预付费/后付费三种计费方式；**API 创建的任务仅支持按 Token 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。  
  - OPD/RL 训练需专属 MTU 资源，例如 `qwen3.5-9b` RL 训练推荐 IV 型模型单元 × 24，费用显著高于普通 SFT [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。  

- **安全与合规**：  
  - 使用 SFT 强化安全合规能力时，系统提示词（`system` content）需明确设定模型角色与行为边界，例如“严格遵守中国法律法规和社会主义核心价值观” [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。  
  - CosyVoice 调优产物为**单音色独立模型**，`voice` 参数固定为 `default`，不再支持声音复刻或声音设计等基础模型能力 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

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
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)


