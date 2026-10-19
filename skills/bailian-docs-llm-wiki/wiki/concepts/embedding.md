# 向量化（Embedding）

向量化（Embedding）是将原始非结构化数据（如文本、图像、视频等）映射到低维稠密实数向量空间的过程，使语义相近的数据在向量空间中距离更近。该向量表征保留了原始数据的语义结构，是检索、聚类、分类、RAG 和跨模态理解等任务的核心基础能力。

## 在百炼平台的不同场景中如何使用

- **语义检索与 RAG**：调用 `qwen3.7-text-embedding` 或 `text-embedding-v4` 对文档分块或用户查询生成文本向量，存入向量数据库后用于相似性检索；RAG 流程中通常由 `DashScopeCloudIndex` 自动完成嵌入与索引构建。
- **多模态搜索与理解**：使用 `qwen3-vl-embedding` 或 `tongyi-embedding-vision-plus-2026-03-06` 对图文混合内容（如带标题的图片、视频帧+字幕）进行联合编码，支持“以图搜文”“以文搜图”“视频片段语义定位”等跨模态任务。
- **批量知识库构建**：对百万级文档/网页/日志等非结构化数据，优先选用异步批处理模型（如 `text-embedding-async-v2`），通过上传文件 URL 提交任务，实现高吞吐、低成本向量化。
- **与排序（Rerank）协同使用**：先用向量检索召回 Top-K 候选（快而粗），再用 `qwen3-rerank` 或 `qwen3-vl-rerank` 进行精细化重排序（准而精），显著提升最终结果相关性。

## 关键参数和配置

| 参数 | 类型 | 是否必选 | 说明 |
|------|------|----------|------|
| `model` | string | 是 | 指定向量化模型名称，例如：<br>• 文本：`qwen3.7-text-embedding`、`text-embedding-v4`<br>• 多模态：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` |
| `input` | string / array<string> / object | 是 | 输入格式依模型而异：<br>• 文本向量：支持单条字符串、字符串数组（批量）、或 `file` 类型（异步）<br>• 多模态向量：必须为 `{"contents": [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": "..."}]}` 结构 |
| `dimensions` | integer | 否 | 指定输出向量维度（如 `1024`, `2048`），仅部分文本/多模态模型支持；`tongyi-embedding-vision-plus` 等模型固定维度，传入将被忽略 |
| `enable_fusion` | boolean | 否（仅 `qwen3-vl-embedding`） | 设为 `true` 时返回单一融合向量（多模态联合表征）；默认 `false` 返回各模态独立向量（便于细粒度控制） |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；仅同步短请求生效，长请求自动忽略 |

> ✅ **最佳实践建议**：  
> - 小批量（≤20 条文本）且需低延迟 → 用同步接口 + `qwen3.7-text-embedding`；  
> - 百万级文档 → 用异步批处理 + `text-embedding-async-v2`（免费额度更高）；  
> - 图文混合内容 → 优先选 `qwen3-vl-embedding` 并显式设置 `enable_fusion=true`；  
> - 输入超长风险高（如日志、长论文）→ 务必提前分块，并校验 `qwen3.7-text-embedding`（128K Token）或 `text-embedding-v4`（8K Token）的长度限制，**平台不自动截断，超限直接报 400**。

---  
*注：所有向量化服务均支持 DashScope SDK 调用（推荐）及标准 HTTP API；OpenAI 兼容模式仅适用于文本向量同步接口，需配置对应 `base_url`。*

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [use cases](../guides/use-cases.md)


