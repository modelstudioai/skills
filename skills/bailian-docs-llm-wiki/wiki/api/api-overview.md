# api [overview](../guides/overview.md)

ParseX API 提供文档、图片及音视频的结构化解析与字段抽取能力，采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均需通过 API Key 鉴权，支持灵活的处理配置与输出定制。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出 Markdown、布局信息、表格、段落、坐标等；支持页码范围控制、页眉页脚解析、图像描述生成等 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供 ASR 转录、人声分离（diarization）、抽帧（支持 `auto`/`frame_rate` 模式）、剧情解析（含摘要、分段、内容描述）等能力 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于 JSON Schema 从解析结果或原始文件中抽取结构化字段，支持引用定位（`citations`）、推断开关（`allow_inference`）和置信度说明（`reason`），但**不支持直接输入音视频** [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

> **注意**：文档解析与字段抽取虽共享 `biz_id` 机制和异步流程，但二者任务类型隔离——`parse/submit` 返回的 `biz_id` 仅用于 `parse/result`；`extract/submit` 返回的 `biz_id` 仅用于 `extract/result`。混用将导致 `NotExistBizId` 错误。

## 关键参数

- **必填鉴权头**：`Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 需通过百炼控制台获取并安全存储 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：`biz_id` 是所有异步操作的核心 ID，由 `/parse/submit` 或 `/extract/submit` 返回，不可跨接口复用。
- **输入源二选一**：
  - 解析任务：`file_url`（必需） + 可选 `file_name` 或 `file_name_extension`；
  - 抽取任务：`file_url` **或** `parsed_file_biz_id`（二者必选其一）；复用解析结果时，需确保其未超 7 天保留期且类型兼容。
- **处理配置优先级**：`processing`（内联对象） > `config_id`（已保存配置）。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于持久化到客户 OSS）等。

## 使用方式

1. **准备凭证**：按 [鉴权](../../raw/application-api-reference/api-overview/authentication.md) 获取并配置 `DASHSCOPE_API_KEY`；
2. **提交任务**：
   - 文档/音视频解析 → 调用 `/parse/submit`，获取 `biz_id`；
   - 字段抽取 → 调用 `/extract/submit`，获取 `biz_id`；
3. **轮询结果**：
   - 解析任务 → 轮询 `/parse/result?biz_id=xxx`，关注 `data.status`（`success`/`failed`/`processing`）；
   - 抽取任务 → 轮询 `/extract/result?biz_id=xxx`，同样依据 `data.status` 判断终止条件；
4. **错误处理**：若返回 `ResultNotReady`，继续轮询；若返回其他错误码（如 `ProcessingTimeout`、`ParseResultNotReusable`），需结合 [错误码](../../raw/application-api-reference/api-overview/errors.md) 文档定位原因。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限，具体配额以控制台实时页面为准；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded` [错误码](../../raw/application-api-reference/api-overview/errors.md)。
- **复用约束**：抽取任务复用解析结果时，必须满足：① `parsed_file_biz_id` 存在且未过期（≤7 天）；② 原始解析类型支持抽取（音视频解析结果不可用于字段抽取）；否则返回 `ParseResultNotReusable`。
- **重试策略**：`FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需检查 URL 可访问性及权限 [错误码](../../raw/application-api-reference/api-overview/errors.md)。
- **Schema 与输入匹配**：抽取任务中 `extract_schema` 必须为合法 JSON 对象，且字段类型需与实际内容语义一致；`InvalidSchema` 错误表明格式非法。
- **OSS 安全**：若使用 `oss_config`，AccessKey 等敏感信息应通过请求体传入，避免硬编码；建议使用临时 Security [Token](../concepts/token.md)。

## 来源文档

- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)


