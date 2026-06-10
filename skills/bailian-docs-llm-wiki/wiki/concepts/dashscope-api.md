# DashScope API 协议

DashScope API 是百炼平台的原生统一调用协议，覆盖文本、图像、音频、视频、3D 等多模态模型的推理与生成任务。相比 OpenAI / Anthropic 兼容接口，DashScope 提供最完整的功能集和参数支持，是所有百炼能力的底层传输层。

## 协议形态

DashScope API 同时提供两种传输形态，按任务耗时自动选择：

| 形态 | 适用场景 | 典型模态 |
| --- | --- | --- |
| 同步（HTTP POST / WebSocket） | 响应延迟低、单次即可完成的任务 | 文本对话、语音合成（流式）、实时翻译 |
| [异步任务](async-task.md)（Async Task） | 耗时较长、需后台排队的任务 | 视频生成、图像生成、3D 模型生成 |

[异步任务](async-task.md)协议是最具辨识度的模式，整个流程分两步：

1. **创建任务**：`POST` 请求到对应服务的 `/api/v1/services/aigc/...` 端点，请求头必须带 `X-DashScope-Async: enable`，响应返回 `task_id`。
2. **轮询结果**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`，直到状态为 `SUCCEEDED` 或 `FAILED`。`task_id` 有效期 24 小时，切勿重复创建任务。

开启[流式输出](streaming-output.md)则使用 `X-DashScope-SSE: enable` 请求头，服务端通过 Server-Sent Events 逐步返回中间结果。

## 统一鉴权

所有 DashScope 请求共享同一套鉴权体系，API Key 通过环境变量 `DASHSCOPE_API_KEY` 管理：

```
Authorization: Bearer <your_api_key>
```

- HTTP 请求：放在请求头 `Authorization` 字段。
- WebSocket 请求：在握手阶段的 Header 中携带，无效 Key 返回 HTTP 401/403。
- 可选 Header：`X-DashScope-WorkSpace`（[业务空间](workspace.md) ID）、`user-agent`（客户端标识）。

## 多地域端点

DashScope 按地域隔离端点，模型、Endpoint URL、API Key **必须属于同一地域**，跨地域调用会失败：

| 地域 | HTTP Endpoint | WebSocket Endpoint |
| --- | --- | --- |
| 华北 2（北京） | `https://dashscope.aliyuncs.com/api/v1/...` | `wss://dashscope.aliyuncs.com/api-ws/v1/...` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/...` | `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/...` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/api/v1/...` | — |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/...` | — |

> 新加坡/法兰克福 URL 中的 `{WorkspaceId}` 需替换为真实的工作空间 ID。新加坡地域旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，应迁移到新域名。

## 各场景的调用模式

### 文本生成

Qwen 系列模型的 DashScope 原生接口提供最完整参数支持（思考模式 `enable_thinking`、Function Calling、结构化输出、批量推理等）。相比 [OpenAI 兼容接口](openai-compatible-api.md)，DashScope 原生接口的参数覆盖面最广。

端点：`POST /api/v1/services/aigc/text-generation/generation`

### 图像生成与编辑

文生图、图像编辑等任务采用**同步或异步** HTTP 接口，按模型不同选择端点：

- 千问图像 / Z-Image / 万相 V2+：`/api/v1/services/aigc/multimodal-generation/generation`（同步）
- 万相 V1、专项能力（翻译、局部重绘、扩图、虚拟模特等）：`/api/v1/services/aigc/image2image/image-synthesis`（异步）

请求体核心字段：`model`、`input.prompt`、`input.media`（参考图数组）、`parameters`（`size`、`n`、`style` 等）。

### 视频生成

所有视频生成模型（万相 Wan、HappyHorse、可灵 Kling 等）统一走**[异步任务](async-task.md)协议**：

- 创建端点：`POST /api/v1/services/aigc/video-generation/video-synthesis`
- 请求头：`X-DashScope-Async: enable`
- 关键参数：`model`、`input.prompt`、`input.media`（`first_frame` / `last_frame` / `reference_image` 等）、`parameters`（`resolution`、`ratio`、`duration`、`prompt_extend`）

任务耗时通常 1–5 分钟，视频编辑统一模型约 5–10 分钟。

### 语音合成（TTS）

| 模式 | 协议 | 端点 |
| --- | --- | --- |
| 非实时（Qwen-TTS / CosyVoice） | HTTP POST，可选 SSE 流式 | `/api/v1/services/audio/tts/SpeechSynthesizer` |
| 实时流式（CosyVoice / Qwen-TTS Realtime） | WebSocket 双向流 | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` |

WebSocket 实时合成通过三类事件交互：`run-task`（声明模型与参数）→ `continue-task`（携带文本）→ `finish-task`（结束）。音频格式支持 `pcm` / `wav` / `mp3` / `opus`，采样率可选 8000–48000 Hz。

### 语音识别（ASR）与实时翻译

ASR 与实时音视频翻译同样基于 WebSocket 长连接，端点路径为 `/api-ws/v1/realtime`，鉴权方式一致。

## 请求体通用结构

尽管不同模态的端点路径不同，DashScope 请求体遵循统一的顶层结构：

```json
{
  "model": "<model-name>",
  "input": {
    "prompt": "文本提示",
    "media": [],
    "text": "待处理文本"
  },
  "parameters": {
    "resolution": "1080P",
    "size": "1024*1024",
    "n": 1
  }
}
```

- `model`：模型标识符（如 `qwen3.7-plus`、`wan2.7-t2v`、`cosyvoice-v3.5-plus`）。
- `input`：输入数据，按模态包含 `prompt` / `text` / `media` / `voice` 等字段。
- `parameters`：控制生成行为的参数，因模型而异。

## SDK 支持

DashScope 提供 Python 与 Java 两种官方 SDK，封装了鉴权、重试、流式解析等细节：

- **Python SDK**：`dashscope` 包，覆盖所有模态的高层 API。
- **Java SDK**：`dashscope-sdk-java`，提供同步 / 异步 / 流式三种调用模式。
- **移动端 SDK**：Android / iOS SDK 主要面向语音合成场景。

对于视频生成、图像生成等异步任务，SDK 内部封装了"提交 + 轮询"的两步流程，开发者只需调用一个方法即可等待最终结果。

## 与其他接口的关系

百炼平台同时提供 OpenAI 兼容（Chat Completions / Responses）和 Anthropic 兼容（Messages）接口，这些接口在底层部分能力仍依赖 DashScope 协议，但对开发者屏蔽了异步任务、地域端点等细节。选择建议：

- **迁移现有 OpenAI 应用** → OpenAI 兼容 Chat Completions，改动最小。
- **需要内置工具且免维护对话历史** → OpenAI 兼容 Responses。
- **需要百炼全部能力（多模态、异步任务、完整参数控制）** → DashScope 原生接口。

DashScope 原生接口是所有接口中功能覆盖面最广的选择，尤其在视频生成、图像编辑、语音合成等非文本模态上，通常只有 DashScope 端点可用。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [video generation api](../api/video-generation-api.md)
- [model inference](../guides/model-inference.md)
- [image generation](../api/image-generation.md)
- [audio api references](../api/audio-api-references.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)


