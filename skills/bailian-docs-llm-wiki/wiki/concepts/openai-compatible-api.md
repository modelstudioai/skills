# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套与 OpenAI API 规范对齐的调用方式，开发者只需将 `api_key`、`base_url` 和模型名称替换为百炼对应的值，即可将现有基于 OpenAI SDK 的代码无缝迁移至百炼平台，调用通义千问及其他第三方模型。

## 接口形态

百炼的 OpenAI 兼容接口目前包含以下几种形态：

| 接口 | 端点路径 | 典型场景 |
|------|---------|---------|
| Chat Completions | `/compatible-mode/v1/chat/completions` | 文本对话、Function Call、视觉理解、翻译等 |
| Responses API | `/compatible-mode/v1/responses` | 智能体场景，内置联网搜索、代码解释器等工具，自动管理对话历史 |
| Completions | `/compatible-mode/v1/completions` | 代码补全、文本续写（FIM） |
| Embedding | `/compatible-mode/v1/embeddings` | 文本向量化 |
| Files | `/compatible-mode/v1/files` | 文件上传与管理 |
| Batch | `/compatible-mode/v1/batch` | 批量推理 |

Chat Completions 是最常用的入口，覆盖文本生成、视觉理解、音视频翻译等多种模态；Responses API 则是其演进版本，简化了上下文管理并提供内置工具能力。

## 通用配置

所有 OpenAI 兼容接口共享三个核心配置项：

- **`base_url`**：百炼服务端点，按地域区分
- **`api_key`**：百炼平台的 API Key（环境变量通常为 `DASHSCOPE_API_KEY`）
- **模型名称**：如 `qwen3.7-plus`、`deepseek-v4-pro` 等百炼支持的模型

### 各地域 Base URL

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

不同地域的 API Key 不通用，新加坡和德国地域还需在 URL 中嵌入 WorkspaceId。

## 基本调用示例

以 Python OpenAI SDK 为例：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}]
)
print(completion.choices[0].message.content)
```

同样的方式适用于 Node.js、Go、Java 等语言的 OpenAI 官方或社区 SDK，只需替换上述三个配置项。

## 在百炼各场景中的使用

### 模型直接调用

通过 Chat Completions 接口调用千问系列（qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等）以及 DeepSeek、Kimi、GLM、MiniMax 等第三方模型，接口格式完全一致。

### 应用调用

百炼已发布的智能体和工作流应用也支持通过 OpenAI 兼容的 Responses API 调用。端点为 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，便于复用 OpenAI 生态代码触发应用执行。

### 专用模型

部分专用模型同样通过 OpenAI 兼容接口调用，如：

- **Qwen-MT**（机器翻译）：通过 `extra_body.translation_options` 传递翻译参数
- **音视频翻译**（qwen3-livetranslate-flash）：通过 Chat Completions 流式接口完成离线翻译
- **意图识别**（tongyi-intent-detect）：支持 OpenAI 兼容和 DashScope 双接口

### 第三方工具与框架集成

百炼的 OpenAI 兼容接口被广泛用于对接第三方工具和框架：

- **AI 编程工具**：Claude Code、Cursor、Cline、Codex、Qwen Code 等均可通过配置 Base URL 和 API Key 接入百炼
- **桌面客户端**：Cherry Studio、Chatbox、QwenPaw 等
- **开发平台**：Dify、LangChain 等主流框架可直接通过 OpenAI SDK 对接

### 订阅套餐

Token Plan 团队版和 Coding Plan 各自拥有独立的 Base URL 和 API Key，与按量计费的通用配置互不相通：

| 套餐 | OpenAI 兼容 Base URL |
|------|---------------------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |
| 按量计费（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

## 与 DashScope 原生接口的对比

| 维度 | OpenAI 兼容接口 | DashScope 原生接口 |
|------|----------------|-------------------|
| 迁移成本 | 极低，改三个参数即可 | 需要使用 DashScope SDK 或调整请求格式 |
| 功能覆盖 | 覆盖主流场景 | 最完整的功能集和参数支持 |
| 生态兼容性 | 可复用 OpenAI 生态的工具和框架 | 百炼专属功能（如应用调用的完整能力） |
| 推荐场景 | 已有 OpenAI 代码迁移、第三方工具接入 | 需要平台全部能力、性能优先的场景 |

如果项目已有 OpenAI SDK 代码，优先选择 OpenAI 兼容接口以降低迁移成本；如需百炼平台的完整功能集（如新版智能体的全部字段），则选择 DashScope 原生接口。

## 注意事项

- 不同地域的 API Key 和 Base URL 不能跨地域混用。
- 不同计费方案（按量计费、Token Plan、Coding Plan）的 API Key 和 Base URL 互不兼容，不可混用。
- OpenAI 兼容接口支持的参数范围可能略少于 DashScope 原生接口，部分百炼特有参数需通过 `extra_body` 传递。
- Responses API 会自动管理对话历史（通过 `previous_response_id`），上下文管理方式与 Chat Completions 不同。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [frameworks](../api/frameworks.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more models](../api/more-models.md)
- [token plan guide](../guides/token-plan-guide.md)


