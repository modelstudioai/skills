# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 以 RESTful 形式提供，统一通过 `Authorization: Bearer <API Key>` 鉴权，并遵循标准 HTTP 状态码与错误响应规范。

## 支持的模型/功能

ParseX 当前提供两类核心能力：

- **文档解析 API**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）、音视频（MP4/MOV/AVI/WAV/MP3）等格式，输出结构化布局（`layouts`）、Markdown 内容、表格/段落/页眉页脚识别、音视频人声分离（`diarization`）、剧情解析（`synopsis_parse`）、抽帧（`frame_extraction`）等。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。

- **字段解析 API**：支持基于 JSON Schema 从已解析或原始文档中抽取结构化字段，返回带引用溯源（`citations`）和推断状态（`inferred`/`found`/`miss`）的结果。**注意：字段解析不支持直接输入音视频文件**，仅支持 `file_url`（文档类）或复用 `parsed_file_biz_id`（需在 7 天保留期内且类型匹配），详见 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档 8 明确指出“抽取不支持音视频输入”，而文档 2 和 3 中文档解析 API 明确支持音视频；二者功能边界清晰，但需开发者严格区分使用场景——音视频必须先经 `/parse/submit` 解析，再将生成的 `biz_id` 作为 `parsed_file_biz_id` 提交至 `/extract/submit`，不可跳过解析步骤直传音视频 URL。

## 关键参数

所有提交接口均依赖以下关键参数组合，且存在明确互斥关系：

- **文件来源**（二选一）：
  - `file_url`：公开可访问的文件 URL（HTTP/HTTPS），适用于首次解析或独立抽取；
  - `parsed_file_biz_id`：此前 `/parse/submit` 返回的 `biz_id`，用于复用解析结果进行字段抽取（仅限文档类解析结果，且需 ≤7 天）。

- **处理定义**（二选一，内联优先）：
  - `config_id`：控制台预存的配置 ID（如 `config_xxx`）；
  - `processing`：内联 JSON 对象，当两者共存时 `processing` 优先生效（见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 和 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)）。

- **核心内联配置字段**：
  - 文档解析：`processing.doc_processing_config`（页码范围、坐标、页眉页脚等）或 `processing.media_processing_config`（人声分离、剧情解析、抽帧参数）；
  - 字段抽取：`processing.extract_processing_config.extract_schema`（必需 JSON Schema）、`citation_required`、`allow_inference`；
  - 公共输出：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于持久化到客户 OSS）。

## 使用方式

1. **鉴权准备**：获取 `DASHSCOPE_API_KEY` 并通过环境变量或 `Authorization` Header 传递，详见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)；
2. **提交任务**：
   - 解析任务：调用 `/api/v2/apps/parse-x/parse/submit`，获取 `biz_id`；
   - 抽取任务：调用 `/api/v2/apps/parse-x/extract/submit`，获取 `biz_id`；
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，逻辑同上；
4. **错误处理**：根据返回的 `code`（如 `ResultNotReady`、`NotExistBizId`、`UnsupportedFileType`）按 [错误码](../../raw/application-api-reference/api-overview/errors.md) 文档指导重试或修正。

## 限制和注意事项

- **异步时效性**：解析/抽取均为异步任务，需主动轮询；`ResultNotReady`（HTTP 409）表示任务未就绪，应指数退避重试。
- **文件限制**：
  - 单文件大小、页数、音视频时长等受配额约束，具体以控制台实际配置为准；
  - `FileFormatNotSupported`、`FileSizeExceeded`、`PageCountExceeded` 等错误码对应明确限制（见 [错误码](../../raw/application-api-reference/api-overview/errors.md)）；
- **复用限制**：
  - `parsed_file_biz_id` 仅支持文档类解析结果，音视频解析结果不可用于字段抽取；
  - 复用有效期为 **7 天**（非文档 7 中提到的解析结果 30 天保留期），超期返回 `ParseResultNotReusable`；
- **安全要求**：
  - API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库；
  - OSS 凭据（`access_key_id`/`access_key_secret`）若需透传，应确保传输与存储安全；
- **Schema 与引用**：字段抽取的 `extract_schema` 必须为合法 JSON Schema；启用 `citation_required` 可获取原文定位（页码、坐标 `bbox`），对审计与可解释性至关重要。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)


