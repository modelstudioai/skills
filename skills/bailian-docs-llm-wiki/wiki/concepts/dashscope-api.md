# DashScope 接口

DashScope 接口是阿里云百炼平台的原生 API 体系，提供最完整的功能集和参数支持，是百炼各类模型与应用调用的核心通道。所有百炼服务（文本生成、语音识别、语音合成、应用调用等）均通过 `dashscope.aliyuncs.com` 域名统一接入。

## 接口定位

百炼平台同时提供 [OpenAI 兼容接口](openai-compatible-api.md)、Anthropic 兼容接口和 DashScope 原生接口三种调用方式。其中 DashScope 接口覆盖面最广：

- 兼容接口为迁移便利而设计，功能集是 DashScope 的子集。
- 需要使用百炼平台全部能力（如[异步任务](async-task.md)、自定义插件透传、声音复刻等）时，应优先选择 DashScope 接口。

## 覆盖的服务场景

### 文本生成模型

通过 DashScope HTTP 接口或 DashScope SDK 调用通义千问（Qwen）系列模型，支持全部模型参数（`temperature`、`top_p`、`top_k`、`max_tokens`、`enable_thinking` 等），以及[流式输出](streaming-output.md)、工具调用等高级功能。

### 应用调用

智能体和工作流应用统一通过以下端点调用：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
```

请求体包含 `input`（[prompt](../guides/prompt.md) / messages / biz_params）、`parameters`、`debug` 三个根字段。DashScope API 相比 OpenAI Responses API 提供更完整的功能：多轮上下文管理、[流式输出](streaming-output.md)、Plugin 透传、RAG、Function Calling、多模态输入（文本/图片/文件/音视频）以及原生[异步任务](async-task.md)支持。

### 语音识别（ASR）

- **实时识别**：通过 WebSocket 端点 `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 接入 Fun-ASR、Paraformer、Qwen-ASR 等模型。
- **录音文件识别**：通过 RESTful 异步接口 `POST /api/v1/services/audio/asr/transcription` 提交长音频转写任务。

### 语音合成（TTS）

- **实时合成**：通过 WebSocket 端点 `wss://dashscope.aliyuncs.com/api-ws/v1/inference` 使用 CosyVoice 系列模型。
- **非实时合成**：通过 HTTP 接口 `POST /api/v1/services/audio/tts/SpeechSynthesizer` 调用。

## 鉴权与凭证

所有 DashScope 接口使用统一的 API Key 鉴权机制：

- 请求头携带 `Authorization: Bearer <API_KEY>`。
- 建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码。
- 敏感场景可通过 `POST /api/v1/tokens` 接口生成有效期 1-1800 秒的临时 API Key（以 `st-` 开头）。

## 多地域支持

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` |

不同地域的 API Key 互相独立，临时 Key 也必须在对应地域使用。部分服务（如 Paraformer 实时识别、非实时语音合成 CosyVoice）仅在华北2（北京）地域可用。

## SDK 支持

| SDK | 安装方式 |
|-----|----------|
| DashScope Python SDK | `pip install -U dashscope` |
| DashScope Java SDK（≥ 2.12.0） | Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java` |

Java SDK 内置 OkHttp 连接池，高并发场景下可调整 `connectionPoolSize`、`maximumAsyncRequests` 等参数优化性能。

## 关键注意事项

- DashScope 接口的参数覆盖面最广，兼容接口可能存在参数差异。
- [异步任务](async-task.md)（文生图、文生视频、长语音识别等）采用先提交后查询模式，可通过 EventBridge 接收完成通知替代轮询。
- 子[业务空间](workspace.md)的 API Key 仅能调用已授权的模型，跨空间调用需携带 `X-DashScope-WorkSpace` 头。
- 非流式调用时不支持 `enable_thinking` 参数，需设为 `false` 或改用[流式输出](streaming-output.md)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [preparations](../api/preparations.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more about models](../api/more-about-models.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [audio api references](../api/audio-api-references.md)



