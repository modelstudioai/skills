# vector and sort

百炼平台的 vector and sort 功能涵盖文本向量化（embedding）、多模态向量化及文本排序（rerank）三大能力，用于构建语义搜索、RAG、跨模态检索等 AI 应用。所有模型均支持同步与异步调用方式，提供 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与原生 DashScope SDK/API，开发者可根据延迟敏感度、批量规模和模态需求灵活选型。

## 支持的模型/功能

- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等系列模型，适用于语义搜索、聚类、分类等任务；[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 和 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md) 分别覆盖实时小批量与海量离线场景。
- **多模态向量**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可对文本、图像、视频进行独立向量或融合向量生成，实现跨模态语义对齐；详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：提供 `qwen3-rerank`（推荐替代已下线的 `gte-rerank`）、`qwen3.7-text-rerank` 及多模态 `qwen3-vl-rerank`，对召回结果进行高精度二次重排，显著提升 RAG 与检索系统准确率。

> **注意**：文档 6 明确指出 `gte-rerank` 模型将于 2026 年 05 月 30 日下线，且 `qwen3-rerank` 已成为主力推荐模型；而文档 7 仅列出入口链接，未更新该关键生命周期信息，应以文档 6 为准。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 所有 | 模型名称，如 `"qwen3.7-text-embedding"`、`"qwen3-rerank"`、`"qwen3-vl-embedding"` | 是 |
| `input` | 所有 | 向量/排序输入内容：文本字符串、字符串数组、文件 URL 或 `contents` 多模态对象数组 | 是 |
| `dimensions` / `dimension` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-*2026-03-06*` | 指定向量维度（如 `1024`, `2560`），不同模型支持值不同；`multimodal-embedding-v1` 和 `tongyi-embedding-vision-plus/flash`（非 2026 版本）不支持 | 否（默认值见各模型概览） |
| `encoding_format` | 同步文本向量 | 控制返回格式：`"float"`（默认）或 `"base64"`；但[老网关不支持 `base64` 输出](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) | 否 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用多模态融合向量（单输入对应单融合向量）；`qwen2.5-vl-embedding` 始终融合，不支持该参数 | 否（仅 `qwen3-vl-embedding`） |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响相关性判断逻辑 | 否（默认为问答检索） |
| `top_n` | 所有 rerank 模型 | 返回前 N 个排序结果；超出文档总数时返回全部 | 否 |
| `return_documents` | `qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2` | 是否在响应中返回原文（`true` 时含 `document.text` 字段） | 否（默认 `false`） |

## 使用方式

- **同步调用（低延迟、小批量）**：  
  - 文本向量：使用 `/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/text-embedding/text-embedding`（DashScope 原生），支持 `string`、`array<string>`、`file` 输入。  
  - 排序：使用 `/api/v1/services/rerank/text-rerank/text-rerank`，`query` 与 `documents` 均嵌套于 `input` 对象内；`qwen3-rerank` 和 `qwen3.7-text-rerank` 还支持 OpenAI 兼容 `/compatible-api/v1/reranks` 接口（参数扁平化）。  
  - 多模态向量：统一使用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，通过 `contents` 数组指定 `text`/`image`/`video`/`multi_images` 组合。

- **异步调用（大批量、长耗时）**：  
  - 文本向量批处理：使用 `text-embedding-async-v2` 模型，通过两步完成：① POST 创建任务（需 `X-DashScope-Async: enable` 头），② GET `/api/v1/tasks/{task_id}` 查询结果；任务数据保留 24 小时。  
  - SDK 封装：DashScope Python/Java SDK 提供 `client.embeddings.jobs.create()` 和 `.wait()` 方法，自动处理轮询与状态等待。

- **地域与认证**：  
  所有请求需配置 `Authorization: Bearer $DASHSCOPE_API_KEY`，并替换 `{WorkspaceId}` 与地域后缀（如 `cn-beijing`、`ap-southeast-1`）；[前提条件](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 要求已获取 API Key 并配置环境变量。

## 限制和注意事项

- **输入长度与批量限制**：  
  - `qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)，最多 20 行；`text-embedding-v4` 限 8,192 [Token](../concepts/token.md)/行、10 行；`text-embedding-async-v2` 支持单次 100,000 行、每行 ≤2,048 [Token](../concepts/token.md)。  
  - `qwen3-vl-rerank` 的 `max_document_count` 因模态而异：文本 100、图片 40、视频 4；`qwen3-rerank` 支持最多 500 文档。  
  - 多模态向量中，`qwen3-vl-embedding` 单次 `contents` 总数 ≤20（图片≤10，视频≤1），而 `tongyi-embedding-vision-plus-2026-03-06` 支持图片≤64、视频≤8。

- **免费额度与计费**：  
  - 北京地域 `qwen3.7-text-embedding`、`text-embedding-v4` 等享有 100 万 Token 免费额度（开通后 90 天有效），但新加坡地域同名模型无免费额度；`text-embedding-async-v2` 提供 2000 万 Token 免费额度。  
  - 多模态向量按模态分别计费（如 `qwen3-vl-embedding`：文本 0.0007 元/千 Token，图片/视频 0.0018 元/千 Token）。

- **兼容性与网关行为**：  
  > **注意**：`encoding_format="base64"` 在老网关下被忽略，始终返回 `float`；新网关仅对短请求生效，长请求仍路由至老网关。此行为差异在 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中明确说明，开发者需根据实际请求长度预判返回格式。  
  - `gte-rerank-v2` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，调用将返回 `model_not_supported` 错误；`qwen3-vl-rerank` 仅支持 DashScope 原生 HTTP 接口，不支持 OpenAI 兼容模式。  
  - `multimodal-embedding-v1` 不支持 `dimension` 参数，固定输出 1024 维向量；`tongyi-embedding-vision-plus`（非 2026 版）同样不支持该参数。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


