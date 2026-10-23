# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用[异步任务](../concepts/asynchronous-task.md)模型。开发者需先通过 API Key 鉴权，提交任务获取 `biz_id`，再轮询查询结果。整个流程支持灵活的配置方式（预存配置 ID 或内联 JSON），并提供细粒度的错误码和状态反馈。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落等；可选页眉页脚、坐标定位、图片描述生成等功能。详见[文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV、AVI、MP3、WAV 等格式，输出 ASR 文本、人声分离（`diarization`）、剧情解析（`synopsis_parse`）、分段（`segments`）、摘要（`summary`）及抽帧结果。抽帧支持 `auto` 和 `frame_rate` 模式，可指定宽高（32–4096 px）。详见[提交解析任务](raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于用户提供的 JSON Schema 从图文材料中抽取结构化字段，支持引用溯源（`citations`）、推断开关（`allow_inference`）及自定义 Prompt。**注意：抽取不支持音视频输入**，且仅能复用 7 天内有效的解析结果（见[错误码](raw/application-api-reference/api-overview/errors.md)中 `ParseResultNotReusable` 和 `ParseResultExpired`）。

> **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 4 中音视频解析示例未提及抽取能力；二者边界清晰，无矛盾。但文档 7 末尾引用的配额说明链接 `raw/application-user-guide/.../supported-files-and-limits.md` 与当前 API 概览层级不一致，该路径实际属于用户指南而非 API 参考，建议以[错误码](raw/application-api-reference/api-overview/errors.md)中明确列出的限制（如 `PageCountExceeded`、`FileSizeExceeded`）为准。

## 关键参数

- **鉴权**：必须在 `Authorization: Bearer <API_KEY>` Header 中传递百炼平台颁发的 `DASHSCOPE_API_KEY`（以 `sk-` 开头），详见[认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：所有异步操作依赖 `biz_id` —— 由 `/parse/submit` 或 `/extract/submit` 返回，用于后续 `/parse/result` 或 `/extract/result` 查询。
- **输入源**（二选一）：
  - `file_url` + `file_name`（或 `file_name_extension`）：直接传入远程文件；
  - `parsed_file_biz_id`：复用已有解析任务结果（仅限文档类，且需在 7 天保留期内）。
- **处理配置**（二选一，内联优先）：
  - `config_id`：复用控制台预设的解析或抽取配置；
  - `processing.*_config`：内联定义，如 `doc_processing_config`、`media_processing_config`、`extract_processing_config`，其中 `extract_schema` 为必需 JSON 对象。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于持久化到客户 OSS）。

## 使用方式

1. **准备凭证**：在百炼控制台获取 `DASHSCOPE_API_KEY`，并通过环境变量或 Header 传递；
2. **提交任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选配置；
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`；
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，解析 `data.extract_result_json` 或细粒度 `data.fields`；
4. **错误处理**：根据响应中的 `code` 和 HTTP 状态码对照[错误码](../../raw/application-api-reference/api-overview/errors.md)，例如 `ResultNotReady`（409）需重试，`FileDownloadTimeout`（400）可重试，`FileDownloadFailed`（400）不可重试。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长等受服务端配额约束，超限时返回 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout` 等错误码，具体阈值以[错误码](../../raw/application-api-reference/api-overview/errors.md)所列为准；
- **保留期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误码对应此期限）；
  - 抽取任务复用解析结果时，仅支持 **7 天内**的有效 `parsed_file_biz_id`（见文档 7 警告）；
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库；建议按应用拆分 Key 并定期轮转，详见[认证](../../raw/application-api-reference/api-overview/authentication.md)；
- **OSS 凭据**：若使用 `output.oss_config`，需确保 `access_key_id`/`access_key_secret`/`security_token` 具备目标 Bucket 的写入权限，且 Token 未过期；
- **Schema 规范**：`extract_schema` 必须是合法 JSON 对象，类型支持 `string`、`number`、`boolean`、`object`、`array`；嵌套过深或字段过多可能导致 `InvalidSchema` 错误。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


