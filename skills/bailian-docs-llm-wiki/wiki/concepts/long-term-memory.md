# 长期记忆

长期记忆是百炼平台提供的结构化、可检索、跨会话持久化的用户与业务知识存储服务，用于沉淀事实（如偏好、日程）、技能（如工具调用流程）和用户画像等关键信息，支撑 Agent 的个性化、连贯性与自主进化能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 运行时上下文**：在 `agent context` 中启用 `memory_config.enabled: true` 后，Agent 会自动将当前 session 的关键对话片段（如用户确认的地址、选择的选项）写入长期记忆库；该记忆不随 session 结束而清除，后续调用可通过语义检索复用。注意：此模式下 Memory 仅作「自动摘要写入 + 检索增强」，不替代手动管理的记忆库 API。
  
- **结构化记忆管理（推荐新项目使用）**：通过 `long term memory new` API 直接操作记忆库，支持三类记忆类型：
  - `observation`：记录用户显式声明或隐式表达的事实（如“我不吃香菜”“会议改到周五下午”）；
  - `skill`：存储可复用的执行逻辑（如“订外卖需依次调用地址校验→商户搜索→下单→支付”）；
  - `profile`：基于预定义 schema（`CreateProfileSchema`）从对话中异步抽取结构化用户画像（如年龄、职业、兴趣标签），供后续精准决策。

- **Flow Agent 工作流编排**：旧版 `Memory`/`MemoryNode` 接口（已标记为遗留）仍可用于简单 key-value 存储，但**不支持语义检索、多类型隔离与画像抽取**；新项目应统一迁移到 `long term memory new` 服务。

- **RAG 场景补充**：长期记忆 ≠ 知识库（Knowledge Base）。知识库面向文档级批量导入与 chunk 检索，适用于通用领域知识；长期记忆面向用户/会话粒度的动态事实沉淀，强调低延迟写入、高精度召回与强业务语义绑定。二者可协同使用（例如：RAG 提供产品说明书，长期记忆提供该用户的历史维修记录）。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必填 |
|------|------|------|------|----------|
| `user_id` | 请求 Body 或 Query | string | 用户唯一标识，实现跨用户记忆隔离 | ✅ |
| `project_id` / `project_ids` | Body | string / string[] | 项目 ID（最多 5 个），用于路由记忆类型（`observation`/`skill`）及权限控制 | ⚠️ 推荐填写，否则落入默认库 |
| `profile_schema` | Body | string | 用户画像模板 ID；传入后触发异步画像抽取 | ❌（仅需画像时填写） |
| `top_k`, `min_score`, `memory_types` | `SearchMemory` Body | integer / number / string[] | 检索控制：返回数量、最小相似度阈值（仅 `plan_version=pro` 生效）、过滤记忆类型 | ❌（按需） |
| `plan_version` | Body | string | `"pro"`（启用 Rerank、`min_score` 过滤）或 `"lite"`（基础向量检索），默认 `"pro"` | ❌（建议显式指定） |
| `memory_library_id` | Body / Query | string | 记忆库 ID；不传则使用业务空间默认库 | ❌ |

> 💡 开发提示：  
> - 写入优先用 `POST /add-async`（异步），尤其含图片、工具调用或多轮上下文时；同步 `/add` 仅适用于纯文本、<1KB 的实时场景。  
> - 检索时务必传 `messages` 字段（如 `[{"role": "user", "content": "我上次订的咖啡是什么口味？"}]`）作为查询语义，而非 raw text。  
> - 用户画像首次查询可能为空，需轮询 `/profile_schemas/{id}/user_profile?user_id=xxx` 直至 `status == "completed"`。

## 面向开发者，简洁实用

- **快速起步**：  
  1. 控制台 → [记忆管理](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) 创建记忆库；  
  2. 调用 `POST /add-async` 写入记忆（带 `user_id` 和 `project_id`）；  
  3. 调用 `POST /memory_nodes/search` 检索（传 `user_id` + 查询消息）。

- **SDK 推荐**：使用 `agentscope-runtime`（已封装鉴权、重试、异步轮询），避免手写 HTTP 轮子。

- **避坑指南**：  
  - ❌ 不要混用新旧记忆接口（`long term memory new` vs `flow agent api` 中的 `Memory`）；  
  - ❌ 不要将大文件、日志全量存入长期记忆——它不是对象存储，而是语义知识中枢；  
  - ✅ 多项目共用同一 `user_id` 时，用不同 `project_id` 实现业务域隔离；  
  - ✅ 敏感字段（如手机号）写入前建议脱敏，平台不提供内置加密。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)
- [get started with agents](../guides/get-started-with-agents.md)


