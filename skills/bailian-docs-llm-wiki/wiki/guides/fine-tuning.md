# fine tuning

fine tuning 是指在百炼平台上基于预训练模型，使用用户自有数据进行增量训练以适配特定任务或领域的过程。它支持文本生成、图像/视频生成、语音合成等多种模态，适用于业务场景定制、性能优化和知识注入等需求。所有 fine tuning 功能均通过 API 或控制台统一接入，训练结果可直接部署为专属模型服务。

## 支持的模型与功能

当前支持 fine tuning 的模型类型包括：  
- 文本生成类（如 Qwen 系列）：支持指令微调、SFT、LoRA 等方式，详见 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)；  
- 多模态生成类：图像生成（WanImage）、视频生成（WanVideo）及语音合成（TTS）模型均提供专用 fine tuning 流程，分别参见 [图像生成模型调优](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 和 [视频生成模型调优](../../raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)；  
- 决策与强化学习类：支持决策模型微调、在线策略蒸馏（OPD）及强化学习（RL）训练范式，相关说明见 [决策模型微调](../../raw/model-user-guide/fine-tuning/decision-model-tuning-guide.md)。

> **注意**：[强化学习](../../raw/model-user-guide/fine-tuning/rl-overview.md) 文档中提及的 PPO 训练流程目前仅对白名单客户开放，而 [在线策略蒸馏](../../raw/model-user-guide/fine-tuning/opd-overview.md) 文档未明确标注该限制，实际调用前请确认权限状态。

## 关键参数

- `base_model`: 必填，指定基础模型 ID（如 `qwen-max-20240815`），需与目标任务类型匹配；  
- `training_type`: 可选 `full`, `lora`, `qlora`，其中 `lora` 为默认值，兼顾效率与效果；  
- `learning_rate`, `epochs`, `batch_size`: 均支持自定义，但部分模型（如 WanVideo）对 `batch_size` 有硬性上限，具体约束见对应文档；  
- `validation_split`: 默认 0.1，用于自动划分验证集，若提供独立验证集则忽略此参数。

## 使用方式

1. 准备符合格式要求的训练数据（JSONL 格式，字段名依任务而异，例如文本生成需含 `prompt` 和 `response` 字段）；  
2. 调用 `/v1/fine_tuning/jobs` 创建训练任务，传入参数及数据集 URL（OSS 或 HTTPS）；  
3. 监控任务状态（`pending` → `running` → `succeeded`/`failed`），成功后获取 `model_id`；  
4. 使用该 `model_id` 调用推理 API，或在控制台发布为服务。完整操作示例见 [千问模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model.md)。

## 限制和注意事项

- 单次训练最大时长为 72 小时，超时将自动终止；  
- 数据集大小上限为 100 GB（压缩后），且必须为 UTF-8 编码；  
- LoRA 微调不支持跨架构迁移（如从 Qwen2 切换至 Qwen3 基座时需重新全量微调）；  
- 图像/视频类 fine tuning 不支持自定义 backbone，仅允许调整 head 层与条件控制模块，细节参见 [图像生成模型调优](../../raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)。

## 来源文档

- [模型调优](../../raw/model-user-guide/fine-tuning.md)


