# 记忆管理

记忆管理是百炼平台提供的结构化、可检索、可演化的上下文持久化能力，用于在 Agent 执行生命周期中跨会话、跨项目地存储与复用事实性知识（observation）、技能逻辑（skill）和用户画像（user_profile）。它独立于模型参数，通过专用存储引擎与统一 API 提供写入、抽取、检索、更新与生命周期控制，是构建具备长期认知能力智能体的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 运行时上下文注入**：在 `agent context` 中启用 `"memory"` 类型后，系统自动将当前 `session_id` 关联的近期会话记忆（按 `window_size` 限制轮数）及匹配的长期记忆（通过语义检索）注入 Prompt；若需跨会话共享，须显式调用 `/v1/memory/{memory_id}/search` 并手动合并结果。  
- **长期记忆服务（Long Term Memory）**：作为独立服务模块，支持三类结构化记忆的异步写入与精准检索：`observation`（如“用户偏好咖啡因”）、`skill`（如“订会议室流程”）、`user_profile`（需配合预定义 schema 抽取）。推荐使用 `AddMemoryAsync` 接口完成多项目并行抽取与联合画像生成。  
- **LLM 应用（Agent 2.0 / Flow Agent）集成**：通过配置 `enable_memory: true` 自动绑定已授权的记忆实例；开发者也可在 Flow Agent 节点中直接调用记忆 SDK（如 `SearchMemory`），实现条件化记忆读取与动态上下文拼接。  
- **治理与可观测性**：所有记忆读写操作（`AddMemoryAsync`、`SearchMemory`、`UpdateMemory` 等）均作为独立 Trace 节点上报至 Agent Governance，支持在观测面板中查看耗时、[Token](token.md) 消耗、检索命中率与失败原因，便于诊断上下文缺失或过载问题。  
- **低代码/可视化编排**：在 Flow Agent 画布中，可通过「记忆节点」拖拽接入，配置 `user_id`、`memory_types`、`top_k` 等参数，无需编写代码即可完成记忆检索与变量注入。

## 关键参数和配置

| 参数 | 说明 | 默认值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | 子用户唯一标识，强制用于跨用户隔离 | — | 所有写入/检索接口必填，不可为空字符串 |
| `memory_library_id` | 记忆库 ID，用于多库隔离 | 使用默认库 | 可选；未传时使用业务空间默认记忆库 |
| `project_ids` | 项目级二级隔离标签，最多 5 个 | — | 与 `project_id` 互斥；建议用于 A/B 测试或灰度发布 |
| `memory_types` | 检索时限定类型，如 `["observation", "skill"]` | 全部类型 | `SearchMemory` 必填，避免冗余召回 |
| `top_k` | 检索返回最大条目数 | `10` | 建议设为 `3–5` 以平衡效果与 [Token](token.md) 开销 |
| `min_score` | 相似度阈值（仅 `plan_version=pro` 生效） | `0.3` | 设为 `0.6+` 可显著提升相关性，降低噪声 |
| `plan_version` | 计费策略版本：`pro`（支持 rerank/min_score）或 `lite` | `"pro"` | 生产环境务必显式指定 `"pro"` 以启用关键过滤能力 |
| `extract_mode` | 异步写入时指定抽取范围：`"profile_only"` 或空 | — | 仅画像场景必需；设为 `"profile_only"` 时 `messages` 不可为空 |

> ⚠️ **重要实践提示**：  
> - 同步接口 `AddMemory` 仅适用于简单 `efficient` 模式，不支持技能抽取与画像联合提取；**所有生产场景请默认使用 `AddMemoryAsync`**；  
> - 用户画像必须先调用 `CreateProfileSchema` 定义字段，再在 `AddMemoryAsync` 中传入 `profile_schema` ID，否则抽取无效；  
> - 多模态内容（如 `image_url`）仅在启用多模态能力的项目中被解析，其他项目自动忽略该字段。

## 面向开发者，简洁实用

- ✅ **快速起步**：设置 `DASHSCOPE_API_KEY` 和 `MEMORY_SERVICE_ENDPOINT`（从控制台「业务空间管理」复制 WorkspaceId），直接调用 SDK `AddMemoryAsync` 和 `SearchMemory`；  
- ✅ **检索优化**：始终指定 `memory_types` 和合理 `top_k`；对高精度场景，强制 `plan_version="pro"` + `min_score=0.6`；  
- ✅ **错误防御**：检查 `GetEvent` 返回状态是否为 `"SUCCEEDED"` 再使用 `memory_node_id`；`DeleteMemory` 不可逆，请先 `GetMemoryNode` 确认；  
- ✅ **调试技巧**：在 Agent 调试器中开启 Trace，观察 `SearchMemory` 节点的 `retrieved_nodes` 字段与 `score`，验证检索质量；  
- ✅ **成本控制**：记忆写入与检索均按 token 计费，避免在 `messages` 中传入冗余长文本；使用 `window_size`（Agent Context）和 `top_k`（LTM）主动限流。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent context](../guides/agent-context.md)
- [agent governance](../guides/agent-governance.md)
- [llm application](../guides/llm-application.md)


