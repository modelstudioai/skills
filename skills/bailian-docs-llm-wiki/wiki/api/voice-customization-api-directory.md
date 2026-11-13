# voice customization api directory

本目录汇总百炼平台支持的音色定制类 API，涵盖音色复刻（voice cloning）与音色设计（voice design）两大能力。所有接口均通过统一的 `/api/v1/services/audio/tts/customization` 路径提供，以 `model="voice-enrollment"` 为标识，支持 Qwen-Audio 和 CosyVoice 系列模型。开发者需先[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并按地域配置 Workspace ID 与对应 API Key。

## 支持的模型/功能

当前支持两类音色生成方式：

- **音色复刻**：基于参考音频（3–30 秒）提取说话人声学特征，生成高保真复刻音色。适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime 及 CosyVoice 系列模型，详见 [音色复刻](raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。
- **音色设计**：通过文本描述（如“沉稳的中年男性，音色低沉浑厚”）和预览文本生成合成音色，无需原始音频。仅适用于 Qwen-Audio-TTS 和 CosyVoice 的语音合成场景，不支持 Realtime 模型。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已过时或迁移；其复刻能力已统一归入 `voice-enrollment` 接口体系，旧 MiniMax 接口说明已移至 [MiniMax HTTP API](https://help.aliyun.com/zh/model-studio/mini-clone-api)，**不再推荐使用**。实际可用模型请严格以 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 中列出的支持列表为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定为 `"voice-enrollment"` |
| `input.action` | string | 是 | 操作类型：`create_voice` / `list_voice` / `query_voice` / `update_voice` / `delete_voice` |
| `input.target_model` | string | 创建/更新时必填 | 目标驱动模型，必须与后续 TTS/Realtime 调用一致。支持型号见 [HTTP API 参考](raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) |
| `input.prefix` | string | 创建时必填 | 音色名称前缀（≤10 字母/数字），生成格式为 `{target_model}-{prefix}-{id}`（复刻）或 `{target_model}-vd-{prefix}-{id}`（设计） |
| `input.audio` 或 `input.url` | string | 创建/更新时必填（复刻） | 复刻用参考音频：支持公网 URL 或 `data:audio/wav;base64,...` 格式；`url` 将逐步废弃，建议优先用 `audio` |
| `input.voice_prompt` | string | 创建时必填（设计） | 声音描述文本（中文/英文，≤500 字） |
| `input.preview_text` | string | 创建时必填（设计） | 预览音频对应文本（15–200 字，中文/英文） |
| `input.language_hints` | string[] | 可选 | 语种提示（长度必须为 1），影响特征提取或发音倾向；默认 `["zh"]` |
| `input.max_prompt_audio_length` | float | 可选（复刻） | 参考音频最大处理时长（秒），范围 `[3.0, 30.0]`，默认 `10.0` |
| `input.enable_preprocess` | boolean | 可选（复刻） | 是否开启降噪/增强/音量规整，默认 `false` |
| `input.enable_volume_normalization` | string / boolean | 可选（复刻） | 音量归一化开关（HTTP 传 `"true"/"false"`，Python SDK 传 `bool`，Java SDK 传 `"true"/"false"`） |

## 使用方式

### 1. 统一接入点
- **华北2（北京）**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
- **新加坡**：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
⚠️ `{WorkspaceId}` 需替换为控制台业务空间详情页中的真实 ID；两地 API Key **不互通**。

### 2. 鉴权与请求头
- `Authorization`: `Bearer <your_api_key>`（从环境变量 `DASHSCOPE_API_KEY` 读取）  
- `Content-Type`: `application/json`

### 3. SDK 快速接入
- **Python**：使用 `dashscope.Client(audio.voices.*)`，详见 [Python SDK 参考](raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)  
- **Java**：使用 `VoiceEnrollmentService`，详见 [Java SDK 参考](raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)  
- 所有 SDK 均要求显式配置 `workspace`（或 `Constants.baseHttpApiUrl`）与 `region`，且地域设置为 Client/全局级。

## 限制和注意事项

- **配额与计费**：Qwen-Audio-Realtime 复刻创建免费，但模型调用按目标模型计费；TTS/CosyVoice 复刻与设计均计入配额，详情见 [配额说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。
- **音频要求**：复刻参考音频需清晰、安静、无混响，采样率建议 16–48 kHz，格式支持 WAV/MP3/FLAC；设计无音频输入要求。
- **状态流转**：新创建音色初始状态为 `DEPLOYING`，审核通过后变为 `OK` 方可使用；`UNDEPLOYED` 表示审核失败，不可调用。
- **地域隔离**：北京与新加坡的 Workspace ID、API Key、域名完全独立，不可跨地域复用。
- **参数兼容性**：`language_hints`、`max_prompt_audio_length`、`enable_preprocess` 等高级参数**仅对指定模型版本生效**（如 `qwen-audio-3.1-tts-plus`），使用前请核对 [HTTP API 参考](raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 中的模型支持列表。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)


