# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、文件与数据管理，以及售后响应机制等核心环节。该支持体系面向生产环境需求设计，强调可配置性、可观测性和边界清晰的服务范围。所有功能均需通过百炼控制台或标准 API 调用启用，不依赖前端渲染逻辑。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合 TopN 结果，适用于问答系统、客户服务、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **结构化数据导入**：支持 Excel/CSV 等格式结构化数据导入，但存在空行截断策略（首行为空则视为无效文件）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持 `stream=True` 全量[流式输出](../concepts/streaming-output.md)；如需增量式（即仅返回本次新增 token），须显式设置 `incremental_output=True`。

> **注意**：文档 1 中第 4 条称 “Agent 和 Assistant API 的最大区别是用户可自行开发插件模型”，但该描述未定义“插件模型”具体指代（是自定义 LLM 还是插件编排逻辑？）。当前平台实际不支持用户替换底层推理模型，仅支持插件调用与 RAG 配置。此条表述易引发歧义，应以控制台实际能力为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否，默认 `False` |
| `incremental_output` | bool | 在 `stream=True` 下启用增量 token 输出（避免重复返回历史内容） | 否，默认 `False` |
| `MD5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |
| `authorization` | string | 自定义插件调用时唯一允许透传的 Header 字段 | 是（其他 Header 将被丢弃） |

## 使用方式

- **插件调用**：通过 Assistant API 提交带 `tools` 定义的请求，模型自动选择并填充参数；自定义插件需符合 OpenAPI 3.0 协议，且仅支持 `authorization` Header 透传。  
- **RAG 测试优化**：若检索结果不准确，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：PDF 文件后缀必须为小写 `pdf`，否则返回错误码 `140010`；单业务空间上限 10 万文档，超限时需提交工单扩容。  
- **售后接入**：7×24 小时支持通过电话（95187）、阿里云 APP 或标准工单获取；基础服务覆盖 API 故障诊断、SDK 使用、控制台问题等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件 Header 限制**：自定义插件调用**不支持透传任意自定义 Header**，仅 `Authorization` 字段有效；其他字段（如 `X-User-ID`、`X-Tenant`）将被服务端静默忽略。  
- **第三方工具责任边界**：阿里云仅对百炼服务端（API 可用性、计费记录、SDK 示例）提供支持；第三方工具（如 Cursor、Windsurf）的安装、配置、本地网络/代理/防火墙问题等，不在售后范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须接受《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需遵守对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **Markdown 渲染**：模型输出中的 `**text**` 等 Markdown 语法需由前端自行解析渲染，百炼 API 不做 HTML 转义或富文本转换。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


