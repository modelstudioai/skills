# model production

百炼平台提供完整的模型生产 API，覆盖从微调训练到压缩优化再到上线部署的全流程。开发者可以通过这组 API 将基础模型定制为业务专属模型，并以在线服务的形式对外提供推理能力。

## 核心能力

模型生产流程包含三个关键环节，各环节均提供独立的 API 接口：

### 模型调优

通过微调训练对基础模型进行定制，生成适配特定业务场景的专属模型。详细的接口说明与参数定义请参考 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)。

### 模型压缩

对训练完成的模型进行量化等压缩处理，在保持模型效果的前提下降低推理成本、提升推理速度。具体的压缩策略与 API 用法请参考 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。

### 模型部署

将微调或导入的模型部署为在线推理服务，使其可通过标准 API 进行调用。部署相关的配置与管理接口请参考 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 典型工作流

一个完整的模型生产流程通常如下：

1. **准备训练数据** — 按平台要求整理并上传微调数据集。
2. **创建调优任务** — 调用模型调优 API 提交微调训练任务，等待训练完成。
3. **压缩模型（可选）** — 对训练产出的模型进行量化压缩，降低部署资源消耗。
4. **部署模型** — 将最终模型部署为在线服务，获取推理端点。
5. **调用推理** — 通过部署生成的端点进行在线推理。

## 注意事项

- 模型调优、压缩和部署为异步操作，提交任务后需轮询或通过回调获取任务状态。
- 部署的模型会持续占用计算资源，不再使用时应及时下线以避免不必要的费用。
- 并非所有基础模型都支持压缩，使用前请确认模型兼容性。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)




