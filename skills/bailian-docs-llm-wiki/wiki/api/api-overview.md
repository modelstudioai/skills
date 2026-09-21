# api [overview](../guides/overview.md)

ParseX API 提供文档、图片及音视频的结构化解析与字段抽取能力，采用异步任务模型。所有接口均需通过 API Key 鉴权，调用流程统一为：提交任务 → 获取 `biz_id` → 轮询查询结果。本概览整合核心能力、参数规范、调用路径及关键约束，面向开发者快速上手。

## 支持的模型/功能

ParseX API 当前提供两类核心能力：

- **文档解析（Document Parsing）**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）、音视频（MP4/MOV/AVI 等）输入，输出结构化布局（`layouts`）、Markdown 内容、分段信息（`segments`）、剧情摘要（`synopsis_summary`）及抽帧图像等。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **字段抽取（Field Extraction）**：基于 JSON Schema 从图文材料中抽取指定字段，支持直接传入文件 URL 或复用已有解析任务的 `parsed_file_biz_id`，返回带引用溯源（`citations`）和推断标记（`inferred`）的结构化结果。详见 [字段解析 API](raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：字段抽取明确不支持音视频作为原始输入（见 [提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md)），且复用解析结果时要求其未超过 7 天保留期；而文档解析本身支持音视频，但其产出的 `parsed_file_biz_id` 仅在满足类型兼容性前提下才可用于后续抽取——该限制在 [错误码](raw/application-api-reference/api-overview/errors.md) 中通过 `ParseResultNotReusable` 明确体现，需开发者主动校验。

## 关键参数

所有请求共用以下基础参数与鉴权机制：

- **鉴权**：必须在 `Authorization: Bearer <API_KEY>` Header 中携带 `DASHSCOPE_API_KEY`，该密钥需通过百炼控制台获取并安全保管，详见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：`biz_id` 是所有异步操作的核心 ID，由 `/parse/submit` 或 `/extract/submit` 返回，后续轮询 `/parse/result` 或 `/extract/result` 均需传入。
- **输入源（二选一）**：
  - `file_url`：公开可访问的文件 URL（支持 HTTP/HTTPS/OSS）；
  - `parsed_file_biz_id`：仅字段抽取支持，用于复用已解析结果（需确保其有效且类型匹配）。
- **处理配置**：
  - 可复用预存 `config_id`，或使用内联 `processing` 对象（优先级更高）；
  - 文档解析支持 `doc_processing_config`（页码范围、坐标、图片描述等）和 `media_processing_config`（人声分离、剧情解析、抽帧等）；
  - 字段抽取必须提供 `extract_processing_config.extract_schema`（JSON Schema 对象）及可选 `citation_required` / `allow_inference`。
- **输出控制**：支持 `output_file_format`（如 `["markdown"]`）、OSS 回写（需完整 `oss_config` 凭据）等。

## 使用方式

标准调用流程为三步异步模式：

1. **提交任务**：  
   - 文档解析：调用 `POST /api/v2/apps/parse-x/parse/submit`，传入 `file_url` 或音视频 URL 及可选配置，获取 `biz_id`。示例见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。  
   - 字段抽取：调用 `POST /api/v2/apps/parse-x/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`，获取 `biz_id`。示例见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

2. **轮询结果**：  
   - 持续调用 `POST /api/v2/apps/parse-x/parse/result` 或 `POST /api/v2/apps/parse-x/extract/result`，传入 `biz_id`；  
   - 检查响应中 `data.status`：`init`/`processing` 时继续轮询（建议指数退避），`success` 或 `failed` 时终止；  
   - `failed` 时需结合 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位原因（如 `ResultNotReady` 表示未就绪，`ParseResultNotReusable` 表示解析结果不可复用）。

3. **解析响应**：  
   - 成功时，文档解析返回 `markdown_content`、`layouts`、`segments` 等；字段抽取返回 `extract_result_json` 和带坐标的 `fields.citations`。

## 限制和注意事项

- **配额与容量**：  
  - 单文件大小、页数、音视频时长均有硬性限制（如 `FileSizeExceeded`、`PageCountExceeded`、`FileDownloadTimeout`），具体数值以控制台配额为准；  
  - 解析结果默认保留 30 天（`ParseResultExpired`），抽取复用的解析结果仅保留 7 天（`ParseResultNotReusable`）。

- **安全与合规**：  
  - API Key 具有账号级权限，**严禁硬编码或提交至代码仓库**，必须通过环境变量管理；建议按应用拆分 Key 并定期轮转（见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)）；  
  - OSS 凭据（`access_key_id`/`access_key_secret`）若用于输出，同样需安全传递，避免泄露。

- **错误处理**：  
  - 所有错误均返回标准结构：`request_id`（用于工单追踪）、`code`（如 `NotExistBizId`）、`message`；  
  - `FileDownloadFailed` 不可重试，`FileDownloadTimeout` 可重试；`ResultNotReady` 必须轮询，不可直接重提任务；  
  - 字段抽取中 `InvalidSchema` 表示 Schema 格式非法，需校验 JSON 结构及类型定义。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


