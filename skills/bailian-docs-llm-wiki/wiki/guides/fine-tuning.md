# fine tuning

阿里云百炼平台提供模型调优（Fine-tuning）能力，支持对文本生成、视觉理解、视频生成、图像生成和语音合成等多种模型进行微调训练。当 [Prompt 工程](../concepts/prompt-engineering.md)和插件调用仍无法满足特定业务需求时，模型调优是提升模型在垂直领域表现的核心手段。百炼支持 SFT（监督微调）、CPT（继续预训练）、DPO（直接偏好优化）三种训练方式，同时提供全参训练和高效训练（LoRA）两种训练模式。

## 调优方法与适用场景

百炼提供的三种调优方式递进且互补，推荐按 `CPT（可选）-> SFT -> DPO（可选）` 的顺序使用：

- **CPT（继续预训练）**：通过海量无标签领域文本（至少 1000 万 Token）注入专业知识，适用于金融、医疗、法律等需要深度领域适配的场景。
- **SFT（监督微调）**：使用 1000+ 条高质量"问-答"对训练模型遵循指令和执行任务，适用于客服机器人、代码助手、Agent 工具调用等场景。
- **DPO（直接偏好优化）**：通过 100+ 组正负样本对齐人类偏好，针对 bad case 进行优化，适用于安全合规强化、输出质量提升等场景。

训练模式方面，**全参训练**更新全部模型参数，效果通常更好；**高效训练（LoRA）**仅更新低秩部分参数，速度更快、成本更低。两种方式费用相同，如果模型支持全参训练则优先选择。详细的方法对比见[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。

## 支持调优的模型

### 文本生成模型

支持 Qwen3.6-Flash、Qwen3.5（27B/9B）、Qwen3（32B/14B/8B/4B/1.7B/0.6B）、Qwen2.5（72B/32B/14B/7B）、千问-Plus-Character 等模型。不同模型支持的训练方式（CPT/SFT 全参/SFT 高效/DPO 全参/DPO 高效）各有差异，具体支持矩阵请参考[模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)中的模型列表。

### 视觉理解模型（千问 VL）

支持 Qwen3-VL-8B-Instruct、Qwen3-VL-8B-Thinking、Qwen3-VL-4B-Instruct、Qwen2.5-VL-72B/32B/7B-Instruct 等模型，均支持 SFT 全参和 SFT 高效训练。VL 模型的训练数据需打包为 ZIP 压缩包，包含 `data.jsonl` 和图片/视频文件。

### 视频生成模型

支持对万相视频生成模型进行 SFT-LoRA 高效微调，包括图生视频-基于首帧（wan2.5-i2v-preview、wan2.2-i2v-flash）和图生视频-基于首尾帧（wan2.2-kf2v-flash）。适用于定制特定动作、特效或风格。详见[微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。

### 图像生成模型

支持对万相图像生成模型（wan2.7-image-pro、wan2.7-image）进行 SFT-LoRA 高效微调，覆盖文生图和图生图两种场景。可用于训练人物 LoRA、风格化 LoRA 和 IP 角色模型。详见[微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

### 语音合成模型（CosyVoice）

支持对 `cosyvoice-v3-flash` 进行 SFT 高效微调，用于同一发音人的高还原度专属音色定制。调优产物为单音色独立模型，适用于品牌 IP 音色定制和长篇有声内容制作。详见 [CosyVoice 模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)。

## 使用方式

### 控制台调优

百炼提供可视化的零代码调优界面，完整流程为：

1. 在[数据管理](https://bailian.console.aliyun.com/?tab=model#/efm/model_data)页面上传训练数据集
2. 在[模型调优](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)页面创建训练任务，选择模型、训练方式和超参数
3. 等待训练完成，通过损失曲线判断训练效果
4. 在[模型部署](https://bailian.console.aliyun.com/?tab=model#/efm/model_deploy)页面部署微调后的模型
5. 在[模型评测](https://bailian.console.aliyun.com/?tab=model#/efm/model_evaluate)页面评估效果

控制台操作的详细步骤见[在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

### API 调优

通过 DashScope API（HTTP）方式完成调优全流程，主要步骤为：上传调优文件 -> 创建调优任务 -> 查询任务状态 -> 部署模型 -> 调用模型。API 方式创建的任务仅支持按 Token 计费。完整 API 示例见[使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。

## 训练数据格式

### SFT 训练集

采用 ChatML 格式的 JSONL 文件，每行一个对话样本：

```json
{"messages": [
  {"role": "system", "content": "系统输入"},
  {"role": "user", "content": "用户输入"},
  {"role": "assistant", "content": "期望的模型输出"}
]}
```

思考模型（Thinking）的训练数据需在最后一个 assistant 输出中使用 `<think>` 标签包裹思考内容。

### DPO 训练集

在 messages 基础上额外提供 `chosen`（正样本）和 `rejected`（负样本）：

```json
{"messages": [...],
 "chosen": {"role": "assistant", "content": "赞同的输出"},
 "rejected": {"role": "assistant", "content": "反对的输出"}}
```

### CPT 训练集

纯文本格式，每行一条：`{"text": "文本内容"}`。

## 关键超参数

| 参数 | 推荐设置 | 说明 |
|------|---------|------|
| batch_size | 使用默认值 | 模型更新参数的数据步长 |
| learning_rate | 高效训练 1e-4 量级，全参训练 1e-5 量级 | 控制权重修正强度 |
| n_epochs | 数据量 < 10000 时 3-5 次，> 10000 时 1-2 次 | 训练遍历次数 |
| max_length | 设为模型支持的最大值 | 单条数据最大 token 长度 |
| lora_rank | 设为模型支持的最大值 | LoRA 低秩矩阵的秩，越大效果越好 |

## 计费说明

训练费用按消耗的 Token 数计费，公式为：`费用 = (训练数据 Token 总数 + 混合训练数据 Token 总数) x 循环次数 x 训练单价`。不同模型的训练单价不同，例如 Qwen3-8B 为 0.006 元/千 Token，Qwen2.5-72B-Instruct 为 0.15 元/千 Token。调优后的模型需要部署后才能使用，部署也会产生额外费用。

## 限制与注意事项

- 所有文本生成模型调优功能仅适用于华北 2（北京）地域。
- 模型调优通常作为优化模型表现的"最后手段"，建议先尝试 [Prompt 工程](../concepts/prompt-engineering.md)和插件调用。
- 训练耗时较长（数小时到数十小时），且调优后模型需部署才能使用，部署费用较高。
- 使用阿里云子账号（RAM 用户）需授予模型调用、训练和部署权限。
- CosyVoice 调优产物为单音色模型，不支持音色切换和指令控制，训练数据应为同一发音人。
- 视频/图像生成模型仅支持 SFT-LoRA 高效微调方式。

> **注意**：通过 API 创建的训练任务仅支持按 Token 计费，不支持使用模型训练单元（预付费或后付费）。如需使用训练单元，请通过控制台创建任务。

## 安全合规调优

百炼支持通过 SFT 微调强化模型的安全合规能力。通过构建覆盖政治安全、历史认知、社会伦理等维度的训练数据集，使模型在面对敏感请求时主动拒绝并提供正面引导。具体方案和实验数据见[0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)。

## 来源文档

- [微调视频生成模型](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)
- [模型调优简介](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)
- [在控制台进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)
- [0 代码强化大模型安全合规能力](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/enhance-the-security-compliance-of-large-models.md)
- [CosyVoice模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)
- [使用 API 或命令行进行模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)
- [微调图像生成模型](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)


