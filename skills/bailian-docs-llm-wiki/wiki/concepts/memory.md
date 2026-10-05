# 长期记忆

长期记忆是百炼平台提供的结构化、跨会话持久化记忆服务，通过语义驱动的自动抽取与向量检索能力，突破大模型单次对话的上下文窗口限制，实现用户状态、事实信息与技能知识的长期留存与智能复用。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：在 Managed Agents 中，长期记忆以「记忆库」形式挂载为会话级资源（路径 `/mnt/memory`），与文件系统并列作为上下文扩展源；Agent 可通过 `memory_search` 工具主动调用，或由平台在 `autoRecall` 钩子中自动注入相关记忆至 Prompt，支撑多轮连贯决策（如“上次我让你查的服务器配置是什么？”）。
- **记忆库原生集成**：通过开放 API（`/add`、`/search`、`/get-user-profile` 等）直接管理记忆生命周期。支持两类核心记忆：
  - **事实记忆**：自动从 `messages` 对话流中提取 `observation`（如提醒、偏好、事件）或显式注册 `skill`（可复用操作流程，含 `skill_name`/`skill_description`）；
  - **用户画像**：基于预定义 `profile_schema`（如年龄、职业、健康目标）结构化抽取，结果异步生成，需轮询 `GetUserProfile` 获取。
- **插件协同场景**：OpenClaw 等插件提供 `memory_store` 工具，允许用户通过自然语言指令（如“记住我的家庭地址”）绕过自动抽取规则，直接写入原始内容；该能力与 `AddMemory` 的被动提炼形成互补，适用于明确意图的主动记忆存档。
- **RAG 增强补充**：虽非传统 RAG 知识库，但长期记忆的语义搜索（`/memory_nodes/search`）可与知识库检索并行调用，在 Prompt 中融合注入，兼顾个性化历史与通用领域知识。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `user_id` | 必填，记忆隔离的最小单元；同一 `user_id` 下所有记忆默认互通 | 严格绑定业务用户标识（如登录态 UID），避免混用导致记忆污染 |
| `memory_library_id` | 指定目标记忆库；不传则使用账号默认库（不可删除，但可编辑） | 多业务线建议创建独立记忆库，便于规则隔离与计费归因 |
| `plan_version` | 控制抽取与检索策略版本（`pro`/`lite`）；`pro` 支持 `min_score` 过滤，`lite` 仅基础检索 | 生产环境统一设为 `pro`；调试阶段可临时降级验证效果差异 |
| `top_k` | 检索最大返回条数（API 默认 10，OpenClaw 插件默认 5） | 初始设为 `3–5`，避免噪声干扰；高精度场景可升至 `10`，勿超 `20` |
| `min_score` | 相似度阈值（0.0–1.0），仅 `plan_version=pro` 时生效（API 默认 0.3） | **强烈建议设为 `0.5–0.7`**：低于 0.5 易召回无关项，高于 0.7 可能漏检关键记忆 |
| `profile_schema` | 触发用户画像抽取的模板 ID；需提前创建 schema 并传入此参数 | 首次调用后需轮询 `GetUserProfile`，若返回空建议 1s 后重试（异步抽取耗时约 0.5–2s） |
| `extract_mode` | 可选 `profile_only`，此时仅执行画像抽取（忽略 `messages` 内容） | 用于纯画像初始化场景，如新用户注册后批量导入基础属性 |

> ⚠️ 注意：`AddMemory`（同步）在 `intelligent` 模式下存在超时风险；**生产环境务必优先使用 `AddMemoryAsync`**，并通过 `GET /events/{event_id}` 轮询状态确保技能/画像抽取成功。

## 面向开发者，简洁实用

- **快速验证三步法**：  
  1. 调用 `POST /add-async` 写入带 `user_id` 的对话消息；  
  2. 控制台 → 记忆库 → 按 `user_id` 查看抽取结果；  
  3. 调用 `POST /memory_nodes/search` 传入新查询消息，验证语义召回。  
- **必做配置**：为每条记忆添加 `meta_data`（如 `{"category": "health", "source": "chat"}`），后续可通过 `filter` 参数精准限定检索范围。  
- **限流应对**：账号级总 QPM ≤ 3000（`add` ≤ 120，`search` ≤ 300），超限返回 `429`；请实现指数退避（1s → 2s → 4s）重试逻辑。  
- **商业化提示**：长期记忆服务将于 **2026 年 8 月 20 日 10:00（北京时间）起正式计费**，此前为免费体验期；当前 10,000 条免费存储额度长期有效。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [application support](../guides/application-support.md)


