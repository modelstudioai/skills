# api overview

ParseX API 提供文档与音视频的结构化解析及字段抽取能力，采用异步任务模型：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均需通过 API Key 鉴权，支持 HTTP REST 调用与百炼 CLI 工具集成。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPEG）等格式，输出布局结构（`layouts`）、Markdown、表格、段落等；可配置页码范围、页眉页脚、坐标定位、图片描述等 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（diarization）、剧情解析（synopsis）、分段（segments）、摘要（summary）、抽帧（frame extraction）等能力 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于 JSON Schema 从图文材料中结构化抽取字段，支持引用溯源（`citations`）、推断开关（`allow_inference`）和复用已有解析结果（需在 7 天保留期内） [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

> **注意**：字段抽取明确不支持音视频输入（见[错误码](../../raw/application-api-reference/api-overview/errors.md)中 `UnsupportedFileType`），且复用解析结果时若类型不匹配或超期，将返回 `ParseResultNotReusable` 错误。

## 关键参数

| 参数 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `file_url` / `parsed_file_biz_id` | string | 二选一：原始文件 URL 或已解析任务 ID（仅抽取支持） | [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `processing.*_config` | object | 内联处理配置，优先级高于 `config_id`；文档/音视频/抽取分别对应 `doc_processing_config`、`media_processing_config`、`extract_processing_config` | [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) |
| `processing.extract_processing_config.extract_schema` | object | 必填（内联模式下）：定义待抽取字段的 JSON Schema | [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `output.output_file_format` | string[] | 输出格式，当前仅支持 `["markdown"]` | [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) |
| `biz_id` | string | 所有异步任务的核心标识符，用于后续 `/parse/result` 或 `/extract/result` 查询 | [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md) |

## 使用方式

1. **认证**：设置环境变量 `DASHSCOPE_API_KEY`，并在每个请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY` [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选配置，获取 `biz_id`；
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`，获取 `biz_id`。
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，同上逻辑。
4. **CLI 辅助**：支持 `bl parsex parse submit` 和 `bl parsex extract submit` 等命令快速调试 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长等受配额约束；具体数值以控制台实时配额为准，非文档硬编码值（见[支持的文件与限制](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)）。
- **保留期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，仅支持 **7 天内** 的 `parsed_file_biz_id`（`ParseResultNotReusable` 错误）。
- **重试策略**：
  - `FileDownloadTimeout` 可重试；
  - `FileDownloadFailed` 不可重试，需修复 URL 或权限。
- **安全要求**：API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **错误处理**：所有失败响应均含 `request_id` 和标准 `code`/`message`，应结合 [错误码](../../raw/application-api-reference/api-overview/errors.md) 文档定位原因。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


