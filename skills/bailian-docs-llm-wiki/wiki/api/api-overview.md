# api [overview](overview.md)

ParseX API 提供文档与音视频的结构化解析能力，以及基于 Schema 的字段抽取能力。所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 以百炼平台统一鉴权体系为基础，面向企业级文档智能处理场景设计。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出 Markdown、布局信息（`layouts`）、表格、段落、页眉页脚等结构化内容。  
- **音视频解析**：支持 MP4、MOV 等主流格式，输出 ASR 文本、人声分离（`diarization`）、抽帧图像（`frame_extraction`）、剧情解析（`synopsis_parse`/`synopsis_segments`/`synopsis_summary`）等多维结果。  
- **字段抽取**：支持基于 JSON Schema 的结构化信息抽取，可复用已有解析结果（需在 7 天保留期内），返回带引用定位（`citations`）的字段级结果。  
- **双模式任务**：支持在线单文件（低延迟）与离线批量清单（高吞吐）两种提交方式，详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 和 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

> **注意**：字段抽取不支持音视频原始输入（仅支持其解析后的文本或图文结果），该限制在 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md) 的 `UnsupportedFileType` 错误中明确说明；而文档解析明确支持音视频，二者能力边界需严格区分。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `file_url` / `batch_job_url` | 在线单文件 URL 或离线任务清单 URL（JSON 数组），二者二选一 | `"https://example.com/doc.pdf"` |
| `biz_id` | 提交后返回的任务 ID，用于轮询查询结果（`/parse/result` 或 `/extract/result`） | `"parseX-2026xxxx-xxxxxxx"` |
| `processing.*_config` | 内联处理配置，优先级高于 `config_id`。文档解析用 `doc_processing_config`，音视频用 `media_processing_config`，抽取用 `extract_processing_config` | `{ "page_index": "1-10", "head_foot": false }` |
| `output.output_file_format` | 输出格式，当前仅支持 `["markdown"]` | `["markdown"]` |
| `processing.extract_processing_config.extract_schema` | 抽取必需的 JSON Schema 定义，必须为有效 JSON 对象 | `{"properties": {"amount": {"type": "number"}}}` |

## 使用方式

1. **认证**：通过环境变量设置 `DASHSCOPE_API_KEY`，并在每个请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。  
2. **提交任务**：  
   - 解析：`POST /api/v2/apps/parse-x/parse/submit` → 获取 `data.biz_id`（在线）或 `data.biz_id_list`（离线）  
   - 抽取：`POST /api/v2/apps/parse-x/extract/submit` → 同样获取 `biz_id` 或 `biz_id_list`  
3. **轮询结果**：  
   - 解析结果：`POST /api/v2/apps/parse-x/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）  
   - 抽取结果：`POST /api/v2/apps/parse-x/extract/result`，同上逻辑  
4. **CLI 快速验证**：支持 `bl parsex parse submit` 和 `bl parsex extract submit` 命令，详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 限制和注意事项

- **文件限制**：单个文档 ≤ 1.5 万页且 ≤ 1 GB；单张图片 ≤ 20 MB；音视频无明确时长上限，但超大文件可能触发 `ProcessingTimeout`。  
- **批量限制**：离线任务单次最多 200 个子任务；超过则静默丢弃（不报错）。  
- **保留期**：解析结果默认保留 7 天，超期后 `parsed_file_biz_id` 不可复用于抽取（错误码 `ParseResultExpired`）。  
- **OSS 配置**：`oss_config` 参数在 `/parse/submit`、`/parse/result`、`/extract/submit`、`/extract/result` 中均支持，但需确保权限完备，否则返回 `CustomerOssWriteFailed`。  
- **错误重试**：`FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需检查 URL 可访问性。  

> **注意**：文档 4 和文档 5 均声明“单个文档支持 1.5 万页及以内且 1 GB 以内的 PDF、Word 等文档”，但文档 7 的错误码表中 `PageCountExceeded` 未注明具体阈值。实际开发应以 1.5 万页为硬上限，并在捕获该错误时降级处理。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)


