# application [support](support.md)

`application support` 指百炼平台为开发者在构建和运行 AI 应用（如 Agent、RAG 应用、插件集成等）过程中提供的技术能力支撑、服务边界说明及使用约束。它涵盖模型/插件调用、流式与增量输出、知识库检索机制、API 参数控制，以及售后支持范围等核心维度。开发者需结合功能文档与协议条款，在平台能力边界内进行集成与问题排查。

## 支持的模型/功能

- **Agent 能力**：支持通过插件扩展智能体行为，官方提供六款内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后选取 topN 结果，适用于问答系统、客户服务、教育培训等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持开发者注册自定义 API 插件，模型可理解其参数结构并参与推理调度；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第4条称“Assistant API 可提供各种类，方便调优”，但未明确定义该 API 的具体形态、接口规范或是否仍为当前主推路径；而平台当前主推的是 `Agent` 架构与 `Assistant`（即 `qwen-plus` 等模型的 Assistant 模式）统一调用方式。建议以控制台最新 SDK 和 `/v1/chat/completions` 接口文档为准，避免依赖过时术语。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)，逐 token 返回响应。
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（区别于全量重发），适用于前端需实时渲染增量内容的场景。
- 文件上传必填 `MD5`：用于校验文件完整性，PDF 文件后缀须为小写 `pdf`，否则触发错误码 `140010`。
- RAG 检索无显式参数控制串行/并行，实际为**并行检索 + 得分融合**，由平台自动调度。

## 使用方式

- 插件调用：通过 `tools` 字段声明插件列表，`tool_choice` 控制调用策略；自定义插件需在控制台完成注册与鉴权配置。
- RAG 应用测试：可在控制台测试窗验证效果；若结果不准确，可通过回复下方“问题反馈”按钮提交，或复制 `RequestId` 提交工单。
- 流式响应解析：前端需自行处理 Markdown 语法（如 `**text**` 渲染为加粗），平台不提供富文本转换服务。
- 备案与合作：接入通义千问模型上架应用市场或小程序，须按 [应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 完成备案，并提交工单申请合作协议。

## 限制和注意事项

- **文件限制**：单业务空间最多上传 10 万个文档；结构化数据导入时，空行将导致后续数据被截断（含首行为空则视为无效文件）。
- **Header 限制**：调用自定义插件时，仅支持透传 `Authorization` Header，其他字段（如 `X-Custom-Header`）会被丢弃。
- **售后边界**：
  - 百炼提供 7×24 工单、电话及在线支持，覆盖模型功能、API 故障、控制台问题等 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)；
  - **不支持**第三方工具（如 Cursor、Windsurf）的部署调试、本地网络/代理/防火墙问题排查、业务代码编写指导，或非百炼侧服务（如其他云厂商 API）的联调支持；
  - 第三方工具引发的问题，阿里云仅提供方向性建议，最终运维责任归属用户及对应工具方 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需符合对应 [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)。

## 来源文档

- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


