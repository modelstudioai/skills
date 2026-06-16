# fine tuning

阿里云百炼平台提供模型调优（Fine-Tuning）能力，支持对文本生成、视觉理解、视频生成、图像生成和语音合成等多种模型进行微调训练。当 [Prompt 工程](../concepts/prompt-engineering.md)或插件调用等优化方法仍无法满足需求时，可通过模型调优提升模型在特定行业和业务场景下的表现，降低输出延迟，并对齐人类偏好。

## 调优方法概览

百炼提供三种递进的模型调优方式，适用于不同阶段和目标：

| 调优方式 | 核心目标 | 输入数据要求 | 典型场景 |
|---------|---------|------------|---------|
| CPT（持续预训练） | 注入领域知识 | 1000万+ Token 无标签文本 | 金融/医疗/法律等垂直领域适配 |
| SFT（监督微调） | 学会遵循指令 | 1000+ 条高质量问答对 | 客服、代码助手、Agent 工具调用 |
| DPO（直接偏好优化） | 对齐人类偏好 | 100+ 组同一指令下的好坏回答对 | 安全合规、降低幻觉、提升回答质量 |

推荐的调优顺序为 `CPT（可选）-> SFT -> DPO（可选）`。详细的调优方法对比和选择建议参见[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持的模型

### 文本生成模型

支持 Qwen3.6、Qwen3.5、Qwen3、Qwen2.5 系列等多款模型，涵盖从 0.6B 到 72B 多种参数规模。不同模型对 CPT、SFT（全参/高效）、DPO（全参/高效）的支持情况各异。代表性模型包括：

- **Qwen3-32B**：支持全部五种训练方式（CPT、SFT 全参、SFT 高效、DPO 全参、DPO 高效）
- **Qwen3-8B / Qwen3-1.7B / Qwen3-0.6B**：同样支持全部训练方式，适合快速验证
- **Qwen2.5-72B-Instruct**：支持全部训练方式，适合追求最优效果

### 视觉理解模型（千问VL）

支持 Qwen3-VL（8B/4B）和 Qwen2.5-VL（72B/32B/7B）系列，均支持 SFT 全参训练和 SFT 高效训练。

### 视频生成模型（万相）

通过 SFT-LoRA 高效微调方式支持以下模型，详见[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)：

- 图生视频-基于首帧：wan2.5-i2v-preview、wan2.2-i2v-flash
- 图生视频-基于首尾帧：wan2.2-kf2v-flash

### 图像生成模型（万相）

通过 SFT-LoRA 高效微调方式支持以下模型，详见[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)：

- 图像生成（文生图/图生图）：wan2.7-image-pro、wan2.7-image

### 语音合成模型（CosyVoice）

支持对 `cosyvoice-v3-flash` 进行 SFT 高效微调，适用于同一发音人的高还原度专属音色定制。详见[CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 训练模式

| 模式 | 说明 | 适用场景 |
|-----|------|---------|
| 全参训练 | 更新全部模型参数，效果通常更好 | 需要学习新能力、追求全局最优效果 |
| 高效训练（LoRA） | 仅更新低秩分解后的部分参数，收敛快 | 对训练时间和成本敏感、快速验证场景 |

由于两种训练方式费用相同，百炼推荐在模型支持全参训练时优先选择全参训练。

## 使用方式

### 控制台方式

通过百炼控制台可视化操作，无需编码。主要步骤：

1. 在模型调优页面创建训练任务，选择调优方式（CPT/SFT/DPO）和基础模型
2. 配置超参数（批次大小、学习率、循环次数等，可使用平台推荐默认值）
3. 上传训练集，配置验证集（支持自动切分）
4. 启动训练并通过 Loss 曲线监控训练过程
5. 训练完成后导出参数快照并部署模型

详细的控制台操作指南参见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

### API 方式

通过 HTTP API 完成完整的调优流程，适合自动化集成。核心步骤：

1. **上传调优文件**：`POST /api/v1/files`，设置 `purpose="fine-tune"`
2. **创建调优任务**：`POST /api/v1/fine-tunes`，指定 `model`、`training_file_ids`、`training_type` 和 `hyper_parameters`
3. **查询任务状态**：`GET /api/v1/fine-tunes/<job_id>`，轮询直到 `status` 为 `SUCCEEDED`
4. **部署模型**：`POST /api/v1/deployments`，使用 `finetuned_output` 作为 `model_name`
5. **查询部署状态**：轮询直到 `status` 为 `RUNNING`，然后调用模型

API 方式创建的训练任务仅支持按 Token 计费，不支持使用模型训练单元。完整的 API 操作示例参见[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 训练数据格式

### SFT 数据集

采用 ChatML 格式的 JSONL 文件，每行一条训练样本，支持多轮对话：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

思考模型（Thinking）的训练数据需要在最后一个 assistant 输出中包含 `<think>` 标签。视觉理解模型（VL）的训练数据需要将 content 字段改为数组格式以支持图片和视频输入，并打包为 ZIP 文件上传。

### DPO 数据集

在 messages 基础上增加 `chosen`（正样本）和 `rejected`（负样本）字段：

```json
{"messages": [...],
 "chosen": {"role": "assistant", "content": "赞同的输出"},
 "rejected": {"role": "assistant", "content": "反对的输出"}}
```

### CPT 数据集

纯文本格式，每行一个 JSON 对象：

```json
{"text": "文本内容"}
```

### 视频/图像微调数据集

需要将训练数据（视频/图像文件 + 标注文件 `data.jsonl`）打包为 ZIP 格式上传。

## 关键超参数

| 参数 | 推荐设置 | 说明 |
|-----|---------|------|
| batch_size | 使用默认值 | 模型每看多少条数据更新一次参数 |
| learning_rate | 高效训练 1e-4；全参训练 1e-5 | 控制权重修正强度，过高易不稳定，过低效果不明显 |
| n_epochs | 数据量<10000 用 3~5；>10000 用 1~2 | 训练循环次数，越多耗时越长费用越高 |
| max_length | 设为模型支持的最大值 | 单条数据 token 最大长度，SFT 超长直接丢弃 |
| lora_rank | 设为模型支持的最大值 | LoRA 低秩矩阵的秩，越大效果越好但训练略慢 |

## 计费说明

模型调优涉及两部分费用：

- **训练费用**：按训练消耗的 Token 数计费，公式为 `（训练数据 Token 总数 + 混合训练数据 Token 总数）x 循环次数 x 训练单价`
- **部署费用**：调优后的模型需部署后才能使用，按模型单元使用时长计费

不同模型的训练单价差异较大，例如 Qwen3-8B 为 0.006 元/千 Token，而 Qwen2.5-72B-Instruct 为 0.15 元/千 Token。

## 限制与注意事项

- 模型调优功能仅在**华北2（北京）地域**可用
- 阿里云子账号需要额外授予模型调用、训练和部署权限
- 模型调优通常作为优化模型表现的"最后手段"，建议先尝试 [Prompt 工程](../concepts/prompt-engineering.md)和插件调用
- 调优后的模型必须先部署才能使用，部署会产生额外费用
- 训练过程耗时较长（数小时到数天不等），请根据 Loss 曲线判断是否需要调整超参数
- 过高的训练轮次可能导致过拟合或基础能力退化

> **注意**：CosyVoice 语音模型的调优产物是独立部署的单音色模型（`voice` 参数必须为 `default`），不支持声音复刻、声音设计和指令控制功能，也无法通过调优扩展基础模型的语种支持范围。

## 典型应用场景

- **安全合规强化**：通过 SFT 微调将安全对齐目标写入模型参数，使模型主动拒绝有害请求并提供正面引导。详见[0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- **角色扮演/IP定制**：训练特定角色的对话风格和人设
- **视频特效定制**：训练 LoRA 模型复现特定视觉特效（如"金钱雨"特效）
- **图像风格定制**：训练人物 LoRA 或风格 LoRA 实现稳定的图像风格化输出
- **品牌音色定制**：基于多条同一发音人的录音训练专属音色模型

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)


