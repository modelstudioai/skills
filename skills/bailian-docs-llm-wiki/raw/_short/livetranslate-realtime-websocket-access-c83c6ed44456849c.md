# Qwen-LiveTranslate-Realtime WebSocket 接入

Qwen-LiveTranslate-Realtime WebSocket 接入

<a id="适用范围"></a>

## 适用范围

本文面向 Qwen-LiveTranslate-Realtime，示例模型为 `qwen3.8-livetranslate-flash-realtime`。系列指南还列有 `qwen3.5-livetranslate-flash-realtime` 和快照版 `qwen3.5-livetranslate-flash-realtime-2026-05-19`。3.8 与 3.5 的配置和事件字段不同，按所选型号查阅事件参考。

-   使用所选地域和业务空间对应的 [API Key](../model-api-reference/preparations/get-api-key.md) 与 [API Host](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)（不含协议和路径）。
-   北京域名：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；新加坡域名：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。
-   长期 API Key 保存在服务端，不放入浏览器或移动端应用。

<a id="地址与鉴权"></a>

## 地址与鉴权

通过查询参数 `model` 指定要调用的模型。

WebSocket`wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-livetranslate-flash-realtime`

WebSocket`wss://WorkspaceId.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-livetranslate-flash-realtime`

其他域名的说明请参见 [Python SDK](realtime-websocket-python-sdk-qwen-livetranslate-8af00207378f749b.md#model-qwen-livetranslate-realtime-lt001prereqh2)。

在 WebSocket 握手请求头中设置 `Authorization: Bearer <API_KEY>`。不要把长期 API Key 放入浏览器或移动端。

可选的 `user-agent` 请求头用于标识客户端。通用 WebSocket 接入资料还列有 `X-DashScope-WorkSpace`（业务空间 ID）和 `X-DashScope-DataInspection`（数据合规检查配置），这两个请求头按模型要求使用。

临时 API Key 的生成方式和权限说明参见[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)。

<a id="会话配置"></a>

## 会话配置

建立连接并收到 `session.created` 后发送 `session.update`。收到 `session.updated` 确认后再发送输入；错误通过 `error` 事件处理。

以下示例使用 `qwen3.8-livetranslate-flash-realtime`，开启音频和图片输入。仅发送音频时，可省略 `input_modalities` 或设为 `["audio"]`。

示例还开启实时声音复刻。`frequency: once` 在会话开始时提取一次输入音色，供后续翻译复用，适合单人场景。详情参见[声音复刻](../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md#8q75hr4eu55j0)。

<a id="code-block"></a>

```json
{
  "type": "session.update",
  "session": {
    "input_modalities": [
      "audio",
      "video"
    ],
    "output_modalities": [
      "text",
      "audio"
    ],
    "audio": {
      "input": {
        "turn_detection": {
          "type": "speaker_detection",
          "threshold": 0.5
        }
      },
      "output": {
        "voice": "default"
      }
    },
    "enable_voice_clone": true,
    "voice_clone_options": {
      "frequency": "once"
    },
    "translation": {
      "language": "en",
      "corpus": {
        "phrases": {
          "人工智能": "Artificial Intelligence",
          "机器学习": "Machine Learning"
        }
      }
    }
  }
}
```

使用 `qwen3.5-livetranslate-flash-realtime` 时，按[客户端事件中的 3.5 示例](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md#af43722339yva)构造请求。配置和事件与 3.8 有以下差异：

-   输出模态使用 `session` 中的 `modalities`，可选值和默认值与 3.8 的 `output_modalities` 相同。
-   使用顶层 `session.voice` 设置音色。
-   可通过 `session` 的 `input_audio_transcription` 对象中的 `language` 指定源语种；省略时自动识别。
-   原文识别增量使用 `conversation.item.input_audio_transcription.text`；3.8 使用 `conversation.item.input_audio_transcription.delta`。
-   仅输出文本时，3.5 通过 `response.text.text` 返回译文增量，3.8 使用 `response.text.delta`。输出文本和音频时，3.5 通过 `response.audio_transcript.text` 返回译文增量，3.8 使用 `response.audio_transcript.delta`。

完整字段、默认值和事件参见[客户端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)、[服务端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)和[实时语音翻译指南](../model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md)。

<a id="输入-结果与结束"></a>

## 输入、结果与结束

音频通过 `input_audio_buffer.append` 发送；输入格式、提交条件和图像输入限制见[客户端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)。处理[服务端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)中的结果、状态和错误，不将连接建立视为业务请求已完成。

使用 `qwen3.8-livetranslate-flash-realtime` 时，按 PCM 24 kHz 播放译音。

实时翻译使用本模型的翻译配置和事件，不套用 Omni 的 `response.create` 对话流程。输入结束后发送 `session.finish`，保持连接并继续接收剩余结果，收到 `session.finished` 后再关闭 WebSocket 连接。需要完整播放译音时，先完成本地播放收尾。具体事件字段见[客户端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)和[服务端事件](../model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)。

<a id="错误处理"></a>

## 错误处理

握手失败时，核对域名、地域、业务空间、API Key、模型名称及模型开通状态与权限。连接建立后，根据 `error` 事件定位问题，并参见[错误码](../model-api-reference/preparations/error-code.md)。保留事件 ID 便于排查，不以无响应判定协议不支持。

<a id="sdk-与参考"></a>

## SDK 与参考

-   [Python SDK](realtime-websocket-python-sdk-qwen-livetranslate-8af00207378f749b.md)
-   [Java SDK](qwen-livetranslate-java-sdk-7300d52ae3d2839e.md)

<a id="可用的-sdk"></a>

## 可用的 SDK

-   [Python SDK](realtime-websocket-python-sdk-qwen-livetranslate-8af00207378f749b.md)
-   [Java SDK](qwen-livetranslate-java-sdk-7300d52ae3d2839e.md)
-   [C# SDK](qwen-livetranslate-csharp-sdk-7dc0bd18d993e44e.md)

![](data:image/png;base64,)
