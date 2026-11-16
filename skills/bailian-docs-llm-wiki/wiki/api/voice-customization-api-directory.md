# voice customization api directory

本目录汇总百炼平台支持的音色定制能力，涵盖音色复刻（Voice Cloning）与音色设计（Voice Design）两类核心 API。所有能力均通过统一的 `voice-enrollment` 模型接口提供，支持 Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 系列模型，开发者可按需选择音频驱动或文本描述方式创建定制化音色。

## 支持的模型与功能

当前支持以下两类音色定制路径：

- **音色复刻**：基于参考音频（URL 或 Base64 Data URI）提取声学特征，生成高保真复刻音色。适用于已有目标人声样本的场景。  
  支持模型包括：  
  `qwen-audio-3.1-tts-plus`/`flash`、`qwen-audio-3.0-tts-plus`/`flash`、  
  `qwen-audio-3.1-realtime-plus`/`flash`、`qwen-audio-3.0-realtime-plus`/`flash`、  
  `cosyvoice-v3-plus`/`v3.5-plus`/`v3.5-flash`/`v3-flash`。  
  详细支持列表见 [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)。

- **音色设计**：通过自然语言描述（如“沉稳的中年男性，音色低沉浑厚”）和预览文本生成全新音色，无需原始音频。适用于创意语音合成场景。  
  功能由同一 `voice-enrollment` 接口承载，但请求体中需传入 `voice_prompt` 和 `preview_text` 字段。  
  该能力文档详见 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已过时或迁移至外部文档；当前百炼平台官方维护的音色复刻能力仅限 Qwen-Audio 与 CosyVoice 系列，MiniMax 接口已归档，参见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 中的说明。

## 关键参数

所有音色定制操作（创建/查询/更新/删除）均围绕 `voice_id` 进行管理，创建时需指定以下核心参数：

- `target_model`（必填）：目标语音合成或实时对话模型，必须与后续 TTS/Realtime 调用时一致，否则报错。
- `prefix`（必填）：音色名称前缀（仅字母数字，≤10 字符），生成格式为 `{target_model}-{prefix}-{uuid}`（复刻）或 `{target_model}-vd-{prefix}-{uuid}`（设计）。
- `language_hints`（可选）：语种提示数组（长度必须为 1），用于辅助音色建模。支持语种因模型而异，完整列表见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。
- `max_prompt_audio_length`（复刻专用，可选）：参考音频最大处理时长（秒），范围 `[3.0, 30.0]`，默认 `10.0`。
- `enable_preprocess`（复刻专用，可选）：是否开启降噪/增强/音量规整，默认 `false`。
- `enable_volume_normalization`（复刻专用，可选）：是否开启音量归一化（HTTP API 传 `"true"`/`"false"`，SDK 传 `bool` 或 `str`），默认 `"false"`。
- `voice_prompt` & `preview_text`（设计专用，必填）：声音描述文本（≤500 字符）和预览文本（15–200 字符），仅用于音色设计流程。

## 使用方式

统一通过 `POST /api/v1/services/audio/tts/customization` 接口调用，地域专属域名推荐使用：
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`

SDK 封装已覆盖主流语言：
- Python：`client.audio.voices.create()` 等方法，详见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- Java：`VoiceEnrollmentService` 类，详见 [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- HTTP：直接构造 JSON 请求体，`input.action` 指定操作类型（`create_voice`/`list_voice`/`query_voice`/`update_voice`/`delete_voice`）

所有 SDK 均要求显式配置 `workspace`（或 `Constants.baseHttpApiUrl`）与 `region`（或全局 URL），且对应地域的 API Key 不可混用。

## 限制和注意事项

- **配额与审核**：音色创建后进入 `DEPLOYING` 状态，需通过自动审核后变为 `OK` 才可使用；审核失败状态为 `UNDEPLOYED`。具体配额限制请查阅控制台或用户指南。
- **音频要求**：复刻音频需为清晰人声（无明显背景噪音）、时长 ≥3 秒，推荐 10–20 秒；支持 WAV/MP3/FLAC 等常见格式，公网可访问或 Base64 Data URI。
- **地域隔离**：北京与新加坡地域的 Workspace ID、API Key、Endpoint 完全独立，不可跨地域复用。
- **参数兼容性**：HTTP API 中 `url` 字段已标记为“逐步废弃”，请优先使用 `audio` 字段；Java SDK 的 `enable_volume_normalization` 参数类型为 `String`（`"true"`/`"false"`），而 Python SDK 为 `bool`，需注意适配。
- **费用说明**：Qwen-Audio-Realtime 复刻音色创建免费，但模型调用按实际用量计费；其他模型创建与调用均计费，详情见计费文档。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)


