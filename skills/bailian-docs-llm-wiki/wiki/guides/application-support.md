# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、功能扩展、参数配置与生命周期管理等核心环节。它面向开发者提供统一的 API 接口和 SDK 封装，用于构建生产级 AI 应用。该能力不直接暴露底层模型训练细节，而是聚焦于推理服务的稳定性、可配置性与可观测性。

## 支持的模型/功能

- 支持调用百炼平台托管的全部公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及用户私有微调模型（需完成模型部署并授权）  
- 提供标准功能：文本生成、流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）、多轮对话状态管理、输入/输出内容安全过滤（默认启用）  
- 不支持直接访问模型权重或自定义前/后处理算子；如需定制化预处理逻辑，须通过 [应用网关插件](../../raw/application-user-guide/application-support.md) 实现。该文档明确指出：“所有预处理必须在请求进入 application [support](support.md) 服务前完成”。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，例如 `qwen-max` 或 `my-finetuned-model-202405`；必须已在控制台完成部署并处于 `ACTIVE` 状态 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应；注意流式模式下 `max_tokens` 为硬限制，超限将中断流 |
| `top_p` / `temperature` | float | 否 | 控制生成多样性；二者不可同时为 0（否则触发确定性采样冲突），详见 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中“参数组合约束”章节 |
| `tools` | array | 否 | [函数调用](../concepts/function-calling.md)工具列表，格式遵循 OpenAI 兼容 schema；工具执行失败时默认返回 `tool_calls` 字段为空数组，而非抛出错误 |

> **注意**：原始文档 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中称 `n` 参数可用于并行生成多条结果，但该功能已于 v2.3.0 版本移除，当前 API 返回 `400 Bad Request`；请改用客户端并发请求实现类似效果。

## 使用方式

1. **HTTP 调用**：向 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat/completions` 发送 POST 请求（需携带 `Authorization: Bearer <api_key>`）  
2. **SDK 调用**（推荐）：使用 `dashscope` Python SDK v1.18.0+，示例：
   ```python
   from dashscope import Application
   resp = Application.call(app_id='app-xxx', model='qwen-plus', messages=[{'role': 'user', 'content': '你好'}])
   ```
3. 所有请求均需通过应用 ID（`app_id`）路由，该 ID 在控制台「应用管理」中创建并绑定模型；未绑定模型的应用调用将返回 `404 Not Found`，而非模型加载失败提示。

## 限制和注意事项

- 单次请求最大上下文长度受所选模型原生限制约束（如 `qwen-max` 为 32768 tokens），`application support` 层不额外截断，但超出模型上限将导致 `400` 错误  
- 流式响应中 `usage` 字段仅在流结束时的 final chunk 中返回；中间 chunk 的 `usage` 均为 `null` —— 此行为与 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 第 4.2 条一致  
- 每个应用默认 QPS 限制为 5，可通过提交工单申请提升；突发流量超过配额时，服务返回 `429 Too Many Requests`，不进行排队或降级  
- 不支持跨区域调用：`app_id` 所属地域必须与 API Endpoint 地域一致（如华东1区应用不可调用华北2区 endpoint）

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


