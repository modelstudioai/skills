# fine tuning

模型调优是提升大模型在特定业务、行业或价值观对齐方面表现的核心技术手段，适用于 Prompt 工程等轻量级优化无法满足效果要求的场景。百炼平台支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）、RL（强化学习）及 OPD（在线策略蒸馏）等多种调优范式，覆盖文本、图像、视频、语音等多模态模型。调优过程需结合数据质量、模型能力边界与训练资源配置进行系统性设计。

## 支持的模型/功能

百炼支持全系列千问（Qwen）文本生成模型、千问 VL 视觉理解模型、万相（Wan）图像/视频生成模型及 CosyVoice 语音合成模型的调优，但各模型支持的调优方式存在显著差异：

- **文本生成模型**：全面支持 CPT、SFT、DPO、RL 和 OPD。其中 Qwen3-32B、Qwen3-14B 等中大型模型支持全部训练模式（含全参与高效训练），而 Qwen3.7-Plus-2026-05-26 等部分 Plus 版本仅支持 CPT 全参训练，不支持 SFT 或 DPO [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问 VL）**：仅支持 SFT 全参与高效训练，不支持 CPT 或 DPO [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型（万相）**：仅支持 SFT 高效微调（LoRA），且训练控制参数与文本模型不同——万相按 `max_steps` 控制训练时长，千问文本模型则按 `n_epochs` 控制 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型（CosyVoice）**：仅支持 `efficient_sft` 方式，且必须使用 `cosyvoice-v3-flash` 基础模型；不支持 CPT、DPO 或 RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：文档 1 明确指出“Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”，而文档 20 的目录结构未体现该限制，实际使用中应以文档 1 的模型支持矩阵为准，避免选择不支持的训练方式导致任务创建失败。

## 关键参数

不同调优方式的核心参数差异较大，开发者需严格匹配模型能力与任务目标：

- **通用超参**（SFT/CPT/DPO）：`learning_rate`、`n_epochs`、`batch_size`、`max_length`、`lora_rank`（高效训练专用）等。其中 `learning_rate` 推荐值因训练方式而异：高效训练为 `1e-4` 量级，全参训练为 `1e-5` 量级，CPT 同样为 `1e-5` 量级 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成模型特有参数**：`max_steps`（总训练步数）、`generation_type`（`t2i`/`i2i`/`i2v`）、`max_pixels`（训练图片最大分辨率）等，无 `n_epochs` 概念 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **RL/OPD 特有参数**：`algorithm`（如 `gspo`）、`kl_loss_coef`、`n_rollouts`、`ppo_mini_batch_size` 等，且必须配置 `resources`（MTU 计费资源）[强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)；OPD 需额外指定 `teacher_model` 字段触发蒸馏 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。
- **语音合成模型特有参数**：`lm_max_epoch` 与 `fm_max_epoch`，其取值直接影响 Token 消耗与训练费用 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

调优任务可通过控制台或 API 两种方式发起，选择依据在于自动化程度与灵活性需求：

- **控制台方式**：面向快速验证与低代码场景，提供可视化向导。用户需依次完成任务命名、模型选择、训练方式（SFT/CPT/DPO）、数据集绑定、超参配置（可使用默认值）等步骤。该方式天然支持训练费用预估与实时日志查看 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 方式**：面向生产环境集成与批量任务管理，需通过 HTTP 请求提交。关键步骤包括：1）调用 `/api/v1/files` 上传训练数据（支持本地文件或 OSS 挂载）；2）调用 `/api/v1/fine-tunes` 创建训练任务，传入 `model`、`training_datasets`、`hyper_parameters` 等必填字段。API 方式仅支持按 Token 计费，不支持训练单元预付费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **特殊流程**：RL 和 OPD 训练需额外环境准备，包括 OpenTelemetry 授权、函数计算（FC）与日志服务（SLS）开通、SDK 安装及 `DASHSCOPE_API_KEY` 等环境变量配置 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)；CosyVoice 调优则强制要求通过 API 发起，控制台暂不支持 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 限制和注意事项

- **地域限制**：绝大多数调优功能（除纯文本 SFT 外）仅在华北2（北京）地域可用，包括 DPO、CPT、OSS 导入、云存储挂载、万相/视频生成模型调优及 CosyVoice 调优 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **数据格式强约束**：SFT 必须使用 JSONL 格式，每条记录为 `{"messages": [...]}` 结构；DPO 要求 `{"chosen": [...], "rejected": [...]}`；CPT 为纯文本 `{"text": "..."}`；图像/视频调优必须打包为 ZIP 文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费差异**：文本模型训练支持按 Token、训练单元预付费/后付费三种方式；而 RL 训练**仅支持训练单元计费**，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)；CosyVoice 训练费用由 `(lm_max_epoch + fm_max_epoch) × 25 × 总时长（秒）` 精确估算 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **产物与部署**：调优产物为独立模型，非基础模型下的音色 ID 或插件；CosyVoice 调优产物固定 `voice="default"`，不可切换音色 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；RL/OPD 产物需通过控制台“发布”后才能部署为 API 服务 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 来源文档

- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)


