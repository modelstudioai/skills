# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套与 OpenAI API 规范对齐的调用协议，允许开发者仅通过替换 `api_key`、`base_url` 和 `model` 三个参数，即可将现有 OpenAI 应用零改造迁移到百炼平台，使用千问、DeepSeek、Kimi、GLM、MiniMax 等模型。

## 支持的接口类型

百炼的 OpenAI 兼容协议覆盖以下接口：

| 接口 | 端点路径 | 典型场景 |
| --- | --- | --- |
| Chat Completions | `/v1/chat/completions` | 最常用的对话接口，支持千问全系列及第三方模型 |
| Responses | `/v1/responses` | 面向智能体场景，内置联网搜索、代码解释器等工具，自动管理对话历史 |
| Completions | `/v1/completions` | 文本/代码补全，支持前缀补全和中间填充（FIM） |
| Vision | `/v1/chat/completions`（多模态） | 图像理解，`messages.content` 传入图片与文本数组 |
| Embedding | `/v1/embeddings` | 文本向量化 |
| Files | `/v1/files` | 文件上传管理 |
| Batch | `/v1/batches` | 批量推理（同步/文件输入） |
| Fine-tuning Jobs | `/v1/fine_tuning/jobs` | 模型微调训练任务 |

此外，百炼应用（智能体、工作流）也提供 OpenAI Responses API 兼容模式，端点为 `/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，便于复用 OpenAI 生态代码调用已发布的应用。

## 服务地址（Base URL）

不同地域和计费方式对应不同的 Base URL，API Key 与模型不能跨地域混用：

| 地域/计费 | Base URL |
| --- | --- |
| 华北2（北京）按量付费 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| Batch（中国内地） | `https://batch.dashscope.aliyuncs.com/compatible-mode/v1` |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/compatible-mode/v1` |

> **注意**：新加坡旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移至新版域名。新加坡与法兰克福的 URL 中 `{WorkspaceId}` 需替换为真实的业务空间 ID。

## 接入方式

使用 OpenAI 官方 SDK 或任何兼容 OpenAI 协议的客户端均可接入。以 Python 为例：

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-dashscope-api-key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
```

Node.js 的 `openai` 包、curl 以及其他语言的 HTTP 客户端同样适用，只需设置对应的 `api_key` 和 `base_url`。

## 兼容的工具与客户端

得益于 OpenAI 协议的广泛生态，以下工具可直接通过百炼 OpenAI 兼容接口接入：

- **对话客户端**：Cherry Studio、Chatbox
- **AI 编码 Agent**：Claude Code、Codex、Qwen Code、OpenCode、Kilo CLI、Hermes Agent
- **IDE 集成**：Cursor、Cline、Qoder
- **框架**：LangChain、LangChain4j、Dify
- **调试工具**：Postman、cURL

## 与其他接口的对比

百炼同时提供 DashScope 原生接口和 Anthropic 兼容接口。三者的选型建议：

- **OpenAI 兼容接口**：迁移成本最低，适合已有 OpenAI 代码的项目和接入第三方工具。
- **DashScope 原生接口**：功能最完整、参数覆盖面最广，需要百炼全部能力时首选。
- **Anthropic 兼容接口**：适合使用 Claude Code 等 Anthropic 生态工具的开发者。

## 注意事项

- OpenAI 兼容接口支持的参数范围是 [DashScope 接口](dashscope-api.md)的子集，部分高级参数仅在 [DashScope 接口](dashscope-api.md)可用。
- Responses 接口会自动管理对话历史（通过 `previous_response_id` 关联），对话状态管理逻辑与 Chat Completions 不同。
- 专用模型（Qwen-MT 翻译、Qwen-OCR 文字识别、GUI-Plus 界面交互）同样支持 OpenAI 兼容接口，但有额外的专属字段需通过 `extra_body` 传入。
- Qwen-Deep-Research 深度研究模型目前不支持 OpenAI 兼容接口，仅可通过 DashScope Python SDK 调用。
- 不同计费方式（按量付费、Token Plan、Coding Plan）的 API Key 和 Base URL 互不通用，混用会导致鉴权失败。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [token plan guide](../guides/token-plan-guide.md)
- [fine tuning jobs api](../api/fine-tuning-jobs-api.md)
- [specialized model](../api/specialized-model.md)
- [bailian application calling](../guides/bailian-application-calling.md)


