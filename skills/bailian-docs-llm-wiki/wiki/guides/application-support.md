# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖模型调用、插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)等核心功能的使用支持，以及售后响应范围与服务边界说明。该支持体系面向生产环境开发者，聚焦可落地的技术细节与限制约束，不包含业务逻辑定制或第三方工具深度运维。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索，按配置策略打分后选取 topN 结果；适用于问答系统、客服对话、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用[流式输出](../concepts/streaming-output.md)；进一步设置 `incremental_output=True` 可实现增量式流式响应（即每次返回新片段而非全量重传） [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持基于 OpenAPI 规范注册的自定义 API 插件，大模型可理解其参数结构并自主调用；但**仅支持透传 `Authorization` header，不支持其他自定义 header**（如 `X-Api-Key` 等）> **注意**：文档 1 第10条明确声明“不支持自定义header，仅支持authorization”，而部分旧版 SDK 示例曾暗示更宽松的 header 透传能力，以本条为准。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（默认 `False`） |
| `incremental_output` | bool | 启用增量式流式输出（需 `stream=True` 时生效） |
| `MD5` | string | 文件上传必填，用于校验文件完整性（见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |

## 使用方式

- **插件调用**：在智能体（Agent）配置中启用对应插件；自定义插件需先在控制台注册并完成鉴权配置。  
- **RAG 调试**：若检索结果不准确，可通过模型回复下方的「问题反馈」按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **Markdown 渲染**：模型输出中的 `**text**` 等 Markdown 语法需由前端自行解析渲染，平台不提供自动 HTML 转换。  
- **售后支持入口**：7×24 小时支持通过官网、电话（95187）、阿里云 APP 或标准工单获取；基础服务覆盖 API 故障诊断、SDK 使用、控制台问题等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；含空行的结构化数据表可能导致后续行被跳过 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **知识库容量**：单业务空间上限为 10 万个文档；超限时需提交工单申请扩容。  
- **第三方工具支持边界**：阿里云仅对百炼服务端本身（API 可用性、计费记录、连通性测试建议）提供支持；**不负责 Cursor、Windsurf 等第三方工具的安装、配置、故障排查或本地网络（如代理、防火墙）问题** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


