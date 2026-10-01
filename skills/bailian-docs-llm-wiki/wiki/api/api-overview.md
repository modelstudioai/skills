# api [overview](../guides/overview.md)

ParseX API 提供文档、图片及音视频的结构化解析与字段抽取能力，采用异步任务模型。所有接口均需通过 API Key 鉴权，调用流程统一为：提交任务 → 获取 `biz_id` → 轮询查询结果。本概览整合核心能力、参数规范、调用路径及关键约束，适用于快速集成。

## 支持的模型/功能

ParseX API 当前提供两类核心能力：

- **文档解析（Document Parsing）**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）、音视频（MP4/MOV/MP3/WAV）等格式，输出结构化布局（`layouts`）、Markdown 内容、分片段落（`segments`）、剧情摘要（`synopsis_summary`）等。音视频支持人声分离（diarization）、抽帧、ASR 与多模态描述生成。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。

- **字段抽取（Field Extraction）**：基于用户提供的 JSON Schema，从已解析文档或原始文件中抽取结构化字段，支持引用定位（`citations`）、推断开关（`allow_inference`）及置信状态标记（`found`/`miss`/`inferred`）。> **注意**：抽取不支持直接输入音视频；复用解析结果时，该结果必须在 7 天保留期内且类型匹配，否则返回 `ParseResultNotReusable` 错误 —— 具体限制见 [错误码](../../raw/application-api-reference/api-overview/errors.md) 中的抽取错误章节。

两类能力均支持配置复用（`config_id`）与内联配置（`processing`），且内联配置优先级高于配置 ID。

## 关键参数

所有请求共用鉴权头 `Authorization: Bearer $DASHSCOPE_API_KEY`。各接口关键参数如下：

- **通用必填**：`biz_id`（用于 `/parse/result` 和 `/extract/result`）；`file_url` 或 `parsed_file_biz_id`（二选一，用于 `/parse/submit` 和 `/extract/submit`）。

- **解析任务提交**（`/parse/submit`）：
  - `file_url` + `file_name`（或 `file_name_extension`）为文件元信息基础组合；
  - `processing.doc_processing_config` 控制文档解析行为（如 `page_index`、`layout_position`）；
  - `processing.media_processing_config` 控制音视频解析行为（如 `enable_diarization`、`frame_extraction.mode`）；
  - `output.output_file_format` 支持 `["markdown"]`，`layout_table_format` 可选 `markdown` 或 `html`。

- **抽取任务提交**（`/extract/submit`）：
  - `processing.extract_processing_config.extract_schema` 为必需 JSON 对象（非字符串），定义待抽取字段结构；
  - `citation_required` 默认 `true`，控制是否返回引用坐标与原文；
  - `allow_inference` 默认 `false`，开启后可能返回 `inferred` 状态字段。

> **注意**：文档 7 中示例代码将 `extract_schema` 写作字符串并提示“需转义”，但实际 API 接收的是原生 JSON 对象（见返回示例中 `extract_result_json` 的结构），该处为文档表述歧义，应以 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 的实际请求体结构为准。

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），推荐通过环境变量配置，避免硬编码。详见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。

2. **异步调用流程**：
   - 解析场景：`POST /parse/submit` → 获取 `biz_id` → 循环 `POST /parse/result?biz_id=...` 直至 `data.status` 为 `success` 或 `failed`；
   - 抽取场景：`POST /extract/submit` → 获取 `biz_id` → 循环 `POST /extract/result?biz_id=...` 直至完成。

3. **轮询建议**：
   - 初始间隔 ≥1s，随进度线性增长（如 1s → 2s → 5s）；
   - 收到 `ResultNotReady`（HTTP 409）时必须重试；收到 `ProcessingFailed` 等 5xx 错误时建议退避后重试。

4. **OSS 输出**：可通过 `output.oss_config` 或 `oss_config` 参数指定客户 OSS 存储，需提供 `bucket`、`endpoint` 及临时凭证（`access_key_id`/`access_key_secret`/`security_token`）。

## 限制和注意事项

- **文件限制**：
  - 单文件大小上限为 100 MB（`FileSizeExceeded`）；
  - 文档页数上限为 1000 页（`PageCountExceeded`）；
  - 音视频时长上限为 2 小时（超时触发 `ProcessingTimeout`）。

- **生命周期**：
  - 解析结果保留 30 天（`ParseResultExpired`）；
  - 抽取任务复用的解析结果仅保留 7 天（`ParseResultNotReusable`）。

- **错误处理**：
  - 所有错误响应含 `request_id`、`code`、`message`，用于问题定位；
  - `FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试（需修复 URL 或权限）；
  - 服务配额耗尽时返回 `ServiceQuotaExhausted`（HTTP 503），需检查控制台配额。

- **安全实践**：
  - API Key 须保密，禁止提交至代码仓库或前端；
  - 建议按应用分配独立 Key，便于审计与撤销；
  - 定期轮转 Key，降低泄露风险。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


