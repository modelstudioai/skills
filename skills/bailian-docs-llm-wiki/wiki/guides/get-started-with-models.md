# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API调用基础配置、关键参数设置及使用约束。所有操作均基于标准 RESTful API 接口，无需额外 SDK 即可完成集成。建议首次使用者按顺序阅读 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 中的引导路径。

## 支持的模型与功能

百炼平台提供多类大语言模型（如 Qwen 系列）、[多模态](../concepts/multi-modal.md)模型及推理优化版本（如 `qwen-max`、`qwen-plus`、`qwen-turbo`），支持文本生成、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应（stream）、工具调用（tool_choice）等核心能力。完整模型列表及特性说明见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型还支持图像输入（需配合 `messages[].content` 中的 `image_url` 字段），具体兼容性请以该文档为准。

## 关键参数

调用模型 API 时，必需参数包括：  
- `model`: 模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；  
- `messages`: 对话历史数组，格式为 `[{ "role": "user", "content": "..." }]`；  
- `api_key`: 从控制台获取的密钥，需通过 `Authorization: Bearer <api_key>` 传递；  
- `base_url`: 根据部署地域选择，例如 `https://dashscope.aliyuncs.com/api/v1`（公共云）或专有云定制地址，详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

> **注意**：[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中列出的部分旧域名（如 `https://api-dashscope.aliyuncs.com`）已弃用，实际应优先采用 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 中标注的当前有效地址。

## 使用方式

1. 登录百炼控制台，创建 API Key 并确认配额状态（参见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)）；  
2. 根据目标模型和业务场景，参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 完成最小可行请求（cURL 或 Python 示例）；  
3. 验证响应结构（含 `id`、`choices[0].message.content`、`usage` 等字段），并按需启用 `stream=true` 实现逐 token 返回。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 [prompt](prompt.md) + completion）受模型上下文窗口限制（如 `qwen-turbo` 为 8K tokens），超长将返回 `400 Bad Request`；  
- 免费试用额度仅适用于指定模型（如 `qwen-turbo`），其他模型需开通后付费，详情见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)；  
- 流式响应中 `delta.content` 可能为空字符串（尤其在 function call 场景），客户端需容错处理；  
- 所有调用受账户级 QPS 和 TPS 限制，突发流量可能触发 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)，建议实现指数退避重试逻辑。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


