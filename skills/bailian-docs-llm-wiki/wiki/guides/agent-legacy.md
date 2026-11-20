# agent legacy

`agent legacy` 是百炼平台早期提供的基于流程编排的智能体框架，用于构建具备多步骤推理与工具调用能力的应用。它采用显式节点连接方式定义执行逻辑，不依赖 LLM 自主规划，适用于确定性较强、流程可控的业务场景。该框架目前已进入维护期，新项目推荐使用 `agent v2`，但存量应用仍可稳定运行。

## 支持的模型与功能

- **模型支持**：仅限百炼平台已上线的 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（v1.0–v1.3 版本），不支持自定义模型或外部模型接入。  
- **核心功能**：支持条件分支（if-else）、循环（for/while）、并行节点、HTTP 请求、数据库查询（MySQL/PostgreSQL）、[函数调用](../concepts/function-calling.md)（Python 脚本）及变量传递。不支持记忆持久化、会话状态自动管理或异步长任务调度。  
- 详细能力说明见 [历史文档](../../raw/application-user-guide/agent-legacy.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `flow_id` | string | 是 | 在控制台创建的 Flow Agent 的唯一标识符，需与 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md) 中定义的 ID 严格一致 |
| `input` | object | 是 | JSON 格式输入，字段必须与 Flow 定义中的 `input_schema` 完全匹配，否则触发校验失败 |
| `timeout` | integer | 否 | 单位为秒，默认 60，最大 300；超时后终止整个流程并返回 `504 Gateway Timeout` |

> **注意**：部分旧版 SDK 示例中将 `timeout` 默认设为 120 秒，但实际服务端强制上限为 300 秒且不可绕过——请以 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md) 中的运行时约束为准。

## 使用方式

1. 在百炼控制台「应用」→「Agent」→「创建旧版 Flow Agent」中完成可视化编排，并发布；
2. 获取 `flow_id`（可在详情页 URL 或 API 响应中提取）；
3. 发起 HTTP POST 请求至 `https://dashscope.aliyuncs.com/api/v1/agents/legacy/run`，携带 `Authorization` 头（Bearer + API Key）及上述参数；
4. 解析响应体中的 `output` 字段（JSON）或 `error` 字段（失败时）。

示例请求体：
```json
{
  "flow_id": "flw-abc123",
  "input": {"query": "杭州天气", "unit": "celsius"},
  "timeout": 90
}
```

## 限制和注意事项

- 单次执行最大节点数：50；单个节点最大执行时间：30 秒（HTTP 节点受后端服务超时策略双重限制）；  
- 不支持流式响应（SSE），所有输出均为终态 JSON；  
- 变量作用域仅限当前流程实例，无跨请求共享机制；  
- 日志仅保留最近 7 天，且不包含中间节点原始输入/输出（仅摘要），调试需依赖控制台「实时日志」开关——该行为与 [历史文档](../../raw/application-user-guide/agent-legacy.md) 描述一致，但与新版 agent 的可观测性设计存在显著差异。

## 来源文档

- [历史文档](../../raw/application-user-guide/agent-legacy.md)


