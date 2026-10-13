# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，采用[异步任务模型](../concepts/asynchronous-tasks.md)。所有接口均需通过 API Key 鉴权，调用流程统一为「提交任务 → 轮询结果」，适用于批量处理和长耗时场景。

## 支持的模型/功能

API 当前支持两类核心能力：

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）及音视频（MP4/MOV/AVI 等）输入，输出结构化布局（`layouts`）、Markdown 内容、分片（`segments`）、剧情摘要（`synopsis_summary`）等。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **字段抽取**：支持从已解析文档或原始文件中，按用户定义的 JSON Schema 抽取结构化字段，返回带引用定位（`citations`）的 `extract_result_json`。注意：**抽取不支持直接输入音视频**，仅支持文本类解析结果或文档 URL；复用解析结果时需确保其未超 7 天保留期且类型匹配。详见 [字段解析 API](raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 4 中音视频解析示例可成功提交并返回 `biz_id`，但该 `biz_id` **不可用于后续抽取任务**。若误将音视频 `biz_id` 传入 `/extract/submit`，将返回 `ParseResultNotReusable` 错误（见 [错误码](raw/application-api-reference/api-overview/errors.md)）。

## 关键参数

所有提交接口共用以下关键参数模式：

- **身份凭证**：必须通过 `Authorization: Bearer $DASHSCOPE_API_KEY` Header 传递，API Key 需提前在控制台获取，详见 [认证](raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：
  - `file_url`（必填或二选一）：待处理文件的公网可访问 URL；
  - `parsed_file_biz_id`（字段抽取专用）：复用已有解析任务 ID，与 `file_url` 互斥；
  - `config_id`（可选）：预存的处理配置 ID；
  - `processing`（可选，高优先级）：内联配置对象，当与 `config_id` 同时存在时覆盖后者。
- **处理配置**（按能力区分）：
  - 文档解析：`processing.doc_processing_config`（页码范围、坐标、页眉页脚等）或 `processing.media_processing_config`（人声分离、抽帧、剧情解析等）；
  - 字段抽取：`processing.extract_processing_config.extract_schema`（必需 JSON 对象，定义字段结构）及 `citation_required`/`allow_inference` 等开关。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于持久化到客户 OSS）。

## 使用方式

1. **鉴权准备**：设置环境变量 `DASHSCOPE_API_KEY`，并在每个请求 Header 中携带 `Authorization`；
2. **提交任务**：
   - 解析任务：调用 `/parse/submit`，获取 `biz_id`；
   - 抽取任务：调用 `/extract/submit`，获取 `biz_id`（支持 `file_url` 或 `parsed_file_biz_id`）；
3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，检查 `data.status`（`success`/`failed`/`processing`），状态为 `processing` 时需重试；
   - 抽取结果：调用 `/extract/result`，同上逻辑；
4. **错误处理**：收到非 `success` 状态时，解析响应中的 `code` 和 `message`，对照 [错误码](raw/application-api-reference/api-overview/errors.md) 定位原因（如 `ResultNotReady` 需重试，`FileDownloadFailed` 需修复 URL）。

## 限制和注意事项

- **配额与超时**：单文件大小、页数、音视频时长等均有硬性限制（如 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout`），具体数值以控制台配额页面为准；
- **保留期约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**（`ParseResultNotReusable` 错误）；
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至代码仓库，推荐使用环境变量 + 定期轮转；
- **异步行为**：所有任务均为异步，无同步阻塞接口；轮询间隔建议 ≥1s，避免高频请求触发限流；
- **OSS 凭证**：若使用 `oss_config`，AccessKey Secret 和 Security Token 属于敏感信息，需严格保密。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


