# fine tuning

fine tuning 是指在百炼平台提供的预训练大模型基础上，使用用户自有数据进行增量训练，以适配特定任务或领域。该能力支持文本生成、图像生成、视频生成和语音合成等[多模态](../concepts/multi-modal.md)模型，适用于需要定制化输出效果的场景。所有 fine tuning 任务均通过平台 API 或控制台提交，训练完成后生成专属模型版本供推理调用。

## 支持的模型与功能

当前支持 fine tuning 的模型类型包括：
- 文本生成模型（如 Qwen 系列）：支持指令微调（SFT）、LoRA 等轻量适配方式；
- 图像生成模型（如 WanImage）：支持基于 ControlNet 或 DreamBooth 风格的定制化图像生成；
- 视频生成模型（如 WanVideo）：支持短时序视频的风格/主体微调；
- 语音合成模型（如 Tongyi Tingwu TTS）：支持音色克隆与语调适配。

> **注意**：强化学习（RL）训练虽在 [模型调优](../../raw/model-user-guide/fine-tuning.md) 文档中列为子项，但其技术路径、API 接口与标准 supervised fine tuning 完全不同，不共享训练配置参数，也不支持导出为常规推理模型——实际使用中应视为独立训练范式，详见 [原文标题](../../raw/model-user-guide/fine-tuning.md)。

## 关键参数

启动 fine tuning 任务需指定以下核心参数：
- `base_model`: 基座模型 ID（如 `qwen2-7b-instruct`），必须为平台支持的可微调模型；
- `training_dataset`: 训练数据集 ID，格式需符合对应任务类型要求（如文本任务需为 JSONL，每行含 `prompt` 和 `response` 字段）；
- `method`: 微调方法，可选 `full`, `lora`, `qlora`（仅部分模型支持）；
- `epochs`, `learning_rate`, `batch_size`: 控制训练强度，平台对不同 base_model 设有默认值与上下限；
- `output_model_name`: 输出模型唯一标识，用于后续部署。

参数约束与默认值请严格参照 [原文标题](../../raw/model-user-guide/fine-tuning.md) 中各模型类型的配置说明，避免因超限导致任务失败。

## 使用方式

1. **准备数据**：按任务类型整理训练数据，上传至百炼数据集管理模块并获取 dataset ID；  
2. **创建训练任务**：调用 `POST /api/v1/fine-tuning/jobs` 接口，传入上述关键参数（或通过控制台表单提交）；  
3. **监控与验证**：任务状态可通过 `GET /api/v1/fine-tuning/jobs/{job_id}` 查询，训练完成后系统自动评估 loss 曲线与样本生成质量；  
4. **部署模型**：任务成功后，使用返回的 `model_id` 调用 `/v1/models/{model_id}/chat/completions` 等标准推理接口。

完整流程示例与 SDK 调用代码见 [原文标题](../../raw/model-user-guide/fine-tuning.md)。

## 限制和注意事项

- 单次训练最大时长为 72 小时，超时自动终止；
- 文本类 LoRA 微调支持最大 rank=64，QLoRA 仅支持 `qwen2-1.5b` 及以上基座；
- 图像/视频微调暂不支持自定义 backbone，仅允许调整 adapter 层与 conditioning 输入；
- 所有 fine tuning 产出模型仅限创建者账号内使用，不支持跨账号共享或导出权重文件；
- 数据隐私：训练数据不会用于平台模型迭代，但需确保数据版权合规——此政策依据见 [原文标题](../../raw/model-user-guide/fine-tuning.md)。

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)



