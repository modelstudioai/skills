# api [overview](overview.md)

ParseX API 提供文档、图片及音视频的结构化解析与字段抽取能力，采用异步任务模型：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均需通过 API Key 鉴权，支持 HTTP REST 调用与百炼 CLI 工具两种使用方式。核心流程分为「解析」与「抽取」两大类，各自独立但可组合复用（如抽取可基于已有解析结果）。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落等；[文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 详细说明了异步流程与能力边界。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（`diarization`）、剧情解析（`synopsis_parse`）、抽帧（`frame_extraction`）及 ASR 文本生成；配置项详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：基于用户提供的 JSON Schema，从图文材料中结构化抽取指定字段；支持直接传入文件 URL 或复用已有的解析任务 ID（`parsed_file_biz_id`），但**不支持音视频输入**；该限制在 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md) 中明确强调。
- > **注意**：文档 7 明确指出“抽取不支持音视频输入”，而文档 4 的音视频解析示例中未提及后续抽取兼容性。二者逻辑一致——音视频解析产出的 `segments` 或 `synopsis_result` 不可作为抽取任务的直接输入，必须先转为图文形式（如 ASR 文本 + 关键帧描述）并保存为新文档后，方可用于抽取。

## 关键参数

- **通用鉴权**：所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY` Header；API Key 获取方式见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
- **任务标识**：
  - `biz_id`：提交任务后返回的唯一业务 ID，用于后续 `/parse/result` 或 `/extract/result` 查询。
  - `parsed_file_biz_id`：仅抽取任务支持，用于复用已有解析结果（需在 7 天保留期内且类型匹配）。
- **输入控制**：
  - `file_url`：公开可访问的文件 URL（HTTP/HTTPS），必须可被服务端直连下载。
  - `file_name` / `file_name_extension`：二选一，用于显式声明文件名或扩展名。
- **处理配置**（优先级：内联 `processing` > `config_id`）：
  - 解析任务：`doc_processing_config`（页码范围、坐标、页眉页脚等）或 `media_processing_config`（人声分离、抽帧参数等）。
  - 抽取任务：`extract_processing_config.extract_schema`（必需 JSON 对象）、`citation_required`、`allow_inference`。
- **输出控制**：`output.output_file_format`（如 `["markdown"]`）、`output.oss_config`（用于持久化到客户 OSS）。

## 使用方式

1. **准备凭证**：按 [认证](../../raw/application-api-reference/api-overview/authentication.md) 获取并配置 `DASHSCOPE_API_KEY` 环境变量。
2. **选择路径**：
   - 若只需结构化内容（如 Markdown、布局、ASR 文本）→ 调用 `/parse/submit` → 轮询 `/parse/result`。
   - 若需按 Schema 提取字段 → 
     - 方式一（端到端）：调用 `/extract/submit` 并传 `file_url`；
     - 方式二（复用解析）：先调 `/parse/submit`，待其 `status` 为 `success` 后，用其 `biz_id` 作为 `parsed_file_biz_id` 提交 `/extract/submit`。
3. **轮询结果**：对 `/parse/result` 或 `/extract/result` 发起 POST 请求，传入 `biz_id`；当 `data.status` 为 `success` 或 `failed` 时停止轮询。
4. **CLI 辅助**：开发者也可使用百炼 CLI 快速验证，命令详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限；具体数值以控制台配额页为准，文档 7 的警告提示“公开配额以正式页面为准，见[支持的文件与限制](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)”。
- **保留期约束**：
  - 解析结果默认保留 **30 天**（见错误码 `ParseResultExpired`）；
  - 复用解析结果进行抽取时，该结果须在 **7 天内**（见文档 7 警告），且类型需匹配（音视频解析结果不可复用）。
- **错误处理**：
  - `ResultNotReady`（HTTP 409）：任务未完成，需继续轮询；
  - `FileDownloadTimeout`（HTTP 400）：可重试；`FileDownloadFailed`（HTTP 400）：不可重试，需检查 URL 权限或网络；
  - `ParseResultNotReusable`（HTTP 400）：解析结果已过期或类型不支持复用（如音视频）。
- **安全要求**：API Key 具有账号级权限，严禁硬编码或提交至代码仓库；建议按应用拆分 Key 并定期轮转（见 [认证](../../raw/application-api-reference/api-overview/authentication.md)）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


