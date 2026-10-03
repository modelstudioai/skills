# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**跨会话、用户级、结构化记忆管理服务**，用于在多轮对话与多次调用中持久化存储和语义化检索关键信息，突破大模型上下文窗口限制，实现个性化、连贯、状态一致的 AI 交互体验。它不依赖模型内部 token 位置，而是通过独立的存储-检索机制，将事实性信息与用户画像解耦管理。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆不是单一功能模块，而是贯穿多个核心能力的横切基础设施，按使用方式可分为三类：

- **自动提取式（被动写入）**：在 `application call` 或 `/v1/chat/completions` 请求中启用 `memory.write: true`，系统根据预设规则（`memory.rules`）从模型响应中自动抽取事实（如“明天下午3点开会”）或结构化画像（如“职业=医生”），并持久化。适用于对话流中自然浮现的关键信息沉淀。

- **主动调用式（显式读写）**：通过 Memory Library 的开放 API（如 `/add`, `/memory_nodes/search`）或 OpenClaw 插件的 `memory_store`/`memory_search` 工具，在 Agent 生命周期钩子（如 `before_agent_start`）中按需写入原始内容或检索相关记忆。适用于用户明确指令（如“记住我的邮箱”）或需要精细控制记忆粒度的场景。

- **托管集成式（零代码启用）**：在 Managed Agents 或智能体控制台中绑定已配置的记忆库，平台自动在每次会话开始前注入匹配记忆、在会话结束后触发规则提取。开发者无需修改代码，即可获得开箱即用的跨会话状态保持能力。

> ✅ 关键区别：`memory.write`（API 层）和 `AddMemory`（Memory Library API）均基于规则抽取；而 `memory_store`（OpenClaw）支持绕过规则、直接写入任意字符串，二者定位互补，不可混用。

## 关键参数和配置

| 参数 | 说明 | 推荐值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | **必填**，用户唯一标识，实现记忆完全隔离 | 业务侧稳定 ID（如 `uid_12345`） | 不同 `user_id` 的记忆物理隔离；OpenClaw 插件强制要求此字段作为 Header `x-bailian-user-id` 传递 |
| `plan_version` | 检索策略版本（`Pro`/`Lite`） | `Pro`（默认） | `Pro` 启用 Rerank，精度高；`Lite` 关闭 Rerank，成本低但召回质量略降；Search 请求中可独立指定，不依赖写入时配置 |
| `top_k` | 单次检索返回最大条数 | `5`（插件） / `10`（API） | 范围 1–100；建议 ≤20，避免噪声干扰 Prompt |
| `min_score` | 相似度阈值（0.0–1.0） | `0.5–0.7` | 默认 `0.3`（API）易召回低质结果；设为 `0.6` 可显著提升注入质量；低于阈值的记忆被静默过滤 |
| `meta_data` | 自定义元数据（JSON 对象） | `{"source": "chat", "priority": "high"}` | 强烈建议添加，用于后续 `metadata_filter` 精确筛选（如仅召回来自知识库的记忆） |
| `memory.rules` | 写入规则数组（仅 API 层） | `[{"field":"email","source":"response.content.email","type":"fact"}]` | `source` 路径不存在时**静默忽略**，不报错；`type: "profile"` 时，空值或纯数字将被跳过写入 |

> ⚠️ 限制提醒：单 `user_id` 下，事实记忆上限 500 条，用户画像上限 100 条；超出返回 `400 Bad Request`。默认 TTL 为 90 天，可在记忆库规则中自定义为 7/30/180 天或永不过期。

## 面向开发者，简洁实用

- **快速验证**：开通服务后，3 步闭环：<br>① `POST /add` 写入测试消息（带 `user_id`）→ ② 控制台查提取结果 → ③ `POST /memory_nodes/search` 检索验证<br>✅ 无需模型适配，所有 Qwen 系列模型（`qwen-max`/`qwen-plus`/`qwen-turbo`/`qwen3-*`）均支持。

- **生产建议**：
  - 优先使用 `Pro` 策略 + `min_score: 0.6` + `top_k: 10` 平衡效果与成本；
  - 用户画像务必提前配置 `profile_schema_id` 并传入请求，首次提取可能异步延迟，建议重试逻辑；
  - 敏感信息（如手机号、身份证）写入前需自行脱敏，平台默认启用**记忆内容安全检测**（自动拦截违规内容）；
  - 避免高频调用：`/add` ≤ 120 QPM，`/search` ≤ 300 QPM，超限返回 `429`，需实现指数退避重试。

- **调试技巧**：  
  - 使用 `GET /memory_nodes?user_id={id}` 查看原始记忆列表及 `score` 字段，快速定位低分噪声；  
  - 在 `memory.rules` 中添加 `"debug": true`（若 SDK 支持）可返回提取过程日志；  
  - OpenClaw 插件中，`memory_search` 返回结果含 `relevance_score`，可直接用于排序过滤。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [application call](../api/application-call.md)
- [managed agents](../guides/managed-agents.md)
- [security guide](../guides/security-guide.md)


