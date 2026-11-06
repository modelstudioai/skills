# agent context

agent context 是 Agent 运行时所依赖的动态上下文环境，用于支撑其感知、推理与执行能力。它由知识库（RAG）、记忆（Memory）、外部连接器（Connector）及结构化解析组件（ParseX）共同构成，决定了 Agent 在每次调用中可访问的信息边界与行为依据。该机制是实现状态感知型、多轮协同式 Agent 的基础支撑 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。

## 支持的模型与功能

- **模型支持**：当前仅 Qwen 系列大模型（如 qwen-max、qwen-plus）原生支持完整的 agent context 语义解析；其他模型（如 Llama、GLM）需通过 `context_enhance: true` 显式启用上下文注入，且不保证 Memory 与 RAG 的联合检索效果 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。  
- **核心功能**：
  - RAG：从知识库实时检索相关文档片段；
  - Memory：读写短期对话历史与长期用户画像；
  - Connector：对接第三方系统（如 CRM、数据库）获取运行时数据；
  - ParseX：对非结构化输入（PDF、表格、邮件正文）进行语义切分与字段提取 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `context_sources` | array | `[]` | 指定启用的上下文源，如 `["rag", "memory", "connector"]`；未声明的源将被忽略 |
| `rag_top_k` | integer | `3` | RAG 检索返回的最大文档片段数 |
| `memory_window` | integer | `10` | Memory 中保留的最近对话轮次（按 message 数计） |
| `connector_timeout_ms` | integer | `5000` | Connector 调用超时时间，单位毫秒 |

> **注意**：`memory_window` 在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档中定义为“最大 token 数”，而本参数实际按 message 条目计数——二者语义不一致，以本表为准（SDK v2.4+ 实现）。

## 使用方式

1. 在 Agent 配置中显式声明 `context_sources`，例如：
   ```json
   {
     "context_sources": ["rag", "memory"],
     "rag_top_k": 5,
     "memory_window": 8
   }
   ```
2. 确保对应上下文模块已启用并完成初始化（如知识库已发布、Memory 已绑定用户 ID）；
3. 发起调用时，上下文将自动注入 prompt，并在 LLM 输出后触发后续动作（如 Connector 写回、Memory 更新）。

## 限制和注意事项

- 单次请求中 `context_sources` 最多启用 3 类（RAG + Memory + Connector / ParseX 三选至多三者），超出将报错 `context_source_limit_exceeded`；
- RAG 与 Memory 的混合检索暂不支持排序融合，结果按来源分别返回后拼接；
- ParseX 对图像内嵌文本（OCR）的支持需额外配置 `parsex_ocr_enabled: true`，且仅限 `qwen-vl` 模型可用；
- 所有上下文数据均在请求生命周期内临时加载，**不持久化到 Agent 全局状态**，如需跨会话复用，必须通过 Memory 的 `user_id` 显式隔离 [Agent 上下文](../../raw/application-user-guide/agent-context.md)。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


