# Qwen-Audio-Realtime 音色配置

创建复刻音色后，在 Qwen-Audio-Realtime 会话中使用音色，并查阅对应 HTTP API。

通过声音复刻接口创建、查询、更新和删除 Qwen-Audio-Realtime 音色。创建时的 `target_model` 必须与使用音色的模型一致。参考[音频要求](../../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md#vc02_audio_h2)准备样本，完整示例参见[声音复刻用户指南](../../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md#qar_vc_h3)。

创建音色免费，使用复刻音色进行实时对话时按目标模型计费，详见[计费说明](../../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md#vc07_billing_h3)。音色数量限制参见[配额与限制](../../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md#vc07_quota_h2)。

<a id="在实时对话中使用音色"></a>

## 在实时对话中使用音色

连接与创建音色时相同的 Qwen-Audio-Realtime 模型，在首次 [session.update](fun-audiochat-client-events.md) 中将 `voice` 设置为返回的 `voice_id`。音色状态为 `OK` 后可使用。

<a id="code-block"></a>

```json
{
  "type": "session.update",
  "session": {
    "voice": "VOICE_ID"
  }
}
```

<a id="接口地址"></a>

<a id="h2-url"></a>

## 接口地址

参见[音色复刻 HTTP API：接口地址](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-url)。

<a id="请求头"></a>

<a id="h2-headers"></a>

## 请求头

参见[音色复刻 HTTP API：请求头](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-headers)。

<a id="创建音色"></a>

<a id="h2-create"></a>

<a id="h3-create-enrollment"></a>

## 创建音色

参见[音色复刻 HTTP API：创建音色](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-create)。

<a id="h3-cr-rq"></a>

参见[音色复刻 HTTP API：请求体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-cr-rq)。

<a id="h3-cr-rs"></a>

参见[音色复刻 HTTP API：返回体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-cr-rs)。

<a id="查询音色列表"></a>

<a id="h2-list"></a>

## 查询音色列表

参见[音色复刻 HTTP API：查询音色列表](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-list)。

<a id="h3-ls-rq"></a>

参见[音色复刻 HTTP API：请求体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-ls-rq)。

<a id="h3-ls-rs"></a>

参见[音色复刻 HTTP API：返回体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-ls-rs)。

<a id="查询音色详情"></a>

<a id="h2-query"></a>

## 查询音色详情

参见[音色复刻 HTTP API：查询音色详情](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-query)。

<a id="h3-qr-rq"></a>

参见[音色复刻 HTTP API：请求体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-qr-rq)。

<a id="h3-qr-rs"></a>

参见[音色复刻 HTTP API：返回体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-qr-rs)。

<a id="更新音色"></a>

<a id="h2-update"></a>

## 更新音色

参见[音色复刻 HTTP API：更新音色](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-update)。

<a id="h3-up-rq"></a>

参见[音色复刻 HTTP API：请求体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-up-rq)。

<a id="h3-up-rs"></a>

参见[音色复刻 HTTP API：返回体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-up-rs)。

<a id="删除音色"></a>

<a id="h2-delete"></a>

## 删除音色

参见[音色复刻 HTTP API：删除音色](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-delete)。

<a id="h3-dl-rq"></a>

参见[音色复刻 HTTP API：请求体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-dl-rq)。

<a id="h3-dl-rs"></a>

参见[音色复刻 HTTP API：返回体](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h3-dl-rs)。

<a id="音色状态说明"></a>

<a id="h2-status"></a>

## 音色状态说明

参见[音色复刻 HTTP API：音色状态说明](../../../_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-status)。
