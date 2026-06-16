# DashScope 接口

DashScope 是阿里云百炼平台的原生 API 接口体系，提供最完整的功能集和参数支持，是百炼各类模型与应用服务的统一调用入口。其 Base URL 为 `https://dashscope.aliyuncs.com`，通过 API Key（环境变量 `DASHSCOPE_API_KEY`）进行鉴权。

## 与其他接口的关系

百炼平台同时提供 [OpenAI 兼容接口](openai-compatible-api.md)和 Anthropic 兼容接口，方便已有代码迁移。DashScope 接口与它们的核心区别在于：

| 维度 | DashScope 接口 | OpenAI / Anthropic 兼容接口 |
|------|---------------|---------------------------|
| 功能覆盖 | 最完整，支持百炼全部能力 | 部分参数和功能可能不可用 |
| 生态定位 | 百炼原生，长期维护 | 便于第三方工具和已有项目迁移 |
| SDK | DashScope Python / Java SDK | OpenAI / Anthropic 官方 SDK |

当需要使用百炼平台的全部能力时，优先选择 DashScope 接口。

## 覆盖的服务类型

DashScope 接口统一承载了百炼平台多种服务的调用：

- **文本生成**：通义千问（Qwen）系列模型，通过 DashScope 可使用最完整的参数集（如思考模式、工具调用等）。
- **应用调用**：智能体和工作流应用通过 `POST /api/v1/apps/{APP_ID}/completion` 端点调用，支持多轮对话（`session_id` 或 `messages`）、自定义参数透传（`biz_params`）、[流式输出](streaming-output.md)和异步调用。
- **语音合成与识别**：CosyVoice 语音合成通过 WebSocket（`wss://dashscope.aliyuncs.com/api-ws/v1/inference`）或 HTTP API 调用；语音识别同样基于 DashScope 服务。
- **专用模型**：翻译（Qwen-MT）、深度研究（Qwen-Deep-Research）、OCR、文本排序、意图理解、法律等垂直模型均通过 DashScope 接口调用。
- **长期记忆**：记忆管理服务的 Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，提供记忆片段和用户画像的增删改查。
- **[异步任务](async-task.md)管理**：文生图、文生视频等长耗时任务的状态查询、批量查询和取消操作。

## 关键参数与配置

### 鉴权

所有请求通过 HTTP Header 传递 API Key：

```
Authorization: Bearer $DASHSCOPE_API_KEY
```

在不可信环境（浏览器、移动端）中，可通过 `POST /api/v1/tokens` 接口换取临时 API Key（`st-` 开头），有效期 1–1800 秒，到期自动失效。

### 通用请求参数

应用调用的请求体一般包含三个根字段：

| 字段 | 说明 |
|------|------|
| `input` | 包含 `prompt`（用户输入）或 `messages`（多轮对话历史） |
| `parameters` | 模型参数或预留扩展字段 |
| `debug` | 调试控制 |

### 多轮对话

DashScope 提供两种上下文管理方式：

- **`session_id`**：云端托管会话，自动加载历史，有效期 1 小时，最多 50 轮。
- **`messages`**：客户端自行维护对话历史，优先级高于 `session_id`。

### 流式与异步

- **[流式输出](streaming-output.md)**：设置 `stream: true`，响应通过 SSE 逐步返回。
- **异步调用**：通过请求头 `X-DashScope-Async: enable` 启用，返回 `task_id` 后轮询或通过 EventBridge 接收完成通知。

### 连接复用

高并发场景下建议配置 SDK 连接池参数（Java SDK 默认 OkHttp 连接池 32 个连接），避免频繁建连带来的延迟开销。

## 多地域支持

DashScope 接口在多个地域可用，不同地域使用独立的 API Key 和 Base URL：

- 华北2（北京）：默认地域，功能最全
- 新加坡、美国（弗吉尼亚）：部分模型可用

子[业务空间](workspace.md)调用时需额外传入 `workspace_id` 参数。

## SDK 安装

- **Python**：`pip install -U dashscope`（建议 ≥ 1.14.0）
- **Java**：Maven artifact `com.alibaba:dashscope-sdk-java`（建议 ≥ 2.12.0）
- **HTTP**：直接使用 cURL 或任意 HTTP 客户端，无需安装 SDK

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [long term memory new](../api/long-term-memory-new.md)
- [more models](../api/more-models.md)
- [audio api references](../api/audio-api-references.md)
- [more about models](../api/more-about-models.md)


