# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种将大语言模型（LLM）与外部知识源动态结合的技术范式：在模型生成响应前，先从结构化或非结构化知识库中检索相关片段，并将其作为上下文注入提示词，从而提升回答的准确性、时效性与领域专业性。

在百炼平台中，RAG 不是独立模块，而是贯穿于智能体（Agent）、应用（Application）、知识库服务（RAG API）等核心能力的横切能力——它通过统一的检索-注入-生成链路，实现私有知识的“即插即用”，无需微调模型即可快速构建可信、可控的企业级 AI 应用。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 场景**：在 `Managed Agent` 或 `Flow Agent` 中，通过启用 `enable_rag: true` 参数，自动关联已发布的 RAG Agent（即知识问答智能体）。检索结果以结构化文本形式注入 LLM 上下文，支持多轮对话中持续引用知识；Sandbox 模式下不支持 RAG，需显式调用 RAG API 实现自定义检索逻辑。  
- **应用（Application）场景**：在网站、企业微信、钉钉等私域渠道部署的 AI 助手，默认采用 RAG 架构。开发者可在控制台应用配置页一键启用“必定调用知识库”，并选择已创建的知识库；也可通过 AppFlow 连接流，在调用百炼 API 前插入 RAG 检索节点，实现混合路由（如：先查知识库，无结果再调用公网搜索插件）。  
- **RAG API 场景**：作为底层服务，提供完整的知识生命周期管理能力。开发者可调用 `/api/v1/indices/knowledge/search` 获取原始检索结果（含文档 ID、分片内容、相关性得分），或直接调用 `/api/v2/apps/knowledge/chat` 发起端到端问答——后者由平台自动完成检索 + 上下文拼接 + LLM 调用 + 格式化输出，适合快速集成。  
- **本地 RAG 场景**：对于敏感数据不出域的场景，可通过 `local_rag` 工具链在自有环境部署轻量级 RAG 流程：自定义文档切分策略、选用嵌入模型（如 `text-embedding-v4`）、对接向量数据库（如 ADB-PG 或本地 Chroma），最终将检索结果通过 API 注入百炼模型调用请求的 `input` 或 `system_prompt` 字段。

> ⚠️ 注意：所有 RAG 调用均受模型上下文长度限制。检索返回的文本会占用输入 token，建议在知识库配置中合理设置切片长度（推荐 256–512 字符），并在 Agent 或应用中监控 `input_tokens` 消耗，避免截断。

## 关键参数和配置

| 参数 | 作用 | 说明 |
|------|------|------|
| `enable_rag` | Agent 级开关 | 布尔值，默认 `false`；设为 `true` 后，Agent 自动调用当前工作空间下默认或指定的 RAG Agent。需配合 `agent_id` 使用。 |
| `agent_id` | 指定 RAG Agent 实例 | 必填（当 `enable_rag=true` 时），取值为通过 RAG API `/api/v1/indices/rag/app/create` 创建并发布后的 `agent_id`。一个知识库可对应多个 RAG Agent（如不同 prompt 配置）。 |
| `top_k` | 检索结果数量 | 可在 RAG Agent 配置中设定（控制台或 API 更新时传 `retrieval_config.top_k`），默认 `3`；影响上下文长度与召回精度平衡。 |
| `rerank_model` | 重排序模型 | 在知识库创建或更新时通过 `rerank_model` 字段指定（如 `qwen3-rerank`），用于对初检结果二次打分，提升相关性。 |
| `knowledgeType` | 知识库类型 | 决定检索方式与能力边界，常见值：`document`（全文语义检索）、`table`（结构化查询）、`image`（多模态图文理解）、`multimedia`（音视频关键帧检索）。 |

- **知识库标识**：所有 RAG 操作依赖 `indexId`（或 `pipelineId`），该 ID 在调用 `/api/v1/indices/rag/index/create_v2` 创建知识库后返回，是后续导入文档、配置 Agent、运行检索的唯一依据。  
- **认证与空间隔离**：RAG API 请求必须携带 `Authorization: Bearer <API-Key>`，且 Endpoint 中的 `{workspace_id}` 必须与知识库所属业务空间一致，跨空间调用将鉴权失败。

## 面向开发者，简洁实用

- ✅ **快速验证**：在控制台「知识库」→「创建知识库」→「上传 PDF/DOCX」→「发布」→「应用配置页启用 RAG」，5 分钟内完成端到端测试。  
- ✅ **精准调试**：若回答不准，优先检查：① 知识库是否已发布；② `agent_id` 是否匹配；③ 检索 `top_k` 是否过小；④ 文档是否被正确切片（查看「切片管理」列表）。  
- ✅ **性能优化**：对高并发场景，建议使用 `ADB-PG` 作为向量存储（支持多应用共享、读写分离），并开启 `rerank_model` 提升首条结果命中率。  
- ❌ **避坑提示**：  
  - `multimedia` 类型知识库不支持直接调用「新增切片」接口，请使用标准文件导入流程；  
  - Agent 中启用 RAG 后，检索内容计入 `input_tokens`，需在模型选型时预留足够上下文（如 `qwen-max` 支持 32K 输入）；  
  - 旧版 Agent 1.0 的 RAG 结果直接拼入 prompt，无重排能力，建议新项目统一使用 Agent 2.0 + RAG API 架构。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [rag api](../api/rag-api.md)
- [application use cases](../guides/application-use-cases.md)
- [agent legacy](../guides/agent-legacy.md)
- [application support](../guides/application-support.md)


