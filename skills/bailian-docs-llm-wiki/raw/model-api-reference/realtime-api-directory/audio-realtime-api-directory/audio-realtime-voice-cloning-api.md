# Qwen-Audio-Realtime 音色配置

创建复刻音色后，在 Qwen-Audio-Realtime 会话中使用音色，并查阅对应 HTTP API。

通过声音复刻接口创建、查询、更新和删除 Qwen-Audio-Realtime 音色。创建时的 `target_model` 必须与使用音色的模型一致。参考[音频要求](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc02_audio_h2)准备样本，完整示例参见[声音复刻用户指南](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#qar_vc_h3)。

创建音色免费，使用复刻音色进行实时对话时按目标模型计费，详见[计费说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_billing_h3)。音色数量限制参见[配额与限制](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。

## 在实时对话中使用音色

连接与创建音色时相同的 Qwen-Audio-Realtime 模型，在首次 [session.update](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/fun-audiochat-client-events.md) 中将 `voice` 设置为返回的 `voice_id`。音色状态为 `OK` 后可使用。

```
{
  "type": "session.update",
  "session": {
    "voice": "VOICE_ID"
  }
}
```

## 接口地址

参见[音色复刻 HTTP API：接口地址](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-url)。

## 请求头

参见[音色复刻 HTTP API：请求头](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-headers)。

## 创建音色

参见[音色复刻 HTTP API：创建音色](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-create)。

参见[音色复刻 HTTP API：请求体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-cr-rq)。

参见[音色复刻 HTTP API：返回体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-cr-rs)。

## 查询音色列表

参见[音色复刻 HTTP API：查询音色列表](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-list)。

参见[音色复刻 HTTP API：请求体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-ls-rq)。

参见[音色复刻 HTTP API：返回体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-ls-rs)。

## 查询音色详情

参见[音色复刻 HTTP API：查询音色详情](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-query)。

参见[音色复刻 HTTP API：请求体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-qr-rq)。

参见[音色复刻 HTTP API：返回体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-qr-rs)。

## 更新音色

参见[音色复刻 HTTP API：更新音色](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-update)。

参见[音色复刻 HTTP API：请求体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-up-rq)。

参见[音色复刻 HTTP API：返回体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-up-rs)。

## 删除音色

参见[音色复刻 HTTP API：删除音色](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-delete)。

参见[音色复刻 HTTP API：请求体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-dl-rq)。

参见[音色复刻 HTTP API：返回体](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h3-dl-rs)。

## 音色状态说明

参见[音色复刻 HTTP API：音色状态说明](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-status)。
