# fine tuning

模型微调（Fine Tuning）是提升大模型在特定业务、行业或安全合规等场景下表现的核心技术手段。它通过在预训练模型基础上，使用领域数据进行有监督或偏好对齐训练，使模型习得专业知识、任务流程、价值观对齐等能力，而非仅依赖提示词工程。百炼平台支持文本生成、多模态理解、图像/视频生成、语音合成及决策模型等多种模态的微调能力，并提供控制台与 API 两种使用方式。

## 支持的模型与功能

百炼平台支持多种模型类型和训练方式，覆盖不同精度、成本与场景需求：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3-8b`、`qwen3-32b`）、Qwen2.5 系列及 `qwen-plus-character` 等，训练方式包括 CPT（持续预训练）、SFT（监督微调）、DPO（直接偏好优化）及 RL（强化学习）。其中 SFT 和 DPO 均支持全参训练与 LoRA 高效训练；CPT 仅支持全参训练 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)。
- **多模态模型（千问VL）**：支持图片/视频理解类模型（如 `qwen3-vl-8b-instruct`），当前仅支持 SFT 全参与高效训练，不支持 DPO/CPT [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)。
- **图像/视频生成模型**：万相（`wan2.7-image-pro`、`wan2.7-i2v`）与千问图像模型（`qwen-image-2.0`）均支持 SFT-LoRA 微调，但超参数语义不同（万相用 `max_steps`，千问用 `n_epochs`）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **语音合成模型**：仅支持 `cosyvoice-v3-flash` 的 SFT 高效微调（`efficient_sft`），不支持 CPT/DPO/RL，且产出为单音色独立部署模型，不可切换音色 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **决策模型**：`decision-model-preview-2026-09-24` 支持专属微调流程，采用结构化 JSONL 格式（含 `state` 与嵌套 `questions`），仅支持 `efficient_sft` 训练类型 [决策模型微调最佳实践](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。
- **强化学习（RL）与在线策略蒸馏（OPD）**：RL 需通过 SDK 提交，依赖函数计算（FC）与 OpenTelemetry 可观测性；OPD 支持纯蒸馏（零代码）与 Agentic 模式（需自定义 Rollout），教师模型必须与学生模型同族且更强 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)、[在线策略蒸馏训练概述](../../raw/model-user-guide/fine-tuning/opd-training-overview.md)。

> **注意**：文档中关于“DPO/CPT 仅支持北京地域”的描述与“决策模型需联系商务经理开通”的说明存在隐含冲突——前者属通用地域限制，后者属权限管控，二者不矛盾；但需注意 `qwen3.7-plus-2026-05-26` 模型虽在表格中标注支持 SFT 全参训练，其部署却需单独联系商务经理，该限制未在所有相关文档中统一强调 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 关键参数

不同训练方式与模型类型对应的关键参数存在显著差异，开发者需按场景选择：

- **通用超参**（SFT/DPO/CPT）：
  - `learning_rate`：高效训练推荐 `1e-4` 量级，全参训练推荐 `1e-5` 量级；CPT 统一用 `1e-5` [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
  - `n_epochs`：数据量 < 10,000 条时建议 3–5 轮，> 10,000 条时建议 1–2 轮；OPD/RL 中该参数仍有效，但 RL 更常以 `n_rollouts` + `batch_size` 控制迭代粒度。
  - `batch_size`：默认值因模型而异，常见为 16 或 32；图像/视频模型通常设为 1（受显存限制）[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - `max_length`：影响单条样本截断行为（SFT 丢弃超长样本，DPO 自动截断），建议设为模型支持的最大值。

- **LoRA 专用参数**（高效训练）：
  - `lora_rank`：默认 8，图像/视频模型示例中常用 32；增大可提升表达能力但增加显存占用。
  - `lora_alpha`：默认 16，控制适配权重缩放强度，通常与 `lora_rank` 同比例调整。

- **图像/视频模型特有参数**：
  - `max_steps`（万相）：训练总步数，建议 ≥500；`eval_steps` 为验证间隔，推荐 200 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
  - `max_pixels`：训练图最大分辨率（如 `"2k"`），系统仅对超限图片缩放。

- **RL/OPD 特有参数**：
  - `algorithm`：RL 常用 `gspo`，OPD 固定为蒸馏算法。
  - `kl_loss_coef`（RL）：KL 散度损失系数，控制策略更新稳定性。
  - `teacher_model`（OPD）：必填字段，指定更强教师模型 ID，传入即触发蒸馏 [在线策略蒸馏训练配置](../../raw/model-user-guide/fine-tuning/opd-training-overview/opd-training-config.md)。

## 使用方式

### 数据准备与上传
- **格式规范**：SFT 文本数据为 JSONL，基于 ChatML `messages` 结构（含 `system`/`user`/`assistant` 角色）；DPO 为 `chosen`/`rejected` 对；CPT 为纯文本 `{text}`；评测集为 XLSX 模板 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **上传途径**：
  - 控制台：在「数据管理」页面点击「新增数据集」，支持本地上传、OSS 导入（北京地域）、日志回流。
  - API：使用 `/api/v1/files` 接口上传，`purpose="fine-tune"`，单文件 ≤300 MB，总配额 100 GB / 10,000 文件 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

### 任务创建
- **控制台**：进入「模型调优」→「创建训练任务」，依次选择训练方法（CPT/SFT/DPO）、模型、数据集、超参，点击「开始训练」[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。
- **API**：调用 `/api/v1/fine-tunes`，请求体需包含 `model`、`training_file_ids`、`training_type`（如 `"efficient_sft"`）、`hyper_parameters` 字段 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **SDK（RL/OPD）**：使用 `AgenticRL().run()` 一步提交，自动完成函数注册、数据上传与任务启动，需提前配置 `DASHSCOPE_API_KEY` 与 FC 权限 [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/fine-tuning/rl-training-overview/rl-training-config-monitoring.md)。

### 部署与调用
- 微调完成后，模型自动发布至「我的模型」列表，可一键部署为 API 服务。
- 调用时，`model` 参数填写部署后的模型 ID（非基础模型 ID），例如 `qwen3-8b-finetuned-20240830`。

## 限制和注意事项

- **地域限制**：DPO、CPT、OSS 导入、云存储挂载仅支持北京地域；图像/视频/语音模型调优也强制要求北京地域 API Key [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)、[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **数据集约束**：数据集类型（训练集/评测集）创建后不可变更；切换训练方式（如 SFT → DPO）会清空已上传文件；已发布版本不可编辑 [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)。
- **计费差异**：
  - API 创建的任务**仅支持按 [Token](../concepts/token.md) 计费**，不支持训练单元；控制台任务则三种计费方式均可选 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
  - CosyVoice 调优费用 = 训练 [Token](../concepts/token.md) 费（0.2 元/千 [Token](../concepts/token.md)s）+ 部署模型单元费；RL/OPD 必须使用 MTU 训练单元（不支持 Token 计费）[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)、[强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。
- **模型能力边界**：调优无法扩展基础模型能力，例如 CosyVoice 调优不能新增语种支持，万相调优不能改变文生图/图生图模式 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。
- **训练稳定性**：SFT 训练中若 `Training Loss` 与 `Validation Loss` 持续下降，表明欠拟合，可增加 `n_epochs`；若验证损失上升而训练损失下降，则过拟合，应减少轮次或增大 `weight_decay` [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)
- [调优数据上传规则](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md)
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
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)


