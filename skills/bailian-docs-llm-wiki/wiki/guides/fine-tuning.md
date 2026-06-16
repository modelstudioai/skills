# fine tuning

阿里云百炼平台提供模型调优（fine tuning）能力，支持对文本生成、视觉理解、视频生成、图像生成和语音合成等多种模型进行微调训练。当 [Prompt 工程](../concepts/prompt-engineering.md)或插件调用等优化手段无法满足特定行业或业务场景的需求时，模型调优是提升模型表现的核心策略，可用于提升领域表现、降低输出延迟、抑制幻觉以及对齐人类偏好。

## 调优方式概览

百炼提供三种递进式的调优方法，推荐按 `CPT（可选）→ SFT → DPO（可选）` 的顺序使用：

| 调优方式 | 全称 | 核心目标 | 数据量要求 |
|---------|------|---------|-----------|
| CPT | 持续预训练 | 注入领域知识（补知识） | 1000 万+ Token 无标签文本 |
| SFT | 监督微调 | 学会遵循指令（学做事） | 1000+ 条问答对 |
| DPO | 直接偏好优化 | 对齐人类偏好（做得更好） | 100+ 组正负样本对 |

每种方式又分为**全参训练**和**高效训练（LoRA）**两种模式。全参训练效果通常更优但耗时更长；LoRA 训练速度快、成本低，适合快速验证。详见 [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持的模型

### 文本生成

支持 Qwen 系列多个规格的模型进行调优，包括：

- **Qwen3 系列**：qwen3-32b、qwen3-14b、qwen3-8b、qwen3-4b-instruct-2507、qwen3-1.7b、qwen3-0.6b 等，其中 qwen3-32b 支持全部五种训练方式（CPT/SFT/efficient_sft/DPO全参/DPO高效）
- **Qwen3.5/3.6 系列**：qwen3.6-flash-2026-04-16、qwen3.5-27b、qwen3.5-9b 等，主要支持 SFT 全参训练
- **Qwen2.5 系列**：qwen2.5-72b-instruct、qwen2.5-32b-instruct 等，支持全部五种训练方式

### 视觉理解（千问 VL）

支持 Qwen3-VL 和 Qwen2.5-VL 系列，包括 qwen3-vl-8b-instruct、qwen3-vl-4b-instruct、qwen2.5-vl-72b-instruct 等，均支持 SFT 全参和高效训练。

### 视频生成（万相）

支持 wan2.5-i2v-preview、wan2.2-i2v-flash（图生视频-基于首帧）和 wan2.2-kf2v-flash（图生视频-基于首尾帧）的 SFT-LoRA 高效微调。详见 [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

### 图像生成（万相）

支持 wan2.7-image-pro、wan2.7-image 的 SFT-LoRA 高效微调，涵盖文生图和图生图两种场景。详见 [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

### 语音合成（CosyVoice）

支持 cosyvoice-v3-flash 的 SFT 高效微调（efficient_sft），适用于同一发音人的高还原度音色定制。详见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

### 控制台操作

百炼控制台提供可视化的模型调优功能，无需编码。基本流程为：

1. 在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面创建训练任务
2. 选择调优方式（SFT/CPT/DPO）、基础模型和训练方式（全参/LoRA）
3. 上传训练集并配置超参数
4. 启动训练，通过损失曲线观察效果
5. 训练完成后部署模型并评测

详细操作步骤参见 [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

### API / 命令行

通过 DashScope API 完成从上传文件、创建任务到部署调用的全流程：

1. **上传调优文件**：`POST https://dashscope.aliyuncs.com/api/v1/files`，设置 `purpose="fine-tune"`
2. **创建调优任务**：`POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`，指定 model、training_file_ids、training_type 和 hyper_parameters
3. **查询任务状态**：`GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>`，等待 status 变为 SUCCEEDED
4. **部署模型**：`POST https://dashscope.aliyuncs.com/api/v1/deployments`，使用 finetuned_output 作为 model_name
5. **调用模型**：部署状态变为 RUNNING 后即可通过 API 调用

详见 [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 数据格式

### SFT 训练数据

采用 ChatML 格式的 JSONL 文件，支持多轮对话：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

思考模型（Thinking）需要在最后一个 assistant 输出中使用 `<think>` 标签包裹思考内容。视觉理解模型（千问 VL）的 content 需使用数组格式，支持传入图片和视频文件。

### DPO 训练数据

在 messages 基础上增加 chosen（正样本）和 rejected（负样本）字段：

```json
{"messages": [..., {"role": "user", "content": "用户输入"}],
 "chosen": {"role": "assistant", "content": "好的回答"},
 "rejected": {"role": "assistant", "content": "差的回答"}}
```

### CPT 训练数据

纯文本格式：`{"text":"文本内容"}`

### 视频/图像/语音调优数据

均需打包为 ZIP 格式上传。视频和图像调优需要包含媒体文件和 data.jsonl 标注文件；语音调优需要 WAV 音频文件和对应的文本标注。

## 关键超参数

| 参数 | 推荐设置 | 说明 |
|------|---------|------|
| learning_rate | 高效训练 1e-4，全参训练 1e-5 | 控制权重修正强度，过高会导致效果变差 |
| n_epochs | 数据 < 1 万条循环 3-5 次，> 1 万条循环 1-2 次 | 训练循环次数，影响训练时间和费用 |
| batch_size | 使用默认值（16/32） | 参数更新的数据步长 |
| max_length | 设置为模型支持的最大值 | 单条数据最大 token 长度 |
| lora_rank | 设置为模型支持的最大值 | LoRA 低秩矩阵的秩，越大效果越好但训练更慢 |
| lr_scheduler_type | linear 或 inverse_sqrt | 学习率动态调整策略 |

## 计费与限制

- **训练费用**：按训练数据 Token 总数 x 循环次数 x 训练单价计算，不同模型单价不同（如 qwen3-8b 为 0.006 元/千 Token，qwen2.5-72b-instruct 为 0.15 元/千 Token）
- **部署费用**：调优后的模型需要部署才能使用，部署按模型单元时长计费
- **地域限制**：所有调优功能仅在华北2（北京）地域可用
- **RAM 权限**：子账号需被授予模型调用、训练和部署权限

> **注意**：模型调优通常作为改进模型表现的"最后手段"。建议优先尝试 [Prompt 工程](../concepts/prompt-engineering.md)或插件调用进行优化，这些方式迭代更敏捷、成本更低。即使最终需要调优，前期的 Prompt 工作也可复用于构建训练数据集。

## 安全合规调优

百炼支持通过零代码 SFT 微调强化模型的安全合规能力。以 Qwen3-8B 为基础模型，使用覆盖政治安全、历史认知、社会伦理等多个维度的高质量训练数据进行微调，可使模型在面对敏感请求时主动拒绝有害内容并提供正面引导。实测在全量微调 + n_epochs=3 + learning_rate=1e-5 配置下，安全评测通过率可从 89% 提升至 99%。详见 [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)






