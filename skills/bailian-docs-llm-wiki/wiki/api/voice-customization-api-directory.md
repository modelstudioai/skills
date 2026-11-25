# voice customization api directory

本目录汇总百炼平台支持的语音音色定制能力，涵盖音色复刻（Voice Cloning）与音色设计（Voice Design）两类核心 API。所有能力均通过 `voice-enrollment` 模型统一接入，支持 Qwen-Audio 和 CosyVoice 系列语音合成/实时语音模型。开发者可通过 HTTP、Python SDK 或 Java SDK 调用，需使用业务空间专属域名并配置对应地域的 API Key。

## 支持的模型/功能

当前支持两大类音色定制方式：

- **音色复刻（Voice Cloning）**：基于参考音频（URL 或 Base64 Data URI）提取并复刻原始说话人音色。适用于 Qwen-Audio-TTS（如 `qwen-audio-3.1-tts-plus`）、Qwen-Audio-Realtime（如 `qwen-audio-3.1-realtime-flash`）及 CosyVoice（如 `cosyvoice-v3.5-plus`）系列模型。具体支持型号详见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)。
- **音色设计（Voice Design）**：基于文本描述（如“沉稳的中年男性，音色低沉浑厚”）生成全新音色，并返回预览音频。仅支持 Qwen-Audio-TTS/CosyVoice，不支持 Realtime 模型。详细参数见 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 链接已失效且未在其余 SDK 或 HTTP 文档中被提及，该能力当前**不纳入本 API 目录支持范围**；MiniMax 接口为独立第三方服务，其文档 [MiniMax HTTP API](https://help.aliyun.com/zh/model-studio/mini-clone-api) 仅作外部引用，**不提供统一 SDK 封装或业务空间域名支持**。

## 关键参数

所有音色操作（创建、查询、更新、删除）均围绕以下核心参数展开：

- `target_model`（必填，创建时）：指定驱动音色的目标模型 ID，必须与后续 TTS/Realtime 接口调用时使用的模型完全一致，否则合成失败。例如 `"qwen-audio-3.1-tts-plus"` 或 `"cosyvoice-v3.5-flash"`。
- `prefix`（必填，创建时；可选，查询列表时）：音色名称前缀，仅允许数字和英文字母，长度 ≤10。生成的完整音色 ID 格式为 `{target_model}-{prefix}-{唯一标识}`（复刻）或 `{target_model}-vd-{prefix}-{唯一标识}`（设计）。
- `audio` / `url`（创建/更新时必填）：参考音频源。支持公网可访问 URL（如 `https://example.com/voice.wav`）或 Base64 Data URI（如 `data:audio/wav;base64,...`）。`url` 参数已标记为兼容旧版，**推荐优先使用 `audio` 字段**（见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)）。
- `language_hints`（可选）：字符串数组，长度必须为 1，用于提示参考音频语种（如 `["zh"]`, `["en"]`），提升特征提取准确性。若与实际语种不符，系统将自动忽略并检测。各模型支持语种详见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)。
- `max_prompt_audio_length`（可选）：参考音频最大有效时长（秒），取值范围 `[3.0, 30.0]`，默认 `10.0`。
- `enable_preprocess`（可选）：布尔值，控制是否开启降噪、增强等音频预处理，默认 `false`。嘈杂环境建议设为 `true`。
- `enable_volume_normalization`（可选）：字符串 `"true"` 或 `"false"`，控制是否对参考音频进行音量归一化，默认 `"false"`。

## 使用方式

### 接口地址与鉴权
- **域名**：必须使用业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/audio/tts/customization`。支持地域包括 `cn-beijing`（华北2）和 `ap-southeast-1`（新加坡）。请将 `{WorkspaceId}` 替换为控制台获取的真实 ID。
- **请求头**：`Authorization: Bearer <your_api_key>`（使用对应地域的 API Key）和 `Content-Type: application/json`。
- **SDK 初始化**：
  - Python：通过 `dashscope.Client(workspace="{WorkspaceId}", region="cn-beijing")` 构造。
  - Java：通过 `Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"` 全局设置。

### 核心操作
- **创建音色**：HTTP POST `/customization`，`input.action="create_voice"`；SDK 调用 `client.audio.voices.create()`（Python）或 `VoiceEnrollmentService.createVoice()`（Java）。
- **查询列表**：HTTP POST `/customization`，`input.action="list_voice"`；SDK 调用 `client.audio.voices.list()` 或 `VoiceEnrollmentService.listVoice()`。
- **查询详情**：HTTP POST `/customization`，`input.action="query_voice"`；SDK 调用 `client.audio.voices.get()` 或 `VoiceEnrollmentService.queryVoice()`。
- **更新音色**：HTTP POST `/customization`，`input.action="update_voice"`；SDK 调用 `client.audio.voices.update()` 或 `VoiceEnrollmentService.updateVoice()`。
- **删除音色**：HTTP POST `/customization`，`input.action="delete_voice"`；SDK 调用 `client.audio.voices.delete()` 或 `VoiceEnrollmentService.deleteVoice()`。

## 限制和注意事项

- **配额与费用**：Qwen-Audio-Realtime 复刻创建免费，但模型调用按目标模型计费；Qwen-Audio-TTS/CosyVoice 复刻与设计均计入配额。具体限额见 [声音复刻用户指南](../../../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md#vc07_quota_h2)。
- **音频要求**：参考音频需清晰、无严重失真或混响。复刻推荐时长 10–30 秒；设计不依赖音频，仅需文本描述。
- **状态管理**：新创建音色初始状态为 `DEPLOYING`（审核中），成功后变为 `OK`（可用），失败则为 `UNDEPLOYED`（不可用）。查询详情可获知当前 `status`。
- **地域隔离**：API Key、Workspace ID、域名三者严格绑定地域。跨地域调用将失败。
- **参数一致性**：`target_model` 必须在创建音色与后续 TTS/Realtime 合成时保持完全一致，否则合成请求将被拒绝。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)


