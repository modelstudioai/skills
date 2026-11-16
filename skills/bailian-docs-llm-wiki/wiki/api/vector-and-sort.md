# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型AI应用链路。所有服务均支持同步与异步调用模式，并提供 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)以降低迁移成本。开发者可根据数据规模、模态类型、延迟敏感度和精度要求选择合适模型与接口。

## 支持的模型/功能

### 文本向量化
- **同步接口**：适用于低延迟、小批量场景（≤20条/请求）。主流模型包括 `qwen3.7-text-embedding`（128K Token上限）、`text-embedding-v4`（2K Token上限，Qwen3-Embedding系列）及 `text-embedding-v3` 等 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：适用于大规模离线任务（单次最多100,000行），仅支持异步，模型为 `text-embedding-async-v1/v2`，需通过文件URL提交 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量化**：支持文本、图像、视频及其组合输入，统一映射至同一语义空间。`qwen3-vl-embedding` 支持独立向量与融合向量双模式；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型支持 `res_level` 和 `max_video_frames` 等精细控制参数 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- **文本排序**：`qwen3-rerank`（推荐替代已下线的 `gte-rerank`）和 `qwen3.7-text-rerank` 支持高精度语义重排，最大500文档/请求；`gte-rerank-v2` 仍可用但不推荐新项目使用。
- **多模态排序**：`qwen3-vl-rerank` 支持文本、图片、视频混合查询与候选，支持 `fps` 参数控制视频抽帧密度。

> **注意**：文档 7 明确指出 `gte-rerank` 模型将于2026年05月30日下线，且其 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不被支持（调用将返回 `model_not_supported` 错误），而 `qwen3-rerank` 和 `qwen3.7-text-rerank` 同时支持 DashScope HTTP 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。

## 关键参数

| 参数 | 适用模型 | 说明 |
|--------|-----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `qwen2.5-vl-embedding`, `tongyi-*` 系列 | 指定向量维度（如 `1024`, `2048`），不同模型支持值不同；`multimodal-embedding-v1` 不支持该参数，固定1024维。 |
| `encoding_format` | 同步文本向量（`text-embedding-*`） | 控制输出格式：`float`（默认）或 `base64`；但老网关强制返回 `float`，长请求亦会降级至老网关。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为单个向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 `text`/`image`/`video` 放入同一 content 对象实现融合，无需此参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响相关性打分逻辑；未指定则按默认问答检索任务执行。 |
| `text_type` | 批处理文本向量（`text-embedding-async-v1/v2`） | 区分 `query`（查询文本）与 `document`（底库文本），对非对称检索任务可提升效果。 |

## 使用方式

### 调用路径选择
- **小批量实时向量生成**（<20条，<128K Token）：优先使用同步接口，支持 OpenAI SDK 或原生 DashScope SDK。
- **超大批量离线向量生成**（>1000条）：必须使用批处理接口（异步），输入为公开可访问的文本文件 URL。
- **多模态内容处理**：统一使用 `/multimodal-embedding` HTTP endpoint，通过 `contents` 数组声明输入模态。
- **召回后精排**：使用 `/rerank` 接口，`query` 与 `documents` 必须同构（均为文本，或均为多模态对象）。

### 地域与Endpoint
- 北京地域 base URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`
- 新加坡地域 base URL：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`
- OpenAI 兼容接口需显式配置 `base_url`（如 `compatible-mode/v1`），且仅限部分模型支持 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

## 限制和注意事项

- **Token 与长度限制严格**：`text-embedding-v4` 单行上限为 8,192 Token，超出直接报错（HTTP 400），**不会自动截断**；`qwen3.7-text-embedding` 单行支持 128,000 Token，但批处理接口（`text-embedding-async-v2`）单行仅限 2,048 Token。
- **异步任务生命周期**：批处理任务结果 URL 有效期仅 **24 小时**，需及时下载；同时运行中任务数上限为 3 个，排队中+运行中总数不超过 50 个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **免费额度时效性**：多数模型（如 `qwen3.7-text-embedding`）免费额度为“百炼开通后90天内”，而 `qwen3-vl-embedding` 为“自开通/模型发布/申请通过之日起90天（以较晚者为准）”，起算点不一致，需注意 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **模型能力差异**：`qwen2.5-vl-embedding` 仅支持融合向量，**不支持独立向量或多图输入**；`tongyi-embedding-vision-plus` 旧版仅支持 8 张图，而 `2026-03-06` 快照版支持最多 64 张。
- **Rerank 输入计算规则**：总 Token 数 = `Query Tokens × Document 数量 + 所有 Document Tokens 总和`，该值不得超过模型规定的“请求最大输入Token”（如 `qwen3-rerank` 为 120,000），否则请求失败。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


