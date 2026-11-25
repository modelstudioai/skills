# model training

模型训练是百炼平台的核心能力之一，支持从数据准备、模型微调、强化学习到蒸馏训练的全链路训练范式。平台提供 SFT、DPO、CPT、RL 和 OPD 五类主流训练方式，覆盖文本、多模态（视觉理解、文生图、图生视频）、语音合成及决策模型等场景，并与数据管理、模型评测、模型压缩等模块深度协同。所有训练任务均需通过控制台或 API 提交，计费按实际资源消耗（Token/训练单元/小时）结算。

## 支持的模型与功能

百炼支持多种模型类型和训练范式，但地域与模型组合存在明确限制：

- **文本生成模型**：支持 Qwen3 系列（如 `qwen3.8-27b`、`qwen3.6-flash-2026-04-16`）的 SFT（全参/高效）、DPO（北京地域）、CPT（北京地域）训练；强化学习（RL）需联系商务经理开通，支持 `qwen3.5-9b` 等模型 [原文标题](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。  
- **多模态模型**：图像生成（万相/千问）支持 SFT-LoRA 微调；视频生成（图生视频）支持基于首帧/首尾帧的 LoRA 微调；视觉理解模型支持 SFT 训练，但 DPO/CPT 不适用 [原文标题](../../raw/model-user-guide/model-training/fine-tuning/wan-image-generation-finetune-guide.md)。  
- **语音合成模型**：CosyVoice 仅支持 `efficient_sft` 方式，且仅限北京地域，不支持 CPT/DPO/RL [原文标题](../../raw/_short/fine-tune-speech-synthesis-model-by-api-961a082a0e1a5d8b.md)。  
- **决策模型**：`decision-model-preview-2026-09-24` 支持微调，专用于封闭集合分类、评分与是非判断任务，不生成文本 [原文标题](../../raw/model-user-guide/model-training/fine-tuning/decision-model-tuning-guide.md)。  
- **OPD 蒸馏训练**：支持 Model OPD（纯文本）与 Agentic OPD（工具调用/多轮交互），需指定教师模型（如 `qwen3.5-397b-a17b`），学生模型为同族小模型 [原文标题](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-training-overview.md)。

> **注意**：文档 7 中表格显示 `qwen3.7-plus-2026-05-26` 仅支持 SFT 全参训练，但文档 41 的模型压缩章节提及该模型“以控制台为准”，且未在压缩支持列表中明确列出；同时文档 42 的“我的模型”列表未包含该模型。建议以控制台实时展示为准，避免依赖过时表格。

## 关键参数

训练任务的关键参数因方式而异，核心配置如下：

- **通用参数**：任务名称（≤50 字符）、任务优先级（L0–L3，影响调度顺序）、基础模型 ID、训练/验证数据集 ID 或路径。  
- **SFT/DPO/CPT 数据格式**：  
  - SFT：`jsonl` 格式，ChatML messages 结构（含 `system`/`user`/`assistant`）；多模态需 `zip` 包含 `data.jsonl` + 媒体文件。  
  - DPO：`jsonl`，每行含 `chosen` 和 `rejected` 字段。  
  - CPT：`jsonl`，纯文本 `{text}` 字段。  
  详见 [调优数据上传规则](../../raw/_short/text-generation-tuning-data-upload-rules-28b04d7fad3dfa13.md)。  
- **RL 参数**：需定义 `Rollout`（轨迹生成）、`Reward`（评分）函数组件；超参如 `max_steps`、`learning_rate`、`batch_size` 通过 YAML 或 `run()` 接口配置 [原文标题](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-training-config-monitoring.md)。  
- **OPD 参数**：必填 `teacher_model`（触发蒸馏），可选 `RewardFunctionComponent` 叠加任务奖励；`functions=None` 表示纯蒸馏（Model OPD）[原文标题](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-model-development-guide.md)。  
- **量化模板（压缩）**：仅适用于已训练完成的模型，选择 MU 规格（如 MU5/MU8）决定部署成本，压缩不可逆 [原文标题](../../raw/model-user-guide/model-training/model-compression-introduction.md)。

## 使用方式

训练任务可通过控制台或 API 两种方式发起：

- **控制台流程**：  
  1. 在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)创建并发布训练集（类型为训练集，场景匹配目标模型）；  
  2. 进入[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击“创建训练任务”，选择训练方式（SFT/DPO/CPT/RL/OPD）；  
  3. 配置模型、数据集、超参（如 SFT 的 `n_epochs`、RL 的 `rollout_extra` 字段）；  
  4. 提交后可在任务列表监控状态、日志与指标。  

- **API 流程（推荐自动化）**：  
  - 使用 DashScope SDK 的 `AgenticRL().run()` 提交 RL/OPD 任务（需预装 `dashscope`）；  
  - SFT/DPO/CPT 文件上传通过 `/api/v1/files` 接口，`purpose="fine-tune"`；  
  - CosyVoice 调优仅支持 API，不支持控制台 [原文标题](../../raw/_short/fine-tune-speech-synthesis-model-by-api-961a082a0e1a5d8b.md)。  

- **数据准备辅助**：  
  - 日志回流：从 SLS 推理日志自动构建训练集，支持 SFT/DPO/CPT，需先授权 `AliyunServiceRoleForSFMAccessSLS` 等角色 [原文标题](../../raw/model-user-guide/model-training/model-data-overview/model-log-backflow.md)；  
  - 数据清洗/增强：仅北京地域可用，支持 SFT-文本生成训练集的敏感信息打码、特殊内容移除等，但不支持 SFT-图片理解或 DPO 训练集 [原文标题](../../raw/model-user-guide/model-training/model-data-overview/data-processing.md)。

## 限制和注意事项

- **地域限制**：DPO、CPT、OSS 导入、云存储挂载、日志回流（新加坡除外）、数据清洗/增强、模型压缩、CosyVoice 调优等功能**仅限华北2（北京）地域**；基线评测也仅在北京可用 [原文标题](../../raw/_short/create-baseline-evaluation-task-644af05297696563.md)。  
- **数据与模型约束**：  
  - 数据集类型（训练集/评测集）创建后不可变更；空数据集禁止发布；  
  - 训练集导入方式中，OSS 导入不支持评测集；日志回流单次上限 10 万条；  
  - 压缩后的模型不支持继续微调或二次压缩；导入模型仅支持 LoRA/全参微调产出，且全参导入需白名单 [原文标题](../../raw/model-user-guide/model-training/model-compression-introduction.md)。  
- **计费与资源**：  
  - API 创建的训练任务仅支持按 Token 计费，不支持预付费训练单元；  
  - RL 训练按训练单元小时计费（如 IV 型 24 实例约 984 元/小时），提交前务必完成自检（`test_functions.py`）以避免高成本失败 [原文标题](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-pre-submission-checklist.md)；  
  - 模型评测中，大模型评估维度产生裁判模型费用（当前限时免费），规则评估成本最低。  
- **安全与合规**：SFT 是强化安全合规能力的有效手段，通过高质量指令数据（如系统设定明确拒绝高危请求）使模型内在对齐价值观，优于仅依赖 Prompt 工程 [原文标题](../../raw/_short/enhance-the-security-compliance-of-large-models-20037a5f23c7138a.md)。

## 来源文档

- [数据管理](../../raw/model-user-guide/model-training/model-data-overview.md)
- [训练集与评测集](../../raw/model-user-guide/model-training/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-training/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-training/model-data-overview/model-log-backflow.md)
- [模型调优](../../raw/model-user-guide/model-training/fine-tuning.md)
- [千问模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model.md)
- [模型调优简介](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [调优数据上传规则](../../raw/_short/text-generation-tuning-data-upload-rules-28b04d7fad3dfa13.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/_short/enhance-the-security-compliance-of-large-models-20037a5f23c7138a.md)
- [微调图像生成模型](../../raw/model-user-guide/model-training/fine-tuning/wan-image-generation-finetune-guide.md)
- [语音合成模型调优](../../raw/model-user-guide/model-training/fine-tuning/fine-tune-speech-synthesis-model.md)
- [CosyVoice模型调优](../../raw/_short/fine-tune-speech-synthesis-model-by-api-961a082a0e1a5d8b.md)
- [强化学习](../../raw/model-user-guide/model-training/fine-tuning/rl-overview.md)
- [强化学习训练概述](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-training-overview.md)
- [强化学习开发指南](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-function-development-guide.md)
- [强化学习提交前自检](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-pre-submission-checklist.md)
- [强化学习训练配置 — 提交与配置](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/rl-training-config-monitoring.md)
- [强化学习的可观测配置与指标参考](../../raw/model-user-guide/model-training/fine-tuning/rl-overview/observable-configuration-for-reinforcement-learning.md)
- [OPD 蒸馏训练概述](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-training-overview.md)
- [Model OPD 开发](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-model-development-guide.md)
- [Agentic OPD 开发](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-agentic-development-guide.md)
- [OPD 蒸馏训练配置](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-training-config.md)
- [微调视频生成模型](../../raw/model-user-guide/model-training/fine-tuning/wan-video-generation-finetune-guide.md)
- [OPD 蒸馏训练可观测配置与指标参考](../../raw/model-user-guide/model-training/fine-tuning/opd-overview/opd-observable-config.md)
- [决策模型微调最佳实践](../../raw/model-user-guide/model-training/fine-tuning/decision-model-tuning-guide.md)
- [模型评测](../../raw/model-user-guide/model-training/model-evaluation-introduction/model-evaluation-overview.md)
- [评测任务](../../raw/model-user-guide/model-training/model-evaluation-introduction/evaluation-task-introduction.md)
- [创建自定义评测任务](../../raw/_short/create-custom-evaluation-task-ae5244ae7d5f81fe.md)
- [创建基线评测任务](../../raw/_short/create-baseline-evaluation-task-644af05297696563.md)
- [查看评测结果](../../raw/_short/view-evaluation-results-57262b43138e3408.md)
- [人工标注评测](../../raw/_short/evaluation-manual-annotation-d9499dc8f91f52e8.md)
- [排行榜](../../raw/model-user-guide/model-training/model-evaluation-introduction/evaluation-task-introduction/evaluation-leaderboard.md)
- [评测维度](../../raw/model-user-guide/model-training/model-evaluation-introduction/evaluation-dimension-introduction.md)
- [OPD 蒸馏训练](../../raw/model-user-guide/model-training/fine-tuning/opd-overview.md)
- [大模型评估](../../raw/_short/evaluation-dimension-llm-0e79ce833f170957.md)
- [规则评估](../../raw/_short/evaluation-dimension-rule-d98afe2913f0935b.md)
- [人工评估](../../raw/_short/evaluation-dimension-manual-f3bd8ee18da624b1.md)
- [模型评测](../../raw/model-user-guide/model-training/model-evaluation-introduction.md)
- [模型压缩](../../raw/model-user-guide/model-training/model-compression-introduction.md)
- [我的模型](../../raw/model-user-guide/model-training/my-model-center.md)
- [评测维度](../../raw/_short/evaluation-metrics-e2db7de73abf0cc7.md)


