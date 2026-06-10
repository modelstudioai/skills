# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组遵循 OpenAI API 规范的服务端点，开发者只需将 `api_key`、`base_url` 和 `model` 三个参数替换为百炼的值，即可将现有 OpenAI 应用无缝迁移到百炼服务，调用千问（Qwen）全系列及第三方大模型。

## 接口类型

百炼提供多种 OpenAI 兼容端点，覆盖不同业务场景：

| 接口 | 端点路径 | 典型用途 |
|------|---------|---------|
| Chat Completions | `/compatible-mode/v1/chat/completions` | 文本对话、多轮会话，最常用的接口 |
| Responses | `/compatible-mode/v1/responses` | 内置联网搜索、代码解释器等工具，自动管理对话历史 |
| Completions | `/compatible-mode/v1/completions` | 代码补全、文本续写（仅 `qwen-coder-turbo`） |
| Vision | `/compatible-mode/v1/chat/completions` | 图像与视频理解 |
| Embeddings | `/compatible-mode/v1/embeddings` | 文本向量化 |
| Files | `/compatible-mode/v1/files` | 文件上传与管理 |
| Batch | `/compatible-mode/v1/batches` | 异步文件批量推理 |

其中 Chat Completions 是使用最广泛的接口，支持千问全系列文本模型，包括流式与非[流式输出](streaming.md)。Responses 接口是其演进版本，通过 `previous_response_id` 自动关联多轮对话，无需手动维护消息列表。

## 认证与服务地址

所有接口统一使用百炼 API Key 认证，通过 `Authorization: Bearer <API_KEY>` 请求头或 SDK 的 `api_key` 参数传入。建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`。

各地域的 Base URL：

| 地域 | Base URL |
|------|---------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

不同地域的 API Key 不通用，切换地域时必须同时更换 `base_url` 和 API Key。新加坡和法兰克福地域的 URL 需填入[业务空间](workspace.md) ID（WorkspaceId）。

## 快速接入示例

使用 OpenAI Python SDK 调用百炼模型：

```python
import os
from openai import OpenAI

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

同样支持 Node.js（OpenAI SDK）、curl 及各类第三方客户端（Cursor、Cherry Studio、Chatbox、Cline 等）。

## 专用模型的兼容接口使用

百炼的专用模型（Qwen-MT 机器翻译、Qwen-OCR 文字识别、GUI-Plus 界面交互等）也通过 OpenAI 兼容接口调用，但请求体中需传入模型专属字段。例如 Qwen-MT 需在 `extra_body.translation_options` 中指定源语言、目标语言和术语表。

## 与 DashScope 原生接口的对比

百炼同时提供 DashScope 原生接口，两者的主要区别：

- **OpenAI 兼容接口**：迁移成本最低，可直接复用 OpenAI SDK 和生态工具，适合已有 OpenAI 代码的项目。
- **DashScope 原生接口**：百炼原生协议，提供最完整的功能集和参数支持，适合需要平台全部能力的场景。

## 注意事项

- 不同接口支持的参数范围存在差异，[DashScope 接口](dashscope-api.md)覆盖面最广。
- Responses 接口会自动管理对话历史（有效期 7 天），上下文管理逻辑与 Chat Completions 不同。
- 使用 Token Plan 团队版、Coding Plan 等计费方案时，Base URL 与按量计费不同，需根据计费方案选择对应地址。
- 新加坡地域旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请尽快迁移至新版域名。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [specialized model](../api/specialized-model.md)
- [frameworks](../api/frameworks.md)


