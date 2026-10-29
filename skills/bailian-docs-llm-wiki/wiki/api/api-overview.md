# api overview

ParseX API 提供文档与音视频的结构化解析、以及基于 Schema 的字段抽取两大核心能力，所有接口均采用[异步任务](../concepts/asynchronous-task.md)模型：先提交任务获取 `biz_id`，再轮询查询结果。API 通过 `DASHSCOPE_API_KEY` 进行鉴权，请求需携带 `Authorization: Bearer <key>` Header。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（JPG/PNG）等格式，输出结构化布局（`layouts`）、Markdown、表格、段落等；支持页码范围、页眉页脚、坐标定位、图片描述等配置。详见 [文档解析 API](raw/application-api-reference/api-overview/document-parsing.md)。
- **音视频解析**：支持 MP4、MOV、AVI 等主流格式，提供 ASR、人声分离（diarization）、剧情解析（synopsis）、抽帧（frame extraction）及多模态描述；支持按时间分片返回 `segments` 和 `video_frames`。详见 [提交解析任务](raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 中的音视频示例。
- **字段抽取**：支持从已解析结果（`parsed_file_biz_id`）或原始文件（`file_url`）中，按 JSON Schema 抽取结构化字段，返回带引用溯源（`citations`）的 `extract_result_json`。> **注意**：抽取不支持直接输入音视频，仅支持图文材料或复用此前生成的解析结果；且复用的解析结果必须在 7 天保留期内，否则返回 `ParseResultNotReusable` 错误 —— 该限制在 [提交抽取任务](raw/application-api-reference/api-overview/field-extraction/extract-submit.md) 中明确说明，而 [错误码](raw/application-api-reference/api-overview/errors.md) 文档进一步指出 `ParseResultNotReusable` 的触发条件包含“输入为音频/视频或类型不匹配”。

## 关键参数

- **通用必填**：`biz_id`（用于结果查询）、`DASHSCOPE_API_KEY`（通过 `Authorization` Header 传递）。
- **解析任务提交**：`file_url`（必需）、`file_name` 或 `file_name_extension`（二选一）、`processing`（内联配置，优先级高于 `config_id`）。音视频需在 `processing.media_processing_config` 中指定 `enable_diarization`、`frame_extraction` 等开关。
- **抽取任务提交**：`file_url` 或 `parsed_file_biz_id`（二选一）、`processing.extract_processing_config.extract_schema`（JSON 对象，内联时必需）、`citation_required`（默认 `true`）。
- **结果查询**：`step_start`/`step_size`（仅解析结果支持分片查询）、`oss_config`（可选，用于自定义 OSS 输出凭证）。

## 使用方式

1. **认证准备**：在百炼控制台获取 `DASHSCOPE_API_KEY`（以 `sk-` 开头），并设为环境变量 `DASHSCOPE_API_KEY`；所有请求必须携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。详见 [认证](raw/application-api-reference/api-overview/authentication.md)。
2. **发起任务**：
   - 解析：调用 `/api/v2/apps/parse-x/parse/submit`，获得 `biz_id`；
   - 抽取：调用 `/api/v2/apps/parse-x/extract/submit`，获得 `biz_id`。
3. **轮询结果**：
   - 解析结果：调用 `/api/v2/apps/parse-x/parse/result`，检查 `data.status`（`success`/`failed`/`processing`）；
   - 抽取结果：调用 `/api/v2/apps/parse-x/extract/result`，同上。
4. **错误处理**：收到 `ResultNotReady`（HTTP 409）时需继续轮询；收到其他错误码（如 `FileSizeExceeded`、`ProcessingTimeout`）应参考 [错误码](raw/application-api-reference/api-overview/errors.md) 文档定位原因。

## 限制和注意事项

- **文件限制**：单文件大小、页数、时长均有上限；超限将返回 `FileSizeExceeded` 或 `PageCountExceeded`；音视频抽帧分辨率范围为 `[32, 4096]` 像素。
- **保留期**：解析结果默认保留 30 天（`ParseResultExpired` 错误），但**仅前 7 天可被抽取任务复用**（`ParseResultNotReusable` 错误）。
- **安全要求**：API Key 必须通过环境变量注入，禁止硬编码或提交至代码仓库；建议为不同应用分配独立 Key 并定期轮转。
- **OSS 配置**：若使用 `output.oss_config` 或查询时传入 `oss_config`，需确保凭证具备对应 Bucket 的读写权限；`security_token` 仅在使用临时凭证时必需。

## 来源文档

- [认证](../../raw/application-api-reference/api-overview/authentication.md)
- [错误码](../../raw/application-api-reference/api-overview/errors.md)
- [文档解析 API](../../raw/application-api-reference/api-overview/document-parsing.md)
- [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)
- [查询解析结果](../../raw/application-api-reference/api-overview/document-parsing/parse-result.md)
- [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)
- [字段解析 API](../../raw/application-api-reference/api-overview/field-extraction.md)
- [查询抽取结果](../../raw/application-api-reference/api-overview/field-extraction/extract-result.md)


