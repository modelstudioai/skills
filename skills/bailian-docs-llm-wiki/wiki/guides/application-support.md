# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型推理、功能扩展、参数配置及生命周期管理等核心环节。它面向开发者提供统一的 API 接口与 SDK 封装，支撑 Web 应用、小程序、企业系统等多端集成场景。该能力依赖平台底层模型服务与资源调度机制，需配合正确的认证与配额策略使用。

## 支持的模型/功能

- 支持调用百炼全系列大模型（如 Qwen-Max、Qwen-Plus、Qwen-Turbo）及自定义微调模型（需已部署至应用环境）  
- 提供流式响应（`stream=true`）、[函数调用](../concepts/function-calling.md)（`tools`）、多轮对话状态保持（`conversation_id`）等高级功能  
- 支持异步任务提交（`async=true`）与结果轮询，适用于长耗时任务（如文档解析、批量生成）  
- 详细能力清单见 [服务支持](../../raw/application-user-guide/application-support.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`；必须与 [服务支持](../../raw/application-user-guide/application-support.md) 中列出的可用模型一致 |
| `input` | object | 是 | 包含 `messages`（对话历史）和可选 `parameters`（温度、top_p 等） |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流，需按 [服务支持](../../raw/application-user-guide/application-support.md) 的流式协议解析 |

## 使用方式

1. **HTTP 调用**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` 发送 POST 请求，携带 `Authorization: Bearer <api_key>` 与 JSON body  
2. **SDK 调用**（Python 示例）：
   ```python
   from dashscope import Generation
   response = Generation.call(model='qwen-max', input={'messages': [{'role': 'user', 'content': '你好'}]})
   ```
3. 所有请求均需通过百炼控制台申请对应模型的调用权限，并确保账号处于有效计费状态 —— 具体权限配置路径参见 [服务支持](../../raw/application-user-guide/application-support.md)

## 限制和注意事项

- 单次请求最大 token 数受模型限制（如 Qwen-Max 为 8192），超限将返回 `400 Bad Request`  
- 流式响应中 `event: error` 事件不保证包含完整错误码，建议同时检查 HTTP 状态码与响应头 `X-DashScope-Status`  
- > **注意**：原始文档中提及的 `async_mode` 参数在 v2.3+ SDK 中已弃用，应改用 `task` 接口并参考最新 [服务支持](../../raw/application-user-guide/application-support.md) 文档中的异步流程说明  
- 免费试用额度仅适用于指定模型（如 `qwen-turbo`），调用其他模型将立即计入付费账单  
- 自定义模型若未完成「上线验证」流程，调用将返回 `404 Not Found`，而非 `401 Unauthorized`

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


