# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过标准 `Authorization: Bearer <API Key>` 进行鉴权，适用于企业级批量处理场景。完整流程详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出 Markdown、带坐标的布局信息（`layout_position`）、页眉页脚（`head_foot`）、图片描述（`image_caption`）等；  
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（`enable_diarization`）、剧情解析（`enable_synopsis_parse`）、抽帧（`frame_extraction`）及多模态摘要能力；  
- **字段抽取**：支持从已解析文档或原始文件中按 JSON Schema 抽取结构化字段，返回带引用定位（`citations`）和推断状态（`inferred`）的结果；  
- **复用机制**：字段抽取可复用此前文档解析任务生成的 `parsed_file_biz_id`，避免重复解析，但仅限 7 天内有效且不支持音视频源 —— 此限制在 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中明确说明。

> **注意**：文档解析支持音视频，但字段抽取**明确不支持音视频输入**（见 [错误码](../../raw/application-api-reference/api-overview/errors.md) 中 `UnsupportedFileType` 条目），且复用解析结果时若源为音视频，将直接报错 `ParseResultNotReusable`。二者能力边界需严格区分。

## 关键参数

| 参数 | 位置 | 说明 | 示例值 |
|------|------|------|--------|
| `file_url` | 请求体 | 待处理文件的公网可访问 URL（HTTP/HTTPS） | `"https://example.com/report.pdf"` |
| `biz_id` | 请求体（查询接口） | 提交任务后返回的唯一业务 ID，用于轮询 | `"parseX-2026xxxx-xxxxxxx"` |
| `processing.*` | 请求体 | 内联处理配置，优先级高于 `config_id`；文档/音视频/抽取各有专属子结构 | `{"doc_processing_config": {"page_index": "1-5"}}` |
| `output.output_file_format` | 请求体 | 指定输出格式，当前仅支持 `["markdown"]` | `["markdown"]` |
| `oss_config` | 请求体（可选） | 指定客户 OSS 存储输出结果，需提供 `bucket`、`endpoint` 及 AK/SK/[Token](../concepts/token.md) | `{ "bucket": "my-bucket", "endpoint": "oss-cn-beijing.aliyuncs.com", ... }` |

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并设为环境变量或请求 Header；详细步骤见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)；  
2. **提交任务**：  
   - 文档/音视频解析 → 调用 `/api/v2/apps/parse-x/parse/submit`；  
   - 字段抽取 → 调用 `/api/v2/apps/parse-x/extract/submit`（支持 `file_url` 或 `parsed_file_biz_id`）；  
3. **轮询结果**：  
   - 解析结果 → 调用 `/api/v2/apps/parse-x/parse/result`；  
   - 抽取结果 → 调用 `/api/v2/apps/parse-x/extract/result`；  
4. **状态判断**：持续轮询直到 `data.status` 为 `"success"` 或 `"failed"`；若为 `"processing"`，建议间隔 1–3 秒重试（无固定速率限制，但需避免高频刷）。

## 限制和注意事项

- **异步时效性**：文档解析通常在数秒至数分钟内完成（取决于页数/复杂度），音视频解析耗时显著更长（如 1 小时视频可能需 10–30 分钟）；  
- **文件限制**：单文件大小上限为 100 MB，PDF 页数上限为 1000 页（见 [错误码](../../raw/application-api-reference/api-overview/errors.md) 中 `FileSizeExceeded` 和 `PageCountExceeded`）；  
- **保留期约束**：解析结果默认保留 30 天（`ParseResultExpired` 错误码），但字段抽取仅支持复用 **7 天内** 的解析结果；  
- **安全要求**：API Key 必须通过环境变量注入，严禁硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转；  
- **错误处理**：`ResultNotReady`（HTTP 409）表示任务未就绪，应继续轮询；`FileDownloadTimeout` 可重试，`FileDownloadFailed` 则需检查 URL 可访问性。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)


