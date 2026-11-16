# api overview

ParseX API 提供文档与音视频的结构化解析及字段级信息抽取能力，采用异步任务模型：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均需通过 API Key 鉴权，支持文件 URL 直接输入或复用已解析结果（需在有效期内）。整体流程清晰、参数可组合，适用于自动化文档处理与智能数据提取场景。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出布局结构（`layouts`）、Markdown、表格等内容；支持页码范围控制、页眉页脚开关、坐标返回、图片描述生成等配置。详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（`enable_diarization`）、剧情解析（`enable_synopsis_parse`）、分段摘要（`enable_synopsis_segments`/`enable_synopsis_summary`）及智能抽帧（支持 `auto` 或 `frame_rate` 模式）等功能。
- **字段抽取**：基于 JSON Schema 从解析结果或原始文档中抽取结构化字段，支持引用定位（`citations`）、推断开关（`allow_inference`）和置信度标注（`status: found/miss/inferred`）。注意：**抽取不支持音视频输入**，且仅接受图文类解析结果复用 —— 此限制在 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中明确说明。
- > **注意**：文档 6 明确指出“抽取不支持音视频输入”，但文档 3 和文档 8 的概述性描述未强调该限制，易造成误解。开发者应以 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 的具体约束为准。

## 关键参数

- **通用必填**：`Authorization: Bearer $DASHSCOPE_API_KEY`（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)），`biz_id`（用于结果查询）。
- **解析任务**：
  - `file_url`（必填）：可公开访问的文件 URL；
  - `processing.doc_processing_config` / `processing.media_processing_config`：内联配置对象，优先级高于 `config_id`；
  - `output.output_file_format`：当前仅支持 `["markdown"]`；
  - `output.oss_config`：用于指定自定义 OSS 存储输出结果。
- **抽取任务**：
  - 输入二选一：`file_url`（原始文件）或 `parsed_file_biz_id`（复用解析结果）；
  - `processing.extract_processing_config.extract_schema`：必需的 JSON Schema 对象（非字符串），定义待抽取字段结构；
  - `processing.extract_processing_config.citation_required`：是否返回原文引用位置（默认 `true`）。
- **结果查询**：`step_start`/`step_size` 用于分片拉取 `layouts`（文档）或 `segments`（音视频），`parse-result.md` 和 `extract-result.md` 均支持该机制。

## 使用方式

1. **鉴权准备**：获取 `DASHSCOPE_API_KEY` 并设为环境变量（如 `export DASHSCOPE_API_KEY="sk-..."`），所有请求需携带 `Authorization` Header —— 具体步骤见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，获取 `biz_id`；
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，获取 `biz_id`（支持复用解析结果）。
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`processing` → 继续轮询；`success`/`failed` → 停止）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，同上逻辑。
4. **CLI 快速验证**：支持百炼 CLI 命令（如 `bl parsex parse submit`），详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限；`FileSizeExceeded`、`PageCountExceeded`、`PageRangeInvalid` 等错误码在 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md) 中明确定义。
- **保留期约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**（`ParseResultNotReusable` 错误）。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至代码仓库；建议按应用拆分 Key 并定期轮转 —— 相关最佳实践见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **重试策略**：`FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需先修复 URL 或访问权限。
- > **注意**：文档 6 提到“Schema 规模和长文档页数仅按工程设计边界规划，公开配额以正式页面为准”，但未给出具体数值。实际使用中应结合 [支持的文件与限制](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)（该路径未在原始文档中提供完整内容）并监控 `ServiceQuotaExhausted` 等配额错误。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)


