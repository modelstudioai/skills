# capabilities

`capabilities` 是百炼平台用于查询和管理模型能力（如支持的模型、功能接口、参数约束等）的核心模块，为开发者提供标准化的能力发现与调用依据。它不直接执行推理或训练，而是作为元能力描述层，支撑 CLI、SDK 和控制台的一致性行为。所有能力声明均以平台当前生产环境实际可用状态为准，动态同步至服务端配置。

## 支持的模型/功能

当前 `capabilities` 模块覆盖以下四类能力域：
- **模型调用**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分第三方开源模型（如 `llama3-8b`）的同步/流式推理；支持多模态输入（图像 URL + 文本）仅限 `qwen-vl-plus` 等显式标注多模态能力的模型。详情见 [模型调用](../../raw/cli/capabilities/model-invocation.md)。
- **模型训练与部署**：支持 LoRA 微调、全参微调及 Serverless 推理部署，但仅对白名单模型开放（如 `qwen-turbo` 支持 LoRA，`qwen-max` 不支持全参微调）。具体支持矩阵请参考 [模型训练与部署](../../raw/cli/capabilities/training-deployment.md)。
- **Agent 基础设施**：提供工具调用（Tool Calling）、记忆管理（Memory）、多步规划（Planning）等基础能力，但 `plan` 能力在 `qwen-plus` 中默认启用，而 `qwen-turbo` 需显式开启 `enable_planning=true`。该差异已在 [Agent 基础设施](../../raw/cli/capabilities/agent-infrastructure.md) 中明确说明。
- **平台管理与工具**：包括密钥轮换、配额查询、事件日志订阅等运维能力，全部通过 `/v1/capabilities/platform` 接口暴露。

> **注意**：原始文档中 `raw/cli/capabilities/agent-infrastructure.md` 提到 “所有模型默认启用 tool_choice=auto”，但实测 `qwen-turbo` 在未设置 `tool_choice` 时仍返回 raw text。该描述已过时，请以 [Agent 基础设施](../../raw/cli/capabilities/agent-infrastructure.md) 的最新注释为准。

## 关键参数

调用 `GET /v1/capabilities` 时可传入以下查询参数：
- `model`（必选）：指定模型 ID，如 `qwen-plus`；
- `capability`（可选）：过滤特定能力类型，如 `tool_calling`、`vision`、`streaming`；
- `version`（可选）：指定模型版本（如 `20240601`），若不传则返回最新稳定版能力。

响应体中关键字段包括：
- `supports_streaming`: 布尔值，标识是否支持流式响应；
- `max_input_tokens` / `max_output_tokens`: 整数，表示该模型实例的实际上下文窗口限制；
- `tool_types`: 字符串数组，如 `["function", "retrieval"]`，反映当前模型可解析的工具类型。

## 使用方式

- **CLI**：`bailian capabilities list --model qwen-plus --capability vision`
- **HTTP API**：`GET https://dashscope.aliyuncs.com/api/v1/capabilities?model=qwen-plus&capability=tool_calling`
- **Python SDK**：  
  ```python
  from bailian import CapabilitiesClient
  client = CapabilitiesClient()
  caps = client.get(model="qwen-turbo", capability="streaming")
  ```

所有调用均需携带有效的 `Authorization: Bearer <api_key>`。更多示例见 [模型调用](../../raw/cli/capabilities/model-invocation.md)。

## 限制和注意事项

- 单次请求最多返回 100 条能力记录，分页需使用 `cursor` 参数（响应头中 `X-Next-Cursor` 提供）；
- `model` 参数必须为平台注册的合法模型 ID，拼写错误将返回 `404 Not Found`，而非能力为空；
- 能力数据每 5 分钟从服务端同步一次，缓存 TTL 为 300 秒，因此新上线模型的能力可能延迟生效；
- 多模态能力（如 `vision`）仅当 `model` 显式声明 `input_types: ["image_url", "text"]` 时才返回 `true`，不可依赖模型名称推断（例如 `qwen-plus` 不代表支持图像输入）。

## 来源文档

- [能力参考](../../raw/cli/capabilities.md)


