# bailian [application call](../api/application-call.md)ing

百炼平台支持通过 API 调用已发布的智能体应用（Agent Application）和工作流应用（Workflow Application），实现与业务系统的深度集成。调用过程遵循统一的 HTTP 接口规范，支持参数透传、异步响应及错误重试机制。所有调用均需携带有效的 API Key 和应用 ID，具体行为受应用配置与平台限流策略约束。

## 支持的模型/功能

- **智能体应用**：基于单个大模型（如 Qwen-Max、Qwen-Plus）封装的对话式应用，支持[流式输出](../concepts/streaming-output.md)与会话上下文管理；详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。  
- **工作流应用**：由多个节点（LLM 调用、工具执行、条件分支等）编排而成的复杂任务流程，支持多轮状态保持与外部系统回调；详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。  
- 两类应用均支持输入参数透传、自定义 system [prompt](prompt.md) 覆盖（若应用允许），以及 `stream=true` 下的 SSE 流式响应。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `application_id` | string | 是 | 应用在百炼控制台发布的唯一 ID，非模型 ID |
| `input` | object | 是 | 用户输入内容，结构由应用定义（如 `{ "query": "..." }`），详见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流，需按 `data:` 行解析 |
| `timeout` | integer | 否 | 单位秒，最大 300；超时后平台主动终止执行并返回 `504 Gateway Timeout` |

> **注意**：原始文档中部分示例仍使用已废弃的 `model` 字段作为必填项，该字段在 v2.3+ 版本中已被移除，实际调用中**不应传入**；请以 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中最新接口定义为准。

## 使用方式

1. 获取应用 ID：在百炼控制台「应用管理」→「已发布应用」中复制目标应用的 `Application ID`；  
2. 构造请求：向 `https://dashscope.aliyuncs.com/api/v1/applications/{application_id}/call` 发送 `POST` 请求；  
3. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；  
4. 解析响应：同步调用返回 JSON（含 `output`, `status`, `session_id`）；流式调用需按行处理 `data:` 事件。

## 限制和注意事项

- 单应用默认 QPS 限流为 5，可通过 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md) 页面申请提升；  
- 输入 `input` 字段总大小（JSON 序列化后）不得超过 1MB；  
- 工作流应用单次执行最长耗时 180 秒，超时将中断并释放资源；  
- `session_id` 用于会话状态追踪，但智能体应用的上下文窗口仅保留最近 10 轮交互，超出后自动截断——此行为与部分旧版文档描述的“无限轮次”不一致，请以 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 最新说明为准。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)


