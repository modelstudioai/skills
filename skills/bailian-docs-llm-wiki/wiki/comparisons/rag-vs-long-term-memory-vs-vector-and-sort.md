# RAG、[长期记忆](../concepts/long-term-memory.md)与向量检索排序能力对比

> **目的与背景**：  
> 在百炼平台构建智能体（Agent）应用时，开发者常需在「知识增强问答」「上下文持续感知」「语义召回与精排」等场景中选择合适的技术路径。RAG API、[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）与向量检索排序（Vector & Sort）三者虽均依赖向量技术，但定位迥异：  
> - **RAG API** 是面向业务知识库的 *端到端解决方案*，封装了知识管理、检索、重排与问答编排能力；  
> - **[长期记忆](../concepts/long-term-memory.md)** 是面向对话与用户行为的 *结构化记忆中枢*，强调事实沉淀、技能复用与画像建模；  
> - **向量与排序能力** 是底层 *原子级模型服务*，提供可自由组合的 Embedding 与 Rerank 原语，适用于自定义检索链路或非标准场景。  
> 本文旨在从技术视角系统对比三者的关键能力边界，为开发者提供清晰、可落地的技术选型依据。

## 关键维度对比表

| 维度 | RAG API | 长期记忆（Long Term Memory） | 向量与排序（Vector & Sort） |
|------|---------|------------------------------|-----------------------------|
| **核心定位** | 知识库驱动的问答与检索服务（SaaS 化 Agent 能力） | 对话/事件驱动的结构化记忆管理服务（用户级上下文中枢） | 底层向量计算与排序模型服务（PaaS 级原子能力） |
| **输入格式** | 支持文档（PDF/Word/Excel/HTML/纯文本）、图片、视频等多源文件导入；运行时支持 `query` + `images` 多模态输入 | `messages` 数组（含 `role`/`content`/`image_url`），支持单轮或多轮对话上下文；支持 `profile_schema` 触发结构化画像抽取 | 文本字符串、`contents` 数组（含 `text`/`image_url`/`video_url`）、或公开 OSS/HTTPS 文件 URL（批处理） |
| **输出格式** | 检索结果：`chunks` 列表（含 `content`、`score`、`doc_id`、`chunk_id`）；问答结果：流式 SSE 或 JSON 响应（含 `answer`、`references`、`trace_id`） | 写入响应：`memory_id` / `event_id`；检索响应：`memory_nodes` 列表（含 `type`、`content`、`score`、`metadata`）；画像响应：结构化 JSON（按 `profile_schema` 定义） | 向量：`data[].embedding`（float 数组或 base64）；排序：`results[].index` / `results[].relevance_score`；批处理：返回结果文件 URL |
| **支持模型** | • 嵌入模型：`text-embedding-v4`、`qwen3-vl-embedding`<br>• 重排序模型：`qwen3-rerank`、`qwen3.7-text-rerank`<br>• Agent 模型：`qwen3.7-plus` 等（由 `agent_config.agent_model` 指定） | • 内置抽取模型（不暴露模型名）：<br> – `efficient` 模式：低延迟轻量模型<br> – `intelligent` 模式：高精度多步推理模型<br>• 支持 `pro` 计费版本启用 Rerank（调用底层 `qwen3-rerank`） | • 文本嵌入：`qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`<br>• 多模态嵌入：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06`<br>• 排序：`qwen3-rerank`、`qwen3.7-text-rerank`、`qwen3-vl-rerank` |
| **API 端点前缀** | `/api/v1/indices/rag/...`（管理）、`/api/v1/indices/knowledge/search`（运行时） | `/api/v2/apps/memory/...`（写入）、`/api/v2/apps/memory/memory_nodes/search`（检索） | `/api/v1/services/embeddings`（文本向量）、`/api/v1/services/multimodal-embeddings`（多模态）、`/api/v1/services/rerank`（排序） |
| **认证方式** | Bearer Token（`Authorization: Bearer <API-Key>`），需绑定业务空间 ID 构造 Base URL | Bearer Token（`DASHSCOPE_API_KEY`），Base URL 同样需带 `workspace_id` | Bearer Token（`DASHSCOPE_API_KEY`），支持 DashScope 原生接口与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（部分模型） |
| **计费方式** | 按调用量计费：<br>• 知识库管理类接口：免费<br>• 检索/问答类接口：按 `agent_id` 调用次数计费（含嵌入+重排+大模型生成）<br>• 存储：知识库容量按 GB/月计费 | 按调用量计费：<br>• `lite` 版本：基础检索（无 Rerank）<br>• `pro` 版本：支持 `min_score` 过滤、Rerank、高精度抽取<br>• 记忆存储：按节点数/月计费（当前免费额度内不限量） | 按模型+调用量计费：<br>• 向量：按 `input_tokens` 或 `output_dimensions × batch_size` 计费<br>• 排序：按 `query × documents` 总 Token 数计费<br>• 批处理：按文件行数+模型规格计费 |
| **典型场景** | • 企业知识库问答（如客服 SOP、产品文档）<br>• 多源资料联合检索（合同+邮件+会议纪要）<br>• 基于知识的 Agent 自动化任务（如“查最新财报并总结风险点”） | • 智能体长期上下文建模（如“用户过去三次都要求简明回复”）<br>• 用户画像动态更新（职业、偏好、设备习惯）<br>• 技能沉淀与复用（如“自动帮用户预约会议室”流程） | • 自研 RAG 系统的向量化模块<br>• 跨模态搜索（图文混合检索商品）<br>• 召回后精排（替代传统 BM25）<br>• 离线批量生成向量（千万级文档预处理） |

## 各方案适用场景建议

### ✅ 优先选用 **RAG API** 当：
- 你拥有结构化/半结构化业务知识（PDF、Word、数据库导出等），需快速上线问答能力；
- 要求开箱即用的「上传→切片→向量化→检索→重排→问答」全链路，且接受平台统一编排；
- 需要细粒度知识库权限控制（如按部门隔离）、文档级标签过滤（`search_filters`）；
- 已有 Agent 应用架构，希望将知识服务作为插件集成（通过 `agent_id` 调用）。

### ✅ 优先选用 **长期记忆** 当：
- 核心需求是**记住用户行为、对话历史与个性化特征**，而非静态知识库；
- 需要区分 `observation`（发生了什么）、`skill`（能做什么）、`user_profile`（是谁）三类语义记忆；
- 要求自动从多轮对话中提取结构化画像（如年龄、城市、高频诉求），并支持模板化扩展；
- 场景对写入实时性要求不高，可接受异步抽取（尤其 `intelligent` 模式下）。

### ✅ 优先选用 **向量与排序能力** 当：
- 你需要**完全掌控检索链路**：例如自定义分块策略、混合召回（BM25 + 向量）、多阶段重排；
- 输入/输出格式高度定制（如视频帧级向量、图像局部特征融合）；
- 处理超大规模离线数据（百万级文档向量化），需批处理能力；
- 已有 OpenAI 生态工具链（LangChain/LlamaIndex），希望最小改造接入百炼向量服务；
- 需要跨服务复用向量（如：同一份商品描述向量既用于搜索，也用于推荐相似商品）。

## 技术选型参考（面向开发者）

| 选型问题 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **我只想让客服机器人回答产品手册问题，3天内上线** | RAG API | 创建知识库 → 上传 PDF → 发布 Agent → 调用 `/knowledge/chat`，无需写向量逻辑 |
| **我的智能体需要记住用户说过的“我不喜欢长篇大论”，并在后续所有回复中生效** | 长期记忆 | 写入 `observation` 类型记忆 → 检索时带上该记忆 → Agent 提示词中引用 `{{memory.content}}` |
| **我正在用 LangChain 构建 RAG，已有自己的分块和召回逻辑，只缺高质量向量和重排** | 向量与排序 | 替换 `OpenAIEmbeddings` 为 `DashScopeTextEmbedding`，替换 `CohereRerank` 为 `DashScopeRerank` |
| **我要为电商平台实现“以图搜同款”，支持用户上传截图匹配商品详情页** | 向量与排序（多模态） | 使用 `/multimodal-embedding` 对用户截图 + 商品图文生成融合向量，再用 `/rerank` 精排候选商品 |
| **我需要同时管理 50 个客户专属知识库，并按客户 ID 动态路由查询** | RAG API + 长期记忆组合 | RAG 管理各客户知识库；长期记忆记录客户偏好（如“客户A只看英文文档”），在 Agent 中注入 `search_filters` 实现动态过滤 |
| **我的应用对延迟极其敏感（<200ms），且每次只查 1 个 query + 10 个候选** | 向量与排序（同步接口） | 直接调用 `/rerank`，避免 RAG 的多跳调度开销；`qwen3-rerank` 同步平均 P99 < 150ms（北京地域） |

> **重要提醒**：  
> - **不要混用“配置即生效”与“发布才生效”逻辑**：RAG 的 `rerankModelName` 和 `agent_model` 必须通过 Agent 发布才能生效；长期记忆的 `plan_version` 和 `profile_schema` 在写入/检索时实时生效；向量模型参数（如 `dimensions`）在每次请求中显式指定。  
> - **命名一致性需手动校验**：RAG 接口存在 `indexId`/`index_id`、`docIds`/`doc_id` 等大小写差异；长期记忆统一使用 `snake_case`（如 `user_id`, `project_id`）；向量服务严格遵循 OpenAI 兼容规范（`input`, `model`, `dimensions`）。  
> - **错误处理策略不同**：RAG 返回 `429` 时需关注 `Retry-After`；长期记忆限流为账号级 QPM，建议加分布式令牌桶；向量服务批处理失败需检查 URL 权限与文件格式，结果 URL 24 小时过期。  

---  
*最后更新：2025年4月 | 百炼平台技术文档中心*

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


