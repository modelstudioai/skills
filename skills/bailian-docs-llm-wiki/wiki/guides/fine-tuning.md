# fine tuning

百炼平台的 fine tuning 是一种核心模型效果优化方式，通过在预训练模型基础上注入领域知识、对齐任务指令或人类偏好，显著提升模型在特定业务场景下的准确性、安全性与响应效率。它支持文本生成、视觉理解、语音合成、图像/视频生成及决策模型等多种模态，并提供 SFT、CPT、DPO、RL 和 OPD 等多种训练范式，兼顾效果、成本与工程灵活性。

## 支持的模型与功能

百炼支持多模态、多阶段的 fine tuning 能力：

- **文本生成**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等模型，覆盖 CPT（持续预训练）、SFT（监督微调）、DPO（直接偏好优化）和 RL（强化学习）四种方式。其中，CPT 用于补知识（如金融术语、法律条文），SFT 用于学做事（如客服流程、工具调用），DPO 用于做得更好（如拒有害建议、答干脆利落），而 RL 则通过 Reward 信号驱动自主策略优化 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
  
- **视觉理解（千问VL）**：支持 `qwen3-vl-8b-instruct` 等模型的 SFT 全参/高效训练，但暂不支持 CPT 或 DPO；数据格式需遵循多模态 SFT 规则（含图片/视频文件与 `data.jsonl` 描述文件）。

- **图像/视频生成**：万相（`wan2.7-image-pro`）与千问图像模型（`qwen-image-2.0`）支持 LoRA 高效微调，适用于文生图、图生图、图生视频等定制风格/特效场景；视频生成仅支持基于首帧或首尾帧的 SFT 微调 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **语音合成**：CosyVoice（`cosyvoice-v3-flash`）支持 SFT 高效微调，面向同一发音人多小时录音的高还原度音色定制，产物为独立部署的单音色模型，调用时 `voice` 固定为 `default` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **决策模型**：`decision-model-preview-2026-09-24` 支持专属微调流程，专用于分类、评分、是非判断等封闭集合决策任务，不参与常规 CPT/SFT/DPO 训练 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

- **在线策略蒸馏（OPD）**：支持学生模型（如 `qwen3.5-9b`）向更强教师模型（如 `qwen3.5-397b-a17b`）逐 token 学习概率分布，实现能力迁移与推理成本降低，适用于纯文本（Model OPD）或带工具调用（Agentic OPD）场景。

> **注意**：文档中关于“全参训练效果优于高效训练”的推荐（见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)）与实际工程权衡存在矛盾——高效训练（LoRA）在多数业务场景下收敛更快、成本更低、显存占用更小，且百炼官方表格明确标注部分小模型（如 `qwen3-1.7b`）仅支持高效训练。开发者应优先按模型支持矩阵选择，而非默认追求全参。

## 关键参数

fine tuning 的关键超参需结合训练方式与模型规模调整：

- **通用参数**：
  - `learning_rate`：SFT 高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5`；CPT/DPO/RL 通常更低（如 `2e-6`）。过高易震荡，过低难收敛。
  - `n_epochs`：数据量 < 10,000 条时建议 `3–5` 轮；> 10,000 条时 `1–2` 轮即可；OPD/RL 通常设为 `1`。
  - `batch_size`：默认值可用，典型取值 `16` 或 `32`；图像/视频生成中常设为 `1`（因分辨率高）。
  - `max_length`：建议设为模型支持的最大值（如 `8192`），SFT 超长数据会被丢弃，DPO 会自动截断。

- **LoRA 特有参数**（高效训练）：
  - `lora_rank`：默认 `8`，增大可提升表达能力但增加显存；图像/语音微调中常设 `32`。
  - `lora_alpha`：默认 `16`，控制缩放强度；`alpha / rank` 比值影响适配幅度。
  - `lora_dropout`：默认 `0.1`，防止过拟合。

- **OPD/RL 特有参数**：
  - `teacher_model`（OPD 必填）：指定更强教师模型 ID，触发蒸馏流程。
  - `algorithm`（RL）：如 `"gspo"`（广义策略优化）。
  - `kl_loss_coef`（RL）：平衡 KL 散度与奖励信号，默认 `0.002`。
  - `n_rollouts`（RL）：每步采样轨迹数，影响策略多样性。

## 使用方式

fine tuning 可通过控制台或 API 两种方式完成：

- **控制台操作**：访问 [模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”，依次配置：① 任务名称与优先级（L0–L3）；② 训练方法（CPT/SFT/DPO/RL）与模型；③ 数据集（需提前上传）；④ 超参（支持默认值一键填充）；⑤ 计费方式（[Token](../concepts/token.md)/预付费/后付费）。全流程可视化，适合快速验证 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **API 调用**：使用 DashScope SDK 或 HTTP 接口，分三步：
  1. **上传数据**：调用 `/api/v1/files` 上传 `jsonl`（SFT/DPO/CPT）、`zip`（多模态）、`xlsx`（评测集）等格式文件；
  2. **创建任务**：调用 `/api/v1/fine-tunes` 提交训练请求，传入 `model`、`training_file_ids`、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`；
  3. **监控与管理**：通过 `/api/v1/fine-tunes/{job_id}` 查询状态、日志与快照。

- **特殊流程**：
  - **RL/OPD**：需额外开发 Rollout（轨迹生成）与 Reward（评分）函数组件，并通过 SDK `AgenticRL().run()` 一步提交，自动完成函数注册、数据上传与任务调度 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
  - **语音/图像/视频**：仅支持 API 方式，且必须使用华北2（北京）地域的 API Key。

## 限制和注意事项

- **地域限制**：绝大多数 fine tuning 功能（除纯文本 SFT 外）仅支持华北2（北京）地域；DPO、CPT、OSS 导入、云存储挂载等功能明确限定于北京 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **数据规范**：
  - SFT 数据必须为 ChatML 格式的 `jsonl`，每行含 `messages` 数组（`system`/`user`/`assistant`）；
  - DPO 数据需包含 `chosen` 与 `rejected` 字段的偏好对；
  - CPT 数据为纯文本 `{text}` 的 `jsonl`；
  - 所有数据集类型（训练/评测）创建后不可变更，已发布版本不可编辑。

- **计费差异**：
  - 控制台支持 [Token](../concepts/token.md) 计费、预付费/后付费训练单元三种方式；**API 创建的任务仅支持按 [Token](../concepts/token.md) 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)；
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总时长（秒）× 0.2 元/千 Tokens`；
  - OPD/RL 训练必须使用 MTU（模型训练单元），不支持 Token 计费。

- **模型兼容性**：
  - 决策模型、CosyVoice、万相系列均不支持 CPT/DPO/RL，仅限 SFT 高效微调；
  - Qwen3.7-Plus-2026-05-26 等部分模型仅支持 SFT 全参训练，不支持高效训练；
  - `loss_weight` 字段仅默认支持 Qwen3.5+，旧版模型需联系商务经理开通。

- **安全与合规**：使用 SFT 强化安全能力时，系统提示词（`system` content）需明确约束模型行为边界，例如设定其为“严格遵守中国法律法规和社会主义核心价值观的安全合规助手” [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)


