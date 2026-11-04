# agent legacy

`agent legacy` 是百炼平台早期提供的基于流程图（Flow）的 Agent 构建能力，现已进入维护模式，不推荐新项目使用。其核心是通过可视化编排节点与连接线定义任务执行逻辑，适用于简单决策链路场景。该能力依赖于特定历史模型和固定参数集，与当前主流的 `agent v2`（基于 LLM 自主规划）存在架构差异。

## 支持的模型/功能

- 仅支持 `qwen-max-20240515`、`qwen-plus-20240515` 等带 `-20240515` 后缀的历史快照模型（见 [历史文档](../../raw/application-user-guide/agent-legacy.md)）；
- 支持基础节点类型：LLM 调用、条件分支（if-else）、HTTP 请求、变量赋值、返回结果；
- **不支持**工具调用（Tool Calling）、多轮自主反思（ReAct）、记忆管理（Memory）等现代 Agent 功能。

## 关键参数

- `flow_id`: 必填，对应在控制台中创建并发布的 Flow ID（格式如 `flw-xxx`）；
- `inputs`: 字典结构，键需严格匹配 Flow 中定义的输入变量名；
- `timeout`: 最大执行时长，单位秒，上限为 120 秒（超过将强制终止）；
- `max_steps`: 最大执行步数，上限为 50（含所有节点调用与跳转），详见 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)。

## 使用方式

通过 `/v1/agents/legacy/run` 接口发起同步调用（POST），请求体为 JSON：

```json
{
  "flow_id": "flw-abc123",
  "inputs": {"query": "今天天气如何？"},
  "timeout": 60,
  "max_steps": 30
}
```

响应包含 `status`（`success`/`failed`）、`outputs` 和 `trace`（执行路径日志）。调试时建议开启 `trace` 并参考 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md) 中的 trace 字段说明。

> **注意**：文档中曾提及支持异步回调（`callback_url`），但当前 API 已移除此字段；实际调用时若传入将被忽略——请以 [历史文档](../../raw/application-user-guide/agent-legacy.md) 中最新接口定义为准。

## 来源文档

- [历史文档](../../raw/application-user-guide/agent-legacy.md)


