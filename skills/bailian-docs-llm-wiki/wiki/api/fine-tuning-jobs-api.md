# [fine tuning](../guides/fine-tuning.md) jobs api

百炼平台提供模型调优（Fine-tuning）API，允许开发者通过微调训练定制专属模型，以满足特定业务场景的需求。该 API 遵循 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)规范，支持对基础模型进行增量训练，从而提升模型在垂直领域的表现。详细说明参见 [模型调优](../../raw/model-api-reference/fine-tuning-jobs-api.md)。

## 功能概述

Fine-tuning Jobs API 的核心能力是通过提交训练数据对已有基础模型进行微调，生成适配具体任务的定制模型。根据 [模型调优](../../raw/model-api-reference/fine-tuning-jobs-api.md) 文档，主要流程包括：

- **创建微调任务**：指定基础模型、训练数据文件和超参数，提交微调训练作业
- **查询任务状态**：获取微调任务的运行状态、进度和训练指标
- **管理微调模型**：列出已完成的微调模型，用于后续推理调用

## 使用方式

开发者可通过 HTTP API 或 SDK 调用 Fine-tuning Jobs 接口。典型流程为：

1. 准备符合格式要求的训练数据（通常为 JSONL 格式）
2. 通过 Files API 上传训练数据文件
3. 调用 Fine-tuning Jobs API 创建微调任务，指定模型和训练参数
4. 轮询或通过回调获取任务完成状态
5. 使用微调后的模型 ID 进行推理调用

具体的接口参数和调用示例请参考 [模型调优](../../raw/model-api-reference/fine-tuning-jobs-api.md) 原始文档。

## 注意事项

- 微调训练的时长和费用取决于训练数据量、模型规模及超参数配置
- 训练数据的质量直接影响微调效果，建议使用高质量、与目标任务匹配的标注数据
- 不同基础模型对微调的支持程度和参数要求可能不同，请以平台实际支持的模型列表为准

## 来源文档

- [模型调优](../../raw/model-api-reference/fine-tuning-jobs-api.md)



