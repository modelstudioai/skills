# fine tuning

阿里云百炼平台提供模型微调（Fine-tuning）能力，支持对文本生成、视觉理解、图像生成、视频生成和语音合成等多种模型进行定制化训练。通过微调，开发者可以在特定业务场景下显著提升模型表现、降低输出延迟，或实现风格/音色等深度定制。百炼支持 SFT（监督微调）、CPT（继续预训练）、DPO（直接偏好优化）三种训练方式，涵盖 API 调用和控制台可视化操作两种使用路径。

## 适用模型与调优方式

百炼支持的微调模型覆盖多个模态，不同模型支持的训练方式有所差异：

**文本生成模型**：支持 SFT（全参/高效）、CPT、DPO（全参/高效），覆盖 Qwen3.6、Qwen3.5、Qwen3、Qwen2.5 等系列。详见[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)中的完整模型列表。

**视觉理解模型（千问VL）**：支持 SFT（全参/高效），覆盖 Qwen3-VL、Qwen2.5-VL 等系列，训练数据可包含图片和视频。

**图像生成模型**：支持 SFT-LoRA 高效微调，适用于 wan2.7-image-pro、wan2.7-image 模型，可实现文生图和图生图的风格/IP 定制。详见[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

**视频生成模型**：支持 SFT-LoRA 高效微调，适用于 wan2.5-i2v-preview、wan2.2-i2v-flash、wan2.2-kf2v-flash 模型，可实现基于首帧或首尾帧的视频特效定制。详见[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

**语音合成模型**：支持 SFT 高效微调（`efficient_sft`），适用于 cosyvoice-v3-flash 模型，面向同一发音人多条录音的高还原度音色定制。详见[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## CPT、SFT、DPO 的选择

三种调优方式并不互斥，而是递进关系：`CPT（可选）-> SFT -> DPO（可选）`。

- **CPT（继续预训练）**：通过海量无标记数据补充行业知识，提升模型在特定领域的"知识深度"。适用于金融、医疗、法律等专业领域。
- **SFT（监督微调）**：通过标注好的输入-输出样本教模型"学做事"，提升特定业务表现。适用于客服机器人、代码助手、工具调用等场景。
- **DPO（直接偏好优化）**：通过同时提供正负样本引入偏好反馈，降低幻觉，对 bad case 做针对性优化。适用于安全合规、回答质量提升等场景。

## 通用微调流程

无论哪种模型，微调的核心流程基本一致：

### 1. 准备数据集

不同模型对数据格式有不同要求：

- **文本生成 SFT**：使用 ChatML 格式的 `.jsonl` 文件，每行一条 JSON，包含 `messages` 数组（含 system/user/assistant 角色）。支持多轮对话、思考模型（thinking）格式，以及 `loss_weight` 参数控制样本重要性。
- **视觉理解 SFT**：在 ChatML 格式基础上，`content` 字段使用数组格式以混合文本、图片和视频。需将数据与图片/视频文件打包为 ZIP，`data.jsonl` 位于压缩包根目录。
- **图像/视频生成**：训练集包含目标图像/视频和 `data.jsonl` 标注文件，打包为 ZIP 上传。
- **语音合成**：训练集包含 `.wav` 音频文件和 `data.jsonl`（含 `wav_fn` 和 `text` 字段），打包为 ZIP 上传。推荐训练音频总时长 1~10 小时，不少于 150 条。

### 2. 上传数据集

通过 API 将 ZIP 文件上传到百炼平台，获取 `file_id`：

```bash
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/files' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'files=@"./training-data.zip"' \
--form 'purpose="fine-tune"'
```

### 3. 创建微调任务

使用 `file_id` 启动训练，获取 `job_id` 和 `finetuned_output`（微调后模型名称）：

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "<模型名称>",
    "training_file_ids": ["<file_id>"],
    "training_type": "efficient_sft",
    "hyper_parameters": { ... }
}'
```

### 4. 查询任务状态

轮询任务接口直到 `status` 变为 `SUCCEEDED`：

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 5. 部署与调用

训练成功后部署模型为在线服务，再像调用普通模型一样使用微调后的模型。

## 使用方式

百炼提供两种操作路径：

- **API / 命令行**：通过 HTTP API 完成上传、训练、部署全流程，适合自动化集成。详见[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
- **控制台（零代码）**：通过百炼控制台可视化界面操作，支持训练单元计费（预付费/后付费），适合快速验证。详见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

> **注意**：通过 API 创建的训练任务仅支持按 Token 计费，暂不支持使用模型训练单元。如需使用训练单元，请通过控制台创建任务。

## 关键超参数

微调效果与超参数配置密切相关，核心参数包括：

| 参数 | 说明 |
|------|------|
| `n_epochs` | 训练轮次，与训练深度正相关 |
| `batch_size` | 每步处理的样本数 |
| `learning_rate` | 学习率，影响收敛速度和稳定性 |
| `lora_rank` | LoRA 低秩矩阵的秩，秩越大可表达更复杂的任务但更易过拟合 |
| `eval_steps` | 每隔多少步进行一次验证 |
| `lr_scheduler_type` | 学习率调度策略（如 cosine） |

**调参建议**：

- 如果 Training Loss 与 Validation Loss 在训练结束时仍在下降（欠拟合），可增加 `n_epochs` 或增大 `lora_rank`。
- 如果 Training Loss 持续下降但 Validation Loss 开始上升（过拟合），应减少 `n_epochs` 或减小 `lora_rank`。
- 如果两者均平稳，说明拟合良好，可直接使用训练产物。

## 典型应用场景

### 安全合规强化

通过 SFT 微调将安全对齐目标写入模型参数，使模型在面对政治、历史、社会等敏感领域的诱导性请求时，主动拒绝并提供正面引导。详见[0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

### 图像/视频风格定制

通过 LoRA 微调训练特定人物、IP 角色或视觉特效的风格模型，微调后可稳定复现训练集中的风格，无需复杂提示词。

### 专属音色定制

当单条音频的声音复刻无法满足还原度要求时，通过 CosyVoice 模型调优训练独立部署的专属音色模型，适用于品牌 IP 音色、有声书等长篇内容生产场景。

## 限制和注意事项

- 模型微调功能仅在**华北2（北京）**地域可用，必须使用该地域的 API Key。
- 阿里云子账号（RAM 用户）需被授予模型调用、训练和部署权限。
- 图像/视频生成模型微调后需先部署（创建 deployment），部署状态为 RUNNING 后才能调用。
- CosyVoice 调优产物为单音色独立模型，`voice` 参数固定为 `default`，不支持声音复刻和声音设计功能。
- 调优平台同一时刻仅运行一个训练任务，后续任务将进入排队状态。
- 训练数据质量直接影响微调效果：文本模型建议使用高质量标注数据，语音模型建议在低噪环境录制、确保发音准确。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)


