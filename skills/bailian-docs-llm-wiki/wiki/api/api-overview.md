# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，请求地址为 `{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/...`。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出 Markdown、布局信息（`layouts`）、表格、段落、页眉页脚、坐标位置等；支持指定页码范围、禁用页眉页脚、生成图片描述等配置。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（Diarization）、剧情解析（Synopsis）、分段（Segments）、摘要（Summary）、抽帧（Frame Extraction）等能力，可返回 ASR 文本、视频帧及语义描述。详见 [提交解析任务](raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：支持从已解析文档或原始文件中按 JSON Schema 抽取结构化字段，返回带引用溯源（`citations`）的 `extract_result_json`，支持推断（`allow_inference`）和引用标记（`citation_required`）。> **注意**：抽取不支持直接输入音视频，仅支持文档类输入或复用解析结果；且复用的 `parsed_file_biz_id` 必须在 7 天保留期内，否则返回 `ParseResultNotReusable` 错误 —— 这一限制在 [提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中明确说明，但 [错误码](raw/application-api-reference/api-overview/errors.md) 文档中将过期阈值标为“7 天”，而另一处提及“解析结果已过期，超过 30 天保留期”（`ParseResultExpired`），此处以 7 天为准，因字段抽取复用场景明确依赖该时效约束。

## 关键参数

- **通用必填**：`biz_id`（用于结果查询）、`file_url` 或 `parsed_file_biz_id`（二选一）、`Authorization` Header。
- **解析任务关键参数**：
  - `processing.doc_processing_config.page_index`：如 `"1-10"`，控制解析页数；
  - `processing.media_processing_config.enable_diarization`：启用说话人分离；
  - `output.output_file_format`：指定 `["markdown"]` 等输出格式。
- **抽取任务关键参数**：
  - `processing.extract_processing_config.extract_schema`：内联 JSON Schema，必须为合法对象（非字符串）；
  - `processing.extract_processing_config.citation_required`：是否返回引用位置（默认 `true`）；
  - `processing.extract_processing_config.allow_inference`：是否允许模型推断缺失字段（默认 `false`）。
- **OSS 输出**：所有提交接口均支持 `output.oss_config`，用于指定客户自有 OSS 存储结果，需提供 `bucket`、`endpoint`、`access_key_id` 等完整凭证。

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并设为环境变量或显式传入 `Authorization` Header —— 具体流程见 [鉴权](raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析：调用 `/parse/submit`，传入 `file_url` 及可选 `processing` 配置，获得 `biz_id`；
   - 抽取：调用 `/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` + `extract_schema`，获得 `biz_id`。
3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，检查 `data.status`（`success`/`failed`/`processing`），状态为 `processing` 时需重试；
   - 抽取结果：调用 `/extract/result`，解析 `data.extract_result_json` 或细粒度 `data.fields` 字段。
4. **错误处理**：收到非 `2xx` 响应时，解析响应体中的 `code` 和 `message`，对照 [错误码](raw/application-api-reference/api-overview/errors.md) 定位原因；例如 `ResultNotReady` 需继续轮询，`FileDownloadTimeout` 可重试，`FileSizeExceeded` 需压缩文件。

## 限制和注意事项

- **文件限制**：单文件大小、页数、音视频时长均有上限，具体配额以控制台实际配置为准；`FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout` 等错误码直接反映此类硬性限制。
- **时效性约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误码对应此周期）；
  - 但**字段抽取仅支持复用 7 天内的解析结果**（`ParseResultNotReusable` 错误码说明），二者存在差异，开发者需按场景区分使用。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；建议按应用拆分 Key 并定期轮转 —— 相关实践详见 [鉴权](raw/application-api-reference/api-overview/authentication.md)。
- **配置优先级**：`config_id` 与内联 `processing` 同时提供时，`processing` 永远优先生效，此规则在 [提交解析任务](raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 和 [提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中一致确认。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


