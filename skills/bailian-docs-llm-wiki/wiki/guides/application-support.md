# application [support](support.md)

`application support` 指百炼平台为开发者在构建和运行 AI 应用（含 Agent、RAG、插件集成等）过程中提供的功能能力、调用支持、服务边界及合规保障。它覆盖模型调用、插件管理、知识库增强、[流式输出](../concepts/streaming-output.md)等核心开发场景，同时明确售后响应范围与第三方集成责任边界。开发者需结合具体功能文档与协议条款进行集成设计与问题排查。

## 支持的模型/功能

- **Agent 能力**：支持六类官方插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分插件需申请开通 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果，适用于问答系统、客服对话、教育训练等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新片段而非全量重传） [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持基于 OpenAPI 规范注册的自定义函数，模型可理解参数结构并生成调用逻辑；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段透传。

> **注意**：文档 1 中第 4 条称 “Assistant API 可以提供各种类，方便调优”，但未明确定义“类”的技术含义（如是否指 SDK 封装类、抽象接口或配置模板），且该表述与其他文档中统一使用的 `Assistant API`（指标准 RESTful 接口）存在语义模糊。建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中定义的 API 和 SDK 支持范围为准，避免依赖非标准化术语。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `stream` | bool | 启用流式响应（逐 token 返回），默认 `False` |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式输出（仅返回新增内容），默认 `False` |
| `MD5` | string | 文件上传必填，用于校验文件完整性（见数据管理章节） |
| `Authorization` | string | 唯一支持透传的 HTTP Header，用于身份鉴权；其他自定义 Header 将被丢弃 |

## 使用方式

- **插件调用**：在 Agent 配置中声明插件列表，模型将根据用户请求自动选择并构造符合 OpenAPI Schema 的调用参数。
- **RAG 应用测试**：在控制台测试窗中输入问题，若结果不准确，可通过回复下方「问题反馈」按钮提交，或复制 `RequestId` 提交工单。
- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；上传前需计算并传入文件 MD5 值。
- **API 调用支持**：官方提供 SDK（Python/Java 等）及 curl 示例，故障诊断、计费核查、连通性测试均属基础售后支持范围 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **插件透传限制**：自定义插件调用时，仅 `Authorization` Header 可透传至目标服务端；其他 Header（如 `X-User-ID`、`X-Tenant`）会被平台拦截，不可用于业务上下文传递。
- **文件与数据限制**：单业务空间最多上传 10 万个文档；结构化数据导入时，空行将导致其后所有数据被跳过（首行为空则视为无效文件）。
- **第三方工具责任边界**：阿里云百炼**不负责**第三方工具（如 Cursor、Windsurf、开源代理框架）的部署、配置、升级或故障排查；仅提供阿里云侧 API 可用性确认、调用示例、计费核查等方向性建议 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需额外遵循对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


