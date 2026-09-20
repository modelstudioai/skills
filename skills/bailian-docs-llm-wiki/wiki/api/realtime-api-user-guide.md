# realtime api user guide

Realtime API 是百炼平台提供的低延迟、流式语音交互接口，适用于实时语音识别（ASR）、语音合成（TTS）及语音到语音（V2V）等端到端实时场景。它基于 WebSocket 协议实现双向流式通信，支持音频流边传边处理，端到端延迟通常低于 300ms。该接口不适用于批量离线任务，如需异步长任务请使用 [Batch API](../../raw/model-api-reference/batch-api-user-guide.md)。

## 支持的模型与功能

- **ASR 模型**：`qwen-audio-realtime-v1`（默认），支持中文普通话、英文及中英混说，采样率 16kHz，单通道 PCM 音频  
- **TTS 模型**：`qwen-tts-realtime-v1`，支持音色克隆（需提前注册声纹）和语速/音调调节  
- **V2V 模型**：`qwen-v2v-realtime-v1`（Beta），支持实时语音转译+合成（如中→英同传播报）  
- 所有模型均要求输入音频为 `audio/pcm; rate=16000; channels=1`，输出文本/音频流严格按帧序返回  
- 更多模型能力细节见 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 必须为上述支持的模型 ID，如 `"qwen-audio-realtime-v1"` |
| `audio_format` | string | 否 | 默认 `"pcm"`；暂不支持 `wav` 或 `mp3` 封装（需自行解封装） |
| `enable_interim_results` | boolean | 否 | 默认 `false`；设为 `true` 可返回中间识别结果（ASR 场景） |
| `voice_id` | string | 否 | TTS/V2V 场景必填，值为已注册的声纹 ID（参见 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)） |
| `max_duration_sec` | integer | 否 | 单次会话最大时长，默认 `120`（秒），上限 `300` |

> **注意**：原始文档中 [快速开始](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide.md) 示例误将 `audio_format` 写为 `"wav"`，实际仅支持裸 PCM 流；请以本节说明为准。

## 使用方式

1. **建立 WebSocket 连接**：向 `wss://dashscope.aliyuncs.com/realtime/v1/chat` 发起连接（需携带 `Authorization: Bearer <api_key>`）  
2. **发送初始化消息**（JSON）：
   ```json
   {
     "type": "session.update",
     "session": {
       "model": "qwen-audio-realtime-v1",
       "enable_interim_results": true
     }
   }
   ```
3. **逐帧发送音频数据**（二进制，每帧 ≤ 20ms PCM 数据，即 320 字节 @16kHz/16bit）  
4. **接收响应流**：服务端按帧返回 `type: "response.audio.delta"` 或 `type: "response.text.delta"` 等事件  
5. 客户端 SDK 推荐使用官方 [AOQ客户端SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md)，已封装重连、心跳、帧对齐等逻辑  

## 限制和注意事项

- 单连接最大并发数：1（不支持复用连接处理多路音频）  
- 音频帧间隔建议 ≤ 50ms，超时 200ms 将触发会话中断  
- 不支持热词增强（`custom_keywords` 参数在 Realtime API 中无效；如需定制识别请使用 [ASR Batch API](../../raw/model-api-reference/asr-batch-api-user-guide.md)）  
- 错误码 `429 Too Many Requests` 表示 QPS 超限，需检查配额或降频；详细错误映射见 [概述](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)  
- 所有音频数据在连接关闭后立即销毁，平台不持久化存储原始音频流

## 来源文档

- [Realtime API](../../raw/model-api-reference/realtime-api-user-guide.md)


