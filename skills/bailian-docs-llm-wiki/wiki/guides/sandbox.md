# sandbox

sandbox 是百炼平台提供的轻量级模型实验与调试环境，支持开发者快速验证提示词、参数配置及多轮对话逻辑，无需部署完整应用。它面向单次推理或短周期交互场景，适用于模型选型、Prompt 工程和 SDK 集成前的功能验证。所有操作均通过 API 或控制台触发，实例生命周期由平台自动管理。

## 支持的模型与功能

sandbox 当前支持以下模型：`qwen-max`、`qwen-plus`、`qwen-turbo`（仅限文本生成），以及 `qwen-vl-plus`（多模态输入）。不支持微调模型或自定义 LoRA。功能上支持单次 completion、流式响应、system/user/assistant 角色消息结构，以及基础的 tool calling（需显式启用 `enable_tool_choice: true`）。图像上传仅限 base64 编码的 JPEG/PNG，最大 5MB。详细能力说明见 [Sandbox](../../raw/application-user-guide/sandbox.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为 sandbox 支持列表中的值 |
| `input.messages` | array | 是 | 至少包含一条 `user` 消息，`system` 消息可选且仅首条生效 |
| `parameters.temperature` | number | 否 | 范围 0.0–2.0，默认 1.0；设为 0 时启用确定性采样 |
| `parameters.top_p` | number | 否 | 范围 0.0–1.0，默认 0.8 |
| `stream` | boolean | 否 | 设为 `true` 启用 SSE 流式响应，此时 `output` 字段不返回完整结果 |

> **注意**：`max_tokens` 参数在 [sandbox-quick-start.md](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 中被列为推荐设置，但实际 API 会忽略该字段——sandbox 使用动态 token 分配策略，由模型自身决定输出长度，此行为与 [sandbox-sdk.md](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 中的说明一致。

## 使用方式

1. **API 调用**：向 `POST /v1/sandbox/completions` 发送 JSON 请求，需携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；
2. **控制台操作**：进入「应用开发」→「Sandbox」页面，选择模型、填写消息后点击「运行」，结果实时渲染并支持复制 raw response；
3. **SDK 集成**：Python SDK 中调用 `client.sandbox.completions.create(...)`，参数结构与 API 完全对齐，详见 [sandbox-sdk.md](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- 单次请求最大上下文长度为 32,768 tokens（含 input + output），超限将返回 `400 Bad Request`；
- 每个 API Key 默认 QPS 限制为 5，可通过工单申请提升；
- sandbox 实例无状态，不保存历史会话，连续多轮交互需客户端自行维护 `messages` 数组；
- 不支持异步批量提交（`batch_size > 1`）或后台任务队列；
- 所有请求日志保留 7 天，不用于训练或模型优化，符合百炼数据治理规范。

## 来源文档

- [Sandbox](../../raw/application-user-guide/sandbox.md)


