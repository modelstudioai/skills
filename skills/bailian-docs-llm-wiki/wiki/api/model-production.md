# model production

模型生产（model production）涵盖百炼平台上从定制模型到上线服务的完整链路：先通过微调训练得到专属模型，再将其部署为在线推理服务。本页汇总 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 与 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 两个 API 的核心信息，帮助开发者快速打通"调优 → 部署 → 调用"的流程。

## 能力概览

| 环节 | 能力 | 对应文档 |
| --- | --- | --- |
| 模型调优 | 通过微调（fine-tuning）训练定制专属模型 | [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) |
| 模型部署 | 将微调产出的模型或外部导入的模型部署为在线推理服务 | [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) |

## 典型使用流程

1. **准备并提交微调任务**：按照 [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md) 中的接口创建微调训练任务，产出定制模型。
2. **部署为在线服务**：微调完成后（或已有导入的模型），按 [模型部署](../../raw/model-api-reference/model-production/deployments-api.md) 中的接口将模型部署为在线推理服务。
3. **调用推理服务**：部署成功后，即可通过在线推理接口以部署得到的模型/服务标识发起调用。

## 支持的模型来源

部署环节支持两类模型来源：

- **微调产出的模型**：由模型调优（fine-tuning）任务训练得到的专属模型。
- **导入的模型**：从外部导入到平台的模型。

## 限制和注意事项

- 微调与部署是两个独立步骤：微调完成不代表模型可直接调用，必须先完成部署才能提供在线推理服务。
- 部署会占用推理资源，实际的计费方式、算力规格与配额请以对应 API 文档和控制台展示为准。

> **注意**：当前两篇原始文档内容较为简略，仅给出能力定位，未包含具体的请求参数、返回结构与错误码。集成前请以最新版 API 参考为准，避免依赖过时字段。

## 来源文档

- [模型调优](../../raw/model-api-reference/model-production/fine-tuning-jobs-api.md)
- [模型部署](../../raw/model-api-reference/model-production/deployments-api.md)


