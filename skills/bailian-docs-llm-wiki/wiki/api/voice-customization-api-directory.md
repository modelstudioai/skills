# voice customization api directory

本目录汇总百炼平台支持的音色定制能力，涵盖音色复刻（Voice Cloning）与音色设计（Voice Design）两类核心 API。所有能力均通过统一的 `voice-enrollment` 模型接口提供，支持 Qwen-Audio 和 CosyVoice 系列模型，开发者可基于参考音频或文本描述创建、管理并调用定制化音色。

## 支持的模型/功能

当前支持两类音色生成方式：

- **音色复刻（Voice Cloning）**：基于一段参考音频（3–30 秒）复刻原始说话人音色，适用于需高度还原特定人声的场景。支持模型包括：
  - Qwen-Audio-TTS 系列：`qwen-audio-3.0/3.1-tts-plus/flash`
  - Qwen-Audio-Realtime 系列：`qwen-audio-3.0/3.1-realtime-plus/flash`
  - CosyVoice 系列：`cosyvoice-v3/v3.5-plus/flash`
  
  详细支持模型列表及语言覆盖见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。

- **音色设计（Voice Design）**：基于自然语言描述（如“沉稳的中年男性，音色低沉浑厚”）和预览文本生成全新音色，无需原始音频。仅支持 `cosyvoice-v3.5-plus` 等指定 CosyVoice 模型，详见 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已过时或迁移至外部文档；其当前不归属本 `voice-enrollment` 统一 API 体系，实际集成请以 [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md) 为准。

## 关键参数

所有操作（创建/查询/更新/删除）均通过 `input.action` 指定行为，核心参数如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `target_model` | string | 是 | 目标语音合成模型（如 `cosyvoice-v3.5-plus`），必须与后续 TTS 调用模型严格一致，否则失败。 |
| `prefix` | string | 是（创建时） | 音色名称前缀（仅字母数字，≤10 字符）；生成 ID 格式为 `{target_model}-{prefix}-{uuid}`（复刻）或 `{target_model}-vd-{prefix}-{uuid}`（设计）。 |
| `audio` 或 `url` | string | 是（复刻创建/更新） | 参考音频地址：公网 URL 或 `data:audio/wav;base64,...` Data URI。`url` 已标记为兼容旧参数，[HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 明确建议优先使用 `audio`。 |
| `voice_prompt` | string | 是（设计创建） | 声音描述文本（中/英文，≤500 字符）。 |
| `preview_text` | string | 是（设计创建） | 用于生成预览音频的文本（中/英文，15–200 字符）。 |
| `language_hints` | array[string] | 否 | 语种提示（如 `["zh"]`），长度必须为 1；若与实际音频/文本不符则被忽略。复刻与设计均支持，但设计要求 `language_hints` 与 `preview_text` 语种一致。 |
| `max_prompt_audio_length` | float | 否 | 复刻时参考音频最大有效时长（秒），范围 `[3.0, 30.0]`，默认 `10.0`。 |
| `enable_preprocess` | bool / boolean | 否 | 是否开启音频预处理（降噪/增强/规整），默认 `false`；嘈杂环境建议设为 `true`。 |
| `enable_volume_normalization` | string / bool | 否 | 音量归一化开关，HTTP API 接受 `"true"`/`"false"` 字符串，SDK 接口类型略有差异（见下文），默认 `"false"`。 |

## 使用方式

### 接口地址与鉴权
- **统一 endpoint**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
  支持地域：`cn-beijing`（华北2）、`ap-southeast-1`（新加坡）。务必替换 `{WorkspaceId}` 并使用对应地域的 API Key。
- **请求头**：`Authorization: Bearer <your_api_key>`，`Content-Type: application/json`。
- **强烈建议**：迁移到业务空间专属域名（如 `xxx.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 —— 此要求在 [Python SDK](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)、[HTTP API](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 和 [Java SDK](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md) 中均被明确强调。

### SDK 快速接入
- **Python**：使用 `dashscope.Client.audio.voices.*` 方法（`create`/`list`/`get`/`update`/`delete`），详见 [Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。
- **Java**：使用 `VoiceEnrollmentService` 类，注意全局设置 `Constants.baseHttpApiUrl`，参数通过 `VoiceEnrollmentParam.builder()` 构建。
- **HTTP**：统一 POST 请求，`input.action` 控制操作类型，`model` 固定为 `"voice-enrollment"`。

## 限制和注意事项

- **配额与计费**：Qwen-Audio-Realtime 复刻创建免费，但模型调用按目标模型计费；其他模型创建与调用均计入配额。具体限额见 [声音复刻用户指南](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。
- **音频要求**：复刻参考音频需清晰、安静、无明显剪辑痕迹，推荐采样率 16–48 kHz，格式 WAV/MP3/OGG；设计无音频输入要求。
- **状态流转**：新创建音色初始状态为 `DEPLOYING`（审核中），成功后变为 `OK`，失败则为 `UNDEPLOYED`；仅 `OK` 状态音色可用于合成。
- **地域隔离**：Workspace ID、API Key、Endpoint 均按地域独立，跨地域调用将失败。
- **参数兼容性**：`enable_volume_normalization` 在 HTTP API 中为字符串（`"true"`/`"false"`），而在 Python SDK 中为布尔值，Java SDK 则接受字符串 —— 开发者需按所选 SDK 类型正确传参，避免类型错误。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)


