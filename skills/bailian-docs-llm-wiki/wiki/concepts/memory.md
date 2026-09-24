# 记忆

记忆是百炼平台提供的跨会话、结构化、可检索的长期记忆服务，用于持久化存储用户事实性信息（如行为偏好、临时计划）与结构化画像（如年龄、职业、兴趣），并在后续对话中基于语义自动召回，使智能体具备持续理解用户的能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：通过 Agent Harness 原生集成，无需代码即可启用记忆。系统在每次对话结束时自动提取关键信息，写入事实记忆或触发用户画像抽取；下一次对话开始前，自动检索并注入相关记忆到上下文，提升个性化响应质量。  
- **工作流（Workflow）应用**：通过「记忆库插件」节点（如 `memory_search` / `memory_store`）在流程中显式调用，支持在条件判断、工具调用前后动态读写记忆，实现状态驱动的流程控制（例如：“若用户历史有健身记录，则推荐运动计划”）。  
- **Managed Agents**：以挂载资源形式接入「记忆库（Memory Store）」，智能体可在沙箱内直接通过 `read`/`write` 工具操作记忆文件树（如 `/mnt/memory/profile.json`），适用于需强一致性、多轮协同或文件级记忆管理的复杂任务。  
- **高代码应用**：通过 RESTful API（如 `POST /add`, `POST /search`）编程式控制记忆生命周期，支持自定义抽取逻辑、多模态内容写入、异步事件处理（`add-async` + `get-event`），适合对时效性、精度和隔离粒度有精细要求的场景。  
- **安全体系**：记忆的读写内容默认接受内容安全检测（如敏感信息识别、提示词注入防护），所有 `AddMemory` 和 `SearchMemory` 请求均被审计留痕，确保记忆数据合规可控。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `user_id` | **必填**，记忆隔离的核心维度。同一 `user_id` 下的所有记忆自动聚合、跨会话共享；不同用户间完全隔离。 | 建议从登录态或业务 ID（如 `uid_123456`）稳定生成，避免使用临时 session_id。 |
| `memory_library_id` | 可选，指定自定义记忆库 ID；不传则使用默认记忆库。配合 `project_id` 可实现项目级隔离。 | 生产环境推荐创建独立记忆库（如 `prod-user-profile`），便于权限管控与监控。 |
| `plan_version` | `pro`（默认）：启用 Rerank、`min_score` 过滤、高精度抽取；`lite`：仅基础向量检索，成本更低。Add 与 Search 可独立设置。 | 对画像抽取、技能提取、高相关性检索等场景，务必使用 `pro`；高频轻量检索（如状态查询）可用 `lite` 降本。 |
| `top_k` | 检索最多返回条数，默认 `10`（API），取值范围 `1–100`。 | 根据下游模型上下文长度合理设置（如 Qwen3-32B 支持 32K tokens，`top_k=20` 通常足够）；避免盲目设大导致噪声注入。 |
| `min_score` | 相似度阈值（0.0–1.0），仅 `plan_version=pro` 时生效，默认 `0.3`。低于此值的记忆将被过滤。 | 初期建议设为 `0.5`，上线后根据召回准确率（Precision@K）逐步下调；`0.7+` 适用于强确定性场景（如身份核验）。 |
| `profile_schema` | 用户画像模板 ID，传入后触发结构化字段抽取（如 `age`, `occupation`）。需先调用 `CreateProfileSchema` 创建。 | 模板字段应精简、明确、有业务价值；避免过度抽取（如 `favorite_color`），每个 schema 字段数建议 ≤15。 |
| `extract_mode` | 可选值：`profile_only`（仅抽画像）、`observation_only`（仅抽事实）、`all`（默认）。 | 当只需更新画像（如用户修改资料）时，显式设为 `profile_only`，跳过冗余事实提取，提升性能。 |

> ⚠️ 注意：用户画像抽取为**异步过程**，首次 `GetUserProfile` 可能返回空；建议轮询（间隔 ≥3 秒，最多 5 次）或监听 `event_id` 状态。事实记忆写入为同步（`add`）或最终一致（`add-async`），无延迟等待需求。

## 面向开发者，简洁实用

- ✅ **快速起步**：开通服务 → 设置 `DASHSCOPE_API_KEY` → 调用 `AddMemory` 写入一条带 `user_id` 的对话消息 → 立即用 `SearchMemory` 检索验证。  
- ✅ **生产就绪**：  
  - 创建自定义记忆库，配置事实记忆规则（设过期时间防堆积）和画像规则（设默认值防空）；  
  - 使用 `add-async` 处理含图片/长文本/多技能的记忆写入；  
  - 在 `meta_data` 中添加业务标签（如 `"source": "workflow_order"`），提升后续定向检索精度。  
- ✅ **避坑指南**：  
  - 不要复用 `user_id` 表示不同用户（如用测试账号 ID 给正式用户）；  
  - `DeleteMemory` 不可逆，删除前务必确认 `id` 或用 `ListMemory?user_id=xxx` 核查；  
  - 默认记忆库不可删除，但可重命名；自定义记忆库删除后数据**永久丢失**；  
  - 免费试用期后按 `Add`/`Search` 次数计费，注意限流（全账号 3000 QPM，`Add` ≤120 QPM）。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [llm application](../guides/llm-application.md)
- [managed agents](../guides/managed-agents.md)
- [security guide](../guides/security-guide.md)


