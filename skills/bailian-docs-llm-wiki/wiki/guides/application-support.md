# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。该支持体系面向生产环境设计，强调可配置性、可观测性和边界清晰的服务范围。所有功能均需通过百炼控制台或标准 API 接入，不提供运行时代码级干预能力。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按用户配置的排序策略（如语义相似度）选取 topN 结果后融合生成；适用于问答系统、客户服务、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：支持 `stream=True` 全量[流式输出](../concepts/streaming-output.md)；若需逐 token 增量返回（避免重复渲染），须显式设置 `incremental_output=True` [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过 OpenAPI 协议注册函数，模型可理解参数结构并调用；但**仅支持透传 `Authorization` header，不支持其他自定义 header**（如 `X-User-ID` 等）。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类型、配置类或抽象接口类）；当前 SDK 文档中无对应概念，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的 API 和 SDK 支持范围为准，避免依赖模糊表述。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `stream` | bool | 否 | 设为 `True` 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） |
| `incremental_output` | bool | 否 | 仅当 `stream=True` 时生效；设为 `True` 表示增量式流式（每次返回新增内容，非全量重传） |
| `MD5` | string | 是（文件上传） | 用于校验上传文件完整性，必须为小写十六进制字符串，且文件后缀需与实际格式一致（如 PDF 文件后缀必须为 `.pdf`） |

## 使用方式

- 插件调用：通过 `tools` 字段声明插件列表，由模型自主决策是否调用及传参；自定义插件需符合 OpenAPI 3.0 规范并完成鉴权注册。  
- RAG 配置：在应用编辑页绑定知识库，设置检索权重、分块策略与重排模型；测试时若结果不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单。  
- 流式消费：客户端需按 SSE（Server-Sent Events）协议解析响应体，对 `incremental_output=True` 的响应，应累积处理 `delta` 字段而非 `message` 全量字段。  
- 文件上传：仅支持 `.pdf`、`.doc`、`.docx`（注意后缀小写），单业务空间上限 10 万文档；超限时需提交工单申请扩容。

## 限制和注意事项

- **Header 限制**：调用自定义插件时，仅 `Authorization` header 可被透传至目标服务端；其他 header 将被丢弃，不可用于身份上下文传递。  
- **数据导入限制**：结构化数据（如 Excel）导入时，空行将导致后续行被截断；首行为空则整份数据被判定为空文件。  
- **第三方工具支持边界**：阿里云仅保障百炼服务端 API 可用性、计费一致性及基础连通性（如 curl 测试）；**不支持 Cursor/Windsurf 等第三方 AI 工具的部署、配置、调试或本地环境（代理/防火墙/OS）问题排查** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需额外遵循其对应许可证条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


