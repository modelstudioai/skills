# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过标准 `Authorization: Bearer <API Key>` 鉴权，适用于自动化集成场景。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPEG）等格式，输出结构化布局（`layouts`）、Markdown 内容、表格/段落/页数统计等；支持页码范围指定、页眉页脚控制、坐标返回、图片描述生成等功能。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV 等主流音视频格式，提供人声分离（diarization）、剧情解析（synopsis）、分段（segments）、摘要（summary）及智能抽帧（frame extraction）能力。
- **字段抽取**：支持基于 JSON Schema 从图文材料中结构化抽取字段，返回带引用定位（`citations`）和置信状态（`found`/`miss`/`inferred`）的结果；支持复用已有解析任务结果（需在 7 天保留期内），但**不支持直接对音视频文件进行抽取**（见 [错误码](../../raw/application-api-reference/api-overview/errors.md) 中 `UnsupportedFileType` 说明）。

> **注意**：文档解析与字段抽取虽共享 `biz_id` 命名空间和异步流程，但属于独立服务通道（`/parse/submit` vs `/extract/submit`），不可混用 `biz_id` 查询结果。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `file_url` | 请求体 | 待处理文件的可公开访问 URL（HTTP/HTTPS），必须可被服务端直连下载 | `"https://example.com/doc.pdf"` |
| `biz_id` | 请求体（查询接口） | 提交任务后返回的唯一业务 ID，用于轮询状态和获取结果 | `"parseX-2026xxxx-xxxxxxx"` |
| `processing` | 请求体（内联配置） | 优先级高于 `config_id`，用于定义解析或抽取行为；文档解析含 `doc_processing_config`/`media_processing_config`，字段抽取含 `extract_processing_config` | 见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 和 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `extract_schema` | `processing.extract_processing_config` 内 | 字段抽取必需的 JSON Schema 对象（非字符串），定义期望输出的字段名、类型及嵌套结构 | `{ "type": "object", "properties": { "total_amount": { "type": "number" } } }` |

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并设置为环境变量或请求 Header；详见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 文档/音视频解析：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选 `processing` 配置；
   - 字段抽取：调用 `/api/v2/apps/parse-x/extract/submit`，二选一提供 `file_url` 或已存在的 `parsed_file_biz_id`，并指定 `extract_schema`。
3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，检查 `data.status`（`init` → `processing` → `success`/`failed`）；
   - 抽取结果：调用 `/extract/result`，同上逻辑；
   - 状态为 `processing` 时建议指数退避重试（如 1s → 2s → 4s）。

## 限制和注意事项

- **文件限制**：单文件大小上限、页数上限、音视频时长上限等由配额控制；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded` 错误（见 [错误码](../../raw/application-api-reference/api-overview/errors.md)）。
- **保留期约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 复用解析结果进行字段抽取时，该结果须在 **7 天内**（`ParseResultNotReusable` 错误）。
- **安全要求**：API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库；建议为不同应用分配独立 Key 以便审计与轮转。
- **错误处理**：所有失败响应均含 `request_id` 和 `code`，应结合 [错误码](../../raw/application-api-reference/api-overview/errors.md) 文档定位原因；例如 `ResultNotReady` 表示需继续轮询，`FileDownloadTimeout` 可重试，而 `FileDownloadFailed` 需人工干预源文件。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)


