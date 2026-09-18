# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索、聚类与分类等典型AI应用。所有能力均通过标准化API提供，支持同步/异步调用、OpenAI兼容模式及SDK封装，适用于从单条实时推理到百万级批量处理的全场景需求。

## 支持的模型与功能

### 文本向量化
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等模型，适用于低延迟、小批量场景（如实时检索）。详情见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2`（推荐）和 `text-embedding-async-v1`，专为超大批量（单次最多 100,000 行）设计，采用异步任务模式，适合离线预处理。详情见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量化**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可对文本、图像、视频及其组合生成统一语义空间的向量，支持独立向量与融合向量两种模式。详情见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- **文本排序**：`qwen3-rerank`（主力推荐）、`qwen3.7-text-rerank`、`gte-rerank-v2`；`gte-rerank` 系列将于 2026年05月30日下线，[请尽快迁移](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **多模态排序**：`qwen3-vl-rerank`，支持文本、图片、视频混合查询与文档排序，适用于跨模态检索场景。

> **注意**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-api/v1/reranks`），而 `qwen3.7-text-rerank`、`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用原生接口（`/api/v1/services/rerank/...`），二者请求体结构、参数层级和响应格式不兼容，不可混用。

## 关键参数

| 参数 | 适用模型 | 说明 |
|--------|-----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度（如 `1024`, `2048`），部分模型（如 `text-embedding-v2`, `multimodal-embedding-v1`）不支持该参数，固定维度。 |
| `encoding_format` | 同步文本向量（`qwen3.7-text-embedding` 等） | 控制返回格式：`float`（默认）或 `base64`；但[老网关不支持 `base64` 输出](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)，长请求亦会降级至老网关。 |
| `enable_fusion` | `qwen3-vl-embedding` | `bool`，启用后将 `contents` 中所有输入融合为单个向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 `text`/`image`/`video` 放入同一 content 对象实现融合，无需此参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响排序策略，建议使用英文。 |
| `top_n` | 所有 Rerank 模型 | 返回前 N 个结果，默认返回全部；仅在 `parameters` 对象内（`qwen3.7-text-rerank`/`qwen3-vl-rerank`/`gte-rerank-v2`）或顶层（`qwen3-rerank`）生效。 |

## 使用方式

### 调用路径
- **文本向量（同步）**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（推荐快速迁移）或 DashScope 原生接口。  
  - OpenAI SDK 示例：`client.embeddings.create(model="qwen3.7-text-embedding", input="hello")`  
  - Base URL（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **文本向量（批量）**：仅支持异步 HTTP 或 DashScope SDK。  
  - 需先创建任务（`POST /api/v1/services/embeddings/text-embedding/text-embedding`），再轮询 `GET /api/v1/tasks/{task_id}` 获取结果。  
  - 文件需托管于公网可访问 URL，单文件 ≤ 200MB，单行 ≤ 2048 Token。
- **多模态向量**：HTTP POST 到 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组中按需组合 `{"text":...}`, `{"image":...}`, `{"video":...}` 等对象。
- **排序（Rerank）**：  
  - `qwen3-rerank`：使用 `/compatible-api/v1/reranks`，`query` 和 `documents` 与 `model` 同级；  
  - 其他 Rerank 模型：使用 `/api/v1/services/rerank/text-rerank/text-rerank`，`query` 和 `documents` 必须嵌套在 `input` 对象内。

### 认证与配置
所有接口均需：
- 设置 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头；
- 配置正确的 `base_url`（含 `{WorkspaceId}` 和地域后缀，如 `cn-beijing` 或 `ap-southeast-1`）；
- 确保已安装最新版 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)（若使用 SDK）。

## 限制和注意事项

- **Token 与尺寸限制**：  
  - `qwen3.7-text-embedding` 单行最长 128,000 Token，`text-embedding-v4` 仅支持 8,192 Token；  
  - 多模态模型中，`qwen3-vl-embedding` 图片单张 ≤ 10 MB，`tongyi-embedding-vision-plus` 视频 ≤ 10 MB；  
  - `qwen3-vl-rerank` 单次最多处理 500 文档（文本）、40 图片或 4 视频，且总输入 Token ≤ 120,000。

- **地域与免费额度差异**：  
  > **注意**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，而新加坡地域同名模型无免费额度 [详见模型概览](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。计费单价也存在微小差异（如北京 `0.0005` 元 vs 新加坡 `0.000525` 元），生产环境需按实际地域确认。

- **异步任务生命周期**：  
  批处理任务 ID 有效期仅 **24 小时**，任务结果 URL 也仅保留 24 小时，务必及时下载或持久化。

- **模型弃用提醒**：  
  `gte-rerank` 系列模型已进入下线倒计时，官方明确要求迁移到 `qwen3-rerank`，请勿在新项目中引入。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


