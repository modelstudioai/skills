# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、跨会话、可编程的持久化记忆能力**，用于显式存储和检索用户事实、偏好、行为画像等关键上下文信息。它不依赖模型内部隐式状态，而是通过独立的存储引擎与标准化 API 实现强一致性、低延迟的读写，是构建高一致性、个性化智能体的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆在百炼平台中并非单一实现，而是根据应用形态和调用路径呈现为**三层抽象、统一语义**的协同能力：

- **API 直接调用层（`/v1/memory/*`）**：面向需要精细控制记忆生命周期的开发者。通过 `POST /v1/memory/fragments` 写入事实（如 `"user_email"`）、`POST /v1/memory/profiles` 绑定用户画像（需 `profile_id`），再在 `/v1/chat/completions` 中启用 `enable_long_term_memory: true`，系统自动注入相关记忆片段至模型输入。此方式适用于定制化对话服务、CRM 集成等场景。

- **Agent 上下文层（`context.memory`）**：在 Agent 编排中作为 `context` 的子模块启用（`context.memory.enabled = true`）。此时记忆以 `memory_id` 为标识，支持 LRU 回溯最近 100 条交互记录（会话级短期记忆），但**不自动关联用户画像或跨会话事实**；若需长期关联，必须显式复用同一 `memory_id` 或结合 `profile_id` 手动注入。

- **Managed Agent / Flow Agent 层（`Memory Store` / `Memory` 组件）**：在 Managed Agents API 中，`Memory Store` 提供键值对 + TTL 的轻量存储，常用于临时缓存会话中间状态；在 Flow Agent API 中，`Memory` 是独立资源实体（`/memories`），支持分页列表与全量管理，适用于工作流编排中需跨步骤共享结构化数据的场景。二者均需开发者主动读写，**不参与自动上下文注入**。

> ✅ 关键区别：只有 **`/v1/memory/*` + `enable_long_term_memory: true`** 组合支持「自动记忆注入」——即系统根据当前 `profile_id` 和对话语义，自动检索并拼接最相关的事实与画像字段到 prompt 中。其他路径均为手动管理，需自行构造上下文。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `enable_long_term_memory` | `/v1/chat/completions` 请求体外层 | boolean | 否 | 启用自动记忆注入，默认 `false`；**仅流式请求（`stream: true`）生效** |
| `profile_id` | 请求头 `x-profile-id` 或 `messages[0].profile_id` | string | 是（启用 LTM 时） | 用户全局唯一 ID（如 OpenID/UUID），用于关联画像与事实 |
| `fragment_key` | `/v1/memory/fragments` 请求体 | string | 是 | 事实记忆的语义键名（如 `"shipping_address"`），建议小写+下划线 |
| `ttl_seconds` | `/v1/memory/fragments` 或 `/v1/memory/profiles` 请求体 | integer | 否 | 过期时间（秒），默认 `31536000`（1 年）；设为 `0` 表示永不过期 |
| `memory_id` | `/v1/memory/profiles` 请求体（可选） | string | 否 | 用户画像唯一标识，未提供时由系统生成；可用于精确覆盖更新 |

> ⚠️ 注意事项：
> - 单个 `profile_id` 下最多存储 1000 个字段（含嵌套），单个 `fragment` 值上限 8192 字符；
> - 高并发写同一 `fragment_key` 存在约 1–3 秒最终一致性延迟；
> - 删除操作暂不开放，过期记忆自动清理；非过期记忆需联系技术支持清除。

## 面向开发者，简洁实用

- **快速上手三步走**：  
  1. 写入用户画像：`POST /v1/memory/profiles`，Body `{ "profile_id": "u_123", "age_group": "25-34", "preferred_language": "zh" }`  
  2. 写入事实记忆：`POST /v1/memory/fragments`，Body `{ "fragment_key": "last_order_id", "value": "ORD-7890", "profile_id": "u_123" }`  
  3. 对话中启用：调用 `/v1/chat/completions`，Header 加 `x-profile-id: u_123`，Body 外层加 `"enable_long_term_memory": true`，且 `stream: true`

- **调试技巧**：  
  - 查询画像：`GET /v1/memory/profiles/u_123`  
  - 按键查事实：`GET /v1/memory/fragments/last_order_id?profile_id=u_123`  
  - 语义搜索（实验性）：`POST /v1/memory/fragments/search`，Body `{ "query": "用户最近下的订单号是什么？" }`

- **避坑指南**：  
  - ❌ 不要混用 `context.memory.enabled` 和 `enable_long_term_memory`：前者是会话回溯，后者是用户画像注入，机制完全不同；  
  - ❌ 不要在非流式请求中依赖 `enable_long_term_memory`——它不会生效；  
  - ✅ 优先使用 `profile_id` 而非 `session_id` 管理长期记忆，确保跨设备、跨会话一致性；  
  - ✅ 敏感字段（如手机号、邮箱）建议加密后存入 `fragments`，平台不提供内置加密。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [application component api reference](../api/application-component-api-reference.md)


