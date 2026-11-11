# Qwen-LiveTranslate-Realtime WebSocket 接入

Qwen-LiveTranslate-Realtime WebSocket 接入

## 适用范围

本文面向 Qwen-LiveTranslate-Realtime，示例模型为 `qwen3.8-livetranslate-flash-realtime`。系列指南还列有 `qwen3.5-livetranslate-flash-realtime` 和快照版 `qwen3.5-livetranslate-flash-realtime-2026-05-19`。3.8 与 3.5 的配置和事件字段不同，按所选型号查阅事件参考。

-   使用所选地域和业务空间对应的 [API Key](raw/model-api-reference/preparations/get-api-key.md) 与 [API Host](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)（不含协议和路径）。
-   北京域名：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；新加坡域名：`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。
-   长期 API Key 保存在服务端，不放入浏览器或移动端应用。

## 地址与鉴权

以下地址默认为北京地域，请将域名替换为业务空间对应的 API Host，并按需修改模型名称。

```
wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-livetranslate-flash-realtime
```

新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-livetranslate-flash-realtime`

其他域名的说明请参见 [Python SDK](https://help.aliyun.com/zh/model-studio/qwen-livetranslate-python-sdk#lt001prereqh2)。

在 WebSocket 握手请求头中设置 `Authorization: Bearer <API_KEY>`。不要把长期 API Key 放入浏览器或移动端。

可选的 `user-agent` 请求头用于标识客户端。通用 WebSocket 接入资料还列有 `X-DashScope-WorkSpace`（业务空间 ID）和 `X-DashScope-DataInspection`（数据合规检查配置），这两个请求头按模型要求使用。

临时 API Key 的生成方式和权限说明参见[生成临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

## 会话配置

建立连接并收到 `session.created` 后发送 `session.update`。收到 `session.updated` 确认后再发送输入；错误通过 `error` 事件处理。

以下示例对应 `qwen3.8-livetranslate-flash-realtime`，其他版本使用各自事件参考中的配置，不混用字段层级。示例开启实时声音复刻，`frequency: once` 在会话开始时提取一次输入音色并在后续复用，适合单人场景。详情请参见[声音复刻](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#8q75hr4eu55j0)。

```
{
  "type": "session.update",
  "session": {
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
      }
    },
    "voice": "default",
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

使用 `qwen3.5-livetranslate-flash-realtime` 时，配置和事件与上述 3.8 示例不同：

-   输出模态使用 `session` 中的 `modalities`，可选值和默认值与 3.8 的 `output_modalities` 相同。
-   可通过 `session` 的 `input_audio_transcription` 对象中的 `language` 指定源语种；省略时自动识别。
-   原文识别增量使用 `conversation.item.input_audio_transcription.text`；3.8 使用 `conversation.item.input_audio_transcription.delta`。
-   仅输出文本时，3.5 通过 `response.text.text` 返回译文增量，3.8 使用 `response.text.delta`。输出文本和音频时，3.5 通过 `response.audio_transcript.text` 返回译文增量，3.8 使用 `response.audio_transcript.delta`。

完整字段、默认值和事件参见[客户端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)、[服务端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)和[实时语音翻译指南](raw/model-user-guide/model-experience/omni-modal/qwen3-5-livetranslate-flash-realtime.md)。

## 输入、结果与结束

音频通过 `input_audio_buffer.append` 发送；输入格式、提交条件和图像输入限制见[客户端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)。处理[服务端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)中的结果、状态和错误，不将连接建立视为业务请求已完成。

实时翻译使用本模型的翻译配置和事件，不套用 Omni 的 `response.create` 对话流程。输入结束后发送 `session.finish`，保持连接并继续接收剩余结果，收到 `session.finished` 后再关闭 WebSocket 连接。需要完整播放译音时，先完成本地播放收尾。具体事件字段见[客户端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)和[服务端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-server-events.md)。

## 错误处理

握手失败时，核对域名、地域、业务空间、API Key、模型名称及模型开通状态与权限。连接建立后，根据 `error` 事件定位问题，并参见[错误码](raw/model-api-reference/preparations/error-code.md)。保留事件 ID 便于排查，不以无响应判定协议不支持。

## SDK 与参考

-   [Python SDK](raw/_short/qwen-livetranslate-python-sdk-147cd38a2304509b.md)
-   [Java SDK](raw/_short/qwen-livetranslate-java-sdk-edfabe658a0fa5ea.md)
