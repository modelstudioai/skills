# voice customization api directory

音色定制 API 提供语音模型的个性化音色生成能力，支持从原始音频中复刻特定人声（音色复刻），或通过文本描述与参数组合设计全新音色（音色设计）。所有接口均基于百炼平台统一鉴权与[异步任务](../concepts/asynchronous-task.md)调度机制，适用于 TTS 场景下的高保真、可控语音合成。当前功能仅对已开通权限的企业用户开放。

## 支持的模型/功能

- **音色复刻**：基于 3–10 秒高质量单人语音样本，生成可调参的复刻音色 ID，支持后续批量合成。该能力依赖 `qwen-audio-2.5` 底层语音模型，需上传 `.wav`（16kHz/16bit/单声道）格式样本。  
- **音色设计**：通过自然语言描述（如“年轻女声、语速偏慢、略带笑意”）结合显式参数（如 `pitch=5`, `energy=3`）生成音色配置，无需原始音频。对应接口详见 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。  
- > **注意**：[音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 文档中提及的“支持 MP3 输入”与当前生产环境实际限制（仅接受 WAV）存在不一致，以 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 的最新服务端校验逻辑为准——MP3 将被拒绝并返回 `400 UnsupportedFormat`。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `voice_id` | string | 是（复刻场景） / 否（设计场景） | 复刻生成的音色 ID；音色设计时留空，由系统返回新 ID |
| `prompt` | string | 否（复刻） / 是（设计） | 自然语言音色描述，长度 ≤ 128 字符 |
| `sample_rate` | integer | 否 | 输出音频采样率，支持 `16000`（默认）、`24000`；`24000` 仅对复刻音色生效 |
| `temperature` | float | 否 | 语音表现力控制（0.1–1.0），值越高越富变化；默认 `0.5` |

## 使用方式

1. 调用 `/v1/voice/customize/create` 提交复刻或设计请求（见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 和 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 的完整请求示例）；  
2. 获取 `task_id`，轮询 `/v1/voice/customize/status?task_id={id}` 查询状态，成功后返回 `voice_id`；  
3. 使用该 `voice_id` 调用标准 TTS 接口（如 `/v1/audio/speech`）进行合成。

## 限制和注意事项

- 单次复刻任务最多上传 3 段样本（总时长 ≤ 15 秒），样本间静音间隔需 ≥ 0.5 秒；  
- 音色设计 prompt 中禁止包含真实人名、品牌名或政治敏感表述，否则返回 `422 InvalidPrompt`；  
- 所有音色 ID 默认有效期为 90 天，过期后不可用于合成，但可通过 `/v1/voice/customize/refresh` 延期一次（+30 天）；  
- [异步任务](../concepts/asynchronous-task.md)超时时间为 120 秒，超时后状态置为 `failed`，需重试。

## 来源文档

- [音色定制](../../raw/model-api-reference/voice-customization-api-directory.md)


