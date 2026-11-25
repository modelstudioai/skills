# agent context

`agent context` 是百炼平台中用于定义 Agent 行为边界与知识来源的核心机制，它决定了 Agent 在执行任务时可访问的外部信息、历史记忆及数据连接能力。通过组合 Knowledge、Memory 和 Connector 等模块，开发者可灵活构建具备上下文感知能力的智能体。该机制不依赖模型自身参数调整，而是通过运行时注入结构化上下文实现行为定制。

## 支持的模型/功能

当前 `agent context` 机制适用于所有支持 `agent_mode: true` 的百炼托管模型（如 Qwen-Max、Qwen-Plus、Qwen-Turbo），且与模型推理层解耦，因此无需更换模型即可启用上下文增强能力。其核心功能模块包括：  
- **Knowledge**：基于向量检索的外部知识库接入（原 RAG 功能），支持文档上传、自动切片与语义召回；  
- **Memory**：[长期记忆](../concepts/long-term-memory.md)存储与检索，支持会话级和用户级记忆隔离；  
- **Connector**：对接企业内部系统（如 CRM、ERP、数据库）的标准化数据通道；  
- **ParseX**：非结构化文档（PDF/Word/Excel 等）的解析与结构化提取能力。  
详见 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md)。

## 关键参数

在调用 `/v1/chat/completions` 或使用 SDK 创建 Agent 实例时，需通过 `context` 字段传入上下文配置对象：

```json
{
  "context": {
    "knowledge": { "kb_ids": ["kb-xxx"] },
    "memory": { "user_id": "u-123", "session_id": "s-456" },
    "connector": { "conn_id": "conn-789" },
    "parsex": { "file_ids": ["file-abc"] }
  }
}
```

各子模块均为可选，但至少需启用一项（如仅启用 `knowledge` 也合法）。参数字段名与类型严格区分大小写，缺失 `kb_ids` 数组或传入空数组将导致 Knowledge 模块静默禁用。更多字段说明请参考 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md)。

## 使用方式

1. **前置准备**：在控制台完成 Knowledge 库创建、Memory 初始化、Connector 授权及 ParseX 文件上传；  
2. **API 调用**：在请求体中嵌入 `context` 对象（如上所示），确保 `model` 参数指向支持 agent_mode 的模型；  
3. **SDK 调用**（Python 示例）：
   ```python
   client.chat.completions.create(
       model="qwen-max",
       messages=[{"role": "user", "content": "我的订单状态？"}],
       context={
           "knowledge": {"kb_ids": ["kb-xxx"]},
           "memory": {"user_id": "u-123"}
       }
   )
   ```
注意：`context` 必须作为顶层字段与 `messages`、`model` 并列，不可嵌套于 `extra_body` 或其他扩展字段中。完整接口规范见 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md)。

## 限制和注意事项

- 单次请求中 `context.knowledge.kb_ids` 最多支持 5 个知识库 ID；`context.parsex.file_ids` 最多支持 10 个文件 ID；  
- Memory 模块要求 `user_id` 必填，`session_id` 可选；若未提供 `session_id`，系统将按 `user_id` 聚合全部历史记忆，可能引发隐私泄露风险；  
- Connector 当前仅支持 HTTP/Webhook 类型，不支持直连数据库（该能力计划于 v2.3 版本上线，当前文档 [overview.md](../../raw/agent-context/overview.md) 中提及的“数据库直连”属过时描述）；  
> **注意**：`context.memory` 的 TTL（默认 30 天）不可通过 API 覆盖，控制台设置的全局 Memory 过期策略优先级高于单次请求参数；  
> **注意**：ParseX 解析结果缓存有效期为 24 小时，超时后需重新上传或调用 `parsex/refresh` 接口，[getting-started-overview.md](../../raw/agent-context/getting-started-overview.md) 中“永久缓存”的说法已失效。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


