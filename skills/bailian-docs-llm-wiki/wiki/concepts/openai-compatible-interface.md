# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套与 OpenAI API 协议完全兼容的调用方式，开发者只需将 `base_url`、`api_key` 和 `model` 三个参数指向百炼即可复用现有 OpenAI SDK 和工具链，实现零改造迁移。

## 接口类型

百炼提供多种 OpenAI 兼容接口，覆盖不同使用场景：

| 接口 | 用途 | 关键特性 |
| --- | --- | --- |
| Chat Completions | 文本对话 | 支持[流式输出](streaming.md)、Function Call、多轮对话，兼容性最广 |
| Responses API | 智能体原生对话 | 内置联网搜索、代码解释器、网页内容提取，自动管理对话历史 |
| Completions | 代码/文本补全 | 支持 FIM（Fill-in-Middle）模式 |
| Vision | 图像/视频理解 | 支持 URL 和 Base64 输入 |
| Embedding | 文本向量化 | 多维度可选（64~2048） |
| Batch | 异步批量推理 | 费用为实时调用的 50% |

## 服务地址配置

所有兼容接口统一使用[业务空间](workspace.md)专属域名：

```
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
```

支持的地域包括华北2（北京）、新加坡、美国（弗吉尼亚）、日本（东京）、德国（法兰克福）。其中 `{WorkspaceId}` 为[业务空间](workspace.md) ID，可在百炼控制台查看。

不同计费方案使用独立的 Base URL：

| 计费方案 | Base URL |
| --- | --- |
| 按量计费 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| [Token](token.md) Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |

## 快速接入

使用 Python OpenAI SDK 接入百炼的最小示例：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ],
    stream=True
)
```

## 支持的模型

兼容接口支持百炼平台上的绝大多数模型，包括：

- **千问系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等全系列
- **第三方模型**：DeepSeek、Kimi、GLM、MiniMax 等
- **专用模型**：qwen-mt-plus（翻译）、qwen3.5-ocr（OCR）、gui-plus（界面交互）、tongyi-intent-detect-v3（意图理解）

> 注意：部分模型仅支持 DashScope 原生协议（如 Qwen-Audio、qwen-deep-research），不支持 OpenAI 兼容接口，使用前需确认模型文档。

## 第三方工具接入

百炼的 OpenAI 兼容接口可直接对接主流 AI 编程工具和聊天客户端：

- **终端编程工具**：Claude Code、Codex、Qwen Code、OpenCode、Kilo CLI 等
- **IDE 插件**：Cursor、Cline、Qoder 等
- **桌面客户端**：Cherry Studio、Chatbox 等
- **开发平台**：Dify、LangChain 等

这些工具只需配置 API Key 和 Base URL 即可接入，无需额外适配。

## 关键参数

| 参数 | 说明 |
| --- | --- |
| `model` | 模型名称，必须精确匹配百炼支持的模型 ID |
| `messages` | 对话消息列表，格式与 OpenAI 一致 |
| `stream` | 是否启用[流式输出](streaming.md) |
| `tools` | Function Call 工具定义列表 |
| `temperature` | 采样温度，控制输出随机性 |
| `stream_options` | 流式选项，设置 `{"include_usage": true}` 可获取 token 统计 |

## 与 DashScope 原生接口的差异

- **功能完整度**：兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数（如部分采样参数、插件字段）
- **工具能力**：联网搜索、代码解释器等内置工具仅 Responses API 支持，Chat Completions 需自行通过 Function Call 实现
- **对话历史**：仅 Responses API 通过 `previous_response_id` 自动管理历史，其他接口需手动维护 messages 数组

如需使用百炼全部原生能力，建议使用 [DashScope SDK](dashscope-sdk.md)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [token plan guide](../guides/token-plan-guide.md)


