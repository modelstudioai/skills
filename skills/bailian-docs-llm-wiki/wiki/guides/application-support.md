# application [support](support.md)

`application support` 指百炼平台为开发者构建和运行 AI 应用（如 Agent、RAG 增强应用、插件集成应用等）所提供的能力支撑与服务边界。它涵盖模型/插件调用、参数配置、[流式输出](../concepts/streaming-output.md)控制、知识库检索机制等核心功能，同时也明确定义了平台侧的技术支持范围与责任边界。开发者需结合具体场景，在平台能力约束内进行集成与优化。

## 支持的模型/功能

- **Agent 能力**：支持基于大模型的智能体编排，内置六款官方插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分插件需申请开通 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **RAG（知识检索增强）**：支持多知识库并行检索，按用户配置的权重与得分选取 topN 结果后融合生成；适用于问答系统、客户服务、教育培训等场景 [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。
- **自定义插件**：支持通过符合协议的 API 接入自定义函数，大模型可理解其参数结构并参与调用决策；但**不支持透传自定义 Header，仅允许 `Authorization` 字段** [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第4条称“Assistant API 可提供各种类，方便调优”，但未说明具体类名或 SDK 接口形态；当前百炼官方 SDK（v1.0+）中实际暴露的是 `AgentClient` 和 `ChatClient` 两类主入口，`Assistant` 并非独立 API 类型。该表述易引发歧义，建议以 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确的 API 支持范围为准。

## 关键参数

- `stream=True`：启用[流式输出](../concepts/streaming-output.md)（逐 token 返回）；
- `incremental_output=True`：启用增量式[流式输出](../concepts/streaming-output.md)（仅返回本次新增内容，非全量重发）；
- 文件上传必填 `MD5`：用于校验文件完整性；
- 知识库检索无显式“串行/并行”开关，行为由系统固定：**并行检索各知识库，再统一排序合并**。

## 使用方式

- 插件调用：通过 `tools` 字段声明插件列表，由模型自主决定是否及如何调用；自定义插件需提供 OpenAPI Spec 格式描述；
- RAG 应用：在应用配置中绑定知识库，无需修改代码逻辑，平台自动注入检索上下文；
- 流式响应解析：前端需处理 `text/event-stream` 响应，并按 `data:` 行解析 SSE 格式事件；增量输出需配合 `incremental_output=True` 使用；
- 问题反馈：测试中发现 RAG 回复不准，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单。

## 限制和注意事项

- **文件上传限制**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被跳过；
- **插件 Header 限制**：调用自定义插件时，仅 `Authorization` 可透传，其他 header（如 `X-Api-Key`、`X-User-ID`）会被丢弃；
- **第三方工具支持边界**：阿里云百炼售后**不负责**第三方工具（如 Cursor、Windsurf 等）的安装、配置、故障诊断或本地环境（代理/防火墙/VPN）问题排查；仅提供阿里云侧接口可用性、SDK 示例、计费核查等方向性建议 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)；
- **服务协议约束**：所有使用须遵守《阿里云百炼服务协议》及《体验功能特别说明》，开源模型还需额外遵循对应 [开源模型协议条款说明](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


