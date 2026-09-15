# application [support](support.md)

百炼平台的应用支持体系面向开发者提供从功能能力、API调用到售后保障的全链路支撑。核心覆盖插件集成、RAG增强、[流式输出](../concepts/streaming-output.md)等关键能力，同时明确服务边界与技术限制。开发者需结合官方文档与协议条款，在合规前提下进行应用开发与问题排查。

## 支持的模型/功能

- **插件能力**：当前官方支持六类插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持并行多知识库检索，按配置策略打分后选取 topN 结果，广泛应用于问答系统、客户服务、教育等领域 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新片段而非全量重传） [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持基于 OpenAPI 规范的[函数调用](../concepts/function-calling.md)，模型可解析参数并生成调用请求；但**仅支持 `Authorization` header 透传，不支持其他自定义 header**（如 `X-User-ID` 等）。

> **注意**：文档1中第4条称“Assistant API 可以提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类、配置类或抽象接口类），且该表述与其他文档中对 Assistant API 的标准化描述（如 `messages` + `tools` 调用范式）存在语义模糊性，建议以最新版 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中的参数与行为说明为准，避免依赖该模糊表述进行架构设计。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用流式响应（逐 token 返回） |
| `incremental_output` | bool | 在 `stream=True` 基础上启用增量模式（仅返回新增内容） |
| `tool_choice` | string / object | 控制插件调用策略（如 `"auto"`、`{"type": "function", "function": {"name": "xxx"}}`） |
| `retrieval_config` | object | RAG 检索配置，含 `top_k`、`score_threshold` 等（详见控制台知识库配置） |

> **注意**：`incremental_output=True` 仅在流式场景下生效；若 `stream=False`，该参数无效。

## 使用方式

- **插件调用**：需在应用配置中启用对应插件，并在 [prompt](prompt.md) 或 tool definition 中声明参数 schema；模型将根据上下文自主决定是否调用及传参。  
- **RAG 集成**：上传文件至知识库（仅支持小写后缀 `.pdf`、`.doc`、`.docx`；空行会导致后续数据截断）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **错误反馈**：RAG 输出不准确时，可通过测试页“问题反馈”按钮提交，或复制 `RequestId` 提交工单。  
- **备案要求**：若应用上架至应用市场或小程序平台，须完成[应用合规备案](raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)，并申请通义千问合作协议。

## 限制和注意事项

- **文件上传**：单业务空间上限 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具支持边界**：阿里云百炼仅保障自身服务端可用性、API 正确性及计费一致性；**不支持第三方工具（如 Cursor、Windsurf 等）的安装、配置、本地环境（代理/防火墙/VPN）、业务代码调试或其内部统计差异解释** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》[相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **MD 渲染**：模型输出中的 `**text**` 等 Markdown 语法需由前端自行解析渲染，平台不提供富文本转换服务。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


