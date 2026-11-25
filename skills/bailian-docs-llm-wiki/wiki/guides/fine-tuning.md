# fine tuning

百炼平台的 fine tuning 是一套面向开发者、支持多模态与多训练范式的模型优化能力，涵盖监督微调（SFT）、继续预训练（CPT）、直接偏好优化（DPO）、强化学习（RL）和在线策略蒸馏（OPD）等多种范式。它适用于文本生成、图像生成、视频生成、语音合成及决策模型等场景，可显著提升模型在特定业务、行业或安全合规维度的表现，并支持从数据准备、训练配置到部署压缩的端到端流程。所有训练任务均需在华北2（北京）地域执行，且多数高级功能（如 DPO、CPT、RL、OPD）需联系商务经理开通权限。

## 支持的模型/功能

百炼支持多种模型与训练方式组合，覆盖文本、图像、视频、语音及专用决策模型：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3.5-9b`、`qwen3.8-27b`、`qwen3-32B`）的 SFT（全参/高效）、CPT、DPO 和 RL 训练；其中 `qwen3-32B` 是目前唯一支持全部五种训练方式（SFT/DPO/CPT/RL/OPD）的模型 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。Qwen3.7-Plus-2026-05-26 仅支持 SFT 全参训练，且调优后部署需联系商务经理。
  
- **图像与视频生成模型**：万相（`wan2.7-image-pro`、`wan2.7-i2v`）和千问图像模型（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，不支持 CPT/DPO/RL [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。视频生成模型（如 `wan2.7-i2v`）同样仅限 LoRA 微调，且必须使用北京地域 API Key。

- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 `efficient_sft` 高效微调，不支持 CPT/DPO/RL，且调优产物为单音色独立模型，调用时 `voice` 参数固定为 `default` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **决策模型**：`decision-model-preview-2026-09-24` 仅支持 SFT 高效训练，全参训练不可选，且当前为限时 0 元/千 token 计费 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

> **注意**：文档 2 中表格显示 `qwen3.6-plus-2026-04-02` 支持 CPT 全参训练，但文档 4 的“CPT、SFT、DPO 如何选择”章节明确指出 CPT 适用于“海量无标注数据”，而该模型未在文档 5 的 API 支持列表中列出 CPT 支持项。结合上下文，该模型的 CPT 支持可能已过时或受限于特定条件，建议以控制台实时选项为准。

## 关键参数

不同训练方式的关键参数差异显著，需按范式区分配置：

- **SFT/DPO/CPT 公共参数**（控制台/API）：
  - `learning_rate`：默认 `3e-4`，范围依模型而异；
  - `n_epochs`：默认 `3`，范围 `[1, 200]`；
  - `eval_steps`：默认 `50`，控制评估频率；
  - `loss_weight`：SFT 数据中可为单条样本指定重要性权重（取值 `(0.0, 1.0]`），Qwen3.5+ 默认支持 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **LoRA 特有参数**：`lora_alpha`（LoRA 缩放因子），仅在高效训练模式下出现；全参训练效果优于高效训练，阿里云推荐优先选用全参训练（若模型支持）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **RL/OPD 专属参数**：
  - RL：需配置 `mtu_capacity`（训练单元数量），其值必须严格等于 `nnodes_rollout × n_gpus_rollout + nnodes_training × n_gpus_training`，否则任务失败 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)；
  - OPD：核心是 `teacher_model` 字段，传入即触发蒸馏；`functions=None` 表示纯蒸馏（不注册任何函数组件），而 `functions=[]` 可能导致行为不一致，必须用 `None` [OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 使用方式

fine tuning 提供控制台与 API 两种入口，适用场景不同：

- **控制台**：适合快速验证与标准流程，支持 SFT/DPO/CPT/RL/OPD 五种训练方式创建，提供可视化参数配置、任务摘要与实时日志。SFT 微调还可零代码完成，尤其适用于安全合规强化等场景 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。决策模型微调也仅支持控制台提交（白名单开通）。

- **API/SDK**：适合自动化集成与复杂工作流。SFT/DPO/CPT 可通过 HTTP API 上传文件并创建任务；RL 和 OPD 必须使用 `dashscope.finetune.reinforcement` 或 `dashscope.finetune.agentic_rl` SDK 提交，需编写 Rollout/Reward 函数（RL/Agentic OPD）或仅传 `teacher_model`（纯 OPD）。CosyVoice 模型调优也仅支持 API 方式。

- **数据准备统一要求**：所有文本类训练（SFT/DPO/CPT/RL/OPD）均采用 JSONL 格式，但结构不同：
  - SFT：`{"messages": [{"role": "system/user/assistant", "content": "..."}]}`；
  - DPO：`{"chosen": [...], "rejected": [...]}`；
  - CPT：`{"text": "纯文本内容"}`；
  - RL/OPD：含 `rollout_extra` 字段透传业务数据（如 `solution` 或 `ground_truth`）。

## 限制和注意事项

- **地域与权限限制**：绝大多数 fine tuning 功能（SFT/DPO/CPT/RL/OPD/图像/视频/语音）仅在华北2（北京）地域可用，且需使用该地域的 API Key。DPO、CPT、OSS 导入、云存储挂载等功能明确限定为北京地域 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。RL 和 OPD 功能需联系商务经理开通权限。

- **计费与资源约束**：
  - API 创建的训练任务暂不支持模型训练单元（MTU），仅支持按 [Token](../concepts/token.md) 计费；而控制台任务可选 MTU 预付费/后付费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - CosyVoice 训练费用按公式 `消耗 Tokens = (lm_max_epoch + fm_max_epoch) × 25 × 训练集总时长(秒)` 估算，单价 0.2 元/千 [Token](../concepts/token.md)s [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - RL 训练成本极高（IV 型 MTU 后付费约 41 元/小时/实例），建议严格使用 [强化学习提交前自检](../../raw/model-user-guide/fine-tuning/rl-overview/rl-pre-submission-checklist.md) 进行本地测试与冒烟验证，避免任务启动后暴露错误。

- **数据与模型约束**：
  - 数据集类型（训练集/评测集）创建后不可变更；已发布版本不可编辑 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - 模型压缩仅支持百炼平台微调产出的自定义模型，不支持基础模型或第三方模型，且压缩不可逆、不支持二次压缩 [模型压缩](../../raw/model-user-guide/fine-tuning/model-compression-introduction.md)。
  - CosyVoice 调优要求训练数据必须为同一发音人，混合多发音人将导致音色还原度下降；调优也无法扩展基础模型的语种支持范围 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型压缩](../../raw/model-user-guide/fine-tuning/model-compression-introduction.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习提交前自检](../../raw/model-user-guide/fine-tuning/rl-overview/rl-pre-submission-checklist.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [OPD 蒸馏训练](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [OPD 蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [OPD 蒸馏训练可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)


