# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `DASHSCOPE_API_KEY` 鉴权，请求需携带 `Authorization: Bearer <key>` Header。整体设计面向企业级集成，支持 OSS 输出、自定义处理配置和细粒度错误定位。

## 支持的模型/功能

ParseX API 不暴露底层大模型选型，而是封装为两类垂直能力：

- **文档解析 API**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）及音视频（MP4/MOV/AVI 等）输入，输出结构化布局（`layouts`）、Markdown 内容、剧情分段（`segments`）、摘要（`synopsis_summary`）及抽帧图像等。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **字段解析 API**：支持从图文材料中按 JSON Schema 抽取结构化字段，可复用已有解析结果（`parsed_file_biz_id`），也可直接传入新文件 URL。**注意：抽取不支持音视频原始输入**，仅支持其解析后的文本/布局结果；若复用解析结果，该结果必须在 7 天保留期内且类型匹配，否则返回 `ParseResultNotReusable` 错误 —— 具体限制见 [错误码](raw/application-api-reference/api-overview/errors.md)。

> **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 4 中音视频解析示例未说明其结果能否直接用于抽取。实际调用时，必须先完成音视频解析（获得 `biz_id`），再将该 `biz_id` 作为 `parsed_file_biz_id` 提交抽取任务；不可将音视频 URL 直接传给 `/extract/submit`。

## 关键参数

所有提交接口共用以下基础参数：
- `file_url`（必填，文档/抽取）或 `parsed_file_biz_id`（必填，抽取复用场景）：指定输入源；
- `config_id` 与 `processing`：二者二选一，`processing` 内联配置优先级更高；
- `output.output_file_format`：当前仅支持 `["markdown"]`（文档解析）；
- `output.oss_config`：用于指定结果写入客户自有 OSS，需提供 `bucket`、`endpoint` 及 AK/SK/[Token](../concepts/token.md)。

文档解析特有参数：
- `processing.doc_processing_config.page_index`：页码范围（如 `"1-10"`）；
- `processing.media_processing_config.frame_extraction`：音视频抽帧配置，含 `mode`（`auto`/`frame_rate`）、`frame_rate`（0.2–5）、宽高（32–4096）。

字段抽取特有参数：
- `processing.extract_processing_config.extract_schema`：必需的 JSON Schema 对象，定义待抽取字段结构；
- `processing.extract_processing_config.citation_required`：是否返回引用位置（默认 `true`）；
- `processing.extract_processing_config.allow_inference`：是否允许模型推断缺失字段（默认 `false`）。

## 使用方式

1. **认证准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并设为环境变量 `DASHSCOPE_API_KEY`；所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header —— 具体步骤详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 文档解析：调用 `/parse/submit`，获取 `biz_id`；
   - 字段抽取：调用 `/extract/submit`，获取 `biz_id`（支持 `file_url` 或 `parsed_file_biz_id`）。
3. **轮询结果**：
   - 文档解析：调用 `/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）；
   - 字段抽取：调用 `/extract/result`，同上逻辑。
4. **错误处理**：收到 `ResultNotReady`（HTTP 409）需重试；`FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试 —— 完整错误分类与建议见 [错误码](../../raw/application-api-reference/api-overview/errors.md)。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限；具体数值未在本文档明确列出，但错误码中已定义 `FileSizeExceeded`、`PageCountExceeded`、`PageRangeInvalid` 等触发条件。配额详情请参考 [支持的文件与限制](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)（注：该路径未在原始文档中提供完整内容，开发者需另行查阅）。
- **结果保留期**：
  - 解析结果保留 **30 天**（`ParseResultExpired` 错误码）；
  - 解析结果用于抽取时，仅支持 **7 天内**复用（`ParseResultNotReusable` 错误码）。
- **安全要求**：API Key 具备账号级权限，**严禁硬编码或提交至代码仓库**；推荐按应用拆分 Key 并定期轮转 —— 实践指南见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **异步行为**：所有任务均为异步，无同步阻塞接口；轮询间隔建议 ≥1s，避免高频请求触发限流。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


