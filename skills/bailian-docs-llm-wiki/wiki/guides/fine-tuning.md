# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，支持通过领域数据对预训练大模型进行定制化训练，以提升其在特定业务场景下的准确性、安全性、响应效率与价值观对齐能力。该能力覆盖文本生成、视觉理解、语音合成、图像/视频生成及决策模型等多种模态，并提供 SFT、CPT、DPO、RL 和 OPD 等多种训练范式，兼顾效果、成本与工程效率。

## 支持的模型/功能

百炼 fine tuning 支持多类模型与训练方式，按模态和任务类型划分：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列（如 `qwen2.5-7b-instruct`）及千问-Plus-Character 等，涵盖 CPT（持续预训练）、SFT（监督微调）、DPO（直接偏好优化）和 RL（强化学习）四种方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问VL）**：支持 `qwen3-vl-8b-instruct` 等，仅限 SFT 全参/高效训练，不支持 CPT/DPO [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型**：万相（`wan2.7-image-pro`, `wan2.7-i2v`）与千问图像模型（`qwen-image-2.0`）仅支持 SFT-LoRA 高效微调，训练控制参数为 `max_steps`（非 `n_epochs`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 `efficient_sft` 方式，且必须为同一发音人多条录音，产出为独立部署的单音色模型 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**：`decision-model-preview-2026-09-24` 不参与常规 CPT/SFT/DPO，但提供专属微调流程，专用于分类、评分、是非判断等封闭集合决策任务 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
- **在线策略蒸馏（OPD）**：支持学生模型（如 `qwen3.5-9b`）向更强教师模型（如 `qwen3.5-397b-a17b`）迁移能力，分为 Model OPD（纯文本）与 Agentic OPD（支持工具调用/多轮交互）[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-training-overview.md)。

> **注意**：文档 2 与文档 5 的表格中，`Qwen3.7-Plus-2026-05-26` 在 CPT 全参训练列均标为 `×`，但文档 2 明确说明“Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理”，暗示其可能支持特殊路径的 CPT；而文档 5 未提此说明。实际使用前请以控制台实时选项或商务确认为准。

## 关键参数

不同训练方式与模型类型对应的关键参数存在差异，开发者需根据场景选择：

- **通用超参**（SFT/CPT/DPO 控制台/API）：
  - `learning_rate`：SFT 高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5`；CPT 统一推荐 `1e-5` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `n_epochs`：数据量 < 10,000 条时建议 `3~5` 轮；> 10,000 条时建议 `1~2` 轮；视频生成模型则固定为 `n_epochs: 50` [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
  - `max_length`：设置为模型支持的最大值（如 `8192`），SFT 会丢弃超长样本，DPO 则自动截断 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `lora_rank`/`lora_alpha`：LoRA 高效训练专用，`lora_rank` 默认 `8`（图像/视频生成模型常设 `32`），`lora_alpha` 默认 `16`（视频生成模型常设 `32`）[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **RL/OPD 专用参数**：
  - RL 训练需配置 `algorithm`（如 `"gspo"`）、`kl_loss_coef`、`n_rollouts`、`ppo_mini_batch_size` 等 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。
  - OPD 训练必须指定 `teacher_model`，并可选配 `opd_teacher_*` 相关部署参数 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-training-config.md)。

## 使用方式

fine tuning 可通过控制台可视化操作或 API/CLI 编程方式完成，流程高度标准化：

1. **准备数据集**：按训练方式选择格式——SFT/DPO/CPT 使用 `jsonl`（ChatML messages 结构），评测集用 `xlsx`，图像/视频用 `zip` 包含 `data.jsonl` 与媒体文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。语音合成需准备同一发音人数小时高质量音频 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
2. **上传数据**：通过控制台“新增数据集”或 API `POST /api/v1/files` 上传，获取 `file_id` [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
3. **创建训练任务**：
   - 控制台：进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning) → “创建训练任务”，选择模型、训练方式（SFT/CPT/DPO/RL）、高效/全参训练，配置超参 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
   - API：调用 `POST /api/v1/fine-tunes`，传入 `model`、`training_file_ids`、`training_type` 及 `hyper_parameters` [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
   - RL/OPD：需额外准备函数组件（Rollout/Reward）或指定 `teacher_model`，通过 SDK `AgenticRL().run()` 一键提交 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-training-config.md)。
4. **监控与验证**：训练中查看 `Training Loss`/`Validation Loss` 曲线判断收敛性；RL/OPD 任务需在控制台“轨迹”页签观察 Span 链路与指标 [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)、[在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-observable-config.md)。

## 限制和注意事项

- **地域与权限限制**：绝大多数 fine tuning 功能（除部分图像/视频外）仅支持华北2（北京）地域；DPO/CPT/OSS 导入仅限北京；RL/OPD 训练必须使用模型训练单元（MTU），不支持按 Token 计费 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **数据与模型约束**：
  - SFT 数据单文件上限 `200 MB`，API 上传单文件上限 `300 MB`；DPO/CPT 数据量要求分别为 `100+` 组偏好对、`1000万+` Token [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - CosyVoice 调优必须使用同一发音人数据，混合发音人将导致音色还原度下降 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
  - 决策模型微调数据中 `target` 概率分布必须归一化（总和为 1），且训练/评估/线上请求的问题定义须严格一致 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
- **计费与资源**：
  - 控制台支持按 Token、训练单元预付费/后付费；API 创建任务仅支持按 Token 计费 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  - RL/OPD 训练强制使用 MTU 资源，需提前购买或开通后付费，最小计费粒度为分钟/小时 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-training-overview.md)。
- **工程实践建议**：
  - 推荐训练顺序为 `CPT（可选）→ SFT → DPO（可选）→ RL/OPD（可选）`，形成知识注入→能力习得→偏好对齐→策略优化的递进链条 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
  - 高效训练（LoRA）速度快、成本低，适合快速验证；全参训练效果通常更优，适用于生产环境 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

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
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)


