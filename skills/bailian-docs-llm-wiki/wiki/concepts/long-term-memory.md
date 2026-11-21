# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于跨会话、跨请求地保存和检索用户偏好、行为特征、历史交互等关键上下文信息。它以细粒度、可检索、可配置的方式支撑个性化与连贯性体验，是构建生产级智能体的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 直接调用（`/v1/memory/fragments` 等）**：开发者通过 RESTful 接口显式管理记忆片段（Fragment），适用于需要精确控制写入时机、内容结构或元数据过滤的场景（如用户设置同步、多步任务状态快照）。  
- **Agent 上下文（`context.memory.type = "user"`）**：在 Agent 配置中启用 `user` 级别 memory，平台自动基于 `user_id` 注入匹配的长期记忆片段，无需手动调用检索接口；适用于客服、个人助理等需持续理解用户身份与偏好的场景。  
- **Managed Agents API（`enable_memory: true`）**：在托管式 Agent 的 `/chat` 请求中启用该开关，系统将自动关联其绑定的 Memory Store，并在模型推理前注入相关 fragment；适合标准化工作流，降低状态管理复杂度。  
- **Sandbox 自定义开发**：通过 Python SDK（`bailian-sdk>=1.12.0`）调用 `memory_fragment.upsert()`、`memory_fragment.retrieve()` 等封装方法，在自研逻辑中灵活组合长期记忆与短期会话状态，实现混合记忆架构。

> ⚠️ 注意：长期记忆仅对 `qwen-max`、`qwen-plus` 和 `qwen-turbo`（v202409+）原生生效；其他模型需显式设置 `enable_long_term_memory: true` 并接受服务端降级处理（如仅注入元数据摘要）。

## 关键参数和配置

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `fragment_id` | string | 服务端生成 | 建议使用业务主键（如 `user:123:settings`），便于后续精准读写与清理 |
| `ttl_seconds` | integer | `2592000`（30 天） | 取值范围：`3600`–`31536000`（1 小时至 1 年）；设为 `0` 将返回 `400` 错误，不支持永不过期 |
| `metadata` | object | `{}` | 键值对（字符串/数字/布尔），最多 16 个 key，总大小 ≤ 4KB；用于 `filter` 检索（如 `{"category": "preference", "version": 2}`） |
| `enable_auto_injection` | boolean | `true` | 控制本次 `/v1/chat/completions` 请求是否自动注入匹配 fragment；设为 `false` 时需手动调用 `/v1/memory/retrieve` |
| `top_k`（检索时） | integer | `5` | `/v1/memory/retrieve` 返回的最大条目数，上限 `20` |

- **容量限制**：单个 `user_id` 最多存储 **5000 个 fragment**；超出写入失败（HTTP `429`）。  
- **内容限制**：单个 fragment 的 `content` 字段最大长度为 **65536 字符**，超长需预处理（截断、分片或摘要）。  
- **延迟影响**：启用 LTM 后，平均请求延迟增加 **80–200ms**（取决于 fragment 数量与检索复杂度）；高并发场景建议对高频 `user_id` 进行缓存预热。

## 面向开发者，简洁实用

- ✅ **推荐实践**：  
  - 使用 `fragment_id` 显式标识业务语义（避免随机 ID），例如 `profile:123`, `order:456:summary`, `feedback:789:rating`；  
  - 将用户画像类字段（如 `timezone`, `language`, `theme_preference`）存为独立 fragment，配合 `metadata` 分类，提升检索精度；  
  - 在 Sandbox 或 Flow Agent 中，优先使用 SDK 封装方法（如 `memory_fragment.upsert(content, fragment_id, metadata)`），而非手拼 HTTP 请求体。

- ❌ **避坑提示**：  
  - 不要依赖 `ttl_seconds=0` 实现“永久记忆”——该值非法，必须设为有效正整数；  
  - 不要在单次请求中写入大量 fragment（如循环插入 100+ 条），应批量聚合后分批提交；  
  - 用户画像（Profile）为只读视图，由系统自动聚合生成，**不可直接写入或修改**；  
  - 启用 LTM 后，务必监控 `429 Too Many Fragments` 错误，及时清理过期或冗余 fragment（调用 `DELETE /v1/memory/fragments/{fragment_id}`）。

- 🔧 **调试建议**：  
  - 开发阶段开启 `enable_auto_injection: false`，先手动调用 `/v1/memory/retrieve` 验证检索逻辑；  
  - 使用 `metadata` 中的 `debug: true` 标记临时 fragment，便于灰度验证后批量清理；  
  - 查看响应头 `X-Bailian-Memory-Hit-Count` 可获知本次自动注入的实际 fragment 数量。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent development](../guides/agent-development.md)


