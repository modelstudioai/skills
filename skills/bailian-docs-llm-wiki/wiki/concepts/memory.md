# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的跨会话、结构化、语义可检索的用户状态与知识持久化服务。它通过自动抽取对话中的关键事实与用户属性，并以向量+结构化双模态方式存储，突破大模型上下文窗口限制，实现真正个性化的智能体交互。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）场景**：在 Managed Agents 中，长期记忆作为挂载的 `memory_store` 资源，供智能体通过文件工具（如 `read`/`write`）直接读写，所有操作自动版本化，适用于沉淀技能知识、任务中间产物或用户偏好配置；同时，Agent Harness 可零代码接入记忆库，自动完成记忆抽取与注入。
- **应用调用（Application Call）场景**：通过 `memory_id` 参数启用长期记忆，调用智能体或工作流时，平台自动为该 `user_id` 检索相关记忆并注入 Prompt 上下文，无需业务方手动拼接。
- **记忆库独立使用场景**：开发者可绕过智能体，直接调用记忆库 API（如 `AddMemoryAsync`、`SearchMemory`），构建自定义记忆闭环——例如在客服系统中将工单结论存为事实记忆，在下次会话中自动召回；或在个性化推荐中将用户画像字段（职业、兴趣标签）持续更新并用于意图增强。
- **RAG 与技能协同场景**：长期记忆可与 RAG 知识库互补：RAG 服务于通用领域知识，长期记忆则聚焦用户专属状态（如“张三过敏花生”“李四偏好简体中文回复”）；技能（Skill）也可注册为 `skill` 类型记忆节点，支持按 `skill_tags` 检索复用。

## 关键参数和配置

| 参数 | 说明 | 是否必填 | 注意事项 |
|------|------|----------|----------|
| `user_id` | 用户唯一标识符，所有读写操作均以此隔离数据空间 | 是 | 必须稳定、全局唯一；建议使用业务系统用户 ID（如 `uid_123456`），避免使用临时 session ID |
| `plan_version` | 计费与能力版本：`Pro`（默认）支持 `min_score` 过滤、Rerank 排序；`Lite` 仅基础向量检索，不生效 `min_score` | 否（Search 默认 `Pro`；Add 由规则决定） | 值必须为 `Pro` 或 `Lite`（首字母大写），小写将导致 400 错误 |
| `top_k` | 检索最大返回条数（1–100） | 否（建议显式设置） | 默认值未声明，生产环境务必指定（如 `top_k=5`），避免结果不可控 |
| `min_score` | 相似度阈值（0.0–1.0），仅 `Pro` 版本生效 | 否（默认 `0.3`） | 推荐设为 `0.5–0.7` 平衡查准率与查全率；低于阈值的记忆不返回 |
| `profile_schema` | 用户画像模板 ID | 条件必填（提取画像时必需） | 需提前通过 `CreateProfileSchema` 创建；传入后 `AddMemory` 才触发画像字段异步抽取 |
| `memory_library_id` | 指定记忆库 ID | 否（不传则使用默认库） | 影响限流配额归属（默认库共享账号级配额，新建库可独立配置） |
| `project_id` / `project_ids` | 项目级二级隔离标识 | 否 | `project_ids` 最多传 5 个，用于多租户或多业务线隔离 |

> ⚠️ 重要提示：  
> - `AddMemory` 接口推荐使用 **异步版 `AddMemoryAsync`**（尤其含图片或多轮消息时），避免 `intelligent` 模式超时；同步接口仅适合 `efficient` 场景。  
> - 用户画像为**异步抽取**：首次 `GetUserProfile` 可能返回空，需按业务逻辑重试（建议指数退避，最多 3 次）。  
> - 所有接口限流为**阿里云账号级别**：总计 ≤ 3000 QPM；`Add` ≤ 120 QPM；`Search` ≤ 300 QPM；超限返回 HTTP `429`，必须实现退避重试。

## 面向开发者，简洁实用

- ✅ **快速上手三步走**：  
  1. 控制台开通记忆库 → 获取 `DASHSCOPE_API_KEY`；  
  2. 调用 `AddMemoryAsync` 写入（传 `user_id` + `messages` + `profile_schema`（如需画像））；  
  3. 调用 `SearchMemory` 检索（传 `user_id` + 当前 `messages`），将返回的 `content` 和 `score` 主动注入 Prompt。  

- ✅ **最佳实践建议**：  
  - 检索后务必校验 `score`：`if (node.score >= 0.5) { injectToPrompt(node.content) }`；  
  - 事实记忆优先用 `custom_content` 直接写入（绕过抽取，更可控）；  
  - 用户画像模板字段名应语义清晰（如 `preferred_language`, `diet_restrictions`），便于模型理解；  
  - 生产环境禁用默认库的 `Lite` 版本检索（查准率低），统一使用 `Pro` + `min_score=0.6`。  

- ❌ **避坑清单**：  
  - 不要省略 `user_id`；  
  - 不要在 `SearchMemory` 请求中传小写 `lite`；  
  - 不要依赖 `AddMemory` 同步返回画像结果；  
  - 不要将敏感信息（密码、身份证号）存入长期记忆（无加密存储，需业务侧脱敏）。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [application use cases](../guides/application-use-cases.md)


