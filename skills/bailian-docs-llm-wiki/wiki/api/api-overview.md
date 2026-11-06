# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过百炼平台统一鉴权，支持 RESTful HTTP 调用及 CLI 工具集成。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出布局结构（`layouts`）、Markdown、表格、段落等；可配置页码范围、是否解析页眉页脚、坐标位置、图片描述等 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，输出分段（`segments`）、ASR 文本、人声分离（`diarization`）、剧情解析（`synopsis_parse`）、抽帧（`frame_extraction`）及摘要 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：支持从原始文件 URL 或**已解析的 `parsed_file_biz_id`** 中按 JSON Schema 抽取结构化字段，返回带引用溯源（`citations`）的 `extract_result_json` 和细粒度 `fields` 结果 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

> **注意**：字段抽取不支持直接输入音视频（见[错误码](../../raw/application-api-reference/api-overview/errors.md)中 `UnsupportedFileType`），且仅能复用**7 天内有效**的解析结果；而文档解析结果保留期为 30 天（见 `ParseResultExpired` 错误码）。二者保留策略不一致，需注意时效性。

## 关键参数

- **必填认证**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header，API Key 通过百炼控制台获取，详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：
  - 解析任务：`file_url`（必需） + 可选 `file_name` 或 `file_name_extension`；
  - 抽取任务：二选一 — `file_url` 或 `parsed_file_biz_id`（复用解析结果）；
- **处理配置**：
  - `config_id`（预存配置）与 `processing`（内联配置）可共存，后者优先级更高；
  - 内联配置需按类型提供：`doc_processing_config`（文档）、`media_processing_config`（音视频）、`extract_processing_config`（抽取）；
  - 抽取必需 `extract_schema`（JSON 对象），且 `extract_schema` 字段值类型需与实际内容匹配，否则可能触发 `InvalidSchema` 错误。
- **输出控制**：
  - `output.output_file_format`：当前仅支持 `["markdown"]`；
  - `output.oss_config`：用于指定结果写入客户 OSS，需完整提供 `bucket`、`endpoint`、`access_key_id`、`access_key_secret`（及可选 `security_token`）。

## 使用方式

1. **准备凭证**：设置环境变量 `DASHSCOPE_API_KEY`，确保其具备对应工作空间调用权限 [认证](../../raw/application-api-reference/api-overview/authentication.md)；
2. **提交任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，获取 `biz_id`；
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，获取 `biz_id`；
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，同上；
4. **终止条件**：`status` 为 `success` 或 `failed` 时停止轮询；若为 `failed`，参考 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位原因。

CLI 用户可使用 `bl parsex parse submit` / `bl parsex extract submit` 等命令替代 HTTP 调用，详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 限制和注意事项

- **文件限制**：
  - 单文件大小上限：100 MB（`FileSizeExceeded`）；
  - 文档页数上限：10,000 页（`PageCountExceeded`）；
  - 音视频时长上限：2 小时（超时将返回 `ProcessingTimeout`）；
- **时效性约束**：
  - 解析结果保留 30 天（`ParseResultExpired`）；
  - 抽取任务复用的解析结果仅限 7 天内（`ParseResultNotReusable`）；
- **重试策略**：
  - `FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需修复 URL 或访问权限；
  - `ResultNotReady` 表示任务仍在运行，应继续轮询而非重试提交；
- **安全要求**：
  - API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库；
  - 建议为不同应用分配独立 API Key，便于权限隔离与轮转管理 [认证](../../raw/application-api-reference/api-overview/authentication.md)。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


