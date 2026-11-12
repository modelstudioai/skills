# voice customization api directory

本目录汇总百炼平台支持的音色定制（voice customization）能力，聚焦于音色复刻（voice cloning / enrollment）类 API。当前核心能力由 Qwen-Audio 和 CosyVoice 系列模型提供，支持通过参考音频或文本描述创建、管理及使用个性化音色。所有操作均需通过 `voice-enrollment` 模型调用统一的 HTTP 接口或对应 SDK。

## 支持的模型/功能

- **核心模型**：`voice-enrollment`（固定 model 名），用于驱动 Qwen-Audio-TTS、Qwen-Audio-Realtime 及 CosyVoice 系列模型的音色复刻能力。
- **目标模型（target_model）**：必须在创建音色时明确指定，且后续语音合成调用必须严格匹配。支持的型号包括：
  - Qwen-Audio-TTS：`qwen-audio-3.1-tts-plus`、`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`
  - Qwen-Audio-Realtime：`qwen-audio-3.1-realtime-plus`、`qwen-audio-3.1-realtime-flash`、`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash`
  - CosyVoice：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-flash`、`cosyvoice-v3-plus`
- **功能覆盖**：创建（create）、查询列表（list）、查询详情（get/query）、更新（update）、删除（delete）音色全生命周期管理。
- **注意**：文档 1 中列出的 [Qwen-Omni/Livetranslate](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning) 和 [MiniMax](https://help.aliyun.com/zh/model-studio/mini-clone-api) 链接指向外部文档，其接口与本目录所述 `voice-enrollment` 统一 API 不兼容，属于独立服务；实际开发中应以 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 文档为唯一入口。

## 关键参数

- **`target_model`**（必填）：音色绑定的目标语音合成模型，决定后续可使用的 TTS 或 Realtime 接口。
- **`prefix`**（必填）：音色名称前缀（仅数字/字母，≤10 字符），生成 ID 格式为 `{target_model}-{prefix}-{uuid}`（HTTP API）或 `{target_model}-{prefix}-{唯一标识}`（Java SDK）。
- **`audio` / `url`**（创建/更新时必填）：参考音频源。支持公网 URL 或 Base64 Data URI（如 `data:audio/wav;base64,...`）。> **注意**：[Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 明确说明 `url` 参数将逐步废弃，**必须优先使用 `audio` 字段**。
- **`language_hints`**（可选）：数组，长度必须为 1，用于提示参考音频语种（如 `["zh"]`, `["en"]`），影响音色语言特征提取。各模型支持语种详见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)。
- **`max_prompt_audio_length`**（可选）：参考音频最大有效时长（秒），范围 `[3.0, 30.0]`，默认 `10.0`。
- **`enable_preprocess`**（可选）：布尔值，控制是否开启降噪/增强等预处理，默认 `false`；嘈杂环境建议设为 `true`。
- **`enable_volume_normalization`**（可选）：字符串 `"true"`/`"false"`（Java/HTTP）或布尔值（Python SDK），控制音量归一化，默认 `"false"`/`False`。

## 使用方式

- **HTTP API**：统一 POST 到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/audio/tts/customization`，`region` 如 `cn-beijing` 或 `ap-southeast-1`，`{WorkspaceId}` 需替换为真实业务空间 ID。请求体结构见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)。
- **SDK**：
  - **Java**：使用 `VoiceEnrollmentService` 类（包路径 `com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService`），需全局设置 `Constants.baseHttpApiUrl`。详细方法签名与示例见 [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)。
  - **Python**：使用 `client.audio.voices` 资源（`dashscope.Client` 构造时传入 `workspace` 和 `region`）。详细方法签名与示例见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。
- **地域与鉴权**：华北2（北京）和新加坡地域需使用对应 Workspace ID 和 API Key；请求头必须包含 `Authorization: Bearer <your_api_key>` 和 `Content-Type: application/json`。

## 限制和注意事项

- **音色状态**：创建后音色处于 `DEPLOYING` 状态，审核通过后变为 `OK` 方可使用；`UNDEPLOYED` 表示审核失败，不可用。状态说明详见 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。
- **配额与计费**：Qwen-Audio-Realtime 复刻免费，但模型调用按目标模型计费；其他模型复刻按次计费。具体配额与费用见官方用户指南。
- **音频要求**：参考音频需清晰、无严重失真或背景噪音；推荐时长 10–30 秒；格式支持 WAV/MP3/PCM。详细要求见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)。
- **命名冲突**：`prefix` 仅用于生成 ID 前缀，不保证全局唯一；同一 `target_model` + `prefix` 组合可能产生多个音色，需通过完整 `voice_id` 区分。
- **地域一致性**：Workspace ID、API Key、SDK 地域配置（`region` 或 `Constants.baseHttpApiUrl`）三者必须严格匹配同一地域（如北京或新加坡），否则调用失败。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)


