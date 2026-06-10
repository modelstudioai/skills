# deployments api

百炼平台提供模型部署 API（Deployments API），用于将微调或导入的模型发布为在线推理服务。部署完成后，应用即可通过推理接口调用该模型。

## 功能定位

模型部署是连接"模型资产"与"在线推理"的桥梁。开发者通过 [模型部署](../../raw/model-api-reference/deployments-api.md) 创建部署任务后，会得到一个可被推理接口寻址的 endpoint。

核心用途：

- 将微调产出的模型版本发布为在线服务
- 将导入的自定义模型部署为可调用服务

## 使用方式

典型流程为：准备模型 → 调用部署 API 创建部署任务 → 等待实例就绪 → 发起推理调用。

详细的 API 字段、请求示例与错误码说明请参见 [模型部署](../../raw/model-api-reference/deployments-api.md) 原始文档。

> **注意**：当前 [模型部署](../../raw/model-api-reference/deployments-api.md) 源文档仅给出功能入口的一句话说明，尚未包含完整的接口参数、规格选项与调用示例，建议结合百炼控制台与官方 API 参考获取完整信息。

## 来源文档

- [模型部署](../../raw/model-api-reference/deployments-api.md)


