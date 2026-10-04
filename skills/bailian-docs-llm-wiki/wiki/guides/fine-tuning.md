# fine tuning

fine tuning 是百炼平台提供的核心模型优化能力，通过在特定领域数据上对预训练大模型进行增量训练，使其在垂直业务场景中获得更优效果、更低延迟和更强的安全合规性。该能力覆盖文本生成、视觉理解、语音合成、视频生成及决策模型等多种模态，并支持 SFT、CPT、DPO、RL 和 OPD 等多种训练范式，兼顾效果、效率与可控性。

## 支持的模型与功能

百炼 fine tuning 支持多类模型与训练方式，按模态和目标划分如下：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列及千问-Plus-Character 等，涵盖 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）和 RL（强化学习）四种核心方式 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。其中，SFT 用于教会模型“学做事”，CPT 用于“补知识”，DPO 用于“做得更好”，而 RL 则通过奖励信号驱动模型自主探索最优策略。

- **视觉理解模型（千问 VL）**：支持 `qwen3-vl-8b-instruct` 等多模态模型，仅支持 SFT 高效/全参训练，不支持 CPT 或 DPO [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **图像/视频生成模型**：万相（`wan2.7-image-pro`、`wan2.7-i2v`）与千问图像模型（`qwen-image-2.0`）均仅支持 SFT-LoRA 高效微调，训练目标为复现特定风格、IP 形象或特效 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)；视频生成同理，仅支持基于首帧或首尾帧的 LoRA 微调 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

- **语音合成模型**：CosyVoice（`cosyvoice-v3-flash`）仅支持 `efficient_sft` 方式，且必须使用同一发音人多条录音，产出为独立部署的单音色模型，不支持切换音色或新增语种 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **决策模型**：`decision-model-preview-2026-09-24` 专用于分类、评分、是非判断等封闭集合决策任务，支持高效微调，计费限时优惠 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

> **注意**：文档 2 明确指出“本文档仅适用于华北2（北京）地域”，但文档 3、7、10、12 等多处强调 DPO/CPT/OSS 导入/视频/语音等能力“仅支持北京地域”，而文档 22 的决策模型示例 API 地址包含中国站与新加坡站双地址。实际使用时，除纯文本 SFT 外，其余高级训练方式（CPT/DPO/RL/OPD/多模态/语音/视频）均强制要求北京地域，跨地域调用将失败。

## 关键参数

fine tuning 的效果高度依赖超参配置，不同训练方式与模型有差异化的推荐值：

- **通用参数**：
  - `n_epochs`（循环次数）：文本 SFT 推荐 1–5 次（数据量 <10k 时取 3–5）；视频 SFT 示例设为 50；RL 训练常设为 1；OPD 蒸馏也常为 1 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `learning_rate`（学习率）：高效训练（LoRA）推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级，CPT 同样为 `1e-5` 量级；CosyVoice 训练中 LM/FM 模块需分别设置 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `batch_size`（批次大小）：文本训练常用 16 或 32；视频训练示例中设为 1（因显存限制）；决策模型示例中设为 1 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

- **LoRA 特有参数**（高效训练）：
  - `lora_rank`：默认 8，视频训练示例中设为 32；
  - `lora_alpha`：默认 16，视频训练示例中设为 32；
  - `lora_dropout`：默认 0.1，范围 [0, 0.2]。

- **RL/OPD 特有参数**：
  - RL 使用 `algorithm`（如 `"gspo"`）、`kl_loss_coef`、`n_rollouts` 等；
  - OPD 必须指定 `teacher_model`，并可叠加 `reward_weight` 控制蒸馏与任务奖励的平衡 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)。

## 使用方式

fine tuning 可通过控制台或 API 两种方式发起，流程统一为：准备数据 → 创建任务 → 配置参数 → 提交训练。

- **数据准备**：所有训练方式均要求 JSONL 格式。SFT 文本数据采用 ChatML `messages` 结构（含 `system`/`user`/`assistant`）；DPO 数据需 `chosen`/`rejected` 字段；CPT 为纯文本 `{text}`；RL/OPD 数据需包含 `rollout_extra` 携带参考答案；语音/图像/视频数据需 ZIP 打包（含 `data.jsonl` + 媒体文件）[调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。

- **控制台操作**：进入 [模型调优页面](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”，依次选择训练方法（SFT/CPT/DPO/RL）、模型、数据集、训练模式（高效/全参），最后配置超参并提交。控制台实时显示费用预估 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

- **API 操作**：先调用 `/api/v1/files` 上传数据获取 `file_id`，再调用 `/api/v1/fine-tunes` 提交任务。API 仅支持按 [Token](../concepts/token.md) 计费，不支持训练单元预付费/后付费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。RL 和 OPD 还需额外部署 Rollout/Reward 函数组件，并通过 SDK 的 `AgenticRL().run()` 提交 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。

## 限制和注意事项

- **地域限制**：除基础文本 SFT 外，CPT、DPO、RL、OPD、多模态（VL）、语音（CosyVoice）、视频（万相）等高级训练能力**仅限华北2（北京）地域**。跨地域调用将报错 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

- **计费差异**：
  - 控制台支持按 [Token](../concepts/token.md)、训练单元预付费、训练单元后付费三种方式；
  - API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)；
  - CosyVoice 训练费用 = `(lm_max_epoch + fm_max_epoch) × 25 × 总时长(秒) × 0.2 元/千 Tokens`，与文本模型计费逻辑不同 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

- **数据与模型约束**：
  - 数据集类型（SFT/DPO/CPT）创建后不可变更；已发布版本不可编辑 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)；
  - CosyVoice 调优产物为单音色独立模型，`voice` 参数固定为 `default`，无法复用基础模型的声音复刻或设计能力 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)；
  - OPD 的教师模型必须与学生模型同系列且能力更强，且需商务经理邀测开通 [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)。

- **训练方式选择建议**：推荐递进式路径 `CPT（可选）→ SFT → DPO（可选）→ RL/OPD（可选）`，其中 CPT 注入领域知识，SFT 对齐任务指令，DPO 对齐人类偏好，RL/OPD 通过反馈信号持续优化 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
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


