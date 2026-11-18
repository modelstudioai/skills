# realtime api directory

Realtime API 目录提供低延迟、流式交互的实时 AI 能力接入入口，覆盖语音识别（ASR）、语音合成（TTS）、多模态理解与生成、音视频实时翻译及端到端语音对话等核心场景。所有接口均基于 WebSocket 协议设计，支持双向流式数据传输与事件驱动响应。该目录是 [Realtime API (raw/model-api-reference/realtime-api-directory.md)](../../raw/model-api-reference/realtime-api-directory.md) 的顶层导航结构，各子能力文档详见其下级链接。

## 支持的模型与功能

- **实时语音识别（ASR）**：支持中英文混合识别、标点预测、语速自适应，模型包括 `qwen2-audio-asr-base` 和 `qwen2-audio-asr-pro`  
- **实时语音合成（TTS）**：提供多音色、情感可控的流式 TTS，支持 SSML 标签与端点检测（EoU）  
- **实时语音对话（Audio Realtime）**：端到端语音交互协议，集成 ASR+LLM+TTS 闭环，适用于智能座舱、客服机器人等场景  
- **实时音视频翻译（LiveTranslate）**：支持双语同传、字幕流与音频流同步输出，当前仅限会议场景白名单接入  
- **多模态实时交互（Omni Realtime）**：融合语音、文本、图像输入的统一实时协议，依赖 [多模态交互开发套件](../../raw/model-api-reference/realtime-api-directory/multimodal-interaction-protocol.md) 实现  
- **AOQ SDK 集成支持**：提供轻量级客户端 SDK，封装连接管理、重连、缓冲区控制等，详见 [Realtime API AOQ SDK](../../raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md)

> **注意**：文档 [实时语音对话](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory.md) 中描述的 `audio-realtime-v1` 协议已废弃，当前生产环境仅支持 `audio-realtime-v2`（见 [Realtime API (raw/model-api-reference/realtime-api-directory.md)](../../raw/model-api-reference/realtime-api-directory.md) 中最新链接），旧版文档未同步更新，请以 v2 接口定义为准。

## 关键参数

所有 Realtime API 均通过 WebSocket 连接初始化，必需参数如下：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen2-audio-asr-base`、`qwen2-audio-tts-zh`；必须与所选能力匹配 |
| `api_key` | string | 是 | 项目级 API Key，需在百炼控制台开通 Realtime 权限 |
| `stream` | boolean | 否（默认 `true`） | 是否启用流式响应；设为 `false` 将退化为单次请求-响应模式（不推荐） |
| `sample_rate` | integer | ASR/TTS 必填 | 音频采样率，支持 8000 / 16000 Hz；ASR 输入与 TTS 输出需严格一致 |
| `language` | string | ASR/TTS/LiveTranslate 必填 | 如 `zh-CN`、`en-US`；多语种场景需显式指定主语言 |

其他协议相关参数（如 `enable_interim_results`、`voice`、`translation_target`）详见各子能力文档，例如 [实时语音识别](raw/model-api-reference/realtime-api-directory/realtime-asr-model-apis.md) 和 [实时音视频翻译](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory.md)。

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/{service}` 发起连接（`{service}` 取值如 `asr`、`tts`、`audio` 等）  
2. **发送初始化消息（`session.update`）**：携带上述关键参数及可选配置（如 `max_duration_ms`、`silence_threshold_ms`）  
3. **流式发送音频/文本/图像数据帧（`input.audio` / `input.text` / `input.image`）**  
4. **接收服务端事件（`response.audio.delta`、`response.text.delta`、`response.transcript` 等）**  
5. **主动关闭或处理连接异常**：建议实现心跳保活（`ping/pong`）与断线自动重连逻辑  

完整交互流程与示例代码参见 [实时多模态](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory.md) 文档中的协议状态机图示。

## 限制和注意事项

- 单连接最大持续时长：**30 分钟**（超时后需重建连接）  
- 音频输入帧大小：单帧 ≤ 64KB，推荐 20–200ms PCM 数据（16-bit little-endian）  
- 并发连接数：免费版 ≤ 2，企业版按配额计费（见控制台「实时 API 配额」页）  
- 不支持跨区域调用：连接 endpoint 必须与模型部署地域一致（如 `cn-shanghai` 模型不可用 `us-west-1` endpoint）  
- 所有音频流必须为单声道；立体声输入将被静音左声道或触发 `error.invalid_audio_format`  
- 客户端需自行处理网络抖动与丢包：服务端不保证音频帧顺序，但保证语义完整性（通过 `sequence_id` 与 `timestamp` 辅助对齐）  

> **注意**：[实时语音合成](raw/model-api-reference/realtime-api-directory/realtime-tts-model-apis.md) 文档中提及的 `output_format=mp3` 选项目前已下线，仅支持 `pcm` 和 `wav`（无压缩），该变更未在原文中同步标注，实际调用请以 OpenAPI Schema 为准。

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-directory.md)


