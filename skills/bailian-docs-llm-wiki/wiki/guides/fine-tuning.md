# fine tuning

fine tuning 是指在百炼平台上基于预训练大模型，使用用户自有数据进行增量训练以适配特定任务或领域的能力。该功能支持文本生成、图像/视频生成、语音合成、强化学习、知识蒸馏及决策建模等多种范式，适用于需要定制化模型行为的生产场景。所有 fine tuning 任务均通过 API 或控制台提交，训练完成后生成专属模型 ID 可直接部署调用。

## 支持的模型与功能

当前支持 fine tuning 的模型类型包括：  
- 文本生成类（如 Qwen 系列）：支持指令微调、SFT 和 LoRA；详见 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)  
- [多模态](../concepts/multi-modal.md)生成类：图像生成（WanImage）、视频生成（WanVideo）和语音合成（TTS）模型均提供专用 fine tuning 流程；参考 [图像生成模型调优](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 和 [视频生成模型调优](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)  
- 决策与优化类：支持决策模型微调及 OPD 蒸馏训练；[决策模型微调](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md) 文档说明了状态-动作对齐等关键约束  

> **注意**：强化学习（RL）fine tuning 当前仅限白名单客户申请使用，且不支持通用 API 提交；[强化学习](../../raw/model-user-guide/fine-tuning/rl-overview/rl-training-overview.md) 文档中描述的 `rlhf` 接口已下线，实际应使用 `rl-train` 新接口（参见控制台最新 API 文档）。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 基座模型 ID（如 `qwen2-7b-instruct`），需从 [支持的基座模型列表](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md) 中选取 |
| `training_dataset` | string (OSS URI) | 是 | 训练数据集路径，格式为 `oss://bucket-name/path/to/data.jsonl`，必须为 JSONL 格式且字段名与基座模型要求一致 |
| `method` | string | 否 | 微调方法，默认 `lora`；可选 `full`（全参数）、`qlora`；`opd` 仅适用于 OPD 蒸馏场景 |
| `learning_rate` | float | 否 | 默认 `2e-5`；文本生成建议范围 `1e-5 ~ 5e-5`，图像生成需按 [图像生成模型调优](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 调整 |

## 使用方式

1. **准备数据**：按目标模型要求构造 JSONL 文件（例如文本生成需含 `prompt`/`response` 字段，图像生成需含 `image_url` 和 `caption`）  
2. **上传至 OSS**：确保 bucket 权限可被百炼服务读取  
3. **发起训练**：调用 `POST /v1/fine-tunes` API 或在控制台「模型调优」页填写表单  
4. **监控与验证**：通过 `GET /v1/fine-tunes/{job_id}` 查询状态；训练完成后使用 `model_id` 调用 `/v1/chat/completions` 进行推理验证  

## 限制和注意事项

- 单次训练最大时长：文本类 ≤ 72 小时，图像/视频类 ≤ 168 小时（超时自动终止）  
- 数据集大小限制：文本 ≤ 10 GB，图像/视频 ≤ 500 GB（需压缩为 ZIP 并索引）  
- LoRA 微调不支持跨架构迁移（例如不能用 Qwen 基座微调 Llama 格式权重）  
- 所有 fine tuning 任务均需显式声明 `region`，且训练与推理 region 必须一致；该约束在 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md) 中未明确强调，但实测不一致将导致加载失败  
- OPD 蒸馏训练要求教师模型与学生模型 tokenization 完全一致，否则会静默跳过 loss 计算——此行为与 [OPD 蒸馏训练](../../raw/model-user-guide/fine-tuning/opd-overview/opd-training-overview.md) 文档中“自动对齐 tokenizer”的描述矛盾，以实际运行日志为准

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


