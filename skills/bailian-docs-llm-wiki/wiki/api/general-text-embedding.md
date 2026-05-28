# general text embedding

通用文本向量模型（Text Embedding）可将非结构化文本转换为高维稠密向量，广泛应用于语义检索、推荐系统、文本聚类与分类等下游任务。平台提供同步与异步（批处理）两种调用模式，开发者可根据数据规模、实时性要求及现有代码基线灵活选择。所有接口调用均需基于标准鉴权与 `[[api-key-configuration]]` 进行环境初始化。

## 支持的模型/功能
- **同步模型**：`text-embedding-v4`（基于 Qwen3-Embedding）、`v3`、`v2`、`v1`。v4 支持 100+ 主流语种及编程语言，v3 支持 50+ 语种。
- **异步模型**：`text-embedding-async-v2`、`text-embedding-async-v1`。底层采用任务队列与轮询机制，专为超大规模离线数据设计。
- **检索优化**：异步接口支持 `text_type` 参数（`query`/`document`），在非对称检索场景下区分查询词与底库文本可显著提升召回精度；聚类/分类等对称任务使用默认 `document` 即可。
- **生态兼容**：同步接口全面对齐 `[[openai-compatible-mode]]` 规范，便于存量项目快速迁移。

## 关键参数
| 参数 | 说明 | 适用范围 |
|:---|:---|:---|
| `model` | 指定调用的模型版本名称 | 全部 |
| `input` | 待处理文本。同步支持 `String`/`Array`/`File`；异步仅支持文本文件的公网 HTTP URL | 全部 |
| `dimensions` | 指定输出向量维度。v4 支持 2048/1536，v3/v4 默认 1024，最低 64 | 仅同步 v3/v4 |
| `text_type` | 向量用途，`query` 或 `document`（默认） | 仅异步接口 |
| `encoding_format` | 返回编码格式，当前仅支持 `float` | 同步接口 |

## 使用方式
### 1. 同步调用（推荐）
面向低延迟场景。请求需发往兼容模式 Endpoint：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings`。直接传入文本及可选的 `dimensions`，即可同步返回向量数组。完整请求体结构、多语言（Python/Java/curl）示例及响应字段解析，请参阅 [同步接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-synchronous-api.md)。

### 2. 异步批处理调用
面向高吞吐场景。HTTP 调用**必须**在 Header 中添加 `X-DashScope-Async: enable`，采用两阶段工作流：
1. **创建任务**：POST 提交包含 `model`、`input.url` 的 JSON 体，获取 `task_id`。
2. **查询结果**：GET 请求 `https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 轮询状态。任务成功后响应中将返回包含嵌入向量的下载链接。详细的状态枚举、SDK `wait()` 封装逻辑及错误排查指引见 [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)。生产环境建议结合 `[[dashscope-sdk]]` 使用，可免去手动轮询。

## 限制和注意事项
- **限流策略**：同步请求受全局 RPM/RPS 约束。异步接口任务下发限流为 1 RPS，排队与运行中任务总数上限 50 个，且任意时刻**最大并发数仅 3 个**，超额请求将进入队列排队。具体阈值参考 `[[rate-limits]]`。
- **Token 与行数限制**：同步接口 `v3/v4` 单行上限 8,192 Token，单次最多 10 行；`v2/v1` 单行上限 2,048 Token，单次最多 25 行。异步接口统一限制单行 2,048 Token，单次上限 100,000 行（文件 ≤ 200MB）。
- **结果有效期**：异步任务返回的输出 URL 仅保留 **24 小时**，超时后自动清除。业务侧需在 `SUCCEEDED` 状态回调或轮询成功后立即持久化向量数据。生命周期说明详见 [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)。

> **注意**：同步与异步接口为独立端点，不可混用。若在同步 `/compatible-mode/v1/embeddings` 端点误传 `X-DashScope-Async: enable` 头，或服务端配置未开启同步通道，将直接报错 `current user api does not [[support|support]] synchronous calls`。请严格按业务场景区分调用路径。
> 
> **注意**：不同模型的免费额度与单价存在差异。例如 `text-embedding-v4` 同步单价为 0.0005 元/千 Token，`async-v2` 为 0.0007 元/千 Token。免费额度有效期均为百炼开通后 90 天，具体配额与计费规则请以 `[[billing-rules]]` 实时账单为准。

## 来源文档

- [批处理接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-batch-api.md)
- [同步接口API详情](../../raw/model-api-reference/general-text-embedding/text-embedding-synchronous-api.md)

