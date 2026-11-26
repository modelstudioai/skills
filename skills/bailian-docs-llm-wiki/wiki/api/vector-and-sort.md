# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/多模态向量化（embedding）与检索后重排序（rerank）两大核心能力，用于构建高精度语义搜索、RAG、跨模态检索等应用。向量模型将原始内容映射到统一语义空间，排序模型则对召回结果进行细粒度相关性打分与重排，二者常协同使用以提升端到端效果。

## 支持的模型/功能

- **文本向量模型**：支持同步（`qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-v3` 等）与异步批处理（`text-embedding-async-v2`, `text-embedding-async-v1`）两种调用模式，详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 和 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量模型**：支持文本、图像、视频及其组合的联合向量化，提供独立向量（各模态单独生成）与融合向量（多模态统一表征）两种模式，覆盖 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等系列，详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **排序（Rerank）模型**：支持纯文本（`qwen3.7-text-rerank`, `qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及兼容型（`gte-rerank-v2`）三类，其中 `gte-rerank` 模型将于 2026 年 5 月 30 日下线，[官方公告](https://www.aliyun.com/notice/118217) 明确推荐迁移至 `qwen3-rerank`。

> **注意**：文档中 `text-embedding-v3` 在北京地域表格中标注“无免费额度”，但在新加坡地域表格中未明确说明；而 `text-embedding-v4` 在两地均标注“无免费额度”。实际以控制台或最新计费页为准，建议通过 [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md) 文档确认当前地域的免费额度策略。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `dimensions` | 同步文本向量（`qwen3.7-text-embedding`, `text-embedding-v3/v4`） | 指定向量维度（如 `1024`, `2048`），默认 `1024`；`v1/v2` 及异步模型不支持该参数。 |
| `encoding_format` | 同步文本向量 | 可选 `float` 或 `base64`，但受网关限制：老网关强制返回 `float`；新网关短请求按设置返回，长请求仍回落为 `float`。 |
| `enable_fusion` | 多模态向量（`qwen3-vl-embedding`） | 设为 `true` 启用融合向量模式，将 `contents` 中所有输入（文本+图片+视频等）编码为单个向量。 |
| `instruct` | 所有 rerank 模型（`qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank`） | 自定义任务指令（如 `"Given a web search query, retrieve relevant passages..."`），显著影响排序逻辑，建议英文书写。 |
| `top_n` | 所有 rerank 模型 | 返回排序后前 N 个结果，默认返回全部；若 `N > 文档总数`，则返回全部。 |
| `fps` | `qwen3-vl-rerank`（视频输入） | 控制视频帧抽取频率（取值 `(0, 5]`，默认 `1.0`），值越小，计算开销越低。 |

## 使用方式

- **同步向量调用**：适用于实时性要求高的场景（如在线搜索）。使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope HTTP 接口，`input` 支持字符串、字符串数组或文件 URL；需注意不同模型的单行 [Token](../concepts/token.md) 上限（`qwen3.7-text-embedding`: 128k，`text-embedding-v4`: 8,192，`text-embedding-v1/v2`: 2,048）和最大行数（20 / 10 / 25）。
- **异步批处理调用**：适用于海量数据离线向量化（如知识库预处理）。通过两步完成：① `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（必须带 `X-DashScope-Async: enable` 头）；② `GET /api/v1/tasks/{task_id}` 查询结果；支持单次最多 100,000 行，每行 ≤2,048 [Token](../concepts/token.md)。
- **多模态向量调用**：HTTP endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`；`input.contents` 为对象数组，每个元素指定 `text`/`image`/`video`/`multi_images`；融合向量需使用 `qwen3-vl-embedding` 并设 `enable_fusion=true`。
- **排序模型调用**：HTTP endpoint 为 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`；`input.query` 与 `input.documents` 必填；`qwen3-vl-rerank` 的 `query` 和 `documents` 支持字典格式（如 `{"text": "xxx"}` 或 `{"image": "url"}`）以指定模态。

## 限制和注意事项

- **[Token](../concepts/token.md) 计算与上限**：  
  - 向量模型：`text-embedding-v4` 单行上限 8,192 Token，超限将报错；`qwen3.7-text-embedding` 支持 128,000 Token，但需确保服务端 tokenizer 兼容长文本。  
  - Rerank 模型：`qwen3-vl-rerank` 的“请求最大输入Token” = `Query Tokens × Document 数量 + Document Tokens 总和`，总和不可超过 120,000；单条 Query/Document 超过其对应上限（如 `qwen3-rerank` 单条 4,000 Token）将直接返回 HTTP 400 错误，**不会自动截断**。  
- **地域与模型可用性**：部分模型（如 `text-embedding-async-v1/v2`）仅在北京地域提供；`qwen3-vl-embedding` 在新加坡地域暂未列出，调用前请确认 [模型概览](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中的地域支持表。  
- **免费额度时效性**：文本向量模型的免费额度（如 100 万 Token）有效期为“百炼开通后 90 天内”，而多模态模型（如 `qwen3-vl-embedding`）为“自开通/模型发布/申请通过之日起 90 天（以较晚者为准）”，需注意起始时间差异。  
- **兼容性提示**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)仅支持同步向量与 `qwen3.7-text-rerank`/`qwen3-rerank` 排序模型，不支持异步向量或多模态 rerank；使用时需配置正确的 `base_url`（如北京地域为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


