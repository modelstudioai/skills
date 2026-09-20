# overview

ParseX 是百炼平台提供的文档与音视频智能解析与结构化抽取服务，支持异步提交任务、轮询结果的标准化 API 流程。核心能力分为两层：底层**文档解析 API** 将原始文件（PDF/图片/音视频）转化为结构化内容（如 Markdown、布局信息、分段摘要）；上层**字段解析 API** 基于 JSON Schema 从解析结果或原始文件中精准抽取指定字段。所有调用均需通过 API Key 鉴权，并遵循统一的错误码体系与异步状态机模型。

## 支持的模型/功能

- **文档解析**：支持 PDF、图像（JPG/PNG）、音视频（MP4/MOV/AVI 等）输入，输出包括：
  - 文档级：Markdown 内容、`layouts`（带坐标和语义的段落/表格/图片）、页眉页脚、抽帧图像（音视频）；
  - 音视频专属：人声分离（`enable_diarization`）、剧情解析（`enable_synopsis_parse`）、分段摘要（`synopsis_segments`）、全局摘要（`synopsis_summary`）。
- **字段抽取**：支持从解析后的结构化结果（`parsed_file_biz_id`）或原始文件 URL 输入，按用户定义的 JSON Schema 抽取结构化字段，返回带引用溯源（`citations`）的 `extract_result_json` 和细粒度 `fields` 结果。
- **配置复用**：支持预存 `config_id` 或内联 `processing` 配置，内联参数优先级更高（详见 [提交解析任务](../../raw/application-api-reference/overview/document-parsing/parse-submit.md) 和 [提交抽取任务](../../raw/application-api-reference/overview/field-extraction/extract-submit.md)）。

## 关键参数

- **通用必填**：`biz_id`（用于轮询）、`Authorization: Bearer $DASHSCOPE_API_KEY`（鉴权头）。
- **解析任务关键参数**：
  - `file_url`（必需）：可公开访问的文件 URL；
  - `processing.doc_processing_config.page_index`：指定页码范围（如 `"1-10"`）；
  - `processing.media_processing_config.frame_extraction`：控制抽帧模式、分辨率等；
  - `output.output_file_format`：指定输出格式（当前仅支持 `["markdown"]`）。
- **抽取任务关键参数**：
  - 二选一输入源：`file_url` 或 `parsed_file_biz_id`（后者需在 7 天保留期内且类型匹配）；
  - `processing.extract_processing_config.extract_schema`：必需的 JSON Schema 对象（非字符串），定义待抽取字段结构；
  - `processing.extract_processing_config.citation_required`：是否返回引用位置（默认 `true`）。
> **注意**：文档 7 中示例将 `extract_schema` 写为字符串并要求“转义”，但实际 API 接收的是 JSON 对象（见返回示例中的 `extract_result_json` 结构）。该描述易引发客户端序列化错误，应以 [查询抽取结果](../../raw/application-api-reference/overview/field-extraction/extract-result.md) 的响应结构为准。

## 使用方式

1. **鉴权准备**：获取 `DASHSCOPE_API_KEY` 并设为环境变量，所有请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 头 —— 详见 [鉴权](../../raw/application-api-reference/overview/authentication.md)。
2. **提交任务**：
   - 解析任务：调用 `/parse/submit`，获取 `biz_id`；
   - 抽取任务：调用 `/extract/submit`，获取 `biz_id`（可复用解析任务的 `biz_id`）。
3. **轮询结果**：
   - 解析任务：调用 `/parse/result?biz_id=xxx`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取任务：调用 `/extract/result?biz_id=xxx`，同上。
4. **错误处理**：收到 `ResultNotReady`（409）需重试；`FileDownloadTimeout`（400）可重试，`FileDownloadFailed`（400）不可重试 —— 具体策略见 [错误码](../../raw/application-api-reference/overview/errors.md)。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限（如 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout`），具体配额以控制台为准；
- **保留期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误码）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**（`ParseResultNotReusable` 错误码）；
- **音视频约束**：抽取任务**不支持直接输入音视频**（`UnsupportedFileType`），必须先解析再抽取；
- **安全要求**：API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库；
- **OSS 输出**：若使用 `output.oss_config`，需确保提供完整的 `access_key_id`、`access_key_secret` 和 `security_token`（临时凭证），且 Bucket 有写入权限。

## 来源文档

- [鉴权](../../raw/application-api-reference/overview/authentication.md)
- [错误码](../../raw/application-api-reference/overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/overview/field-extraction/extract-result.md)


