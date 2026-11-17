# api [overview](overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，采用[异步任务](../concepts/asynchronous-task.md)模型：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均通过 RESTful HTTP 调用，需使用百炼平台颁发的 API Key 进行鉴权。开发者可选择直接调用 HTTP 接口，或使用百炼 CLI 工具简化流程。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出布局结构（`layouts`）、Markdown、表格、段落等；支持页码范围、页眉页脚、坐标定位、图片描述等精细化控制。详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等常见视频格式及 MP3、WAV 等音频格式，提供人声分离（Diarization）、剧情解析（Synopsis）、分段（Segments）、抽帧（Frame Extraction）及 ASR 文本等能力。
- **字段抽取**：支持从已解析文档或原始文件中，按用户提供的 JSON Schema 抽取结构化字段，返回带引用溯源（`citations`）和置信状态（`found`/`miss`/`inferred`）的结果。> **注意**：抽取不支持直接输入音视频文件，仅支持文档类输入或复用解析任务生成的 `parsed_file_biz_id`；该限制在 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中明确说明，与部分旧版文档中模糊表述存在差异。

## 关键参数

- **通用认证**：所有请求必须携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}` Header，API Key 通过百炼控制台获取，详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：`biz_id` 是核心任务 ID，由 `/parse/submit` 或 `/extract/submit` 返回，用于后续轮询 `/parse/result` 或 `/extract/result`。
- **输入源二选一**：
  - 解析任务：`file_url`（必填）或 `config_id`（可选）；
  - 抽取任务：`file_url` 与 `parsed_file_biz_id` 二选一（后者需在 7 天保留期内且类型匹配）。
- **处理配置**：`processing` 对象支持内联定义，优先级高于 `config_id`。文档解析含 `doc_processing_config`，音视频解析含 `media_processing_config`，字段抽取含 `extract_processing_config`（必须包含 `extract_schema`）。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于持久化到客户 OSS）等。

## 使用方式

1. **准备凭证**：设置环境变量 `DASHSCOPE_API_KEY`，确保其安全存储；
2. **提交任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选配置；
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`；
3. **轮询结果**：以返回的 `biz_id` 调用对应 `/result` 接口，检查 `data.status` 字段：
   - `init` / `processing` → 继续轮询（建议指数退避）；
   - `success` → 解析结果在 `data.layouts` / `data.output_format_result`，抽取结果在 `data.extract_result_json` / `data.fields`；
   - `failed` → 查看 `code` 和 `message`，结合 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md) 定位原因；
4. **CLI 辅助**：可使用 `bl parsex parse submit` / `bl parsex extract result` 等命令替代手动 HTTP 调用，详见 CLI 文档。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限（如 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout`），具体配额以控制台实时显示为准；
- **保留期约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**（`ParseResultNotReusable` 错误）；
- **重试策略**：
  - `FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需修复 URL 或权限；
  - `ResultNotReady` 表示任务未完成，应继续轮询而非重提；
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；建议按应用拆分 Key 并定期轮转；
- **Schema 有效性**：`extract_schema` 必须为合法 JSON 对象，否则返回 `InvalidSchema`（HTTP 400）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)


