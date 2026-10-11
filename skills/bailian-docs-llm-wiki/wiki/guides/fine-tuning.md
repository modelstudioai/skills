# fine tuning

模型微调（Fine Tuning）是百炼平台提供的核心模型优化能力，通过在预训练大模型基础上注入领域知识、业务逻辑或人类偏好，显著提升其在特定场景下的准确性、安全性与响应效率。该能力覆盖文本生成、视觉理解、语音合成、图像/视频生成及决策模型等多种模态，并支持 SFT、CPT、DPO、RL 和 OPD 等多种训练范式，兼顾效果、成本与工程可控性。

## 支持的模型与功能

百炼支持多模态、多阶段的模型调优能力：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`、`qwen3-14b`、`qwen3-32b`）、Qwen2.5 系列及千问 VL 视觉语言模型，训练方式涵盖 **SFT（监督微调）**、**CPT（持续预训练）**、**DPO（直接偏好优化）** 和 **RL（强化学习）** [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。其中，CPT 适用于注入海量无标签领域语料（如金融术语、法律条文），SFT 用于对齐指令与输出（如客服流程、代码范式），DPO 则通过正负样本对齐价值观（如拒有害建议、答干脆利落）。

- **多模态与生成模型**：  
  - **视觉理解（VL）**：支持 `qwen3-vl-8b-instruct` 等模型的 SFT 训练，但 **不支持 DPO/CPT** [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)；  
  - **图像/视频生成**：万相（`wan2.7-image-pro`）、千问图像（`qwen-image-2.0`）及图生视频模型（`wan2.7-i2v`）仅支持 **SFT-LoRA 高效微调**，目标为风格、IP 或特效的稳定复现；  
  - **语音合成**：`cosyvoice-v3-flash` 仅支持 **SFT 高效微调**，用于同一发音人音色的高还原度定制，**不支持 CPT/DPO/RL** [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；  
  - **决策模型**：`decision-model-preview-2026-09-24` 专用于分类、评分、是非判断等封闭集合决策任务，仅支持 `efficient_sft` 微调。

- **高级训练范式**：  
  - **RL（强化学习）**：需通过 SDK 开发自定义 Rollout（生成轨迹）与 Reward（评分函数），仅支持北京地域且**必须使用模型训练单元（MTU）计费，不支持按 Token 计费** [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)；  
  - **OPD（在线策略蒸馏）**：通过教师模型（如 `qwen3.5-397b-a17b`）对学生模型（如 `qwen3.5-9b`）进行逐 token 概率分布监督，支持纯蒸馏（零代码）与叠加 Reward 的进阶模式。

> **注意**：文档中关于“全参训练效果优于高效训练”的推荐与实际工程实践存在矛盾。[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md) 明确指出“由于两种训练方式的费用相同，阿里云百炼推荐您如果模型支持全参训练，请优先选择全参训练”，但该结论未考虑 LoRA 在收敛速度、显存占用和迭代效率上的显著优势，且未说明全参训练在多数业务场景下并非必要。开发者应根据数据规模、迭代周期与资源约束综合评估，而非默认采纳该推荐。

## 关键参数

超参配置需严格匹配训练方式与模型能力，以下为通用核心参数（部分参数仅在特定训练类型中生效）：

| 参数 | 默认值 | 说明 | 推荐范围/值 |
|------|--------|------|-------------|
| `training_type` | — | 训练方式标识 | `sft` / `dpo` / `cpt` / `efficient_sft` / `rl` / `opd` |
| `n_epochs` | `3` | 训练轮数（SFT/CPT/DPO）；RL/OPD 中为策略更新轮次 | SFT: 数据量 < 10k 条时设 `3–5`；≥10k 条时设 `1–2`；RL/OPD 通常 `1` |
| `batch_size` | — | 每步处理的数据条数 | 文本 SFT 常用 `16` 或 `32`；决策模型常为 `1`；视频生成常为 `1` |
| `learning_rate` | `3e-4`（SFT 高效） | 控制参数更新强度 | **高效训练**：`1e-4` 量级；**全参训练**：`1e-5` 量级；**CPT**：`1e-5`；**RL/OPD**：`1e-6`–`2e-6` |
| `max_length` | `8192` | 输入最大 token 数 | 范围 `[500, 131072]`，需与模型上下文窗口匹配 |
| `lora_rank` / `lora_alpha` | `8` / `16` | LoRA 低秩适配关键参数 | 视模型规模调整，视频/语音模型常设 `32` |
| `teacher_model` | — | OPD 必填，指定更强教师模型 | 如 `qwen3.5-397b-a17b` → `qwen3.5-9b` |

- **RL/OPD 特有参数**：`n_rollouts`（每轮采样数）、`kl_loss_coef`（KL 散度系数）、`algorithm`（如 `gspo`）等，详见 [强化学习训练配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md) 与 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。
- **地域限制**：CPT、DPO、OSS 导入、云存储挂载及 RL/OPD 全流程**仅支持华北2（北京）地域**；SFT、本地上传、API 上传全地域支持。

## 使用方式

调优任务可通过控制台或 API 两种方式发起，路径一致但能力边界不同：

- **控制台操作**（推荐快速验证）：  
  进入 [模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务” → 选择模型、训练方法（SFT/CPT/DPO）、训练模式（高效/全参）→ 上传或选择已发布数据集 → 配置超参 → 提交。控制台实时显示费用预估与任务摘要 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **API 调用**（推荐自动化与生产集成）：  
  1. **上传数据**：使用 `/api/v1/files` 接口上传 JSONL（SFT/DPO/CPT）、ZIP（多模态）或音频文件（CosyVoice），获取 `file_id`；  
  2. **提交任务**：调用 `/api/v1/fine-tunes`，传入 `model`、`training_datasets`（含 `file_id`）、`hyper_parameters` 及 `training_type`。  
     > **注意**：通过 API 创建的任务**仅支持按 Token 计费**，不支持训练单元预付费/后付费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

- **高级范式专用流程**：  
  - **RL**：需安装 DashScope SDK，开发 Rollout/Reward 函数，通过 `AgenticRL().run()` 提交，**强制依赖 MTU 训练单元**；  
  - **OPD**：除 `model` 外，**必须传入 `teacher_model`**，`functions=None` 表示纯蒸馏，`functions=[Reward...]` 表示叠加任务奖励。

## 限制和注意事项

- **地域与权限**：所有调优功能（除基础 SFT 上传外）均**仅限华北2（北京）地域**；使用子账号需授予 `AliyunBailianFullAccess` 或最小化权限策略（含 `bailian:CreateFineTuneJob`, `bailian:ListFiles` 等）。
- **数据格式强约束**：  
  - SFT 必须为 JSONL，`messages` 字段含 `system`/`user`/`assistant` 角色；  
  - DPO 要求 `chosen`/`rejected` 字段成对出现；  
  - CPT 为纯文本 `{text: "..."}` JSONL；  
  - 视频/语音数据必须 ZIP 打包，结构需严格匹配文档模板。
- **计费差异**：  
  - 控制台支持按 Token、训练单元预付费/后付费三种方式；  
  - **API 任务仅支持按 Token 计费**；  
  - RL/OPD **强制使用 MTU 训练单元**（不支持 Token 计费）；  
  - CosyVoice 调优费用 = 训练 Token 费（0.2 元/千 Tokens） + 部署模型单元费。
- **模型与训练方式兼容性**：  
  - `qwen3.7-plus-2026-05-26` 等新模型**仅支持 CPT 全参训练，不支持 SFT/DPO**；  
  - 千问 VL 模型**不支持 DPO/CPT**；  
  - 决策模型与 CosyVoice **仅支持 `efficient_sft`**。
- **产物与部署**：调优产物为独立模型（非音色 ID 或插件），部署后需通过新模型 ID 调用；CosyVoice 调优产物 `voice` 固定为 `default`，不可切换音色。

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
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)


