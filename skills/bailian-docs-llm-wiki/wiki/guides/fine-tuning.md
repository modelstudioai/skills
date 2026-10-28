# fine tuning

fine tuning 是阿里云百炼平台提供的核心模型优化能力，支持通过领域数据对预训练大模型进行定制化训练，以提升其在特定业务场景下的准确性、安全性、响应速度与合规性。该能力覆盖文本生成、视觉理解、语音合成、图像/视频生成及决策模型等多种模态，并提供 SFT（监督微调）、CPT（持续预训练）、DPO（直接偏好优化）、RL（强化学习）和 OPD（在线策略蒸馏）等多种训练范式，兼顾效果、成本与工程效率。

## 支持的模型与功能

百炼支持多类模型的 fine tuning，不同模型支持的训练方式存在差异：

- **文本生成模型**：全面支持 CPT、SFT（全参/高效）、DPO（全参/高效）及 RL 训练。例如 `qwen3-32b` 支持全部五种方式，而 `qwen3.7-plus-2026-05-26` 仅支持 SFT 全参训练 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解模型（千问VL）**：支持 SFT 全参/高效训练，但不支持 CPT 和 DPO [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **图像/视频生成模型（万相、千问图像）**：仅支持 SFT-LoRA 高效微调，且训练控制参数与文本模型不同（如万相使用 `max_steps`，千问使用 `n_epochs`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型（CosyVoice）**：仅支持 `efficient_sft` 方式，且必须为同一发音人多条录音，产出为独立部署的单音色模型 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**：`decision-model-preview-2026-09-24` 不参与常规 CPT/SFT/DPO 训练，需使用专属微调流程 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

> **注意**：文档 2 和文档 5 的表格中，`Qwen3.6-Plus-2026-04-02` 在 CPT 全参训练列均标为 ✓，但文档 2 明确说明“**重要**本文档仅适用于华北2（北京）地域”，而文档 5 未提地域限制。实际使用时，CPT 训练仅在北京地域可用，其他地域用户尝试将失败。

## 关键参数

fine tuning 的效果高度依赖超参数配置，关键参数及其推荐值如下：

- **`learning_rate`**：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 训练也推荐 `1e-5` 量级。过高易导致模型发散，过低则收敛缓慢 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **`n_epochs`**：数据量 < 10,000 条时推荐 3–5 轮；> 10,000 条时推荐 1–2 轮。过多轮次易过拟合 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **`batch_size`**：默认值通常适用，常见推荐值为 16 或 32。具体范围因模型和训练方式而异，需以控制台显示为准 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **`max_length`**：建议设为模型支持的最大值（如 8192）。SFT 会丢弃超长数据，DPO 则自动截断 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **LoRA 参数（`lora_rank`, `lora_alpha`, `lora_dropout`）**：高效训练专用，默认值（`rank=8`, `alpha=16`, `dropout=0.1`）适用于多数场景；调整 `rank` 和 `alpha` 可平衡效果与参数量 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 使用方式

fine tuning 可通过控制台或 API 两种方式完成，二者流程一致但细节有别：

- **控制台方式**：适用于快速验证和低代码场景。流程为：创建训练任务 → 选择模型与训练方法（CPT/SFT/DPO/RL）→ 上传或选择数据集 → 配置超参数 → 启动训练。控制台支持训练单元预付费/后付费及按 [Token](../concepts/token.md) 计费 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API 方式**：适用于自动化流水线和集成开发。需先调用 `/api/v1/files` 上传数据文件（`purpose="fine-tune"`），再调用 `/api/v1/fine-tunes` 创建训练任务。**通过 API 创建的任务仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元计费 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **特殊模型（RL/OPD/决策模型）**：必须使用 API（SDK）方式。RL 和 OPD 需要自定义函数组件（Rollout/Reward）并部署到函数计算；决策模型微调也仅支持 API 提交 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)、[在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-training-config.md)、[决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

## 限制和注意事项

- **地域限制**：绝大多数 fine tuning 功能（包括 CPT、DPO、RL、OPD）**仅在华北2（北京）地域可用**。部分模型（如 CosyVoice）明确声明仅支持北京地域 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **数据格式与大小**：SFT/DPO/CPT 数据需为 JSONL 格式，单文件上限 200 MB；API 上传单文件上限 300 MB，总配额 100 GB [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。视频生成模型数据需为 ZIP 格式 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **计费差异**：
  - 控制台支持三种计费方式：按 [Token](../concepts/token.md)、训练单元预付费、训练单元后付费。
  - **API 创建的任务仅支持按 Token 计费** [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - RL 训练**仅支持训练单元计费**，不支持按 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **模型选择逻辑**：对于文本生成模型，阿里云百炼推荐递进式训练顺序：`CPT（可选）→ SFT → DPO（可选）→ RL（可选）`，以分别实现补知识、学做事、做得更好、学推理的目标 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。

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
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-training-overview/observable-configuration-for-reinforcement-learning.md)
- [在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-agentic-development-guide.md)
- [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-training-config.md)
- [在线策略蒸馏可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)


