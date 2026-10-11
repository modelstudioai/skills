# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将大语言模型（LLM）的生成能力与外部知识源的精准检索能力相结合的技术范式。它通过在模型推理前动态检索相关知识片段，并将其作为上下文注入提示（[prompt](../guides/prompt.md)），显著提升回答的事实准确性、领域专业性和可追溯性，同时降低幻觉风险。

## 在百炼平台的不同场景中，这个概念如何使用

在百炼平台，RAG 不是单一功能模块，而是贯穿数据接入、检索服务、模型生成与应用集成的端到端能力体系：

- **知识库即服务（KBaaS）**：百炼知识库是 RAG 的核心基础设施，支持 PDF/Word/TXT/Excel/图片/音视频等多模态数据的自动解析、语义切片、向量化与混合检索（关键词 + 向量）。开发者无需自建向量数据库，即可获得开箱即用的私有知识托管与检索能力。

- **RAG API 直接调用**：通过 `/v1/knowledge/query` 接口，开发者可将用户问题与指定知识库 ID 传入，平台自动完成检索 → 重排 → 调用绑定的 Qwen 系列模型（如 `qwen3.5-plus`）生成带引用的答案，返回结构化响应（`answer` + `references`），适用于需精细控制链路的定制化场景。

- **智能体（Agent）增强**：在百炼智能体应用中，RAG 以“知识技能”形式嵌入 Agent 工作流。配置为“必定调用”后，每轮对话均自动触发知识检索，实现多轮上下文感知的问答；支持与工具调用历史联动，构建 Agentic RAG（如先查政策再生成合同条款）。

- **低代码应用集成**：通过 AppFlow 可视化编排，RAG 能力可一键注入网站悬浮窗、微信公众号、企业微信、钉钉机器人等渠道。无需写代码，即可让业务系统具备基于私有文档的智能客服、FAQ 自助查询等能力。

- **框架级深度集成**：对开发者友好，百炼原生支持 LlamaIndex（`DashScopeCloudIndex`/`DashScopeCloudRetriever`）和 Spring AI Alibaba，允许在标准框架内调用百炼的嵌入模型（`text-embedding-v4`）、重排模型（`qwen3-rerank`）及云端知识库，实现从本地开发到云上部署的平滑迁移。

## 关键参数和配置

以下参数直接影响 RAG 效果，建议根据业务需求合理设置：

| 参数 | 所属层级 | 说明 | 推荐值 | 注意事项 |
|------|----------|------|--------|----------|
| `top_k` | 检索层 | 返回最相关切片数量 | 3–10（问答）；20–50（调试/分析） | API 默认 3，最大 50；知识库独立配置最大召回为 100，但最终返回上限为 20 |
| `similarity_threshold` | 检索层 | 过滤低分切片的相似度阈值 | 0.3–0.6（平衡精度与召回） | 值过高易漏召，过低引入噪声；仅对向量检索生效 |
| `enable_hybrid_search` | 检索层 | 是否启用关键词+向量混合检索 | `true`（默认，强烈推荐） | 纯向量检索对术语、缩写、数字敏感，混合模式显著提升鲁棒性 |
| `rerank_model_name` | 重排层 | 重排模型名称 | `qwen3-rerank`（文本）、`qwen3-vl-rerank`（多模态） | 重排在检索后执行，可大幅提升 Top-K 结果的相关性排序质量 |
| `chunk_max_length` | 数据层 | 切片最大 token 长度 | 512–1024（兼顾信息密度与上下文窗口） | 创建知识库时设定，不可更改；默认 600，过长影响语义聚焦，过短割裂逻辑 |
| `temperature` | 生成层 | 控制模型输出随机性 | 0.1–0.3（客服/知识问答场景） | 低值确保答案稳定、忠实于检索内容，避免过度发挥 |

> ⚠️ **重要限制提醒**：  
> - 所有 RAG 请求必须在 **华北2（北京）地域**（中国站）或 **新加坡地域**（国际站）调用，跨地域请求将失败；  
> - 单次 `query` 长度 ≤ 2048 字符，超长将被截断并返回 `400`；  
> - 知识库单文档大小上限：PDF/Word ≤ 100 MB，其他格式 ≤ 50 MB；  
> - 免费试用额度下，每知识库每分钟最多 60 次 `/query` 调用。

## 面向开发者，简洁实用

- **快速验证**：直接使用控制台 [Playground](https://bailian.console.aliyun.com/?tab=app#/playground) 选择知识库输入问题，实时查看检索切片与生成答案，5 分钟完成效果验证。
- **最小可行集成**：
  ```bash
  # 1. 认证（环境变量）
  export DASHSCOPE_API_KEY="sk-xxx"
  
  # 2. 发起 RAG 查询（curl 示例）
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/knowledge/query" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "knowledge_base_id": "kb-xxx",
          "query": "我们的SaaS产品支持单点登录吗？",
          "top_k": 5,
          "enable_hybrid_search": true
        }'
  ```
- **生产优化建议**：
  - 对关键业务文档，启用 **标签过滤**（`tags`）缩小检索范围，提升精度与速度；
  - 多知识库场景，优先使用 `/api/v1/indices/knowledge/search`（联合检索接口），由平台自动路由与混排；
  - 需要高并发检索时，按需配置 **RCU（Retrieval Compute Unit）** 规格（1 RCU ≈ 50 QPS），避免限流；
  - 流式响应（`stream=true`）适用于 Web 前端逐字渲染，注意处理 SSE 格式。

RAG 是百炼平台“私有知识 × 大模型”的核心纽带。善用其托管能力，你只需关注业务知识本身——解析、检索、重排、生成，全部交由平台保障。

## 关联主题页

- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [frameworks](../api/frameworks.md)


