# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索、聚类等典型AI应用。所有能力均通过统一API框架提供同步/异步调用支持，并兼容OpenAI生态，便于快速集成与迁移。

## 支持的模型与功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等主流模型，适用于低延迟、小批量场景（如实时检索）。详情见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2`（推荐）和 `text-embedding-async-v1`，专为超大批量（最高10万行/请求）设计，采用[异步任务](../concepts/asynchronous-task.md)模式，适合离线预处理。详情见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量模型
支持文本、图像、视频统一语义空间表征，提供两种向量生成模式：
- **独立向量**：为每个输入（text/image/video/multi_images）生成独立向量，适用于以图搜图、以文搜图等逐项匹配场景；
- **融合向量**：将多种模态输入融合为单个向量，适用于商品图文联合表征等整体理解场景。`qwen3-vl-embedding` 通过 `enable_fusion=true` 开启；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型则通过将 text/image/video 放入同一 content 对象实现。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
用于对召回结果进行精准重排序，显著提升Top-K相关性：
- `qwen3.7-text-rerank` 和 `qwen3-rerank`：纯文本排序，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)；
- `qwen3-vl-rerank`：支持文本、图像、视频混合查询与文档排序；
- `gte-rerank-v2`：轻量级文本排序模型（**注意**：`gte-rerank` 系列将于2026年05月30日下线，[官方公告](https://www.aliyun.com/notice/118217) 明确要求迁移到 `qwen3-rerank`）。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|------|----------|------|--------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `qwen2.5-vl-embedding`, `tongyi-*` 系列 | 指定向量维度（非所有模型均支持）。不同模型支持的取值范围不同，需严格对照文档。 | `1024`, `2048`, `2560` |
| `encoding_format` | 同步文本向量（`text-embedding-*`） | 控制返回格式：`float`（默认）或 `base64`。**注意**：老网关强制返回 `float`，长请求也自动降级为老网关，实际不支持 `base64` 输出。详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 | `"float"`, `"base64"` |
| `text_type` | 批处理文本向量（`text-embedding-async-v*`） | 区分查询文本（`query`）与底库文本（`document`），对检索类任务可提升精度。默认 `document`。 | `"query"`, `"document"` |
| `enable_fusion` | `qwen3-vl-embedding` | `bool` 类型，启用后将 `contents` 中所有输入融合为单个向量。其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过结构化输入实现融合，**不使用此参数**。 | `true`, `false` |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令，影响模型对“相关性”的判定逻辑（如问答检索 vs 语义相似度）。建议使用英文。 | `"Given a web search query, retrieve relevant passages that answer the query."` |

## 使用方式

### 调用路径选择
- **小批量（≤20条文本）+ 低延迟** → 同步文本向量 API（`/compatible-mode/v1/embeddings`）；
- **超大批量（>20条，最高10万行）+ 可接受异步** → 批处理文本向量 API（`/api/v1/services/embeddings/text-embedding/text-embedding`）；
- **含图片/视频的多模态输入** → 多模态向量 API（`/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`）；
- **对召回结果二次精排** → Rerank API（`/api/v1/services/rerank/text-rerank/text-rerank` 或 OpenAI 兼容 `/compatible-api/v1/reranks`）。

### 地域与Endpoint
- **北京地域**（默认）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`
- **新加坡地域**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`
- **全局服务（DashScope）**：`https://dashscope.aliyuncs.com/api/v1/...`（仅多模态向量和部分Rerank模型支持）
> `{WorkspaceId}` 必须替换为真实业务空间ID，详见 [Base URL 总览](raw/model-api-reference/preparations/base-url.md)。

### SDK与CLI示例
- **OpenAI SDK（同步向量）**：配置 `base_url` 为兼容模式地址，调用 `client.embeddings.create()`；
- **DashScope SDK（批处理）**：使用 `client.embeddings.jobs.create()` 提交[异步任务](../concepts/asynchronous-task.md)，再调用 `.wait()` 或 `.fetch()` 查询结果；
- **dashscope CLI**：`dashscope embeddings create -m text-embedding-v3 -i "hello"` 或 `dashscope rerank create -m qwen3-rerank -q "query" -d "doc1" -d "doc2"`。

## 限制与注意事项

- **[Token](../concepts/token.md) 限制差异大**：`qwen3.7-text-embedding` 单行支持 128,000 [Token](../concepts/token.md)，而 `text-embedding-v4` 仅支持 8,192 [Token](../concepts/token.md)，`multimodal-embedding-v1` 文本仅限 512 Token。务必按模型文档核对上限，超限将直接返回 HTTP 400 错误。
- **免费额度时效性**：多数模型（如 `qwen3.7-text-embedding`）的 100 万 Token 免费额度**有效期为百炼开通后90天内**，过期作废；而 `qwen3-vl-embedding` 的免费额度有效期为“自开通/模型发布/申请通过之日起90天（以较晚者为准）”，二者逻辑不一致，需特别关注。
- **[异步任务](../concepts/asynchronous-task.md)生命周期**：批处理任务（`text-embedding-async-*`）的 `task_id` 仅保留 **24 小时**，结果 URL 也仅在此期限内有效，务必及时下载。
- **模型能力冲突**：文档中明确指出 `qwen2.5-vl-embedding` **仅支持融合向量，不支持独立向量**；而 `tongyi-embedding-vision-plus` **仅支持独立向量，不支持融合向量**。若错误混用 `enable_fusion` 参数或输入结构，将导致行为异常或报错。
- **OpenAI 兼容性边界**：`gte-rerank-v2` 和 `qwen3-vl-rerank` **不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，调用 `/compatible-api/v1/reranks` 会返回 `model_not_supported` 错误，必须使用 DashScope 原生 HTTP 接口。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


