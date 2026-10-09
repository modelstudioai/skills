# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过统一的 `Authorization: Bearer <API Key>` 鉴权，支持灵活的处理配置（内联或预存）和 OSS 输出选项。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出 Markdown、布局结构（`layouts`）、段落/表格/图片计数等；可选页眉页脚、坐标定位、图片描述生成 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV 等主流格式，提供 ASR 转录、人声分离（`enable_diarization`）、抽帧（支持 `auto` 或指定 `frame_rate`）、剧情解析（`synopsis_parse`/`synopsis_segments`/`synopsis_summary`）等能力 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于 JSON Schema 从已解析内容或原始文件中抽取结构化字段，支持引用溯源（`citations`）、推断（`allow_inference`）和自定义 Prompt [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：字段抽取不支持直接输入音视频文件，仅支持 `file_url`（文档类）或 `parsed_file_biz_id`（需为文档解析结果）；音视频解析结果不可用于后续抽取任务 [错误码](../../raw/application-api-reference/api-overview/errors.md) 中明确标注 `UnsupportedFileType` 和 `ParseResultNotReusable`。

## 关键参数

- **鉴权**：必须通过 `Authorization: Bearer $DASHSCOPE_API_KEY` Header 传递，API Key 需提前在控制台获取并安全存储 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：所有异步操作依赖 `biz_id`（由 `/submit` 接口返回），用于后续 `/result` 查询。
- **输入源**（二选一）：
  - `file_url`：公开可访问的文件 URL（需确保服务端可直连下载）；
  - `parsed_file_biz_id`：复用已有解析任务 ID（仅限文档解析结果，且须在 7 天保留期内）。
- **处理配置**（二选一）：
  - `config_id`：复用控制台预存的配置；
  - `processing`：内联配置对象，优先级更高，包含 `doc_processing_config`（文档）或 `media_processing_config`（音视频）等子项。
- **输出控制**：`output.oss_config` 支持自定义 OSS 存储，`output.output_file_format` 可指定 `["markdown"]` 等格式。

## 使用方式

1. **准备凭证**：设置环境变量 `DASHSCOPE_API_KEY`，确保其具备对应权限 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 文档/音视频解析 → 调用 `/parse/submit`；
   - 字段抽取 → 调用 `/extract/submit`；
   - 均返回 `data.biz_id`。
3. **轮询结果**：
   - 解析任务 → 调用 `/parse/result`，检查 `data.status`（`init`/`processing`/`success`/`failed`）；
   - 抽取任务 → 调用 `/extract/result`，同上逻辑；
   - 状态为 `processing` 时需重试（建议指数退避），`failed` 时参考错误码排查。
4. **结果消费**：成功响应中，解析结果含 `markdown_content`、`layouts`、`segments` 等；抽取结果含 `extract_result_json` 和带坐标的 `fields[].citations`。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长等受配额约束，具体以控制台实际配额为准；超限返回 `FileSizeExceeded` 或 `PageCountExceeded` 错误 [错误码](../../raw/application-api-reference/api-overview/errors.md)。
- **时效性**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired`）；
  - 复用解析结果进行抽取时，该结果须在 **7 天内**（`ParseResultNotReusable`）。
- **重试策略**：
  - `FileDownloadTimeout` 可重试；
  - `FileDownloadFailed` 不可重试，需修复 URL 或网络条件。
- **安全要求**：API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库；建议按应用拆分 Key 并定期轮转 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)


