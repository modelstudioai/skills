# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析能力，以及基于 Schema 的字段抽取能力。所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过标准 `Authorization: Bearer <API Key>` 进行鉴权，适用于自动化集成与批量处理场景。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出 Markdown、布局结构（`layouts`）、表格、段落、页码等；支持页码范围指定、页眉页脚控制、坐标返回、图片描述生成等配置。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV 等主流音视频格式，输出 ASR 文本、人声分离（`diarization`）、抽帧图像、剧情解析摘要（`synopsis_summary`）、分段剧情（`synopsis_segments`）及视觉帧描述（`text_info`）。详见 [提交解析任务](raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于用户提供的 JSON Schema，从已解析文档或原始文件中抽取结构化字段（如合同编号、金额），支持引用溯源（`citations`）、推断开关（`allow_inference`）和置信状态（`found`/`miss`/`inferred`）。> **注意**：抽取不支持直接输入音视频，仅支持文档类输入或复用文档解析结果；且复用的解析结果必须在 7 天保留期内，否则返回 `ParseResultNotReusable` 错误 —— 具体限制请参考 [错误码](raw/application-api-reference/api-overview/errors.md) 中的说明。

## 关键参数

- `biz_id`：所有异步任务的核心标识，由 `/parse/submit` 或 `/extract/submit` 返回，用于后续 `/parse/result` 或 `/extract/result` 查询。
- `file_url`：必须为公网可访问、带有效签名（如 OSS 签名 URL）的文件地址；不支持内网或需登录跳转的链接。
- `processing` 对象：内联处理配置，优先级高于 `config_id`。关键子字段包括：
  - `doc_processing_config.page_index`（如 `"1-5"`）、`head_foot`、`layout_position`
  - `media_processing_config.enable_synopsis_parse`、`frame_extraction.mode`
  - `extract_processing_config.extract_schema`（必需 JSON 对象，非字符串）、`citation_required`
- `output.oss_config`：用于指定结果写入客户自有 OSS，需完整提供 `bucket`、`endpoint`、`access_key_id`、`access_key_secret`（及可选 `security_token`）。

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并通过环境变量或请求 Header 传递。务必遵循安全规范，避免硬编码或泄露 —— 具体操作见 [鉴权](raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析任务：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选 `processing` 配置；
   - 抽取任务：调用 `/api/v2/apps/parse-x/extract/submit`，二选一提供 `file_url` 或 `parsed_file_biz_id`，并确保 `extract_schema` 正确嵌套在 `processing.extract_processing_config` 中。
3. **轮询结果**：使用返回的 `biz_id` 定期调用对应的结果端点（`/parse/result` 或 `/extract/result`），检查 `data.status` 字段。状态为 `processing` 时继续轮询；为 `success` 或 `failed` 时终止。轮询间隔建议 ≥1s，避免高频请求触发限流。

## 限制和注意事项

- **文件限制**：单文件大小上限为 100 MB；PDF 页数上限为 1000 页；音视频时长上限为 2 小时；超出将返回 `FileSizeExceeded` 或 `PageCountExceeded` 错误。
- **保留期约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，该结果必须在 **7 天内**（`ParseResultNotReusable` 错误），且类型匹配（音视频解析结果不可用于字段抽取）。
- **错误处理**：所有失败响应均含 `request_id`、`code` 和 `message`。例如 `ResultNotReady`（409）表示任务未完成，应继续轮询；`FileDownloadTimeout`（400）可重试，而 `FileDownloadFailed`（400）需修复源文件；详细含义请查阅 [错误码](raw/application-api-reference/api-overview/errors.md)。
- **配额与计费**：服务受账号级配额限制，超限返回 `ServiceQuotaExhausted`（503）；欠费将返回 `AccountOverdue`（403）。实际配额以控制台实时显示为准。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)


