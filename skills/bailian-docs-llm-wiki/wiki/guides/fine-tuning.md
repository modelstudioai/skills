# fine tuning

fine tuning 是指在百炼平台上基于预训练模型，使用自有数据对模型进行增量训练以适配特定任务或领域的能力。它支持文本生成、图像/视频生成、语音合成等多种模态，适用于业务逻辑定制、风格迁移、领域知识注入等场景。所有 fine tuning 操作均通过 API 或控制台提交训练任务，训练完成后生成专属模型版本供推理调用。

## 支持的模型与功能

当前支持 fine tuning 的模型类型包括：
- 文本生成类（如 Qwen 系列）：支持指令微调、SFT、LoRA 等方式，详见 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)；
- 图像生成模型（WanImage）：支持 ControlNet 微调、Prompt-aware 微调等，参见 [图像生成模型调优](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)；
- 视频与语音模型：分别提供时序建模适配和声学特征对齐能力，具体配置参考 [视频生成模型调优](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md) 和 [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)；
- 决策与强化学习类：支持 RLHF、PPO、在线策略蒸馏（OPD）及决策模型专用微调流程，详见 [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md) 与 [在线策略蒸馏](../../raw/model-user-guide/fine-tuning/opd-overview.md)。

> **注意**：[决策模型微调](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md) 中描述的“全参数微调为默认模式”与最新 API 文档中默认启用 LoRA 的行为不一致；实际调用时请以 `lora_rank` 参数显式指定为准，避免因隐式默认值导致训练失败。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 基座模型 ID（如 `qwen-max`），需在 [模型调优](../../raw/model-user-guide/fine-tuning.md) 列表中确认是否支持 fine tuning |
| `training_data` | string (OSS URI) | 是 | 训练数据集路径，格式为 `oss://bucket-name/path/to/data.jsonl`，每行须为标准 fine tuning 格式（如 text2text 或 instruction JSON） |
| `lora_rank` | integer | 否 | LoRA 秩，默认为 8；设为 0 表示全参数微调（仅部分模型支持） |
| `learning_rate` | float | 否 | 学习率，默认 `2e-5`；图像/视频模型建议调低至 `1e-6`～`5e-6` |

## 使用方式

1. 准备符合格式要求的训练数据（参考各模态文档中的 schema 示例）；
2. 调用 `POST /v1/fine_tunes` 接口提交任务，或在控制台「模型调优」页选择对应模型并上传数据；
3. 监控训练状态（`pending` → `running` → `succeeded`/`failed`），成功后获得 `fine_tuned_model_id`；
4. 使用该 ID 调用 `/v1/chat/completions` 等推理接口，无需额外配置。

## 限制和注意事项

- 单次训练最大数据量：文本类 ≤ 10M tokens，图像类 ≤ 5,000 张（分辨率 ≤ 1024×1024），视频类 ≤ 200 个 clip（总时长 ≤ 30 分钟）；
- 训练任务最长运行时间：72 小时，超时自动终止；
- 所有 fine tuning 任务均隔离运行，不共享基座模型权重，但需确保 `model_id` 与训练数据模态匹配（例如不可用文本模型训练图像数据）；
- 免费额度仅覆盖基础 LoRA 微调；全参数微调、RLHF、OPD 等高级模式需开通企业版权限，详情见 [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md) 和 [在线策略蒸馏](../../raw/model-user-guide/fine-tuning/opd-overview.md)。

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


