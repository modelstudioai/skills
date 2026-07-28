# fine tuning

模型微调（fine tuning）是阿里云百炼平台在 Prompt 工程等手段无法满足需求时的核心模型优化方式，覆盖文本生成、视觉理解、图像/视频生成、语音合成等多种模态。平台提供 CPT（继续预训练）、SFT（监督微调，含 LoRA 高效训练）、DPO（直接偏好优化）以及 RL（强化学习）等训练方式，统一走"上传数据集 → 创建训练任务 → 部署 → 调用"的流程，支持控制台零代码操作和 DashScope API/命令行两种入口。

> **注意**：本主题下所有微调能力均仅支持**华北2（北京）**地域，必须使用该地域的 API Key；RAM 子账号需先授予模型调用、训练和部署权限。

## 调优方式与选型

根据 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)，各调优方式是递进而非互斥的，推荐顺序为 `CPT（可选）→ SFT → DPO（可选）→ RL（可选）`：

| 方式 | 一句话定位 | 数据要求 | 典型场景 |
| --- | --- | --- | --- |
| CPT 持续预训练 | 补知识（领域适应） | 1000万+ Token 无标签领域文本，格式 `{"text":"..."}` | 金融术语、医疗病理、法律条文 |
| SFT 监督微调 | 学做事（遵循指令） | 1000+ 条高质量 ChatML 问答对 | 客服流程、代码助手、Agent 工具调用 |
| DPO 直接偏好优化 | 做得更好（对齐偏好） | 100+ 组 chosen/rejected 回答对 | 抑制幻觉、安全对齐、bad case 修复 |
| RL 强化学习 | 学推理（Reward 驱动） | 数十至数百条起步（含 `rollout_extra` 参考答案） | 数学推理、代码生成、Agent 调用稳定性 |

训练模式上分**全参训练**与**高效训练（LoRA）**：两者费用相同，若模型支持全参训练官方建议优先全参（效果更好）；LoRA 训练更快、适合快速验证与小数据集场景。LoRA 关键参数 `lora_rank` 需为 2 的幂（如 16/32/64），秩越大拟合能力越强但更易过拟合。

## 支持的模型

- **文本生成**：Qwen3.7/3.6/3.5 商业版（仅 SFT 全参）、Qwen3 系列（qwen3-32b、qwen3-14b、qwen3-8b 等，多数支持 CPT/SFT/efficient_sft/DPO）、Qwen2.5 系列等，详细支持矩阵与训练单价见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问 VL）**：Qwen3-VL-8B/4B、Qwen2.5-VL-7B/32B/72B 等，支持 SFT 全参与高效训练。
- **图像生成**：wan2.7-image-pro、wan2.7-image（文生图 t2i / 图生图 i2i），仅支持 SFT-LoRA。
- **视频生成**：wan2.7-i2v、wan2.5-i2v-preview、wan2.2-i2v-flash（首帧）、wan2.2-kf2v-flash（首尾帧），仅支持 SFT-LoRA。
- **语音合成**：cosyvoice-v3-flash，仅支持 `efficient_sft`，且仅能通过 API 发起。
- **RL 训练**：qwen3.5-9b、qwen3.6-flash、qwen3.5-flash，需联系商务经理开通。

## 使用方式

### 控制台（零代码）

在控制台"模型调优"页面创建训练任务，选择训练方法（高效/全参）、模型、数据集与超参即可，详见 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。关键超参建议：

- `learning_rate`：高效训练 1e-4 量级，全参/CPT 1e-5 量级
- `n_epochs`：数据量 < 10,000 时循环 3~5 次，> 10,000 时 1~2 次
- `batch_size`：一般建议 16/32，具体范围以控制台显示为准
- 其他默认值：`lora_rank=8`、`lora_alpha=16`、`max_length=8192`、`warmup_ratio=0.05` 等

训练中可通过 Training Loss / Validation Loss 曲线判断拟合状态：双双仍在下降为欠拟合（加 `n_epochs` 或 `lora_rank`），Validation Loss 回升为过拟合（减小两者）。一个端到端的零代码实践（含裁判模型自动评测与超参对照实验）见 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

### API / 命令行

统一走 DashScope 三个接口，详见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)：

1. **上传数据集**：`POST /api/v1/files`，`purpose=fine-tune`，返回 `file_id`；也支持 `oss_mount` 挂载未压缩的数据集目录（OSS Bucket 仅支持 cn-beijing 和 ap-southeast-1）。
2. **创建微调任务**：`POST /api/v1/fine-tunes`，指定 `model`、`training_type`（sft / efficient_sft / cpt / dpo_full / dpo_lora）与 `hyper_parameters`，返回 `job_id` 与 `finetuned_output`（新模型名）；轮询 `GET /api/v1/fine-tunes/{job_id}` 直到 `status=SUCCEEDED`。
3. **部署与调用**：`POST /api/v1/deployments`（LoRA 模型用 `"plan": "lora"`），轮询部署状态至 `RUNNING` 后即可调用。

> **注意**：通过 API 创建的训练任务仅支持按 [Token 计费](../concepts/token-billing.md)，不支持模型训练单元（MTU）；而 RL 训练恰好相反，**仅支持** MTU 计费。需要训练单元时请走控制台创建任务。

### 数据格式要点

- **SFT ChatML**：`{"messages":[{"role":"system"...},{"role":"user"...},{"role":"assistant"...}]}`，所有 assistant 输出都会被训练；不支持 OpenAI 的 `name`/`weight` 参数；`loss_weight` 为邀测参数。
- **SFT 思考模型**：只训练最后一个 assistant 输出，思考内容用 `<think>\n...\n</think>\n\n` 包裹且换行必须保留；若训练成不输出 `<think>`，训练后不建议再开思考模式调用。
- **SFT 视觉理解**：system 消息的 `content` 必须为数组格式；ZIP 包最大 2 GB，`data.jsonl` 必须位于压缩包根目录，图片单张宽高不超过 1024px 且文件名全局唯一。
- **DPO**：在 `messages` 之外提供 `chosen` 与 `rejected` 两个 assistant 回答。
- **CPT**：纯文本 `{"text":"文本内容"}`。

## [多模态](../concepts/multimodal.md)微调

### 图像/视频生成（万相 LoRA）

用于定制特定人物、IP 形象、风格或特效，仅当 Prompt 优化无法满足时使用。流程与文本模型一致（上传 zip 数据集 → fine-tunes → 部署 → [异步调用](../concepts/async-invocation.md)），细节见 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 与 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。要点：

- 图像模型超参以 `max_steps`（建议 ≥ 500）+ `max_token_length` 控制训练量；视频模型以 `n_epochs × ⌈数据集/batch_size⌉` 控制，建议总步数 ≥ 800。
- 视频部署时可通过 `aigc_config`（`prompt` 模板 + `lora_prompt_default`）实现"无提示词自动触发特效"。
- 部署后的图像模型仅支持**[异步调用](../concepts/async-invocation.md)**（`X-DashScope-Async: enable`）。

> **注意**：图像模型创建任务用 `training_datasets` 字段（对象数组，支持 file_id / oss_mount），而视频模型示例用的是 `training_file_ids` 字符串数组，两类接口入参形态不同，编写代码时请以对应文档为准。

### 语音合成（CosyVoice）

面向**同一发音人**多条录音的高还原度音色定制，产出独立部署的单音色模型（调用时 `voice` 固定为 `default`），仅支持 API 发起，见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。关键限制：

- 仅有单条音频、或只想调整朗读风格时，应优先使用声音复刻 / 声音设计 / SSML，而非调优。
- 调优无法扩展基础模型的语种范围；调优产物不支持 `instruction` 指令控制。
- 数据建议：`.wav`、≥16kHz、单条 2~30 秒、总时长 1~10 小时、不少于 150 条；`text` 必须为纯文本（禁止 SSML/LaTeX 标签）。
- 超参分 LM（韵律）与 FM（音色）两组，推荐 `lm_max_epoch=60`、`fm_max_epoch=100`；轮次越高基础能力"遗忘"越严重。
- 训练费 0.2 元/千 Token，估算公式：`(lm_max_epoch + fm_max_epoch) × 25 × 训练集总秒数`；平台同一时刻仅运行一个训练任务，超出的排队（QUEUING）。

### 强化学习（RL）

通过"Rollout 采样 → Reward 评分 → 策略更新"循环提升推理/Agent 能力，无需标注标准答案，见 [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)。使用离线 DashScope SDK（Python ≥ 3.10）提交，需自定义 Rollout / Reward 函数并部署到函数计算（FC），首次使用需在控制台授权 OpenTelemetry、FC、SLS 三项服务。推荐算法 GSPO，核心超参含 `batch_size`、`learning_rate=2e-6`、`n_rollouts` 等；训练中重点观察 `critic/rewards/mean` 指标。

## 计费与限制

- **按 [Token 计费](../concepts/token-billing.md)**：训练费用 =（训练数据 Token + 混合训练数据 Token）× 循环次数 × 训练单价；如 qwen3-8b 为 ¥0.006/千 Token，qwen2.5-72b-instruct 为 ¥0.15/千 Token，完整价目见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **训练单元（MTU）**：预付费包月（IV 型 19,914 元/月/实例）或后付费（41 元/小时/实例）；RL 训练仅支持此方式。
- **文件配额**：单文件最大 300MB（zip 数据集最大 2GB），总空间 100GB，总数 10000 个，无存储时限。
- **部署**：LoRA 产物需以 `plan=lora` 部署为在线服务后才能调用，部署约 5~10 分钟；调优后模型的部署与调用会产生独立的部署费用。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [强化学习训练概述](../../raw/model-user-guide/fine-tuning/rl-training-overview.md)


