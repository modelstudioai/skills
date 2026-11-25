# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、跨会话、用户级状态持久化能力**，用于安全存储和高效检索用户画像、对话片段、业务上下文等关键信息。它独立于单次推理请求生命周期，支持向量语义检索与结构化查询双模态访问，是构建个性化、有状态智能体的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **多轮对话 Agent 中自动增强上下文**：在调用 `/v1/chat/completions` 或 `/v1/services/aigc/text-generation` 时，启用 `enable_long_term_memory: true` 并配置 `ltm_config`，平台将根据 `memory_id`（如 `user_id`）自动检索匹配的记忆片段（`fragment`），注入至 `system` 角色上下文，供模型实时参考。  
- **Agent 上下文（Agent Context）中显式声明**：在 `context.memory` 字段中传入 `{"user_id": "u-123", "session_id": "s-456"}`，系统将按用户粒度聚合记忆，并可选按会话隔离（避免跨会话信息泄露）。该方式与模型无关，适用于所有支持 `agent_mode` 的模型（如 `qwen-max`、`qwen-plus`）。  
- **独立记忆管理（非推理场景）**：通过专用 Memory API（如 `POST /v1/memory/fragments`、`POST /v1/memory/profiles/query`）直接写入、批量查询或软删除记忆，无需绑定任何模型调用，适合后台任务、用户建模、行为分析等异步场景。  
- **Flow Agent 与 Managed Agent 中统一接入**：在 Agent 创建或调用时设置 `enable_memory: true`（需已绑定 Memory 模块），平台自动启用记忆读写——写入内容默认基于当前 `user_id` 和 `session_id` 自动打标，支持后续向量检索。

> ✅ 提示：`fragment` 类型支持向量化（用于语义召回），`profile` 类型仅支持结构化查询（如按 `metadata.category` 精确过滤），二者不可混用索引。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `memory_id` | string | 否（推荐必填） | 用户级唯一标识。若未提供，平台生成 UUID；**强烈建议业务侧传入稳定 ID（如 `user_id`）**，以保障跨设备、跨会话一致性。 |
| `type` | string | 是 | 记忆类型，取值为 `"fragment"`（支持向量检索的文本片段）或 `"profile"`（结构化用户画像，不参与向量索引）。注意：旧版 `profile_type: "user"` 已废弃，使用即报 400。 |
| `ttl_seconds` | integer | 否 | 过期时间（秒），默认 `2592000`（30 天），最大 `31536000`（1 年）。**该值不可在单次推理请求中覆盖，由控制台全局策略或写入时指定为准。** |
| `embedding_model` | string | 否 | 仅对 `type="fragment"` 且含 `content` 时生效；默认 `text-embedding-v3`，**不支持切换为旧版 `text-embedding` 模型**。 |
| `ltm_config.top_k` | integer | 否（默认 3） | 推理时最多注入多少条匹配记忆（向量检索结果）。建议设为 1–5，避免上下文过载。 |
| `ltm_config.filter` | object | 否 | 结构化过滤条件，格式为 `{"metadata.key": "value"}`，支持嵌套字段（如 `{"metadata.source": "survey_v2"}`）。 |

> ⚠️ 注意事项：  
> - 单个 `memory_id` 下最多存 1000 个 `fragment` + 100 个 `profile`，超限返回 `429 Too Many Items`；  
> - `content` 长度上限 8192 字符，超长需分片；  
> - 删除为软删除，数据保留 7 天后物理清除；  
> - `session_id` 在 `context.memory` 中为可选，但**不填将导致该用户全部历史记忆被聚合检索，存在隐私风险**。

## 面向开发者：快速上手提示

- ✅ **写入一条用户偏好**：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/memory/fragments \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "memory_id": "u-123",
          "type": "fragment",
          "content": "用户偏好无糖冷泡茶",
          "metadata": {"category": "preference", "source": "onboarding"}
        }'
  ```

- ✅ **在推理中启用记忆注入**（Qwen 系列模型）：  
  ```json
  {
    "model": "qwen-max",
    "messages": [{"role": "user", "content": "推荐一款茶？"}],
    "parameters": {
      "enable_long_term_memory": true,
      "ltm_config": {
        "top_k": 2,
        "filter": {"metadata.category": "preference"}
      }
    }
  }
  ```

- ✅ **在 Agent Context 中启用**（通用方式，不限模型）：  
  ```json
  {
    "model": "qwen-plus",
    "messages": [...],
    "context": {
      "memory": {"user_id": "u-123", "session_id": "s-456"}
    }
  }
  ```

- ❌ 避免：在 `fragment` 写入时传 `profile_type`；在 `ltm_config` 中设置 `ttl_seconds`；对 `profile` 条目期望向量检索。  

长期记忆不是缓存，而是生产级用户状态中枢——请始终用 `memory_id` 对齐业务身份，用 `type` 明确数据用途，用 `filter` 精准控制注入范围。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent governance](../guides/agent-governance.md)


