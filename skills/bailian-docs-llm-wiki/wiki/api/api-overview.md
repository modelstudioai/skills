# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用[异步任务](../concepts/asynchronous-task.md)模型。调用流程统一为：提交任务 → 获取 `biz_id` → 轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，需提前在百炼控制台获取凭证。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出布局结构（`layouts`）、Markdown 等可读格式，并可选返回坐标、页眉页脚、图片描述等增强信息。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV、AVI、MP3、WAV 等格式，提供人声分离（diarization）、剧情解析（synopsis）、分段（segments）、抽帧（frame extraction）及摘要生成能力。
- **字段抽取**：支持基于 JSON Schema 从已解析文档或原始文件中抽取结构化字段，返回带引用溯源（`citations`）的 `extract_result_json` 和细粒度 `fields` 结果。注意：**抽取不支持直接输入音视频**，仅支持文本类输入（含解析后的文档），详见 [字段解析 API](raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 4 中音视频解析示例未说明其结果能否用于后续抽取——实际复用需确保解析结果为文本型（如 `markdown` 输出），且仍在 7 天保留期内；否则将返回 `ParseResultNotReusable` 错误。

## 关键参数

- **通用必填**：`Authorization` Header（含 `DASHSCOPE_API_KEY`）、`file_url` 或 `parsed_file_biz_id`（二选一）、`biz_id`（查询时必填）。
- **解析任务关键参数**：
  - `processing.doc_processing_config`：控制页码范围（`page_index`）、是否返回坐标（`layout_position`）等；
  - `processing.media_processing_config`：控制人声分离、剧情解析、抽帧模式（`auto`/`frame_rate`）及分辨率；
  - `output.output_file_format`：当前仅支持 `["markdown"]`。
- **抽取任务关键参数**：
  - `processing.extract_processing_config.extract_schema`：必须为合法 JSON 对象（非字符串），定义待抽取字段结构；
  - `processing.extract_processing_config.citation_required`：是否返回引用位置，默认 `true`；
  - `processing.extract_processing_config.allow_inference`：是否允许模型推断缺失字段，默认 `false`。

## 使用方式

1. **认证准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并配置为环境变量或请求 Header；详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析：调用 `/parse/submit`，传入 `file_url` 及可选处理配置，获得 `biz_id`；
   - 抽取：调用 `/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` + `extract_schema`，获得 `biz_id`。
3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `/extract/result`，同上逻辑；
   - 状态为 `processing` 时需重试（建议指数退避），`failed` 时参考错误码定位原因，详见 [错误码](../../raw/application-api-reference/api-overview/errors.md)。
4. **结果消费**：
   - 解析结果通过 `data.output_format_result[].output_file_url` 下载 Markdown；
   - 抽取结果直接在 `data.extract_result_json` 中获取结构化对象，`data.fields` 提供字段级溯源信息。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限，超限将返回 `FileSizeExceeded` 或 `PageCountExceeded`；具体配额以控制台为准，参考 [支持的文件与限制](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)。
- **时效性约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**，否则返回 `ParseResultNotReusable`（见文档 7 警告）。
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库；建议按应用拆分 Key 并定期轮转，详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **错误处理**：`ResultNotReady`（409）表示结果未就绪，应继续轮询；`FileDownloadTimeout`（400）可重试，`FileDownloadFailed`（400）不可重试，需先修复 URL 权限。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


