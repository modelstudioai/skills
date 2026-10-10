# fine tuning

模型微调（Fine Tuning）是百炼平台提供的核心模型优化能力，通过在特定领域数据上对预训练模型进行增量训练，显著提升其在垂直业务场景下的准确性、安全性与响应效率。它支持多种训练范式（SFT/CPT/DPO/RL/OPD），覆盖文本、图像、视频、语音及决策模型，并提供控制台可视化操作与 API 编程两种使用路径。微调后的模型可一键部署为生产级 API 服务。

## 支持的模型与功能

百炼支持多模态、多任务模型的细粒度调优，主要分为以下几类：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问 Plus 等，涵盖 SFT（监督微调）、CPT（继续预训练）、DPO（直接偏好优化）和 RL（强化学习）四种方式。其中 CPT 适用于注入行业知识（如金融术语、法律条文），SFT 用于教会模型执行具体任务（如客服流程、代码生成），DPO 则针对 bad case 进行偏好对齐（如拒有害建议、答干脆利落）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  
- **视觉理解（VL）与多模态模型**：支持 `qwen3-vl-8b-instruct` 等 VL 模型的 SFT 微调，兼容图片/视频输入及工具调用格式，但 DPO 和 CPT 不支持视觉理解场景 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **图像与视频生成模型**：万相（`wan2.7-image-pro`）和千问图像（`qwen-image-2.0`）支持 LoRA 高效微调，用于定制 IP 形象或特效风格；万相视频（`wan2.7-i2v`）支持图生视频微调，目标是稳定复现“金钱雨”“时尚杂志”等运动特效 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

- **语音合成模型**：仅支持 CosyVoice（`cosyvoice-v3-flash`）的 SFT 高效微调，面向同一发音人多条录音的高还原度音色定制，不支持 CPT/DPO [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **决策模型**：`decision-model-preview-2026-09-24` 支持微调，专用于封闭集合上的分类、评分与是非判断（如工单分流、内容审核），输出结构化概率而非自由文本 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

- **高级训练范式**：
  - **强化学习（RL）**：需自定义 Rollout（生成轨迹）与 Reward（评分）函数，适用于数学推理、Agent 工具调用稳定性优化等需自主探索的场景，**仅支持模型训练单元（MTU）计费，不支持按 [Token](../concepts/token.md) 计费** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
  - **在线策略蒸馏（OPD）**：用大教师模型（如 `qwen3.5-397b-a17b`）逐 token 指导小学生模型（如 `qwen3.5-9b`）训练，实现能力迁移与推理成本降低，支持纯蒸馏（零代码）与 Agentic（带工具调用）两种模式 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档 7 明确列出 `Qwen3.7-Plus-2026-05-26` 的调优后部署需联系商务经理，而文档 1 未提及该限制，此处以文档 7 的明确说明为准。

## 关键参数

参数配置需结合训练方式与模型类型，控制台与 API 均支持调整，但部分参数仅对特定训练方式生效：

- **通用超参**：
  - `n_epochs`：训练轮数，默认 `3`；数据量 < 10,000 条时推荐 `3~5` 轮，> 10,000 条时 `1~2` 轮。
  - `learning_rate`：学习率，高效训练（LoRA）推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级，CPT 同样适用 `1e-5` 量级。
  - `batch_size`：批次大小，通常设为 `16` 或 `32`，具体范围依模型和训练方式而定。
  - `max_length`：最大上下文长度，默认 `8192`，范围 `[500, 131072]`。
  - `lr_scheduler_type`：学习率调度器，推荐 `"linear"` 或 `"cosine"`。

- **LoRA 专用参数**（高效训练）：
  - `lora_rank`：秩值，默认 `8`。
  - `lora_alpha`：缩放因子，默认 `16`。
  - `lora_dropout`：丢弃率，默认 `0.1`，范围 `[0, 0.2]`。

- **图像/视频生成特有参数**：
  - 万相图像：使用 `max_steps`（训练总步数）替代 `n_epochs`，推荐不少于 `500` 步 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - 万相视频：`task_type` 区分 `"i2v"`（首帧）与 `"kf2v"`（首尾帧），`n_epochs` 仍为必填项（如 `50`） [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成特有参数**：
  - CosyVoice 调优使用 `lm_max_epoch` 与 `fm_max_epoch` 控制语言模型与声学模型训练轮次，[Token](../concepts/token.md) 消耗公式为 `(lm_max_epoch + fm_max_epoch) × 25 × 总音频秒数` [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **OPD/RL 特有参数**：
  - OPD：必须指定 `teacher_model`，并设置 `algorithm`（如 `"gspo"`）、`kl_loss_coef`（KL 散度系数）等。
  - RL：需配置 `algorithm`、`n_rollouts`（每轮采样数）、`ppo_mini_batch_size` 等 PPO 相关参数 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。

## 使用方式

### 控制台操作（推荐入门）
1. 进入 [模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”。
2. 选择训练方式（SFT/CPT/DPO/RL）、基础模型（首次推荐官方模型）及训练模式（高效/全参）。
3. 上传已准备好的数据集（支持拖拽或从已有数据集选择），系统自动校验格式。
4. 在“超参配置”面板中设置关键参数（如 `n_epochs`, `learning_rate`），其余可沿用默认值。
5. 提交任务，实时查看训练日志、损失曲线及验证指标。

### API/命令行操作（适合自动化）
1. **上传数据**：使用 DashScope API 上传 JSONL/ZIP 文件，获取 `file_id`：
   ```bash
   curl --request POST 'https://dashscope.aliyuncs.com/api/v1/files' \
     --header 'Authorization: Bearer ${DASHSCOPE_API_KEY}' \
     --form 'files=@data.jsonl' \
     --form 'purpose="fine-tune"'
   ```
2. **创建任务**：调用 `/api/v1/fine-tunes` 接口，传入 `model`、`training_datasets`（含 `file_id`）、`hyper_parameters` 及 `training_type`（如 `"sft"` 或 `"efficient_sft"`）。注意：API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

### 高级范式（RL/OPD）
- **RL**：需先完成环境授权（OpenTelemetry/FC/SLS），编写 Rollout/Reward 函数，再通过 SDK 的 `AgenticRL().run()` 提交，**必须使用 MTU 训练单元** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
- **OPD**：只需在 `run()` 中传入 `teacher_model` 参数即可触发蒸馏，纯蒸馏无需编写任何函数组件 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

## 限制和注意事项

- **地域限制**：绝大多数调优功能（SFT/DPO/CPT/OPD/RL）**仅支持华北2（北京）地域**；CosyVoice、万相图像/视频调优也强制要求北京地域 API Key [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **计费差异**：
  - 控制台支持按 Token、训练单元（预付费/后付费）三种计费方式；
  - **API 创建的任务仅支持按 Token 计费**，且无法使用训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)；
  - RL 训练**强制使用训练单元（MTU）计费**，不支持按 Token [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。

- **数据格式与规模**：
  - SFT 数据为 JSONL 格式，每行一个 `{"messages": [...]}` 对象，支持 system/user/assistant 多轮对话；
  - DPO 数据需包含 `chosen`/`rejected` 字段的偏好对；
  - CPT 数据为纯文本 JSONL（`{"text": "..."}`），需海量无标签数据（建议 ≥1000 万 Token）；
  - 所有文件单个上限 300MB（API）或 200MB（控制台），总配额 100GB/10000 个文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **训练方式互斥性**：虽然文档 2 和 11 提出“CPT→SFT→DPO→RL”的递进链路，但**同一模型实例不能同时启用 CPT 和 DPO**；训练类型在创建任务时即锁定，切换需新建任务 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **模型能力边界**：调优无法扩展基础模型的固有能力，例如 CosyVoice 调优不能增加新语种支持，万相图像调优不能改变其文生图/图生图的底层架构 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习概览](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [在线策略蒸馏概览](../../raw/model-user-guide/fine-tuning/opd-overview.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)


