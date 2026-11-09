# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，请求与响应统一返回 `request_id` 用于问题排查。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPEG）等格式，输出布局结构（`layouts`）、Markdown、表格、段落等；可配置页码范围、页眉页脚、坐标位置、图片描述等 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，输出分段（`segments`）、ASR 文本、人声分离（`diarization`）、剧情解析（`synopsis_parse`）、抽帧及图像描述等 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于用户提供的 JSON Schema，从图文材料中结构化抽取字段，支持引用溯源（`citations`）、推断（`allow_inference`）和复用已有解析结果（`parsed_file_biz_id`）；**不支持音视频直接输入**，详见[错误码](../../raw/application-api-reference/api-overview/errors.md)中 `UnsupportedFileType` 说明。

> **注意**：文档解析与字段抽取虽共享 `biz_id` 命名逻辑，但二者任务类型隔离——`parse/submit` 返回的 `biz_id` 仅可用于 `parse/result`，`extract/submit` 返回的 `biz_id` 仅可用于 `extract/result`。混用将返回 `NotExistBizId` 错误。

## 关键参数

- **必填认证参数**：`Authorization: Bearer $DASHSCOPE_API_KEY`（需提前在控制台获取，详见[认证](../../raw/application-api-reference/api-overview/authentication.md)）。
- **核心业务参数**：
  - `file_url`：公开可访问的文件 URL（HTTPS），需确保服务端可直连下载；
  - `biz_id`：[异步任务](../concepts/asynchronous-task.md)唯一标识，由 `submit` 接口返回，用于后续 `result` 查询；
  - `parsed_file_biz_id`（抽取专用）：复用已有解析结果时传入，须在 7 天保留期内且类型匹配；
  - `processing` 对象：内联处理配置，优先级高于 `config_id`；文档解析含 `doc_processing_config` / `media_processing_config`，字段抽取含 `extract_processing_config`（必须提供 `extract_schema`）；
  - `output.output_file_format`：当前仅支持 `["markdown"]`；
  - `output.oss_config`：用于指定结构化结果的 OSS 输出位置（可选）。

## 使用方式

1. **准备凭证**：设置环境变量 `DASHSCOPE_API_KEY`，并在每个请求 Header 中携带 `Authorization`；
2. **提交任务**：
   - 解析：调用 `POST /api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选配置；
   - 抽取：调用 `POST /api/v2/apps/parse-x/extract/submit`，二选一传入 `file_url` 或 `parsed_file_biz_id`，并提供 `extract_schema`；
3. **轮询结果**：
   - 解析结果：调用 `POST /api/v2/apps/parse-x/parse/result`，传入 `biz_id`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `POST /api/v2/apps/parse-x/extract/result`，传入 `biz_id`，检查 `data.status`；
4. **错误处理**：当 `status` 为 `failed` 时，结合响应中的 `code` 和 `message`，对照[错误码](../../raw/application-api-reference/api-overview/errors.md)定位原因（如 `ResultNotReady` 需重试，`FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试）。

## 限制和注意事项

- **文件限制**：单文件大小上限、页数上限、音视频时长上限以控制台配额为准；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded`；
- **保留期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired`）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**（`ParseResultNotReusable`）；
- **重试策略**：
  - `ResultNotReady`（409）：必须重试，使用原 `biz_id`；
  - `FileDownloadTimeout`（400）：建议重试；
  - `FileDownloadFailed`（400）：不可重试，需修复 URL 或网络可达性；
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至代码仓库；推荐按应用拆分 Key 并定期轮转；
- **Schema 规范**：`extract_schema` 必须为合法 JSON Schema 对象（非字符串），示例中因 curl 转义需要而显示为嵌套 JSON，实际请求体中应为原生对象结构。

## 来源文档

- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)


