# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、文件与数据管理，以及售后响应机制等核心环节。该支持体系面向生产环境需求设计，强调可配置性、可观测性和问题闭环路径。所有能力均需结合具体 API 调用方式与参数约束使用。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合 TopN 结果，广泛应用于问答系统、客户服务、教育与内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：支持 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新 token，而非全量重传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过标准协议注册函数/API，大模型可理解其参数结构并自主调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段透传。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”的技术含义（如是否指 SDK 封装类、Agent 类型或抽象接口），且与文档 3 中明确限定的售后支持范围（仅覆盖百炼 API/SDK 故障诊断，不含业务代码指导）存在边界模糊风险。实际开发中应以 API 协议和 SDK 文档为准，避免依赖未声明的抽象能力。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式 token 输出（避免重复回传历史内容） | 否（默认 `False`） |
| `MD5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |

## 使用方式

- **插件调用**：通过 `tools` 字段声明插件列表（含 `type` 和 `function` 描述），由模型自主决定调用时机与参数填充；自定义插件需符合 OpenAI-style function calling 协议。  
- **RAG 配置**：在应用编辑页绑定知识库，设置检索 topK、重排序策略及 chunk 处理方式；检索为并行执行，无串行依赖。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；空行将导致后续结构化数据被截断（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。  
- **问题反馈**：RAG 输出不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **插件限制**：自定义插件不支持除 `Authorization` 外的任何 HTTP Header 透传；非官方插件需自行保障安全性与稳定性。  
- **数据规模**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后边界**：阿里云百炼售后**不覆盖**第三方工具（如 Cursor、Windsurf 等）的安装配置、本地环境（代理/防火墙/VPN）、业务逻辑代码编写与调试；仅提供方向性建议（如连通性测试、API 示例核查）[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须审阅《阿里云百炼服务协议》及《体验功能特别说明》，开源模型使用还需遵守对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


