# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用异步任务模型：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，所有请求需携带有效凭证。完整调用流程与错误处理机制详见[错误码](../../raw/application-api-reference/api-overview/errors.md)。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落等；支持页码范围控制、页眉页脚解析、坐标定位及图片描述生成。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（Diarization）、剧情解析（Synopsis）、分段摘要、关键帧抽取（支持 `auto` 或指定帧率模式）等功能。
- **字段抽取**：基于用户提供的 JSON Schema，从已解析文档或原始文件中抽取结构化字段；支持引用溯源（`citations`）、推断启用控制（`allow_inference`）及自定义 Prompt；**不支持直接对音视频进行抽取**，详见[字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

> **注意**：文档解析与字段抽取虽共享 `biz_id` 任务标识和异步模型，但二者输入约束不同——字段抽取复用解析结果时，要求 `parsed_file_biz_id` 对应的解析结果必须在 **7 天保留期内**，且原始输入类型须为文档/图片（音视频解析结果不可复用），否则返回 `ParseResultNotReusable` 错误（参见[错误码](../../raw/application-api-reference/api-overview/errors.md)）。

## 关键参数

| 参数 | 位置 | 说明 | 示例/约束 |
|------|------|------|-----------|
| `file_url` | 请求体（必填之一） | 文件可公开访问的 HTTPS URL | 必须可被服务端直连下载；超时或不可达将触发 `FileDownloadFailed` 或 `FileDownloadTimeout` |
| `biz_id` | `/parse/result` 和 `/extract/result` 请求体（必填） | 异步任务唯一 ID，由 `/parse/submit` 或 `/extract/submit` 返回 | 用于轮询状态，不可跨接口混用 |
| `processing` | 请求体（可选） | 内联处理配置对象，优先级高于 `config_id` | 文档解析中使用 `doc_processing_config`，音视频使用 `media_processing_config`，字段抽取使用 `extract_processing_config`；内联配置时 `extract_schema` 为必需字段（见[提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)） |
| `output.output_file_format` | 请求体（可选） | 指定输出格式，当前仅支持 `["markdown"]` | 未指定时默认不生成 Markdown 输出 |
| `oss_config` | 请求体（可选） | 用户自有 OSS 输出配置，用于结果持久化 | 需提供 `bucket`、`endpoint`、`access_key_id`、`access_key_secret`（及可选 `security_token`） |

## 使用方式

1. **鉴权准备**：获取百炼平台 `DASHSCOPE_API_KEY`（以 `sk-` 开头），通过环境变量配置并注入 `Authorization: Bearer $DASHSCOPE_API_KEY` Header（详见[认证](../../raw/application-api-reference/api-overview/authentication.md)）；
2. **提交任务**：
   - 解析任务：调用 `/parse/submit`，传入 `file_url` 及可选 `processing` 配置，获取 `biz_id`；
   - 抽取任务：调用 `/extract/submit`，二选一提供 `file_url` 或 `parsed_file_biz_id`，并确保 `processing.extract_processing_config.extract_schema` 已定义；
3. **轮询结果**：持续调用 `/parse/result` 或 `/extract/result`，检查 `data.status` 字段：
   - `init` / `processing` → 继续轮询（建议指数退避）；
   - `success` → 解析结果在 `data.layouts` / `data.extract_result_json` 中，抽取引用信息在 `data.fields[].citations`；
   - `failed` → 查看 `code` 和 `message`，结合[错误码](../../raw/application-api-reference/api-overview/errors.md)定位原因。

## 限制和注意事项

- **文件限制**：单文件大小上限为 100 MB；PDF 页数上限为 1000 页；音视频时长上限为 2 小时；超出触发 `FileSizeExceeded` 或 `PageCountExceeded` 错误。
- **保留期约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，该结果必须在 **7 天内**（`ParseResultNotReusable` 错误）；
- **重试策略**：
  - `FileDownloadTimeout` 可重试；
  - `FileDownloadFailed` 不可重试，需修复 URL 或网络可达性；
  - `ResultNotReady` 必须使用原 `biz_id` 重试，不可新建任务；
- **安全要求**：API Key 严禁硬编码或提交至代码仓库；建议按应用拆分 Key 并定期轮转。

## 来源文档

- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [认证](../../raw/application-api-reference/api-overview/authentication.md)


