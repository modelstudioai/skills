# fine tuning

百炼平台的 fine tuning（模型调优）是一套面向生产场景的模型能力增强体系，支持通过监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）、强化学习（RL）及在线策略蒸馏（OPD）等多种方式，将通用大模型适配至特定行业、业务或安全合规要求。调优过程可显著提升领域表现、抑制幻觉、对齐人类偏好，并降低推理延迟。

## 支持的模型与功能

百炼支持文本生成、视觉理解（千问VL）、图像生成、视频生成、语音合成及决策模型六大类模型的调优，但各类型支持的训练方式与地域存在差异：

- **文本生成模型**（如 Qwen3 系列）：全面支持 CPT、SFT（全参/高效）、DPO（全参/高效）及 RL 训练；其中 SFT/DPO/CPT 数据上传规则详见[调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **视觉理解模型**（如 Qwen3-VL 系列）：仅支持 SFT（全参/高效），不支持 CPT 和 DPO [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型**（万相、千问图像/视频）：仅支持 SFT-LoRA 高效微调，且训练控制参数不同（万相用 `max_steps`，千问用 `n_epochs`）[原文标题](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**（CosyVoice）：仅支持 `efficient_sft` 方式，且必须使用 `cosyvoice-v3-flash` 模型，不支持 CPT/DPO/RL [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**（`decision-model-preview-2026-09-24`）：不参与常规 CPT/SFT/DPO 流程，需使用专属微调流程，其数据格式与训练逻辑完全独立 [原文标题](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
- **在线策略蒸馏（OPD）**：为独立调优范式，需指定教师模型与学生模型，支持纯蒸馏（零代码）及 Agentic（带工具调用）模式，不与 SFT/CPT/DPO 互斥但机制完全不同。

> **注意**：文档 1 和文档 14 的表格中，Qwen3.7-Plus-2026-05-26 在“CPT全参训练”列均标为“×”，但文档 1 的说明文字称“Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”，未明确否定 CPT 支持；而文档 14 表格与文档 1 完全一致。此处以表格为准，视为不支持 CPT。若需确认，应联系商务经理。

## 关键参数

调优任务的核心参数分为通用超参与训练方式特有参数两类：

- **通用超参**（适用于 SFT/CPT/DPO）：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 同样适用 `1e-5` 量级。
  - `n_epochs`：循环次数，默认 `3`；数据量 < 10,000 条时建议 `3~5` 次，> 10,000 条时建议 `1~2` 次。
  - `batch_size`：默认值因模型而异，一般建议 `16` 或 `32`。
  - `lora_rank` / `lora_alpha` / `lora_dropout`：仅高效训练（LoRA）生效，默认值分别为 `8`、`16`、`0.1`。
  - `max_length`：最大上下文长度，默认 `8192`，范围 `[500, 131072]`。

- **训练方式特有参数**：
  - **RL**：`algorithm`（如 `gspo`）、`kl_loss_coef`、`n_rollouts`、`ppo_mini_batch_size` 等，需通过 SDK 的 `hyper_parameters` 字典传入 [原文标题](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。
  - **OPD**：必须指定 `teacher_model`，并配置 `opd_teacher_*` 相关超参（如 `opd_teacher_temperature`），`functions=None` 表示纯蒸馏模式。
  - **图像/视频生成**：万相模型使用 `max_steps`（建议 ≥500）而非 `n_epochs`；千问图像/视频模型则使用 `n_epochs`。

## 使用方式

调优可通过控制台或 API 两种方式发起，二者能力基本对等，但计费与权限略有差异：

- **控制台方式**：适用于快速验证与低代码场景。进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)页面，点击“创建训练任务”，按向导选择训练方法（SFT/CPT/DPO）、模型、数据集及超参。RL 和 OPD 任务需通过 SDK 提交，控制台仅提供入口引导。
- **API 方式**：适用于自动化流水线与批量任务。首先调用 `/api/v1/files` 上传数据集（单文件 ≤300MB），获取 `file_id`；再调用 `/api/v1/fine-tunes` 创建任务，请求体中指定 `model`、`training_datasets`（含 `file_id`）、`training_type`（如 `efficient_sft`）及 `hyper_parameters`。**注意**：通过 API 创建的任务仅支持按 [Token](../concepts/token.md) 计费，不支持训练单元（MTU）预付费/后付费 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **SDK 方式**（RL/OPD 必选）：RL 和 OPD 任务必须使用 DashScope Python SDK 的 `AgenticRL().run()` 方法提交，该方法自动完成函数注册、数据上传与任务提交。环境需配置 `DASHSCOPE_API_KEY` 及 `FC_PYPI_LIB`，并完成函数计算（FC）、日志服务（SLS）和 ARMS 的授权。

## 限制和注意事项

- **地域限制**：绝大多数调优功能（SFT/DPO/CPT/RL/OPD/决策模型）仅在华北2（北京）地域可用；图像/视频生成调优同样限定北京地域。
- **数据格式与规模**：
  - SFT 文本数据为 JSONL 格式，每条记录为 ChatML `messages` 数组；DPO 为 `chosen`/`rejected` 对；CPT 为纯文本 `{text}` 字段。
  - SFT 推荐数据量 ≥1000 条，DPO ≥100 组，CPT ≥1000万 [Token](../concepts/token.md)。
  - 视觉理解、图像、视频调优需 ZIP 打包（含 `data.jsonl` + 媒体文件），语音调优需多条同一发音人音频。
- **计费差异**：
  - 控制台任务支持按 [Token](../concepts/token.md)、训练单元·预付费、训练单元·后付费三种方式；API 任务仅支持按 Token 计费。
  - CosyVoice 调优费用 = 训练 Token 费（0.2 元/千 Tokens） + 部署模型单元费；RL/OPD 任务强制使用 MTU 训练单元（不支持 Token 计费）。
- **模型产物与部署**：
  - 调优产物为独立新模型（非基础模型下的音色 ID 或版本），部署后需通过新模型 ID 调用。
  - CosyVoice 调优产物固定 `voice="default"`，不可切换音色；决策模型调优后输出为分类/评分结果，不生成文本。
- **安全与合规**：SFT 是强化安全合规能力的核心手段，通过高质量指令数据（含 system/user/assistant 三元组）可使模型主动拒绝高危请求 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)


