# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**跨会话、结构化、用户级**的记忆管理能力，用于持久化存储和语义化检索用户事实性信息（如订单、地址、偏好事件）与静态画像特征（如语言习惯、兴趣标签），独立于单次对话上下文，支撑个性化、一致性和状态感知型智能交互。

## 在百炼平台的不同场景中如何使用

长期记忆在平台中存在三种技术形态，面向不同架构层级和使用诉求，开发者需根据模型类型、调用方式与功能需求选择适配方案：

- **Agent 场景（`qwen-agent-2.5+`）**：通过 `context_config.memory_library_id` 声明记忆库 ID，启用自动化的**会话级记忆注入**。该模式下，Agent 在每次调用时自动从指定记忆库中检索与当前 `session_id` 和 `user_id` 关联的近期记忆片段（基于 LRU 缓存策略），并作为上下文注入提示词。适用于多轮协作型 Agent，无需手动调用记忆 API，但仅支持读取，不开放写入控制。

- **通用大模型调用场景（`qwen-max`/`qwen-plus`/`qwen-turbo`）**：通过独立 `/v1/memory` 系列 REST API（`write`/`query`/`clear`）进行**显式、细粒度记忆操作**。必须携带 `user_id` 实现数据隔离，支持区分 `fact`（默认 TTL 30 天）与 `profile`（默认 TTL 1 年）两类记忆，适用于需自主控制记忆生命周期、构建用户档案或实现个性化推荐的业务逻辑。

- **Managed Agents 场景**：通过 `Memory Store` 组件提供**键值对 + TTL 的轻量级持久化存储**，由 Agent 运行时自动管理（如 `session_id` 绑定的临时状态）。该能力不支持自然语言查询，仅支持精确 key 查询与过期自动清理，适用于技能编排中的中间状态暂存（如表单填写进度、多步任务上下文），与前述两种“长期记忆”在语义、API 和用途上正交，建议避免混淆。

> ⚠️ 注意：三者互不兼容——Agent 的 `memory_library_id` 不能指向 `/v1/memory` 创建的记忆库；`/v1/memory` 写入的内容不会被 Agent 自动检索；Managed Agents 的 `Memory Store` 不接入统一记忆服务。

## 关键参数和配置

| 参数 | 所属场景 | 类型 | 说明 |
|------|----------|------|------|
| `memory_library_id` | Agent Context | string | 指向控制台创建的「记忆库」ID；需提前授权并发布；启用后自动注入相关记忆片段 |
| `user_id` | `/v1/memory` API | string | 必填，用于严格隔离用户数据；建议使用业务系统用户 ID（如 `uid_12345`），不可为空或泛化值（如 `"guest"`） |
| `memory_type` | `/v1/memory` API | `"fact"` 或 `"profile"` | 必填；决定存储结构、默认 TTL 和检索权重；二者不可混存于同一写入请求 |
| `ttl_seconds` | `/v1/memory` API | integer | 可选；`fact` 默认 2592000（30 天），`profile` 默认 31536000（1 年）；设为 `0` 表示永不过期（受配额约束） |
| `metadata` | `/v1/memory` API | object | 可选；最多 10 对字符串键值，仅用于 `query` 时的过滤条件（如 `{"source": "crm"}`），不参与语义匹配 |

- **配额限制（`/v1/memory`）**：单 `user_id` 下，`fact` 最多 1000 条，`profile` 最多 100 条；超出返回 `400 Bad Request`。
- **Agent 记忆缓存**：最大会话数 10,000，超限自动淘汰最久未访问项（LRU）；无单用户条目数限制，但受总容量约束。

## 开发者提示

- ✅ **优先选型**：若使用 `qwen-agent-2.5+` 且只需读取历史信息 → 配置 `context_config.memory_library_id`；若需写入、更新或构建用户画像 → 必须调用 `/v1/memory` API。
- ✅ **安全合规**：所有 `/v1/memory` 写入内容默认不参与训练、不出现在日志/审计导出中，但开发者须确保 `content` 字段已脱敏（如掩码手机号、哈希邮箱）。
- ❌ **禁止嵌套**：不要在 Connector 返回内容、RAG 检索结果或 Prompt 模板中动态拼接 `/v1/memory/query` 结果——所有记忆操作必须在应用层显式发起。
- 📌 **调试建议**：首次集成时，先用 `POST /v1/memory/write` 写入测试记忆，再用 `POST /v1/memory/query` 验证检索效果（如 query_text=`"用户住在哪？"`），确认 `user_id` 和 `memory_type` 匹配无误后再接入 Agent 或业务流。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [long term memory new](../api/long-term-memory-new.md)
- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)


