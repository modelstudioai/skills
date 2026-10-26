# RAG 与[长期记忆](../concepts/long-term-memory.md)能力对比

## 背景与目的  
在百炼平台构建智能应用时，开发者常需解决两类关键上下文问题：  
- **外部知识增强**：如何让模型准确、可靠地引用企业私有文档（如产品手册、合同、FAQ）、多模态资料（PDF/音视频/图片）等结构化或非结构化知识？  
- **用户状态延续**：如何在跨会话、多轮对话中持续记住用户身份、偏好、历史行为等个性化事实，避免重复提问、提升体验一致性？  

RAG（[检索增强生成](../concepts/rag.md)）与[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）是百炼平台提供的两种互补但定位迥异的底层能力。本文旨在从技术实现、接口设计、适用边界和工程实践角度进行系统性对比，帮助开发者清晰理解二者本质差异，规避常见误用（如用 RAG 存用户手机号、用 LTM 管理 10GB 技术文档），并基于真实业务需求做出高效、可维护的技术选型。

---

## 关键维度对比

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（LTM） |
|------|---------|----------------|
| **核心定位** | 外部知识库的**离线构建 + 在线检索增强**，聚焦“**我知道什么**”（领域知识） | 用户级事实与画像的**在线持久化 + 动态召回**，聚焦“**你是什么样的人**”（个体状态） |
| **输入格式** | 支持多源异构数据：<br>• 文档类：PDF/Word/Excel/PPT/Markdown/TXT/HTML<br>• 多模态：MP4/MOV/AVI（音频+视频）、JPG/PNG（图像）<br>• 结构化：数据库连接器、API 数据源<br>• 元数据：自定义 `category_id`、`doc_id`、标签等 | 严格结构化输入：<br>• 事实记忆（Fragments）：`fragment_key`（字符串键） + `value`（≤8192 字符值） + 可选 `profile_id`<br>• 用户画像（Profiles）：`profile_id` + JSON 对象（字段数 ≤1000，支持嵌套） |
| **输出格式** | • 检索接口（`/search`）：返回带相关性分数、来源文档片段、元数据的结构化结果数组<br>• 问答接口（`/chat`）：SSE 流式响应，含规划→工具调用→生成三阶段 token 流，附带引用溯源信息（`citations`） | • 查询接口（`GET /fragments/{key}` 或 `GET /profiles/{id}`）：返回精确匹配的 JSON 对象<br>• 语义搜索（`POST /fragments/search`）：返回按相关性排序的 Fragment 列表（实验性）<br>• 自动注入：在 `/v1/chat/completions` 响应中，以系统消息形式插入记忆内容（仅流式生效） |
| **支持模型** | **无模型绑定**：所有 RAG 接口独立于大模型运行；检索与问答结果可被任意兼容模型（Qwen 系列、第三方模型）消费；嵌入/重排模型可自由指定（如 `text-embedding-v4`, `qwen3-rerank`） | **强模型绑定**：仅 `qwen-max`、`qwen-plus`、`qwen-turbo` 原生支持自动记忆注入（`enable_long_term_memory: true`）；其他模型需手动拼接记忆文本到 `messages` 中 |
| **API 端点** | • 知识库管理：`/api/v1/indices/rag/index/*`<br>• 数据导入：`/api/v1/connector/dash/*`, `/api/v1/indices/rag/index/job/*`<br>• 运行时检索：`/api/v1/indices/knowledge/search`<br>• 运行时问答：`/api/v2/apps/knowledge/chat`<br>• Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com` | • 写入：`POST /v1/memory/fragments`, `POST /v1/memory/profiles`<br>• 查询：`GET /v1/memory/fragments/{key}`, `GET /v1/memory/profiles/{id}`, `POST /v1/memory/fragments/search`<br>• 注入：在 `/v1/chat/completions` 请求头或消息体中启用<br>• Base URL：统一 DashScope 网关（同 RAG） |
| **计费方式** | 按**调用量分项计费**：<br>• 知识库创建/更新/删除：按次<br>• 文档切片/导入任务：按文档页数或字节数<br>• 检索请求（`/search`）：按 QPS 和调用次数<br>• 问答请求（`/chat`）：按 token 数 + 检索调用次数<br>• 监控查询（`/monitor`）：按次（低频） | 按**存储量 + 操作次数**计费：<br>• 记忆写入（Fragments/Profiles）：按条计费<br>• 记忆查询（GET）：按次计费<br>• 语义搜索（POST）：按次计费<br>• **存储空间**：按占用的结构化数据量（KB/MB）月结；过期自动清理不产生费用 |
| **典型场景** | • 客服机器人：基于产品文档、工单记录回答技术问题<br>• 合规审查助手：检索合同条款、监管文件并生成摘要<br>• 多模态知识库：上传会议录像+PPT+会议纪要，支持“找张总提到AI落地的那段视频”<br>• Agent 工具调用：作为 `retrieval` 工具为 Agent 提供实时知识支撑 | • 电商导购：记住用户尺码偏好、常购品类、过敏史（`profile_id=uid_123`）<br>• 金融顾问：持久化用户风险测评结果、持仓偏好、联系方式（`fragment_key="user_risk_level"`）<br>• SaaS 应用：跨会话保持用户界面主题、语言设置、常用筛选条件<br>• 个性化推荐：动态更新用户近期点击/收藏行为，用于实时重排 |

---

## 适用场景建议

### ✅ 优先选用 RAG 的场景：
- **知识规模大、更新频率低**：如企业知识库（>1000 份文档）、法规库、历史档案。
- **内容非结构化、需语义理解**：PDF 表格识别、音视频语音转文字后检索、图片 OCR 文字搜索。
- **要求强溯源与可解释性**：需明确告知用户答案来自哪份文档第几页，满足审计或合规要求。
- **多租户隔离需求强**：通过 `workspace_id` + 独立知识库 ID 实现物理级数据隔离。
- **需联合多知识源检索**：同时查询“产品文档库”+“客户案例库”+“内部 Wiki”。

### ✅ 优先选用长期记忆（LTM）的场景：
- **用户粒度状态管理**：需在不同会话、不同设备间同步同一用户的偏好、身份属性、行为快照。
- **高频读写、低延迟要求**：如每轮对话都需读取/更新用户当前购物车状态、登录令牌、临时决策标记。
- **数据高度结构化、键值明确**：如 `user_email`, `preferred_language`, `last_order_time` 等可枚举字段。
- **需与 Qwen 原生模型深度集成**：利用 `enable_long_term_memory: true` 自动注入，减少应用层上下文拼接逻辑。
- **轻量级、免运维状态存储**：替代自建 Redis/MySQL 存储用户 session 级别元数据。

### ⚠️ 明确不推荐的误用模式：
- **❌ 用 RAG 存储用户手机号、地址等隐私字段**：<br>→ RAG 不提供字段级权限控制、不支持 TTL 自动过期、删除不可逆、审计成本高；应使用 LTM 的 `fragments` 并设 `ttl_seconds`。
- **❌ 用 LTM 管理 500 页 PDF 或 2 小时会议录像**：<br>→ LTM 单 value 限 8KB，不支持分块、OCR、音视频解析；应使用 RAG 导入并切片。
- **❌ 在非 Qwen 模型上强制开启 `enable_long_term_memory: true`**：<br>→ 该参数对 `qwen-turbo` 以外模型无效，且可能引发未知错误；需手动构造上下文。
- **❌ 依赖 LTM 事务性写入**：<br>→ LTM 不保证强一致性，高并发写同一 `fragment_key` 可能丢失中间状态；关键业务（如库存扣减）仍需自有数据库。

---

## 技术选型参考（面向开发者）

| 选型考量 | RAG API | 长期记忆（LTM） | 建议动作 |
|----------|---------|----------------|----------|
| **是否需要处理原始文件（PDF/视频/图片）？** | ✅ 是 | ❌ 否 | 选 RAG；LTM 仅接受纯文本键值对 |
| **数据所有权归属用户个体（而非企业知识）？** | ❌ 否（属知识库所有者） | ✅ 是（绑定 `profile_id`） | 选 LTM；RAG 无用户维度抽象 |
| **是否要求每次检索返回原文片段及出处？** | ✅ 是（`citations` 字段） | ❌ 否（仅返回值） | 选 RAG；LTM 返回即最终值，无溯源 |
| **是否需支持毫秒级写入+亚秒级读取（如实时聊天状态）？** | ⚠️ 否（导入有延迟，检索依赖向量索引构建） | ✅ 是（写入后 1–3 秒内可查） | 选 LTM；RAG 更适合准实时（分钟级） |
| **是否已有成熟向量数据库或定制 Embedding 流程？** | ⚠️ 可替换（支持自定义嵌入模型） | ❌ 否（完全托管，不可替换） | 若需深度定制向量能力，RAG 更开放；若求开箱即用，LTM 更省心 |
| **是否需与百炼 Agent 框架深度协同？** | ✅ 是（Agent 可直接配置 `kb_search_configs` 调用 RAG） | ⚠️ 有限（仅通过 `enable_long_term_memory` 注入，无法作为 Agent 工具显式调用） | 构建复杂 Agent 时，RAG 是首选知识工具；LTM 作为隐式上下文增强 |

> **终极建议**：**RAG 与 LTM 并非互斥，而是天然协同**。典型高阶架构为：  
> **用户请求 → LTM 查询用户画像/偏好 → 注入至 Prompt → 调用 RAG 检索领域知识 → Agent 规划 → RAG 获取具体文档片段 → 模型生成答案**。  
> 百炼平台已支持在同一应用中同时启用二者——开发者只需分别调用对应 API，并在 `messages` 中合理组织上下文顺序即可。

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


