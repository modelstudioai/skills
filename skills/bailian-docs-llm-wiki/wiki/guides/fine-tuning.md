# fine tuning

阿里云百炼平台提供模型调优（Fine-Tuning）能力，支持对文本生成、视觉理解、图像生成、视频生成及语音合成等多种模型进行微调训练，以提升模型在特定行业或业务场景下的表现。调优方式包括监督微调（SFT）、继续预训练（CPT）和直接偏好优化（DPO），用户可通过控制台或 API 两种途径完成全流程操作。

## 调优方式概览

百炼提供三种递进式调优方式，推荐按 `CPT（可选）→ SFT → DPO（可选）` 的顺序使用：

| 方式 | 核心目标 | 输入数据要求 | 典型场景 |
|------|---------|-------------|---------|
| **CPT（继续预训练）** | 注入领域知识 | 1000万+ Token 无标签领域文本 | 金融术语、医疗病理、法律判例等专业知识 |
| **SFT（监督微调）** | 学会遵循指令 | 1000+ 条高质量"问-答"对 | 客服流程、代码范式、Agent 工具调用 |
| **DPO（直接偏好优化）** | 对齐人类偏好 | 100+ 组同指令下的"更好-更差"回答对 | 安全合规、简洁输出、客观中立 |

详见[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持的模型

### 文本生成

支持 Qwen3.6/3.5/3/2.5 系列多种规格模型，训练方式覆盖 CPT、SFT（全参/高效）、DPO（全参/高效）。主要模型包括：

- **Qwen3-32B**：支持全部五种训练方式（CPT/SFT全参/SFT高效/DPO全参/DPO高效）
- **Qwen3-8B / Qwen3-14B**：支持 SFT 和 DPO
- **Qwen2.5-72B-Instruct / 32B / 14B / 7B**：支持全部五种训练方式
- **千问-Plus-Character**：支持 SFT 和 DPO

### 视觉理解（千问VL）

支持 Qwen3-VL（8B/4B）和 Qwen2.5-VL（72B/32B/7B）系列，训练方式为 SFT 全参和 SFT 高效训练。

### 图像生成（万相）

支持 wan2.7-image-pro、wan2.7-image 模型的 SFT-LoRA 高效微调，适用于文生图和图生图场景。详见[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

### 视频生成（万相）

支持 wan2.5-i2v-preview、wan2.2-i2v-flash（基于首帧）和 wan2.2-kf2v-flash（基于首尾帧）模型的 SFT-LoRA 高效微调。详见[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

### 语音合成（CosyVoice）

支持 cosyvoice-v3-flash 模型的 SFT 高效微调，可针对特定发音人的音色、韵律、停顿节奏进行定制。详见[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

### 控制台操作

百炼控制台提供可视化的零代码调优能力，操作流程为：

1. **选择调优方式**：在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面创建训练任务，选择 CPT/SFT/DPO
2. **配置超参数**：设置 batch_size、learning_rate、n_epochs 等参数
3. **上传数据集**：在[数据管理](https://bailian.console.aliyun.com/?tab=model#/efm/model_data)上传 `.jsonl` 或 `.xlsx` 格式训练数据
4. **启动训练**：观察 Training Loss 和 Validation Loss 曲线判断训练效果
5. **部署模型**：训练完成后在[模型部署](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)页面一键部署

详见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

### API 操作

通过 DashScope API 完成调优全流程，核心步骤为：

1. **上传文件**：`POST /api/v1/files`，获取 `file_id`
2. **创建调优任务**：`POST /api/v1/fine-tunes`，指定 model、training_file_ids、training_type 和 hyper_parameters
3. **查询任务状态**：`GET /api/v1/fine-tunes/<job_id>`，轮询直到 `status` 为 `SUCCEEDED`
4. **部署模型**：`POST /api/v1/deployments`，获取 `deployed_model`
5. **调用模型**：使用 `deployed_model` 作为 model 参数发起推理请求

详见[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 训练数据格式

### SFT 数据集

使用 ChatML 格式的 `.jsonl` 文件，支持多轮对话：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

- **思考模型（Thinking）**：最后一个 assistant 输出中使用 `<think>...</think>` 标签包裹思考内容
- **视觉理解（千问VL）**：content 使用数组格式，支持 image/video 字段，需将图片和 data.jsonl 打包为 ZIP
- **图像/视频生成（万相）**：训练集包含目标图像/视频和 data.jsonl 标注文件，打包为 ZIP

### DPO 数据集

在 SFT 格式基础上增加 `chosen`（正样本）和 `rejected`（负样本）字段。

### CPT 数据集

纯文本格式：`{"text": "文本内容"}`，需至少 1000 万 Token。

## 关键超参数

| 参数 | 推荐值 | 说明 |
|------|-------|------|
| **learning_rate** | 高效训练 1e-4，全参训练 1e-5 | 过高导致训练不稳定，过低则效果不明显 |
| **n_epochs** | 数据量 <10000 设 3-5，>10000 设 1-2 | 循环次数越多费用越高 |
| **batch_size** | 默认值（16/32） | 模型每看多少条数据更新一次参数 |
| **max_length** | 设为模型支持的最大值 | SFT 超长数据直接丢弃，DPO 超长数据截断 |
| **lora_rank** | 设为模型支持的最大值 | LoRA 秩越大效果越好，但训练略慢 |
| **lr_scheduler_type** | linear 或 inverse_sqrt | 学习率调整策略，推荐线性递减 |

> **注意**：全参训练与高效训练（LoRA）费用相同，如果模型支持全参训练则推荐优先选择全参训练，效果更好。

## 训练效果判断

通过 Training Loss 和 Validation Loss 曲线判断训练状态：

- **欠拟合**（两者仍在下降）：增加 n_epochs 或增大 lora_rank
- **过拟合**（Training Loss 下降但 Validation Loss 上升）：减少 n_epochs 或减小 lora_rank
- **良好拟合**（两者均趋于平稳）：可结束训练进入部署

## 适用地域与限制

- 模型调优功能仅在**华北2（北京）**地域可用，需使用该地域的 API Key
- 子账号（RAM 用户）需授予调用、训练和部署权限
- 通过 API 创建的训练任务仅支持按 Token 计费，使用训练单元需通过控制台
- 单个上传文件最大 300 MB，有效文件总空间 5 GB，总数量 100 个

## 典型应用场景

- **安全合规强化**：通过 SFT 微调使模型在面对敏感请求时主动拒绝并正面引导，详见[0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- **图像风格定制**：微调万相模型生成特定 IP 形象或画面风格
- **视频特效定制**：微调万相视频模型实现特定动作或特效
- **语音音色定制**：微调 CosyVoice 模型还原特定发音人的声学特征

## 来源文档

- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)
- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)



