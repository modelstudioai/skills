# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析能力，以及基于 Schema 的字段抽取能力。所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `DASHSCOPE_API_KEY` 鉴权，请求需携带 `Authorization: Bearer <key>` Header。

## 支持的模型/功能

ParseX API 当前提供两类核心能力：

- **文档解析 API**：支持 PDF、Word、PPT、Excel、图片（JPG/PNG）、音视频（MP4/MOV/AVI 等）等多格式输入，输出结构化布局（`layouts`）、Markdown 内容、分段信息（`segments`）、剧情摘要（`synopsis_summary`）等。音视频支持人声分离（diarization）、帧提取、ASR 文本及视觉描述生成。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。

- **字段解析 API**：支持从已解析文档或原始文件中按 JSON Schema 抽取结构化字段，返回带引用溯源（`citations`）的 `extract_result_json`。**注意：抽取不支持直接输入音视频文件**；若复用解析结果，该结果必须在 7 天保留期内且类型匹配（如文档解析结果不可用于音视频抽取）。详见 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档 8 明确警告“抽取不支持音视频输入”，而文档 4 的音视频解析示例中未提及后续抽取限制；实际调用时若对音视频解析结果调用 `/extract/submit`，将返回 `UnsupportedFileType` 错误（见 [错误码](../../raw/application-api-reference/api-overview/errors.md)），请严格遵循输入类型约束。

## 关键参数

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `file_url` / `parsed_file_biz_id` | 请求体 | 是（二选一） | 文件来源：远程 URL 或已存在的解析任务 ID（仅字段抽取支持后者） |
| `biz_id` | 请求体（查询接口） | 是 | `/parse/submit` 或 `/extract/submit` 返回的任务 ID，用于轮询 |
| `processing.*_config` | 请求体 | 否（但内联配置时必填子字段） | 控制解析/抽取行为，如 `doc_processing_config.page_index`、`media_processing_config.enable_synopsis_parse`、`extract_processing_config.extract_schema` |
| `output.output_file_format` | 请求体 | 否 | 指定输出格式，当前仅支持 `["markdown"]`（文档解析） |
| `oss_config` | 请求体（可选） | 否 | 用于指定客户 OSS 存储输出结果，需提供 `bucket`、`endpoint` 及 AK/SK/[Token](../concepts/token.md) |

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并设置为环境变量 `export DASHSCOPE_API_KEY="sk-..."`；所有请求需携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header。详见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。

2. **提交任务**：
   - 文档/音视频解析：调用 `/parse/submit`，传入 `file_url` 及可选处理配置，获得 `biz_id`。
   - 字段抽取：调用 `/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` + `extract_schema`，获得 `biz_id`。

3. **轮询结果**：
   - 解析任务：调用 `/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）。
   - 抽取任务：调用 `/extract/result`，同上逻辑。
   - 收到 `ResultNotReady`（HTTP 409）时应重试；收到 `ProcessingFailed`（HTTP 500）等错误时需结合 [错误码](../../raw/application-api-reference/api-overview/errors.md) 排查。

## 限制和注意事项

- **异步时效性**：任务状态轮询建议间隔 ≥1s；解析结果默认保留 30 天（`ParseResultExpired`），抽取复用的解析结果仅保留 7 天（`ParseResultNotReusable`）。
- **文件限制**：单文件大小、页数、时长等受配额约束，超限将返回 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout` 等错误（见 [错误码](../../raw/application-api-reference/api-overview/errors.md)）。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至公开仓库；推荐按应用拆分 Key 并定期轮转。
- **Schema 与类型约束**：`extract_schema` 必须为合法 JSON 对象；音视频解析结果不可用于字段抽取，否则触发 `UnsupportedFileType`；`file_name` 与 `file_name_extension` 二选一填写，避免冲突。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)


