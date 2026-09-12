# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。你将了解支持的模型类型、关键调用参数、基础使用方式，以及必须注意的服务限制与配置要求。所有操作均基于标准 REST API 接口，无需额外 SDK 即可集成。

## 支持的模型与功能

百炼平台当前提供多类预训练大语言模型（如 Qwen 系列）、[多模态](../concepts/multi-modal.md)模型及定制化推理服务，覆盖文本生成、代码补全、对话理解等场景。模型列表及能力说明详见 [选择模型](../../raw/model-user-guide/get-started-with-models.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（function calling）和自定义 system [prompt](prompt.md)，具体以各模型文档为准。动态推理能力（如工具调用、结构化输出）需配合对应参数启用，参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models.md) 中的示例。

## 关键参数

调用模型 API 时，以下参数为必需或强推荐：

- `model`: 模型标识符（如 `qwen-max`, `qwen-plus`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models.md) 中公布的名称严格一致；
- `input.messages`: 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `parameters.temperature`: 控制输出随机性（0.0–2.0），默认值因模型而异；
- `parameters.max_tokens`: 输出长度上限，超出将被截断；
- `headers.Authorization`: Bearer [Token](../concepts/token.md) 形式，需通过阿里云 RAM 凭据或 API Key 获取。

> **注意**：`base_url` 不再统一固定为 `https://dashscope.aliyuncs.com/`；实际接入地址取决于所选地域和服务部署范围，请务必查阅 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models.md)，否则请求将返回 404 或 403。

## 使用方式

1. 登录 [Model Studio 控制台](https://dashscope.console.aliyun.com/)，开通服务并获取 API Key；
2. 根据目标模型确定 `base_url` 和 `model` 名称（参见 [Base URL总览](../../raw/model-user-guide/get-started-with-models.md) 和 [选择模型](../../raw/model-user-guide/get-started-with-models.md)）；
3. 构造 HTTP POST 请求，`Content-Type: application/json`，Body 包含 `model` 和 `input` 字段；
4. 发送请求并处理响应（成功状态码为 `200`，流式响应需按 SSE 协议解析）。

示例 cURL 命令可在 [首次调用千问API](../../raw/model-user-guide/get-started-with-models.md) 中直接复用。

## 限制和注意事项

- 所有模型调用受动态限流策略约束，配额按账号维度分配，不可跨账号共享；详细规则见 [动态限流](../../raw/model-user-guide/get-started-with-models.md)；
- 单次请求 `input.messages` 总 token 数（含 [prompt](prompt.md) + completion）不得超过模型上下文窗口限制（例如 `qwen-max` 为 32768），超限将触发 `400 Bad Request`；
- 非中国大陆地域节点（如 ap-southeast-1）暂不支持部分新模型，部署前请确认 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models.md) 中的可用性说明；
- `parameters.top_p` 与 `temperature` 同时设置时，优先级行为未在文档中明确定义，建议避免同时高灵敏度调整二者。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)



