# api overview

ParseX API 提供文档解析与结构化信息抽取的编程接口，所有能力通过 DashScope 网关统一接入。接口采用标准 RESTful 设计，基于 HTTPS + JSON 协议，支持异步任务提交与轮询结果获取。开发者需使用有效的 `DASHSCOPE_API_KEY` 进行认证，具体流程详见 [API 概览](../../raw/application-api-reference/api-overview.md)。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（含 OCR）、纯文本等格式的语义解析与版面还原；  
- **音视频解析**：支持 MP4、MOV、AVI 等常见格式的语音转写、关键帧提取与时间轴对齐；  
- **结构化抽取**：基于用户提供的 JSON Schema，从解析结果中抽取指定字段（如合同条款、发票要素、简历信息等），能力说明见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)；  
- 所有功能均以异步方式执行，不提供同步阻塞式调用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `biz_id` | string | 否（仅结果查询时必填） | 任务唯一标识，由提交接口返回，用于轮询结果；详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) |
| `file_url` 或 `file_bytes` | string / base64 | 是（二选一） | 文档/音视频原始数据来源；`file_url` 需为公网可访问的 HTTPS 地址，`file_bytes` 为 Base64 编码内容（≤50MB） |
| `schema` | object | 仅抽取任务必填 | 符合 JSON Schema Draft-07 的结构定义，决定输出字段与校验规则 |

> **注意**：原始文档中未明确 `file_bytes` 的最大长度限制，但实际服务端限制为 50MB；该值与 [错误码](../../raw/application-api-reference/api-overview/errors.md) 中 `RequestEntityTooLarge` 错误描述一致，建议以 50MB 为准。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`；  
2. **提交任务**：向 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x` 发送 POST 请求，路径根据功能选择（如 `/parse` 或 `/extract`）；  
3. **轮询结果**：使用返回的 `biz_id` 调用 `/result` 接口，按 `data.status` 字段判断状态（`processing` / `success` / `failed`），直至完成；  
4. **处理响应**：成功时 `data.result` 包含结构化输出；失败时参考 `code` 和 `message` 字段定位问题。

## 限制和注意事项

- 单次请求体（含 `file_bytes`）不得超过 50MB；若使用 `file_url`，源文件大小仍受后端解析能力限制（PDF 建议 ≤1000 页）；  
- 异步任务最长保留结果 7 天，超时后 `biz_id` 不再有效；  
- 所有接口仅支持 `POST` 方法，不支持 GET 或其他动词；  
- 响应中 `request_id` 是排查问题的必需字段，务必在日志中留存；  
- 若发现 `data.status` 长期为 `processing`（>30 分钟），应检查输入格式或联系技术支持，而非无限重试。

## 来源文档

- [API 概览](../../raw/application-api-reference/api-overview.md)


