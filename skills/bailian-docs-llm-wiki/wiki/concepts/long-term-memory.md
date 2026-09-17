# 长期记忆

长期记忆是百炼平台提供的结构化、语义驱动的跨会话用户状态存储与检索能力，用于突破大模型上下文窗口限制，实现用户偏好、关键事件、结构化属性等信息的持久化保存与智能召回。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：通过 `application call` API 的 `memory_id` 参数启用，自动在对话开始前注入相关记忆、结束时捕获新记忆。需在应用配置中开启“长期记忆”开关并发布。
- **记忆库（Memory Library）独立使用**：开发者可直接调用 `AddMemory` / `SearchMemory` 等 RESTful API 或 `agentscope-runtime` SDK，实现全生命周期管理：
  - `AddMemory`：从 `messages`（最多 50 条，一问一答计为 2 条）或 `custom_content`（≤512 字符）中自动抽取记忆片段；传入 `profile_schema` 可同步更新结构化用户画像。
  - `SearchMemory`：基于自然语言查询进行语义检索，支持 `top_k`、`min_score`、`plan_version`（`pro`/`lite`）等精细控制，结果可直接注入 LLM 提示词。
- **OpenClaw 框架集成**：安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件后，通过 `openclaw.json` 配置 `apiKey` 和 `userId`，即可零代码启用 `autoCapture`（自动写入）与 `autoRecall`（自动检索），无需修改业务逻辑。
- **工作流（Workflow）与高代码应用**：不原生支持长期记忆参数，但可通过调用记忆库 API 在节点中手动集成（如在「函数节点」中调用 `SearchMemory` 获取用户历史）。

> ⚠️ 注意：长期记忆以 `user_id` 为隔离边界，同一 `user_id` 下的记忆可跨应用、跨会话被检索；但 `memory_id`（应用级）与 `memory_library_id`（租户级）不可混用——前者仅用于智能体应用调用链路，后者用于直接 API 调用。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 | 场景 |
|------|------|------|------|------|------|
| `user_id` | body/query | string | 是 | 用户唯一标识（≤64 字符），所有接口必需；用于记忆空间隔离与检索范围限定 | 全部 |
| `memory_library_id` | body | string | 否 | 记忆库 ID（≤32 字符）；不传则使用默认库；需在控制台创建后获取 | 直接 API 调用 |
| `project_id` | body | string | 否 | 记忆片段规则 ID；决定抽取策略（如 `plan_version`）、默认过期时间等；不传则使用默认规则 | `AddMemory` |
| `profile_schema` | body | string | 否 | 用户画像模板 ID；传入后触发结构化字段抽取（如年龄、职业）；需先调用 `CreateProfileSchema` 创建 | `AddMemory`（画像场景） |
| `plan_version` | body | string | 否 | 检索策略：`"pro"`（启用 Rerank，精度高）或 `"lite"`（轻量快）；`SearchMemory` 中显式指定，优先级高于规则默认值 | `SearchMemory` |
| `top_k` | body | int | 否 | 检索返回最大条数，默认 `10`（API）或 `5`（OpenClaw 插件）；取值范围 `[1, 100]` | `SearchMemory` |
| `min_score` | body | double | 否 | 检索相似度阈值，默认 `0.3`；低于此值的结果将被过滤 | `SearchMemory` |
| `expired_in_days` | body | int | 否 | 记忆片段有效期（天）；显式传入时生效；未传则由 `project_id` 对应规则决定（默认 180 天）；**系统不强制删除，仅影响检索可见性** | `AddMemory` |

> ✅ 实用提示：  
> - 若需长期保留记忆，**不要传 `expired_in_days`**，或设为 `0`（表示永不过期）；  
> - `pro` 策略适用于对召回质量敏感的场景（如个性化推荐），`lite` 适用于高并发、低延迟场景（如客服会话摘要）；  
> - `custom_content` 优先级高于 `messages`，二者互斥，避免同时传入导致 400 错误。

## 面向开发者，简洁实用

- **快速上手三步走**：  
  1. 控制台创建记忆库 → 获取 `memory_library_id`；  
  2. 调用 `AddMemory` 写入（带 `user_id` + `messages` 或 `custom_content`）；  
  3. 调用 `SearchMemory` 检索（带 `user_id` + `query`），将 `memory_nodes` 注入 LLM `system` 或 `user` 消息。  

- **调试建议**：  
  - 使用 `ListMemory?user_id=xxx&limit=10` 查看最新写入的记忆；  
  - 检索无结果时，先检查 `user_id` 是否一致、`min_score` 是否过高、`plan_version` 是否匹配训练策略；  
  - OpenClaw 插件日志中搜索 `memory-recall` 可确认自动召回是否触发。

- **生产注意**：  
  - 阿里云账号级限流：`AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM；  
  - 计费将于 **2026 年 8 月 20 日** 开始，按 `pro`/`lite` 版本分别计费；  
  - 所有记忆数据默认加密存储，符合阿里云安全合规要求。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [application call](../api/application-call.md)
- [llm application](../guides/llm-application.md)
- [start using](../guides/start-using.md)


