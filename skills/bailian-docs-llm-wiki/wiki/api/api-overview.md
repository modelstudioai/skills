# api [overview](../guides/overview.md)

ParseX API 提供文档解析与结构化信息抽取的编程接口，所有能力通过 DashScope 网关统一接入。接口采用标准 RESTful 设计，基于 HTTPS 协议，以异步任务模式为主，适用于高并发、多格式（PDF/Word/音视频等）的自动化处理场景。开发者需使用有效的 `DASHSCOPE_API_KEY` 进行认证。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片及音视频文件的版面分析、文字识别（OCR）、表格重建与语义段落切分；  
- **结构化抽取**：支持按用户定义的 JSON Schema 提取字段（如合同关键条款、发票要素、简历信息等），底层调用 ParseX 专用抽取模型；  
- **多模态扩展能力**：音视频解析自动关联语音转写、关键帧提取与时间戳对齐，详见 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md)。  

> **注意**：原始文档中未明确列出支持的模型名称（如 `parsex-v1` 或 `parsex-video`），仅通过路径和 biz_id 前缀（如 `parseX-video-...`）间接体现。实际可用模型请以 [提交解析任务](../../raw/application-api-reference/api-overview/document-parsing/parse-submit.md) 中的 `model` 参数枚举为准，避免依赖 biz_id 命名推断。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `biz_id` | string | 是（结果查询时） | 异步任务唯一标识，由提交接口返回，用于轮询结果；见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `model` | string | 否（默认 `parsex-general`） | 指定解析模型，如 `parsex-video`、`parsex-contract`；不同模型对输入格式和字段 schema 有约束 |
| `file_url` / `file_bytes` | string / base64 | 是（二选一） | 文件来源，推荐使用 `file_url`（需公网可访问的直链）以提升大文件稳定性 |
| `schema` | object | 是（抽取任务） | 符合 JSON Schema Draft-07 的结构定义，决定输出字段粒度与校验规则 |

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`；  
2. **提交任务**：向 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x` 发送 POST 请求，Body 包含文件引用与配置；  
3. **轮询结果**：使用返回的 `biz_id` 调用 `/result` 接口（路径为 `/api/v2/apps/parse-x/result`），按 `data.status` 字段判断状态，直至 `success` 或 `failed`；  
4. **错误处理**：统一响应含 `code` 与 `message`，需结合 [错误码](../../raw/application-api-reference/api-overview/errors.md) 文档定位问题。

## 限制和注意事项

- 单次请求最大文件体积为 100 MB（音视频建议 ≤ 500 MB，但处理超时风险显著上升）；  
- `biz_id` 有效期为 7 天，过期后结果不可查，需重新提交；  
- 所有接口强制 HTTPS，明文 HTTP 请求将被网关拒绝；  
- 响应体 UTF-8 编码，非 UTF-8 字符（如 GBK 中文）可能导致解析失败；  
- 异步轮询建议间隔 ≥ 2 秒，高频请求可能触发限流（HTTP 429），具体配额见 [鉴权](../../raw/application-api-reference/api-overview/authentication.md) 文档。

## 来源文档

- [API 概览](../../raw/application-api-reference/api-overview.md)


