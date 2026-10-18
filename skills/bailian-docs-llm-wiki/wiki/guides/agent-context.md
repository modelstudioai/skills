# agent context

agent context 是 Agent 执行过程中用于支撑决策与响应的关键信息集合，包括知识库检索结果（RAG）、历史对话记忆（Memory）、外部系统连接器（Connector）及结构化内容解析（ParseX）等模块。它决定了 Agent 能“知道什么”和“记住什么”，直接影响响应准确性与任务完成能力。该机制通过统一上下文管理框架实现多源信息的动态注入与生命周期控制。

## 支持的模型/功能

当前 agent context 仅在 `qwen-plus`、`qwen-max` 及 `qwen2.5-72b-instruct` 等支持 tool calling 与 long-context 的模型上完整启用；轻量模型（如 `qwen-turbo`）仅支持 Memory 的基础会话级缓存，不支持 RAG 或 Connector 动态注入。所有 context 模块均需在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 文档中声明启用，未显式配置的模块默认不参与上下文构建。

## 关键参数

- `context_window_size`: 控制总上下文 token 长度上限（含 prompt + memory + RAG chunks），默认为 32768，最大支持 65536（需模型支持）  
- `memory_ttl_seconds`: 记忆条目存活时间，默认 3600（1 小时），设为 `0` 表示永不过期  
- `rag_top_k`: RAG 检索返回的最大 chunk 数，默认 `3`，超过 `10` 可能触发截断警告  
- `connector_timeout_ms`: 外部服务调用超时，默认 `5000`，低于 `1000` 不推荐用于生产环境  
详细参数说明见 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的“配置参考”章节。

## 使用方式

1. 在 Agent 创建时通过 `context_config` 字段声明启用模块：  
   ```json
   "context_config": {
     "memory": {"enabled": true, "type": "session"},
     "rag": {"enabled": true, "knowledge_base_id": "kb-xxx"},
     "connector": {"enabled": true, "connector_id": "conn-yyy"}
   }
   ```
2. RAG 和 Connector 的输入数据需提前通过对应服务注册（参见 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md) 和 [Connector](../../raw/application-user-guide/agent-context/overview.md) 文档）；  
3. ParseX 解析结果自动作为 context 的一部分注入，无需额外配置，但需确保上传文件格式在 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 支持列表内。

## 限制和注意事项

- 单次请求中 RAG 与 Memory 合计 token 超过 `context_window_size` 时，系统按 LRU 策略丢弃最旧 memory 条目，**不**丢弃 RAG 内容；  
- Memory 的 `session` 类型仅在同一个 `session_id` 下有效，跨 session 不共享；`user` 类型需配合用户身份认证，否则降级为 `session`；  
- > **注意**：原始文档中 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 提到“支持全局 memory 缓存”，但该功能已于 v2.3.0 下线，实际行为以 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中“Memory 生命周期”章节为准；  
- Connector 返回的非 JSON 响应（如纯文本或二进制）将被忽略，不进入 context；  
- 所有 context 模块均不支持运行时热更新配置，修改后需重建 Agent 实例。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


