# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过统一的 `Authorization: Bearer <API Key>` 鉴权，适用于企业级文档处理与信息提取场景。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出 Markdown、布局结构（`layouts`）、表格、段落、页眉页脚等；支持指定页码范围、坐标定位、图片描述生成等高级配置。详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等常见音视频格式，提供人声分离（diarization）、ASR 转录、抽帧（支持 `auto` 或 `frame_rate` 模式）、剧情解析（`synopsis_parse`）、分段摘要（`synopsis_segments`）及全局摘要（`synopsis_summary`）等功能。
- **字段抽取**：支持基于 JSON Schema 的结构化信息抽取，输入可为原始文件 URL 或复用已解析的 `parsed_file_biz_id`（需在 7 天保留期内且类型匹配）；支持引用溯源（`citation_required`）和可控推断（`allow_inference`）。> **注意**：抽取不支持直接输入音视频，仅支持图文材料或复用其解析结果，该限制在 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中明确说明，与部分旧版文档中模糊表述存在差异。

## 关键参数

| 参数 | 位置 | 说明 | 示例 |
|------|------|------|------|
| `file_url` | `/parse/submit`, `/extract/submit` | 文件公网可访问 URL，协议需为 `https` 或 `http` | `"https://example.com/doc.pdf"` |
| `biz_id` | `/parse/result`, `/extract/result` | 提交任务后返回的唯一业务 ID，用于轮询 | `"parseX-2026xxxx-xxxxxxx"` |
| `processing.*` | 内联配置 | 优先级高于 `config_id`；文档解析含 `doc_processing_config`，音视频含 `media_processing_config`，抽取含 `extract_processing_config` | 见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 和 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 示例 |
| `extract_schema` | `/extract/submit`（内联时必填） | JSON Schema 对象，定义待抽取字段结构；字符串形式需转义 | `{"type":"object","properties":{"amount":{"type":"number"}}}` |
| `step_start` / `step_size` | `/parse/result` | 分片查询参数，用于分批获取 `layouts`（文档）或 `segments`（音视频） | 默认 `0`，`step_size=100` 可分页拉取 |

## 使用方式

1. **鉴权准备**：获取百炼控制台颁发的 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并设为环境变量或通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传递。详见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 解析任务：调用 `/parse/submit`，传入 `file_url` 及可选处理配置，获得 `biz_id`；
   - 抽取任务：调用 `/extract/submit`，二选一提供 `file_url` 或 `parsed_file_biz_id`，并指定 `extract_schema`（内联时）或 `config_id`。
3. **轮询结果**：持续调用 `/parse/result` 或 `/extract/result`，检查 `data.status` 字段。状态为 `processing` 时继续轮询（建议间隔 ≥1s）；为 `success` 或 `failed` 时终止。失败时参考 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位原因。
4. **结果消费**：成功响应中，文档解析结果含 `markdown_content` 和 `layouts`；音视频含 `segments`、`synopsis_result` 等；抽取结果含 `extract_result_json` 和带引用坐标的 `fields` 数组。

## 限制和注意事项

- **文件限制**：单文件大小上限、页数上限、音视频时长上限等由服务配额控制；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded` 错误（见 [错误码](../../raw/application-api-reference/api-overview/errors.md)）。
- **保留期约束**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误）；
  - 复用解析结果进行抽取时，该结果须在 **7 天内**，否则返回 `ParseResultNotReusable`（见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 警告）。
- **重试策略**：`FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需修复 URL 或权限。
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库；建议按应用拆分 Key 并定期轮转（见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md) 安全建议）。
- **异步行为**：所有任务均为异步，无同步阻塞接口；轮询时请勿高频请求（如 <500ms），避免触发限流。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


