# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，全部采用[异步任务](../concepts/asynchronous-task.md)模式。开发者需先提交任务获取 `biz_id`，再轮询查询结果；所有请求均需通过 API Key 鉴权。整体流程清晰、职责分离，适用于构建自动化文档处理流水线。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPEG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落等；支持页码范围控制、页眉页脚开关、坐标返回、图片描述生成等功能 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流音视频格式，提供人声分离（Diarization）、ASR 转录、帧提取、剧情解析（`synopsis_parse`）、分段摘要（`synopsis_segments`/`synopsis_summary`）等能力 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于 JSON Schema 从已解析内容或原始文件中抽取结构化字段，支持引用定位（`citations`）、推断开关（`allow_inference`）和结果溯源；**不支持直接对音视频输入进行抽取**，仅接受 `parsed_file_biz_id` 或文档 URL [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档 6 明确指出“抽取不支持音视频输入”，而文档 2 和 3 中音视频解析能力完整，二者无冲突；但需注意字段抽取必须依赖前置解析任务（且该解析结果须在 7 天保留期内），不可跳过解析直接对音视频调用抽取接口。

## 关键参数

- **通用必填**：`biz_id`（用于结果查询）、`Authorization: Bearer $DASHSCOPE_API_KEY`（鉴权）。
- **解析任务提交**（`/parse/submit`）：
  - 必填：`file_url`
  - 二选一：`file_name` 或 `file_name_extension`
  - 配置优先级：内联 `processing` > `config_id`
  - 音视频特有：`media_processing_config` 下的 `enable_diarization`、`frame_extraction` 等
- **抽取任务提交**（`/extract/submit`）：
  - 文件来源二选一：`file_url` 或 `parsed_file_biz_id`（后者需确保未过期且类型匹配）
  - Schema 定义：必须通过 `processing.extract_processing_config.extract_schema`（内联）或 `config_id` 提供
- **结果查询**：`step_start`/`step_size` 用于分片拉取大文档布局或音视频段落，避免单次响应过大。

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`，并通过环境变量或 Header 注入请求 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析：调用 `/parse/submit`，获得 `biz_id`（如 `parseX-2026xxxx-xxxxxxx` 或 `parseX-Video-xxx`）
   - 抽取：调用 `/extract/submit`，可复用解析 `biz_id` 或传新 `file_url`
3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）
   - 抽取结果：调用 `/extract/result`，解析 `data.extract_result_json` 或细粒度 `data.fields`
4. **错误处理**：状态为 `failed` 时，依据响应中的 `code` 字段对照[错误码](../../raw/application-api-reference/api-overview/errors.md)排查原因（如 `ResultNotReady` 需重试，`FileDownloadFailed` 需修复 URL）。

## 限制和注意事项

- **异步时效性**：解析任务最长保留 30 天（`ParseResultExpired`），抽取复用的解析结果仅保留 7 天（`ParseResultNotReusable`）。
- **文件限制**：单文件大小、页数、音视频时长均有上限；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded` 错误。
- **重试策略**：`FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需人工干预 URL 或权限。
- **Schema 与输入匹配**：抽取时若 `extract_schema` 格式无效，返回 `InvalidSchema`；音视频作为原始输入直接提交抽取会触发 `UnsupportedFileType`。
- **OSS 配置安全**：`output.oss_config` 和查询时的 `oss_config` 均需显式传入完整凭证（`access_key_id`/`secret`/`security_token`），不继承默认配置。

> **注意**：文档 6 的警告明确要求“复用的解析结果若已超过 7 天保留期或类型不匹配，接口会返回对应错误”，而文档 1 的 `ParseResultNotReusable` 错误说明中亦强调“输入是音频/视频或类型不匹配”，二者一致；但文档 5 未提及该保留期限制，实际应以文档 6 和文档 1 为准。

## 来源文档

- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [认证](../../raw/application-api-reference/api-overview/authentication.md)


