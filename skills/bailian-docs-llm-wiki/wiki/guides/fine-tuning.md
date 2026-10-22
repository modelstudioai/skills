# fine tuning

模型微调（Fine Tuning）是提升大模型在特定业务场景下表现的核心技术手段。百炼平台支持多种训练范式，包括监督微调（SFT）、持续预训练（CPT）、直接偏好优化（DPO）、强化学习（RL）及在线策略蒸馏（OPD），覆盖从知识注入、任务对齐到偏好对齐与能力迁移的完整优化链条。所有训练方式均需通过华北2（北京）地域服务调用，且部分高级功能需联系商务经理开通。

## 支持的模型与功能

百炼支持文本生成、视觉理解（千问VL）、图像生成、视频生成、语音合成及决策模型六大类模型的微调，各类型支持的训练方式如下：

- **文本生成**：全面支持 CPT、SFT（全参/高效）、DPO（全参/高效）及 RL；[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md) 提供了详细的支持矩阵，例如 `qwen3-32b` 支持全部五种训练方式，而 `qwen3.7-plus-2026-05-26` 仅支持 SFT 全参训练。
- **视觉理解（千问VL）**：支持 SFT 和 DPO，但不支持 CPT 或 RL；[调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md) 明确指出 DPO/CPT 仅限北京地域，且不支持图片/视频输入的 DPO 训练。
- **图像/视频生成**：仅支持 SFT-LoRA 高效微调，如 `wan2.7-image-pro`、`wan2.7-i2v` 等模型；其超参数体系与文本模型不同（如万相按 `max_steps` 控制，千问按 `n_epochs` 控制）。
- **语音合成（CosyVoice）**：仅支持 `efficient_sft` 方式，且产出为独立部署的单音色模型，不支持 CPT/DPO/RL；[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md) 强调训练数据必须为同一发音人。
- **决策模型**：`decision-model-preview-2026-09-24` 不参与常规 CPT/SFT/DPO 流程，需使用专属微调流程；其数据格式为结构化 JSONL（含 `state` 和 `questions` 字段），与通用文本 SFT 完全不同。

> **注意**：文档 2 中表格显示 `Qwen3.6-Plus-2026-04-02` 支持 CPT 全参训练，但文档 4 的对应表格中该模型 CPT 列为 `×`。经交叉核对，文档 4 为最新 API 接口支持列表，应以文档 4 为准，即该模型当前不支持 CPT。

## 关键参数

不同训练方式的核心参数差异显著，开发者需按场景选择：

- **SFT/CPT/DPO**（控制台/API）：
  - `n_epochs`：循环次数，默认 `3`；数据量 < 10,000 条时推荐 `3~5` 次，> 10,000 条时推荐 `1~2` 次。
  - `learning_rate`：学习率，高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级。
  - `batch_size`：批次大小，通常设为 `16` 或 `32`。
  - LoRA 特有参数：`lora_rank`（默认 `8`）、`lora_alpha`（默认 `16`）、`lora_dropout`（默认 `0.1`）。
- **RL**：核心为 `algorithm`（如 `gspo`）、`batch_size`、`n_rollouts`、`kl_loss_coef` 及 `reward_metric_weight`；必须配置 `resources`（如 `mtu_spec_code: "MTU4"`），且**仅支持训练单元计费，不支持按 Token 计费**。
- **OPD**：必须指定 `teacher_model`（如 `qwen3.5-397b-a17b`）和 `model`（学生模型），`functions=None` 表示纯蒸馏；超参数中 `algorithm`、`learning_rate` 等与 RL 类似，但新增 `opd_teacher_*` 相关部署参数。
- **决策模型**：`batch_size` 默认为 `1`（因输入结构复杂），`learning_rate` 建议 `2e-5`，且 `training_type` 固定为 `efficient_sft`。

## 使用方式

- **控制台操作**：适用于快速验证，流程为「创建训练任务 → 选择模型与训练方式（CPT/SFT/DPO）→ 上传数据集 → 配置超参 → 提交」；[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md) 提供了可视化配置指南。
- **API/命令行**：适用于自动化与集成，流程为「上传文件（`/api/v1/files`）→ 创建训练任务（`/api/v1/fine-tunes`）→ 查询状态」；所有 API 调用均需 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，且文件上传 `purpose` 必须为 `"fine-tune"`。
- **SDK 编程**：RL 和 OPD 必须使用 `dashscope.finetune` SDK，通过 `AgenticRL().run()` 一步提交；需预先完成 OpenTelemetry 授权、设置 `FC_PYPI_LIB` 等环境变量，并编写 `RolloutProcessor`/`RewardProcessor` 函数组件。

## 限制和注意事项

- **地域与权限**：除文本 SFT 外，DPO、CPT、RL、OPD、图像/视频/语音微调均**仅支持华北2（北京）地域**；子账号需被授予模型调用、训练与部署权限。
- **数据规范**：
  - SFT 数据为 JSONL 格式，每行 `{"messages": [...]}`，支持 `system`/`user`/`assistant` 角色及 `loss_weight`（Qwen3.5+）；
  - DPO 数据需 `chosen`/`rejected` 对，CPT 数据为纯文本 `{text}`；
  - RL 数据需包含 `rollout_extra` 字段，OPD 数据需含 `rollout_extra.solution` 作为评分基准。
- **计费差异**：
  - 控制台支持按 Token、训练单元预付费/后付费三种方式；API 创建的任务**仅支持按 Token 计费**（见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)）；
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总时长（秒）× 0.2 元/千 Tokens`；
  - RL/OPD 必须使用训练单元（MTU），无 Token 计费选项。
- **模型产物**：微调后模型为独立部署实体，非基础模型的音色 ID 或插件；例如 CosyVoice 调优产物 `voice` 参数固定为 `default`，无法切换音色。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)


