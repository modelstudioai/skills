# RAG、知识库与[长期记忆](../concepts/memory.md)方案对比

为帮助开发者在百炼平台上高效构建具备上下文理解、领域知识融合与用户状态延续能力的智能应用，本文对三种核心能力——**RAG API（[检索增强生成](../concepts/rag.md)服务接口）**、**知识库（Knowledge Base，面向文档/数据的知识管理载体）** 和 **[长期记忆](../concepts/memory.md)（Long Term Memory, LTM，面向用户/会话的状态持久化机制）** 进行系统性对比分析。三者虽均依赖向量检索与大模型协同，但在设计目标、数据边界、生命周期、集成方式及适用场景上存在本质差异。本对比聚焦技术选型关键维度，旨在为架构设计与方案落地提供清晰、可执行的决策依据。

## 关键维度对比

| 维度 | RAG API | 知识库（Knowledge Base） | [长期记忆](../concepts/memory.md)（Long Term Memory） |
|------|---------|---------------------------|------------------------------|
| **核心定位** | **开发者导向的底层能力接口集**：提供知识库全生命周期管理、Agent 封装、运行时检索/问答等原子能力，强调可控性与可编排性 | **产品化知识服务载体**：面向业务人员与开发者的一站式知识管理平台，集成解析、切片、向量化、检索、问答、监控等端到端功能，强调开箱即用与体验一致性 | **结构化用户状态持久化机制**：专为多轮对话与跨会话场景设计，用于存储事实片段（Fragments）与用户画像（Profiles），强调低延迟读写与语义连续性 |
| **输入格式** | • 文档文件（PDF/DOCX/MD/PNG/JPG/MP4 等）<br>• 原始文本/JSON 结构化数据<br>• `docIds`、`chunkId`、`leaseId` 等显式 ID 字符串<br>• Agent 配置 JSON（含 `agent_model`, `rerankModelName` 等） | • 控制台拖拽上传或 API 批量导入的多模态文件<br>• 支持 OCR、版面恢复、大模型结构化解析<br>• 切片策略（按页/标题/智能分段）在创建时静态配置<br>• 检索/问答请求体含 `query`, `top_k`, `temperature` 等参数 | • `fragment`: 短文本事实（≤2048 字符），支持语义嵌入与去重<br>• `profile`: 键值对（key ≤64 字符，value ≤1024 字符），支持类型校验与 TTL<br>• 必填 `memory_type`（`fragment`/`profile`）、`namespace`、`user_id` |
| **输出格式** | • 管理类接口：标准 REST 响应（`code`, `message`, `request_id`）<br>• 检索接口（`/rag/index/retrieve`）：返回原始 `chunks` 数组（含 `content`, `metadata`, `score`）<br>• 问答接口（`/apps/knowledge/chat`）：SSE 流式响应或 JSON 格式回答 + 引用切片 | • 检索服务：返回带元数据的切片列表（`chunks`），支持高亮与来源定位<br>• 问答服务：结构化 JSON 或 SSE 流式响应，含 `answer`, `references`, `thoughts`（启用 thinking 时）<br>• Playground 提供可视化调试界面与日志回溯 | • `/v1/memory/query`: 返回匹配的 `fragments` 或 `profiles` 列表（含 `id`, `content`/`value`, `score`, `ttl_seconds`）<br>• `/v1/chat/completions`（启用 `enable_memory`）：模型自动注入相关记忆，不显式返回记忆内容 |
| **支持模型** | • **嵌入模型**：`text-embedding-v4`, `qwen3-vl-embedding`（可指定）<br>• **重排模型**：`qwen3-rerank`, `qwen3-vl-rerank`（可配置）<br>• **生成模型**：由绑定的 Agent 指定（如 `qwen3.7-plus`），非 RAG API 自身能力 | • **嵌入模型**：默认 `text-embedding-v4`，创建后不可更改；支持自定义选择<br>• **重排模型**：`qwen3-rerank`, `qwen3-vl-rerank`（服务级配置）<br>• **生成模型**：问答服务绑定 `qwen3.6-plus` 等 Qwen 系列模型，支持 `temperature`, `enable_thinking` 等调控 | • **原生支持模型**：仅 `qwen-max`, `qwen-plus`, `qwen-turbo`（v202409+）可自动注入/更新记忆<br>• **通用支持**：所有模型均可通过显式调用 `/v1/memory/query` & `/v1/memory/upsert` 接口管理记忆<br>• **嵌入模型**：可选 `text-embedding-v3`，未指定则用平台默认 |
| **API 端点（典型）** | • 管理：`/api/v1/indices/rag/index/create_v2`<br>• 导入：`/api/v1/connector/dash/addFile` + `/api/v1/indices/rag/index/job/create`<br>• 检索：`/api/v1/indices/knowledge/search`（需 `agent_id`）<br>• 问答：`/api/v2/apps/knowledge/chat`（需 `agent_id`） | • 底层检索：`/api/v1/indices/rag/index/retrieve`（单库）<br>• 应用检索：`/api/v1/indices/knowledge/search`（多库联合，需 `agent_id`）<br>• 问答：`/api/v2/apps/knowledge/chat`（需 `agent_id`）<br>• 控制台服务发布后生成独立 endpoint | • 查询：`POST /v1/memory/query`<br>• 写入：`POST /v1/memory/upsert`<br>• 注入调用：`POST /v1/chat/completions`（`enable_memory: true`）<br>• 删除：`POST /v1/memory/delete_by_filter` |
| **计费方式** | • 按 **API 调用量** 计费：<br>  – 知识库管理类（创建/删除/更新）：按次<br>  – 数据导入（解析/切片/向量化）：按文档页数或字节数<br>  – 运行时检索/问答：按 token（输入+输出）或请求次数<br>• 具体费率见 [RAG API 计费说明](../../raw/application-api-reference/rag-api/rag-api-billing.md) | • 按 **知识库规格 + 使用时长** 计费：<br>  – 标准版（含向量索引、基础检索、问答）<br>  – 高级版（含多模态、Agentic 检索、高级安全控制）<br>• 提供 720 小时一次性免费额度（2026 年起正式计费） | • 按 **记忆存储量 + API 调用量** 计费：<br>  – 存储量：按 GB/月（`fragment` + `profile` 总占用）<br>  – 调用量：`/v1/memory/query` & `/v1/memory/upsert` 按次计费<br>• 不与模型调用费用捆绑，独立计量 |
| **典型场景** | • 构建定制化 RAG Pipeline（如私有协议解析、混合检索策略编排）<br>• 需要精细控制切片逻辑、嵌入/重排模型选型的中大型项目<br>• 与 LangChain/LlamaIndex 等框架深度集成<br>• 需要审计级日志与错误追踪（强依赖 `request_id`） | • 快速上线客服知识库、内部文档助手、产品 FAQ 机器人<br>• 非技术用户主导的知识运营（上传→调试→发布）<br>• 多模态知识服务（图片问答、音视频搜索）<br>• 需要统一监控、SLS 日志投递与权限管控的企业级部署 | • 智能客服中的用户偏好记忆（如“上次说喜欢简体中文”）<br>• 电商导购中持续积累的用户兴趣画像（`preferred_brand`, `size_preference`）<br>• 多轮会议助手中的待办事项跟踪与事实确认（“你提到下周三开会，已记下”）<br>• Agent 中需要跨会话复用的轻量级状态（非文档级知识） |

## 各方案的适用场景建议

- **优先选用 RAG API 当**：  
  你的团队具备较强工程能力，需要**完全掌控知识处理链路**（例如：自定义 PDF 解析规则、动态切换嵌入模型、组合关键词+向量+重排三级检索、对接自有向量数据库）。适用于构建 PaaS 平台、AI 中台能力底座，或对延迟、精度、审计有严苛要求的金融、政企场景。⚠️ 注意：需自行处理鉴权、限流、错误重试、ID 命名不一致等细节，开发成本较高。

- **优先选用知识库当**：  
  你的目标是**以最短路径交付高质量知识服务**，且数据源以文档为主（PDF/Word/网页等）。适用于业务部门自助建设知识助手、快速验证 RAG 效果、或作为第三方低代码平台（Dify/Coze）的后端知识引擎。其控制台 + Playground + CLI 的三层体验大幅降低使用门槛，但牺牲了底层灵活性（如切片策略不可变、嵌入模型不可更换）。

- **优先选用长期记忆当**：  
  你的应用核心诉求是**维护用户级、会话级的轻量事实与偏好**，而非管理海量文档知识。适用于构建个性化 Agent、多轮对话机器人、用户旅程分析系统。LTM 与模型深度耦合（尤其 `qwen-*` 系列），能实现“无感记忆注入”，但**不能替代知识库存储文档内容**——它存储的是“用户说了什么”，而非“文档里写了什么”。

> ✅ **最佳实践组合**：  
> 在复杂智能体应用中，三者常协同使用：  
> **知识库** 作为企业级文档知识中枢（如产品手册、合同模板）；  
> **RAG API** 用于构建定制化知识服务网关（如路由至不同知识库、融合外部 API 结果）；  
> **长期记忆** 作为用户侧状态层（如“用户刚咨询过退款政策，当前对话应优先关联该知识库”）。  
> 此时，知识库提供“域知识”，LTM 提供“用户上下文”，RAG API 提供“调度与编排能力”。

## 面向开发者的技术选型参考

| 选型考量 | RAG API | 知识库 | 长期记忆 |
|----------|---------|--------|----------|
| **是否需要完全自主控制知识处理流程？** | ✅ 强推荐 | ❌ 不适用（封装过深） | ❌ 不适用（仅状态层） |
| **是否以文档/数据文件为主要知识源？** | ✅ 可用，但需编码集成 | ✅ 最佳匹配 | ❌ 不适用（非文档存储） |
| **是否需快速验证 RAG 效果或交付 MVP？** | ⚠️ 可用，但学习曲线陡峭 | ✅ 强推荐（控制台 5 分钟上线） | ⚠️ 仅适用于状态类 MVP |
| **是否需存储用户偏好、行为画像等轻量事实？** | ❌ 不适用（无用户状态模型） | ⚠️ 可通过元数据模拟，但非设计本意 | ✅ 强推荐（原生支持 Profiles/Fragments） |
| **是否需跨会话保持上下文连续性？** | ❌ 不提供会话状态管理 | ⚠️ 问答服务支持单次会话上下文，但无跨会话持久化 | ✅ 强推荐（TTL 与 namespace 隔离保障） |
| **是否需与 LangChain/LlamaIndex 等框架集成？** | ✅ 官方 SDK 与适配器完善 | ⚠️ 需通过 REST API 封装，无原生链式支持 | ⚠️ 需手动注入 `memory` 到 Chain 中 |
| **是否关注细粒度计费与成本优化？** | ✅ 按调用精确计量，适合流量波动大的场景 | ⚠️ 按规格包月，适合稳定中高负载 | ✅ 存储+调用分离计费，适合低频高价值状态存储 |

**最终建议**：  
- **起步阶段**：从知识库开始，利用 Playground 快速验证效果，再逐步用 RAG API 替换关键环节；  
- **规模化阶段**：用 RAG API 构建统一知识网关，将多个知识库与 LTM 统一编排；  
- **个性化阶段**：在所有对话入口启用 LTM，并将高频用户意图（如“查订单”）自动触发知识库检索，形成“LTM → RAG → Knowledge Base”的闭环增强

## 被对比主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [long term memory new](../api/long-term-memory-new.md)


