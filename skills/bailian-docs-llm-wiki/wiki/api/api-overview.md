# api [overview](../guides/overview.md)

ParseX API 提供文档解析与结构化信息抽取的编程接口，所有能力通过 DashScope 网关统一接入。接口采用标准 RESTful 设计，基于 HTTPS 协议，以异步任务模式为主，适用于高吞吐、多格式（PDF/Word/音视频等）的自动化处理场景。详细协议约定见 [API 概览](../../raw/application-api-reference/api-overview.md)。

## 支持的模型/功能

- **文档解析**：支持 PDF、DOCX、PPTX、TXT、图像（OCR）、音视频（ASR+OCR）等多模态输入，输出结构化文本、段落、表格、图表元数据等。
- **字段抽取**：支持按用户定义的 JSON Schema 进行定制化信息抽取（如合同关键条款、发票要素、简历字段），底层调用 ParseX 专用抽取模型。
- **异步工作流**：所有任务均返回 `biz_id`，需轮询结果接口获取最终状态与数据，详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 和 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `biz_id` | string | 是（结果查询时） | 异步任务唯一标识，由提交接口返回，用于轮询结果 |
| `file_url` 或 `file_bytes` | string / base64 | 是（提交时） | 文档原始内容来源；推荐使用 `file_url`（需公网可访问的 HTTPS 地址） |
| `schema` | object | 否（抽取任务必填） | JSON Schema 定义期望抽取的字段结构，格式与校验规则见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `callback_url` | string | 否 | 可选回调地址，任务完成后将 POST 结果至该 URL（需自行实现接收逻辑） |

> **注意**：`file_bytes` 字段在大文件（>10MB）场景下易触发请求超时或内存溢出，官方文档已明确建议优先使用 `file_url` —— 请严格遵循 [API 概览](../../raw/application-api-reference/api-overview.md) 中“协议约定”章节的传输规范。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`（API Key 获取方式见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md)）和 `Content-Type: application/json`；
2. **提交任务**：向 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x/{endpoint}` 发送 POST 请求（如 `/parse` 或 `/extract`），传入必要参数；
3. **轮询结果**：使用返回的 `biz_id` 调用 `/result?biz_id=xxx`，检查 `data.status` 字段，直到为 `success` 或 `failed`；
4. **错误处理**：依据响应中的 `code` 和 `message` 字段定位问题，完整错误码列表见 [错误码](../../raw/application-api-reference/api-overview/errors.md)。

## 限制和注意事项

- 单次请求体大小上限为 **50MB**（含 JSON 封装开销），`file_bytes` 实际有效载荷建议 ≤30MB；
- `biz_id` 有效期为 **7 天**，超期后结果接口返回 `NotFound`；
- 音视频解析任务默认超时时间为 **30 分钟**，长视频需提前评估处理耗时；
- 所有接口仅支持 `POST` 方法，不支持 GET 查询或 PUT/PATCH 更新；
- 响应中 `request_id` 是排查问题的必需字段，务必在日志中持久化记录。

## 来源文档

- [API 概览](../../raw/application-api-reference/api-overview.md)


