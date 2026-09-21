# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、功能扩展、参数配置与生命周期管理等核心环节。它面向开发者提供统一的 API 接口和 SDK 封装，用于构建生产级 AI 应用。该能力依赖平台底层模型服务与资源调度系统，需配合具体模型实例使用。

## 支持的模型/功能

- 支持调用百炼平台托管的全部大语言模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型（需通过 [应用接入协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 授权）；
- 提供 Prompt 工程支持（含变量注入、模板版本管理）、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应、多轮会话状态维护；
- 支持异步任务提交（如长文本摘要、批量推理），结果通过回调或轮询获取。  
> **注意**：文档中提及的“支持所有开源模型本地部署”与 [应用售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中明确限定“仅支持平台已上架模型”存在冲突，以售后说明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符（如 `qwen-max`, `qwen-plus`），必须在 [服务支持](../../raw/application-user-guide/application-support.md) 列出的可用模型列表内 |
| `temperature` | float | 否 | 采样温度（0.0–2.0），默认 1.0；值越低输出越确定 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；设为 `true` 时需按 SSE 协议解析 |
| `top_p` | float | 否 | 核采样阈值（0.0–1.0），默认 0.8 |

## 使用方式

1. 通过 `POST /v1/applications/{app_id}/chat/completions` 发起请求（需携带 `Authorization: Bearer <api_key>`）；  
2. 请求体为标准 OpenAI 兼容格式，但 `messages` 中 `role` 仅支持 `system`/`user`/`assistant`，不支持 `tool`（工具调用需使用专用 `/tools` 接口）；  
3. SDK 调用示例（Python）：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = bailian_models.Client(...)
   response = client.chat_completions(
       app_id="app-xxx",
       model="qwen-plus",
       messages=[{"role": "user", "content": "你好"}],
       stream=True
   )
   ```

## 限制和注意事项

- 单次请求最大 token 数受模型本身限制（如 `qwen-max` 为 32768），超出将返回 `400 Bad Request`；
- 流式响应下，若连接中断超过 60 秒未收到新 chunk，服务端将自动关闭连接；
- 异步任务最长保留结果 7 天，超期后无法查询；  
> **注意**：原始文档 [服务支持](../../raw/application-user-guide/application-support.md) 未说明 token 限制细节，实际行为应以 [应用常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中“Q：单次请求最大长度是多少？”条目为准。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


