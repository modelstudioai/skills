# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，所有接口均采用[异步调用](../concepts/asynchronous-invocation.md)模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，请求地址为 `{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/...`。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落、页眉页脚、坐标信息等；支持指定页码范围、抽帧（音视频）、人声分离、剧情解析与摘要生成。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，可提取 ASR 文本、说话人分离（diarization）、视频分段（segments）、关键帧（frame extraction）、剧情解析（synopsis）及摘要。注意：音视频解析结果中 `segments` 和 `frames` 均按时间戳组织，非页码逻辑。
- **字段抽取**：支持从已解析文档或原始文件中，按 JSON Schema 抽取结构化字段，返回带引用定位（`citations`）的结果；支持复用已有解析任务结果（需在 7 天保留期内），但**不支持直接对音视频输入进行抽取**（见 [错误码](../../raw/application-api-reference/api-overview/errors.md) 中 `UnsupportedFileType`）。该能力依赖解析前置步骤，不可跳过。

> **注意**：文档 8 明确警告“抽取不支持音视频输入”，而文档 5 和文档 2 均未限定抽取输入类型。以文档 8 的明确限制为准，开发者不得向 `/extract/submit` 提交音视频 `file_url`，否则将返回 `400 UnsupportedFileType` 错误。

## 关键参数

- **必填认证参数**：`Authorization: Bearer $DASHSCOPE_API_KEY`（环境变量配置方式见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）。
- **核心业务参数**：
  - `file_url`：公开可访问的文件 URL（HTTP/HTTPS），需确保服务端可直连下载。
  - `biz_id`：所有轮询接口（`/parse/result`, `/extract/result`）的唯一标识符，由对应 `submit` 接口返回。
  - `parsed_file_biz_id`：字段抽取时复用解析结果的专用参数，与 `file_url` 二选一。
- **配置优先级规则**：`processing` 内联对象始终优先生效于 `config_id`（见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 和 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)）。
- **Schema 与处理控制**：
  - 解析：通过 `processing.doc_processing_config` 或 `processing.media_processing_config` 控制行为（如 `page_index`, `enable_diarization`）。
  - 抽取：必须提供 `processing.extract_processing_config.extract_schema`（JSON 对象），且 `citation_required` 和 `allow_inference` 可显式开关。

## 使用方式

1. **鉴权准备**：获取并安全配置 `DASHSCOPE_API_KEY`（推荐环境变量），确保 RAM 子账号已授权对应权限（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）。
2. **发起任务**：
   - 解析：调用 `/parse/submit`，传入 `file_url` + 可选 `processing` 配置 → 获取 `biz_id`。
   - 抽取：调用 `/extract/submit`，二选一传入 `file_url` 或 `parsed_file_biz_id` + 必填 `extract_schema` → 获取 `biz_id`。
3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，传入 `biz_id`，检查 `data.status`（`success`/`failed`/`processing`）；状态为 `processing` 时需重试（建议指数退避）。
   - 抽取结果：调用 `/extract/result`，传入 `biz_id`，检查 `data.status` 并解析 `extract_result_json` 或 `fields` 数组。
4. **CLI 辅助**：开发调试阶段可使用百炼 CLI 快速验证流程（见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)）。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有硬性上限（如 `FileSizeExceeded`, `PageCountExceeded`, `ProcessingTimeout`），具体数值以控制台配额页为准（文档 8 提示参考 [supported-files-and-limits.md](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)）。
- **结果保留期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误码）；
  - 复用解析结果进行抽取时，该结果须在 **7 天内**（`ParseResultNotReusable` 错误码）。
- **错误处理**：
  - `ResultNotReady`（HTTP 409）：任务未完成，应继续轮询；
  - `FileDownloadFailed`（HTTP 400）：不可重试，需检查 URL 权限或有效性；
  - `FileDownloadTimeout`（HTTP 400）：可重试；
  - 所有错误响应均含 `request_id` 和 `code`，用于问题定位（见 [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)）。
- **安全实践**：API Key 严禁硬编码或提交至代码仓库；建议按应用拆分 Key 并定期轮转（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)


