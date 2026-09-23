# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、文件与数据管理、售后响应机制等核心环节。其目标是保障应用功能正确性、调用稳定性及问题可追溯性。所有支持能力均需在服务协议约定范围内使用，并受平台当前功能版本约束。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分选取 topN 结果进行生成；已应用于问答系统、对话系统、客户服务等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持两种模式：`stream=True`（全量流式）与 `incremental_output=True`（增量式流式），后者可避免重复渲染历史内容。  
- **自定义插件**：支持通过标准协议接入，大模型可理解参数结构并生成调用逻辑；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第 4 条称 “Assistant API 可提供各种类，方便调优”，但未明确类名、接口契约或 SDK 版本兼容性；该描述缺乏可操作细节，实际开发请以最新版 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中确认的支持范围为准。

## 关键参数

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `stream` | bool | 启用流式响应（逐 token 返回） | 否（默认 `False`） |
| `incremental_output` | bool | 启用增量式流式（仅返回新增 token，非全量重传） | 否（需 `stream=True` 时生效） |
| `MD5` | string | 文件上传时用于校验完整性的哈希值 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |

## 使用方式

- **插件调用**：在智能体（Agent）配置中启用对应插件，自定义插件需符合 OpenAPI 3.0 协议规范，并在函数描述中清晰声明参数类型与用途。  
- **RAG 调试**：若检索结果不准确，可通过模型回复下方的「问题反馈」按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；空行将导致后续结构化数据被截断，需预处理清洗 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后支持入口**：7×24 小时可通过官网、电话（95187 / 400）、阿里云 APP 或标准工单获取基础技术支持；深度定制需求（如业务代码指导）需联系商务经理订购增值服务 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件 Header 限制**：自定义插件调用时，仅支持透传 `Authorization` 请求头，其他 header（如 `X-User-ID`、`X-Tenant`）会被丢弃。  
- **知识库容量上限**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。  
- **第三方工具责任边界**：阿里云仅对百炼服务端（API、计费、控制台）负责；第三方工具（如 Cursor、Windsurf）的安装、配置、故障排查不在支持范围内 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：所有使用行为须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需额外遵循对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


