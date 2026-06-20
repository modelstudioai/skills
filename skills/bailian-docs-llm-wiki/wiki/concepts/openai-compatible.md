# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一种 API 协议，允许开发者使用 OpenAI SDK 和工具直接调用百炼上的模型服务，只需替换 API Key 和 Base URL，无需修改业务代码。

## 工作原理

百炼实现了与 OpenAI Chat Completions API 兼容的端点，接受相同的请求格式并返回相同结构的响应。开发者已有的 OpenAI 生态代码可以零成本迁移到百炼平台，同时享受千问（Qwen）系列及 DeepSeek、Kimi、GLM 等第三方模型的能力。

## 支持的协议变体

百炼在 OpenAI 兼容的基础上提供了两个层级的接口：

- **Chat Completions**：标准的对话补全接口，与 OpenAI 客户端库直接兼容，适合大多数文本生成、对话、代码生成场景。
- **Responses**：在 Chat Completions 基础上扩展，内置联网搜索、代码解释器、网页内容提取等工具能力，并可自动管理对话历史，适合需要工具调用的复杂场景。

> 百炼还提供 Anthropic 兼容 Messages 接口和 DashScope 原生接口。DashScope 原生接口功能最完整，但 OpenAI 兼容接口迁移成本最低。

## Base URL 配置

不同计费方案和地域对应不同的 Base URL，配置时必须确保 API Key 与 Base URL 来自同一方案：

| 计费方案 | Base URL |
|---------|----------|
| 按量计费（华北2/北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 按量计费（北京，含 WorkspaceId） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 按量计费（新加坡） | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 按量计费（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |

北京和新加坡地域推荐使用含 WorkspaceId 的新版专属域名，性能和稳定性更好。

## 快速接入示例

使用 OpenAI Python SDK 调用百炼模型：

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DASHSCOPE_API_KEY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}]
)
print(completion.choices[0].message.content)
```

Node.js、curl 等其他语言/工具的接入方式类似，只需设置对应的 `api_key` 和 `base_url`。

## 适用场景

- **模型推理**：文本生成、视觉理解、机器翻译、意图识别等模型均支持通过 OpenAI 兼容接口调用。
- **应用调用**：百炼智能体和工作流应用提供 Responses API（OpenAI 兼容），支持同步/异步调用。
- **第三方工具接入**：Cursor、Cline、Claude Code、Codex、Qwen Code 等 AI 编程工具和聊天客户端均可通过 OpenAI 兼容协议接入百炼。
- **子[业务空间](workspace.md)**：子空间的 API Key 同样支持通过 OpenAI 兼容接口调用已授权的模型。

## 注意事项

- 三种计费方案（按量计费、Token Plan、Coding Plan）的 API Key 互不通用，不能跨方案混用。
- 部分高级功能（如批量推理、模型调优后的模型调用）可能仅支持 DashScope 原生接口，不支持 OpenAI 兼容方式。
- 部分专用模型（如 Qwen-Deep-Research）暂不支持 OpenAI 兼容接口。
- 在第三方工具中使用时，部分模型名称可能需要使用别名格式（如 Cursor 中 `kimi-k2.6` 需写为 `kimi-k2-6`）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model inference](../guides/model-inference.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more models](../api/more-models.md)
- [more about models](../api/more-about-models.md)


