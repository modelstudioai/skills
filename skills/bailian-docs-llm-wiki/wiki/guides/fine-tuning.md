# fine tuning

阿里云百炼平台的模型调优（Fine-tuning）功能允许开发者基于自有数据定制模型，提升模型在特定行业或业务场景下的表现、降低输出延迟、抑制幻觉、对齐人类偏好。平台支持文本生成、视觉理解、图像生成、视频生成及语音合成等多种模态的模型调优，提供控制台和 API 两种操作方式。

## 调优方法概览

百炼平台提供三种递进式调优方法，推荐按 `CPT（可选）→ SFT → DPO（可选）` 的顺序使用：

| 方法 | 目标 | 数据要求 | 典型场景 |
|------|------|----------|----------|
| CPT（继续预训练） | 注入领域知识 | 1000万+ [Token](../concepts/token.md) 无标签文本 | 金融/医疗/法律等垂直领域适配 |
| SFT（监督微调） | 学会遵循指令 | 1000+ 条高质量问答对 | 客服、代码助手、Agent 工具调用 |
| DPO（直接偏好优化） | 对齐人类偏好 | 100+ 组正负样本对 | 安全合规强化、降低幻觉 |

每种方法还区分**全参训练**和**高效训练（LoRA）**两种模式。全参训练效果更好但耗时更长；高效训练收敛快、成本低，适合快速验证和对时间敏感的场景。详细对比参见[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持的模型

### 文本生成

支持 Qwen3.6/3.5/3/2.5 系列多个规格的模型，包括：

- **全参+高效训练均支持**：qwen3-32b、qwen3-8b、qwen3-4b-instruct-2507、qwen3-1.7b、qwen3-0.6b、qwen2.5-72b/32b/14b/7b-instruct 等
- **仅 SFT 全参**：qwen3.6-flash-2026-04-16、qwen3.5-flash-2026-02-23
- **SFT 全参+高效**：qwen3.5-27b、qwen3.5-9b、qwen3-14b 等

### 视觉理解（千问VL）

支持 Qwen3-VL-8B/4B-Instruct、Qwen2.5-VL-72B/32B/7B-Instruct 等模型的 SFT 全参和高效训练。

### 图像与视频生成

- **图像生成**：wan2.7-image-pro、wan2.7-image（SFT-LoRA），支持文生图和图生图微调
- **视频生成**：wan2.5-i2v-preview、wan2.2-i2v-flash、wan2.2-kf2v-flash（SFT-LoRA）

### 语音合成

- **CosyVoice**：cosyvoice-v3-flash（SFT 高效微调），用于高还原度专属音色定制

## 使用方式

### 控制台操作

百炼控制台提供零代码的可视化调优界面，操作流程为：

1. 在[数据管理](https://bailian.console.aliyun.com/?tab=model#/efm/model_data)页面上传训练数据集
2. 在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面创建训练任务，选择模型、训练方式和超参数
3. 观察 Training Loss / Validation Loss 曲线判断训练状态
4. 训练完成后在[模型部署](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)页面一键部署

具体步骤参见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

### API 操作

通过 DashScope API 完成全流程：

```bash
# 1. 上传训练文件
curl --request POST 'https://dashscope.aliyuncs.com/api/v1/files' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--form 'files=@"/path/to/file.jsonl"' \
--form 'purpose="fine-tune"'

# 2. 创建调优任务
curl --location "https://dashscope.aliyuncs.com/api/v1/fine-tunes" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json' \
--data '{"model":"qwen3-8b", "training_file_ids":["<file_id>"], "training_type":"sft", ...}'

# 3. 查询任务状态（轮询直到 SUCCEEDED）
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

完整 API 参数和示例参见[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 训练数据格式

### SFT 文本生成

采用 ChatML 格式的 JSONL 文件，每行一条训练样本：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

思考模型（Thinking）需要在最后一个 assistant 输出中使用 `<think>` 标签包裹思考内容。

### SFT 视觉理解

在 ChatML 基础上，user content 使用数组格式，支持 image 和 video 字段，训练数据与图片/视频打包为 ZIP 上传。

### DPO 数据集

在 messages 基础上增加 `chosen` 和 `rejected` 字段，分别提供正面和负面示例。

### 图像/视频生成

训练集打包为 ZIP，包含 `data.jsonl` 标注文件和训练图像/视频文件。图像生成训练集需包含触发词（trigger word）以激活 LoRA 风格。

### 语音合成

ZIP 包内含 `data.jsonl`（每行 `wav_fn` + `text`）和 `train/` 目录下的 WAV 音频文件，推荐总时长 1-10 小时、不少于 150 条样本。

## 关键超参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| learning_rate | 高效训练 1e-4；全参训练 1e-5 | 过高导致效果退化，过低则变化不明显 |
| n_epochs | 数据量<1万时 3-5 次；>1万时 1-2 次 | 循环次数越多费用越高 |
| batch_size | 16 或 32 | 模型每看多少条数据更新一次参数 |
| max_length | 设为模型支持最大值 | SFT 超长数据会被丢弃，DPO 会截断 |
| lora_rank | 设为模型支持最大值 | 秩越大效果越好，但训练略慢 |

## 部署与调用

微调完成后需要将模型部署为在线服务才能调用：

```bash
# 部署模型
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json' \
--data '{"model_name": "<finetuned_output>", "capacity": 1, "plan": "lora"}'
```

部署状态变为 RUNNING 后即可通过标准 API 调用微调后的模型。

## [计费](../concepts/billing.md)说明

训练费用按 [Token](../concepts/token.md) 用量[计费](../concepts/billing.md)：`费用 = 训练数据 Token 总数 x 循环次数 x 训练单价`。不同模型单价不同，从 0.003 元/千[Token](../concepts/token.md)（qwen3-0.6b）到 0.15 元/千[Token](../concepts/token.md)（qwen2.5-72b-instruct）不等。可在控制台查看预估费用。

## 限制和注意事项

- 模型调优功能**仅在华北2（北京）地域可用**，必须使用该地域的 [API Key](../concepts/api-key.md)
- 子账号需要单独授予模型调用、训练和部署权限
- 通过 API 创建的训练任务仅支持按 [Token](../concepts/token.md) [计费](../concepts/billing.md)，暂不支持训练单元
- 单个文件最大 300MB，有效文件总空间配额 5GB，总数量 100 个
- 图像/视频生成模型微调后仅支持[异步调用](../concepts/async-invocation.md)
- CosyVoice 调优产物为单音色模型，voice 参数必须固定为 `default`

## 安全合规微调

通过 SFT 微调可强化模型的安全合规能力，使模型在面对敏感请求时主动拒绝并正面引导。实测显示，使用全量微调（n_epochs=3, learning_rate=1e-5）可将安全通过率从 89% 提升至 99%。详见[0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)





