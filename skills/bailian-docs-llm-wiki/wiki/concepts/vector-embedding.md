# 向量嵌入

向量嵌入（Vector Embedding）是将原始非结构化数据（如文本、图像、视频等）映射到高维连续语义空间中的固定长度稠密向量的过程。该向量能表征输入内容的语义本质，使得语义相似的内容在向量空间中距离更近，从而支撑检索、聚类、去重、RAG 等下游任务。

## 在百炼平台的不同场景中如何使用

- **RAG（知识库检索）**：知识库创建或文档导入时，平台自动调用指定嵌入模型（如 `text-embedding-v4` 或 `qwen3.7-text-embedding`）对文档切片进行向量化，并构建向量索引；后续用户查询时，先将问题转为向量，在索引中执行近似最近邻（ANN）搜索召回候选切片。
- **语义搜索与跨模态检索**：通过 `vector and sort` 功能，可独立调用文本或多模态嵌入模型（如 `qwen3-vl-embedding`），支持文本→图像、图像→文本、图文混合→统一向量等多种输入组合；启用 `enable_fusion=true` 可生成融合向量，实现跨模态语义对齐。
- **Agent 与记忆库（Memory Library）**：Agent 执行记忆检索（`memory.search`）时，底层调用嵌入模型将用户指令或上下文编码为向量；记忆库 Pro/Lite 版本差异直接影响嵌入后是否触发 Rerank 精排，进而影响召回质量与 [Token](token.md) 消耗。
- **框架集成（LlamaIndex / Spring AI Alibaba）**：开发者可通过 `EmbeddingClient` 接口直接调用百炼嵌入服务，无需手动封装 HTTP 请求；框架自动处理 `api_key`、`model` 和 endpoint 配置，与原生 API 行为一致。
- **异步批量预处理**：对海量文档（如百万级 PDF/网页），可使用 `text-embedding-async-v2` 等异步接口提交批处理任务，单次最多支持 100,000 行，每行 ≤2,048 [Token](token.md)，适用于知识库初始化或定期更新。

## 关键参数和配置

| 参数 | 适用模型/场景 | 说明 | 默认值 | 注意事项 |
|------|----------------|------|--------|----------|
| `dimensions` | 同步文本嵌入（`qwen3.7-text-embedding`, `text-embedding-v3/v4`） | 指定向量维度（如 `512`, `1024`, `2048`） | `1024` | `v1/v2` 及异步模型不支持；维度越高，表征能力越强，但存储与计算开销增大 |
| `encoding_format` | 同步文本嵌入 | 返回格式：`float`（原始浮点数组）或 `base64`（Base64 编码字符串） | `float` | 新网关短请求按设置返回；长请求或老网关强制回落为 `float` |
| `enable_fusion` | 多模态嵌入（`qwen3-vl-embedding`） | 是否将文本、图像、视频等多模态输入融合为单个向量 | `false` | 设为 `true` 时，`input.contents` 中所有模态被联合编码；设为 `false` 则返回各模态独立向量 |
| `input` | 所有嵌入接口 | 输入内容：支持字符串、字符串数组、文件 URL（如 `https://xxx.png`）或 `contents` 对象数组（多模态） | — | 文本嵌入单行 [Token](token.md) 上限因模型而异（`qwen3.7-text-embedding`: 128k；`text-embedding-v4`: 8,192） |

> ⚠️ 提示：  
> - 免费额度策略按地域和模型独立配置（如 `text-embedding-v4` 在北京/新加坡均无免费额度），请以控制台最新计费页为准；  
> - 向量维度变更不影响已有索引，但新嵌入必须与索引维度一致，否则检索失败；  
> - 多模态嵌入需确保输入文件 URL 可公开访问且有效期 ≥10 分钟（推荐使用 OSS 直传 URL）。

## 面向开发者：简洁实用建议

- ✅ **选型优先级**：实时 RAG 场景用 `qwen3.7-text-embedding`（高精度+低延迟）；海量离线处理用 `text-embedding-async-v2`；跨模态需求首选 `qwen3-vl-embedding` + `enable_fusion=true`。  
- ✅ **性能优化**：对长文本，建议预切分（如按段落/句子）再向量化，避免超 Token 限制；多模态输入避免混入无关模态（如空 `image` 字段），减少冗余计算。  
- ✅ **成本控制**：`TopK`（初步召回数）直接影响 Rerank 的 Token 消耗，建议从 `20–50` 起调优；异步任务可结合事件总线回调替代轮询，降低 QPS 压力。  
- ✅ **调试技巧**：使用 `curl` 或 Postman 测试时，先用小样本（单字符串/单图）验证 `200 OK` 和向量长度；生产环境务必显式指定 `model` 和 `dimensions`，避免依赖默认值导致行为漂移。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [agent billing](../guides/agent-billing.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)
- [model production](../api/model-production.md)


