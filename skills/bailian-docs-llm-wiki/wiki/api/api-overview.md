# api [overview](../guides/overview.md)

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取能力，所有接口均采用异步调用模式：先提交任务获取 `biz_id`，再轮询查询结果。API 通过统一的 `Authorization: Bearer <API Key>` 鉴权，支持文件 URL 直接解析或复用已有解析结果，适用于自动化文档处理流水线。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出 Markdown、布局结构（`layouts`）、表格、段落、页眉页脚、坐标信息等；支持指定页码范围、禁用页眉页脚、启用图像描述等配置。详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等常见格式，提供人声分离（diarization）、剧情解析（synopsis）、分段（segments）、摘要（summary）、抽帧（frame extraction）及帧级图文描述能力。
- **字段抽取**：支持基于 JSON Schema 的结构化信息抽取，输入可为原始文件 URL 或复用解析任务生成的 `parsed_file_biz_id`；支持引用定位（`citations`）、推断（`allow_inference`）和自定义 Prompt。注意：**抽取不支持音视频直接输入**，仅支持从已解析的图文结果中抽取 —— 此限制在 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中明确说明，与文档解析能力形成互补。

> **注意**：文档 6 明确指出“抽取不支持音视频输入”，而文档 4 中音视频解析示例未提及后续可被抽取复用。实际流程中，音视频需先解析为图文内容（如 `synopsis_result` 或 `segments.text_info`），再作为文本输入提交抽取任务；但该路径未在任一原始文档中给出完整示例或确认支持，开发者应避免假设音视频解析结果可直接用于抽取。

## 关键参数

- **必填鉴权**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header，API Key 须通过百炼控制台获取，详见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：`biz_id` 是所有异步操作的核心 ID，由 `/parse/submit` 或 `/extract/submit` 返回，用于后续 `/parse/result` 或 `/extract/result` 查询。
- **输入源二选一**：
  - 解析任务：`file_url`（必填）或 `file_name_extension`（与 `file_name` 二选一）；
  - 抽取任务：`file_url` **或** `parsed_file_biz_id`（二者必须且只能选其一）。
- **处理配置优先级**：`processing` 内联对象始终优先生效于 `config_id`；若同时提供，`config_id` 被忽略。
- **Schema 定义**：字段抽取必需 `processing.extract_processing_config.extract_schema`（JSON 对象），且需符合 OpenAPI Schema 规范；示例中需注意 JSON 字符串转义要求。

## 使用方式

1. **准备凭证**：设置环境变量 `DASHSCOPE_API_KEY`，确保密钥安全存储（不入代码仓库、按应用拆分、定期轮转）。
2. **提交任务**：
   - 文档/音视频解析 → 调用 `/api/v2/apps/parse-x/parse/submit`；
   - 字段抽取 → 调用 `/api/v2/apps/parse-x/extract/submit`。
3. **轮询结果**：使用返回的 `biz_id` 持续调用对应 `/result` 接口，检查 `data.status` 字段：
   - `init` / `processing`：继续轮询（建议指数退避）；
   - `success`：读取 `data.extract_result_json` 或 `data.markdown_content` 等结果字段；
   - `failed`：结合错误码定位问题（见下文）。
4. **错误处理**：收到 `ResultNotReady`（HTTP 409）时需重试；`FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试 —— 具体策略参见 [错误码](../../raw/application-api-reference/api-overview/errors.md)。

## 限制和注意事项

- **保留期限制**：
  - 解析结果默认保留 **30 天**（`ParseResultExpired` 错误码）；
  - 抽取任务复用解析结果时，该结果须在 **7 天内**（`ParseResultNotReusable` 错误码），且类型匹配（音视频解析结果不可直接用于抽取）。
- **文件限制**：
  - 单文件大小、页数、音视频时长均有硬性上限，具体数值以控制台配额页面为准；`FileSizeExceeded`、`PageCountExceeded`、`PageRangeInvalid` 等错误码对应不同超限场景。
- **安全与权限**：
  - API Key 具有账号级权限，RAM 子账号需显式授权；
  - OSS 输出配置中的 `access_key_id`/`access_key_secret` 属于高危凭证，不应明文传入生产请求，推荐使用临时 STS Token（`security_token`）。
- **异步行为**：所有任务均为后台执行，无同步阻塞接口；轮询间隔需自行控制，避免高频请求触发限流（`ServiceQuotaExhausted`）。

## 来源文档

- [鉴权](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)


