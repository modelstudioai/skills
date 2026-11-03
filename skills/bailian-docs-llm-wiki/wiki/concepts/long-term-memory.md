# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、持久化、语义可检索的记忆存储能力**，用于在多轮对话、跨会话甚至跨用户场景中可靠保存关键信息。它不是临时上下文缓存，而是具备明确生命周期、类型区分和向量索引的生产级记忆基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）推理增强**：当调用支持 LTM 的模型（如 `qwen-max` v20240915+）时，系统可在生成响应前自动检索匹配的长期记忆，并将其注入提示词上下文，从而让 Agent “记住”用户偏好、业务事实或历史约定。
- **事实性知识管理**：通过 `memory_type: "fragment"` 存储可验证、非人格化的客观信息（例如“合同模板版本号为 v3.2”“API 接口变更于 2024-08-15 生效”），适用于合规、客服、技术支持等需强一致性的场景。
- **用户画像构建**：通过 `memory_type: "profile"` 存储聚合性、人格化属性（例如 `"preference": "technical_docs"`, `"language": "zh-CN"`, `"tier": "enterprise"`），支持个性化响应与分群策略；同一 `user_id` 的多次写入会自动合并字段，具备幂等性。
- **低代码/可视化编排集成**：在 Flow Agent 或 Managed Agent 的控制台配置中，可绑定已创建的长期记忆实例，无需编码即可启用记忆感知能力。
- **API 级精细控制**：开发者可通过 `/memories` REST 接口直接写入、批量操作或按 ID 查询记忆；也可在 `ChatCompletion` 请求中通过 `enable_retrieval: false` 显式禁用某次调用的记忆注入，实现动态上下文裁剪。

> ⚠️ 注意：长期记忆能力**严格依赖模型版本**——仅 `qwen-max`、`qwen-plus`、`qwen-turbo` 的 **v20240915 及之后版本**支持读写与自动注入；旧版模型或第三方模型调用时，LTM 相关参数将被忽略。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 约束 |
|--------|------|------|------|------|
| `memory_type` | string | 是 | 取值必须为 `"fragment"` 或 `"profile"`，决定记忆语义类型与生命周期策略 | 不可混用；类型决定元数据校验逻辑 |
| `memory_id` | string | 否 | 显式指定唯一 ID；不提供时服务端自动生成 UUIDv4 | 建议业务侧生成以保障幂等与可追溯 |
| `ttl_seconds` | integer | 否 | 过期时间（秒）；默认 `31536000`（1 年） | `fragment` 类型下设为 `0` 将被强制重置为默认值；`profile` 类型支持 `0`（永不过期） |
| `enable_retrieval` | boolean | 否 | 控制本次请求是否启用 LTM 检索，默认 `true` | 设为 `false` 可临时关闭记忆注入，适用于调试或确定性模式（`temperature=0`）场景 |

**其他重要限制**：
- 单条 `fragment` 的 `content` 最长 8192 字符；单条 `profile` 的 `profile_fields` 键值对 ≤ 100 个；
- 每个应用默认配额 **10 万条记忆**（按 `memory_id` 去重计数），超限返回 `429`；
- 检索结果默认最多返回 **5 条**，且仅在 `temperature > 0` 时参与上下文构建（确定性模式下不注入）；
- 所有记忆均通过向量化索引实现语义检索，无需关键词匹配。

## 面向开发者，简洁实用

- ✅ **优先使用新 API**：`/v1/applications/{app_id}/memories`（含 batch）是当前推荐接口；旧版 Flow Agent 的 `memoryId`/`memoryNodeId` 接口已标记为遗留，**新项目请勿采用**。
- ✅ **写入即生效**：`POST /memories` 后，下次匹配查询即可命中，无额外同步步骤。
- ✅ **Profile 自动合并**：对同一 `user_id` 多次写入 `profile`，字段自动 deep-merge（同 key 覆盖，新 key 追加）。
- ❌ **不要依赖 session_id 绑定 LTM**：长期记忆独立于会话（session），`session_id` 仅用于短期上下文快照（见 `agent context`），二者逻辑分离。
- 📌 **调试技巧**：在请求中添加 `"debug": {"return_retrieved_memories": true}`（若 SDK 支持），可直接查看本次检索命中的原始记忆内容与 score。

如需快速验证，可使用以下最小可行调用（Python SDK）：

```python
# 写入用户画像
client.memories.create(
    app_id="app-xxx",
    memory_type="profile",
    user_id="u_123",
    profile_fields={"industry": "finance", "timezone": "Asia/Shanghai"},
    ttl_seconds=0  # 永不过期
)

# 调用时启用记忆检索
response = client.chat.completions.create(
    model="qwen-plus-v20240915",
    messages=[{"role": "user", "content": "根据我的行业偏好，推荐一个报告模板"}],
    enable_retrieval=True  # 显式开启（默认即 true）
)
```

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent development](../guides/agent-development.md)


