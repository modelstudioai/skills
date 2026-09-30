# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 知识增强、[流式输出](../concepts/streaming.md)、API 调用规范及售后响应机制等核心环节。其目标是保障应用功能正确性、调用稳定性与问题可追溯性。所有支持行为均以阿里云百炼服务协议为法律基础，并受制于平台当前能力边界与计费策略。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（[检索增强生成](../concepts/rag.md)）**：支持多知识库并行检索，按配置得分选取 topN 结果后融合生成；适用于问答系统、客服对话、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming.md)**：支持两种模式：`stream=True`（全量流式）与 `incremental_output=True`（增量式流式），后者可避免重复渲染历史内容。  
- **自定义插件**：支持通过标准 OpenAPI 协议接入，模型可理解参数结构并自主编排调用逻辑；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”指代 SDK 类型、API 分组还是抽象能力模型；该表述缺乏上下文与示例，易引发歧义，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确列出的 API 与 SDK 支持范围为准。

## 关键参数

| 参数名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| `stream` | bool | 启用流式响应（逐 token 返回） | 否（默认 `False`） |
| `incremental_output` | bool | 启用增量式流式（仅返回新增 token，非全量重发） | 否（需 `stream=True` 时生效） |
| `MD5` | string | 文件上传时用于校验完整性的哈希值，见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节 | 是（文件导入必填） |

## 使用方式

- **插件调用**：在智能体（Agent）配置中启用对应插件，或通过 Assistant API 的 `tools` 字段声明函数 schema；自定义插件需符合 OpenAPI 3.0 规范并完成鉴权注册。  
- **RAG 配置**：在应用编辑页绑定知识库，设置检索权重、topK、重排序策略；测试时若结果不准，应复制 `RequestId` 提交工单反馈 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式消费**：客户端需按 SSE（Server-Sent Events）协议解析 `data:` 块，对 `incremental_output=True` 响应需自行维护上下文状态以拼接完整语义。  
- **文件上传**：仅支持小写后缀的 `pdf`/`doc`/`docx`；空行将导致后续结构化数据被截断，须预处理清洗 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **插件限制**：自定义插件无法透传除 `Authorization` 外的任何 HTTP Header；非官方插件的稳定性、安全性及兼容性由用户自行负责。  
- **知识库容量**：单业务空间上限为 10 万文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后边界**：阿里云百炼仅保障自身服务端可用性、API 行为一致性及计费准确性；第三方工具（如 Cursor、Windsurf）、本地网络环境、业务代码实现等问题不在基础售后范围内，详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型调用还需符合对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


