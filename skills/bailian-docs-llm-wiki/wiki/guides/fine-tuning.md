# fine tuning

模型微调（Fine-tuning）是当 Prompt 工程、插件调用等方法仍无法满足需求时，通过训练直接修改模型参数以提升特定行业/业务表现的核心手段。百炼平台的调优能力覆盖文本生成、视觉理解、图像/视频生成与语音合成等多种模态，支持 SFT、CPT、DPO 等训练方式，并可通过控制台或 API 发起。所有调优功能**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key。

## 支持的模型与训练方式

不同模态支持的模型和训练方式差异较大：

- **文本生成（千问系列）**：支持 CPT（继续预训练）、SFT（监督微调）、DPO（直接偏好优化），并区分全参训练与高效训练（LoRA）。可训练模型包括 qwen3.5 系列、qwen3 系列、qwen2.5 系列等，详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md) 的支持模型表。
- **视觉理解（千问 VL）**：qwen3-vl、qwen2.5-vl 系列，仅支持 SFT（全参/高效），不支持 CPT/DPO。
- **图像生成**：wan2.7-image-pro、wan2.7-image，仅支持 SFT-LoRA 高效微调，覆盖文生图（t2i）与图生图（i2i），见 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成**：图生视频-基于首帧（wan2.5-i2v-preview、wan2.2-i2v-flash）、图生视频-基于首尾帧（wan2.2-kf2v-flash），同样为 SFT-LoRA，见 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成**：cosyvoice-v3-flash，仅支持 `efficient_sft`，且**仅能通过 API 发起，控制台暂不支持**，见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 调优方式选型（CPT / SFT / DPO）

三种方式并不互斥，而是递进关系：`CPT（可选）→ SFT → DPO（可选）`。

| 方式 | 一句话 | 输入数据 | 典型用途 |
| --- | --- | --- | --- |
| CPT（继续预训练） | 补知识 | 1000 万+ Token 无标签领域文本 | 注入专业词汇、事实 |
| SFT（监督微调） | 学做事 | 1000+ 条高质量问答对 | 学会指令遵循、任务执行 |
| DPO（直接偏好优化） | 做得更好 | 100+ 组「更好-更差」回答对 | 对齐人类偏好、抑制幻觉 |

训练模式方面，官方推荐**若模型支持全参训练则优先选择全参训练**（效果更好且与高效训练计费相同）；对训练时间/成本敏感或数据集较小时选择高效训练（LoRA）。详见 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 数据集格式

- **SFT**：ChatML 格式（`messages` 数组，含 system/user/assistant），支持多轮对话；思考模型（thinking）只训练最后一个 assistant 输出，且 `<think>` 标签前后的 `\n` 必须保留。
- **DPO**：在 `messages` 基础上额外提供 `chosen` 与 `rejected` 两个 assistant 输出。
- **CPT**：纯文本格式 `{"text":"文本内容"}`。
- **视觉理解（VL）**：ChatML 中 content 用数组格式，可含 `image`/`video` 字段；训练数据打包为 ZIP，`data.jsonl` 必须位于根目录，单张图片尺寸不超过 1024px。
- **图像/视频生成**：训练集打包为 `.zip` 上传，或通过 OSS 挂载方式加载（OSS 方式不支持 zip，需上传未压缩文件夹）。
- **语音合成（CosyVoice）**：目录含 `data.jsonl` 与 `train/` 音频目录，`wav_fn` 必须以 `train/` 为前缀；音频为 `.wav`、采样率不低于 16 kHz，推荐单条 2~30 秒，训练数据须为**同一发音人**。

> **注意**：SFT 与 DPO 对超长数据的处理不同——SFT 会直接**丢弃**超过 `max_length` 的数据，DPO 则**自动截断**后续 token 并仍参与训练。

## 关键超参数

文本调优的核心超参（见 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)）：

- **learning_rate**：高效训练 1e-4 量级，全参训练与 CPT 为 1e-5 量级。
- **n_epochs**：数据量 < 10000 循环 3~5 次；> 10000 循环 1~2 次；取值范围 [1, 200]。
- **max_length**：建议设为模型支持的最大值，取值范围 [500, 32768]。
- **lora_rank**（高效训练）：建议设为模型支持的最大值，秩越大效果越好但训练略慢。
- **lr_scheduler_type**：推荐 `linear` 或 `Inverse_sqrt`。

通过 API 创建任务时，`n_epochs`、`batch_size`、`max_length` 为**影响计费的必填项**；`training_type` 可选 `cpt` / `sft` / `efficient_sft` / `dpo_full` / `dpo_lora`。

CosyVoice 则使用独立的 LM/FM 双网络超参（`lm_*` / `fm_*`），推荐值 `lm_max_epoch=60`、`fm_max_epoch=100`；文档给出的最小化超参（如 `lm_max_epoch=4`）仅用于跑通流程，不可用于生产。

## 使用方式

模型调优可通过**控制台**（可视化零代码，见 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)）或 **API/命令行**（DashScope HTTP 接口，见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)）发起。API 流程通用为四步：

1. **上传数据集**：`POST /api/v1/files`（`purpose=fine-tune`），返回 `file_id`。
2. **创建调优任务**：`POST /api/v1/fine-tunes`，返回 `job_id`、`finetuned_output`、`status`（初始 `PENDING`）。
3. **查询任务状态**：轮询 `GET /api/v1/fine-tunes/<job_id>`，直到 `status` 变为 `SUCCEEDED`。
4. **部署并调用**：`POST /api/v1/deployments` 部署，轮询直到 `status` 为 `RUNNING`，再用返回的 `deployed_model` 调用。

调优后模型的调用参数与对应基础模型的 API 基本一致。对于图像/视频 LoRA 模型，提示词中建议携带触发词（如 `s86b5p`）以激活训练风格，调用视频模型时建议关闭 `prompt_extend`。

## 限制与注意事项

- **地域限制**：所有调优功能仅在华北2（北京）可用，须使用该地域 API Key；OSS 挂载 Bucket 仅支持北京（cn-beijing）和新加坡（ap-southeast-1）。
- **权限**：RAM 子账号需被授予模型调用、训练和部署权限。
- **文件配额**（文本调优）：单文件最大 300MB，有效文件总空间 5GB、总数量 100 个。
- **计费**：文本/视频/图像调优按训练 Token 计费；CosyVoice 训练按 0.2 元/千 Tokens、部署按模型单元时长计费。

> **注意**：通过 API 创建的训练任务仅支持按 Token 计费，暂不支持模型训练单元（预付费/后付费）；如需使用训练单元，必须通过控制台创建任务。

> **注意**：CosyVoice 调优产物是单音色独立模型，调用时 `voice` 必须固定为 `default`、不支持 `instruction` 指令控制，且**无法扩展基础模型不支持的语种**。若仅需单条音频克隆或文字描述生成音色，应优先使用声音复刻/声音设计而非调优。

> **注意**：训练轮次并非越高越好——轮次过高会加剧基础模型原有能力的「遗忘」（长文本稳定性、多音字准确率退化），并可能导致过拟合。可通过观察 Training Loss / Validation Loss 曲线判断欠拟合、过拟合还是良好拟合，从而决定是否调整 `n_epochs` 与 `lora_rank`。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


