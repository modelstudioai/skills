# api [overview](overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过标准 `Authorization: Bearer <API Key>` 鉴权，支持 RESTful HTTP 调用及百炼 CLI 工具集成。

## 支持的模型/功能

ParseX API 当前提供两类独立但可组合的功能：

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）、音视频（MP4/MOV/AVI 等）等格式，输出结构化布局（`layouts`）、Markdown 内容、ASR 文本、帧图像、剧情摘要（`synopsis_summary`）及分段（`synopsis_segments`）等。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **字段抽取**：基于用户提供的 JSON Schema，从已解析文档或原始文件中抽取结构化字段，并返回带引用定位（`citations`）的结果。**不支持直接对音视频进行抽取**，仅支持文档类输入或复用解析任务生成的 `parsed_file_biz_id`。详见 [字段解析 API](raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档 8 明确警告“抽取不支持音视频输入”，而文档 3 和文档 5 均指出解析支持音视频；二者功能边界清晰，无矛盾。但需注意：复用解析结果进行抽取时，该结果必须在 **7 天保留期内**（文档 8），而解析结果本身保留期为 **30 天**（文档 2 中 `ParseResultExpired` 错误码说明）。此差异属设计使然，非文档错误。

## 关键参数

所有请求共用以下基础参数：

- `Authorization` Header：必填，格式为 `Bearer $DASHSCOPE_API_KEY`，凭证获取方式见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- `biz_id`：所有结果查询接口（`/parse/result`, `/extract/result`）的必填路径/请求体参数，由对应提交接口返回。

核心业务参数按功能区分：

- **解析提交**（`/parse/submit`）：
  - `file_url`（必填）：可公开访问的文件 URL。
  - `processing.doc_processing_config` / `processing.media_processing_config`：分别控制文档与音视频的解析行为（如页码范围、抽帧模式、剧情解析开关等），详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
  - `output.output_file_format`：当前仅支持 `["markdown"]`。

- **抽取提交**（`/extract/submit`）：
  - 输入二选一：`file_url`（原始文件） 或 `parsed_file_biz_id`（复用解析结果）。
  - `processing.extract_processing_config.extract_schema`：必填（当使用内联配置时），为合法 JSON Schema 对象，定义待抽取字段结构。
  - `processing.extract_processing_config.citation_required`：是否返回引用位置信息（默认 `true`）。

## 使用方式

完整调用流程为 **提交 → 轮询 → 获取结果**，所有任务均为异步：

1. **提交任务**：调用 `/parse/submit` 或 `/extract/submit`，传入必要参数，获得 `data.biz_id`。
2. **轮询状态**：以 `biz_id` 为参数，周期性调用 `/parse/result` 或 `/extract/result`。响应中 `data.status` 为 `processing` 时需继续轮询；为 `success` 或 `failed` 时终止。
3. **处理结果**：
   - 解析成功时，重点关注 `data.output_format_result[].output_file_url`（如 Markdown 下载地址）或 `data.segments`/`data.synopsis_result`（音视频）。
   - 抽取成功时，解析 `data.extract_result_json`（结构化结果）和 `data.fields`（含引用定位的细粒度字段）。

CLI 用户可使用 `bl parsex parse submit` / `bl parsex extract submit` 及对应 `result` 命令替代 HTTP 调用，详见 [使用 CLI](raw/application-user-guide/agent-context/getting-started-overview/integration-overview/cli.md)。

## 限制和注意事项

- **配额与计费**：服务受账号级配额约束，超限将返回 `ServiceQuotaExhausted`（503）错误；欠费将触发 `AccountOverdue`（403）；详情参见 [错误码](../../raw/application-api-reference/api-overview/errors.md)。
- **文件限制**：
  - 单文件大小、页数、音视频时长均有上限，具体数值以控制台实时配额为准；
  - 不支持格式返回 `FileFormatNotSupported`（400）；超限返回 `FileSizeExceeded` 或 `PageCountExceeded`（400）。
- **复用限制**：
  - 抽取任务复用解析结果时，`parsed_file_biz_id` 必须在 **7 天内**且类型匹配，否则返回 `ParseResultNotReusable`（400）；
  - 解析结果本身保留 **30 天**，过期后查询返回 `ParseResultExpired`（400）。
- **安全要求**：API Key 必须通过环境变量（如 `DASHSCOPE_API_KEY`）注入，**严禁硬编码或提交至代码仓库**，详见 [认证](../../raw/application-api-reference/api-overview/authentication.md) 中的安全建议。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)


