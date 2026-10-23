# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、可持久化、显式可控**的用户级记忆存储与检索能力。它独立于模型参数和会话上下文，通过 API 显式创建、写入与关联，用于在多轮对话及跨会话场景中稳定保存用户事实性信息、行为偏好与结构化画像，确保记忆可审计、可更新、可隔离。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）调用场景**：在 `/v1/chat/completions` 或 `/v1/agents/{id}/chat` 等推理请求中，通过外层传入 `memory_id` 字段，平台将自动将该 memory 下关联的 **Fragments（事实记忆）** 和 **Profiles（用户画像）** 注入为系统上下文，供支持的模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）直接感知和引用。  
- **工作流（Workflow）与应用调用场景**：仅新版智能体应用（Agent 2.0）支持 `memory_id` 参数；工作流和旧版智能体不支持长期记忆注入，需自行通过 `biz_params` 或 Connector 接入外部存储。  
- **Agent 上下文（Agent Context）编排场景**：当 `context_type` 设置为 `"memory"` 或包含 `"memory"`（如 `["rag", "memory"]`）时，平台将根据 `memory_id` 拉取对应记忆数据，并按 `context_ttl` 缓存、按 `max_context_length` 截断后注入上下文。此时记忆内容以压缩摘要形式参与推理，不暴露原始键值结构。  
- **Flow Agent 组件管理场景**：旧版长期记忆（`CreateMemory` / `CreateMemoryNode` 等接口）仍可用，但属遗留能力，仅支持扁平化文本片段（`content` ≤ 200 字符），**不支持 Profiles、版本控制或 TTL**，新项目应优先使用新版 LTM API。  

> ⚠️ 注意：`memory_id` **不具备租户隔离**——不同 `app_id` 若复用同一 `memory_id`，将共享同一份记忆数据；敏感字段（如手机号、身份证号）必须由应用层完成脱敏后再写入。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_id` | string | ✅ | 记忆实例唯一 ID，由应用侧生成并维护；长度 1–64 字符，仅支持字母、数字、`-`、`_`；全局唯一且不可变更。 |
| `memory_type` | string | ❌ | 取值 `fragment`（默认）或 `profile`；决定后续读写接口路径（`/fragments` 或 `/profiles`）及语义行为。 |
| `ttl_seconds` | integer | ❌（仅 `fragment` 有效） | 过期时间（秒），范围 300–2592000（5 分钟–30 天），默认 86400（24 小时）；`profile` 永不过期。 |

- **配额限制**：单个 `memory_id` 最多存储 1000 条 fragment 或 100 条 profile；超出返回 `400 Bad Request`。  
- **删除语义**：调用 `DELETE /v1/memories/{memory_id}` 后，所有关联数据**立即物理删除且不可恢复**（强一致性）。  

## 面向开发者，简洁实用

- ✅ **只用三步即可启用**：  
  1. `POST /v1/memories` 创建 `memory_id`；  
  2. `POST /v1/memories/{id}/fragments` 写入键值对（如 `{"phone": "138****1234"}`）；  
  3. 在推理请求中添加 `"memory_id": "xxx"` —— 模型自动注入。  
- ✅ **严格模型兼容**：仅 `qwen-max`、`qwen-plus`、`qwen-turbo` 原生支持；其他模型（含 `llama-3-70b`）会静默忽略 `memory_id`，不报错但无效果。  
- ✅ **安全第一**：所有数据默认加密落盘，但**不提供字段级权限控制**；请勿写入明文敏感信息，务必前置脱敏（如掩码、哈希、泛化）。  
- ✅ **调试建议**：使用 `GET /v1/memories/{id}/fragments?limit=10` 快速验证写入结果；避免在生产环境高频轮询 `ListMemories`（受 1 秒限流约束）。  
- ❌ **避免踩坑**：不要复用 `memory_id` 跨应用；不要依赖旧版 Flow Agent 记忆接口开发新功能；不要在 `messages` 内容中拼接 `memory_id`（必须置于请求体顶层）。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [application call](../api/application-call.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent development](../guides/agent-development.md)


