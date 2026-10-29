# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境中的限制与注意事项。所有操作均基于 RESTful API 接口，无需安装额外 SDK（但 SDK 可选）。

## 支持的模型与核心功能

百炼平台提供多类预训练大语言模型（LLM）、多模态模型及专用小模型，涵盖文本生成、代码补全、对话理解、图像描述等能力。模型按能力、尺寸和部署形态分类，包括 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、Qwen-VL 多模态模型，以及部分第三方授权模型。详细模型列表与适用场景请参阅 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态推理能力（如流式响应、[函数调用](../concepts/function-calling.md)、工具集成）需结合对应模型版本启用，具体支持情况以 [产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中的功能矩阵为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：非空消息数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `parameters`（可选）：控制生成行为，常见字段有 `temperature`（0.0–2.0）、`top_p`、`max_tokens`（默认 1024，最大 8192）；
- `stream`（布尔值）：启用流式响应需设为 `true`，此时响应体为 SSE 格式。

> **注意**：`max_tokens` 的实际上限因模型而异——例如 `qwen-turbo` 最高支持 4096 tokens，而 `qwen-max` 支持 8192；该差异未在 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 中明确说明，应以各模型文档为准。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AccessKey ID / Secret），并确保对应账号已开通模型服务权限；
2. **构造请求**：使用 HTTPS POST 向对应地域的 Base URL 发送请求，例如华东1（杭州）地域的通用入口为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；
3. **发起调用**：参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供的 cURL 示例或 Python requests 代码片段，验证基础连通性；
4. **处理响应**：检查 HTTP 状态码（200 表示成功）、`output.text` 字段（非流式）或逐块解析 `data:` 行（流式）。

## 限制和注意事项

- 每个 API Key 默认享有每日配额与每分钟限流（RPS），具体额度由账号等级与资源包决定，详见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 和 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档；
- 请求体大小上限为 16 MB（含图片 base64 编码），单次请求中 `input.messages` 总长度不得超过模型上下文窗口（如 `qwen-max` 为 32768 tokens）；
- 地域选择影响延迟与合规性，务必通过 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 确认可用 endpoint，跨地域调用可能导致 403 错误或额外网络开销；
- 所有模型调用均受内容安全策略约束，含敏感词、违法信息或高频异常请求将被拦截并返回 400 错误，不计入配额。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


