# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、跨会话持久化记忆管理能力，用于突破大模型上下文窗口限制，实现用户状态延续、个性化交互与行为一致性。它不依赖外部大模型推理，而是由平台内置的记忆抽取引擎自动从对话或自定义内容中提取语义关键信息，并以 `user_id` 为隔离维度进行存储与检索。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Managed Agents）**：通过 `memory_id` 参数在应用调用时显式绑定记忆库，使 Agent 在多轮会话中自动读取并注入相关事实记忆或用户画像，无需手动拼接上下文。该能力深度集成于 Agent 执行引擎，支持与工具调用、RAG 检索协同工作。
  
- **工作流与插件（OpenClaw 等）**：通过插件模式启用 `autoCapture`（自动写入）和 `autoRecall`（自动检索），在消息流入/流出节点透明捕获事实或触发画像抽取，实现零代码记忆接入。

- **API 直接集成（DashScope）**：开发者可独立调用 `/add`（同步）或 `/add-async`（推荐）写入记忆，再通过 `/memory_nodes/search` 检索。适用于需精细控制记忆生命周期、多模态内容处理或批量项目管理的场景。

- **记忆库（Memory Library）统一管理**：作为上层抽象，记忆库提供控制台可视化管理、规则配置（如事实提取模板、画像 Schema）、权限隔离（多应用共享/独占）及计费聚合能力，是长期记忆能力的运营与治理入口。

- **[安全防护](security.md)（Security Guide）**：所有长期记忆的读写操作均默认纳入内容安全检测范围，包括输入内容过滤、记忆片段投毒识别与审计留痕，确保记忆数据的可信性与合规性。

## 关键参数和配置

| 参数 | 说明 | 取值/范围 | 注意事项 |
|------|------|-----------|----------|
| `user_id` | 记忆归属的唯一用户标识，强制隔离不同用户的记忆空间 | 字符串（非空） | 所有读写接口必填；建议与业务系统用户 ID 对齐，避免硬编码匿名 ID |
| `plan_version` | 检索/抽取策略版本 | `"Pro"`（默认） / `"Lite"` | `Search` 和 `GetUserProfile` 接口由请求参数控制；`Add` 接口由记忆库规则决定；大小写敏感，必须为 `"Pro"` 或 `"Lite"`（非 `"pro"`） |
| `top_k` | 检索返回的最大记忆条数 | `1–100` | 默认值依调用路径而异（控制台建议 `10`，插件默认 `5`），生产环境建议显式指定（如 `5–10`）以平衡效果与开销 |
| `min_score` | 相似度阈值（仅 `plan_version="Pro"` 生效） | `0.0–1.0`，默认 `0.3` | 推荐设为 `0.5–0.7` 提升精度；过低易引入噪声，过高可能导致漏召 |
| `memory_library_id` | 目标记忆库 ID | 字符串 | 非必填；不传则使用账号默认记忆库（不可删除，但可编辑） |
| `project_id` / `project_ids` | 项目级二级分组标识（增强组织性） | 字符串 / 最多 5 个字符串数组 | 推荐在多业务线或多租户场景中使用，便于后续按项目过滤与统计 |
| `profile_schema` | 用户画像模板 ID | 字符串 | 仅当需触发结构化画像抽取时必填；需先通过 `/profile_schemas` 创建 |

> ⚠️ **重要行为提示**：
> - `SearchMemory` 的 `plan_version` **完全由请求参数决定**，与记忆库规则配置无关；
> - 用户画像提取为**异步过程**，首次 `GetUserProfile` 可能返回空，需轮询或重试；
> - 生产环境写入请优先使用 `/add-async` + `/events/{event_id}` 轮询，避免同步接口超时风险；
> - 所有记忆数据**无自动过期机制**，长期存储，生命周期由开发者自主管理（支持 `DELETE /memory_nodes/{id}`）。

## 面向开发者，简洁实用

- ✅ **快速起步**：只需 3 步 ——（1）用 `AddMemory` 写入带 `user_id` 的对话消息；（2）用 `SearchMemory` 检索相同 `user_id` 的相关记忆；（3）将结果注入 [prompt](../guides/prompt.md) 或 `context` 字段即可生效。
- ✅ **推荐实践**：
  - 为每个业务域创建独立记忆库（而非共用默认库），便于权限与成本管控；
  - 事实记忆用 `custom_content` 显式传入结构化事件（如 `{"type": "reminder", "time": "09:00"}`），提升提取准确性；
  - 用户画像务必预定义 `profile_schema` 并在 `AddMemory` 中传入，避免字段缺失；
  - 在 `biz_params` 或 `meta_data` 中补充业务标签（如 `"source": "app_ios"`），便于后续审计与分析。
- ❌ **避坑指南**：
  - 不要省略 `user_id` —— 否则记忆将写入/检索失败；
  - 不要混用 `plan_version` 大小写（如 `"lite"`）—— 将导致参数忽略或报错；
  - 不要在高并发场景下频繁调用同步 `/add` —— 优先走异步流；
  - 不要依赖记忆库“自动清理”—— 需主动调用 `DELETE` 或设计 TTL 清理逻辑（如定时任务）。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [security guide](../guides/security-guide.md)


