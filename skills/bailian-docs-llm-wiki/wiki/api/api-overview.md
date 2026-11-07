# api overview

ParseX API 提供文档/音视频解析与结构化字段抽取两大核心能力，采用异步任务模型：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均需通过 API Key 鉴权，支持 RESTful 调用与百炼 CLI 工具。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出结构化布局（`layouts`）、Markdown、表格等内容；[文档解析 API](raw/application-api-reference/api-overview/document-parsing.md) 详细说明了该流程。
- **音视频解析**：支持 MP4、MOV 等常见格式，可进行人声分离（diarization）、剧情解析（synopsis）、抽帧（frame extraction）及图像描述生成；相关参数详见 [提交解析任务](raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 中的 `media_processing_config` 配置项。
- **字段抽取**：基于用户提供的 JSON Schema，从已解析文档或原始文件中抽取结构化字段，支持引用溯源（`citations`）和推断（`allow_inference`）；其能力边界与限制请参考 [字段解析 API](raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：字段抽取不支持直接输入音视频（见[提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md)警告），且复用解析结果时要求 `parsed_file_biz_id` 对应的解析任务未超过 7 天保留期；而文档解析结果的保留期为 30 天（见[错误码](raw/application-api-reference/api-overview/errors.md)中 `ParseResultExpired` 说明）。二者保留策略不一致，调用时需按实际业务时效性分别校验。

## 关键参数

- **通用鉴权**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header，API Key 通过百炼控制台获取，详见 [认证](raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：`biz_id` 是所有异步操作的核心 ID，由 `/parse/submit` 或 `/extract/submit` 返回，用于后续 `/parse/result` 或 `/extract/result` 查询。
- **输入源**（二选一）：
  - `file_url`：直传文件 URL（支持公网可访问 OSS、HTTPS 等）；
  - `parsed_file_biz_id`：复用已有解析任务结果（仅限字段抽取，且需在 7 天内）。
- **处理配置**（二选一，内联优先）：
  - `config_id`：复用控制台预设的解析/抽取配置；
  - `processing.*_config`：内联定义，如 `doc_processing_config`、`media_processing_config`、`extract_processing_config`，其中 `extract_schema` 为必填 JSON 对象（非字符串）。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于指定结果落库至客户 OSS）。

## 使用方式

1. **准备凭证**：按 [认证](raw/application-api-reference/api-overview/authentication.md) 获取并安全配置 `DASHSCOPE_API_KEY`。
2. **提交任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选处理配置；
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`。
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，同上。
4. **错误处理**：收到 `ResultNotReady`（HTTP 409）需重试；其他错误码需结合 [错误码](raw/application-api-reference/api-overview/errors.md) 文档定位原因，例如 `FileSizeExceeded`（400）、`ProcessingTimeout`（500）等。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长等受配额约束，具体以控制台实时配额为准；`FileSizeExceeded`、`PageCountExceeded`、`PageRangeInvalid` 等错误码明确标识超限场景。
- **复用限制**：解析结果仅保留 30 天（`ParseResultExpired`），但字段抽取仅允许复用 7 天内的解析结果（`ParseResultNotReusable`）。
- **安全要求**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转。
- **重试策略**：`FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需先修复 URL 或权限；`ProcessingTimeout` 和 `InternalError` 建议指数退避重试。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


