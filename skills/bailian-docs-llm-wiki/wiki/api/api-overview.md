# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，采用异步任务模型。所有接口均需通过 API Key 鉴权，调用流程统一为：提交任务 → 轮询结果 → 获取结构化输出。核心能力覆盖 PDF/图片/音视频多模态输入，支持内联配置与预存配置双模式。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出 Markdown、布局信息（`layouts`）、表格、段落、页眉页脚、坐标位置等；支持指定页码范围、抽帧（音视频）、人声分离、剧情解析等高级处理 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV 等主流格式，可生成 ASR 文本、分段音频/视频、关键帧图像、剧情摘要（`synopsis_summary`）、剧情分段（`synopsis_segments`）及视觉描述（`text_info`）[查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)。
- **字段抽取**：支持从已解析文档（`parsed_file_biz_id`）或原始文件 URL 中，按 JSON Schema 抽取结构化字段；支持引用溯源（`citations`）、推断开关（`allow_inference`）和自定义 Prompt [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。
- > **注意**：字段抽取明确不支持音视频直接输入（见文档 7），且复用解析结果时要求其未超 7 天保留期；而文档解析文档（文档 4）中音视频示例表明其原生支持，二者边界清晰，无矛盾。

## 关键参数

| 参数 | 说明 | 示例/约束 |
|------|------|-----------|
| `file_url` / `parsed_file_biz_id` | 二选一：原始文件 URL 或已解析任务 ID | `https://example.com/doc.pdf` 或 `parseX-2026xxxx-xxxxxxx` |
| `processing` | 内联处理配置，优先级高于 `config_id` | 包含 `doc_processing_config`（文档）、`media_processing_config`（音视频）、`extract_processing_config`（抽取）三类子对象 |
| `processing.extract_processing_config.extract_schema` | 抽取必需的 JSON Schema 对象（非字符串） | `{ "type": "object", "properties": { "name": { "type": "string" } } }`（注意：文档 7 示例中误将 `extract_schema` 写为字符串并要求转义，实际应为原生 JSON 对象；以 [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md) 返回结构为准） |
| `output.output_file_format` | 输出格式数组 | `["markdown"]`（仅文档解析支持） |
| `step_start` / `step_size` | 分片查询参数（仅 `/parse/result` 支持） | 默认 `0`，用于分页获取 `layouts` 或 `segments` |

## 使用方式

1. **鉴权**：设置环境变量 `DASHSCOPE_API_KEY`，并在每个请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY` [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，获取 `biz_id`；
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，获取 `biz_id`。
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，同上。
4. **错误处理**：收到 `ResultNotReady`（409）需重试；`FileDownloadTimeout`（400）可重试，`FileDownloadFailed`（400）不可重试；失败时参考 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位原因。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限，具体配额以控制台实时页面为准；`FileSizeExceeded`、`PageCountExceeded`、`PageRangeInvalid` 等错误码对应明确阈值 [错误码](../../raw/application-api-reference/api-overview/errors.md)。
- **保留期**：解析结果默认保留 30 天（`ParseResultExpired`），但字段抽取复用时仅支持 7 天内结果（`ParseResultNotReusable`）。
- **安全实践**：API Key 必须通过环境变量管理，禁止硬编码或提交至仓库；建议按应用分配独立 Key 并定期轮转 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
- **配置优先级**：`processing` 内联配置始终优先生效于 `config_id`，二者同时提供时后者被忽略（所有提交接口均明确说明）。
- > **注意**：文档 7 中“`extract_schema` 是字符串，因此其中的 JSON 需要转义”的表述与实际返回结构（`extract_result_json` 为 object）及 OpenAPI 规范冲突，开发者应直接传入合法 JSON 对象，而非字符串化转义形式。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


