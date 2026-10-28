# api overview

ParseX API 提供文档解析与结构化信息抽取的编程接口，所有能力通过 DashScope 网关统一接入。接口采用标准 RESTful 设计，基于 HTTPS 协议、JSON 格式通信，支持异步任务提交与轮询获取结果。开发者需使用有效的 `DASHSCOPE_API_KEY` 进行认证。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（含扫描件）、纯文本等格式的版面分析、文字识别与语义分块；  
- **音视频解析**：支持 MP4、MOV、AVI 等常见格式的语音转写、关键帧提取与时间轴对齐；  
- **结构化抽取**：基于用户提供的 JSON Schema，从解析结果中抽取指定字段（如合同金额、签署方、生效日期等），详见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)；  
- 所有功能均以异步方式执行，不提供同步返回完整结果的接口，具体流程见 [异步调用流程](../../raw/application-api-reference/api-overview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `biz_id` | string | 是（结果查询时） | 由提交接口返回的任务唯一标识，用于轮询结果；首次调用时不可传入 |
| `file_url` 或 `file_bytes` | string / base64 | 是（提交时） | 文档或音视频文件的公网可访问 URL，或 Base64 编码内容（≤50MB） |
| `schema` | object | 否（抽取任务必需） | 符合 JSON Schema Draft-07 的结构定义，决定抽取字段与类型约束；详见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `parse_mode` | string | 否 | 可选 `layout`（默认，保留版面结构）或 `semantic`（按语义段落聚合），仅对文档解析生效 |

> **注意**：原始文档中 `parse_mode` 的默认值未在 [API 概览](../../raw/application-api-reference/api-overview.md) 明确说明，但在 [document-parsing/parse-submit.md](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 中确认为 `"layout"`；请以该文档为准。

## 使用方式

1. **构造请求**：向 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x` 发送 `POST` 请求；  
2. **设置 Header**：必须包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`；  
3. **提交任务**：调用 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 或 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)，获取 `biz_id`；  
4. **轮询结果**：使用 `biz_id` 调用对应的结果查询接口（路径为 `/result/{biz_id}`），直到响应中 `data.status` 为 `"success"` 或 `"failed"`；  
5. **处理响应**：成功时 `data.result` 包含结构化输出；失败时参考 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位问题。

## 限制和注意事项

- 单次请求体（JSON）总大小 ≤ 5 MB；文件内容（`file_bytes`）≤ 50 MB；`file_url` 指向的资源需在 5 分钟内可稳定访问；  
- 异步任务最长保留 24 小时，超时后 `biz_id` 不再有效；  
- 所有接口仅支持 HTTPS，明文 HTTP 请求将被拒绝；  
- 响应中 `request_id` 是排查问题的必需字段，请务必记录；  
- 错误响应中 `code` 字段为平台级错误码（如 `InvalidParameter`, `ResourceNotFound`），业务逻辑错误（如 schema 校验失败）会返回 `code: "ValidationError"`，详细信息见 [错误码](../../raw/application-api-reference/api-overview/errors.md)。

## 来源文档

- [API 概览](../../raw/application-api-reference/api-overview.md)


