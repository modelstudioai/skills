# api overview

ParseX API 提供文档/音视频解析与结构化字段抽取两大核心能力，所有接口均采用[异步任务](../concepts/asynchronous-task.md)模型：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，适用于自动化处理场景。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出布局结构（`layouts`）、Markdown、表格、段落等；支持页码范围、页眉页脚、坐标定位、图片描述等配置 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等常见格式，提供人声分离（diarization）、剧情解析（synopsis）、分段（segments）、摘要（summary）、抽帧（frame extraction）等能力 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于 JSON Schema 从已解析内容或原始文件中抽取结构化字段，支持引用溯源（`citations`）、推断开关（`allow_inference`）和置信状态（`found`/`inferred`/`miss`） [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：字段抽取明确不支持音视频直接输入（见[提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)警告），且仅可复用 7 天内有效的解析结果；而文档解析本身支持音视频，二者能力边界需严格区分。

## 关键参数

| 参数 | 说明 | 示例/约束 |
|------|------|-----------|
| `file_url` / `parsed_file_biz_id` | 二选一：原始文件 URL 或已解析任务 ID | `https://example.com/doc.pdf` 或 `parseX-xxx` |
| `config_id` / `processing` | 二选一：预存配置 ID 或内联处理对象；`processing` 优先级更高 | `config_xxx` 或 `{ "doc_processing_config": { "page_index": "1-5" } }` |
| `processing.extract_processing_config.extract_schema` | 字段抽取必需：JSON Schema 对象（非字符串），定义目标字段结构 | `{ "type": "object", "properties": { "name": { "type": "string" } } }` |
| `output.output_file_format` | 文档解析可选：指定输出格式，当前仅支持 `["markdown"]` | `["markdown"]` |
| `biz_id` | 所有轮询接口必填：由 `/submit` 接口返回的唯一任务标识 | `parseX-2026xxxx-xxxxxxx` 或 `biz_xxx` |

## 使用方式

1. **认证准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并通过环境变量或 `Authorization` Header 传递 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析任务：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 和可选配置；
   - 抽取任务：调用 `/api/v2/apps/parse-x/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`。
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，同上逻辑。
4. **错误处理**：收到 `ResultNotReady`（409）需重试；`FileDownloadTimeout`（400）可重试，`FileDownloadFailed`（400）不可重试 —— 具体策略详见[错误码](../../raw/application-api-reference/api-overview/errors.md)。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限（如 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout`），具体配额以控制台为准。
- **保留期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误码）；
  - 抽取任务复用解析结果仅限 **7 天内**（`ParseResultNotReusable` 错误码）。
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **OSS 输出**：若需将结果写入客户 OSS，必须在 `output.oss_config` 或 `oss_config` 中完整提供 `bucket`、`endpoint`、`access_key_id`、`access_key_secret`（及可选 `security_token`）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)


