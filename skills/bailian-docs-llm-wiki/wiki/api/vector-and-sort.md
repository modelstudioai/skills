# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型AI应用链路。所有能力均支持同步与异步调用模式，适配OpenAI兼容接口与DashScope原生SDK，并在多地（北京、新加坡等）部署以满足低延迟与合规需求。详细模型能力与参数请参考 [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)。

## 支持的模型/功能

- **文本向量（Text Embedding）**  
  - 同步模型：`qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`；其中 `qwen3.7-text-embedding` 和 `text-embedding-v4` 支持最高 2560 维与 2048 维向量，`text-embedding-v4` 属于 [Qwen3-Embedding](https://qwenlm.github.io/zh/blog/qwen3-embedding/) 系列。  
  - 异步批处理模型：`text-embedding-async-v2`（推荐）、`text-embedding-async-v1`，单次支持最多 100,000 行文本，适用于大规模底库向量化。  
  - 所有文本向量模型均支持中、英、西、法、日、韩等 50–201 种语种，具体以 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中“支持语种”列为准。

- **多模态向量（Multimodal Embedding）**  
  - 支持文本、图像、视频及多图序列输入，统一映射至同一语义空间。  
  - 模型包括：`qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（新版Qwen3底座，支持多分辨率与融合）、`tongyi-embedding-vision-flash-2026-03-06`、`tongyi-embedding-vision-plus`、`tongyi-embedding-vision-flash` 及 `multimodal-embedding-v1`。  
  > **注意**：`tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 不支持 `dimension` 参数（固定1152/768维），而 `tongyi-embedding-vision-plus-2026-03-06` 明确支持 `64/128/256/512/1024/1152` 维可选，详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

- **文本排序（Rerank）**  
  - 主力模型：`qwen3-rerank`（OpenAI兼容接口）、`qwen3.7-text-rerank`（原生接口）、`qwen3-vl-rerank`（支持图文视频混合排序）。  
  - 已弃用模型：`gte-rerank-v2` 将于 2026年05月30日下线，[官网公告](https://www.aliyun.com/notice/118217) 明确要求迁移至 `qwen3-rerank`。  
  - `qwen3-vl-rerank` 支持跨模态查询（如图搜文、图搜图），最大文档数按模态类型区分：文本 100 条、图片 40 张、视频 4 个。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `model` | 全部 | 必填。需严格匹配文档中列出的模型名称（如 `qwen3-rerank` ≠ `qwen3.7-text-rerank`），地域差异（北京/新加坡）不影响模型名，但影响计费与限流策略。 |
| `input` / `query` & `documents` | Embedding / Rerank | Embedding 的 `input` 支持 `string` / `array<string>` / `file`；Rerank 的 `query` 和 `documents` 结构因模型而异：`qwen3-rerank` 要求扁平化参数（同级），其余模型需嵌套于 `input` 对象内。 |
| `dimensions` | 文本/多模态向量 | 可选。仅部分模型支持（如 `qwen3.7-text-embedding`、`text-embedding-v4`、`qwen3-vl-embedding`），值必须为文档明确列出的维度之一；`text-embedding-v2`、`tongyi-embedding-vision-plus` 等不支持该参数。 |
| `encoding_format` | 同步Embedding | 可选，取值 `float` 或 `base64`。但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 明确指出：老网关强制返回 `float`，长请求亦路由至老网关，实际 `base64` 输出不可靠。 |
| `enable_fusion` / 融合内容结构 | 多模态向量 | `qwen3-vl-embedding` 通过 `enable_fusion=true` 开启融合；`tongyi-embedding-vision-plus-2026-03-06` 则需将 `text`/`image`/`video` 放入**同一 content 对象**（而非数组内多个对象）实现融合，二者逻辑不一致。 |
| `instruct` | Rerank | 可选。用于指定任务类型（如 `"Given a web search query..."`），仅对 `qwen3.7-text-rerank`、`qwen3-rerank`、`qwen3-vl-rerank` 生效；`gte-rerank-v2` 不支持。 |

## 使用方式

- **同步调用（Embedding/Rerank）**  
  推荐用于实时性要求高、输入规模小的场景（如单Query实时检索）。使用 OpenAI 兼容 SDK 时，需配置 `base_url` 为地域专属地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；调用 Rerank 时注意 `qwen3-rerank` 使用 `/compatible-api/v1/reranks`，其余模型使用 `/api/v1/services/rerank/...`。

- **异步批处理（Embedding）**  
  适用于百万级文档向量化。需两步：① 调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（`X-DashScope-Async: enable` 必须）；② 用返回的 `task_id` 轮询 `/api/v1/tasks/{task_id}` 获取结果。文件需托管于公网可访问 URL，单行 ≤2048 [Token](../concepts/token.md)，总行数 ≤100,000，文件大小 ≤200MB。

- **多模态输入格式**  
  - 独立向量：`contents` 数组中每个元素为单一模态（`{"text":"..."}`、`{"image":"url"}`、`{"multi_images":[...]}`）。  
  - 融合向量：`qwen3-vl-embedding` 在 `parameters` 中设 `"enable_fusion": true`；`tongyi-embedding-vision-plus-2026-03-06` 则需 `contents` 中某一项同时含 `text` + `image` 键（如 `{"text":"...", "image":"url"}`）。  

- **SDK 与 CLI**  
  DashScope SDK（Python/Java）封装了异步轮询、错误重试等逻辑；`dashscope` CLI 支持快速调试（如 `dashscope embeddings create -m text-embedding-v3 -i "hello"`）。所有示例代码中的 `{WorkspaceId}` 和地域（`cn-beijing`/`ap-southeast-1`）需按实际替换。

## 限制和注意事项

- **地域与免费额度差异**：北京地域多数模型提供免费额度（如 `qwen3.7-text-embedding` 各100万[Token](../concepts/token.md)），而新加坡地域 `qwen3.7-text-embedding` 无免费额度，且单价略高（0.000525元 vs 0.0005元）。  
- **[Token](../concepts/token.md) 计费逻辑**：文本向量按输入 Token 数计费；多模态向量中，文本与图片/视频分开计费（如 `qwen3-vl-embedding` 文本 0.0007元/千Token，图片/视频 0.0018元/千Token）。  
- **限流策略**：  
  - 同步Embedding：依赖网关限流，具体阈值见 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit#953ddcd76495l)；  
  - 异步Embedding：单用户并发运行中任务 ≤3 个，排队中+运行中总数 ≤50 个；  
  - Rerank：`qwen3-vl-rerank` 的“最大文档数”按模态类型分别限制（文本100、图片40、视频4），非全局总数。  
- **模型兼容性风险**：  
  > **注意**：`text-embedding-v1` 在文档2中列为支持语种“中文、英语、西班牙语、法语、葡萄牙语、印尼语”，但文档3的批处理模型 `text-embedding-async-v1` 未列出印尼语，存在语种覆盖不一致；生产环境建议优先选用 `text-embedding-v4` 或 `qwen3.7-text-embedding`。  
  > **注意**：文档2称 `text-embedding-v2` “最大行数25”，但文档3的异步模型 `text-embedding-async-v2` 最大行数为100,000——二者属不同调用路径，不可混用参数描述。  
- **响应数据保留期**：异步任务结果（URL）仅保留 **24小时**，需及时下载；同步接口无此限制。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


