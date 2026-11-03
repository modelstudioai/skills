# RAG 与[长期记忆](../concepts/long-term-memory.md)（LTM）技术对比

本页旨在为百炼平台开发者提供 **RAG（[检索增强生成](../concepts/rag.md)）** 与 **[长期记忆](../concepts/long-term-memory.md)（Long Term Memory, LTM）** 两类核心知识管理能力的系统性对比，帮助技术团队在构建智能应用（如客服助手、企业知识中枢、个性化 Agent）时，基于场景目标、数据特性、架构约束和成本模型，做出清晰、可落地的技术选型决策。二者虽均涉及“记忆”与“检索”，但在设计哲学、数据生命周期、调用范式及适用边界上存在本质差异：**RAG 面向外部结构化/非结构化知识的静态建模与按需检索，LTM 则聚焦于对话过程中动态沉淀的用户与业务事实的持久化与上下文感知注入**。

---

## 关键维度对比

| 维度 | RAG API | [长期记忆](../concepts/long-term-memory.md)（LTM） |
|------|---------|----------------|
| **核心定位** | 外部知识库的全生命周期管理 + 语义检索/问答服务 | 对话中动态生成的关键事实与用户画像的结构化持久化与自动上下文注入 |
| **输入格式** | 支持[多模态](../concepts/multi-modal.md)原始数据：<br>• 文本（PDF/Word/Markdown/TXT 等）<br>• 表格（CSV/Excel）<br>• 图片（JPG/PNG）<br>• 音视频（MP4/MKV，需转文本或帧提取）<br>• 结构化 JSON 数据 | 严格结构化输入：<br>• `fragment`：纯文本 `content`（≤8192 字符），含可选 `metadata`<br>• `profile`：键值对字典 `profile_fields`（≤100 对），绑定 `user_id` |
| **输出格式** | • 检索接口（`/knowledge/search`）：返回带相关性分数、来源文档片段、元数据的 JSON 数组<br>• 问答接口（`/knowledge/chat`）：SSE 流式响应，含规划（Plan）、工具调用（Tool Call）、生成（Generation）三阶段结构化事件 | • 写入：返回 `memory_id` 及状态<br>• 检索（自动注入）：无独立输出；记忆内容作为隐式上下文注入到 LLM 的 `messages` 中，影响最终生成结果<br>• 显式检索需通过 `/memories/search`（非默认路径，需额外调用）获取 JSON 列表 |
| **支持模型** | • 嵌入模型：`text-embedding-v4`、`qwen3-vl-embedding` 等可配置<br>• 重排模型：`qwen3-rerank` 等可配置<br>• Agent 生成模型：`qwen3.7-plus`、`qwen-max` 等任意百炼支持的大模型（与记忆能力无关） | • **仅限特定模型版本**：`qwen-max`、`qwen-plus`、`qwen-turbo` 的 `v20240915+` 版本<br>• 模型必须显式启用记忆能力（API 请求中设置 `enable_retrieval: true` 或 system message） |
| **API 端点** | • 统一 DashScope 网关：<br> `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`<br>• 分层路径：<br> `/api/v1/indices/rag/...`（管理）<br> `/api/v1/indices/knowledge/search`（运行时检索）<br> `/api/v2/apps/knowledge/chat`（运行时问答） | • 独立 LTM 网关（与 ChatCompletion 同域）：<br> `https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/memories`<br>• 写入/批量操作使用 `/memories` 和 `/memories/batch`<br>• 检索依赖 ChatCompletion 接口的 `enable_retrieval` 参数或 system message 触发 |
| **计费方式** | • 按调用量分项计费：<br> – 知识库创建/更新（次）<br> – 文档导入（GB）<br> – 检索请求（次）<br> – 问答请求（次）<br> – 嵌入/重排 [Token](../concepts/token.md)（千 [Token](../concepts/token.md)）<br>• 无记忆条目存储费，但知识库容量有配额限制 | • **按记忆条目数计费**：<br> – 写入每条 `fragment` 或 `profile` 计为 1 条<br> – 存储按条目数 × 时长（TTL）计费（当前免费试用期后按月结算）<br>• 无独立检索调用费，但计入 ChatCompletion 总 [Token](../concepts/token.md) 消耗 |
| **典型场景** | • 企业知识库问答（HR政策、产品手册）<br>• 客服工单辅助（历史案例检索）<br>• [多模态](../concepts/multi-modal.md)内容搜索（图文混搜、视频关键帧问答）<br>• 数据库自然语言查询（Table RAG） | • 多轮对话中的用户偏好记忆（“上次说喜欢Python教程”）<br>• 跨会话身份延续（“用户张三的公司是阿里云”）<br>• 销售线索沉淀（“客户预算50万，关注AIGC方案”）<br>• 个性化内容推荐（基于画像动态调整生成风格） |

---

## 适用场景建议

### ✅ 优先选用 RAG 的场景：
- **知识源稳定、规模较大、需专业检索能力**：如将 1000 份 PDF 产品文档构建成可精准回答“XX功能如何配置”的知识库。
- **要求强溯源与可解释性**：需明确返回答案对应的具体文档页码、表格行、图片区域。
- **处理非文本模态**：需对图片中的图表、音视频中的语音内容进行语义理解与问答。
- **知识更新频率低（周/月级）**：适合批量导入与离线索引构建。
- **需细粒度权限控制与多租户隔离**：RAG 知识库天然支持按业务空间、Agent、类目分级管理。

### ✅ 优先选用 LTM 的场景：
- **对话状态强依赖上下文延续**：如智能导购需记住用户已浏览商品、筛选条件、价格敏感度。
- **用户画像需跨会话聚合与演化**：如教育 App 持续积累学生错题类型、掌握程度、学习节奏。
- **事实需高频写入与实时检索**：如客服系统在每轮对话中自动记录“用户投诉订单号：123456”，下轮自动关联。
- **数据高度结构化且语义简单**：如 `{"user_id": "u789", "preferred_language": "zh", "last_purchase_date": "2024-06-01"}`。
- **追求极简集成**：只需在 ChatCompletion 请求中加一行 `{"use_memory": true}` 即可启用，无需单独建库、切片、索引。

### ⚠️ 不建议混合滥用的场景：
- **将 LTM 当作小型知识库使用**：LTM 单条内容上限 8KB，不支持 PDF 解析、表格结构识别、图片 OCR，无法替代 RAG 处理复杂文档。
- **用 RAG 存储用户对话摘要**：RAG 知识库无用户维度隔离、无 TTL 自动过期、无 profile 字段合并能力，维护成本高且易污染。
- **在无记忆能力模型上强行调用 LTM**：`qwen-turbo-v20240601` 等旧版模型调用 LTM 将静默失败，必须核验模型版本。

---

## 技术选型参考（面向开发者）

| 选型考量点 | 推荐方案 | 说明 |
|------------|----------|------|
| **是否需要处理原始文件（PDF/Excel/图片）？** | → RAG | LTM 仅接受纯文本或结构化键值，无文件解析能力。 |
| **知识是否来自外部系统（如 CRM、ERP、文档中心）？** | → RAG | RAG 提供 OSS 直传、数据库连接器等标准化接入方式；LTM 需业务侧自行抽取并调用写入 API。 |
| **是否需支持“用户说‘查我上个月的报销’”，自动关联其身份与历史数据？** | → LTM | RAG 无法绑定 `user_id`，也无法自动注入用户专属上下文；LTM 的 `profile` 类型专为此设计。 |
| **是否要求每次问答都返回答案出处（文档名+页码）？** | → RAG | LTM 检索结果不暴露原始来源，仅作为隐式提示影响生成。 |
| **是否需在单次请求中同时检索 10 个不同知识库（如法务库+财务库+IT库）？** | → RAG | RAG Agent 支持 `enable_kb_router` 自动路由；LTM 是全局向量池，无知识库概念。 |
| **是否希望记忆自动随对话轮次衰减（如 24 小时后失效）？** | → LTM | RAG 无 TTL 机制；LTM 的 `ttl_seconds` 可精确控制生命周期。 |
| **团队无 NLP 工程师，希望最快上线一个“记住用户喜好”的 Bot？** | → LTM | 5 行代码即可启用（写入 profile + ChatCompletion 开启 memory）；RAG 需完成知识库创建、文档清洗、Agent 配置、发布等 10+ 步骤。 |

> **最佳实践提示**：  
> - **组合使用更强大**：典型架构为 *RAG 提供领域知识底座* + *LTM 注入用户上下文*。例如：客服机器人先用 RAG 检索“退换货政策”，再用 LTM 注入“用户张三近 3 次投诉均因物流延迟”，最终生成个性化回复。  
> - **注意配额与限流**：RAG 的 `knowledge/chat` 接口默认 25 QPS，而 LTM 写入受应用级 10 万条配额约束，高并发场景需提前申请扩容。  
> - **监控重点不同**：RAG 应关注检索召回率、答案准确率、嵌入延迟；LTM 应监控记忆写入成功率、检索命中率、profile 字段覆盖率。  

---  
*最后更新：2024年10月*

## 被对比主题页

- [rag api](../api/rag-api.md)
- [long term memory new](../api/long-term-memory-new.md)


