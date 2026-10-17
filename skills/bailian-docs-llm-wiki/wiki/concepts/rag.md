# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示（prompt），从而提升回答的准确性、时效性与可溯源性。

在百炼平台中，RAG 不是独立 API，而是通过 **Agent 工具链** 与 **模型调用基础设施** 协同实现的核心能力。开发者无需自行搭建向量数据库或重排服务，可直接复用平台内置的检索能力，快速构建具备领域知识的智能应用。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agent 场景**：  
  通过绑定 `skill-kb-search` 类型 Skill（知识库检索工具），Agent 在执行过程中自动触发语义检索——平台将用户问题向量化，在已配置的知识库（如上传的 PDF/Word/网页等）中召回 Top-K 相关文本段落，并拼接进 LLM 的系统提示中。整个过程对开发者透明，仅需在创建 Agent 时声明该 Skill 即可生效。

- **Flow Agent 场景**：  
  在可视化流程中拖入「知识库检索」节点，配置知识库 ID 和检索参数（如 `top_k=3`, `rerank=true`），其输出可直接连接至后续 LLM 节点的 `context` 字段。支持多知识库并行检索与结果融合，适用于需要显式控制检索逻辑的复合问答场景。

- **Sandbox 自定义场景**：  
  开发者可在 Python 沙箱中调用百炼提供的 `bailian.retrieval.search()` SDK 方法（需安装 `dashscope>=1.20.0`），传入 query 和 knowledge_base_id，同步获取带元数据（来源文件、页码、置信度）的检索结果，再按需构造 prompt。适合需定制重排策略、混合检索（关键词+向量）、或对接私有知识源的高级用例。

- **纯模型调用（/v1/chat/completions）场景**：  
  RAG 需由开发者自行完成：先调用 `/v1/knowledge_bases/{kb_id}/search` 接口获取检索结果，再将 `retrieved_chunks` 手动拼入 `messages` 中的 system 或 user 角色内容。此方式灵活性最高，但需承担上下文长度管理、去重、排序等工程责任。

> ✅ 提示：所有知识库检索均默认启用混合检索（稠密向量 + 稀疏关键词）与内置重排（Rerank），无需额外配置即可获得优于单一路由的精度。

## 关键参数和配置

| 参数 | 位置 | 说明 | 默认值 |
|------|------|------|--------|
| `knowledge_base_id` | Skill 配置 / Flow 节点 / SDK 调用 | 指定要检索的知识库唯一标识符，需提前在控制台创建并发布 | — |
| `top_k` | Skill 配置体 / Flow 节点参数 / SDK `search()` 方法 | 控制返回的最相关片段数量 | `3` |
| `rerank` | Skill 配置体 / Flow 节点参数 | 是否启用深度重排模型（qwen-rerank）对初检结果二次打分排序 | `true` |
| `enable_highlight` | SDK `search()` 方法（仅 Python） | 是否在返回结果中标记匹配关键词（HTML `<mark>` 标签） | `false` |
| `max_chunk_length` | 知识库创建时设置（非运行时参数） | 切片时每段文本最大 token 数，影响检索粒度与精度平衡 | `512` |

⚠️ 注意：  
- 知识库检索结果会自动过滤低置信度项（score < 0.3），且不返回原始二进制内容，仅提供文本片段与元数据；  
- `top_k` 值受 Agent 上下文长度限制约束：若 `top_k × 平均片段长度 + 其他 prompt` 超过 32K tokens，将触发截断并告警（可通过 `enable_tracing` 查看实际注入内容）；  
- 启用 `rerank=true` 会增加约 200–500ms 延迟，但对长尾问题准确率提升显著（实测 +12%～28% MRR@3）。

## 面向开发者，简洁实用

- ✅ **快速起步**：控制台 →「知识库」→ 上传文档 → 发布 → 创建 Managed Agent 时勾选 `skill-kb-search` → 完成 RAG 集成；  
- ✅ **调试技巧**：开启 `enable_tracing=true`，查看 trace 中 `tool_call` 步骤的完整检索输入、召回片段及 LLM 最终接收的 prompt；  
- ✅ **性能优化**：对高并发场景，优先复用 Managed Agent 或 Flow Agent（平台级缓存检索结果），避免 Sandbox 中重复调用 `search()`；  
- ❌ **避坑提醒**：勿在 `system` message 中硬编码知识片段——应交由平台检索机制动态注入，否则无法响应知识库更新；  
- 📦 **扩展建议**：如需跨知识库联合检索，使用 Flow Agent 的「并行检索」+「结果聚合」模式，或在 Sandbox 中批量调用 `search()` 后自定义融合逻辑。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [agent development](../guides/agent-development.md)
- [get started with models](../guides/get-started-with-models.md)
- [model experience](../guides/model-experience.md)


