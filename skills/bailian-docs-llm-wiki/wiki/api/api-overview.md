# api [overview](overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，采用异步任务模型（提交 → 轮询 → 获取结果）。所有接口均通过 `Authorization: Bearer <API Key>` 鉴权，请求需指定 workspace ID 和区域 endpoint。开发者应优先使用环境变量管理凭证，并遵循最小权限原则配置 RAM 子账号权限。

## 支持的模型/功能

ParseX API 当前支持两类主功能：

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）及音视频（MP4/MOV/AVI 等）输入，输出结构化布局（`layouts`）、Markdown 内容、帧图像、ASR 文本、人声分离、剧情解析（`synopsis_segments`/`synopsis_summary`）等。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **字段抽取**：支持从已解析文档或原始文件中，按用户提供的 JSON Schema 抽取结构化字段，返回带引用定位（`citations`）和置信状态（`found`/`miss`/`inferred`）的结果。**注意：抽取不支持直接输入音视频**，仅支持图文材料或复用解析任务生成的 `parsed_file_biz_id`；且复用的解析结果必须在 7 天保留期内、类型匹配，否则将失败 —— 具体限制见 [错误码](raw/application-api-reference/api-overview/errors.md) 中 `ParseResultNotReusable` 和 `UnsupportedFileType` 条目。

> **注意**：文档 8 明确指出“抽取不支持音视频输入”，而文档 4 的音视频解析示例中未说明其结果能否用于后续抽取。实际调用时，若尝试对音视频解析任务的 `biz_id` 调用抽取接口，将返回 `ParseResultNotReusable` 错误。请严格按 [提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 所述，仅对文档类解析结果复用。

## 关键参数

所有提交接口共用以下关键参数模式：

- **身份认证**：`Authorization: Bearer $DASHSCOPE_API_KEY`（必须），详见 [认证](raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：`biz_id`（由 `/submit` 接口返回，用于所有 `/result` 查询）。
- **输入源（二选一）**：
  - `file_url` + `file_name`（或 `file_name_extension`）：适用于首次解析或抽取；
  - `parsed_file_biz_id`：仅用于字段抽取，复用已有解析结果（需在 7 天内且类型合法）。
- **处理配置（二选一，内联优先）**：
  - `config_id`：引用控制台预设的解析/抽取配置；
  - `processing` 对象：支持细粒度控制，如 `doc_processing_config.page_index`、`media_processing_config.enable_diarization`、`extract_processing_config.extract_schema` 等。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于持久化到客户 OSS）。

## 使用方式

标准[异步调用](../concepts/asynchronous-invocation.md)流程为三步：

1. **提交任务**：调用 `/parse/submit` 或 `/extract/submit`，传入文件 URL 或解析 ID、处理配置等，获取 `biz_id`；
2. **轮询状态**：以 `biz_id` 调用 `/parse/result` 或 `/extract/result`，检查 `data.status` 字段；
   - `init` / `processing`：继续轮询（建议指数退避）；
   - `success`：读取 `data.output_format_result`（解析）或 `data.extract_result_json`（抽取）；
   - `failed`：结合 `code` 字段查 [ParseX API 错误码](raw/application-api-reference/api-overview/errors.md) 定位原因；
3. **结果消费**：解析结果含 Markdown URL、布局坐标、音视频分段等；抽取结果含结构化 JSON、字段级引用（`citations`）及推理说明（`reason`）。

CLI 用户可使用 `bl parsex parse submit` / `bl parsex extract result` 等命令替代 HTTP 调用，详见 [使用 CLI](raw/application-user-guide/agent-context/getting-started-overview/integration-overview/cli.md)。

## 限制和注意事项

- **配额与计费**：服务受账户配额约束，超限返回 `ServiceQuotaExhausted`（503）；欠费将触发 `AccountOverdue`（403）；详情见控制台配额管理。
- **文件限制**：
  - 单文件大小、页数、时长均有上限，超限返回 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout` 等错误；
  - 不支持格式返回 `FileFormatNotSupported`；URL 不可达返回 `InvalidFileUrl` 或 `FileDownloadFailed`（不可重试）/`FileDownloadTimeout`（可重试）。
- **结果时效性**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired`）；
  - 解析结果复用于抽取的窗口期为 **7 天**（`ParseResultNotReusable`）；
  - 音视频解析的 `segments` 和 `frames` 也受相同保留策略约束。
- **安全实践**：
  - API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库；
  - 建议为不同应用分配独立 API Key，便于审计与撤销；
  - OSS 凭据（`access_key_id`/`access_key_secret`）若用于输出，同样需保密并定期轮转。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)


