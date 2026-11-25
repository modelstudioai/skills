# api [overview](overview.md)

ParseX API 是百炼平台提供的文档与音视频智能解析及结构化信息抽取服务，采用异步任务模型。开发者通过提交任务获取 `biz_id`，再轮询查询结果，支持文档、图片、音视频的多模态解析，以及基于 JSON Schema 的字段级结构化抽取。所有请求均需通过 API Key 鉴权。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、TXT、图片（JPG/PNG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落等；支持页码范围控制、页眉页脚识别、坐标定位、图片描述生成等高级配置。详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（diarization）、剧情解析（synopsis）、分段摘要、关键帧抽取（含自定义分辨率与帧率）等功能。
- **字段抽取**：支持基于 JSON Schema 从已解析文档或原始文件中抽取结构化字段，返回带引用溯源（`citations`）的 `extract_result_json` 和细粒度 `fields` 结果；**不支持直接对音视频输入进行抽取**（见 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md) 中 `UnsupportedFileType` 错误说明）。
- > **注意**：文档 5 明确指出“抽取不支持音视频输入”，而文档 7 未作此限制说明，存在表述不一致；以文档 5 及错误码文档为准。

## 关键参数

- **必填参数**：
  - `file_url`（解析/抽取）或 `parsed_file_biz_id`（抽取，二选一）
  - `biz_id`（查询结果时必填）
- **核心可选参数**：
  - `config_id`：复用控制台预设的解析/抽取配置
  - `processing`：内联配置对象，优先级高于 `config_id`，包含：
    - `doc_processing_config`（文档）或 `media_processing_config`（音视频）或 `extract_processing_config`（抽取）
    - `user_prompt`：支持自定义提示词引导处理行为
    - `extract_schema`（抽取必需）：JSON Schema 定义目标字段结构，类型需严格匹配（见 [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md) 返回示例）
  - `output`：控制输出格式（如 `["markdown"]`）及 OSS 托管配置
- **分片查询参数**（仅 `/parse/result`）：
  - `step_start` / `step_size`：用于分页拉取 `layouts` 或 `segments`，避免单次响应过大

## 使用方式

1. **认证准备**：获取 `DASHSCOPE_API_KEY` 并通过环境变量或 Header 传递（`Authorization: Bearer <key>`），详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，返回 `biz_id`
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，返回 `biz_id`
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，同上逻辑
4. **CLI 辅助**：支持百炼 CLI 快速验证流程（如 `bl parsex parse submit`），详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 限制和注意事项

- **异步时效性**：任务状态为 `processing` 时需主动轮询，无 Webhook 回调机制；建议间隔 ≥1s 重试，避免高频请求。
- **文件限制**：
  - 文件 URL 必须公网可访问且鉴权开放（如 OSS 公共读或带签名 URL）
  - 不支持本地文件直传；需先上传至可公开访问的存储服务
  - 单文件大小、页数、时长等硬性限制见错误码文档（如 `FileSizeExceeded`、`PageCountExceeded`）
- **生命周期约束**：
  - 解析结果默认保留 **30 天**（错误码 `ParseResultExpired`），但抽取任务复用时仅支持 **7 天内**的 `parsed_file_biz_id`（见文档 5 警告）
- **安全要求**：
  - API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库
  - OSS 凭据（`access_key_id` 等）若在请求体中透传，需确保传输链路加密（HTTPS）且服务端不落盘
- > **注意**：文档 3 和文档 5 均声明“调用前请确保已获取 API Key，详见[鉴权](../authentication.md)”，但实际路径应为 `../../raw/...`；此处已按规范统一修正为两级回溯引用。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


