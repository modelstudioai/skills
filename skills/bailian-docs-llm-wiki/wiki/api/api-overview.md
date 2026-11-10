# api overview

ParseX API 提供文档、图片及音视频的结构化解析与字段抽取能力，采用[异步任务](../concepts/asynchronous-task.md)模型。所有接口均需通过 API Key 鉴权，调用流程统一为：提交任务 → 获取 `biz_id` → 轮询查询结果。本页汇总核心能力、参数规范、调用方式及关键约束，适用于快速集成。

## 支持的模型/功能

ParseX API 当前提供两类核心能力：

- **文档解析（Document Parsing）**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）、音视频（MP4/MOV/MP3/WAV）等格式，输出结构化布局（`layouts`）、Markdown 内容、帧图像、ASR 文本、剧情摘要（`synopsis_summary`）及分段（`synopsis_segments`）等。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。
- **字段抽取（Field Extraction）**：基于用户提供的 JSON Schema，从已解析文档或原始文件中抽取结构化字段，支持引用定位（`citations`）与推断（`allow_inference`）。**注意**：抽取不支持直接输入音视频；若复用解析结果，该结果必须在 7 天保留期内且类型匹配 —— 否则将返回 `ParseResultNotReusable` 错误（见 [错误码](../../raw/application-api-reference/api-overview/errors.md)）。

> **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 2 和 4 中音视频解析示例未说明其结果能否用于抽取。经交叉验证，文档 7 的警告具有权威性，且文档 3 中 `UnsupportedFileType` 错误码明确指向抽取场景，因此音视频解析结果**不可用于后续字段抽取**。

## 关键参数

所有提交类接口（`/parse/submit`、`/extract/submit`）均遵循统一参数设计原则：

- **身份与来源**：必填 `file_url` 或 `parsed_file_biz_id`（二选一）；`file_name` 与 `file_name_extension` 亦为二选一，用于辅助类型识别。
- **处理配置**：支持 `config_id`（预设配置）或内联 `processing` 对象（优先级更高）。其中：
  - 解析接口的 `processing` 包含 `doc_processing_config`（文档）或 `media_processing_config`（音视频）；
  - 抽取接口的 `processing` 必须包含 `extract_processing_config`，且其中 `extract_schema` 为必需 JSON 对象（非字符串）—— 文档 7 示例中 `extract_schema` 直接写为对象而非转义字符串，与文档 7 正文描述一致，**文档 7 的代码示例存在误导性**（其 curl 示例中错误地将 `extract_schema` 写作嵌套 JSON 字符串，实际应为原生 JSON 对象）。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于持久化结果至客户 OSS）。

## 使用方式

1. **认证准备**：获取 `DASHSCOPE_API_KEY` 并通过环境变量或 `Authorization: Bearer <key>` Header 传递。详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **异步调用流程**：
   - 提交任务（`POST /parse/submit` 或 `POST /extract/submit`），获得 `biz_id`；
   - 持续轮询 `POST /parse/result` 或 `POST /extract/result`，检查 `data.status`；
   - 状态为 `success` 时读取 `data.output_format_result`（解析）或 `data.extract_result_json`（抽取）；
   - 状态为 `failed` 时，依据 `code` 字段查 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位原因。
3. **CLI 辅助**：支持百炼 CLI 快速验证，命令为 `bl parsex parse submit` / `bl parsex extract submit` 等，详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限，具体配额以控制台为准；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded`（见 [错误码](../../raw/application-api-reference/api-overview/errors.md)）。
- **结果保留期**：解析结果默认保留 30 天（`ParseResultExpired`），但**仅解析结果可复用于抽取的窗口期为 7 天**（文档 7 警告）；超过后调用抽取将失败。
- **重试策略**：`FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需修复 URL 或权限。
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码或提交至仓库；建议按应用分配独立 Key 并定期轮转（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


