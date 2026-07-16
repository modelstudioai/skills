# model production

百炼平台提供模型生产相关的 API，覆盖从模型微调训练到部署上线的完整流程。开发者可以通过[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)接口定制专属模型，再通过[模型部署](../../raw/model-api-reference/model-production/deployments-api.md)接口将其发布为在线推理服务。

## 模型调优

模型调优（Fine-tuning）允许开发者通过微调训练定制专属模型，以适配特定业务场景。调优流程通常包括：

- **创建调优任务**：指定基础模型、训练数据集和超参数，提交微调训练任务
- **查询任务状态**：轮询或监听训练任务进度，获取训练指标
- **管理调优产物**：训练完成后获取调优模型，用于后续部署或评估

详细的接口定义和参数说明请参考[模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)文档。

## 模型部署

模型部署将微调或导入的模型发布为在线推理服务，使其可通过 API 调用进行推理。部署流程通常包括：

- **创建部署**：选择调优完成的模型或外部导入的模型，配置推理资源和服务参数
- **管理部署实例**：查看部署状态、调整资源配置、启停服务
- **调用推理服务**：部署成功后，通过标准 API 端点发送推理请求

详细的接口定义和参数说明请参考[模型部署](../../raw/model-api-reference/model-production/deployments-api.md)文档。

## 典型工作流

1. 准备训练数据集
2. 通过调优 API 提交微调训务，等待训练完成
3. 通过部署 API 将调优产物部署为在线服务
4. 调用部署后的模型端点进行推理

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)











