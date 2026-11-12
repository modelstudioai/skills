# api overview

ParseX API 提供文档/音视频解析与结构化字段抽取两大核心能力，采用异步任务模型：先提交任务获取 `biz_id`，再轮询查询结果。所有接口均需通过 API Key 鉴权，支持 RESTful 调用及百炼 CLI 工具。整体设计面向企业级文档智能处理场景，强调可复用性、配置灵活性与错误可观测性。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出结构化布局（`layouts`）、Markdown、表格等内容；支持页码范围、页眉页脚、坐标定位、图片描述等精细化控制。  
- **音视频解析**：支持 MP4、MOV 等主流格式，提供人声分离（Diarization）、剧情解析（Synopsis）、分段（Segments）、抽帧（Frame Extraction）及多模态描述能力。  
- **字段抽取**：基于 JSON Schema 从图文材料中提取结构化字段，支持引用溯源（`citations`）、推断开关（`allow_inference`）和复用已解析结果（需在 7 天保留期内），但**不支持音视频直接作为抽取输入**（详见[错误码](../../raw/application-api-reference/api-overview/errors.md)中 `UnsupportedFileType` 错误说明）。  
- **配置复用**：两类任务均支持 `config_id`（预存配置）与内联 `processing` 对象两种定义方式；当二者共存时，内联配置优先生效（见[提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)与[提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)示例）。

> **注意**：文档 7 明确指出“复用的解析结果若已超过 7 天保留期或类型不匹配，接口会返回对应错误”，而文档 2 的 `ParseResultNotReusable` 错误码说明中提到“解析结果不可复用……因输入是音频/视频或类型不匹配”，但未明确提及 7 天期限；此处以文档 7 的明确时限为准。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **通用鉴权** | `Authorization: Bearer $DASHSCOPE_API_KEY` | 必须通过 Header 传递，API Key 由百炼控制台获取（见[认证](../../raw/application-api-reference/api-overview/authentication.md)） |
| **任务标识** | `biz_id` | 所有异步任务的核心 ID，由 `/parse/submit` 或 `/extract/submit` 返回，用于后续 `/parse/result` 或 `/extract/result` 查询 |
| **输入源** | `file_url` / `parsed_file_biz_id` | 二选一：`file_url` 指向原始文件；`parsed_file_biz_id` 复用已有解析结果（仅限文档类，且需 ≤7 天） |
| **处理配置** | `processing.*_config` | 文档解析用 `doc_processing_config`，音视频用 `media_processing_config`，抽取用 `extract_processing_config`；内联配置优先级高于 `config_id` |
| **Schema 定义** | `processing.extract_processing_config.extract_schema` | 字段抽取必需，为 JSON 对象（非字符串），示例中已修正转义问题（见[提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)代码块） |
| **输出控制** | `output.output_file_format`, `output.oss_config` | 控制 Markdown 输出、OSS 回写等；OSS 凭证可随请求传入，也可在控制台预设 |

## 使用方式

1. **准备凭证**：在百炼控制台获取 `DASHSCOPE_API_KEY` 并配置为环境变量（见[认证](../../raw/application-api-reference/api-overview/authentication.md)）；  
2. **提交任务**：  
   - 解析任务：调用 `/api/v2/apps/parse-x/parse/submit`，传入 `file_url` 及可选 `processing` 配置；  
   - 抽取任务：调用 `/api/v2/apps/parse-x/extract/submit`，传入 `file_url` 或 `parsed_file_biz_id` 及 `extract_schema`；  
3. **轮询结果**：  
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；  
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，解析 `extract_result_json` 或细粒度 `fields`；  
4. **CLI 辅助**：支持 `bl parsex parse submit` / `bl parsex extract result` 等命令（见[文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)与[字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)说明）。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长等受配额约束，具体数值以[支持的文件与限制](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md)为准；超限时返回 `FileSizeExceeded` 或 `PageCountExceeded`（见[错误码](../../raw/application-api-reference/api-overview/errors.md)）；  
- **保留期**：解析结果默认保留 30 天（`ParseResultExpired` 错误），但**仅前 7 天支持被抽取任务复用**；音视频解析结果的 `segments` 和 `frames` 也适用此复用窗口；  
- **重试策略**：`FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试；`ResultNotReady` 需持续轮询，非错误；  
- **安全要求**：API Key 必须通过环境变量管理，禁止硬编码；建议按应用拆分 Key 并定期轮转（见[认证](../../raw/application-api-reference/api-overview/authentication.md)安全建议）；  
- **错误处理**：所有失败响应均含 `request_id` 和标准 `code`/`message`，需结合[错误码](../../raw/application-api-reference/api-overview/errors.md)文档定位根因，例如 `InvalidSchema` 表示 JSON Schema 格式非法，`ProcessingTimeout` 属服务端内部超时。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


