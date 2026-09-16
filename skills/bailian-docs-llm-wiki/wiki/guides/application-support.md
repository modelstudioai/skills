# application [support](support.md)

application [support](support.md) 是阿里云百炼平台面向开发者提供的应用层能力支撑体系，涵盖插件集成、RAG增强、[流式输出](../concepts/streaming-output.md)、自定义[函数调用](../concepts/function-calling.md)等核心功能，并配套明确的售后支持边界与使用约束。该支持体系以 API 可编程性为基础，兼顾开箱即用性与深度定制能力，适用于智能体（Agent）、助手（Assistant）及知识库应用等典型场景。具体能力与限制需结合协议条款与技术文档协同理解。

## 支持的模型/功能

- **插件能力**：官方提供六款内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果融合生成，广泛应用于问答系统、客户服务、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件与[函数调用](../concepts/function-calling.md)**：支持通过 OpenAPI 协议注册自定义 API 插件，大模型可解析参数并生成调用指令；但**仅支持 `Authorization` header 透传，不支持其他自定义 header** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新片段而非全量重发）。  

> **注意**：文档2中“Agent和Assistant API的最大区别”描述为“调整插件模型、基于上下文的理解，用户可以自己去开发，而Assistant API是可以提供各种类，方便调优”，该表述模糊且未体现实际架构差异（如 Assistant API 实际封装了工具调用循环逻辑），建议以[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)中对 API 调用与故障诊断的支持范围为准，避免依赖该主观对比。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（默认 `False`） |
| `incremental_output` | bool | 启用增量式流式输出（需 `stream=True` 时生效） |
| `MD5` | string | 文件上传必填，用于校验文件完整性 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) |

## 使用方式

- **插件调用**：在应用配置中启用对应插件；自定义插件需在控制台完成注册、Schema 定义与鉴权配置。  
- **RAG 应用**：在知识库管理中上传 PDF/DOC/DOCX 文件（注意后缀须为小写 `pdf`），单业务空间上限 10 万文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **错误反馈**：RAG 测试中若回复不准确，可点击回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单。  
- **Markdown 渲染**：模型输出中的 `**text**` 等标记需由前端自行解析渲染，百炼服务端不执行格式转换。  

## 限制和注意事项

- **协议约束**：所有应用需遵守[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)、[体验功能特别说明](../../raw/application-user-guide/application-support/application-related-agreements.md)及开源模型相关条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **第三方集成边界**：阿里云百炼仅保障自身服务端可用性、API 接口规范与计费准确性；对第三方工具（如 Cursor、Windsurf 等）的部署、配置、故障排查及本地环境（代理/防火墙/VPN）问题**不提供支持** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **文件与数据限制**：结构化数据导入时，空行将导致后续数据被截断；首行为空行则视为无效文件 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **备案要求**：接入通义千问模型并上架应用市场或小程序，须按[应用合规备案](raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)指南完成备案，并通过工单申请合作协议。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


