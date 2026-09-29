# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过标准 `Authorization: Bearer <API Key>` 鉴权，适用于自动化集成场景。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出 Markdown、布局信息（`layouts`）、表格、段落、页眉页脚、坐标位置等；支持指定页码范围、图像描述生成等高级配置。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流视频格式及音频文件，提供人声分离（diarization）、剧情解析（synopsis）、分段（segments）、摘要（summary）、抽帧（frame extraction）等功能。
- **字段抽取**：支持从已解析文档或原始文件中按 JSON Schema 抽取结构化字段，返回带引用溯源（`citations`）的 `extract_result_json` 和细粒度字段级结果（`fields`）。注意：**抽取不支持直接输入音视频**，仅支持文本类输入（含解析后的文档），详见 [字段解析 API](raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 4 中音视频解析示例未提及抽取复用限制；二者无直接冲突，但需严格遵循文档 7 的约束——音视频必须先完成解析，再以 `parsed_file_biz_id` 形式提交抽取，且该解析结果须在 7 天保留期内。

## 关键参数

- **通用必填**：`biz_id`（用于结果查询）、`file_url` 或 `parsed_file_biz_id`（二选一）、`Authorization` Header。
- **解析任务关键参数**：
  - `processing.doc_processing_config`：控制文档解析行为（如 `page_index`, `head_foot`, `layout_position`）；
  - `processing.media_processing_config`：控制音视频解析行为（如 `enable_diarization`, `frame_extraction.mode`）；
  - `output.output_file_format`：指定输出格式（当前仅支持 `["markdown"]`）。
- **抽取任务关键参数**：
  - `processing.extract_processing_config.extract_schema`：必需的 JSON Schema 对象，定义待抽取字段结构；
  - `processing.extract_processing_config.citation_required`：是否返回引用位置（默认 `true`）；
  - `processing.extract_processing_config.allow_inference`：是否允许模型推断缺失字段（默认 `false`）。

## 使用方式

1. **鉴权准备**：获取 `DASHSCOPE_API_KEY` 并设为环境变量，请求头携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。详细流程见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析任务：调用 `/parse/submit`，传入 `file_url` 及可选处理配置，获得 `biz_id`；
   - 抽取任务：调用 `/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` + `extract_schema`，获得 `biz_id`。
3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，检查 `data.status`（`success`/`failed`/`processing`），状态为 `processing` 时需重试；
   - 抽取结果：调用 `/extract/result`，同理轮询直至 `success` 或 `failed`。
4. **错误处理**：收到 `ResultNotReady`（409）需继续轮询；`FileDownloadTimeout`（400）可重试，`FileDownloadFailed`（400）不可重试。完整错误码说明见 [错误码](../../raw/application-api-reference/api-overview/errors.md)。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限，具体数值以控制台配额为准；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded` 错误。
- **保留期限制**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误码）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**，否则返回 `ParseResultNotReusable`。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；建议按应用拆分 Key 并定期轮转。参见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md) 中的安全建议。
- **配置优先级**：当 `config_id` 与内联 `processing` 同时存在时，`processing` 始终优先生效（文档 4 和文档 7 均明确说明）。
- **OSS 输出**：若使用 `output.oss_config`，需确保提供的 AccessKey 具备对应 Bucket 的写入权限，否则返回 `CustomerOssWriteFailed`。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


