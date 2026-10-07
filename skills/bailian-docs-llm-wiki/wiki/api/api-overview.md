# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，请求与响应统一返回 `request_id` 用于问题定位。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出 Markdown、布局信息（`layouts`）、段落/表格/图片计数等；可配置页码范围、是否解析页眉页脚、是否返回坐标及图片描述等 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等常见音视频格式，提供 ASR 文本、人声分离（`diarization`）、剧情解析（`synopsis_parse`）、抽帧（支持 `auto` 或指定帧率）等能力 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：支持从已解析文档（`parsed_file_biz_id`）或原始文件（`file_url`）中，按用户提供的 JSON Schema 抽取结构化字段；支持引用溯源（`citations`）、推断开关（`allow_inference`）和自定义 Prompt [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

> **注意**：字段抽取明确不支持音视频直接输入（见[错误码](../../raw/application-api-reference/api-overview/errors.md)中 `UnsupportedFileType` 错误说明），且仅能复用**7 天内**的解析结果（`ParseResultNotReusable` 错误即由此触发）。

## 关键参数

| 参数 | 位置 | 说明 | 必填 |
|------|------|------|------|
| `file_url` / `parsed_file_biz_id` | 请求体 | 文件来源二选一：远程 URL 或已存在的解析任务 ID | 是（二者必选其一） |
| `config_id` / `processing` | 请求体 | 处理配置二选一：预存配置 ID 或内联对象；若同时存在，`processing` 优先生效 | 否（但至少需提供其一） |
| `processing.doc_processing_config` / `media_processing_config` / `extract_processing_config` | `processing` 内嵌 | 分别对应文档、音视频、抽取场景的专用配置对象 | 按场景必填（如使用 `processing`） |
| `processing.extract_processing_config.extract_schema` | 内嵌 | 字段抽取必需的 JSON Schema 对象（非字符串） | 是（使用内联抽取配置时） |
| `biz_id` | 查询接口请求体 | 所有结果查询接口（`/parse/result`, `/extract/result`）的唯一路径标识 | 是 |

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并通过环境变量或 `Authorization` Header 传递；
2. **提交任务**：
   - 解析任务：调用 `/api/v2/apps/parse-x/parse/submit`，获取 `biz_id`；
   - 抽取任务：调用 `/api/v2/apps/parse-x/extract/submit`，获取 `biz_id`；
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed` 停止，`processing` 继续）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，逻辑同上；
4. **错误处理**：当 `status` 为 `failed` 时，结合响应中的 `code` 字段，查阅 [错误码](../../raw/application-api-reference/api-overview/errors.md) 进行归因与重试决策。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限（如 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout`），具体配额以控制台实时配置为准；
- **保留期限制**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，仅支持 **7 天内** 的 `biz_id`（`ParseResultNotReusable` 错误）；
- **重试策略**：
  - `FileDownloadTimeout` 可重试；
  - `FileDownloadFailed` 不可重试，需修复 URL 或访问权限；
  - `ResultNotReady` 需持续轮询同一 `biz_id`，不可新建任务；
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转。

## 来源文档

- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


