# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套遵循 OpenAI API 规范的调用方式，开发者只需将 API Key、Base URL 和模型名称替换为百炼对应的值，即可将现有 OpenAI 生态的代码和工具无缝迁移至百炼平台，调用千问（Qwen）、DeepSeek、Kimi、GLM 等模型。

## 兼容的接口类型

百炼提供多种 OpenAI 兼容接口，覆盖不同业务场景：

| 接口 | 适用场景 |
|------|----------|
| Chat Completions | 多轮对话、Function Call、文本生成 |
| Responses API | Chat Completions 的演进版，内置联网搜索、代码解释器等工具，自动管理对话历史 |
| Completions | 代码补全、文本续写（FIM 模式） |
| Vision | 图片理解、视觉问答 |
| Embedding | 文本向量化 |
| Files | 文件上传与管理 |
| Batch Chat / Batch File | 批量推理，费用为实时调用的 50% |
| Conversations | 跨设备会话管理，配合 Responses API 使用 |

## 接入配置

### Base URL

各地域的 OpenAI 兼容 Base URL 如下（不同地域的 API Key 不通用）：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` 或 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

> 北京和新加坡地域推出了含 WorkspaceId 的专属域名，在性能和稳定性上优于旧版，建议尽快迁移。

### API Key

通过百炼控制台获取，推荐配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。

## 典型使用场景

### 模型推理

文本生成、视觉理解、图片生成、音视频翻译、文本向量化等模型推理任务均可通过 OpenAI 兼容接口调用。以文本生成为例，使用 OpenAI SDK 只需设置百炼的 `api_key` 和 `base_url`：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
```

### 应用调用

百炼已发布的智能体和工作流应用支持通过 OpenAI 兼容的 Responses API 调用，便于复用现有 OpenAI 代码库。支持同步调用（实时交互）和异步调用（`background: true`，适合耗时任务）。

### 第三方工具与框架接入

百炼的 OpenAI 兼容特性使其可直接对接大量第三方工具和框架：

- **AI 编程工具**：Codex、Cursor、Cline、Qwen Code、Kilo CLI 等通过 OpenAI 协议接入
- **桌面客户端**：Cherry Studio、Chatbox、QwenPaw 等通过 OpenAI 协议配置模型
- **开发框架**：LangChain、LangChain4j 等框架可直接使用 OpenAI 兼容接口集成百炼模型
- **Anthropic 协议工具**：Claude Code、Hermes Agent、OpenCode、OpenClaw 等通过 Anthropic 兼容接口接入

## 与 [DashScope 接口](dashscope-api.md)的区别

DashScope 是百炼的原生接口，提供最完整的功能集和参数支持。OpenAI 兼容接口在参数覆盖上可能不如 DashScope 全面，但迁移成本最低。选择建议：

- 已有 OpenAI 代码的项目优先选 OpenAI 兼容接口
- 需要百炼平台全部能力时选 [DashScope 接口](dashscope-api.md)
- 部分模型（如 Qwen-Audio、Qwen-Deep-Research）仅支持 DashScope 协议

## 注意事项

- 不同地域的 API Key 和 Base URL 不能跨地域混用
- Responses API 会自动管理对话历史，无需手动维护上下文，对话状态管理逻辑与 Chat Completions 不同
- 三方直供模型（如 SiliconFlow DeepSeek）仅在中国站中国内地地域可用，需先在控制台开通
- 批量推理（Batch）接口费用为实时调用的 50%，适合大量请求且对延迟不敏感的场景

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model inference](../guides/model-inference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [general text embedding](../api/general-text-embedding.md)


