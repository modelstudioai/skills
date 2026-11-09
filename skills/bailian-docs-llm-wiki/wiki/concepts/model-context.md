# 模型上下文

模型上下文（Model Context）是百炼平台中用于向大语言模型注入运行时所需外部信息的统一机制，它决定了模型在单次推理过程中可感知和利用的知识边界、历史状态与实时数据。该机制不改变模型权重，而是通过结构化组装并前置注入 `system_prompt` 末尾的方式，动态扩展模型的“认知视野”，是实现 RAG、记忆增强、多源协同等高级能力的基础载体。

## 在百炼平台的不同场景中，这个概念如何使用

模型上下文并非独立功能模块，而是贯穿多个核心能力的底层支撑机制，其具体形态和注入方式依使用场景而异：

- **Agent 场景**：作为 `agent context` 的核心实现，模型上下文由平台自动组装 RAG 检索结果、[长期记忆](long-term-memory.md)（observation/skill）、Connector 实时数据、ParseX 解析内容四类信息，并以 `<context>...</context>` 标签包裹后注入 `system_prompt` 末尾。开发者无需手动拼接，只需在 Agent 配置中声明 `context_type` 及对应参数。
  
- **RAG API 调用**：当通过 `/api/v2/apps/knowledge/chat` 等接口发起知识问答时，模型上下文由 RAG 服务端隐式构建——检索出的 top-k 文档片段经重排序后，按相关性降序拼接为纯文本块，作为 `context` 字段注入模型输入（等效于 `system_prompt + "\n<context>..."`）。此过程对调用方透明，但可通过 `rerank_top_n`、`hybrid_rerank` 等参数调控上下文质量。

- **[长期记忆](long-term-memory.md)集成**：调用 `memory_nodes/search` 接口返回的记忆节点（含 `score` 和 `content`）本身即为待注入的上下文候选；开发者需在构造请求时，将高分记忆条目显式拼入 `system_prompt` 或 `messages[0].content` 中，平台不自动注入。这是唯一需开发者主动参与上下文组装的场景。

- **插件（Plug-in）调用**：插件本身**不提供模型上下文**。插件执行是独立于模型推理的异步动作，其返回结果（如搜索摘要、计算结果）会作为 `tool_calls` 响应被模型接收，并参与后续 `tool_response` 轮次的 prompt 构建——此时插件输出成为*下一轮*推理的上下文组成部分，而非当前轮次的初始上下文。

- **应用（Application）调试与部署**：在控制台测试窗或 API 调用中，若启用 RAG 或 Memory 功能，模型上下文即按对应规则自动注入；若仅使用基础模型 API（如 `/v1/services/aigc/text-generation`），则无上下文注入能力，需开发者自行管理 prompt 结构。

## 关键参数和配置

| 参数名 | 所属场景 | 类型 | 说明 | 是否必填 |
|--------|----------|------|------|----------|
| `context_type` | Agent | string \| string[] | 指定上下文来源类型：`"rag"`、`"memory"`、`"connector"`、`"parsex"`，支持组合（如 `["rag", "memory"]`） | 是 |
| `rag_config.kb_ids` | Agent | string[] | 当启用 `"rag"` 时，指定要检索的知识库 ID 列表 | 条件必填 |
| `memory_config.scope` | Agent | string | 当启用 `"memory"` 时，取值 `"user"`（用户级）、`"session"`（会话级）或 `"global"`（全局共享） | 条件必填 |
| `connector_config.connector_id` | Agent | string | 当启用 `"connector"` 时，指定已注册的 Connector ID | 条件必填 |
| `parsex_config.parsex_id` | Agent | string | 当启用 `"parsex"` 时，指定 ParseX 解析任务 ID | 条件必填 |
| `rerank_top_n` | RAG API / Agent | number | 控制最终注入模型的上下文片段数量（默认 3，最大 10） | 否（有默认值） |
| `search_filters` | RAG API | object | 对检索结果按 `doc_id`、`tags` 或自定义 meta 过滤，影响实际注入内容 | 否 |

> ⚠️ 注意：所有上下文内容均计入模型总 token 限制（当前上限 8192 tokens）。超限时平台自动截断，优先级顺序为：RAG > Memory > Connector > ParseX。建议通过 `debug: true` 开启调试日志，查看 `context_summary` 字段确认实际注入内容。

## 面向开发者，简洁实用

- ✅ **做对的事**：  
  - Agent 场景：专注配置 `context_type` 和对应 ID，让平台自动组装上下文；  
  - RAG 场景：调用 `/knowledge/chat` 即可获得上下文增强的响应，无需手动处理检索逻辑；  
  - 记忆场景：调用 `search` 获取高分记忆后，**手动拼入 `system_prompt`**（这是唯一需要你动手的地方）；  
  - 插件场景：理解插件输出是 *下一轮* 上下文，不是本轮初始上下文。

- ❌ **避免踩坑**：  
  - 不要在 `system_prompt` 中硬编码知识库内容或记忆片段——这会绕过平台的重排、过滤与 token 管理；  
  - 不要混用不同场景的上下文参数（如在 RAG API 请求中传 `context_type`）；  
  - 不要假设 `qwen-turbo` 支持完整上下文——它仅支持基础 memory 注入，不支持 RAG/Connector/ParseX；  
  - 不要忽略 `context_summary` 调试字段——它是验证上下文是否按预期注入的最直接依据。

- 🛠️ **快速验证**：  
  在 Agent 测试窗开启 `debug: true`，观察返回 JSON 中的 `context_summary` 字段；若为空或缺失关键内容，请检查：  
  ① 对应 KB/Connector/ParseX 是否处于 `active` 状态；  
  ② `kb_ids` 等 ID 是否拼写正确且归属同一业务空间；  
  ③ 总 token 是否超限（可通过 `usage.total_tokens` 辅助判断）。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [plug in](../guides/plug-in.md)
- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [application support](../guides/application-support.md)


