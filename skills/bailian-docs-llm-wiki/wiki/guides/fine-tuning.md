# fine tuning

百炼平台的 fine tuning（模型调优）是提升大模型在特定业务、行业或安全合规场景下表现的核心能力，支持文本生成、视觉理解、图像/视频生成及语音合成等多种模态。它通过 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）和 RL（强化学习）等方法，将领域知识、任务指令、人类偏好或奖励信号注入模型参数，实现效果对齐与性能优化。所有调优任务均需在华北2（北京）地域执行，且不同模态与训练方式对应差异化的数据格式、超参体系与计费规则。

## 支持的模型/功能

百炼支持多模态、多阶段的模型调优能力：

- **文本生成**：覆盖 Qwen3 系列（如 `qwen3-8b`, `qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等数十个预置模型，支持 CPT、SFT（全参/高效）、DPO 和 RL 四种训练方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问 VL）**：支持 `qwen3-vl-8b-instruct` 等模型，仅限 SFT 和 DPO 高效训练，不支持 CPT 或全参训练。
- **图像/视频生成**：万相（`wan2.7-image-pro`）、千问图像（`qwen-image-2.0`）及万相视频（`wan2.7-i2v`）模型仅支持 SFT-LoRA 高效微调，不支持 CPT/DPO/RL [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成**：CosyVoice 模型（`cosyvoice-v3-flash`）仅支持 `efficient_sft` 方式，且必须通过 API 发起，控制台暂不支持 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）**：作为高级调优方式，支持 `qwen3.5-9b` 等指定模型，但需商务经理开通权限，并强制使用模型训练单元（MTU）计费，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

> **注意**：文档 1 中表格显示 `Qwen3.7-Plus-2026-05-26` 支持 CPT 全参训练，但文档 4 明确指出“CPT（继续预训练）：仅支持批次大小、学习率、循环次数……不支持 LoRA 相关参数、学习率预热比例和权重衰减”，且其训练方式字段为 `✓`；而文档 1 同行中该模型的 “CPT全参训练” 列为 `×`。经交叉验证，文档 1 的表格存在笔误，应以文档 4 的参数约束为准：CPT 仅支持全参训练（无 LoRA），且不兼容 LoRA 参数。实际训练时若选择 CPT，控制台不会展示 LoRA 相关配置项。

## 关键参数

不同调优方式与模态的关键参数差异显著，开发者需严格匹配：

- **通用超参（文本生成 SFT/DPO）**：`learning_rate`（高效训练推荐 `1e-4` 量级，全参/CPT 推荐 `1e-5`）、`n_epochs`（数据量 <10k 时建议 3–5 轮）、`max_length`（建议设为模型支持最大值，SFT 超长数据会被丢弃，DPO 自动截断）、`lora_rank`（高效训练推荐设为模型支持的最大值）[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **图像/视频生成专用参数**：万相模型使用 `max_steps`（训练总步数，≥500）、`eval_steps`（验证间隔）、`max_pixels`（训练图最大分辨率）；千问图像模型则使用 `n_epochs` 和 `eval_epochs`，且学习率不同（`qwen-image-2.0`: `5e-5`, `qwen-image-2.0-pro`: `1e-4`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成（CosyVoice）参数**：`lm_max_epoch` 与 `fm_max_epoch`（LM/FM 训练轮次），Token 消耗公式为 `(lm_max_epoch + fm_max_epoch) × 25 × 总音频秒数`，直接影响训练费用 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **强化学习（RL）必填参数**：`algorithm`（如 `gspo`）、`batch_size`、`n_rollouts`（每条 [prompt](prompt.md) 采样数）、`kl_loss_coef`（KL 散度惩罚系数）、`learning_rate`（通常 `2e-6` 量级），且 `resources` 必须指定 `mtu_spec_code`（如 `MTU4`）与 `mtu_capacity`（如 `24`）[强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。

## 使用方式

调优可通过控制台或 API 两种方式发起，适用场景不同：

- **控制台方式**：适用于快速验证、低代码需求。流程为：创建训练任务 → 选择模型与训练方法（SFT/CPT/DPO）→ 上传/选择已准备好的数据集 → 配置超参（默认值可直接使用）→ 提交。支持实时查看损失曲线（Training/Validation Loss）辅助判断是否过拟合或欠拟合 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 方式**：适用于自动化流水线、大规模批量任务或非文本模态（如图像、视频、语音）。需先调用 `/api/v1/files` 上传 `.jsonl`（文本）或 `.zip`（图像/视频/语音）文件获取 `file_id`，再调用 `/api/v1/fine-tunes` 创建任务。语音与 RL 任务**仅支持 API**，控制台不可用 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **数据准备规范**：
  - 文本 SFT：`jsonl` 格式，`messages` 数组含 `system`/`user`/`assistant` 角色，支持 `loss_weight`（Qwen3.5+）与 `<think>` 深度思考标签 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
  - 图像/视频：`.zip` 包含 `data.jsonl`（描述样本）与对应图片/视频文件，文生图需 `prompt` 字段，图生图需 `image_url` 字段 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - RL：`jsonl` 格式，每行含 `messages`（用户问题）与 `rollout_extra`（参考答案等业务数据），`rollout_extra` 会透传至 Reward 函数 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 限制和注意事项

- **地域与权限限制**：所有调优功能（除部分文本 SFT 外）仅在华北2（北京）地域可用；CPT/DPO/OSS 导入仅支持北京地域；RL 训练需完成 OpenTelemetry、函数计算（FC）和日志服务（SLS）三项云服务授权 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)、[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **数据与文件限制**：SFT/DPO 数据单文件上限 200 MB；API 上传单文件上限 300 MB，总空间配额 100 GB；图像分辨率长宽比不得超过 `200:1`，推荐控制在 `8K` 以内以防超时 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **计费差异**：文本生成调优支持按 Token、训练单元预付费/后付费三种方式；但 API 创建的任务**仅支持按 Token 计费**；RL 训练**强制使用训练单元（MTU）**，不支持按 Token 计费；CosyVoice 调优训练费用为 `0.2 元/千 Tokens`，部署费用另计 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)、[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **模型与训练方式绑定**：并非所有模型都支持全部训练方式。例如，千问 VL 模型不支持 CPT；CosyVoice 仅支持 `efficient_sft`；RL 模型需商务经理开通权限且仅限指定型号 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

## 来源文档

- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-function-development-guide.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)


