# fine tuning

百炼平台提供模型调优（fine tuning）能力，支持对文本生成、视觉理解、图像生成、视频生成、语音合成等多类模型进行训练，将业务/场景知识直接写入模型参数，从而在 Prompt 工程之外进一步压低延迟、抑制幻觉、对齐人类偏好并复刻特定风格。调优方式涵盖继续预训练（CPT）、监督微调（SFT）、直接偏好优化（DPO）三种，并细分为全参训练与 LoRA 高效训练两种模式。

## 调优方式与适用场景

百炼提供的三种调优方式互不互斥，而是递进相辅的关系：`CPT（可选）→ SFT → DPO（可选）`。

| 方式 | 一句话定位 | 输入数据 | 核心目标 |
| --- | --- | --- | --- |
| CPT（继续预训练） | 补知识 / 注入领域知识 | 1000 万+ [Token](../concepts/token.md) 无标签领域文本 | 领域适应，学习专业词汇与事实 |
| SFT（监督微调） | 学做事 / 遵循指令 | 1000+ 条高质量问-答对 | 教会模型对话格式与任务执行 |
| DPO（直接偏好优化） | 做得更好 / 对齐人类偏好 | 100+ 组同指令下的更好-更差回答对 | 增大好答案概率、降低坏答案概率 |

训练模式上分**全参训练**与**高效训练（LoRA，推荐）**：前者追求全局效果最优但耗时长、收敛慢；后者只训练部分参数，速度快、成本低，适合快速验证或数据集较小的场景，详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持的模型与能力

### 文本生成与视觉理解（千问系列）

文本生成支持 Qwen3.x、Qwen2.5 系列（如 qwen3-32b、qwen3-8b、qwen2.5-72b-instruct 等）以及千问-Plus-Character，覆盖 CPT、SFT（全参/高效）、DPO（全参/LoRA）多种组合；视觉理解支持 Qwen3-VL、Qwen2.5-VL 系列（如 qwen3-vl-8b-instruct、qwen2.5-vl-72b-instruct 等），但仅支持 SFT（全参/高效）。不同模型对 CPT/SFT/DPO 的支持矩阵不同，使用前请按 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md) 中的支持表核对。

> **注意**：`-Base` 后缀的模型只完成预训练，无法正常对话，不直接用于调优对话场景。

### 图像生成（万相 wan2.7）

- 支持微调方式：SFT-LoRA 高效微调（`efficient_sft`）。
- 支持模型：`wan2.7-image-pro`、`wan2.7-image`。
- 适用场景：文生图（t2i）训练人物/IP 角色 LoRA；图生图（i2i）训练特定风格（如"末日废土红黑机甲"）LoRA，输入参考图像无需提示词即可复现风格。
- 调用微调后的 LoRA 模型时，输入参数与万相图像生成与编辑 2.7 API 保持一致；建议在提示词中包含触发词（如 `s86b5p`）以激活 LoRA 风格。

### 视频生成（万相 wan2.2/wan2.5）

- 支持微调方式：SFT-LoRA 高效微调。
- 支持模型：图生视频-基于首帧 `wan2.5-i2v-preview`、`wan2.2-i2v-flash`；图生视频-基于首尾帧 `wan2.2-kf2v-flash`。
- 部署时通过 `aigc_config` 预置提示词模板与 `lora_prompt_default`，调用时通常关闭 `prompt_extend` 并按模型类型选择分辨率（480P/720P）。

### 语音合成（CosyVoice）

- 支持调优方式：SFT 高效微调（`efficient_sft`），暂不支持 CPT/DPO。
- 支持模型：`cosyvoice-v3-flash`。
- 适用场景：同一发音人有多条/数小时录音，单条声音复刻还原度不足时，训练独立部署的专属音色模型。调优产物为单音色模型，调用时 `voice` 必须固定为 `default`，详见 [CosyVoice 模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

> **注意**：CosyVoice 调优**仅支持通过 API（HTTP）发起，控制台暂不支持**；且无法通过调优扩展基础模型不支持的语种。

## 关键参数

文本类调优任务的关键超参数（不同模型默认值不同，请在控制台核对）：

- `n_epochs`：训练循环次数，与训练深度正相关。
- `batch_size`：批次大小。
- `max_length`：序列长度。**以上三项直接影响训练费用，必须填写。**
- `learning_rate` / `lr_scheduler_type`：学习率与调度策略（如 `linear`、`cosine`）。
- `split`：训练/验证集自动切分比例（如 0.9 表示 90% 训练、10% 验证）。
- `eval_steps` / `eval_epochs`：评估步数/轮次。
- `save_total_limit` / `save_strategy`：Checkpoint 保留数量与保存策略。
- `lora_rank` / `lora_alpha`：LoRA 低秩矩阵的秩与缩放，秩越大表达能力越强但更易过拟合。

万相图像/视频微调还涉及 `max_pixels`、`generation_type`（t2i/i2i）、`val_img_size` 等视觉相关超参；CosyVoice 调优的费用估算公式为：`消耗 Tokens = (lm_max_epoch + fm_max_epoch) × 25 × 训练集总时长(秒)`。

## 使用方式

### 控制台方式（零代码）

适合初学者或安全合规等零代码场景：在百炼控制台「模型调优」页面创建训练任务，选择调优方式（CPT/SFT/DPO）、基础模型、训练模式（全参/高效 LoRA）、训练集与验证集，配置超参后开始训练，详见 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。任务优先级分 L0–L3 四级，优先级越高越早被调度。

### API / 命令行方式

通过 DashScope API 完成「上传数据集 → 创建调优任务 → 查询状态 → 部署 → 调用」全流程，详见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。核心接口：

1. **上传文件**：`POST /api/v1/files`，获取 `file_id`。
2. **创建调优任务**：`POST /api/v1/fine-tunes`，传入 `model`、`training_file_ids`、`training_type`（`cpt`/`sft`/`efficient_sft`/`dpo_full`/`dpo_lora`）与 `hyper_parameters`，返回 `job_id`、`finetuned_output`、`status`（初始为 `PENDING`）。
3. **查询任务状态**：`GET /api/v1/fine-tunes/{job_id}`，轮询直到 `status` 变为 `SUCCEEDED`。
4. **部署模型**：`POST /api/v1/deployments`，将 `finetuned_output` 部署为在线服务，轮询 `GET /api/v1/deployments/{deployed_model}` 直到 `status` 变为 `RUNNING`。
5. **调用模型**：使用 `deployed_model` 名称像调用基础模型一样发起请求。

> **注意**：通过 API 创建的训练任务**仅支持按 [Token](../concepts/token.md) 计费，暂不支持使用模型训练单元（预付费或后付费）**；如需使用训练单元，请通过控制台创建任务。

### 万相图像/视频微调的统一流程

图像与视频生成模型的微调流程与文本类一致，但数据集格式与部署参数不同：

- **数据集**：打包为 `.zip`，内含 `data.jsonl`（标注文件）与训练图像/视频；文生图需训练目标图像与 [prompt](prompt.md)，图生图还需参考输入图像；图生视频基于首帧或首尾帧组织样本。
- **部署**：万相视频模型部署时需在 `aigc_config` 中配置 `use_input_prompt`、`prompt`（预置模板）与 `lora_prompt_default`，以在推理时自动激活 LoRA 特效。
- **调用**：图像生成走 `image-generation/generation` 异步接口，视频生成走 `video-synthesis` 异步接口，均通过 `task_id` 轮询结果（图像 URL 有效期 24 小时）。

## 数据集格式

- **SFT（文本）**：ChatML 格式 `.jsonl`，每行一个 `{"messages":[...]}` 对象，支持多轮对话；不支持 OpenAI 的 `name`、`weight` 参数，所有 assistant 输出都会被训练；`loss_weight`（0.0~1.0）为邀测参数。
- **SFT 思考模型（thinking）**：只能针对**最后**的 assistant 输出训练，思考内容用 `<think>...</think>` 包裹，思考标签前后的 `\n` 必须保留。
- **SFT 视觉理解（千问 VL）**：`content` 必须用数组格式（如 `[{"text":"..."}]`），system 消息的 `content` 不能用字符串；图像/视频以文件名引用，文件名需全局唯一、平铺结构。
- **DPO**：在 `messages` 之外提供 `chosen` 与 `rejected` 的 assistant 回答，深度思考内容同样用 `<think>` 标签包裹。
- **CPT**：纯文本格式，每行 `{"text":"文本内容"}`。
- **CosyVoice**：`data.jsonl` 每行 `{"wav_fn":"train/xxx.wav","text":"..."}`，音频为 `.wav`、采样率 ≥16 kHz、单条 1–30 秒，训练数据须为同一发音人。

## 计费说明

文本/视觉模型按训练数据量计费：`训练费用 = (训练数据 Token 总数 + 混合训练数据 Token 总数) × 循环次数 × 训练单价`，最小计费单位为 1 [Token](../concepts/token.md)。预置模型训练单价随规模变化，例如 qwen3-8b 为 ¥0.006/千 Token、qwen2.5-72b-instruct 为 ¥0.15/千 Token，自定义模型单价与对应预置模型相同。视觉模型的图像/视频 Token 按像素与抽帧数估算。

万相图像/视频微调按训练消耗的 Token 计费（响应 `usage` 字段）；CosyVoice 训练单价为 0.2 元/千 Tokens，部署费用按模型单元使用时长计费。

## 限制与注意事项

- **地域限制**：所有调优功能**仅适用于华北2（北京）地域**，必须使用该地域的 [API Key](../concepts/api-key.md)；万相图像/视频微调同样仅在该地域可用。
- **权限要求**：使用 RAM 子账号需授予模型调用、训练和部署权限。
- **文件限制**：单个文件最大 300MB，有效文件总配额 5GB / 100 个，文件存储无时间限制。
- **训练耗时参考**：万相文生图约 77 分钟、图生图约 110 分钟（2K、300 步）；万相视频微调需数小时；CosyVoice 高效训练约 15–30 分钟；模型部署通常 3–10 分钟。
- **安全合规**：如需让模型主动拒绝敏感/诱导性请求，可通过零代码 SFT 微调（如基于 Qwen3-8B）将安全对齐目标写入模型参数，覆盖政治、历史、社会、网络安全等多维度，详见 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。训练前应观察 Training Loss 与 Validation Loss 曲线判断欠拟合/过拟合，并相应调整 `n_epochs` 与 `lora_rank`。
- **CosyVoice 能力边界**：调优产物为单音色独立模型，不再提供声音复刻、声音设计、指令控制能力；语种支持由基础模型决定，无法通过调优扩展；训练音频中的语速、情感、错读等统计特性会直接反映到调优产物的默认合成风格上。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


