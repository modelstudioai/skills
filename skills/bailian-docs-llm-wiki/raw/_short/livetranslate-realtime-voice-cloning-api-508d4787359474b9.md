# Qwen-LiveTranslate-Realtime 音色配置

配置实时提取输入音色或使用预建音色，并查阅预建音色 API。

`qwen3.8-livetranslate-flash-realtime` 和 `qwen3.5-livetranslate-flash-realtime` 可以在翻译时从输入音频提取音色，也可以使用提前创建的固定音色。实时复刻不额外收取复刻费用；提前创建音色另行计费。模型调用仍按 Token 用量计费，详情参见[计费说明](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#e02a82e668y2c)。

## 配置会话

在 [session.update](https://help.aliyun.com/zh/model-studio/live-translator-client-events#af43722339yva) 中设置 `enable_voice_clone`、`voice_clone_options.frequency` 和 `voice`。以下示例以 WebSocket 接入的 `qwen3.8-livetranslate-flash-realtime` 为例。使用 `qwen3.5-livetranslate-flash-realtime` 时，将 `output_modalities` 改为 `modalities`，其余声音复刻参数相同。

方式

`frequency`

`voice`

说明

实时复刻一次

`once`

`default`

会话开始时从输入音频提取一次音色，后续输出复用该音色。

持续实时复刻

`always`

`default`

每次输出前从输入音频提取音色，适用于多人对话。

使用预建音色

`never`

预建音色 ID

不在本次翻译中重新提取音色，使用事先创建的固定音色。

`frequency` 为 `once` 或 `always` 时，`voice` 必须为 `default`；预建音色的目标模型须与会话模型一致。

#### 实时复刻一次

```
{
  "type": "session.update",
  "session": {
    "output_modalities": ["text", "audio"],
    "voice": "default",
    "translation": {"language": "en"},
    "enable_voice_clone": true,
    "voice_clone_options": {"frequency": "once"}
  }
}
```

#### 持续实时复刻

```
{
  "type": "session.update",
  "session": {
    "output_modalities": ["text", "audio"],
    "voice": "default",
    "translation": {"language": "en"},
    "enable_voice_clone": true,
    "voice_clone_options": {"frequency": "always"}
  }
}
```

#### 使用预建音色

```
{
  "type": "session.update",
  "session": {
    "output_modalities": ["text", "audio"],
    "voice": "VOICE_ID",
    "translation": {"language": "en"},
    "enable_voice_clone": true,
    "voice_clone_options": {"frequency": "never"}
  }
}
```

## 创建预建音色

使用[创建预建音色 API](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#h2-create)。`target_model` 须与之后翻译会话使用的模型一致。

### 请求体

字段定义参见[预建音色 API](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#h2-create)。

### 请求示例

完整请求与响应示例参见[创建预建音色](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#h2-create)。

## 删除预建音色

参见[删除预建音色 API](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning#h2-delete)。

更多交互步骤参见[实时语音/音视频翻译](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#8q75hr4eu55j0)。
