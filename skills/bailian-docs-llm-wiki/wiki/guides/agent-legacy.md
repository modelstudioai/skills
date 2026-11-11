# agent legacy

`agent legacy` 是百炼平台早期提供的 Flow Agent 实现，用于构建基于预定义流程的自动化任务代理。该版本已进入维护模式，新项目应优先选用 `agent v2`，但部分存量应用仍在使用此架构。其核心能力围绕节点编排、工具调用和状态流转展开，适用于对流程确定性要求较高的轻量级场景。

## 支持的模型与功能

- 仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型（[历史文档](../../raw/application-user-guide/agent-legacy.md)）；
- 支持同步执行模式（`sync`），不支持流式响应（streaming）；
- 提供基础工具调用（Tool Calling）、条件分支（if-else）、循环（loop）及变量传递能力；
- 不支持多轮对话记忆管理、长期会话上下文自动压缩，需用户自行维护 state（参见 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `flow_id` | string | 是 | 在控制台创建的 Flow ID，对应 `agent-legacy` 下的流程定义 |
| `inputs` | object | 是 | 输入变量键值对，字段必须与流程中声明的 input schema 严格一致 |
| `timeout` | integer | 否 | 超时时间（秒），默认 30，最大支持 120 |
| `enable_tracing` | boolean | 否 | 是否启用执行链路追踪，默认 `false`；开启后可在日志中查看各节点耗时（[历史文档](../../raw/application-user-guide/agent-legacy.md)） |

> **注意**：`enable_tracing=true` 时 trace 数据仅保留 1 小时，且不计入配额统计；而新版 `agent v2` 的 tracing 默认持久化 7 天并支持查询 API，二者行为不一致，请勿直接迁移配置。

## 使用方式

通过 `/v1/agents/legacy/run` 接口发起调用（POST）：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/agents/legacy/run" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "flow_id": "fl-xxx",
        "inputs": {"query": "今天天气如何？"},
        "timeout": 60
      }'
```

响应体为 JSON，包含 `status`（`success`/`failed`）、`outputs`（最终输出对象）和 `execution_id`（用于问题排查）。

## 限制和注意事项

- 单次执行最大节点数：50；单个节点最大执行时间：10 秒；
- 工具调用仅支持同步 HTTP 工具（Webhook），不支持异步回调或长时任务；
- `inputs` 中禁止传入嵌套过深（>5 层）或总大小超 512KB 的 JSON；
- 所有日志和 trace 数据均不落盘至客户专属存储，仅临时缓存于百炼服务端（[Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)）；
- 自 2024 年 10 月起，`agent legacy` 不再接收新功能迭代，安全补丁仅覆盖 CVE 高危项。

## 来源文档

- [历史文档](../../raw/application-user-guide/agent-legacy.md)


