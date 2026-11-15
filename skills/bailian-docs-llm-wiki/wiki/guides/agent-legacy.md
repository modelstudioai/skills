# agent legacy

`agent legacy` 是百炼平台早期提供的基于流程编排的智能体框架，用于构建具备多步骤推理与工具调用能力的应用。它采用显式节点连接方式定义执行逻辑，不依赖 LLM 自主规划，适用于确定性较强、流程可控的业务场景。该框架目前已进入维护期，新项目推荐使用 `agent v2`，但存量应用仍可继续运行和迭代。

## 支持的模型与功能

- **支持模型**：仅限百炼平台已上线的 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（v1.0–v1.5 版本），不支持 `qwen2.5` 及后续大版本模型。  
- **核心功能**：  
  - 多节点顺序/条件分支执行（如 `LLMNode`、`ToolNode`、`IfNode`）  
  - 同步工具调用（支持 HTTP、SQL、Python 函数等自定义工具）  
  - 上下文变量传递与 JSONPath 提取  
  - 基础日志与 trace 可视化（见 [历史文档](../../raw/application-user-guide/agent-legacy.md)）  

> **注意**：原始文档中提及的 `qwen-vl` 支持已在 v1.3.2 后移除，实际部署时若指定该模型将触发 `ModelNotSupportedError` —— 请以 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md) 中的兼容性表格为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `flow_id` | string | 是 | 在控制台创建的 Flow ID，对应 `agent-legacy` 的唯一部署实例 |
| `input` | object | 是 | 输入数据，结构需与 Flow 定义中的 `input_schema` 严格匹配 |
| `timeout` | integer | 否 | 全局超时（秒），默认 30，最大 120 |
| `enable_tracing` | boolean | 否 | 是否启用 trace 上报，默认 `false`；开启后可在控制台查看节点级耗时（参见 [历史文档](../../raw/application-user-guide/agent-legacy.md)） |

## 使用方式

1. 在百炼控制台「应用」→「Agent」→「旧版 Flow Agent」中创建并发布 Flow；  
2. 调用 SDK 或 REST API：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/agents/legacy \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "flow_id": "fl-xxx",
           "input": {"query": "今天杭州天气如何？"},
           "timeout": 60
         }'
   ```  
3. 响应结构为标准 JSON，含 `output`（最终结果）、`status`（`success`/`failed`）及可选 `trace` 字段。

## 限制和注意事项

- **并发限制**：单个 `flow_id` 默认最大并发 5，超出请求将被拒绝（HTTP 429），不可通过配额提升；  
- **输入大小**：`input` 序列化后总长度 ≤ 100 KB，超限返回 `InputTooLargeError`；  
- **工具调用**：所有工具必须预先在 Flow 编辑器中注册，运行时动态注册无效；  
- **状态保持**：`agent legacy` 无内置会话状态管理，需由上层应用自行维护 `session_id` 并透传至每个请求（详见 [Flow Agent（旧版）](../../raw/application-user-guide/agent-legacy/legacy-flow-agent.md)）；  
- **弃用提示**：自 2024 年 Q3 起，控制台新建 Flow 功能已隐藏，仅支持编辑已有 Flow。

## 来源文档

- [历史文档](../../raw/application-user-guide/agent-legacy.md)


