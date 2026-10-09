# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索、聚类与分类等典型AI应用。所有能力均通过标准化API提供，支持同步/异步调用、OpenAI兼容接口及DashScope SDK封装，适用于从单条实时推理到百万级批量处理的全场景需求。

## 支持的模型与功能

### 文本向量化
- **同步模型**：`qwen3.7-text-embedding`（2560维可选）、`text-embedding-v4`（2048维）、`qwen3.7-text-embedding-flash`（1024维默认）等，支持中、英、日、韩等201种语种，单次最多处理20条文本（`qwen3.7-text-embedding`）或10条（`text-embedding-v4`），单条最长128,000 [Token](../concepts/token.md) [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理模型**：`text-embedding-async-v2`（1536维）、`text-embedding-async-v1`，专为超大规模文本（单次100,000行）设计，需通过任务ID轮询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量化
支持文本、图像、视频统一语义空间表征，提供**独立向量**（每模态各1个向量）与**融合向量**（多模态输入合成1个向量）两种模式：
- `qwen3-vl-embedding`：支持融合（`enable_fusion=true`）与独立向量，2560维可调，支持33+语言、多图+视频混合输入；
- `tongyi-embedding-vision-plus-2026-03-06`：Qwen3底座新版，支持`res_level`与`max_video_frames`参数，同时支持独立/融合向量；
- `qwen2.5-vl-embedding`：仅支持融合向量，不支持多图 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
对召回结果进行二次精准重排：
- `qwen3-rerank`：OpenAI兼容接口，轻量高效，单次最多500文档，单文档最大4,000 [Token](../concepts/token.md)；
- `qwen3.7-text-rerank`：高精度文本排序，支持`instruct`指令微调排序策略（如问答检索 vs 语义相似度）；
- `qwen3-vl-rerank`：支持文本/图像/视频混合查询与文档，跨模态排序；
- **注意**：`gte-rerank`系列模型将于2026年05月30日下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档明确推荐迁移至`qwen3-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度（如1024、1536、2560），部分模型（如`multimodal-embedding-v1`）固定维度不可调。 |
| `text_type` | 异步批处理模型（`text-embedding-async-*`） | 取值`document`（默认，用于底库）或`query`（用于检索查询），影响向量空间对齐效果。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true`时启用融合向量；其他模型（如`tongyi-embedding-vision-plus-2026-03-06`）通过将text/image/video置于同一content对象实现融合，**无需此参数**。> **注意**：文档5中对`tongyi-embedding-vision-plus-2026-03-06`的融合机制描述与`enable_fusion`参数存在逻辑冲突，实际应以“同content对象”为准。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如`"Retrieve semantically similar text."`），显著影响排序逻辑。 |
| `top_n` | 所有Rerank模型 | 返回前N个结果，默认返回全部。 |

## 使用方式

### 同步调用（推荐小批量/低延迟场景）
- **OpenAI兼容接口**：使用`base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`，调用`/embeddings`或`/reranks`端点，参数结构与OpenAI完全一致。
- **DashScope原生SDK**：Python示例：`dashscope.TextEmbedding.call(model="qwen3.7-text-embedding", input=["hello", "world"])`。

### 异步批处理（推荐超大批量场景）
- 仅限`text-embedding-async-*`模型，必须设置请求头`X-DashScope-Async: enable`。
- 分两步：① `POST /text-embedding` 创建任务获取`task_id`；② `GET /tasks/{task_id}` 轮询结果（有效期24小时）[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态与排序调用
- **多模态向量**：HTTP请求体`input.contents`为数组，每个元素为`{"text": "..."}, {"image": "..."}, {"video": "..."}`或`{"multi_images": [...]}`。
- **Rerank**：`qwen3-rerank`使用兼容接口（`/compatible-api/v1/reranks`），`query`与`documents`与`model`同级；其余模型使用`/api/v1/services/rerank/...`，需嵌套在`input`对象内。

## 限制和注意事项

- **[Token](../concepts/token.md)与尺寸限制**：  
  - 同步文本向量：`text-embedding-v4`单行限8,192 Token，`qwen3.7-text-embedding`单行限128,000 Token；  
  - 多模态：`qwen3-vl-embedding`图片单张≤10 MB，视频≤50 MB；  
  - Rerank：`qwen3-vl-rerank`单次最多40张图片或4个视频，总输入Token上限120,000。

- **地域与Endpoint差异**：  
  - 北京地域：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；  
  - 新加坡地域：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；  
  - 多模态通用接口（非地域绑定）：`dashscope.aliyuncs.com/api/v1/...`。

- **免费额度与限流**：  
  - 同步模型免费额度按开通后90天计（如`qwen3.7-text-embedding`各100万Token）；  
  - 异步批处理：单用户并发运行中任务≤3个，排队中+运行中总数≤50个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

- **编码与格式**：  
  - `encoding_format`（`float`/`base64`）在长请求时可能被老网关强制转为`float`，不保证`base64`输出；  
  - 图片Base64需符合`data:image/{format};base64,{data}`格式，视频URL必须公开可访问。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


