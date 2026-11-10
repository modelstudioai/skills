# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或安全合规场景下表现的核心技术手段，支持从文本生成、多模态理解到语音合成、视频生成等全模态模型的定制化训练。其核心价值在于将领域知识、业务逻辑与人类偏好直接注入模型参数，而非依赖[提示词工程](../concepts/prompt.md)或后处理过滤，从而实现更稳定、更低延迟、更可控的推理效果。

## 支持的模型/功能

百炼支持多种调优方式与模型类型，覆盖文本、视觉、语音、视频及专用决策模型：

- **文本生成模型**：支持 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）、RL（强化学习）和 OPD（在线策略蒸馏）五种训练方式。Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列（如 `qwen2.5-7b-instruct`）及决策模型（`decision-model-preview-2026-09-24`）均全面支持 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。其中，决策模型仅支持 SFT 高效训练，不参与常规 CPT/SFT/DPO 流程，需参考专属指南 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
- **多模态模型**：千问 VL（Qwen3-VL 系列）支持 SFT 训练，但不支持 DPO 和 CPT [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **生成式模型**：万相图像生成（`wan2.7-image-pro`）、视频生成（`wan2.7-i2v`）及 CosyVoice 语音合成（`cosyvoice-v3-flash`）均仅支持 SFT 高效微调（LoRA），不支持全参训练或其他调优方式 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **专用模型**：OPD 蒸馏训练要求教师模型与学生模型同系列且能力更强（如 `qwen3.5-397b-a17b` → `qwen3.5-9b`），且仅限邀测客户使用 [OPD 蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档中关于“高效训练推荐优先级”的表述存在矛盾。[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md) 明确指出“如果模型支持全参训练，请优先选择全参训练，因为全参训练效果比高效训练效果要好，性价比更高”；而 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md) 在示例配置中却默认选用高效训练，并说明其“速度快、成本低”。开发者应根据效果要求与资源约束权衡：对效果敏感的生产环境优先选全参；对快速验证或成本敏感场景可选高效训练。

## 关键参数

调优任务的关键参数分为通用超参与模态特有参数两类：

- **通用超参**（适用于文本 SFT/DPO/CPT/RL/OPD）：
  - `learning_rate`：默认 `3e-4`，范围通常为 `1e-6`–`1e-3`；
  - `n_epochs`：默认 `3`，范围 `[1, 200]`；视频生成模型则用 `max_steps` 替代（如万相推荐 `≥500` 步）；
  - `batch_size`：默认值因模型而异，建议从 `16` 或 `32` 开始尝试；
  - `lora_rank` / `lora_alpha` / `lora_dropout`：仅高效训练有效，默认 `8` / `16` / `0.1`；
  - `max_length`：默认 `8192`，范围 `[500, 131072]`；
  - `eval_steps`：默认 `50`（控制台）或 `10`（安全合规示例），用于控制验证频率。

- **模态特有参数**：
  - **RL 训练**：必填 `algorithm`（如 `gspo`）、`n_rollouts`、`kl_loss_coef`、`ppo_mini_batch_size` 等 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)；
  - **OPD 训练**：必须指定 `teacher_model`，并配置 `opd_teacher_*` 相关部署参数 [OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)；
  - **CosyVoice 调优**：需设置 `lm_max_epoch` 与 `fm_max_epoch`，其值直接影响 [Token](../concepts/token.md) 消耗量 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

调优任务可通过控制台或 API 两种方式创建，二者能力基本对齐，但存在关键差异：

- **控制台方式**：面向无代码用户，提供可视化向导。支持全部五种训练方式（SFT/DPO/CPT/RL/OPD），可灵活选择计费模式（[Token](../concepts/token.md)/预付费/后付费），并实时显示任务摘要。适用于首次尝试、快速验证及决策模型等白名单服务 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。**注意**：CosyVoice 调优明确说明“控制台暂不支持”，必须使用 API [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **API 方式**：面向开发者，通过 HTTP 请求或 SDK（如 `dashscope.finetune`）提交任务。支持所有训练方式，但计费方式受限：通过 API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元预付费/后付费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。RL 和 OPD 训练强烈依赖 SDK 封装的函数组件（Rollout/Reward）与可观测性配置，需严格遵循 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md) 和 [OPD 模型开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md) 文档。

数据准备统一遵循 JSONL 格式，但结构因训练方式而异：
- SFT：`{"messages": [{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}`；
- DPO：`{"chosen": [...], "rejected": [...]}`；
- CPT：`{"text": "纯文本内容"}`；
- RL/OPD：需包含 `rollout_extra` 字段携带 `ground_truth` 或 `solution` [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

## 限制和注意事项

- **地域限制**：绝大多数调优功能（SFT/DPO/CPT/RL/OPD/决策模型）**仅在华北2（北京）地域可用**；部分功能（如 CosyVoice、万相图像/视频微调）也明确限定该地域 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)、[语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)。
- **计费限制**：API 创建任务**仅支持按 Token 计费**；而控制台支持三种计费方式。RL 训练**强制要求使用训练单元（MTU）计费，不支持按 Token 计费** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
- **数据与权限**：DPO/CPT/OSS 导入仅支持北京地域；所有调优任务均需 RAM 子账号具备对应模型调用、训练和部署权限 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **模型与数据约束**：CosyVoice 调优要求训练数据**必须为同一发音人**；决策模型输入数据中 `questions` 的 `label` 与 `target` 必须严格匹配 `criteria` 定义 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **功能边界**：调优无法扩展基础模型能力（如 CosyVoice 不支持新语种）；OPD 蒸馏中教师模型仅输出概率分布，不参与对话或[工具调用](../concepts/tool-calling.md) [OPD 蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [OPD 蒸馏训练](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [OPD 蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [OPD 蒸馏训练可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)


