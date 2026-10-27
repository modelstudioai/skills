# api overview

ParseX API 提供文档解析与结构化信息抽取的编程接口，所有能力通过 DashScope 网关统一接入。接口采用标准 RESTful 设计，基于 HTTPS 协议、JSON 格式通信，支持异步任务提交与轮询获取结果。开发者需使用有效的 `DASHSCOPE_API_KEY` 进行认证。

## 支持的模型/功能

- **文档解析**：支持 PDF、Word、Excel、PPT、图片（含扫描件）、纯文本等格式的版面分析、文字识别与语义分块；  
- **音视频解析**：支持 MP4、MOV、AVI 等常见格式的语音转写、关键帧提取与时间轴对齐；  
- **结构化抽取**：基于用户提供的 JSON Schema，从解析结果中抽取指定字段（如合同金额、签署方、生效日期等），详见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md)；  
- 所有功能均以异步方式执行，不提供同步阻塞式调用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `biz_id` | string | 是（结果查询时） | 由提交接口返回，用于轮询任务状态和获取最终结果；首次提交时不可传入 |
| `file_url` 或 `file_bytes` | string / binary | 是（提交时） | 指定待处理文件来源；`file_url` 需为公网可访问的 HTTPS 地址，`file_bytes` 以 base64 编码嵌入请求体 |
| `schema` | object | 否（抽取任务必填） | 符合 JSON Schema Draft-07 的结构定义，决定抽取字段的类型、约束与嵌套关系；详见 [提交抽取任务](../../raw/application-api-reference/api-overview/field-extraction/extract-submit.md) |
| `parse_config` | object | 否 | 控制解析粒度（如是否启用表格识别、公式识别、OCR 精度模式等），具体字段见 [API 概览](../../raw/application-api-reference/api-overview.md) |

> **注意**：原始文档中 `parse_config` 的可用字段未在 [API 概览](../../raw/application-api-reference/api-overview.md) 中完整列出，实际支持项请以最新 SDK 文档或 OpenAPI Spec 为准；部分配置项（如 `"enable_formula": true`）在 v2.3+ 版本才生效，旧版调用将被忽略。

## 使用方式

1. **认证准备**：在 DashScope 控制台获取 `DASHSCOPE_API_KEY`，并按要求设置请求头：  
   ```http
   Authorization: Bearer $DASHSCOPE_API_KEY
   Content-Type: application/json
   ```
2. **提交任务**：向 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/parse-x` 发送 POST 请求，路径后缀根据功能选择（如 `/parse` 或 `/extract`），请求体包含文件引用与可选配置；  
3. **轮询结果**：使用响应中的 `biz_id` 调用 `/result` 接口（如 `/api/v2/apps/parse-x/result?biz_id=xxx`），直到 `data.status` 为 `"success"` 或 `"failed"`；  
4. **解析响应**：成功时 `data.result` 包含结构化输出（如 `pages`, `tables`, `fields` 等），失败时参考 [错误码](../../raw/application-api-reference/api-overview/errors.md) 定位问题。

## 限制和注意事项

- 单次请求最大文件体积为 100 MB（音视频建议 ≤ 500 MB，但处理耗时显著增加）；  
- `biz_id` 有效期为 7 天，超期后结果接口返回 `404`；  
- 同一 `workspaceId` 下并发任务数默认上限为 20，可通过工单申请提升；  
- 所有接口仅支持 HTTPS，明文 HTTP 请求将被网关拒绝；  
- 响应中 `request_id` 是排查问题的唯一追踪标识，务必在日志中持久化记录；  
- 异步流程中若连续 5 次轮询间隔 < 1s，可能触发限流，建议采用指数退避策略（如 1s → 2s → 4s → 8s）。

## 来源文档

- [API 概览](../../raw/application-api-reference/api-overview.md)


