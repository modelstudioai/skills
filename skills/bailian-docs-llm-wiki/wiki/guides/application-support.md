# application [support](support.md)

application [support](support.md) 是阿里云百炼平台面向开发者提供的应用层能力支撑体系，涵盖[插件](../concepts/plugin.md)集成、RAG 知识增强、流式/增量输出、自定义[函数调用](../concepts/function-calling.md)等核心功能，并配套完善的售后支持机制与合规协议要求。开发者需结合服务协议、FAQ 实践指南及售后服务范围说明进行集成与问题排查。

## 支持的模型/功能

- **[插件](../concepts/plugin.md)能力**：官方提供六类内置[插件](../concepts/plugin.md)：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索（按用户配置策略执行），再基于得分聚合选取 topN 结果，广泛应用于问答系统、客户服务、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义函数/插件**：支持通过 Assistant API 注册并调用自定义 API 插件，模型可理解参数结构并返回结构化结果；但**不支持透传自定义 Header，仅允许 `Authorization` 字段** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **渲染与输出控制**：支持 Markdown 格式解析（如 `**text**` 渲染为加粗），并可通过 `stream=True` 和 `incremental_output=True` 启用增量式[流式输出](../concepts/streaming-output.md)。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回本次新增内容，非全量覆盖） |
| `MD5` | string | 文件上传必填，用于校验文件完整性（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)） |

> **注意**：文档 2 中第 8 条明确 `incremental_output=True` 为增量式流式输出开关，但当前 SDK 文档中该参数名在部分版本中可能被标记为实验性或已更名（如 `delta=True`），请以实际 SDK 版本说明为准。

## 使用方式

- **插件调用**：通过 Assistant API 配置插件 schema（OpenAPI Spec 或 Function Calling 格式），模型自动解析参数并触发调用；自定义插件需确保 endpoint 可公网访问且响应符合协议。  
- **RAG 应用构建**：在控制台创建知识库 → 上传 PDF/DOC/DOCX（注意后缀必须为小写 `pdf`）→ 绑定至应用；单业务空间上限 10 万个文档，超限时需提交工单扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **错误反馈与调试**：RAG 输出不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单；文件导入失败（如仅导入 20/100 条）需检查表格是否存在空行（首行为空即判为无效文件） [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **协议约束**：使用前须遵守 [阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)、[体验功能特别说明](../../raw/application-user-guide/application-support/application-related-agreements.md) 及 [开源模型协议条款](../../raw/application-user-guide/application-support/application-related-agreements.md)，尤其注意合规备案要求（如上架小程序需参考 [应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)）。  
- **第三方工具边界**：阿里云百炼售后**不支持**第三方工具（如 Cursor、Windsurf 等）的安装、配置、故障诊断或本地环境（代理/防火墙/VPN）问题排查；仅提供阿里云侧接口可用性、SDK 调用示例、计费核查等方向性建议 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **Header 限制**：调用自定义插件时，仅 `Authorization` 头可透传，其他自定义 Header 将被丢弃 —— 此为硬性限制，非配置问题 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


