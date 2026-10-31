# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、持久化状态管理服务，用于在 Agent 应用中跨会话保存和复用用户事实、技能知识与个性化画像，支撑上下文感知、个性化响应与行为持续进化。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 应用（Managed/Flow/Sandbox）**：通过 `memory_session_id` 显式注入到 `context` 中，使 Agent 在每次调用时自动加载关联的长期记忆（如用户偏好、历史决策、已掌握技能），实现“记住用户”的能力。注意：仅 `qwen-max`、`qwen-plus` 及 `qwen-turbo`（v20240915+）原生支持该注入；其他模型忽略 memory 字段。
  
- **Flow Agent API（旧版）**：提供 `Memory` 与 `MemoryNode` 两级接口，支持基础 CRUD 和会话级记忆管理，但已被标记为**遗留方案**，新项目应优先采用「长期记忆新版本」。

- **长期记忆新版本（推荐）**：作为独立服务，按三类结构化节点组织记忆：
  - `observation`：从对话自动抽取的事实（如“用户每周三健身”），适用于行为建模；
  - `skill`：显式注册的可复用能力（含 `skill_name`/`skill_description`/`skill_tags`），支持导出元信息供 Agent 动态调用；
  - `user_profile`：基于预定义 `ProfileSchema` 模板抽取的结构化用户画像（如年龄、职业、兴趣标签），需先创建模板再写入。

- **多模态场景**：`messages` 中可携带 `image_url`，若业务空间已开通多模态能力，则图像内容参与记忆抽取（文本始终支持）。

> ⚠️ 注意：`session_id`（Flow Agent 中的会话 ID）与 `memory_session_id`（Agent Context 中的记忆会话 ID）**语义不同、不可混用**；前者仅触发短期上下文缓存（1 小时失效），后者绑定长期记忆库并支持冷存档（7 天无访问后解冻延迟 2–3s）。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `user_id` | string | 是 | 记忆隔离的核心标识，所有读写操作（Add/Search/Get）均需指定，建议与业务系统用户 ID 对齐。 |
| `memory_library_id` | string | 否 | 指定自定义记忆库；不传则使用默认库（每个 Workspace 一个默认库）。 |
| `profile_schema` | string | `user_profile` 类型必填 | 已创建的有效画像模板 ID，配合 `extract_mode: "profile_only"` 可精准触发画像抽取。 |
| `skill_name` / `skill_description` / `skill_tags` | string / string / array[string] | `skill` 类型必填（异步写入） | 定义技能元信息，用于后续语义搜索与技能发现。 |
| `extract_scene` | `"efficient"` \| `"intelligent"` | 否（默认 `"efficient"`） | 控制抽取精度与延迟：`efficient` 适合实时写入；`intelligent` 推荐仅用于异步接口（`AddMemoryAsync`），同步调用可能超时。 |
| `plan_version` | `"lite"` \| `"pro"` | 否（默认 `"lite"`） | 影响搜索能力：`pro` 支持 `min_score` 过滤与 Rerank；`lite` 下 `min_score` 不生效。 |
| `min_score` | float | 否（默认 `0.3`） | 仅 `plan_version="pro"` 时有效，用于过滤低相关性搜索结果（范围 `[0.0, 1.0]`）。 |

## 面向开发者的关键实践建议

- ✅ **优先使用新版本 API**：`AddMemoryAsync` + `SearchMemory` 组合替代旧版 `MemoryNode`，获得结构化、可检索、可扩展的记忆能力。
- ✅ **异步写入是常态**：对 `intelligent` 抽取、多类型混合写入（如同时更新 skill + profile）、含图片内容等场景，必须使用 `AddMemoryAsync` 并轮询 `GetEvent`。
- ✅ **认证与 Endpoint 严格匹配**：长期记忆新版本使用 `DASHSCOPE_API_KEY` + `MEMORY_SERVICE_ENDPOINT`（格式：`https://<workspace-id>.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`），**末尾不带 `/`**；勿与 Flow Agent 的 AccessKey 签名方式混淆。
- ❌ **避免同步写入 `intelligent` 模式**：文档明确提示该模式下同步接口可能超时，生产环境请规避。
- ❌ **不要复用 `session_id` 作为 `memory_session_id`**：二者归属不同系统，混用将导致记忆加载失败或数据错位。

> 提示：控制台入口 → [百炼控制台 > 记忆管理](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)，可查看记忆库、模板、任务事件及调试日志。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent context](../guides/agent-context.md)
- [agent development](../guides/agent-development.md)


