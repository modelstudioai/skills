# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话记忆管理能力，用于将用户对话中的关键信息（如偏好、待办事项、固有属性）自动提取、持久化存储，并在后续交互中基于语义检索动态注入上下文，从而突破大模型单次调用的上下文窗口限制，实现个性化、连贯、有状态的智能体体验。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：在 Agent 2.0 中，长期记忆作为内置上下文增强能力，可零代码启用。平台在 `agent_end` 钩子自动调用 `AddMemory` 捕获对话摘要，在 `before_agent_start` 钩子自动执行 `SearchMemory` 并将高相关性记忆片段注入系统提示词，无需修改业务逻辑。
- **工作流（Workflow）应用**：通过集成 `@modelstudio/modelstudio-memory-for-openclaw` 插件，可在任意节点前后挂载记忆写入与召回逻辑；也可手动编排 `AddMemory` / `SearchMemory` API 节点，实现细粒度控制（例如仅对“设置提醒”类意图触发事实记忆写入）。
- **高代码应用（Serverless/K8s）**：开发者直接调用 DashScope 长期记忆 REST API（如 `/v2/apps/memory/add` 和 `/v2/apps/memory/memory_nodes/search`），在自定义 Python 函数中完成记忆的条件写入、多源融合检索与结果后处理。
- **Managed Agents 托管服务**：长期记忆与会话生命周期深度集成——`session_id` 自动映射到 `user_id`，会话恢复时默认加载该用户最新匹配的记忆，实现“无感状态延续”。
- **API 直接调用（Application Call）**：在 `application call` 请求中，可通过 `biz_params.memory_id` 显式指定要关联的长期记忆实例（需提前创建并授权），适用于多租户 SaaS 场景下的隔离记忆绑定。

> ✅ 提示：所有场景均以 `user_id` 为隔离边界，同一 `user_id` 下的事实记忆与用户画像自动共享，不同 `user_id` 完全物理隔离。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | 所有 API 请求体 | string | 是 | 记忆归属唯一标识，最大 64 字符；**必须与业务系统用户 ID 严格对齐**，不可使用会话 ID 或临时 token 替代。 |
| `messages` / `custom_content` | `AddMemory` 请求体 | array / string | 是（互斥） | `messages`：传入对话消息数组（最多 50 条），用于自动提取；`custom_content`：传入纯文本（≤512 字符），用于直接写入结构化事实。 |
| `profile_schema` | `AddMemory` 请求体 | string | 否 | 用户画像模板 ID；**不传则跳过画像提取，仅处理事实记忆**。首次使用需先调用 `CreateProfileSchema` 创建模板。 |
| `plan_version` | `AddMemory` / `SearchMemory` 请求体 | string | 否 | `"Pro"`（默认，启用 Rerank，精度高）或 `"Lite"`（跳过 Rerank，成本低）；大小写敏感，影响提取/检索质量与计费档位。 |
| `top_k` | `SearchMemory` 请求体 | integer | 否 | 返回最大条数，范围 `1–100`，默认 `10`。建议设为 `5–20` 平衡效果与性能。 |
| `min_score` | `SearchMemory` 请求体 | float | 否 | 相似度阈值，范围 `0.0–1.0`，默认 `0.3`；生产环境推荐 `0.5–0.7`，避免低质噪声注入。 |
| `meta_data` | `AddMemory` 请求体 | object | 否 | 键值对元数据，如 `{"category": "health_reminder", "source": "voice_input"}`，用于后续按标签精确过滤检索。 |

> ⚠️ 注意：`plan_version` 切换仅对**新写入/新检索**生效；历史记忆的提取策略与检索质量由其写入时的 `plan_version` 决定，不可 retroactively 修改。

## 面向开发者，简洁实用

- **快速验证三步走**：  
  1. `curl -X POST https://dashscope.aliyuncs.com/api/v2/apps/memory/add \  
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \  
     -H "Content-Type: application/json" \  
     -d '{"user_id":"u123","messages":[{"role":"user","content":"每天上午9点提醒我喝水"}]}'`  
  2. `curl "https://dashscope.aliyuncs.com/api/v2/apps/memory/memory_nodes/search?user_id=u123" \  
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \  
     -d '{"messages":[{"role":"user","content":"我的喝水提醒是什么？"}]}'`  
  3. 查看返回的 `memory_nodes` 是否包含正确提取的提醒项。

- **生产建议**：  
  - 为 `user_id` 建立业务映射表（如 `business_user_id → platform_user_id`），避免直接暴露平台 ID；  
  - 对高频查询场景，用 `meta_data.category` + `min_score=0.65` 组合过滤，降低无效召回；  
  - 用户画像提取为异步操作，`AddMemory` 返回后需等待 ≥3 秒再调用 `GetUserProfile`；  
  - `SearchMemory` 调用应置于 LLM 推理前，且结果需经 `min_score` 过滤后再拼接进 system [prompt](../guides/prompt.md)，防止低质记忆污染输出。

- **避坑指南**：  
  - ❌ 不要复用 `user_id` 表示不同用户（如用 session_id 代替）；  
  - ❌ 不要在 `AddMemory` 中遗漏 `profile_schema` 却期望提取画像；  
  - ❌ 不要将 `plan_version` 设为 `"pro"`（小写），必须为 `"Pro"`；  
  - ❌ 不要依赖 `ListMemory` 做实时检索——它不支持语义搜索，仅用于运维查看。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)


