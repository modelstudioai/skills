# bailian [application call](../api/application-call.md)ing

百炼平台支持通过 API 调用已发布的智能体应用（Agent Application）和工作流应用（Workflow Application），实现与业务系统的深度集成。调用过程遵循标准 HTTP 协议，需携带认证凭证、应用 ID 及必要输入参数。所有调用均受平台统一限流策略约束，开发者需关注错误码与重试机制。

## 支持的模型/功能

- **智能体应用**：基于单个大模型智能体构建，适用于对话式任务（如客服问答、内容生成），支持流式响应；详情见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。  
- **工作流应用**：由多个节点（含 LLM 调用、工具执行、条件分支等）编排而成，适用于多步骤复杂任务（如合同审核+风险提示+摘要生成）；详情见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。  
- 两类应用均支持参数透传、上下文继承（需显式开启）及自定义元数据注入，具体规则参见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用管理」中获取 |
| `input` | object | 是 | 用户输入数据，结构需与应用定义的 input schema 严格匹配 |
| `stream` | boolean | 否 | `true` 时启用 SSE 流式响应（仅智能体应用支持）；工作流应用不支持该参数，强制忽略 |
| `trace_id` | string | 否 | 用于链路追踪的唯一 ID，建议业务侧生成并透传 |

> **注意**：原始文档中 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 提到 `stream=true` 对工作流应用有效，但实测该参数被静默丢弃且无任何警告。请以实际 API 行为为准，勿依赖此行为。

## 使用方式

1. 获取应用 `app_id` 和访问密钥（`api_key` 或 `access_token`）；  
2. 构造 POST 请求，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat`；  
3. 设置请求头：`Authorization: Bearer <token>`，`Content-Type: application/json`；  
4. 在请求体中传入 `input` 对象（其他可选参数见上表）；  
5. 解析响应：成功时返回 `output` 字段（JSON 结构），失败时返回标准错误码（如 `429 Too Many Requests`）。

## 限制和注意事项

- 单应用默认 QPS 限流为 5，可通过控制台申请提升，详见 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)；  
- 输入 `input` 字段总大小（JSON 序列化后）不得超过 1MB；  
- 工作流应用单次执行超时时间为 120 秒，智能体应用为 60 秒；  
- 所有调用均计入账户配额，跨区域调用（如华东1调用华北2部署的应用）可能产生额外延迟，不推荐。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)


