# fine tuning

fine tuning 是指在百炼平台上基于预训练大模型，使用用户自有数据进行增量训练以适配特定任务的过程。它支持文本生成、图像/视频生成、语音合成等多种模态，适用于领域适配、风格迁移、指令对齐等场景。所有 fine tuning 任务均通过 API 或控制台提交，训练完成后生成专属模型版本供推理调用。

## 支持的模型与功能

当前支持 fine tuning 的模型类型包括：  
- 文本生成类（如 Qwen 系列）：支持监督微调（SFT），详见 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)；  
- 图像生成模型（WanImage）：支持 LoRA 微调与全参数微调，参见 [图像生成模型调优](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)；  
- 视频与语音模型：分别提供专用微调流程，具体请查阅 [视频生成模型调优](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md) 和 [语音合成模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model.md)。  
强化学习（RL）、在线策略蒸馏（OPD）及决策模型微调属于高级调优范式，仅对白名单用户开放，其原理与接口规范见 [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md) 和 [决策模型微调](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

## 关键参数

- `base_model`: 必填，指定基础模型 ID（如 `qwen2-7b-instruct`），需与训练数据模态匹配；  
- `training_dataset`: 必填，OSS 路径或数据集 ID，格式须符合对应任务要求（如文本微调需为 JSONL，每行含 `prompt` 和 `completion` 字段）；  
- `learning_rate`, `num_epochs`, `batch_size`: 可选，若未指定则采用平台默认值（默认学习率依模型规模动态缩放）；  
- `lora_rank` / `lora_alpha`: 仅 LoRA 微调有效，用于控制低秩适配器维度；  
- `enable_gradient_checkpointing`: 建议开启以降低显存占用，尤其在长上下文训练中。

## 使用方式

1. 准备标注数据并上传至 OSS，确保路径可被百炼服务访问；  
2. 调用 `POST /v1/fine_tunes` 接口，传入参数（参考 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md) 中的请求示例）；  
3. 轮询 `GET /v1/fine_tunes/{fine_tune_id}` 获取状态，`status: succeeded` 表示完成；  
4. 使用返回的 `model_id` 进行推理，例如 `qwen2-7b-instruct-ft-abc123`。

## 限制和注意事项

- 单次训练最大时长为 72 小时，超时自动终止；  
- 文本微调数据集上限为 100 万 token（按 base model tokenizer 统计），图像/视频数据集按文件数与总大小双重限制；  
- 所有 fine tuning 任务不支持跨地域训练（即 OSS Bucket 必须与训练集群同 Region）；  
> **注意**：原始文档中 [强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md) 提到“支持 PPO 在线更新”，但当前 API 实际仅支持离线 RLHF 流程（即 reward modeling + SFT + PPO 离线训练三阶段），在线策略更新尚未开放。  
> **注意**：[在线策略蒸馏](../../raw/model-user-guide/fine-tuning/opd-overview.md) 文档描述的实时蒸馏能力仍处于内测阶段，公开 API 暂不提供 `opd_enabled` 参数，调用将返回 400 错误。  
- 微调后模型不继承原模型的系统提示（system [prompt](prompt.md)）行为，需在推理时显式传入 `system` 字段。

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


