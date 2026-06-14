# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组与 OpenAI API 规范对齐的调用端点，开发者可以直接使用 OpenAI 官方 SDK（Python、Node.js 等）或任何兼容 OpenAI 格式的工具和框架来调用百炼上的模型服务，只需替换 API Key、Base URL 和模型名称即可完成迁移。

## 接口类型

百炼提供多种 OpenAI 兼容接口，覆盖不同的使用场景：

| 接口 | 端点路径 | 适用场景 |
|------|----------|----------|
| Chat Completions | `/compatible-mode/v1/chat/completions` | 文本对话、Function Call、视觉理解、翻译等 |
| Responses API | `/compatible-mode/v1/responses` | 智能体原生功能，内置联网搜索、代码解释器等工具 |
| Completions | `/compatible-mode/v1/completions` | 代码补全、文本续写（FIM） |
| Embeddings | `/compatible-mode/v1/embeddings` | 文本向量化 |
| Files | `/compatible-mode/v1/files` | 文件上传与管理 |
| Batch | `/compatible-mode/v1/batches` | 批量推理（同步或异步） |
| Conversations | `/compatible-mode/v1/conversations` | 跨设备会话管理 |

## 通用配置

所有 OpenAI 兼容接口共享统一的认证和端点配置，迁移时只需修改三个参数：

- **api_key**：百炼平台的 API Key（通过控制台创建，存入环境变量 `DASHSCOPE_API_KEY`）
- **base_url**：根据地域选择对应的服务端点
- **model**：替换为百炼支持的模型名称（如 `qwen-plus`、`qwen3.7-max` 等）

### 各地域 Base URL

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

不同地域的 API Key 不通用，需分别申请。新加坡和德国地域还需要在 URL 中嵌入 WorkspaceId。

## 基本调用示例

以 Python 为例，使用 OpenAI SDK 调用百炼模型：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
print(completion.choices[0].message.content)
```

Node.js 调用方式类似，使用 `openai` npm 包，设置相同的 `apiKey` 和 `baseURL` 即可。

## 支持的模型

通过 OpenAI 兼容接口可调用的模型包括：

- **通义千问系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等全系列文本生成模型
- **第三方模型**：deepseek-v4-pro、kimi-k2.6、glm-5.1、MiniMax-M2.7 等
- **专用模型**：Qwen-MT（机器翻译）、Qwen-OCR（文字提取）、GUI-Plus（界面交互）、tongyi-intent-detect（意图识别）
- **音视频翻译**：qwen3-livetranslate-flash（离线翻译）
- **向量模型**：text-embedding-v1/v2/v3/v4

## Chat Completions 与 Responses API 的选择

Chat Completions 是最通用的接口，适合绝大多数对话和推理场景，迁移成本最低。

Responses API 是 Chat Completions 的演进版本，核心优势：

- 内置联网搜索、网页抓取、代码解释器等工具，无需自行实现
- 支持直接传入字符串作为输入，也兼容 Chat 格式的消息数组
- 通过 `previous_response_id` 自动关联历史对话，无需手动构建消息列表

如果需要百炼平台的全部功能（如完整的参数集、[异步任务](async-task.md)等），可选择 DashScope 原生接口。

## 在应用调用中使用

百炼的智能体和工作流应用也支持通过 OpenAI 兼容模式调用。应用调用使用专用端点：

```
POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses
```

开发者可以通过 OpenAI SDK 的 `client.responses.create` 方法调用已发布的应用，便于复用 OpenAI 生态代码。

## 第三方工具接入

百炼的 OpenAI 兼容接口可以无缝对接主流 AI 开发工具和客户端，包括：

- **AI 编程工具**：Cursor、Cline、Claude Code、Codex 等
- **桌面客户端**：Cherry Studio、Chatbox 等
- **开发框架**：LangChain、Dify 等
- **API 测试**：Postman、cURL

配置时根据计费方案（按量计费、Coding Plan、Token Plan 团队版）选择对应的 Base URL 和 API Key。

## 与 [DashScope 接口](dashscope-api.md)的区别

| 维度 | OpenAI 兼容接口 | DashScope 原生接口 |
|------|-----------------|-------------------|
| 请求/响应格式 | 遵循 OpenAI API 规范 | 百炼自有格式 |
| SDK | OpenAI 官方 SDK | DashScope SDK |
| 功能覆盖 | 覆盖主要功能 | 最完整的功能集和参数支持 |
| 迁移成本 | 已有 OpenAI 代码可直接迁移 | 需要学习 DashScope API |
| 生态兼容性 | 兼容 OpenAI 生态的所有工具和框架 | 仅限 DashScope 生态 |

对于大多数开发场景，推荐优先使用 OpenAI 兼容接口以降低接入成本。当需要使用百炼平台特有的高级功能时，再考虑切换到 [DashScope 接口](dashscope-api.md)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [specialized model](../api/specialized-model.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)



