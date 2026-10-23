# llm application

`llm application` 是百炼平台提供的 LLM 应用构建与托管能力，支持通过低代码/高代码方式快速创建面向终端用户的 AI 应用（如智能体、工作流、文件问答等），并提供统一的 API 调用入口和权限管控机制。应用可基于平台内置模型或用户自定义模型运行，适用于对话交互、自动化任务编排、文档理解等多种场景。详细能力演进见 [新版智能体应用（Agent 2.0）](../../raw/raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 支持的模型与功能

- **模型支持**：默认使用平台托管的 `qwen-max`、`qwen-plus` 等通义系列模型；也支持绑定用户自有模型（需已部署在百炼模型中心）。  
- **应用类型**：包括智能体应用（Agent 1.0 / [Agent 2.0](../../raw/raw/application-user-guide/llm-application/new-single-agent-application.md)）、[工作流应用](../../raw/raw/application-user-guide/llm-application/workflow-application.md)、[文件问答](../../raw/raw/application-user-guide/llm-application/file-q-a.md)、高代码应用等。  
- **扩展能力**：支持集成 [插件](../../raw/raw/application-user-guide/plug-in.md)、自定义 Prompt、外部知识库（RAG）及多轮上下文管理。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，创建后生成，用于 API 调用和权限控制 |
| `model_id` | string | 否 | 指定推理模型 ID；未指定时使用应用默认模型 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅部分应用类型（如 Agent 2.0）完全支持 |
| `user_id` | string | 推荐 | 用于会话隔离与审计追踪，建议传入业务侧用户标识 |

> **注意**：`stream=true` 在 [工作流应用](../../raw/raw/application-user-guide/llm-application/workflow-application.md) 中行为受限（仅首节点支持流式），与 [新版智能体应用（Agent 2.0）](../../raw/raw/application-user-guide/llm-application/new-single-agent-application.md) 的全链路流式能力不一致，调用前请确认应用类型。

## 使用方式

1. **创建应用**：在控制台「应用开发」页选择类型（如「智能体应用」），配置 Prompt、工具、知识库等；参考 [开始使用](../../raw/raw/application-user-guide/llm-application/llm-application-start-using.md)。  
2. **发布应用**：完成调试后发布为线上版本，获取 `app_id`；发布流程详见 [应用发布与分享](../../raw/raw/application-user-guide/llm-application/application-publishing-and-sharing.md)。  
3. **API 调用**：使用 `POST /v1/applications/{app_id}/chat` 接口，携带 `Authorization: Bearer <api_key>` 及请求体（含 `messages` 数组）；完整调用规范见 [应用调用](../../raw/raw/application-user-guide/bailian-application-calling.md)。

## 限制和注意事项

- 单次请求 `messages` 最多 50 条，总 token 数上限取决于所选模型（如 `qwen-max` 当前为 32768）；超限将返回 `400` 错误。  
- 文件问答类应用仅支持 `.pdf`, `.docx`, `.xlsx`, `.txt`, `.pptx` 格式，单文件 ≤ 100MB；上传后自动解析，但表格/PPT 中复杂格式可能丢失。  
- 所有应用默认开启内容安全过滤（敏感词、涉政、违法等），不可关闭；若需调整策略，须提交工单申请白名单配置。  
- Agent 1.0 已进入维护期，新项目应优先选用 [新版智能体应用（Agent 2.0）](../../raw/raw/application-user-guide/llm-application/new-single-agent-application.md)，其支持更灵活的工具调用与状态管理。

## 来源文档

- [Flow Agent](../../raw/application-user-guide/llm-application.md)


