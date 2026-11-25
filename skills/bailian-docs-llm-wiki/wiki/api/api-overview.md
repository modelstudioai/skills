# api [overview](overview.md)

ParseX API 提供文档与音视频的结构化解析能力，以及基于 Schema 的字段抽取能力。所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 进行鉴权，适用于开发者集成到自动化流程或企业级应用中。

## 支持的模型/功能

ParseX API 当前提供两类核心能力：

- **文档解析（Document Parsing）**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）、音视频（MP4/MOV/AVI 等）等格式，输出结构化布局（`layouts`）、Markdown 内容、分段信息（`segments`）、剧情摘要（`synopsis_summary`）及帧级视觉描述等。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。
  
- **字段抽取（Field Extraction）**：支持从已解析文档（`parsed_file_biz_id`）或原始文件（`file_url`）中，按用户定义的 JSON Schema 抽取结构化字段，返回带引用定位（`citations`）和推断状态（`inferred`/`found`）的结果。**注意：抽取不支持直接输入音视频**，仅支持图文类输入；复用解析结果时需确保其未超 7 天保留期且类型匹配 —— 此限制在 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中明确说明，但 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 未提及该保留期约束，开发者需以抽取文档为准。

> **注意**：  
> 文档解析支持音视频，但字段抽取明确不支持音视频输入（见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中“警告”）。若尝试对音视频 `biz_id` 调用抽取接口，将返回 `ParseResultNotReusable` 错误码（参见 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)）。

## 关键参数

所有请求共用以下基础参数与认证机制：

- **认证**：必须在 `Authorization` Header 中携带 `Bearer $DASHSCOPE_API_KEY`，API Key 需通过百炼控制台获取并安全存储（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）。
- **`biz_id`**：所有异步任务的核心标识符，由 `/parse/submit` 或 `/extract/submit` 返回，后续 `/parse/result` 和 `/extract/result` 均需传入。
- **输入来源（二选一）**：
  - `file_url` + `file_name`/`file_name_extension`：适用于首次解析或直接抽取；
  - `parsed_file_biz_id`：仅用于抽取，复用已有解析结果（需在 7 天内且非音视频源）。
- **处理配置（二选一）**：
  - `config_id`：引用控制台预设的解析/抽取配置；
  - `processing` 对象：内联定义，优先级高于 `config_id`，支持细粒度控制（如 `doc_processing_config.page_index`、`media_processing_config.enable_diarization`、`extract_processing_config.extract_schema` 等）。
- **输出控制**：
  - `output.output_file_format`：指定 `["markdown"]` 等格式；
  - `output.oss_config`：可选，用于将结果写入客户 OSS（需提供完整凭证）。

## 使用方式

标准调用流程为 **提交 → 轮询 → 获取结果**，所有接口均为 POST 请求：

1. **提交任务**：
   - 解析：`POST /api/v2/apps/parse-x/parse/submit`
   - 抽取：`POST /api/v2/apps/parse-x/extract/submit`
   - 响应含 `data.biz_id`，用于后续查询。

2. **轮询结果**：
   - 解析：`POST /api/v2/apps/parse-x/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）
   - 抽取：`POST /api/v2/apps/parse-x/extract/result`
   - 建议初始间隔 1–2 秒，随进度延长至 5–10 秒；收到 `ResultNotReady`（HTTP 409）时需重试（见 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)）。

3. **结果消费**：
   - 解析成功后，通过 `data.output_format_result[].output_file_url` 下载 Markdown 等格式结果，或解析 `data.layouts`/`data.segments` 等结构化字段；
   - 抽取成功后，`data.extract_result_json` 为 Schema 对齐的 JSON 对象，`data.fields` 提供字段级溯源信息（含 `bbox` 坐标与原文引用）。

CLI 工具亦支持全流程（如 `bl parsex parse submit`），详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 限制和注意事项

- **文件限制**：
  - 单文件大小、页数、时长等有硬性上限（如 `FileSizeExceeded`、`PageCountExceeded`、`FileFormatNotSupported`），具体数值以控制台配额页为准（见 [支持的文件与限制](../../../application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)）；
  - 音视频解析支持抽帧（`frame_extraction`），但输出图像宽高须在 `[32, 4096]` 区间。

- **生命周期约束**：
  - 解析结果默认保留 **30 天**（错误码 `ParseResultExpired`）；
  - 抽取任务复用的解析结果仅保留 **7 天**（见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)）；
  - `biz_id` 本身无过期时间，但关联资源失效后查询将失败。

- **安全与运维**：
  - API Key 必须通过环境变量管理，严禁硬编码或提交至代码仓库（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）；
  - 推荐为不同应用分配独立 API Key，便于权限隔离与轮转；
  - OSS 凭证（`access_key_id` 等）若传入请求体，仅限临时使用，不应长期暴露。

- **错误处理**：
  - 所有错误响应统一含 `request_id`、`code`、`message`，便于日志追踪；
  - `FileDownloadTimeout` 可重试，`FileDownloadFailed` 需修复 URL 权限后再试；
  - `ProcessingTimeout`/`InternalError` 等服务端错误建议指数退避重试。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)


