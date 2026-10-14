# api overview

ParseX API 提供文档、图片及音视频的结构化解析与字段抽取能力，采用异步任务模型：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均需通过 API Key 鉴权，支持灵活的处理配置与多格式输出。该 API 服务于结构化内容生成、合同信息提取、音视频剧情分析等典型场景。

## 支持的模型/功能

API 当前提供两类核心能力：

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）、音视频（MP4/MOV/AVI 等）输入，输出 Markdown、布局结构（`layouts`）、分段内容（`segments`）、剧情摘要（`synopsis_summary`）等。音视频解析额外支持人声分离（diarization）、帧提取、ASR 文本与视觉描述生成。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。
  
- **字段抽取**：基于用户提供的 JSON Schema，从已解析文档或原始文件中抽取结构化字段，支持引用定位（`citations`）、推断开关（`allow_inference`）及字段级状态反馈（`found`/`miss`/`inferred`）。**注意**：抽取不支持直接输入音视频，仅支持文档类输入或复用解析结果；若复用解析结果，其必须在 7 天保留期内且类型匹配。详见 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 2 和 5 中音视频解析流程完整，二者功能边界清晰——音视频仅可解析，不可直接抽取；抽取必须基于解析后的结构化中间结果或文本型原始文件。

## 关键参数

- **必填认证参数**：`Authorization: Bearer $DASHSCOPE_API_KEY`（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）。
- **任务标识**：`biz_id`（由 `/parse/submit` 或 `/extract/submit` 返回），用于所有后续轮询请求。
- **输入源二选一**：
  - 解析任务：`file_url`（必需） + 可选 `file_name` 或 `file_name_extension`；
  - 抽取任务：`file_url` **或** `parsed_file_biz_id`（二者互斥）。
- **处理配置**：
  - 解析：通过 `processing.doc_processing_config`（文档）或 `processing.media_processing_config`（音视频）控制页码范围、抽帧策略、剧情解析开关等；
  - 抽取：必须提供 `processing.extract_processing_config.extract_schema`（内联 Schema）或 `config_id`，且 `extract_schema` 为合法 JSON 对象（非字符串，文档 7 示例中 `curl` 的 `-d` 内嵌写法已正确体现对象结构，无需额外转义为字符串）。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于指定客户 OSS 存储）。

## 使用方式

1. **鉴权准备**：获取 `DASHSCOPE_API_KEY` 并设为环境变量（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）；
2. **提交任务**：
   - 解析：调用 `/parse/submit`，传入 `file_url` 及可选处理配置，获得 `biz_id`；
   - 抽取：调用 `/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 Schema，获得 `biz_id`；
3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`），状态为 `processing` 时需重试（建议指数退避）；
   - 抽取结果：调用 `/extract/result`，逻辑同上；
4. **错误处理**：收到 `ResultNotReady`（HTTP 409）应继续轮询；收到其他错误码（如 `NotExistBizId`、`FileDownloadFailed`）需依据 [错误码](../../raw/application-api-reference/api-overview/errors.md) 文档定位原因。

## 限制和注意事项

- **文件限制**：单文件大小、页数、音视频时长均有上限（具体数值未在原始文档中统一说明，但错误码中明确列出 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout`）；解析结果保留期为 **30 天**（`ParseResultExpired`），而抽取复用的解析结果保留期为 **7 天**（文档 7 警告）；
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）；
- **异步可靠性**：任务失败后不会自动重试，需应用层根据错误码判断是否可重试（例如 `FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试）；
- **功能约束**：抽取任务无法直接作用于音视频原始文件；复用解析结果时，若 `parsed_file_biz_id` 对应结果已过期或类型不匹配（如用文档解析 ID 提交音视频抽取），将返回 `ParseResultNotReusable` 错误。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


