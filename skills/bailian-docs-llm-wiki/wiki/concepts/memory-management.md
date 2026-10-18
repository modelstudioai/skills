# 记忆管理

记忆管理是百炼平台中用于持久化、检索和生命周期控制 Agent 对话历史与上下文状态的核心机制，支撑多轮交互的连贯性与个性化响应能力。它并非单一存储组件，而是融合会话级缓存、用户级长期记忆、向量/键值双模存储及自动 TTL 管控的统一抽象层。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agent**：开箱即用的记忆能力，由平台全自动管理。默认启用 `vector` 类型 Memory Store（支持语义检索），可选 `kv` 模式（仅精确匹配）；记忆条目按 `session_id` 或 `user_id` 隔离，自动注入 LLM 提示词，并参与 RAG 重排序与工具调用决策链。
  
- **Flow Agent**：通过 `enable_memory: true` 显式开启会话记忆；依赖 `session_id` 维持上下文连续性；若需跨会话记忆，须配合组件类 API（如 `/memories` 接口）手动读写长期记忆体（注意：该能力已标记为“旧版”，推荐迁移到 Managed Agent 的统一 Memory Store）。

- **Sandbox Agent**：**不提供内置记忆管理**，开发者必须自行实现：例如使用 `session_id` 作为 key 存储于 Redis、或在沙箱内存中维护 `dict` 缓存。平台仅保证 `session_id` 在单次请求链路中透传，不提供持久化、过期、检索等任何辅助能力。

- **Agent Context 框架**：记忆作为 `context_config.memory` 子模块参与上下文构建。支持两种作用域：
  - `type: "session"`（默认）：绑定 `session_id`，1 小时无访问自动过期（可配 `memory_ttl_seconds`）；
  - `type: "user"`：需配合身份认证（如 OIDC [Token](token.md)），实现跨设备、跨会话的用户级记忆，未认证时自动降级为 session 级。

> ⚠️ 注意：全局共享记忆（global memory）功能已于 v2.3.0 下线；所有记忆均按 scope 隔离，无隐式跨用户/跨应用共享。

## 关键参数和配置

| 参数 | 位置 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enable_memory` | Agent 创建参数（Managed / Flow） | boolean | `true`（Managed）、`false`（Flow） | 控制是否启用平台托管记忆；Sandbox 中无效 |
| `memory_store_type` | Managed Agent API `POST /v1/agents` body | string | `"vector"` | 可选 `"vector"`（支持语义检索）或 `"kv"`（仅 key 精确查，实验性，生产禁用） |
| `memory_ttl_seconds` | Agent Context `context_config.memory` | integer | `3600`（1 小时） | 单条记忆存活时间；设为 `0` 表示永不过期（慎用，避免内存泄漏） |
| `context_window_size` | Agent Context 全局配置 | integer | `32768` | 记忆 + RAG + prompt 总 token 上限；超限时按 LRU 裁剪最旧记忆条目（RAG 优先保留） |
| `session_id` | 所有 `/chat` 或 `/messages` 请求体/路径 | string | — | 必填（除首次创建 session 外），用于绑定和检索对应记忆上下文 |

## 面向开发者，简洁实用

- ✅ **首选 Managed Agent**：若需可靠、开箱即用的记忆，优先选用 Managed Agent —— 它自动处理存储、检索、过期、安全隔离与模型提示注入，无需代码干预。
- ✅ **Flow Agent 记忆 = 会话粘性**：`enable_memory: true` 仅保障同一 `session_id` 内的历史可见；如需用户画像或历史汇总，应在 Flow 中插入自定义节点调用 Managed Agent 的 Memory API 或外部数据库。
- ❌ **Sandbox 不代管记忆**：不要依赖平台；使用 `session_id` 作为 key，结合百炼提供的 `redis://` 连接串（通过环境变量 `REDIS_URL` 获取）或本地 `dict` 实现轻量缓存；注意沙箱无持久化，进程重启即丢失。
- 🔍 **调试技巧**：调用 `/v1/sessions/{session_id}/messages` 可查看当前 session 已加载的记忆摘要；日志中搜索 `memory_loaded_count` 字段确认实际注入条目数。
- 🛑 **避坑提醒**：`kv` 模式不支持语义检索，且为实验性；`memory_ttl_seconds=0` 在高并发场景易导致内存溢出；跨 session 复用 `session_id` 将造成记忆污染。

## 关联主题页

- [agent development](../guides/agent-development.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)


