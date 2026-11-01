# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用[异步任务](../concepts/asynchronous-task.md)模型。调用流程统一为：提交任务 → 获取 `biz_id` → 轮询查询结果。API 通过 `Authorization: Bearer <API Key>` 鉴权，需提前在百炼控制台获取凭证。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出结构化布局（`layouts`）、Markdown 等；可配置页码范围、是否保留页眉页脚、坐标信息、图片描述等 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（`diarization`）、剧情解析（`synopsis_parse`）、分段（`segments`）、摘要（`summary`）及智能抽帧等功能 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：支持从已解析文档或原始文件中按 JSON Schema 抽取结构化字段，返回带引用定位（`citations`）的 `extract_result_json` 和细粒度 `fields` 结果；**不支持直接输入音视频** [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

> **注意**：文档解析与字段抽取虽共享 `biz_id` 命名空间和轮询机制，但任务类型隔离——`parse/submit` 返回的 `biz_id` 仅能用于 `/parse/result`，`extract/submit` 返回的 `biz_id` 仅能用于 `/extract/result`；混用将返回 `NotExistBizId` 错误。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `file_url` | 请求体（必填之一） | 可公开访问的文件 URL，协议需支持 HTTPS | `"https://example.com/doc.pdf"` |
| `parsed_file_biz_id` | 请求体（`extract/submit` 专用） | 复用已有解析结果的 `biz_id`，需在 7 天保留期内 | `"parseX-2026xxxx-xxxxxxx"` |
| `processing` | 请求体（可选） | 内联处理配置，优先级高于 `config_id`；文档解析含 `doc_processing_config`，音视频含 `media_processing_config`，抽取含 `extract_processing_config` | 见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 和 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 示例 |
| `extract_schema` | `processing.extract_processing_config` 内（抽取必填） | 定义抽取目标的 JSON Schema 对象（非字符串），支持嵌套对象与数组 | `{ "type": "object", "properties": { "amount": { "type": "number" } } }` |
| `biz_id` | 所有 `/result` 接口请求体（必填） | [异步任务](../concepts/asynchronous-task.md)唯一标识，由对应 `/submit` 接口返回 | `"parseX-Video-2026xxxx-xxxxxxx"` |

## 使用方式

1. **鉴权准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并通过环境变量或 Header 传递：  
   ```bash
   curl -H "Authorization: Bearer $DASHSCOPE_API_KEY" ...
   ```
   详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。

2. **提交任务**：
   - 解析：调用 `/parse/submit`，传入 `file_url` 或音视频 URL，获得 `biz_id`；
   - 抽取：调用 `/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` + `extract_schema`，获得 `biz_id`。

3. **轮询结果**：
   - 解析结果：调用 `/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `/extract/result`，同上；
   - 状态为 `processing` 时需重试（建议指数退避），`failed` 时参考 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位原因。

## 限制和注意事项

- **文件限制**：单文件大小上限、页数上限、音视频时长上限等详见错误码文档中的 `FileSizeExceeded`、`PageCountExceeded`、`ProcessingTimeout` 等条目 [错误码](../../raw/application-api-reference/api-overview/errors.md)。
- **保留期**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**（`ParseResultNotReusable` 错误）。
- **安全要求**：API Key 具备账号级权限，**严禁硬编码或提交至代码仓库**；推荐按应用拆分 Key 并定期轮转 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **OSS 输出**：若需将结果写入客户 OSS，需在 `output.oss_config` 或 `oss_config` 中完整提供 `bucket`、`endpoint`、`access_key_id`、`access_key_secret` 和 `security_token`（RAM 子账号需额外授权）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


