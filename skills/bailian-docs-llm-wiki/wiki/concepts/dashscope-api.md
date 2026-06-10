# DashScope 接口

DashScope 是阿里云百炼平台的原生 API 体系，为文本生成、图像生成、视频生成、语音合成与识别、应用调用等全部模态提供统一的接入端点和鉴权机制。相比 OpenAI / Anthropic 兼容接口，DashScope 接口覆盖的功能集最完整、参数支持最广泛，是需要使用百炼平台全部能力时的首选。

## 统一鉴权与端点

所有 DashScope 接口共享同一套鉴权方式：在请求头中携带 `Authorization: Bearer <API_KEY>`，API Key 通过百炼控制台创建，建议写入环境变量 `DASHSCOPE_API_KEY` 以避免硬编码泄露。

不同地域使用不同的端点基础域名：

| 地域 | HTTP 端点 |
| --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/api/v1/...` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/...` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/api/v1/...` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/...` |

模型、端点和 API Key 必须属于同一地域，跨地域调用会失败。新加坡与法兰克福地域的 URL 中需将 `{WorkspaceId}` 替换为真实的[业务空间](workspace.md) ID。

## 各场景的调用方式

### 文本生成

通义千问（Qwen）系列模型通过 DashScope 接口调用时拥有最完整的功能集和参数支持，端点与 [OpenAI 兼容接口](openai-compatible-api.md)并行提供。当项目需要使用百炼独有的高级参数时，应优先选择 DashScope 原生接口。

### 应用调用

调用已发布的智能体或工作流应用时，DashScope API 端点为：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
```

请求体核心字段包括 `input.prompt`（用户输入）、`input.messages`（多轮对话历史）、`parameters`（模型参数如 `temperature`、`top_p`、`incremental_output` 等）。SDK 层面通过 `Application.call`（Python）或 `ApplicationParam.builder`（Java）封装。DashScope API 在应用调用场景中功能最全、性能最高，支持多轮上下文、[流式输出](streaming.md)、Plugin、RAG、Function Calling 等。

### 视频生成

视频生成 API 统一采用[异步任务](async-task.md)协议，分两步完成：

1. **创建任务**：`POST .../services/aigc/video-generation/video-synthesis`，请求头需额外携带 `X-DashScope-Async: enable`。
2. **轮询结果**：`GET .../tasks/{task_id}`，task_id 有效期 24 小时。

请求体通过 `model` 指定模型、`input.prompt` 提供提示词、`input.media` 传入媒体素材、`parameters` 控制分辨率和时长等参数。

### 图像生成

图像生成模型可通过 HTTP 或 DashScope SDK 调用。万相 2.6 及以上版本支持 HTTP 同步调用；较早版本仅支持异步调用（创建任务 + 轮询结果），流程与视频生成一致。

### 语音合成与识别

语音类接口同时提供 HTTP REST 和 WebSocket 两种协议。实时语音合成（CosyVoice）采用 WebSocket 双向流，通过 `run-task`、`continue-task`、`finish-task` 三类事件交互；非实时合成使用 HTTP POST，可选开启 SSE 流式返回。WebSocket 端点为 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`。

## SDK 与接入方式

百炼提供官方 DashScope SDK（Python、Java）以及 OpenAI 兼容的多语言 SDK。DashScope SDK 安装方式：

```bash
# Python
pip install -U dashscope

# Java (Maven)
<dependency>
  <groupId>com.alibaba</groupId>
  <artifactId>dashscope-sdk-java</artifactId>
</dependency>
```

语音场景还提供 Android 和 iOS 原生 SDK。

## 关键配置与最佳实践

- **连接复用**：高并发场景下应配置 DashScope SDK 的连接池参数（Java SDK 内置 OkHttp 连接池，可调整 `connectionPoolSize`、`maximumAsyncRequests` 等）以减少 TCP 连接建立开销。
- **[异步任务](async-task.md)管理**：长耗时任务（文生图、文生视频、长语音识别）返回 `task_id` 后，可通过通用任务管理 API 查询、批量查询或取消任务，查询结果保留 24 小时。建议接入 EventBridge 事件通知替代高频轮询。
- **临时 API Key**：在浏览器或移动端等不可信环境中，可通过后端接口换取有效期 1~1800 秒的临时 Key（以 `st-` 开头），到期自动失效。
- **[业务空间](workspace.md)隔离**：当应用位于子[业务空间](workspace.md)时，请求中必须携带 `Workspace ID`。同一业务空间内的 API Key 权限相同，无需为不同模态分别创建。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [video generation api](../api/video-generation-api.md)
- [audio api references](../api/audio-api-references.md)
- [image generation](../api/image-generation.md)
- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)


