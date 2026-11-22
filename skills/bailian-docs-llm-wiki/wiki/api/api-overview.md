# api [overview](overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用[异步任务](../concepts/asynchronous-task.md)模型：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，请求需指向工作空间专属域名（如 `{workspaceId}.cn-beijing.maas.aliyuncs.com`）。完整调用流程详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出布局结构（`layouts`）、Markdown、表格、段落等；可配置页码范围、是否解析页眉页脚、坐标定位、图片描述等。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，输出 ASR 文本、人声分离（`diarization`）、剧情解析（`synopsis_parse`）、抽帧（支持 `auto` 或指定 `frame_rate`）及帧描述。
- **字段抽取**：基于用户提供的 JSON Schema，从解析结果或原始文件中抽取结构化字段；支持引用溯源（`citations`）、推断开关（`allow_inference`）和置信度标注（`status: found/miss/inferred`）。
- **复用机制**：抽取任务可复用已有解析结果（通过 `parsed_file_biz_id`），但仅限 7 天内且类型匹配（[错误码文档](../../raw/application-api-reference/api-overview/errors.md) 明确列出 `ParseResultNotReusable` 等限制条件）。

> **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 4 中音视频解析示例未提及抽取能力，二者一致；但文档 2 的错误码表中 `UnsupportedFileType` 说明为“Extract does not [support](../guides/support.md) audio/video input”，与文档 7 完全吻合，确认该限制有效。

## 关键参数

| 参数类别 | 关键参数 | 说明 |
|----------|----------|------|
| **通用鉴权** | `Authorization: Bearer $DASHSCOPE_API_KEY` | 必须通过 Header 传递，API Key 由百炼控制台获取，详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。 |
| **任务标识** | `biz_id` | 所有[异步任务](../concepts/asynchronous-task.md)的核心 ID，由 `/parse/submit` 或 `/extract/submit` 返回，用于后续 `/parse/result` 或 `/extract/result` 查询。 |
| **输入源** | `file_url` / `parsed_file_biz_id` | 二选一：直接传文件 URL，或复用已存在的解析任务 ID（后者需在 7 天保留期内）。 |
| **处理配置** | `processing.*_config` | 支持 `doc_processing_config`（文档）、`media_processing_config`（音视频）、`extract_processing_config`（抽取）三类内联配置，优先级高于 `config_id`。 |
| **Schema 定义** | `processing.extract_processing_config.extract_schema` | 字段抽取必需，为 JSON 对象（非字符串），文档 7 示例中误写为“`extract_schema` 是字符串，因此其中的 JSON 需要转义”，**实际应为原生 JSON 对象**（见文档 7 curl 示例中未转义的 `{"type": "object", ...}` 结构），该处为文档错误。 |
| **输出控制** | `output.output_file_format`, `output.oss_config` | 指定 Markdown 输出、或配置 OSS 直接落库；OSS 凭据可随请求传入，也可预授权。 |

## 使用方式

1. **准备凭证**：按 [认证](../../raw/application-api-reference/api-overview/authentication.md) 获取并安全配置 `DASHSCOPE_API_KEY`；
2. **提交任务**：
   - 解析任务：调用 `/api/v2/apps/parse-x/parse/submit`，传 `file_url` 及可选 `processing` 配置；
   - 抽取任务：调用 `/api/v2/apps/parse-x/extract/submit`，传 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`；
3. **轮询结果**：使用返回的 `biz_id` 调用对应 `/result` 接口，检查 `data.status`（`init` → `processing` → `success`/`failed`）；
4. **处理响应**：成功时解析 `data.output_format_result`（解析）或 `data.extract_result_json`（抽取）；失败时依据 `code` 查 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)。

CLI 用户可使用 `bl parsex parse submit` / `bl parsex extract submit` 等命令替代 HTTP 调用，详见各 API 概览页说明。

## 限制和注意事项

- **配额与超限**：文件大小、页数、音视频时长、帧数等均有硬性限制（如 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout`），具体数值以控制台配额页面为准，文档 7 提示“公开配额以正式页面为准”；
- **保留期约束**：解析结果默认保留 30 天（`ParseResultExpired`），但复用解析结果进行抽取仅限 7 天内（`ParseResultNotReusable`）；
- **重试策略**：`FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试；`ResultNotReady` 需持续轮询，非错误；
- **安全红线**：API Key 具备账号级权限，严禁硬编码、提交至仓库或明文日志；建议按应用拆分 Key 并定期轮转；
- **异步模型**：所有任务均为异步，无同步阻塞接口；轮询间隔建议 ≥1s，避免高频请求触发限流（`ServiceQuotaExhausted`）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


