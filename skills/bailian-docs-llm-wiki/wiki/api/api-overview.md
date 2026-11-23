# api [overview](overview.md)

ParseX API 提供文档/音视频解析与结构化字段抽取两大核心能力，采用异步任务模型（提交 → 轮询 → 获取结果）。所有接口均基于 RESTful 设计，通过 `Authorization: Bearer <API Key>` 鉴权，支持文件 URL 或复用已有解析结果作为输入源。开发者需重点关注任务状态流转、错误码处理及资源生命周期限制。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（PNG/JPG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落等；支持页码范围、页眉页脚、坐标定位、图片描述等细粒度控制。详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。
- **音视频解析**：支持 MP4、MOV 等主流格式，提供人声分离（diarization）、剧情解析（synopsis）、分段（segments）、抽帧（frame extraction）及摘要生成能力。
- **字段抽取**：基于 JSON Schema 从图文材料中提取结构化字段，支持引用溯源（`citations`）、推断开关（`allow_inference`）及置信度标注；可直接输入文件 URL，或复用 7 天内有效的解析结果（`parsed_file_biz_id`）。详见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。
- > **注意**：字段抽取明确不支持音视频原始输入（见[错误码文档](../../raw/application-api-reference/api-overview/errors.md)中 `UnsupportedFileType`），仅支持对已解析的图文内容进行抽取。

## 关键参数

- **通用必填**：`biz_id`（用于轮询结果）、`file_url` 或 `parsed_file_biz_id`（二选一）、`DASHSCOPE_API_KEY`（Header 中传递）。
- **解析任务关键参数**：
  - `processing.doc_processing_config.page_index`：指定页码范围（如 `"1-5"`）
  - `processing.media_processing_config.enable_diarization`：启用说话人分离
  - `output.output_file_format`：指定输出格式（如 `["markdown"]`）
- **抽取任务关键参数**：
  - `processing.extract_processing_config.extract_schema`：内联 JSON Schema 定义（必须为合法 JSON 对象）
  - `processing.extract_processing_config.citation_required`：是否返回原文引用位置（默认 `true`）
- **OSS 输出配置**：所有提交与查询接口均支持 `output.oss_config` 或 `oss_config` 字段，用于指定客户自有 OSS 存储目标。

## 使用方式

1. **认证准备**：获取 `DASHSCOPE_API_KEY` 并设为环境变量，请求头携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。详见 [认证](../../raw/application-api-reference/api-overview/authentication.md)。
2. **异步调用流程**：
   - 解析场景：`POST /parse/submit` → 获取 `biz_id` → 循环 `POST /parse/result?biz_id=...` 直至 `data.status` 为 `success` 或 `failed`
   - 抽取场景：`POST /extract/submit` → 获取 `biz_id` → 循环 `POST /extract/result?biz_id=...` 直至完成
3. **CLI 快速验证**：支持百炼 CLI 命令 `bl parsex parse submit` 和 `bl parsex extract submit`，降低调试门槛（见[文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)）。

## 限制和注意事项

- **生命周期限制**：
  - 解析结果保留期为 **30 天**（`ParseResultExpired` 错误码），但复用解析结果进行抽取时，仅支持 **7 天内**的有效结果（见[提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)警告）。
- **文件限制**：
  - 单文件大小、页数、音视频时长等受配额约束，具体数值以控制台实时配额为准；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded`。
  - 文件 URL 必须公网可访问且无鉴权跳转，否则触发 `InvalidFileUrl` 或 `FileDownloadFailed`。
- **错误处理**：
  - `ResultNotReady`（HTTP 409）表示任务仍在运行，需继续轮询；
  - `FileDownloadTimeout` 可重试，`FileDownloadFailed` 不可重试（需修复 URL 或权限）；
  - 所有错误响应均含 `request_id`，用于服务端问题定位。
- > **注意**：文档 7 明确指出“Schema 规模和长文档页数仅按工程设计边界规划，公开配额以正式页面为准”，而文档 8 未提配额细节，实际使用应以控制台或 [支持的文件与限制](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/supported-files-and-limits.md) 文档为准。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [ParseX API 错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


