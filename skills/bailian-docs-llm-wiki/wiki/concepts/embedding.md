# 向量嵌入

向量嵌入（Embedding）是将原始非结构化数据（如文本、图像、视频）映射到低维稠密实数向量空间的过程，使语义相近的内容在向量空间中距离更近。该向量表示保留了原始内容的语义特征，是检索、聚类、去重、RAG 等 AI 应用的底层基础能力。

## 在百炼平台的不同场景中如何使用

- **知识库（Knowledge Base）**：文档切片后，由指定嵌入模型（如 `text-embedding-v4`）统一生成向量，并构建可检索的向量索引；创建知识库时选定嵌入模型，**创建后不可更改**。
- **RAG API**：在 `/knowledge/query` 等接口中，系统自动调用知识库绑定的嵌入模型对用户查询和文档切片进行向量化，支撑 `vector` 或 `hybrid` 检索模式。
- **向量与排序服务（Vector & Sort）**：提供独立的 Embedding 接口（同步/异步），支持文本、图像、视频三模态输入，可用于自建检索系统、语义聚类、相似性分析等定制场景。
- **工具链与框架（Toolkits & Frameworks）**：通过 [OpenAI 兼容接口](openai-compatible-interface.md)（如 `/compatible-mode/v1/embeddings`）调用，无缝集成 LangChain、LlamaIndex 等主流框架，无需修改 SDK 代码。
- **多模态理解与生成流程**：在图文/音视频混合处理链路中，嵌入模型（如 `qwen3-vl-embedding`）可输出独立模态向量或融合向量（启用 `enable_fusion=true`），为跨模态检索与重排提供统一表征。

## 关键参数和配置

| 参数 | 说明 | 是否必填 | 注意事项 |
|------|------|----------|-----------|
| `model` | 嵌入模型名称，必须严格匹配平台支持列表（如 `text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3-vl-embedding`） | 是 | 模型决定输入类型（纯文本/多模态）、最大长度、维度范围及是否支持融合 |
| `input` | 输入内容：支持单字符串、字符串数组、文件 URL（如 OSS 地址）；多模态输入需按 `content` 数组组织（含 `type` 和 `data` 字段） | 是 | 异步批处理接口（如 `text-embedding-async-v2`）要求 JSONL 格式，每行一个 `input` |
| `dimensions` | 指定向量维度（如 `512`、`1024`），仅部分新模型支持（`qwen3.7-text-embedding`、`text-embedding-v4`、`qwen3-vl-embedding` 等） | 否 | 默认值因模型而异（如 `text-embedding-v4` 默认 1024）；旧模型（如 `text-embedding-v2`）不支持该参数 |
| `encoding_format` | 输出格式：`float`（默认，返回浮点数数组）或 `base64`（Base64 编码的二进制向量） | 否 | 当前同步接口强制返回 `float`；长请求或老网关会自动降级为 `float`，`base64` 实际不可用 |
| `enable_fusion` | 仅 `qwen3-vl-embedding` 支持：设为 `true` 时，将文本+图像+视频输入融合为单个向量；设为 `false`（默认）则返回各模态独立向量 | 否 | 其他多模态模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过输入结构隐式控制融合行为 |

> ⚠️ 注意：  
> - 所有嵌入模型**均不支持稀疏向量输出**（传入 `output_type=sparse` 将返回空 embedding）；  
> - `text-embedding-async-v2` 的 `text_type`（`document`/`query`）仅影响下游检索策略，**不改变向量本身**；  
> - 多模态嵌入需注意模型能力边界：`qwen2.5-vl-embedding` 仅支持融合向量，`tongyi-embedding-vision-plus` 仅支持独立向量。

## 面向开发者的小贴士

- ✅ **优先选用新模型**：`qwen3.7-text-embedding`（2560 维，128K token）和 `text-embedding-v4`（64–2048 维可调）兼顾精度、灵活性与性能，推荐用于新项目。  
- ✅ **多模态场景明确输入结构**：使用 `qwen3-vl-embedding` 时，若需融合向量，务必传 `{"enable_fusion": true}` 并确保 `content` 中包含至少两种模态；否则默认返回独立向量。  
- ✅ **批量处理选异步接口**：单次 >1000 条文本向量化，请用 `text-embedding-async-v2`（支持 10 万行/请求），避免同步超时。  
- ❌ **避免维度误配**：调用 `dimensions` 参数前，务必查阅对应模型文档确认支持范围（如 `qwen3-vl-embedding` 支持 256–2560，超出将报错）。  
- 📌 **调试建议**：在 Playground 中使用 “Embedding” 工具快速验证输入格式与向量输出；生产环境请始终校验响应中的 `usage.total_tokens` 与 `data[0].embedding.length` 是否符合预期。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model data overview](../guides/model-data-overview.md)


