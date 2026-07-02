# model production

百炼平台提供模型生产（model production）相关的 API，覆盖从模型调优、模型压缩到[模型部署](../concepts/model-deployment.md)的完整链路。开发者可以通过这些接口对基础模型进行微调定制、压缩优化以及部署上线，形成端到端的模型生产能力。

## 能力概览

模型生产链路由三个相互衔接的环节组成：

1. **模型调优（Fine-tuning）**：通过微调训练在基础模型上注入领域知识或特定任务能力，定制出专属模型。
2. **模型压缩（Compression）**：通过量化等手段压缩模型体积，降低推理时的资源占用与调用成本。
3. **[模型部署](../concepts/model-deployment.md)（Deployment）**：将微调或导入的[模型部署](../concepts/model-deployment.md)为在线推理服务，供应用调用。

三者构成典型的「调优 → 压缩 → 部署」流水线，详见 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 与 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)。

## 支持的能力

- **微调训练**：基于平台支持的基础模型发起调优任务，产出定制模型产物。
- **模型压缩**：对已有模型执行量化等压缩操作，在精度可接受范围内换取更低的推理成本，参见 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)。
- **在线部署**：将微调或导入的模型发布为可调用的推理服务。

## 使用方式

典型的模型生产流程如下：

1. 选定基础模型，调用模型调优 API 创建 fine-tuning 任务，等待训练完成获得定制模型。
2. 如需降低成本，对定制模型调用模型压缩 API 执行量化压缩。
3. 调用模型部署 API，将最终模型部署为在线推理服务，获取可调用的接入点。

## 限制和注意事项

- 调优、压缩、部署三类任务的耗时与资源消耗差异较大，建议关注各接口的异步任务状态轮询机制。
- 压缩会带来精度损失，部署前应结合业务验收结果决定是否启用压缩环节。
- 部署后的推理服务需关注并发与配额限制，具体上限以部署接口返回为准。

> **注意**：当前各原始文档仅给出能力的一句话概述，具体支持的模型清单、参数字段与接口细节请以平台控制台和对应 API 参考文档的实时信息为准。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型压缩](../../raw/model-api-reference/model-production/model-compression-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)






