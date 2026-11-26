# application [support](support.md)

`application support` 指百炼平台为开发者构建和运行 AI 应用（如 Agent、RAG 增强应用、插件集成应用等）所提供的能力支撑与服务边界。它涵盖模型调用、插件管理、知识库检索、[流式输出](../concepts/streaming-output.md)控制等核心功能，同时定义了 API 行为约束、售后支持范围及合规要求。开发者需结合具体场景，在功能可用性、参数配置与服务边界之间做出合理设计。

## 支持的模型/功能

- **Agent 能力**：支持通过官方插件（Python 解释器、计算器、图片生成、夸克搜索、二维码生成、GitHub 搜索）扩展智能体行为；自定义插件可被大模型理解并调用，但仅支持 `authorization` header 透传，不支持其他自定义 header [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG 检索增强**：支持多知识库并行检索，按配置策略打分后取 topN 结果融合生成；广泛应用于问答系统、客服、教育、内容创作等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **[流式输出](../concepts/streaming-output.md)控制**：支持增量式流式响应，需显式设置 `stream=True` 和 `incremental_output=True` 参数，避免前端重复渲染全量内容 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `stream` | bool | 启用[流式输出](../concepts/streaming-output.md)（逐 token 返回） | `True` |
| `incremental_output` | bool | 启用增量式流式输出（仅返回新增部分，非累计） | `True` |
| `MD5` | string | 文件上传必填，用于校验文件完整性 | `"d41d8cd98f00b204e9800998ecf8427e"` |

> **注意**：文档 1 中明确要求 `incremental_output=True` 才能实现增量输出，但该参数在当前主流 SDK（如 `dashscope` v1.18+）中已统一归入 `stream_options` 对象，直接传入顶层参数可能被忽略。建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中推荐的官方 SDK 文档为准进行适配。

## 使用方式

- **插件调用**：自定义插件需遵循 OpenAPI Schema 协议注册，参数由大模型自动解析并构造请求；[函数调用](../concepts/function-calling.md)结果将完整返回给模型用于后续推理。
- **知识库导入**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx` 格式；结构化数据导入时需确保无空行，否则空行之后的数据将被跳过。
- **问题反馈与排查**：
  - RAG 输出不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单；
  - 文件上传失败（如错误码 `140010`）应检查后缀大小写与格式兼容性；
  - 第三方工具对接问题（如 Cursor、Windsurf 等），阿里云仅提供方向性建议，不承担其部署、配置或故障诊断责任 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件限制**：部分官方插件（如夸克搜索、GitHub 搜索）需申请开通；自定义插件本身免费，但涉及 prompt 优化、应用调用测试等操作将产生计费。
- **文件管理**：单业务空间最多支持 10 万个文档；超限时需提交工单申请扩容。
- **协议与合规**：所有应用上线至小程序或应用市场前，必须完成[应用合规备案](../../model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)及通义千问合作协议备案；相关法律条款详见 [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE) 与 [阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html) [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。
- **售后边界**：阿里云不支持对用户本地环境（代理、防火墙、VPN）、第三方工具内部逻辑、业务代码实现等问题提供深度支持；复杂集成需求建议联系商务经理定制服务方案 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 来源文档

- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


