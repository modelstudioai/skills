# bailian [application call](../api/application-call.md)ing

百炼平台支持通过 API 调用已发布的智能体应用（Agent Application）和工作流应用（Workflow Application），实现与业务系统的深度集成。调用过程遵循统一的 HTTP 接口规范，支持参数透传、异步响应及[流式输出](../concepts/streaming-output.md)。所有调用均需携带有效的 API Key 和应用 ID，并遵守平台配额与安全策略。

## 支持的模型/功能

- **智能体应用**：基于单个大模型智能体构建，适用于对话式任务（如客服问答、知识检索）。调用方式详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。  
- **工作流应用**：由多个节点（含LLM调用、工具执行、条件分支等）编排而成，支持复杂业务逻辑。其调用机制与智能体应用不同，需额外处理 `workflow_id` 和节点上下文，参考 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。  
- **参数透传能力**：支持将用户输入、会话状态、自定义元数据等作为 `input` 字段透传至应用内部，具体字段结构和约束见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `application_id` | string | 是 | 应用唯一标识，可在控制台「应用管理」中获取 |
| `input` | object | 是 | 用户输入内容，结构由应用定义；必须为 JSON 对象，不支持纯字符串或数组 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应（仅部分应用支持） |
| `trace_id` | string | 否 | 用于链路追踪的唯一标识，建议业务侧生成并透传 |

> **注意**：原始文档中未明确 `input` 字段是否允许空对象 `{}`，但实测部分工作流应用会因空 `input` 返回 400 错误；建议始终提供至少一个有效字段（如 `"query": ""`），以兼容所有应用类型。

## 使用方式

1. 构造 POST 请求，目标 URL 为 `https://dashscope.aliyuncs.com/api/v1/applications/{application_id}/call`  
2. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`  
3. 在 Body 中提交 JSON，包含 `input` 及可选参数（如 `stream`, `trace_id`）  
4. 处理响应：同步调用返回完整结果（`output` 字段）；流式调用需按 SSE 协议解析 `data:` 事件  

示例请求体：
```json
{
  "input": {
    "query": "今天杭州天气如何？",
    "user_id": "u_12345"
  },
  "stream": false
}
```

## 限制和注意事项

- 单次调用 `input` 总大小上限为 1MB（含嵌套 JSON 序列化后长度）；超出将返回 `413 Payload Too Large`  
- 智能体应用默认超时 60 秒，工作流应用默认超时 120 秒；可通过控制台调整，但不可超过平台全局上限（参见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 的“超时配置”章节）  
- 同一 `application_id` 下，若同时存在智能体与工作流版本，API 仅路由至最新发布版本，旧版本不可回退调用  
- 不支持跨地域调用：API Endpoint 与应用部署地域必须一致（例如华东1区应用只能调用 `dashscope.aliyuncs.com`，不可用 `dashscope.cn-shanghai.aliyuncs.com`）

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)


