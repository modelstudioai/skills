# api [overview](overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步任务模型，通过 `biz_id` 轮询状态获取结果。API 使用百炼统一的 `DASHSCOPE_API_KEY` 鉴权，支持通过 HTTP 直接调用或百炼 CLI 工具集成。开发者需重点关注文件来源、处理配置、输出格式及生命周期限制等关键维度。

## 支持的模型/功能

ParseX API 当前提供两类结构化处理能力：

- **文档解析（Document Parsing）**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）、音视频（MP4/MOV/MP3/WAV）等格式，输出布局结构（`layouts`）、Markdown 内容、分段信息（`segments`）、剧情摘要（`synopsis_summary`）等。音视频支持人声分离、抽帧、剧情解析等高级能力，详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
  
- **字段抽取（Field Extraction）**：支持基于 JSON Schema 从已解析文档或原始文件中抽取结构化字段，返回带引用定位（`citations`）和推断标识（`inferred`）的结果。**注意**：抽取不支持直接输入音视频，仅支持文档类输入或复用解析结果；且复用的 `parsed_file_biz_id` 必须在 7 天保留期内且类型匹配，否则将返回 `ParseResultNotReusable` 错误 —— 具体错误含义请参考 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)。

> **注意**：文档解析与字段抽取虽共享 `biz_id` 异步模型和鉴权机制，但二者任务系统隔离、API 路径不同（`/parse/...` vs `/extract/...`），不可混用 `biz_id` 查询。

## 关键参数

所有提交接口均需以下基础参数：

- `file_url`（文档/抽取）或 `parsed_file_biz_id`（抽取）：二选一，指定输入源；
- `config_id` 或内联 `processing` 对象：二选一，后者优先级更高；
- `output` 配置（可选）：支持 `output_file_format`（如 `["markdown"]`）、`layout_table_format` 及 OSS 输出配置。

关键内联配置字段包括：
- 文档解析：`processing.doc_processing_config.page_index`、`head_foot`、`layout_position`；音视频解析：`media_processing_config.enable_diarization`、`frame_extraction.mode` 等；
- 字段抽取：`processing.extract_processing_config.extract_schema`（必需 JSON 对象）、`citation_required`、`allow_inference`。

所有查询接口均以 `biz_id` 为必填参数，并支持分片查询（`step_start`/`step_size`）以应对大结果集，详见 [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md) 和 [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)。

## 使用方式

1. **认证准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并设置为环境变量 `export DASHSCOPE_API_KEY="sk-..."`；每个请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header —— 具体流程见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析任务：调用 `POST /api/v2/apps/parse-x/parse/submit`，获取 `biz_id`；
   - 抽取任务：调用 `POST /api/v2/apps/parse-x/extract/submit`，获取 `biz_id`。
3. **轮询结果**：
   - 解析结果：调用 `POST /api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `POST /api/v2/apps/parse-x/extract/result`，同上逻辑。
4. **CLI 辅助**：推荐使用百炼 CLI 快速验证，例如 `bl parsex parse submit --file-url ...` 和 `bl parsex extract result --biz-id ... --follow`，详见各 API 概览页说明。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有硬性上限（如 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout`），具体数值以控制台配额页面为准；音视频抽帧分辨率范围为 `[32, 4096]` 像素。
- **生命周期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用的解析结果仅限 **7 天内**（`ParseResultNotReusable` 错误）；
  - 所有任务 `biz_id` 本身无长期有效性，结果就绪后应尽快下载或持久化。
- **安全与权限**：API Key 具备账号级权限，严禁硬编码或提交至公开仓库；RAM 子账号需显式授权对应接口权限。
- **错误处理**：所有失败响应均含 `request_id`、`code` 和 `message`，务必结合 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md) 进行分类重试（如 `FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试）或修正输入（如 URL 权限、Schema 格式）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


