# [长期记忆](../concepts/long-term-memory.md)与向量检索能力对比

## 对比目的与背景

在构建智能 Agent、个性化推荐系统或[检索增强生成](../concepts/rag.md)（RAG）应用时，开发者常需在「结构化长期状态管理」与「通用语义检索能力」之间进行技术选型。百炼平台同时提供两类核心能力：  
- **[长期记忆](../concepts/long-term-memory.md)（Long Term Memory）**：面向 Agent 场景设计的、带用户/项目隔离、支持事实建模与画像抽取的**结构化记忆服务**；  
- **向量与排序（Vector and Sort）**：面向通用嵌入与重排序任务的**底层向量计算能力**，不维护状态，无数据持久化逻辑。  

本对比旨在帮助开发者清晰区分二者定位、能力边界与集成路径，避免误用（如用向量 API 实现用户画像存储）、规避计费与架构风险，并为 Agent 构建、RAG 优化、个性化建模等典型场景提供可落地的技术选型依据。

---

## 关键维度对比

| 维度 | [长期记忆](../concepts/long-term-memory.md)（Long Term Memory） | 向量与排序（Vector and Sort） |
|------|-----------------------------|------------------------------|
| **核心定位** | 结构化记忆管理服务：持久化存储、语义检索、动态更新用户/技能/画像数据 | 底层向量计算能力：文本/图像嵌入生成、候选结果相关性重排序 |
| **输入格式** | JSON Body，含 `user_id`、`messages`（对话上下文）、`profile_schema`（可选）、`memory_types` 等结构化字段；支持多模态 `image_url`（仅限启用项目） | 模型强约束：<br>• 文本向量：`string` 或 `string[]`<br>• 多模态向量：`[{ "image": "base64...", "text": "..." }]`<br>• Rerank：`{ "query": "...", "documents": [...] }` |
| **输出格式** | 语义检索返回 `memory_nodes` 列表，含 `id`、`type`（`observation`/`skill`/`profile`）、`content`、`score`、`metadata`；画像接口返回结构化 JSON（如 `{"age": 28, "interests": ["AI", "travel"]}`） | • 文本向量：`{ "data": [{ "embedding": [0.12, ..., 0.87], "index": 0 }] }`（维度固定为 1024）<br>• Rerank：`{ "results": [{"index": 1, "relevance_score": 0.95}] }`（无原始向量） |
| **支持模型/功能** | 内置统一服务，不暴露底层模型选择；按 `plan_version=pro/lite` 控制检索精度（如 `min_score` 过滤），`skill` 类型需导出获取完整元信息 | 显式指定模型：<br>• `text-embedding-v3`（文本向量）<br>• `multimodal-embedding-v1`（图文联合嵌入）<br>• `rerank-v3`（重排序）<br>旧版模型（如 `text-embedding-v1`）已下线 |
| **API 端点** | 全部以 `/v1/long-term-memory/...` 开头：<br>• `POST /add`（同步写入）<br>• `POST /add-async`（异步写入）<br>• `POST /memory_nodes/search`（语义检索）<br>• `GET /profile_schemas/{id}/user_profile`（查画像） | 统一基础路径 `/v1/`：<br>• `POST /embeddings`（同步向量）<br>• `POST /embeddings/async`（异步文本向量）<br>• `POST /rerank`（同步重排序）<br>• 不支持异步 rerank / 多模态向量 |
| **认证方式** | DashScope API Key 鉴权（`Authorization: Bearer $DASHSCOPE_API_KEY`），与平台其他服务一致 | 同样使用 DashScope API Key 鉴权，Header 格式完全一致 |
| **计费方式** | 自 **2026 年 8 月 20 日起正式商业化**：<br>• `Pro` 版本：支持 `min_score` 过滤、高精度检索，按调用次数计费<br>• `Lite` 版本：基础检索能力，价格更低<br>• 所有 `Add` / `Search` / `GetProfile` 调用均计费 | 按调用次数计费，**当前已商用**：<br>• 文本向量：按 `input` 条数计费（单次最多 128 条）<br>• 多模态向量：按 `input` 条数计费（单次最多 32 条）<br>• Rerank：按 `documents` 数量计费（单次最多 100 条） |
| **数据持久化** | ✅ 是。所有写入的记忆节点默认持久化至用户专属记忆库，支持后续任意时间点检索、更新、删除 | ❌ 否。纯计算服务，无状态、不存储任何输入/输出数据，结果需由调用方自行保存 |
| **用户/项目隔离** | ✅ 强隔离：<br>• 必填 `user_id` 实现跨用户隔离<br>• 可选 `memory_library_id` / `project_ids` 实现多租户/多项目分组 | ❌ 无隔离机制。所有请求在模型层平等处理，隔离逻辑需由上层业务实现（如在向量数据库中添加 `user_id` 字段） |
| **典型场景** | • Agent 的上下文持久化（记住用户偏好、历史操作）<br>• 技能复用管理（提取并调用 `skill` 流程）<br>• 用户画像实时构建与查询（基于预定义 schema）<br>• 跨会话个性化响应生成 | • RAG 中对召回文档做向量化 & 重排序<br>• 搜索引擎语义召回<br>• 图文内容匹配（如商品图搜）<br>• 推荐系统候选集精排 |

---

## 适用场景建议

### ✅ 优先选用 **长期记忆** 当：
- 需要为每个用户独立维护行为记录、技能模板或结构化属性（如年龄、职业、兴趣标签）；
- Agent 需在多次对话中“记住”用户说过的话、做过的事，并据此生成个性化响应；
- 业务要求记忆数据可被显式增删改、支持分页列表、导出分析，且需与 `user_id` 强绑定；
- 已有画像 schema 定义，希望在写入对话时自动触发结构化抽取（如从“我今年35岁，喜欢爬山”中提取 `age=35`, `hobbies=["hiking"]`）；
- 对检索结果要求可解释性（如返回 `skill_name` 和 `skill_description`）及业务语义过滤（如只查 `type=skill` 且 `score > 0.7`）。

### ✅ 优先选用 **向量与排序** 当：
- 构建 RAG 系统，需将外部知识库文档批量向量化并存入向量数据库（如 Milvus、PGVector），再结合 query 向量做相似度检索；
- 需对搜索引擎或推荐系统返回的粗筛结果（如 top-50）进行细粒度相关性重打分与重排序；
- 处理多模态内容（如电商场景中用商品图+标题联合嵌入，实现以图搜图/以图搜商品）；
- 需要灵活控制嵌入维度、归一化方式（如 `encoding_format=base64` 降低传输体积），或需直接参与向量距离计算（如余弦相似度）；
- 无用户状态管理需求，仅需一次性的、无状态的语义计算能力。

### ⚠️ 注意：二者可协同，但不可替代
- **典型协同模式**：  
  使用 `vector and sort` 将知识库文档向量化并存入自建向量库 → 用户提问时，先用 `vector and sort` 获取 query 向量并在向量库中召回候选 → 再调用 `long term memory` 的 `search` 接口，融合用户历史记忆（如过往提问、已掌握技能）进行上下文增强排序。  
- **禁止替代场景**：  
  ❌ 不可用 `vector and sort` 替代 `long term memory` 存储用户画像——因前者不持久化、无 `user_id` 隔离、无法结构化抽取；  
  ❌ 不可用 `long term memory` 替代 `vector and sort` 做通用文档嵌入——因前者不开放向量输出、不支持批量文档编码、无 `rerank` 功能。

---

## 开发者技术选型参考

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我要让 Agent 记住用户上次说想学 Python，并在下次主动推荐教程” | ✅ 长期记忆 | 支持 `user_id` 隔离 + `observation` 类型写入 + 跨会话语义检索 |
| “我有一份 10 万条 FAQ 文档，需要支持用户自然语言提问并返回最匹配的 3 条” | ✅ 向量与排序 + 自建向量库 | `text-embedding-v3` 提供高质量嵌入，`rerank-v3` 可进一步提升 top-K 准确率；长期记忆不适用于海量外部知识索引 |
| “我需要从用户聊天记录中自动提取‘所在城市’‘预算范围’‘购买意向’等字段” | ✅ 长期记忆（Profile） | 必须先定义 `profile_schema`，再在 `AddMemory` 中传入，由平台完成结构化抽取与存储 |
| “我的 App 支持拍照识物，需根据图片匹配商品库中的图文描述” | ✅ 向量与排序（多模态） | `multimodal-embedding-v1` 原生支持图像+文本联合嵌入，长期记忆仅支持 `image_url` 辅助解析，不提供跨模态向量能力 |
| “我需要统计过去一周所有用户对‘退款流程’的提问频次，并导出分析” | ✅ 长期记忆 | 支持按 `type=observation` + `time_range` 列表查询 + 全量导出；向量服务无数据存储与聚合能力 |
| “我已有向量数据库，只需一个稳定、低延迟的嵌入 API” | ✅ 向量与排序 | 直接调用 `/v1/embeddings`，无需管理记忆库、用户 ID、schema 等长期记忆特有概念，轻量高效 |

> **最后提醒**：  
> - 若项目涉及 **用户隐私数据**（如手机号、身份证号），请务必遵循《百炼平台数据安全规范》，长期记忆中禁止写入明文敏感字段，建议脱敏后存入 `custom_content` 或使用加密字段；  
> - 向量服务中所有文本输入按 Unicode 字符计长，超限（如 `query` > 512 字符）将直接报错 `400`，需前置截断或摘要；  
> - 生产环境务必使用 SDK 封装（如 `agentscope_runtime.tools.modelstudio_memory`）调用长期记忆，以自动处理鉴权、限流退避（429）、异步轮询等健壮性逻辑。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [vector and sort](../api/vector-and-sort.md)


