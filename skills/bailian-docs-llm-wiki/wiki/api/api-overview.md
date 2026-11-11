# api overview

ParseX API 提供文档、图片及音视频的结构化解析与字段抽取能力，采用异步任务模型：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均需通过 API Key 鉴权，支持 RESTful 调用与百炼 CLI 两种集成方式。核心流程覆盖从文件输入、处理配置、结果输出到错误处理的完整链路。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落等；支持页码范围、页眉页脚、坐标定位、图片描述等精细控制。详见[文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供人声分离（`diarization`）、剧情解析（`synopsis_parse`）、抽帧（`frame_extraction`）、ASR 文本、视频分段与图像描述等能力。
- **字段抽取**：基于 JSON Schema 从图文材料中结构化抽取字段，支持引用溯源（`citations`）、推断开关（`allow_inference`）及复用已有解析结果（需在 7 天保留期内）。详见[字段解析 API](raw/application-api-reference/api-overview/field-extraction.md)。
- > **注意**：字段抽取明确不支持音视频直接输入（见[提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md)警告），且复用解析结果时要求类型匹配（如文档解析结果不可用于音视频抽取），否则返回 `ParseResultNotReusable` 错误。

## 关键参数

| 参数 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `file_url` / `parsed_file_biz_id` | string | 二选一：原始文件 URL 或已解析任务 ID（仅抽取支持） | [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `processing` | object | 内联处理配置，优先级高于 `config_id`；文档解析含 `doc_processing_config`，音视频含 `media_processing_config`，抽取含 `extract_processing_config` | [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) |
| `processing.extract_processing_config.extract_schema` | object | 抽取必需的 JSON Schema 定义，需为合法 JSON 对象（非字符串） | [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `output.output_file_format` | string[] | 仅文档解析支持，当前仅 `["markdown"]` | [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) |
| `biz_id` | string | 所有异步任务的核心标识符，用于后续 `/parse/result` 或 `/extract/result` 查询 | [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md) |

## 使用方式

1. **认证**：设置环境变量 `DASHSCOPE_API_KEY`，并在每个请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。凭证获取与安全规范详见[认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **提交任务**：
   - 文档/音视频解析：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选 `processing` 配置；
   - 字段抽取：调用 `/api/v2/apps/parse-x/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`。
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，解析 `data.extract_result_json` 或细粒度 `data.fields`。
4. **CLI 辅助**：支持 `bl parsex parse submit` 和 `bl parsex extract submit` 等命令，降低调试门槛（见[文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)）。

## 限制和注意事项

- **配额与超限**：单文件大小、页数、音视频时长、Schema 复杂度等受服务配额约束；超限触发 `FileSizeExceeded`、`PageCountExceeded`、`ServiceQuotaExhausted` 等错误（见[错误码](raw/application-api-reference/api-overview/errors.md)）。
- **时效性约束**：
  - 解析结果默认保留 **30 天**，超期返回 `ParseResultExpired`；
  - 抽取任务复用解析结果仅限 **7 天内**，且类型必须匹配（文档↔文档，音视频↔音视频）。
- **重试策略**：
  - `FileDownloadTimeout` 可重试；`FileDownloadFailed` 不可重试，需修复 URL 或权限；
  - `ResultNotReady` 表示任务未完成，应继续轮询同一 `biz_id`。
- **安全强制项**：API Key **不得硬编码或提交至代码仓库**，推荐使用环境变量 + RAM 子账号最小权限授权（见[认证](../../raw/application-api-reference/api-overview/authentication.md)）。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)


