# application [support](support.md)

`application support` 指百炼平台为开发者构建和运行 AI 应用（如 Agent、RAG 增强应用、插件集成应用等）所提供的能力支撑与服务边界。它涵盖模型/插件调用、参数配置、[流式输出](../concepts/streaming.md)控制、知识库检索机制等核心功能，同时也明确定义了技术支持范围与限制条件。开发者需结合具体场景，在平台能力边界内进行集成与优化。

## 支持的模型/功能

- **Agent 能力**：支持通过插件扩展智能体行为，官方提供六款内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分插件需申请开通 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（[检索增强生成](../concepts/rag.md)）**：支持多知识库并行检索，并按得分选取 topN 结果后融合生成；适用于问答系统、客户服务、教育、内容创作等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持开发者注册 HTTP API 插件，模型可理解其参数协议并完成调用；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第4条称“Assistant API 可提供各种类，方便调优”，但未说明具体类名或接口形态；当前百炼 SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)中并无 `Assistant` 类抽象，实际使用以 `ChatCompletion` 或 `AgentRuntime` 为主。该描述可能已过时或指代内部实验性接口，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确支持的 API 和 SDK 文档为准。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming.md)（逐 token 返回）；
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming.md)（仅返回新增内容，非全量重发）；
- 文件上传必填 `MD5`：用于校验文件完整性；
- 知识库检索无显式串行/并行开关，系统默认**并行检索各知识库**，再统一排序合并结果。

## 使用方式

- 插件调用：通过 `tools` 字段声明插件 schema，由模型自主决定是否调用及传参；
- RAG 应用：在应用配置中绑定知识库，无需修改代码逻辑，平台自动注入检索上下文；
- 自定义插件调试：可在测试窗中直接触发，但涉及 prompt 优化、API 调用与测试窗测试将产生计费；
- 问题反馈：RAG 输出不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单。

## 限制和注意事项

- **文件上传限制**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断；
- **知识库容量**：单业务空间上限为 10 万个文档，超限时需提交工单申请扩容；
- **Header 限制**：调用自定义插件时，仅支持透传 `Authorization` header，其他字段会被丢弃；
- **第三方工具支持边界**：阿里云百炼售后**不负责**第三方工具（如 Cursor、Windsurf 等）的安装、配置、升级或故障排查；仅提供阿里云侧接口可用性、SDK 示例、调用明细核查等方向性建议 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)；
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需符合对应[开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


