# voice customization api directory

音色定制 API 提供语音克隆与合成能力，支持基于少量音频样本复刻目标音色，或通过文本描述生成全新音色。该能力面向需要个性化语音交互的开发者，适用于智能助手、有声内容生成等场景。所有接口均需通过百炼平台认证后调用。

## 支持的模型/功能

当前开放两类核心能力：
- **音色复刻**：基于用户上传的 3–10 秒高质量单人语音样本（无背景音、无混响），生成高保真复刻音色，支持实时推理与批量合成。详见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。
- **音色设计**：不依赖原始语音样本，仅通过自然语言描述（如“年轻女声，语速适中，带轻微粤语口音”）生成可控音色，适用于创意语音内容生产。详见 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

> **注意**：[音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 文档中声明支持 1 秒最小样本时长，但最新 SDK v2.3.0 实际要求不低于 3 秒；请以 SDK 错误提示及 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 的“限制和注意事项”节为准。

## 关键参数

通用必填参数（所有子接口共用）：
- `model`: 字符串，取值为 `voice-customization-sr`（复刻）或 `voice-customization-vd`（设计）
- `input.text`: 合成文本（UTF-8，最大 500 字符）
- `voice_id`: 复刻场景下为已创建的音色 ID；设计场景下可留空，由系统动态生成

复刻专属参数：
- `audio_url`: 指向 WAV/PCM 格式样本的公网可访问 URL（HTTPS，≤10 MB）

设计专属参数：
- `voice_description`: 描述性字符串（最大 200 字符），影响音色风格与韵律

## 使用方式

1. 调用 `/v1/voices/create` 创建音色（复刻需传 `audio_url`，设计需传 `voice_description`）  
2. 获取返回的 `voice_id`  
3. 调用 `/v1/audio/speech` 提交合成请求，携带 `voice_id` 和 `input.text`  
完整流程示例见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 的“快速开始”节。

## 限制和注意事项

- 单次请求 `input.text` 不得超过 500 字符；超长文本需分段调用并自行拼接音频
- 复刻样本必须为单人、纯净语音；含音乐/噪声/多人对话将导致失败或音质劣化
- 所有音色 ID 有效期为 90 天，过期后需重新创建；设计类音色不支持持久化存储
- 音频输出格式固定为 `mp3`（16kHz，单声道），暂不支持 WAV 或采样率调整 —— 此限制在 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中未明确说明，但实测响应头 `Content-Type: audio/mpeg` 可验证

## 来源文档

- [音色定制](../../raw/model-api-reference/voice-customization-api-directory.md)


