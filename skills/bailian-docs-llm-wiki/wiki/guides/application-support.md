# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。其目标是保障应用功能正确性、调用稳定性与问题可追溯性。所有支持能力均以平台当前正式发布的 API 行为和控制台配置为准。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置独立执行），再基于相关性得分聚合选取 topN 结果，适用于问答系统、客户服务、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持两种模式：`stream=True`（全量流式）与 `incremental_output=True`（增量式流式），后者可避免重复渲染历史内容。  
- **自定义插件**：支持通过标准协议注册函数或 API，大模型可理解参数结构并生成调用请求；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类型、配置类或抽象接口类）；该表述缺乏上下文与示例，易引发歧义，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的 API 和 SDK 支持范围为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（逐 token 返回） | 否（默认 `False`） |
| `incremental_output` | bool | 启用增量式[流式输出](../concepts/streaming-output.md)（仅返回新增 token） | 否（需 `stream=True` 时生效） |
| `MD5` | string | 文件上传时用于校验完整性的哈希值 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |

## 使用方式

- 插件调用：在智能体（Agent）配置中启用对应插件，或通过 Assistant API 的 `tools` 字段声明函数 schema；自定义插件需符合 OpenAI-style function calling 协议。  
- RAG 应用调试：若检索结果不准确，可通过前端反馈按钮提交问题类型，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 文件上传：仅支持小写后缀的 `pdf`/`doc`/`docx`；空行将导致后续结构化数据被截断（第一行为空则视为无效文件）。  
- 售后接入：7×24 小时支持通过官网、电话（95187）、阿里云 APP 或标准工单获取；基础服务覆盖 API 故障诊断、SDK 使用、控制台问题等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件限制**：自定义插件不支持除 `Authorization` 外的任何 HTTP Header 透传；非官方插件需自行承担安全与合规责任。  
- **数据规模**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具免责**：阿里云仅对百炼服务端（API、计费、控制台）负责；第三方工具（如 Cursor、Windsurf 等）的安装、配置、故障排查不在支持范围内，详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 第 4 条。  
- **协议约束**：使用前须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需遵循对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


