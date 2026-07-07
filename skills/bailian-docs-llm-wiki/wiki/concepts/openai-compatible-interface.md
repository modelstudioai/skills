# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组遵循 OpenAI API 协议规范的接口，开发者只需将 `api_key`、`base_url`、`model` 三个参数替换为百炼的值，即可复用现有 OpenAI SDK 和生态工具直接调用百炼模型服务，实现最低成本的迁移接入。

## 覆盖的接口类型

百炼兼容的 OpenAI 接口覆盖以下能力，调用路径均挂载在 `compatible-mode/v1` 下：

| 接口 | HTTP 路径 | 典型场景 |
| --- | --- | --- |
| Chat Completions | `POST /chat/completions` | 多轮对话、function call、[流式输出](streaming.md) |
| Responses | `POST /responses` | 智能体原生能力、内置工具（联网搜索、代码解释器、网页抓取）、自动管理对话历史 |
| Completions | `POST /completions` | 代码补全、文本续写（FIM） |
| Embeddings | `POST /embeddings` | 文本向量化 |
| Vision | 走 Chat Completions | 图像/视频理解 |
| File | `POST /files` 等 | 文件上传/查询/删除 |
| Batch | `POST /batches` | 异步批量推理（费用 50%） |
| Conversations | `POST /conversations` | 跨设备会话状态管理 |

其中 Chat Completions 是最常用的接口，支持 Qwen 全系列、DeepSeek、Kimi、GLM、MiniMax 等模型；Responses 接口作为 Chat Completions 的演进版本，额外内置联网搜索、代码解释器和网页内容提取，并由平台自动管理对话历史。

## 接入三要素

所有兼容接口的迁移都围绕以下三个参数：

- **api_key**：替换为百炼 API Key，建议通过环境变量 `DASHSCOPE_API_KEY` 注入。不同计费方案（按量计费、Token Plan 团队版、Coding Plan）的 API Key 互不通用。
- **base_url**：使用[业务空间](workspace.md)专属域名，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`，其中 `{WorkspaceId}` 为[业务空间](workspace.md) ID。不同计费方案和地域的 Base URL 不能混用。
- **model**：指定目标模型名称，如 `qwen3.7-plus`、`deepseek-v4-pro` 等。

### 各地域 Base URL

| 地域 | Base URL |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`（仅 Responses 接口） |

### 订阅套餐专属 Base URL

| 方案 | Base URL |
| --- | --- |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |

## 调用示例

以 Python 为例，使用 OpenAI SDK 调用百炼 Qwen 模型：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

Node.js 和 curl 的用法同理，只需替换对应的 api_key、base_url 和 model 即可。

## 在不同场景中的使用

- **模型直接调用**：通过 Chat Completions 或 Responses 接口调用 Qwen、DeepSeek、Kimi 等文本生成模型，以及翻译模型（qwen-mt-plus）、OCR 模型（qwen3.5-ocr）、GUI 交互模型（gui-plus）等专用模型。
- **应用调用**：百炼智能体和工作流应用支持通过 OpenAI 兼容的 Responses API 调用，Endpoint 为 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，支持同步、异步和[流式输出](streaming.md)。
- **AI 编程工具接入**：Claude Code、Cursor、Cline、OpenCode 等终端工具均可通过 OpenAI 兼容协议接入百炼，配置对应的 API Key 和 Base URL 即可。
- **框架集成**：LangChain、LangChain4j 等框架可直接通过 OpenAI 兼容接口对接百炼，无需额外适配。

## 限制与注意事项

- **功能完整度**：兼容接口为保证协议一致性，可能不暴露百炼原生 DashScope 接口的全部参数。如需最完整的采样参数和业务字段，建议使用 DashScope 原生接口。
- **接口能力差异**：联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力，Chat Completions 接口不内置这些工具。
- **对话历史管理**：仅 Responses 接口自动维护对话历史，使用其他接口时需自行管理上下文。
- **模型兼容性**：部分模型（如 Qwen-Audio、qwen-deep-research）不支持 OpenAI 兼容协议，仅支持 DashScope 协议，使用前需确认目标模型的协议支持情况。
- **API Key 与 Base URL 必须匹配**：按量计费、Token Plan、Coding Plan 的 API Key 和 Base URL 互不通用，混用会导致 401/403 错误。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [more models](../api/more-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [token plan guide](../guides/token-plan-guide.md)
- [application call](../api/application-call.md)


