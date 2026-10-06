# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或安全合规场景下表现的核心能力。它通过在预训练模型基础上进行有监督或无监督的增量训练，使模型学习领域知识、任务指令、人类偏好或决策逻辑，从而替代更重模型、降低延迟、抑制幻觉并强化价值观对齐。调优方式涵盖 SFT、CPT、DPO、RL 和 OPD 等多种范式，支持文本、多模态、语音、图像、视频及专用决策模型。

## 支持的模型与功能

百炼支持全栈模型调优能力，覆盖不同模态与任务类型：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`, `qwen3.5-plus-2026-02-15`）、Qwen2.5 系列及千问 Plus Character 模型，提供 CPT（补知识）、SFT（学做事）、DPO（做得更好）和 RL（学推理）四种训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问 VL）**：支持 `qwen3-vl-8b-instruct` 等模型的 SFT 训练，但暂不支持 DPO/CPT [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **图像/视频生成模型**：万相（`wan2.7-image-pro`, `wan2.7-i2v`）与千问图像模型（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，不支持全参训练或 DPO/RL [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 `efficient_sft` 方式，且必须为同一发音人多条录音；不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**：`decision-model-preview-2026-09-24` 专用于分类/评分/是非判断，仅支持 `efficient_sft` 微调，输入格式为结构化 JSONL（含 `state` 和 `questions` 字段）[决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
- **强化学习（RL）与在线策略蒸馏（OPD）**：均需通过 SDK 提交，依赖函数计算（FC）与 OpenTelemetry 可观测性，仅支持北京地域且需商务经理开通权限 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档 1 明确指出“本文档仅适用于华北2（北京）地域”，而文档 6、7、9、11、16 均强调图像/视频/语音/RL/OPD 功能“仅在华北2（北京）地域可用”。但文档 22（千问模型调优）作为总览页未限定地域，且文档 4（API 调优）示例中 OSS 挂载支持新加坡（ap-southeast-1）。实际使用时，除明确标注北京专属的功能外，基础 SFT/CPT/DPO 文本调优在其他地域可能受限，建议以控制台实际可选地域为准。

## 关键参数

调优任务的核心参数分为通用超参与模态特有参数两类：

- **通用超参（文本/SFT 主流配置）**：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 同样适用 `1e-5` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `n_epochs`：数据量 < 10,000 条时推荐 3–5 轮；> 10,000 条时推荐 1–2 轮；RL/OPD 中该参数常设为 `1` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `batch_size`：默认值通常可用；文本 SFT 推荐 16 或 32；决策模型因输入结构特殊，常设为 `1` [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
  - `max_length`：默认 `8192`，范围 `[500, 131072]`；图像/视频模型则用 `max_pixels` 控制分辨率 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
  - LoRA 参数：`lora_rank`（默认 8）、`lora_alpha`（默认 16）、`lora_dropout`（默认 0.1）；视频模型常设 `lora_rank=32` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **模态特有参数**：
  - 图像/视频：`max_steps`（万相核心参数，非 `n_epochs`）、`task_type`（`i2v` 或 `kf2v`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - RL：`algorithm`（如 `gspo`）、`kl_loss_coef`、`n_rollouts`、`ppo_mini_batch_size` [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。
  - OPD：`teacher_model`（必填，触发蒸馏）、`opd_teacher_*` 相关部署参数 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。
  - 决策模型：`finetuned_output_suffix`（输出模型名后缀），用于区分部署实例 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

## 使用方式

调优任务可通过控制台或 API/SDK 两种路径发起，选择依据为功能支持度与工程需求：

- **控制台（Web UI）**：适用于文本 SFT/CPT/DPO 的快速验证与常规调优。流程为：进入[模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning) → 创建训练任务 → 选择模型、训练方式（高效/全参）、上传数据集 → 配置超参 → 提交。支持实时费用预估与训练状态监控 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API（HTTP）**：适用于文本、决策模型等标准化调优。需先调用 `/api/v1/files` 上传数据（`purpose="fine-tune"`），再调用 `/api/v1/fine-tunes` 提交任务，请求体中指定 `model`、`training_datasets`（含 `file_id`）、`hyper_parameters` 等 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **SDK（Python）**：**唯一支持 RL 和 OPD 的方式**，也适用于复杂文本调优（如带自定义 Reward 函数）。需安装 `dashscope` SDK，编写 `RolloutProcessor`/`RewardProcessor` 类，通过 `AgenticRL().run()` 一键提交，自动完成函数注册、数据上传与任务调度 [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。
- **命令行（curl）**：适用于图像/视频/语音等非文本模型的轻量级调优，流程与 API 类似，但需手动处理文件上传响应中的 `file_id` 并填入后续请求 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 限制和注意事项

- **地域与权限限制**：CPT、DPO、RL、OPD、图像/视频/语音调优均**仅限华北2（北京）地域**；使用子账号（RAM 用户）需提前授予 `AliyunBailianFullAccess` 或最小化权限策略 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据格式强约束**：SFT 必须为 JSONL 格式，每行含 `messages` 数组（`system`/`user`/`assistant` 角色）；DPO 需 `chosen`/`rejected` 字段；CPT 为纯文本 `{text}`；决策模型为结构化 JSONL；所有格式均不支持嵌套数组或非法字符 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费差异**：控制台支持按 [Token](../concepts/token.md)、训练单元预付费/后付费；**API 创建的任务仅支持按 [Token](../concepts/token.md) 计费**；RL/OPD **强制要求使用训练单元（MTU）**，不支持 [Token](../concepts/token.md) 计费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)、[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
- **模型产物与部署**：调优产出为独立新模型（非原模型的音色 ID 或版本），需单独部署；CosyVoice 调优产物固定 `voice="default"`，不可切换音色；决策模型调优后仍需通过 `/v1/services/decision-model` 接口调用 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **训练稳定性**：高效训练（LoRA）收敛快、成本低，适合快速验证；全参训练效果更优但耗时长、费用高；文档 3 建议“如模型支持全参训练，请优先选择”，但文档 5 在安全合规案例中明确选用高效训练，开发者应根据效果目标与资源预算权衡 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

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
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)


