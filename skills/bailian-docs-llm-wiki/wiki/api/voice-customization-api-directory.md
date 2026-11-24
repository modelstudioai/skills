# voice customization api directory

本目录汇总百炼平台支持的音色定制类 API，涵盖音色复刻（voice cloning）与音色设计（voice design）两大能力。所有接口均通过统一的 `/api/v1/services/audio/tts/customization` 路径提供，以 `model: "voice-enrollment"` 为标识，支持 Qwen-Audio 和 CosyVoice 系列模型。开发者可通过 HTTP API、Python SDK 或 Java SDK 进行集成。

## 支持的模型/功能

当前支持两类音色生成方式：

- **音色复刻**：基于参考音频（WAV/MP3）提取声纹特征，生成高保真复刻音色。适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime 及 CosyVoice 全系列模型（如 `qwen-audio-3.1-tts-plus`、`cosyvoice-v3.5-flash` 等），详见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。
- **音色设计**：通过文本描述（如“沉稳的中年男性，音色低沉浑厚”）和预览文本生成合成音色，无需原始音频。仅支持 CosyVoice 及部分 Qwen-Audio-TTS 模型（如 `cosyvoice-v3.5-plus`），不适用于 Qwen-Audio-Realtime。该能力在 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中完整定义。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已过时或迁移——`Qwen-Omni/Livetranslate` 不支持音色复刻；`MiniMax` 接口已下线，其说明已归档至 [MiniMax HTTP API](https://help.aliyun.com/zh/model-studio/mini-clone-api)，**不再属于本目录维护范围**。

## 关键参数

所有操作共用以下核心参数（HTTP API 与 SDK 均映射一致）：

- `model`: 固定为 `"voice-enrollment"`。
- `input.action`: 必填，取值为 `"create_voice"`、`"list_voice"`、`"query_voice"`、`"update_voice"` 或 `"delete_voice"`。
- `target_model`: 创建/更新时必填，指定驱动音色的目标模型（如 `"cosyvoice-v3.5-plus"`），**必须与后续 TTS/Realtime 调用时的模型完全一致**。
- `prefix`: 创建时必填（音色名前缀，≤10 字母/数字），查询列表时可选用于筛选。
- `voice_id`: 查询详情、更新或删除时必填。

**音色复刻特有参数**（仅 `create_voice`/`update_voice`）：
- `audio`（或兼容旧字段 `url`）：参考音频，支持公网 URL 或 `data:audio/wav;base64,...` 格式。
- `language_hints`: 字符串数组（长度为 1），如 `["zh"]`，用于辅助语种识别；若与实际音频不符则被忽略。
- `max_prompt_audio_length`: 浮点数（3.0–30.0），控制有效音频时长，默认 `10.0`。
- `enable_preprocess`: 布尔值，是否开启降噪/增强，默认 `false`。
- `enable_volume_normalization`: 字符串 `"true"`/`"false"`，是否音量归一化，默认 `"false"`。

**音色设计特有参数**（仅 `create_voice`，`model="voice-enrollment"`）：
- `voice_prompt`: 描述性文本（≤500 字符），中英文均可。
- `preview_text`: 合成预览文本（15–200 字符），用于生成试听音频。
- `parameters.sample_rate` / `parameters.response_format`: 控制预览音频采样率（16000/24000/48000 Hz）与格式（pcm/wav/mp3）。

## 使用方式

### 接口地址与鉴权
- **地域专属域名（推荐）**：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`
- `{WorkspaceId}` 需从百炼控制台【业务空间详情】获取；不同地域需使用对应 API Key（[获取 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。
- 请求头：`Authorization: Bearer <your_api_key>`，`Content-Type: application/json`。

### SDK 快速接入
- **Python SDK**：使用 `client.audio.voices.create()` 等方法，`workspace` 和 `region` 参数决定地域（见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)）。
- **Java SDK**：通过 `VoiceEnrollmentService` 类调用，需预先设置 `Constants.baseHttpApiUrl`（见 [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)）。

> **注意**：HTTP API 文档中 `audio` 字段已替代旧版 `url` 字段（虽仍兼容），SDK 中 `url` 参数实为 `audio` 的别名；但 Java SDK 的 `enable_volume_normalization` 参数类型为 `String`（`"true"`/`"false"`），而 Python SDK 中为 `bool`，二者行为一致但传参格式不同，请按 SDK 文档严格使用。

## 限制和注意事项

- **配额与计费**：Qwen-Audio-Realtime 复刻创建免费，但模型调用按目标模型计费；其他模型创建与调用均计入配额。具体限额见 [配额说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。
- **音频要求**：复刻参考音频需清晰、安静、无混响，时长建议 10–30 秒；设计模式无需音频。
- **音色状态**：新建音色初始为 `DEPLOYING`，审核通过后变为 `OK` 才可使用；`UNDEPLOYED` 表示审核失败。
- **跨地域隔离**：北京与新加坡的 Workspace ID、API Key、域名完全独立，不可混用。
- **模型兼容性**：`language_hints`、`max_prompt_audio_length` 等参数并非所有模型均支持（如 `cosyvoice-v3-plus` 不支持 `pt`/`th` 等语种），请以各模型支持的语言列表为准。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)


