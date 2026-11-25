# voice customization api directory

本目录汇总百炼平台支持的语音音色定制能力，涵盖音色复刻（Voice Cloning）与音色设计（Voice Design）两类核心 API。所有接口均通过统一的 `/api/v1/services/audio/tts/customization` 端点提供，支持 HTTP、Python SDK 和 Java SDK 三种调用方式，适用于 Qwen-Audio 和 CosyVoice 系列模型。

## 支持的模型/功能

当前支持两大类音色定制能力：

- **音色复刻（Voice Cloning）**：基于用户提供的参考音频（WAV/MP3 等），提取并复刻特定人声特征。支持模型包括：
  - `qwen-audio-3.x-tts-plus/flash`（TTS 合成）
  - `qwen-audio-3.x-realtime-plus/flash`（实时语音对话）
  - `cosyvoice-v3/v3.5-plus/flash`
  
  > **注意**：文档 1 中列出的 [Qwen-Omni/Livetranslate](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning) 和 [MiniMax](https://help.aliyun.com/zh/model-studio/mini-clone-api) 均为外部链接，**不属于百炼平台原生 Voice Customization API 体系**；其接入方式、鉴权机制与配额管理独立，不适用本文档所述统一流程。请以 [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md) 为准。

- **音色设计（Voice Design）**：基于文本描述（如“沉稳的中年男性，音色低沉浑厚”）和预览文本，由模型生成全新音色，无需参考音频。仅支持 `cosyvoice-v3.5-plus` 等 CosyVoice 系列模型（详见 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)）。

两类能力共用同一 API 接口与资源管理逻辑（`model=voice-enrollment`），但请求体结构与必选参数不同，需严格区分使用场景。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 来源 |
|------|------|------|------|------|
| `model` | string | 是 | 固定为 `"voice-enrollment"` | [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) |
| `input.action` | string | 是 | 操作类型：`create_voice` / `list_voice` / `query_voice` / `update_voice` / `delete_voice` | 同上 |
| `input.target_model` | string | 创建时必填 | 目标驱动模型，如 `qwen-audio-3.1-tts-plus` 或 `cosyvoice-v3.5-plus`；**必须与后续 TTS 调用时的 `model` 一致** | 同上 |
| `input.prefix` | string | 创建时必填 | 音色名称前缀（≤10 字母/数字），生成格式为 `{target_model}-{prefix}-{uuid}` | 同上 |
| `input.audio` 或 `input.url` | string | 创建/更新时必填（二选一） | 参考音频：公网 URL 或 `data:audio/wav;base64,...` 格式 Data URI；`url` 已标记为兼容旧参数，**推荐优先使用 `audio`** | 同上 |
| `input.voice_prompt` | string | 音色设计创建时必填 | 声音描述文本（中/英文，≤500 字符） | [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) |
| `input.preview_text` | string | 音色设计创建时必填 | 用于生成预览音频的文本（15–200 字符，中/英文） | 同上 |
| `input.language_hints` | array[string] | 可选 | 语种提示（如 `["zh"]`），长度必须为 1；仅影响特征提取，不强制约束输出语种 | 同上及 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md) |

> **注意**：`enable_volume_normalization` 在 HTTP API 文档中要求传字符串 `"true"`/`"false"`，但在 Python SDK 中为布尔值 `True`/`False`，Java SDK 中则为字符串（见 `VoiceEnrollmentParam`）。开发者需按所选 SDK 规范传参，避免因类型不匹配导致静默失败。

## 使用方式

### 1. 统一端点与认证
- **接口地址**（替换 `{WorkspaceId}`）：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`
- **请求头**：
  - `Authorization: Bearer <your_api_key>`
  - `Content-Type: application/json`
- **API Key**：需通过 [获取 API Key](../../../preparations/get-api-key.md) 流程获取，并确保与 Workspace 地域匹配（北京 vs 新加坡 Key 不互通）。

### 2. 多语言 SDK 封装
- **Python SDK**：使用 `dashscope.Client(audio.voices)` 操作，方法名简洁（`create`, `list`, `get`, `update`, `delete`），参数与 HTTP 语义对齐，推荐新项目首选。详见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。
- **Java SDK**：通过 `VoiceEnrollmentService` 类操作，需手动设置 `Constants.baseHttpApiUrl` 并使用 `VoiceEnrollmentParam.builder()` 构建扩展参数，适合 Java 生态集成。
- **HTTP 直连**：适用于所有语言，需自行构造 JSON 请求体与签名，灵活性最高，调试成本略高。

### 3. 典型流程示例（音色复刻）
```bash
# 创建音色（使用 Base64 Data URI）
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voice-enrollment",
    "input": {
      "action": "create_voice",
      "target_model": "qwen-audio-3.1-tts-plus",
      "prefix": "myvoice",
      "audio": "data:audio/wav;base64,..." 
    }
  }'
```

## 限制和注意事项

- **地域隔离**：北京与新加坡 Workspace 的 API Key、Endpoint、配额完全独立，不可混用。
- **配额与计费**：
  - 音色创建本身免费，但后续调用 TTS/Realtime 模型时按目标模型计费；
  - 音色数量受业务空间配额限制（详情见 [配额说明](../../../../model-user-guide/model-experience/speech-and-audio/speech-synthesis/voice-customization/voice-cloning-user-guide.md#vc07_quota_h2)）；
  - Qwen-Audio-Realtime 复刻音色创建免费，但实时对话调用按 token 计费。
- **音色状态**：新建音色初始状态为 `DEPLOYING`（审核中），成功后变为 `OK`；若为 `UNDEPLOYED` 则不可用，需检查参考音频质量或重试。
- **音频要求**：
  - 时长：建议 5–20 秒纯净人声（无背景音乐/噪音）；
  - 格式：WAV（PCM 16-bit, 16/24/48kHz）、MP3；
  - `max_prompt_audio_length` 默认 10.0 秒，可设为 3.0–30.0 秒范围内的浮点数。
- **命名冲突**：`prefix` 仅作前缀，完整音色 ID 由系统追加唯一标识，故相同 `prefix` 可创建多个音色，但需通过 `voice_id` 精确管理。
- **旧参数弃用**：`url` 字段在 HTTP API 中已标记为“逐步废弃”，请迁移至 `audio`；SDK 中仍保留兼容，但新代码应遵循文档推荐写法。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)


