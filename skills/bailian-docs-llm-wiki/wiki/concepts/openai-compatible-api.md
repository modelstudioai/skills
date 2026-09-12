# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 官方 API 的路径、请求/响应结构、字段命名与语义规范（如 `/v1/chat/completions`），使开发者能直接复用现有 OpenAI 客户端（如 `openai>=1.0` SDK）、工具链（Dify、LangChain、Cursor 等）和工作流代码，无需修改业务逻辑即可接入 Qwen 系列大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与原型验证**：已有 OpenAI 项目只需替换 `api_key` 和 `base_url`，即可调用 `qwen-max`、`qwen-plus`、`qwen-turbo` 等文本模型，大幅降低迁移成本；  
- **第三方工具集成**：支持 Chatbox、Dify、Hermes Agent、Postman、LangChain 等主流客户端与框架，通过配置 `base_url=https://dashscope.aliyuncs.com/compatible-mode/v1` 即可开箱即用；  
- **结构化输出与批量处理**：支持 `response_format={"type": "json_object"}`（需模型兼容）、`/v1/batches` 批量推理、`/v1/files` 文件上传与管理等高级能力，适用于生产级自动化任务；  
- **智能体增强场景**：通过 **OpenAI兼容-Responses** 子模式，额外启用联网搜索、代码解释器、网页提取等内置工具，自动维护对话历史，适合构建免开发的智能体应用；  
- **评测与对比实验**：模型评测系统支持将 OpenAI 兼容接口作为标准接入方式之一，实现多模型（含第三方模型）在统一协议下的横向性能比对。

> ⚠️ 注意：`qwen-vl`、`qwen-audio` 等多模态模型**不支持** OpenAI 兼容接口，必须使用 DashScope 原生接口；`system` 消息、`logprobs`、`top_k`、`repetition_penalty` 等高级参数也仅在 DashScope 原生接口中可用。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 百炼实际部署的模型 ID，如 `"qwen-max"`、`"qwen-plus"`；不可使用 `gpt-4` 等别名 |
| `api_key` | string | 是 | 百炼平台生成的 DashScope API Key（格式为 `sk-xxx`），非阿里云 AccessKey |
| `base_url` | string | 是（客户端侧） | 固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `messages` | array | 是（chat 接口） | 标准 OpenAI 格式：`[{"role": "user", "content": "..."}, ...]`；`system` 角色**不支持** |
| `stream` | boolean | 否 | 启用流式响应（默认 `false`），返回 `data: {...}` 行格式，需按 SSE 协议解析 |
| `response_format` | object | 否 | 控制输出结构，如 `{"type": "json_object"}`（仅 `qwen-max` 等部分模型支持） |
| `tools` / `tool_choice` | object/array | 否 | 仅 **OpenAI兼容-Responses** 支持完整工具调用协议（需显式启用该模式） |

## 面向开发者，简洁实用

✅ **推荐做法**：  
- 使用官方 `openai` Python SDK（v1.0+）调用，代码零改造：  
  ```python
  from openai import OpenAI
  client = OpenAI(api_key="sk-xxx", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
  response = client.chat.completions.create(model="qwen-plus", messages=[{"role":"user","content":"你好"}])
  ```

✅ **调试建议**：  
- 首先用 `curl` 验证基础连通性（参考 [qwen api reference](../../raw/model-api-reference/qwen-api-reference.md) 中示例）；  
- 流式响应请按 `data:` 前缀逐行解析，避免依赖工具默认的 OpenAI 解析逻辑（部分旧版工具存在丢帧风险）；  
- 工具类调用务必确认是否启用 **OpenAI兼容-Responses** 模式（Endpoint 相同，但需服务端开启增强能力）。

❌ **禁止行为**：  
- 尝试在 OpenAI 兼容接口中传入 `system` 消息或 `top_k` 等非标准参数（将被忽略或报错）；  
- 对多模态模型（`qwen-vl-plus` 等）使用该接口（会返回 404 或模型不支持错误）；  
- 混用不同地域的 API Key 与 Endpoint（如华东1区 Key 不可用于国际站域名）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


