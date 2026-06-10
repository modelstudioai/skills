# fine tuning

阿里云百炼的模型调优（Fine-tuning）是在通用大模型基础上，通过训练数据进一步调整模型参数，以提升模型在特定行业或业务场景表现的优化手段。当 Prompt 工程、插件调用等方法难以达到预期效果时，模型调优可作为"最后的手段"，把领域知识、表达习惯、安全合规等目标直接写入模型参数。模型在调优过程中会学习训练数据中的知识、语气、表达习惯和自我认知等业务特征，训练后 One-Shot / Zero-Shot 的 Prompt 效果通常优于训练前的 Few-Shot，可节省大量输入 Token 并降低输出延迟。

## 调优方式

百炼提供三种训练方式，分别对应不同的优化目标，可按需单独使用或组合使用。

| 方式 | 全称 | 目标 | 数据要求 | 典型应用 |
| --- | --- | --- | --- | --- |
| CPT | 持续预训练（Continue Pre-Training） | 注入领域知识 | 1000 万+ Token 无标签文本 | 金融 / 医疗 / 法律等专业领域 |
| SFT | 监督微调（Supervised Fine-Tuning） | 教会模型遵循指令 | 1000+ 条高质量问答对 | 客服机器人、代码助手、Agent 工具调用 |
| DPO | 直接偏好优化（Direct Preference Optimization） | 对齐人类偏好 | 100+ 组"好-差"回答对 | 安全合规、简洁性、客观中立 |

学习方式上，CPT 采用自监督学习（预测下一个词），SFT 采用监督学习（模仿标准答案），DPO 采用直接偏好学习（增大好答案概率、降低坏答案概率）。典型递进流程为 `CPT（可选）→ SFT → DPO（可选）`：先用 CPT 补知识广度与深度，再用 SFT 学做事（对话格式、任务执行），最后用 DPO 做得更好（对齐价值观与偏好）。

## 训练模式

SFT 与 DPO 均提供两种训练模式：

- **全参训练**：更新模型全部参数，适合需要模型学习新能力、追求全局效果最优的场景。训练时间较长、收敛速度较慢、成本较高。
- **高效训练（LoRA，推荐）**：仅更新低秩修正矩阵，适合对训练时间和成本敏感的场景。收敛速度快，是百炼推荐的首选模式。二次高效微调时，`lora_rank`、`lora_alpha`、`lora_dropout` 三个参数必须保持一致。

## 支持的模型

### 文本生成（Qwen 系列）

覆盖 Qwen3.6、Qwen3.5、Qwen3、Qwen2.5 等多代模型，规模从 0.6B 到 72B，包括 `qwen-plus-character-2025-11-06` 等角色模型。不同模型支持的训练方式不同：

- Qwen3-32B、Qwen3-30B-A3B-Instruct-2507、Qwen2.5-72B/32B/14B/7B-Instruct 等旗舰模型同时支持 CPT / SFT 全参 / SFT 高效 / DPO 全参 / DPO 高效全套方式。
- Qwen3-14B / 8B、Qwen3-1.7B / 0.6B、Qwen3.5-27B / 9B 等主要支持 SFT（全参 + 高效）与 DPO（全参 + 高效），部分支持 CPT。
- Qwen3.6-Flash-2026-04-16、Qwen3.5-Flash-2026-02-23 等 Flash 系列仅支持 SFT 全参训练。

### 视觉理解（Qwen-VL 系列）

包括 Qwen3-VL-8B-Instruct / Thinking / 4B-Instruct、Qwen2.5-VL-72B / 32B / 7B-Instruct 等。支持 SFT 全参与高效训练，暂不支持 CPT 与 DPO。训练数据支持文本、图像、视频（视频文件路径模式或图片帧列表模式，仅 qwen3.5 及以后的 VL 模型支持视频输入）。

### 语音合成（CosyVoice）

支持对 `cosyvoice-v3-flash` 进行 SFT 高效微调（`efficient_sft`），用于同一发音人的高还原度专属音色定制，面向品牌 IP 形象、长篇有声书、播客、纪录片解说等场景。调优产物是独立部署的新模型，调用时 `voice` 参数必须固定为 `default`，不再提供声音复刻或声音设计能力。语种支持、SSML / LaTeX 请求级控制等能力由基础模型决定，调优无法扩展。当前仅支持通过 API（HTTP）发起，控制台暂不支持；仅对华北 2（北京）地域可用。

### 视频生成（万相 Wan 系列）

- 图生视频-基于首帧：`wan2.5-i2v-preview`、`wan2.2-i2v-flash`
- 图生视频-基于首尾帧：`wan2.2-kf2v-flash`

通过 SFT-LoRA 训练特定动作、特效或风格的 LoRA 模型，微调后无需提示词即可稳定复现训练集中的视觉效果（如"金钱雨"、"时尚杂志"特效）。

### 图像生成（万相 Wan 系列）

支持 `wan2.7-image-pro` 的文生图与图生图 SFT-LoRA 微调，用于固定特定人物形象、艺术风格（如"末日废土红黑机甲"）或画面效果。

## 入口方式

### 控制台

百炼控制台提供可视化的零代码调优界面，适合初次接触模型调优的用户。典型流程为：在"模型调优"页面创建训练任务 → 选择基础模型与训练方式（推荐 SFT + 高效训练）→ 上传训练集 → 配置超参（保持百炼推荐默认值即可）→ 配置 Checkpoint 保存参数 → 开始训练 → 导出参数快照 → 在"模型部署"页面部署自定义模型 → 在"模型评测"页面评估训练效果。

### API 与命令行

通过 DashScope HTTP API 与 Shell 命令行可编程化完成调优全流程，前提已开通服务并获得 API-KEY，子账号需被授予调用、训练和部署权限：

1. **上传训练文件**：`POST /api/v1/files`，`purpose=fine-tune`。单文件最大 300MB，总配额 5GB / 100 个文件，文件存储无时间限制。
2. **创建调优任务**：`POST /api/v1/fine-tunes`，指定 `model`（基础模型 ID 或其他调优任务产出的模型 ID）、`training_file_ids`、`training_type`（`cpt` / `sft` / `efficient_sft` / `dpo_full` / `dpo_lora`）以及 `hyper_parameters`。
3. **查询任务**：`GET /api/v1/fine-tunes/<job_id>`，任务状态包含 `PENDING` / `QUEUING` / `RUNNING` / `CANCELING` / `SUCCEEDED` / `FAILED` / `CANCELED`。训练成功后 `finetuned_output` 字段即为调优产出的模型 ID，可用于部署。
4. **查询与发布快照**：仅 SFT 微调训练（`efficient_sft` / `sft`）支持中间 Checkpoint 的保存与发布。发布任务异步执行，需通过快照列表 API 观察发布状态（`PENDING` / `PROCESSING` / `SUCCEEDED` / `FAILED`）。
5. **部署与调用**：通过 `POST /api/v1/deployments` 部署，部署状态为 `RUNNING` 后即可像调用其他模型一样使用。支持按 Token 用量（`plan=lora`）或按模型单元使用时长（`plan=mu`）两种计费方式。

通过 API 创建的任务仅支持按 Token 计费；如需使用模型训练单元（预付费 / 后付费），请通过控制台创建。

## 数据格式

训练数据统一采用 JSONL 格式，每行一个 JSON 对象。

- **SFT**：ChatML（Chat Markup Language）格式，支持多轮对话与 system / user / assistant 多角色。所有 assistant 输出都会被训练（不支持 OpenAI 的 `name`、`weight` 参数）。思考模型（Thinking）需用 `<think>` 标签包裹思考内容，且只能出现在最后一条 assistant 输出中，标签前后的换行符必须保留。
- **DPO**：在 SFT 基础上增加 `chosen`（赞同回答）和 `rejected`（反对回答）两个字段，模型将 `messages` 内所有内容作为输入，对最后一条用户输入的正负反馈进行训练。深度思考内容同样需用 `<think>` 标签包裹。
- **CPT**：纯文本格式 `{"text":"文本内容"}`。
- **VL 多模态**：content 使用数组形式 `[{"text":"..."}, {"image":"...jpg"}, {"video":"...mp4"}]`，如需传入 `system` 消息则 `content` 必须使用数组格式。视频训练素材需打包为 ZIP（最大 2GB，文件名仅支持 ASCII 字母、数字、下划线、连字符；`data.jsonl` 必须位于根目录；图片单张宽高不超 1024px、单张不超 10MB，支持 `.bmp` / `.jpeg` / `.jpg` / `.png` / `.tif` / `.tiff` / `.webp`）。

每条 assistant 或 chosen 输出支持 `loss_weight`（0.0 ~ 1.0，数值越大重要性越高）参数控制该行在训练中的相对重要性（邀测参数，需联系商务经理开通）。

## 数据集构建建议

- **规模**：CPT 至少 5000 万 Token 优质预训练数据；SFT 至少 1000 条优质调优数据；DPO 至少 100 组人类偏好数据。数据不足时，最简单的改进方法是收集更多数据。也可借助更大规模的大模型模拟生成辅助样本，或使用百炼的"数据处理"功能进行清洗与增强。
- **多样性与均衡性**：训练效果不仅取决于数据量，更取决于针对场景的专业性与多样性。各场景 / 业务的数据数量应相对均衡、比例符合实际场景分布，避免单一类型占比过高导致模型泛化能力下降。
- **验证集拆分**：控制台支持自动切分（默认 80/20，验证集最多 1000 条）或独立上传验证集。
- **与 RAG 结合**：缺少数据时建议先构建 RAG 应用，在收集到足够应用数据后再通过调优继续提升。典型做法是用调优解决语气、表达习惯、自我认知等问题，用知识库动态引入专业知识。

## 计费

按训练数据 Token 数量计费：`训练费用 = (训练数据 Token 总数 + 混合训练数据 Token 总数) × 循环次数 × 训练单价`，最小计费单位为 1 Token。不同基础模型单价不同，例如：

- Qwen3-8B：¥0.006 / 千 Token
- Qwen3-14B / 30B-A3B-Instruct-2507：¥0.03 / 千 Token
- Qwen3-32B：¥0.04 / 千 Token
- Qwen3.5-9B：¥0.02 / 千 Token
- Qwen2.5-72B-Instruct、千问-Plus-Character-2025-11-06：¥0.15 / 千 Token
- Qwen3-VL-8B-Instruct / Thinking：¥0.012 / 千 Token
- Qwen2.5-VL-72B-Instruct：¥0.05 / 千 Token

控制台创建任务时可在底部查看预估训练费用及计算详情。训练后的自定义模型需部署后才能使用，模型部署按 Token 用量或模型单元另行计费。

## 超参数要点

创建调优任务时影响训练费用与效果的关键超参数：

- **必填**：`n_epochs`（循环次数，数据量 < 1 万条建议 3-5 次，> 1 万条建议 1-2 次）、`batch_size`（批次大小）、`max_length`（单条数据 Token 上限，超过则直接丢弃该条，推荐 8192）。
- **学习率（`learning_rate`）**：百炼提供推荐默认值，通常无需手动调整。过高会导致模型参数剧烈变化、效果变差，过低则收敛不明显。
- **学习率调度策略（`lr_scheduler_type`）**：推荐 `linear` 或 `Inverse_sqrt`；`Constant` 策略下 `warmup_ratio` 无效。
- **预热比例（`warmup_ratio`）**：学习率由小值线性递增至设定值的比例，限制初始阶段参数变化幅度。比例过大等效于过低学习率，过小等效于过高学习率。
- **混合训练**：`data_augmentation=true` 时将训练数据与百炼通用数据集（多领域 / 多行业 / 多场景）混合，可提升效果并避免能力退化。混合数据计入总训练 Token 按标准计费。`augmentation_types` 可选中文 / 英文对话、数学、代码、通用、NLP 等类型，需与 `augmentation_ratio` 一一对应（范围 0.0 ~ 2.0）。千问 2 系列、千问 3 系列、千问 3 VL 系列各有对应的预置数据集。
- **LoRA 专属**：`lora_rank`（推荐 64，越大效果越好但训练越慢）、`lora_alpha`（控制原模型权重与 LoRA 修正项的缩放系数）、`lora_dropout`（增强通用化能力，过大会导致效果不明显）。
- **视觉模型**：`freeze_vit=true` 可冻结视觉主干网络参数，且只有冻结后才能按 Token 用量计费部署。
- **快照保存**：`save_strategy`（`epoch` 或 `steps`）、`save_steps`（建议为 `eval_steps` 的整数倍）、`save_total_limit`（默认 10）。

## 安全合规强化

通用大语言模型在开放域对话中可能生成不符合中国法律法规或主流价值观的内容，仅依赖 Prompt 工程或后处理过滤难以从根本上解决模型的"内在倾向"问题。通过 SFT 微调可将安全对齐目标直接写入模型参数，使模型在面对敏感或诱导性请求时主动拒绝并给出正面引导。典型做法是以 Qwen3-8B 等模型为基础，构造覆盖政治安全、历史认知、社会伦理、网络安全、心理健康、金融安全、青少年保护、公共安全等多维度安全风险的高质量指令数据集，通过百炼控制台的零代码 SFT 微调能力完成训练，再部署为在线 API 服务，并通过独立的 LLM 安全性评估分类器量化微调效果。

## 调优前的替代方案

模型调优成本高（数据集构建、训练、部署）、迭代慢（需重新收集数据、清洗、发起调研），百炼推荐在考虑调优前优先尝试：

1. **Prompt 工程（Prompt Engineering）**：通过改进提示词技巧提升效果，迭代更敏捷、成本更低。
2. **插件调用（Function Calling）**：为模型接入外部工具或 API，扩展能力边界。
3. **知识库 RAG**：通过智能体应用的知识库索引增强模型在特定领域的表现。

许多任务中，模型最初可能表现不佳，但通过应用正确的 Prompt 技巧即可改进，不一定需要调优。即使最终一定要进行调优，前期的 Prompt 工程与插件优化工作也不会浪费，其产出可直接复用为调优数据集的输入。

## 典型场景示例

- **角色扮演**：基于 SFT 训练具有特定语气、自我认知的客服 / 虚拟人角色模型。
- **目标检测**：基于 Qwen-VL 训练特定领域的视觉识别模型。
- **专属音色**：基于 CosyVoice 为品牌 IP 训练高还原度的单音色合成模型，用于有声书、播客、课件等长篇稳定生产。
- **视频特效**：基于万相训练"金钱雨"、"时尚杂志"等特定动作 / 风格 LoRA，微调后无需提示词即可稳定复现视频特效。
- **图像风格**：基于万相训练特定人物形象或艺术风格 LoRA，实现一致的角色 / 风格输出（文生图 / 图生图）。
- **安全合规**：对大模型进行安全对齐训练，使其主动拒绝高危请求并提供正面引导。
- **Agent 工具调用**：通过 SFT 训练模型遵循 MCP 等工具调用范式。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)


