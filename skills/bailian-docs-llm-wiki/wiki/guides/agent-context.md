# agent context

`agent context` 是百炼平台中用于定义 Agent 行为边界与知识来源的核心机制，它决定了 Agent 在执行任务时可访问的外部信息、历史记忆及数据连接能力。通过显式配置上下文，开发者可精准控制 Agent 的“所知”与“所见”，避免信息过载或知识泄露。该机制并非模型内置能力，而是平台层提供的运行时上下文注入框架。

## 支持的模型/功能

当前仅 `qwen-max`、`qwen-plus` 及 `qwen-turbo`（v20240915 及之后版本）原生支持完整的 `agent context` 注入能力；其他模型（如 `qwen-1.5` 系列旧版）虽可接收 context 字段，但实际不解析或忽略其中的 RAG/Memory 内容。RAG、Memory 和 Connector 三大上下文组件均需配合对应服务启用：RAG 依赖知识库服务 [Agent 上下文](../../raw/application-user-guide/agent-context.md)，Memory 需启用 Memory Library [Agent 上下文](../../raw/application-user-guide/agent-context/memory-library-overview.md)，Connector 则需预先配置数据源连接 [Agent 上下文](../../raw/application-user-guide/agent-context/overview.md)。

> **注意**：文档中提及的 `ParseX` 上下文能力（见 [Agent 上下文](../../raw/application-user-guide/agent-context/getting-started-overview.md)）已在 v202410 版本中移除，不再受支持；请勿在新应用中引用 `parsex_context` 相关参数。

## 关键参数

调用 `/v1/chat/completions` 时，通过 `context` 字段传入 JSON 对象，结构如下：
```json
{
  "rag": { "knowledge_base_ids": ["kb-xxx"] },
  "memory": { "session_id": "sess-123", "limit": 10 },
  "connector": { "connector_id": "conn-abc" }
}
```
- `rag.knowledge_base_ids`：必填数组，最多 3 个知识库 ID；ID 必须已对当前 API Key 授权  
- `memory.session_id`：必填字符串，长度 1–64 字符，仅支持 ASCII 字母、数字、`-`、`_`  
- `connector.connector_id`：选填，若指定则自动触发对应 connector 的实时数据拉取  

## 使用方式

1. 在百炼控制台创建并发布知识库、Memory Library 或 Connector 实例；  
2. 获取对应资源 ID（如 `kb-xxx`、`mlib-yyy`、`conn-zzz`）；  
3. 发起请求时，在 `messages` 同级传入 `context` 字段（非 `messages[0].content` 内嵌）；  
4. 注意：`context` 仅在 `stream=false` 模式下生效；流式响应暂不支持上下文注入。

## 限制和注意事项

- 单次请求 `context` 总大小上限为 2MB（含所有嵌套内容），超限返回 `400 Bad Request`；  
- RAG 与 Memory 的检索结果会以系统消息形式注入 prompt，计入模型 token 限额；  
- 同一 `session_id` 的 memory 读写操作非原子性，高并发场景下可能出现覆盖，建议业务层加锁或使用唯一 session；  
- Connector 数据拉取超时为 8 秒，失败时不中断主流程，但对应字段置空——此行为与 [Agent 上下文](../../raw/application-user-guide/agent-context/overview.md) 中描述的“阻塞等待”存在差异，请以实际 SDK 行为为准。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


