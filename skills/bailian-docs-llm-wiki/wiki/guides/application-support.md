# application [support](support.md)

`application support` 指百炼平台为开发者构建和运行 AI 应用（如 Agent、RAG 增强应用、插件集成应用等）所提供的能力支撑与服务边界。它涵盖模型调用、插件管理、知识库检索、[流式输出](../concepts/streaming-output.md)控制等核心功能，同时也明确定义了技术支持范围、参数约束及合规要求。开发者需结合具体场景，在平台能力边界内进行集成与优化。

## 支持的模型/功能

- **Agent 能力**：支持通过官方插件（Python 解释器、计算器、图片生成、夸克搜索、二维码生成、GitHub 搜索）扩展智能体行为；自定义插件可接入，但仅支持 `authorization` header 透传，[不支持其他自定义 header](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG 检索增强**：支持多知识库并行检索，按配置策略打分后选取 topN 结果；适用于问答系统、客服对话、教育内容生成等场景，详见 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **流式与增量输出**：可通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新生成 token，而非全量重发），避免前端重复渲染。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式输出（仅返回新增内容） | 否（默认 `False`） |
| `MD5` | string | 文件上传接口必填，用于校验文件完整性 | 是（见 [数据管理](../../raw/application-user-guide/application-support/application-faq.md)） |

> **注意**：文档 1 中第 8 条明确 `incremental_output=True` 为增量式[流式输出](../concepts/streaming-output.md)开关，但该参数未在官方 OpenAPI 文档中统一标注为标准字段；实际使用前请以最新 SDK 或 `/v1/chat/completions` 接口文档为准。

## 使用方式

- **插件调用**：自定义插件需按协议定义函数签名（含 name、description、parameters），由大模型理解并调用；参数信息将透传至模型上下文供推理使用。
- **RAG 应用调试**：若检索结果不准确，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交阿里云工单（参考 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时需避免空行，否则后续行将被忽略。

## 限制和注意事项

- **插件限制**：部分官方插件（如夸克搜索、GitHub 搜索）需申请开通；自定义插件本身免费，但涉及 [prompt](prompt.md) 优化、应用调用测试等操作将产生计费。
- **文件与容量限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。
- **售后支持边界**：  
  - ✅ 支持范围包括：API/SDK 故障诊断、控制台问题、账号与计费咨询、连通性基础测试（如 curl 验证服务可达性）。  
  - ❌ 不支持范围包括：第三方工具（如 Cursor、Windsurf）的部署/配置/排障、用户本地网络/代理/防火墙问题、业务代码编写指导、非阿里云侧服务的运维——详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **合规要求**：上架应用或小程序前，必须完成[应用合规备案](../../model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)，并申请通义千问合作协议（参见 [应用/小程序备案](../../raw/application-user-guide/application-support/application-faq.md)）。

## 来源文档

- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


