# application component api reference

应用组件 API 是百炼平台提供的核心能力封装，用于在自定义应用中集成大模型推理、知识库检索、工作流编排等能力。该接口统一采用 RESTful 风格设计，支持通过 HTTP 请求调用，并要求使用 RAM 凭据进行身份鉴权。所有功能均基于百炼平台托管的模型与服务运行，开发者无需自行部署模型或维护基础设施。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：
- **大模型推理**：调用 `qwen-max`、`qwen-plus`、`qwen-turbo` 等 Qwen 系列模型（具体支持列表见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)）；
- **知识库增强问答**：绑定指定知识库 ID 后，自动启用 RAG 检索与答案生成；
- **多步骤工作流执行**：通过 `workflow_id` 参数触发预置工作流，支持条件分支与异步回调。

> **注意**：文档中提及的 `qwen-vl` 和 `qwen-audio` 模型在最新 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中已被标记为“已下线”，实际调用将返回 `404 Not Found`，请勿在生产环境使用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-plus`；必须与 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的可用模型一致 |
| `input` | object | 是 | 包含 `messages`（对话历史）或 `prompt`（单轮提示词）的输入结构 |
| `parameters` | object | 否 | 推理参数，如 `temperature`（0.0–2.0）、`max_tokens`（默认2048，上限8192） |
| `knowledge_id` | string | 否 | 绑定知识库时必填，需为已在控制台创建并发布的知识库 ID |

## 使用方式

1. 获取服务接入点：参考 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 获取 Region 对应的 endpoint URL（如 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat`）；  
2. 构造 HTTP POST 请求，Header 中携带 `Authorization: Bearer <api_key>` 或使用 RAM STS [Token](../concepts/token.md)（详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）；  
3. Body 使用 JSON 格式，示例：
```json
{
  "model": "qwen-plus",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.7}
}
```

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 32 轮对话历史，总 token 数不得超过模型上下文长度（`qwen-plus` 为 8192）；
- 免费试用额度仅适用于 `qwen-turbo`，其他模型按量计费，计费粒度为千 tokens；
- 异步工作流调用需额外配置回调地址，且回调超时时间为 60 秒，超时后任务状态变为 `failed`；
- 所有请求必须在 `X-DashScope-Date` Header 中提供 ISO8601 格式时间戳（精确到秒），偏差超过 15 分钟将被拒绝。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


