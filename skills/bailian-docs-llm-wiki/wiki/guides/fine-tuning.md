# fine tuning

百炼平台的 fine tuning（模型调优）是一套面向开发者、覆盖多模态与多任务的模型定制能力，支持通过 SFT、DPO、CPT、RL、OPD 等多种训练范式，在文本生成、视觉理解、图像/视频生成、语音合成及决策建模等场景中提升模型在特定业务、行业或安全合规维度的表现。调优过程可全程通过控制台可视化操作或 API 编程完成，底层统一基于 LoRA 高效训练与全参训练双模式，并按 [Token](../concepts/token.md) 或训练单元计费。

## 支持的模型与功能

百炼支持对**文本生成、视觉理解（千问VL）、图像生成（万相/千问图像）、视频生成（万相图生视频）、语音合成（CosyVoice）及决策模型**六大类模型进行 fine tuning，但各模态支持的训练方式存在显著差异：

- **文本生成模型**（如 `qwen3.8-27b`, `qwen3-14B`）：全面支持 CPT（继续预训练）、SFT（监督微调）、DPO（直接偏好优化）、RL（强化学习）和 OPD（在线策略蒸馏）五种方式，且多数模型同时支持全参训练与高效训练（LoRA）。[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md) 中的表格明确列出了各模型对不同训练方式的支持状态。
- **视觉理解模型**（如 `qwen3-vl-8b-instruct`）：仅支持 SFT 全参与高效训练，不支持 DPO、CPT 或 RL。
- **图像/视频生成模型**（如 `wan2.7-image-pro`, `wan2.7-i2v`）：仅支持 SFT-LoRA 高效微调，且训练控制参数为 `max_steps`（步数）而非 `n_epochs`（轮数），详见 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 和 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成模型**（`cosyvoice-v3-flash`）：仅支持 SFT 高效微调，且必须为同一发音人多条录音，产出为独立部署的单音色模型，不支持 CPT/DPO/RL [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**（`decision-model-preview-2026-09-24`）：仅支持 SFT 高效训练，不支持全参训练，其数据格式为结构化 JSONL（含 `state` 与 `questions` 字段），与通用文本 SFT 完全不同 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

> **注意**：文档中关于“DPO/CPT 仅支持北京地域”的描述与“RL 训练仅支持通过模型训练单元（MTU）计费”存在隐含矛盾——前者是地域限制，后者是计费方式限制，二者不冲突；但需注意 RL 的 MTU 资源申请必须严格匹配 `nnodes_rollout × n_gpus_rollout + nnodes_training × n_gpus_training` 公式，否则任务提交失败 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。

## 关键参数

调优任务的核心参数分为**通用超参**与**模态特有参数**两类：

- **通用超参**（适用于文本 SFT/DPO/CPT 及部分 OPD/RL）：
  - `learning_rate`：默认 `3e-4`，范围通常为 `[1e-6, 1e-3]`；
  - `n_epochs`：默认 `3`，范围 `[1, 200]`（图像/视频模型使用 `max_steps` 替代）；
  - `batch_size`：默认值因模型而异，建议保持默认；
  - `lora_rank` / `lora_alpha` / `lora_dropout`：LoRA 高效训练专属，控制低秩适配器规模与正则强度，默认值分别为 `8`、`16`、`0.1`；
  - `max_length`：默认 `8192`，范围 `[500, 131072]`，影响上下文长度与显存占用。

- **模态特有参数**：
  - **图像/视频生成**：`max_steps`（必需，推荐 ≥500）、`task_type`（`i2v` 或 `kf2v`）、`max_pixels`（图像分辨率上限）；
  - **语音合成**：`lm_max_epoch` 与 `fm_max_epoch`（分别控制语言模型与声学模型训练轮次），直接影响 [Token](../concepts/token.md) 消耗量；
  - **RL 训练**：`algorithm`（如 `gspo`）、`kl_loss_coef`、`n_rollouts`、`ppo_mini_batch_size` 等，需结合 Reward 函数设计；
  - **OPD 蒸馏**：`teacher_model`（必需，指定教师模型 ID）、`opd_teacher_*` 系列参数（控制教师模型调用行为）。

所有参数均以 `hyper_parameters` 字典形式传入 API，控制台界面会根据所选模型动态过滤不可用参数。

## 使用方式

fine tuning 可通过**控制台**或**API/SDK**两种方式启动，流程高度一致：**准备数据集 → 创建训练任务 → 配置参数 → 提交训练 → 监控与部署**。

- **数据准备**：必须遵循对应训练方式的数据格式规范。SFT 文本生成要求 `jsonl` 文件，每行含 `messages` 数组（`system`/`user`/`assistant` 角色）；DPO 要求 `chosen`/`rejected` 字段；CPT 为纯文本 `{text}`；RL/OPD 则需 `rollout_extra` 携带参考答案。所有数据均需通过 `/api/v1/files` 接口上传并获取 `file_id`，该 ID 在创建训练任务时作为 `training_file_ids` 参数传入 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **任务创建**：
  - 控制台：在 [模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning) 页面点击“创建训练任务”，选择训练方式（SFT/DPO/CPT/RL/OPD）、基础模型、数据集及超参后提交。
  - API：调用 `POST /api/v1/fine-tunes`，请求体中指定 `model`、`training_file_ids`、`training_type`（如 `"efficient_sft"`）及 `hyper_parameters`。
- **高级训练**（RL/OPD）：需额外开发函数组件（Rollout/Reward）并打包上传。RL 要求用户编写 Python 函数处理轨迹生成与评分；OPD 则分 Model OPD（零代码纯蒸馏）与 Agentic OPD（需自定义 Rollout 处理工具调用） [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)。

## 限制和注意事项

- **地域与服务开通**：绝大多数 fine tuning 功能（除 CosyVoice 外）仅在**华北2（北京）地域**可用，且需确保账号已开通百炼服务、获得相应 RAM 权限，并为 RL/OPD/决策模型等新功能单独申请白名单或联系商务经理开通 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据与版本管理**：数据集类型（训练集/评测集）创建后不可变更；已发布版本不可编辑；切换训练方式（如从 SFT 改为 DPO）会清空已上传文件 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费差异**：
  - 控制台任务支持按 [Token](../concepts/token.md)、训练单元预付费/后付费三种方式；
  - **API 创建的任务仅支持按 Token 计费**，不支持训练单元 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)；
  - CosyVoice 调优费用 = 训练 Token 费（0.2 元/千 Tokens） + 部署模型单元费；
  - RL/OPD 必须使用模型训练单元（MTU），不支持 Token 计费 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)。
- **模型与输出约束**：调优产物为独立模型，非基础模型下的配置项。例如 CosyVoice 调优后 `voice` 参数强制为 `default`，无法切换音色；决策模型调优后仅支持结构化决策输出，不生成文本。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习开发指南](../../raw/model-user-guide/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md)
- [OPD 蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [Model OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-model-development-guide.md)
- [OPD 蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-config.md)
- [Agentic OPD 开发](../../raw/model-user-guide/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [OPD 蒸馏训练可观测配置与指标参考](../../raw/model-user-guide/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)
- [OPD 蒸馏训练](../../raw/model-user-guide/fine-tuning/opd-overview.md)


