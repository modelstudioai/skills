# api [overview](overview.md)

ParseX API 提供文档解析与结构化信息抽取的编程接口，所有能力通过 DashScope 网关统一接入。接口采用标准 RESTful 设计，基于 HTTPS 协议、JSON 格式通信，支持异步任务提交与轮询获取结果。开发者需使用有效的 `DASHSCOPE_API_KEY` 进行认证。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（含扫描件）、纯文本等格式的版面分析、文字识别与语义分块；  
- **音视频解析**：支持 MP4、MOV、AVI 等常见格式的语音转写、关键帧提取与时间轴对齐；  
- **结构化抽取**：基于用户提供的 JSON Schema 自动从解析结果中抽取字段（如合同金额、签署日期、甲方名称等），详见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)；  
- 所有功能均以异步方式执行，不提供同步返回完整结果的接口，具体流程见 [异步调用流程](../../raw/application-api-reference/api-overview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `biz_id` | string | 是（结果查询时） | 由提交接口返回的唯一任务标识，用于轮询状态和拉取结果；首次调用无需提供 |
| `file_url` 或 `file_bytes` | string / base64 | 是（提交时） | 文档或音视频文件的公网可访问 URL，或 Base64 编码内容（≤50MB） |
| `schema` | object | 否（抽取任务必填） | 符合 JSON Schema 规范的结构定义，决定抽取字段与约束逻辑；参考 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `callback_url` | string | 否 | 可选回调地址，任务完成后将 POST 结果至该 URL（需自行实现接收端） |

> **注意**：原始文档中 `file_bytes` 的 Base64 编码要求为无换行、无前缀（如 `data:application/pdf;base64,`），但 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 示例中误含 `data:` 前缀，实际调用会返回 `InvalidParameter` 错误，请严格按 `base64-encoded-string` 格式传入。

## 使用方式

1. **构造请求**：向 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x` 发起 `POST` 请求；  
2. **设置 Header**：必须包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`；  
3. **提交任务**：调用 `/parse`（解析）或 `/extract`（抽取）端点，传入必要参数；  
4. **轮询结果**：使用返回的 `biz_id` 调用 `/result/{biz_id}`，检查 `data.status` 字段，直到值为 `success` 或 `failed`；  
5. **处理响应**：成功时 `data.result` 包含结构化输出；失败时参考 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位问题。

## 限制和注意事项

- 单次请求体（JSON）最大 5 MB，文件内容（`file_bytes`）最大 50 MB；  
- `file_url` 必须为公网可直连地址，且响应头需包含 `Content-Length` 和合法 `Content-Type`；  
- 异步任务默认最长保留 7 天，超时后 `biz_id` 不再有效；  
- 所有接口仅支持 `POST` 方法，不支持 `GET` 或其他 HTTP 方法；  
- 响应中 `request_id` 是排查问题的关键凭证，建议日志中持久化记录。

## 来源文档

- [API 概览](../../raw/application-api-reference/api-overview.md)


