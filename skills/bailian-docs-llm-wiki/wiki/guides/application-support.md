# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。该支持体系面向生产环境设计，聚焦可落地的配置项与明确的责任边界。具体能力与限制详见下文。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按用户配置的排序策略（如语义相似度）选取 topN 结果后融合生成，广泛应用于问答系统、客户服务、教育与内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token，而非全量重传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持基于 OpenAPI 规范注册的自定义 API 插件，大模型可理解其参数结构并自主调用；但**不支持透传除 `Authorization` 外的任意 HTTP Header**，该限制已在实际调用中验证 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可以提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类型、抽象接口或配置模板），且文档 2 和 3 均未提及该表述；该描述缺乏上下文支撑，建议以控制台实际配置项和 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的服务边界为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式 token 输出（避免重复返回历史内容） | 否（默认 `False`） |
| `MD5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |

## 使用方式

- **插件调用**：在智能体（Agent）配置中启用对应插件，自定义插件需完成 OpenAPI Schema 注册并通过审核；调用时由模型自动解析参数并构造请求。  
- **RAG 配置**：在应用编辑页绑定知识库，设置检索权重、topK、重排策略等；测试时若结果不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；上传前需计算并传入 `MD5` 值校验完整性。  
- **售后支持入口**：7×24 小时支持通过官网、电话（95187）、阿里云 APP 或标准工单获取；基础服务覆盖 API/SDK 故障诊断、控制台问题、计费咨询等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件 Header 限制**：自定义插件仅允许透传 `Authorization` Header，其他 Header（如 `X-User-ID`、`X-Tenant` 等）将被丢弃，不可用于身份或上下文透传。  
- **文件数量上限**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具责任边界**：阿里云仅对百炼服务端（API、计费、控制台）负责；第三方工具（如 Cursor、Windsurf）的部署、配置、兼容性及本地环境（代理、防火墙、内网）问题不在支持范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需符合对应 [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


