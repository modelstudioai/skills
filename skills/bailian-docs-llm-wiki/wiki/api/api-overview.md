# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，采用[异步任务](../concepts/asynchronous-task.md)模型（提交 → 轮询 → 获取结果）。所有接口均通过 `Authorization: Bearer <API Key>` 鉴权，请求需指向工作空间专属域名。开发者应优先复用解析结果以提升效率并降低成本。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出布局结构（`layouts`）、Markdown 等可读格式；支持页码范围、页眉页脚、坐标定位、图片描述等细粒度控制 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（Diarization）、剧情解析（Synopsis）、分段（Segments）、抽帧（Frame Extraction）及摘要生成能力 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **字段抽取**：支持从图文材料中按 JSON Schema 抽取结构化字段，可直接输入文件 URL，或复用已存在的解析任务结果（`parsed_file_biz_id`），并返回引用位置（`citations`）和推断依据 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

> **注意**：字段抽取明确不支持音视频原始输入（见[错误码](../../raw/application-api-reference/api-overview/errors.md)中 `UnsupportedFileType`），仅支持对已解析的图文内容进行抽取；而文档解析本身支持音视频输入。

## 关键参数

- **通用必填**：`biz_id`（用于轮询结果）、`Authorization` Header（`Bearer $DASHSCOPE_API_KEY`）。
- **解析提交**：`file_url`（必需）或 `file_name_extension`（二选一）；`processing` 内联配置优先于 `config_id`；音视频需在 `media_processing_config` 中显式启用所需能力（如 `enable_synopsis_parse: true`）。
- **抽取提交**：必须二选一指定输入源：`file_url`（触发完整解析+抽取）或 `parsed_file_biz_id`（复用已有解析结果）；若使用内联配置，`processing.extract_processing_config.extract_schema` 为必需字段，且为 JSON 对象（非字符串）——注意 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 示例中 `extract_schema` 的实际传值是未转义的 JSON 对象，而非字符串字面量。
- **OSS 输出**：`output.oss_config` 可用于指定结果写入客户 OSS，各字段（`bucket`, `endpoint`, `access_key_id` 等）需同时提供，缺一不可。

## 使用方式

1. **鉴权准备**：获取百炼控制台颁发的 `DASHSCOPE_API_KEY`（以 `sk-` 开头），通过环境变量或 Header 传递 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **异步调用流程**：
   - 解析场景：调用 `/parse/submit` → 获取 `biz_id` → 轮询 `/parse/result` 直至 `data.status == "success"`。
   - 抽取场景：调用 `/extract/submit` → 获取 `biz_id` → 轮询 `/extract/result` 直至 `data.status == "success"`。
3. **CLI 辅助**：支持通过 `bl parsex parse submit` / `bl parsex extract submit` 等 CLI 命令快速验证，详见 [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md) 和 [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)。

## 限制和注意事项

- **保留期限制**：解析结果默认保留 **30 天**（见 `ParseResultExpired` 错误码），但**仅前 7 天可被抽取任务复用**（见 `ParseResultNotReusable` 错误说明）。
- **文件限制**：单文件大小、页数、时长等有硬性上限，具体配额以控制台实时页面为准；`FileSizeExceeded`、`PageCountExceeded`、`PageRangeInvalid` 等错误码对应明确的超限类型。
- **重试策略**：`FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需检查 URL 权限或有效性。
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码或提交至代码仓库；建议为不同应用分配独立 Key 以便审计与撤销 [认证](../../raw/application-api-reference/api-overview/authentication.md)。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


