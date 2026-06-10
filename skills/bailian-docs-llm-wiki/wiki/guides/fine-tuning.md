# fine tuning

阿里云百炼平台提供模型调优（Fine-tuning）能力，支持对文本生成、视觉理解、视频生成、图像生成和语音合成等多种模型进行微调训练，以提升模型在特定行业或业务场景下的表现。模型调优包含监督微调（SFT）、继续预训练（CPT）和直接偏好优化（DPO）三种训练方式，支持全参训练和高效训练（LoRA）两种训练模式。当 Prompt 工程或插件调用等优化方法仍无法满足需求时，模型调优是改进模型表现的核心手段。

## 调优方法与适用场景

百炼提供的三种调优方式并不互斥，而是递进的、相辅相成的，推荐按 `CPT（可选）→ SFT → DPO（可选）` 的顺序使用：

| 方法 | 核心目标 | 输入数据要求 | 典型场景 |
|------|---------|------------|---------|
| CPT（继续预训练） | 注入领域知识 | 1000 万+ Token 无标签文本 | 金融、医疗、法律等垂直领域适配 |
| SFT（监督微调） | 学会遵循指令 | 1000+ 条高质量问答对 | 客服机器人、代码助手、Agent 工具调用 |
| DPO（直接偏好优化） | 对齐人类偏好 | 100+ 组同一指令的好坏回答对 | 安全合规强化、降低幻觉、风格调整 |

详细的方法对比和流程说明参见[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持的模型

### 文本生成模型

支持 Qwen3.6、Qwen3.5、Qwen3、Qwen2.5 系列及千问-Plus-Character 等模型。主要模型的调优方式支持情况：

- **Qwen3-32B**：支持 CPT、SFT 全参、SFT 高效、DPO 全参、DPO 高效（全量支持）
- **Qwen3-8B / Qwen3-14B**：支持 SFT 全参、SFT 高效、DPO 全参、DPO 高效
- **Qwen3-1.7B / Qwen3-0.6B**：全量支持所有训练方式
- **Qwen2.5 系列（72B/32B/14B/7B）**：全量支持所有训练方式

### 视觉理解模型（千问 VL）

支持 Qwen3-VL（8B-Instruct、8B-Thinking、4B-Instruct）和 Qwen2.5-VL（72B/32B/7B）系列，均支持 SFT 全参和 SFT 高效训练。

### 视频生成模型

支持万相视频系列模型的 SFT-LoRA 高效微调，包括图生视频基于首帧（wan2.5-i2v-preview、wan2.2-i2v-flash）和基于首尾帧（wan2.2-kf2v-flash）模型。详见[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

### 图像生成模型

支持 wan2.7-image-pro 模型的 SFT-LoRA 高效微调，可用于文生图和图生图两种场景。详见[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

### 语音合成模型（CosyVoice）

支持 cosyvoice-v3-flash 模型的 SFT 高效微调，用于高还原度专属音色定制。调优产物为独立部署的单音色模型，适用于品牌 IP 音色定制和长篇有声内容生产。详见[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 训练模式：全参 vs 高效（LoRA）

| 维度 | 全参训练 | 高效训练（LoRA） |
|------|---------|----------------|
| 适用场景 | 需要模型学习新能力，追求全局效果最优 | 优化特定场景效果，对训练时间和成本敏感 |
| 训练时间 | 较长，收敛速度较慢 | 较短，收敛速度快 |
| 训练费用 | 与高效训练相同 | 与全参训练相同 |

由于两种训练方式费用相同，如果模型支持全参训练，建议优先选择全参训练，性价比更高。

## 使用方式

### 控制台操作

百炼控制台提供可视化的模型调优界面，无需编码即可完成训练任务创建、参数配置、训练监控和模型部署。基本流程为：创建训练任务 → 选择调优方式和模型 → 配置超参数 → 上传数据集 → 开始训练 → 部署模型。详细操作步骤参见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

### API/命令行操作

通过 DashScope API（HTTP）操作，基本流程为：

1. **上传调优文件**：`POST https://dashscope.aliyuncs.com/api/v1/files`，设置 `purpose="fine-tune"`
2. **创建调优任务**：`POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`，指定模型、训练文件和超参数
3. **查询任务状态**：`GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}`，轮询直到 `status` 变为 `SUCCEEDED`
4. **部署模型**：`POST https://dashscope.aliyuncs.com/api/v1/deployments`，使用 `finetuned_output` 作为模型名称
5. **调用模型**：部署状态变为 `RUNNING` 后，使用 `deployed_model` 名称调用

详细的 API 参数和示例参见[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

> **注意**：通过 API 创建的训练任务仅支持按 Token 计费，暂不支持使用模型训练单元（预付费或后付费）。如需使用训练单元，请通过控制台创建任务。

## 数据格式要求

### SFT 训练集

使用 ChatML 格式的 JSONL 文件，支持多轮对话：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

对于思考模型（Thinking），最后一个 assistant 输出需使用 `<think>` 标签包裹思考内容。视觉理解模型（千问 VL）的训练数据需使用数组格式的 content 字段以支持图片和视频输入。

### DPO 训练集

在 SFT 格式基础上增加 `chosen`（正样本）和 `rejected`（负样本）字段。

### CPT 训练集

纯文本格式：`{"text": "文本内容"}`，数据量要求至少 1000 万 Token。

### 视频/图像/语音模型训练集

均需打包为 ZIP 格式上传，包含 `data.jsonl` 标注文件和对应的媒体文件。各模型对文件格式、分辨率、时长等有不同的规格要求。

## 关键超参数

| 参数 | 推荐设置 | 说明 |
|------|---------|------|
| n_epochs | 数据量 < 10000 设 3~5；> 10000 设 1~2 | 训练循环次数，直接影响训练时间和费用 |
| learning_rate | 高效训练 1e-4 级别；全参训练 1e-5 级别 | 过高导致效果变差，过低导致效果不明显 |
| batch_size | 使用默认值（通常 16 或 32） | 每批训练的数据量 |
| max_length | 设置为模型支持的最大值 | SFT 超出会丢弃数据，DPO 超出会截断 |
| lora_rank | 设置为模型支持的最大值（仅高效训练） | 秩越大效果越好，训练略慢 |

## 计费说明

训练费用公式：**（训练数据 Token 总数 + 混合训练数据 Token 总数）x 循环次数 x 训练单价**。

不同模型单价差异较大，例如 Qwen3-8B 为 0.006 元/千 Token，Qwen2.5-72B-Instruct 为 0.15 元/千 Token。调优后的模型需要部署才能使用，部署费用另计。

CosyVoice 语音模型训练费用为 0.2 元/千 Token，另需按部署时长计费。

## 限制与注意事项

- 模型调优仅适用于**中国内地部署模式（北京地域）**，视频和图像生成模型微调需使用北京地域的 API Key
- 调优后的模型必须**先部署再使用**，部署费用较高，建议在 Prompt 工程和插件调用无法满足需求时再考虑调优
- 子账号（RAM 用户）需要被授予模型调用、训练和部署权限
- 调优平台同一时刻仅运行一个训练任务，新任务会排队等待
- 通过控制台可观察 Training Loss 和 Validation Loss 曲线判断训练效果：若两者均下降为欠拟合（增加 n_epochs），Training Loss 下降但 Validation Loss 上升为过拟合（减少 n_epochs）
- CosyVoice 调优产物为单音色模型，训练数据应为同一发音人，不支持通过调优扩展基础模型不支持的语种
- 安全合规场景可通过 SFT 微调将安全对齐目标写入模型参数，详见[0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)


