# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，请求与响应统一返回 `request_id` 用于问题定位。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出 Markdown、布局信息（`layouts`）、分片内容及 OSS 可访问链接；支持页码范围控制、页眉页脚开关、坐标返回、图片描述生成等配置 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV 等主流格式，提供人声分离（`enable_diarization`）、剧情解析（`enable_synopsis_parse`）、段落切分（`segments`）、摘要生成（`synopsis_summary`）及智能抽帧（`frame_extraction`）等能力 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：支持从已解析结果（`parsed_file_biz_id`）或原始文件（`file_url`）中按 JSON Schema 抽取结构化字段，返回带引用溯源（`citations`）和推断标识（`inferred`）的 `extract_result_json` [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档解析与字段抽取虽共享 `biz_id` 命名空间，但二者任务类型隔离；复用解析结果进行抽取时，必须确保 `parsed_file_biz_id` 在 7 天保留期内且类型匹配，否则将返回 `ParseResultNotReusable` 错误 —— 此限制在 [错误码](../../raw/application-api-reference/api-overview/errors.md) 中明确说明，但 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 文档中误写为“7 天保留期”，实际应以错误码文档为准。

## 关键参数

- **必填鉴权头**：`Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需通过百炼控制台获取并安全存储 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：所有查询接口（`/parse/result`、`/extract/result`）均需 `biz_id`，该 ID 由对应提交接口（`/parse/submit` 或 `/extract/submit`）返回。
- **输入源二选一**：
  - 解析任务：`file_url`（必需）或 `file_name_extension`（与 `file_name` 二选一）；
  - 抽取任务：`file_url` **或** `parsed_file_biz_id`（二者不可共存）。
- **处理配置优先级**：内联 `processing` 对象始终覆盖 `config_id`；若同时传入，以 `processing` 为准（见各提交接口示例）。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.layout_table_format`（`markdown`/`html`）及 `oss_config`（用于持久化输出）均为可选。

## 使用方式

1. **准备凭证**：获取并配置 `DASHSCOPE_API_KEY` 环境变量 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 文档/音视频解析 → 调用 `/api/v2/apps/parse-x/parse/submit`；
   - 字段抽取 → 调用 `/api/v2/apps/parse-x/extract/submit`。
3. **轮询结果**：
   - 解析任务 → 调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`；
   - 抽取任务 → 调用 `/api/v2/apps/parse-x/extract/result`，检查 `data.status`；
   - 状态为 `processing` 时需重试（建议指数退避），`success` 或 `failed` 时终止。
4. **错误处理**：收到 `failed` 状态后，结合响应中的 `code` 字段查阅 [错误码](../../raw/application-api-reference/api-overview/errors.md) 文档定位原因（如 `FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试）。

## 限制和注意事项

- **文件限制**：单文件大小上限、页数上限、音视频时长上限等详见配额文档；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded` 错误 [错误码](../../raw/application-api-reference/api-overview/errors.md)。
- **保留期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误对应此周期）；
  - 抽取任务复用的解析结果仅支持 **7 天内**（`ParseResultNotReusable` 错误触发条件）。
- **不支持场景**：字段抽取 **不支持直接输入音视频**（`UnsupportedFileType` 错误），必须先解析为图文再抽取；`file_url` 必须可公开访问或携带有效鉴权（如 OSS 签名 URL）。
- **安全要求**：API Key 严禁硬编码或提交至代码仓库，推荐按应用拆分并定期轮转 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。

## 来源文档

- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)


