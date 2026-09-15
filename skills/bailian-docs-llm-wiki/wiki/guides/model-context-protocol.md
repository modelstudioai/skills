# model context protocol

Model Context Protocol（MCP）是百炼平台提供的标准化上下文交互协议，用于在大模型调用中动态注入结构化外部数据（如知识库、实时API、数据库结果等），从而增强模型推理的准确性与可控性。它通过声明式配置和轻量服务接口实现模型与上下文源的解耦，支持同步/异步上下文获取。该协议并非模型内置能力，而是平台级调度层对上下文供给链路的统一抽象。

## 支持的模型与功能

MCP 当前适用于所有支持 `context` 字段注入的百炼托管模型（包括 Qwen 系列、Qwen2 系列及部分第三方微调模型），但**不适用于直接调用的开源模型 API（如 HuggingFace raw endpoint）**。核心功能包括：  
- 上下文片段的按需加载与缓存（TTL 可配）  
- 多源上下文并行获取与优先级合并（基于 `weight` 字段）  
- 错误降级策略（如某 MCP 服务超时，自动跳过并记录告警）  
详细兼容模型列表见 [MCP 简介](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md)。

## 关键参数

在请求体中通过 `context` 字段启用 MCP，其结构为：

```json
{
  "context": {
    "sources": [
      {
        "type": "mcp",
        "url": "https://your-mcp-service.com/v1/context",
        "method": "POST",
        "headers": { "Authorization": "Bearer xxx" },
        "body": { "query": "{{input.query}}", "user_id": "{{user.id}}" },
        "timeout_ms": 3000,
        "weight": 0.8
      }
    ]
  }
}
```

- `url`：必须为 HTTPS，且需在百炼控制台[官方 MCP 服务](../../raw/application-user-guide/model-context-protocol/official-and-third-party-mcp.md)或[自定义MCP服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md)中完成白名单注册  
- `body` 支持 Jinja2 模板语法（仅 `{{input.*}}` 和 `{{user.*}}` 两类变量）  
- `weight` 范围为 `[0.0, 1.0]`，影响上下文在 [prompt](prompt.md) 中的相对长度占比  

> **注意**：文档中提及的 `retry_policy` 参数已在 v2.3.0 版本移除，实际请求中设置将被忽略；请参考 [MCP 外部调用](../../raw/application-user-guide/model-context-protocol/mcp-external-calls.md) 的最新参数说明。

## 使用方式

1. **启用协议**：在调用 `chat/completions` 或 `completions` 接口时，于请求 JSON 中显式传入 `context` 对象（空对象 `{}` 不触发 MCP）  
2. **服务部署**：自建 MCP 服务需遵循 [自定义MCP服务](../../raw/application-user-guide/model-context-protocol/custom-mcp.md) 定义的响应格式（HTTP 200 + JSON array of `{content: string, type: "text"|"code"|"table"}`）  
3. **调试验证**：使用 `X-Bailian-Debug: true` 请求头可返回 `x-bailian-mcp-trace` 响应头，含各 source 的耗时与状态码  

## 限制和注意事项

- 单次请求最多配置 5 个 `sources`，总上下文 token 数上限为模型 `max_context_length` 的 30%（例如 Qwen2-72B 最高约 3k tokens）  
- MCP 服务响应必须在 `timeout_ms` 内完成，超时后该 source 被丢弃，不阻塞主模型推理  
- 所有上下文内容在进入 tokenizer 前会自动添加分隔符 `--- CONTEXT SOURCE: <id> ---`，不可禁用  
- 若同时配置了 `retrieval`（向量检索）和 MCP，二者上下文将合并，但 `retrieval` 结果默认 `weight=1.0`，优先级高于 MCP；此行为与 [MCP 简介](../../raw/application-user-guide/model-context-protocol/mcp-introduction.md) 中“完全独立”的描述存在偏差，以实际运行逻辑为准

## 来源文档

- [MCP](../../raw/application-user-guide/model-context-protocol.md)


