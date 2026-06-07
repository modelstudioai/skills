# fine tuning

阿里云百炼平台提供模型调优（Fine-Tuning）功能，当 Prompt 工程或插件调用等方式仍无法满足业务需求时，可通过模型调优进一步提升模型在特定行业、业务场景下的表现。百炼支持对文本生成、视觉理解、语音合成、视频生成和图像生成等多种模型进行调优，提供控制台零代码操作和 API 编程两种使用方式。

## 调优方法

百炼提供三种递进式的调优方法，详见[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)：

- **CPT（持续预训练）**：通过海量无标签领域文本（至少 1000 万 Token）注入专业知识，提升模型在特定行业的表现。
- **SFT（监督微调）**：使用高质量"问-答"对（1000+ 条）教会模型遵循指令和执行任务。
- **DPO（直接偏好优化）**：通过"更好-更差"回答对（100+ 组）对齐人类偏好，抑制幻觉。

推荐的调优顺序为 `CPT（可选）-> SFT -> DPO（可选）`，三者相辅相成。

## 训练模式

每种调优方法又分为两种训练模式：

| 特性 | 全参训练 | 高效训练（LoRA） |
|------|---------|----------------|
| 原理 | 全量更新模型参数 | 通过低秩矩阵分解更新部分参数 |
| 适用场景 | 需要学习新能力、追求全局最优 | 特定场景优化、对时间和成本敏感 |
| 训练时间 | 较长 | 较短 |
| 推荐 | 若模型支持，优先选择全参训练 | 快速验证或数据集较小时适用 |

两种模式的训练费用相同，详见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

## 支持的模型

### 文本生成模型

支持 Qwen3.6/3.5/3/2.5 系列及千问-Plus-Character 等模型，不同模型对 CPT/SFT/DPO 的支持情况不同。代表性模型包括：

- **Qwen3-32B**：支持全部 5 种训练方式（CPT、SFT 全参、SFT 高效、DPO 全参、DPO 高效）
- **Qwen3-8B**：支持 SFT 和 DPO（全参+高效），不支持 CPT
- **Qwen2.5-72B-Instruct**：支持全部训练方式

### 视觉理解模型（千问 VL）

支持 Qwen3-VL 和 Qwen2.5-VL 系列，仅支持 SFT 全参训练和 SFT 高效训练。训练数据需要以 ZIP 压缩包格式上传，包含 `data.jsonl` 和对应的图片/视频文件。

### 语音合成模型（CosyVoice）

仅支持对 `cosyvoice-v3-flash` 进行 SFT 高效微调（`efficient_sft`），目前只能通过 API 方式发起。适用于同一发音人的高还原度专属音色定制，训练音频推荐总时长 1~10 小时。详见 [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

### 视频生成模型（万相）

支持 wan2.5-i2v-preview、wan2.2-i2v-flash（图生视频-基于首帧）和 wan2.2-kf2v-flash（基于首尾帧），采用 SFT-LoRA 高效微调。适用于定制特定动作、特效或风格，详见[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

### 图像生成模型（万相）

支持 wan2.7-image-pro 模型，采用 SFT-LoRA 高效微调，可用于文生图和图生图场景，适合训练特定人物、IP 角色或风格化 LoRA 模型，详见[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 数据格式

### SFT 训练集（文本生成）

使用 ChatML 格式的 JSONL 文件，支持多轮对话：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

对于思考模型（Thinking），思考内容需要用 `<think>` 标签包裹，且只能在最后一个 assistant 输出中使用。

### DPO 训练集

在 SFT 格式基础上增加 `chosen`（正样本）和 `rejected`（负样本）字段：

```json
{"messages": [...],
 "chosen": {"role": "assistant", "content": "赞同的输出"},
 "rejected": {"role": "assistant", "content": "反对的输出"}}
```

### CPT 训练集

纯文本格式，每行一条：

```json
{"text": "文本内容"}
```

### VL 模型训练集

需要以 ZIP 格式上传，包含 `data.jsonl` 和图片/视频文件。`content` 字段使用数组格式，支持图片（`image`）和视频（`video`）字段。

### CosyVoice 训练集

ZIP 压缩包包含 `data.jsonl` 和 `train/` 目录下的 `.wav` 音频文件，每行指定音频路径和对应文本。

## 使用方式

### 控制台操作

在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面创建训练任务，按向导完成配置。主要步骤：选择调优方式和模型 -> 参数配置 -> 选择训练数据 -> 开始训练 -> 发布模型 -> 部署模型 -> 评测模型。

### API 操作

通过 DashScope API 完成全流程，详见[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。核心步骤：

1. **上传数据文件**：`POST /api/v1/files`
2. **创建调优任务**：`POST /api/v1/fine-tunes`，指定 `model`、`training_file_ids`、`training_type` 和 `hyper_parameters`
3. **查询任务状态**：`GET /api/v1/fine-tunes/<job_id>`，等待状态变为 `SUCCEEDED`
4. **部署模型**：`POST /api/v1/deployments`
5. **调用模型**：使用部署后的模型 ID 进行推理调用

## 关键超参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `n_epochs`（循环次数） | 数据量 < 10000 设 3~5，> 10000 设 1~2 | 遍历训练数据的次数 |
| `learning_rate`（学习率） | 高效训练 1e-4 量级，全参训练 1e-5 量级 | 控制参数更新幅度 |
| `batch_size`（批次大小） | 使用默认值 | 每次更新参数的数据量 |
| `max_length`（序列长度） | 设为模型支持的最大值 | 超长数据 SFT 会丢弃，DPO 会截断 |
| `lr_scheduler_type` | linear 或 Inverse_sqrt | 学习率调整策略 |
| `lora_rank`（LoRA 秩值） | 设为最大值 | 秩越大效果越好，训练略慢 |

## 计费说明

- **训练费用**：按训练数据 Token 总数 x 循环次数 x 训练单价计费（最小计费单位 1 token）
- **部署费用**：调优后的模型需要部署才能使用，按模型单元使用时长计费
- **评测费用**：不额外收费

训练单价因模型而异，如 Qwen3-8B 为 0.006 元/千 Token，Qwen2.5-72B-Instruct 为 0.15 元/千 Token。

## 最佳实践与注意事项

- **优先尝试 Prompt 工程和插件调用**：模型调优通常作为改进模型表现的"最后手段"，迭代优化 Prompt 比调优更敏捷、成本更低。
- **数据质量优先**：训练数据需要覆盖目标场景的多样性，且各类场景数据数量应相对均衡。
- **关注损失曲线**：训练中若 Training Loss 下降而 Validation Loss 上升，表明过拟合，需减少训练次数或增加数据多样性。
- **安全合规场景**：可通过 SFT 微调将安全对齐目标写入模型参数，强化模型在政治安全、历史认知等维度的合规表现，详见[0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。
- **地域限制**：模型调优功能仅适用于中国大陆版（北京地域）。
- **调优后模型不支持导出**：只能在百炼平台上部署后使用，不支持下载到本地。

> **注意**：通过 API 创建的训练任务仅支持按 Token 计费，暂不支持使用模型训练单元（预付费或后付费）。如需使用训练单元，请通过控制台创建任务。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)


