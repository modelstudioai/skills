# voice customization api directory

本目录汇总百炼平台支持的语音音色定制能力，涵盖音色复刻（voice cloning）与音色设计（voice design）两类核心 API。所有接口均通过统一的 `/api/v1/services/audio/tts/customization` 端点提供，采用 `model: "voice-enrollment"` 标识调用类型，支持 Qwen-Audio 和 CosyVoice 系列模型。开发者需先[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并配置对应地域的 Workspace ID。

## 支持的模型/功能

当前支持两类音色定制方式：

- **音色复刻（Voice Cloning）**：基于用户提供的参考音频（WAV/MP3，时长 3–30 秒），提取并复刻特定人声特征。适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime 及 CosyVoice 全系列模型（如 `qwen-audio-3.1-tts-plus`、`cosyvoice-v3.5-flash` 等）。详细支持列表见 [Qwen-Audio/Cosyvoice](raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)。
- **音色设计（Voice Design）**：基于文本描述（如“沉稳的中年男性，音色低沉浑厚”）和预览文本自动生成全新音色，无需原始音频。仅支持 CosyVoice 及部分 Qwen-Audio-TTS 模型（如 `cosyvoice-v3.5-plus`），不适用于 Realtime 模型。该能力在 [音色设计 API 参考](raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中完整定义。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已过时。`Qwen-Omni` 不支持音色复刻；`MiniMax` 接口已下线，其功能由 Qwen-Audio/CosyVoice 统一承接。请以 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 为准。

## 关键参数

所有操作均通过 `input` 对象传递参数，核心字段如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | 是 | 操作类型：`create_voice`、`list_voice`、`query_voice`、`update_voice`（仅复刻）、`delete_voice` |
| `target_model` | string | 是（创建/更新时） | 目标驱动模型，必须与后续 TTS/Realtime 调用一致。例如 `cosyvoice-v3.5-plus` |
| `prefix` | string | 是（创建时） | 音色名称前缀（≤10 字母/数字），生成格式为 `{target_model}-{prefix}-{id}`（复刻）或 `{target_model}-vd-{prefix}-{id}`（设计） |
| `audio` / `url` | string | 复刻创建/更新时必填 | 参考音频源：公网 URL 或 `data:audio/wav;base64,...` Base64 Data URI（推荐 `audio`，`url` 已标记为兼容旧参数） |
| `voice_prompt` | string | 设计创建时必填 | 声音描述文本（≤500 字符，中/英文） |
| `preview_text` | string | 设计创建时必填 | 用于生成预览音频的文本（15–200 字符，中/英文） |
| `language_hints` | string[] | 可选 | 语种提示（长度必须为 1），如 `["zh"]`、`["en"]`。复刻与设计均支持，但设计要求与 `preview_text` 语种一致 |
| `max_prompt_audio_length` | float | 复刻可选 | 参考音频最大处理时长（秒），范围 [3.0, 30.0]，默认 10.0 |
| `enable_preprocess` | boolean | 复刻可选 | 是否开启降噪/增强等预处理，默认 `false` |
| `enable_volume_normalization` | string (复刻) / boolean (设计 SDK) | 复刻可选 | 音量归一化开关，取值 `"true"`/`"false"`（HTTP）或 `True`/`False`（Python SDK） |

## 使用方式

### 1. 基础配置
- **API Key**：从百炼控制台获取，并通过环境变量 `DASHSCOPE_API_KEY` 或 SDK 初始化传入。
- **Endpoint**：必须使用业务空间专属域名（**强烈建议迁移**）：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`
  > `{WorkspaceId}` 在控制台「业务空间详情」页查看。不同地域的 API Key 不互通。

### 2. SDK 快速接入
- **Python**：使用 `dashscope.Client(workspace="xxx", region="cn-beijing").audio.voices` 资源，方法名与 HTTP action 一致（`create`, `list`, `get`, `update`, `delete`）。详见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。
- **Java**：初始化 `VoiceEnrollmentService` 并设置 `Constants.baseHttpApiUrl`，调用 `createVoice()`, `listVoice()` 等方法。详见 [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)。

### 3. HTTP 示例（创建音色）
```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voice-enrollment",
    "input": {
      "action": "create_voice",
      "target_model": "cosyvoice-v3.5-plus",
      "prefix": "mydesign",
      "voice_prompt": "温柔知性的女声",
      "preview_text": "今天天气真好"
    }
  }'
```

## 限制和注意事项

- **地域隔离**：华北2（北京）与新加坡地域的 Workspace ID 和 API Key 完全独立，不可混用。
- **配额与计费**：音色创建本身免费，但受[配额限制](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)；后续使用音色进行 TTS/Realtime 合成时按目标模型计费。
- **音频要求**：复刻参考音频需清晰、安静、无明显剪辑痕迹；推荐采样率 16kHz/24kHz，格式 WAV/MP3，时长 10–20 秒效果最佳。
- **状态流转**：新创建音色初始状态为 `DEPLOYING`，审核通过后变为 `OK` 才可使用；`UNDEPLOYED` 表示审核失败，需检查音频质量或描述合规性。
- **参数兼容性**：`url` 参数在复刻 API 中仍可用，但官方明确标注“将逐步废弃”，请优先使用 `audio` 字段。此差异已在 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 中强调。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)


