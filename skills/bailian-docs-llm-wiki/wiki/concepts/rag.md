# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是百炼平台的核心能力范式，指在大模型生成响应前，先从私有知识库中实时检索相关片段，并将检索结果作为上下文注入提示（[prompt](../guides/prompt.md)），从而提升回答的准确性、时效性与可溯源性。它本质是“检索 + 生成”的协同机制，既规避了模型幻觉，又避免了全量微调的成本。

## 在百炼平台的不同场景中，这个概念如何使用

RAG 在百炼中不是单一接口，而是贯穿多个层级的工程化能力，按使用方式可分为三类：

- **独立 RAG 服务**：通过 RAG API（`/v1/knowledge/retrieve` 和 `/v1/knowledge/ask`）直接调用。适用于需完全自主控制流程的场景，如构建定制客服后台、嵌入自有系统。开发者负责知识库管理、文档上传、切片配置及检索参数调控，服务端自动完成向量化、召回、重排与生成。

- **Agent 上下文集成**：在 Agent 配置中启用 `context_type: "rag"` 或组合模式（如 `["rag", "memory"]`），平台自动将绑定的知识库检索结果注入 LLM 输入。适用于多轮对话型智能体，RAG 结果不缓存、每次请求重新检索，确保信息新鲜；同时受 `max_context_length` 截断策略约束，优先保留 RAG 内容。

- **应用级开箱即用**：在百炼控制台创建“智能体应用”时，一键绑定知识库并开启“必定调用”，即可在网站挂件、微信公众号、企业微信等渠道中零代码启用 RAG 能力。该模式由 AppFlow 统一编排，底层复用 RAG API 与知识库服务，面向业务人员提供低门槛接入。

所有场景均共享同一套知识库基础设施（含切片、向量索引、重排模型），确保语义一致性与运维统一性。

## 关键参数和配置

RAG 行为主要由以下参数控制，分属不同调用层级：

| 参数 | 所属层级 | 类型 | 默认值 | 说明 |
|------|----------|------|--------|------|
| `top_k` | RAG API / 知识库运行期 | integer | `5` | 向量检索返回的最相关切片数（范围 1–100）。值越大召回越广，但可能引入噪声；问答场景建议 3–7，调试检索质量时可设为 20+。 |
| `enable_rerank` | RAG API | boolean | `true` | 是否启用重排（默认开启）。关闭后跳过 `bge-reranker-v2-m3` 或 `qwen3-rerank` 等重排模型，降低延迟但可能影响排序精度。注意：`stream=true` 时不可设为 `false`。 |
| `context_type` | Agent Context | string/array | `"auto"` | 显式指定 RAG 参与上下文注入（如 `"rag"` 或 `["rag", "memory"]`）。设为 `"auto"` 时平台根据知识库绑定状态与会话历史自动决策。 |
| `max_context_length` | Agent Context | integer | `4096` | 注入 LLM 的总上下文 token 上限（含系统提示）。超出时按优先级截断：RAG > memory > connector。实际可用给 RAG 的 token 数 ≈ `max_context_length - system_prompt_tokens - history_tokens`。 |
| `相似度阈值` | 知识库运行期（控制台） | float | `0.3` | 过滤向量检索低分切片（范围 0.01–1.0）。值越高越严格，适合高精度问答；值过低易引入无关内容，建议从 0.4 开始调优。 |
| `标签过滤` | 知识库运行期（控制台/API） | string[] | `[]` | 通过预设标签（如 `["产品_百炼", "版本_v3.5"]`）实现精准范围检索，无需修改原始文档内容，适合多租户或分场景知识隔离。 |

> ⚠️ 注意：  
> - 向量模型（如 `text-embedding-v4`）和重排模型在知识库创建或服务配置时选定，**不可在单次请求中动态覆盖**；  
> - 切片长度（默认 512 token）为知识库创建期固定参数，API 层无运行时调整入口；  
> - RAG 检索结果在 Agent 中不缓存，每次请求均为全新检索，保障数据实时性。

## 面向开发者，简洁实用

- ✅ **快速验证**：用控制台 Playground → 选择知识库 → 切换“知识检索”模式，输入 query 查看原始切片与分数，比对 `top_k` 和 `相似度阈值` 效果。  
- ✅ **调试技巧**：若问答结果不准，先调用 `/v1/knowledge/retrieve` 检查检索是否命中关键段落；未命中则优化 query 改写或调整切片策略；命中但生成差，则检查 `max_context_length` 是否截断了重要上下文。  
- ✅ **生产建议**：高并发场景下，优先启用 `enable_rerank=false` 降低 P99 延迟；对精度敏感场景（如合同审核），务必开启重排并配合 `标签过滤` 缩小检索范围。  
- ❌ **避坑提醒**：不要在 RAG API 中尝试传入 `rerank_model` 参数（已废弃）；不要在 Agent 中依赖 RAG 结果缓存（它不存在）；上传文档时确保后缀为小写 `.pdf`（`.PDF` 会被拒绝）。

## 关联主题页

- [rag api](../api/rag-api.md)
- [agent context](../guides/agent-context.md)
- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [application support](../guides/application-support.md)


