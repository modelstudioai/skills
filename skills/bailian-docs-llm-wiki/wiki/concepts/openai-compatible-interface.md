# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组遵循 OpenAI API 协议的调用端点，开发者无需修改已有的 OpenAI SDK 代码，只需替换 `api_key`、`base_url` 和 `model` 三个参数即可接入百炼的模型服务。

## 接口类型

百炼兼容的 OpenAI 接口覆盖多种能力，调用路径均位于 `compatible-mode/v1` 下：

| 接口 | HTTP 路径 | 典型场景 |
| --- | --- | --- |
| Chat Completions | `POST /chat/completions` | 多轮对话、function call、[流式输出](streaming.md) |
| Responses | `POST /responses` | 智能体原生能力、内置工具（联网搜索、代码解释器、网页内容提取）、自动上下文管理 |
| Completions | `POST /completions` | 代码补全、文本续写（FIM） |
| Embeddings | `POST /embeddings` | 文本向量化 |
| Vision | 走 Chat Completions | 图像/视频理解 |
| File | `POST /files` 等 | 上传/查询/删除文件 |
| Batch | `POST /batches` | 异步批量推理，费用 50% |
| Conversations | `POST /conversations` | 跨设备会话状态管理 |

其中 **Chat Completions** 是最常用的接口，支持 Qwen 全系列、DeepSeek、Kimi、GLM、MiniMax 等大语言模型；**Responses** 接口是 Chat Completions 的演进版本，内置联网搜索、代码解释器和网页内容提取工具，并由平台自动管理对话历史，无需在请求中手动拼接 `messages`。

百炼还提供 Anthropic 兼容接口和 DashScope 原生接口。当 OpenAI 兼容接口无法满足全部参数需求时，可考虑使用 DashScope 原生接口获取最完整的功能集。

## 接入三要素

从 OpenAI 迁移到百炼时，需要替换以下三项配置：

- **api_key**：替换为百炼 [API Key](api-key.md)，建议通过环境变量 `DASHSCOPE_API_KEY` 注入。不同地域的 [API Key](api-key.md) 相互独立，不能跨地域混用。
- **base_url**：使用[业务空间](workspace.md)专属域名，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`，其中 `{WorkspaceId}` 为[业务空间](workspace.md) ID。
- **model**：替换为百炼支持的模型名称，如 `qwen3.7-max`、`qwen3.7-plus`、`deepseek-v4-pro` 等。

## 各地域 Base URL

| 地域 | Base URL |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`（Responses 接口） |

> 弗吉尼亚地域使用固定域名，不带 `{WorkspaceId}`；其余地域均需替换为真实[业务空间](workspace.md) ID。

订阅套餐用户使用专属域名：

| 套餐 | Base URL |
| --- | --- |
| [Token](token.md) Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |

三类 [API Key](api-key.md) 与 Base URL 互不相通，误用会导致 401/403 错误。

## 快速上手

安装 OpenAI Python SDK 后即可调用：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ]
)
print(completion.choices[0].message.content)
```

## 支持的第三方工具

百炼的 OpenAI 兼容接口可直接对接主流 AI 编程工具和聊天客户端：

- **终端 CLI**：Claude Code、Codex、Qwen Code、OpenCode、Kilo CLI 等
- **桌面客户端**：Cherry Studio、Chatbox、QwenPaw
- **IDE 插件**：Cursor、Cline、Qoder
- **开发平台**：Dify、LangChain、LangChain4j

这些工具只需在配置中填入百炼的 API Key 和 Base URL 即可完成接入。

## 应用调用

百炼的智能体和工作流应用也支持通过 OpenAI 兼容的 Responses API 调用，Endpoint 格式为：

```
POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses
```

支持同步/[异步调用](async-invocation.md)、多轮对话、[流式输出](streaming.md)和[多模态](multimodal.md)输入。

## 限制与注意事项

- **功能完整度**：兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数。如需最完整的采样参数和业务字段，建议使用 DashScope 原生接口。
- **工具能力差异**：联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力，Chat Completions 接口不内置这些工具。
- **对话历史管理**：仅 Responses 接口自动维护对话历史，其余接口需由调用方自行管理上下文。
- **模型兼容性**：部分专用模型（如 `qwen-deep-research`）暂不支持 OpenAI 兼容接口，仅支持 [DashScope SDK](dashscope-sdk.md) 调用。`Qwen-Audio` 同样仅支持 DashScope 协议。
- **地域限制**：[Token](token.md) Plan 团队版仅支持华北2（北京）地域；三方直供模型仅在中国站的中国内地地域可用。
- **迁移评估**：从 OpenAI 迁移时，应先确认目标模型在兼容接口下是否支持所需参数（如 `temperature`、`tools`、`stream` 等），再决定接口选型。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [get started with models](../guides/get-started-with-models.md)
- [more models](../api/more-models.md)
- [token plan guide](../guides/token-plan-guide.md)
- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)


