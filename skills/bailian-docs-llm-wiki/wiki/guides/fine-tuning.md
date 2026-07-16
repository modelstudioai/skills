# fine tuning

模型微调（Fine-tuning）是阿里云百炼在 Prompt 工程、插件调用等手段仍无法满足效果时提供的深度定制手段。它覆盖文本生成、视觉理解（Qwen-VL）、图像/视频生成（万相）以及语音合成（CosyVoice）等多种模态，通过 SFT、CPT、DPO 等训练方式，把领域知识、任务能力、人类偏好或特定音色/风格直接写入模型参数。

> **注意**：以下所有微调、部署与调用能力均**仅在华北2（北京）地域可用**，且必须使用该地域的 API Key；子账号（RAM 用户）需预先被授予调用、训练和部署权限。

## 支持的模型与训练方式

按模态划分，不同模型支持的训练方式差异明显：

- **文本生成（千问系列）**：支持 CPT、SFT（全参 `sft` / 高效 `efficient_sft`）、DPO（全参 `dpo_full` / 高效 `dpo_lora`）。是否支持某种方式因模型而异，例如 Qwen3-32B、Qwen3-4B/1.7B/0.6B、Qwen2.5 系列支持全部 5 种；而 Qwen3.5-Plus/Flash、Qwen3.6/3.7 等新模型往往仅支持 `sft`。详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **视觉理解（千问 VL）**：Qwen3-VL、Qwen2.5-VL 系列支持 SFT 全参与高效训练，不支持 CPT/DPO。
- **图像生成（万相）**：`wan2.7-image-pro`、`wan2.7-image`，仅支持 SFT-LoRA 高效微调，见 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。
- **视频生成（万相）**：图生视频-基于首帧 `wan2.7-i2v`/`wan2.5-i2v-preview`/`wan2.2-i2v-flash`，基于首尾帧 `wan2.2-kf2v-flash`，同样仅支持 SFT-LoRA，见 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。
- **语音合成（CosyVoice）**：`cosyvoice-v3-flash`，仅支持 `efficient_sft`，且**当前只能通过 API 发起，控制台暂不支持**，见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 三种调优方式（文本生成）

推荐按递进顺序组合使用：`CPT（可选）→ SFT → DPO（可选）`。

| 方式 | 目标 | 数据量 | 数据形态 |
| --- | --- | --- | --- |
| CPT（持续预训练） | 补领域知识 | 1000 万+ Token | 无标签领域文本 `{"text":"..."}` |
| SFT（监督微调） | 学会遵循指令 | 1000+ 条 | ChatML「问-答」对 |
| DPO（直接偏好优化） | 对齐人类偏好 | 100+ 组 | 同指令下「更好/更差」回答对（`chosen`/`rejected`） |

训练模式分**全参训练**与**高效训练（LoRA）**：两者费用相同，官方建议在模型支持全参训练时优先选择全参（效果更好、性价比更高）；LoRA 适合对训练时间/成本敏感或数据集较小的场景。

## 关键超参数

文本生成调优的常用超参及默认值（以控制台实际显示为准）：

- `learning_rate`：高效训练建议 `1e-4` 量级，全参/CPT 建议 `1e-5` 量级。
- `n_epochs`：默认 `3`，范围 `[1, 200]`；数据量 <10000 建议循环 3~5 次，>10000 建议 1~2 次。
- `batch_size`：一般 16/32。
- `max_length`：建议设为模型支持的最大值；SFT 会**丢弃**超长数据，DPO 则**截断**后仍训练。
- `lora_rank` / `lora_alpha` / `lora_dropout`：LoRA 专用，秩越大效果略好但更慢、更易过拟合。
- 通过 API 创建任务时，`n_epochs`、`batch_size`、`max_length` 因影响计费而**必填**。

> **注意**：默认学习率各文档取值不一致。控制台参数面板列出的 `learning_rate` 默认值为 `3e-4`（对应高效训练默认场景），而 API 示例中 SFT 全参使用的是 `1.6e-5`。请以实际训练方式对应的量级为准，切勿照搬。

万相图像/视频与 CosyVoice 使用各自独立的超参集，例如万相有 `max_steps`/`generation_type`/`val_img_size`，CosyVoice 分 `lm_*`（影响韵律）与 `fm_*`（影响音色）两组网络的 `*_max_epoch`/`*_step`/`*_num`/`*_batch_size`（8 个子字段全部必填）。

## 使用方式

**控制台（推荐入门）**：在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面创建训练任务 → 选训练方式与模型 → 配置训练集/验证集（可自动切分）→ 配置 Checkpoint 保存 → 开始训练 → 部署 → 评测。零代码场景可参考 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)，其中给出了以 Qwen3-8B 为例的完整安全对齐 SFT 流程与超参实验对照（全参 `n_epochs=3`/`lr=1e-5` 或 LoRA `n_epochs=3`/`lr=3e-4` 效果较好）。

**API / 命令行**：统一四步流程，详见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)：

1. 上传数据集到 `POST /api/v1/files`（`purpose=fine-tune`），获取 `file_id`。
2. `POST /api/v1/fine-tunes` 创建任务，关注返回的 `job_id`、`finetuned_output`、`status`。
3. 轮询 `GET /api/v1/fine-tunes/<job_id>` 直到 `status` 变为 `SUCCEEDED`。
4. `POST /api/v1/deployments` 部署（`plan=lora`），轮询直到 `status` 为 `RUNNING`，再用 `deployed_model` 调用。

> **注意**：通过 API 创建的训练任务**仅支持按 Token 计费**，不支持模型训练单元（预付费/后付费）；如需使用训练单元，必须通过控制台创建。

数据集除 `file_id` 外还可用 OSS 挂载（`data_source_type=oss_mount`），OSS Bucket 地域支持 `cn-beijing` 与 `ap-southeast-1`，挂载时只需指定 `data.jsonl` 路径。

## 数据格式要点

- **SFT**：ChatML `{"messages":[...]}`，支持多轮；不支持 OpenAI 的 `name`/`weight`，所有 assistant 行都会被训练；思考模型（thinking）只训练**最后**一个 assistant 输出且须保留 `<think>` 标签前后的换行。
- **DPO**：在 `messages` 基础上追加 `chosen`/`rejected`。
- **CPT**：纯文本 `{"text":"..."}`。
- **视觉理解**：`content` 用数组，`image`/`video` 声明文件名（不含路径），打包为 ZIP（≤2GB），`data.jsonl` 必须在根目录，文件名全局唯一且仅含 ASCII。
- **CosyVoice**：`data.jsonl` 每行 `{"wav_fn":"train/xxx.wav","text":"..."}`，`wav_fn` 必须以 `train/` 前缀；`text` 须为纯文本，禁止 SSML/LaTeX/情感标注。

## 限制与注意事项

- **成本与耗时高**：文本模型微调需构建大规模数据集，且调优后模型**必须部署才能使用**，部署费用较高；官方明确将模型调优定位为「最后的手段」，建议先充分尝试 Prompt 工程与插件调用。
- **训练耗时差异大**：万相文生图约数十分钟，视频微调可达数小时；文本 LoRA 通常 15~30 分钟；部署一般需 3~10 分钟。
- **计费方式各异**：文本/VL 按训练 Token 计费（`训练Token × 循环次数 × 单价`）；CosyVoice 按 `(lm_max_epoch+fm_max_epoch)×25×音频总秒数` 估算 Token，单价 0.2 元/千 Token，另加部署时长费用。
- **能力边界不可突破**：CosyVoice 调优产物为单音色模型（`voice` 锁定 `default`），无法新增基础模型不支持的语种、也不支持 `instruction` 指令控制。
- **过拟合/欠拟合判断**：观察 Training/Validation Loss 曲线，欠拟合可增大 `n_epochs`/`lora_rank`，过拟合则反向调整。
- 万相 LoRA 调用需在提示词中包含**触发词**以激活风格；图像模型部署后当前仅支持异步调用。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)



