# voice customization api directory

本目录汇总了百炼平台支持的音色定制（Voice Customization）相关 API，涵盖音色复刻（Voice Cloning）与音色设计（Voice Design）两大能力。所有接口均通过统一的 `voice-enrollment` 模型服务提供，支持 Qwen-Audio 和 CosyVoice 系列模型，可通过 HTTP API 或多语言 SDK（Python/Java）调用。开发者需先配置 Workspace ID 与对应地域的 API Key，并注意模型兼容性与参数约束。

## 支持的模型/功能

当前支持两类音色定制方式：

- **音色复刻（Voice Cloning）**：基于参考音频（URL 或 Base64 Data URI）提取并复刻原始说话人音色。适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime 及 CosyVoice 全系列模型，包括：
  - `qwen-audio-3.0/3.1-tts-plus/flash`、`qwen-audio-3.0/3.1-realtime-plus/flash`
  - `cosyvoice-v3/v3.5-plus/flash`
  
  详细支持模型列表及对应语种见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。

- **音色设计（Voice Design）**：基于文本描述（`voice_prompt`）和预览文本（`preview_text`）生成全新音色，无需参考音频。仅支持 `cosyvoice-v3.5-plus` 等 CosyVoice 模型（不支持 Qwen-Audio-Realtime）。该能力在 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中完整定义。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已失效或迁移至外部文档；其当前状态与本目录中统一的 `voice-enrollment` 接口无直接集成关系，实际开发请以 [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md) 为准。

## 关键参数

所有操作均通过 `input` 对象传递核心参数，关键字段如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | 是 | 操作类型：`create_voice` / `list_voice` / `query_voice` / `update_voice` / `delete_voice` |
| `target_model` | string | 创建/查询时必填 | 目标语音模型 ID，**必须与后续 TTS/Realtime 调用时一致**，否则合成失败。例如 `cosyvoice-v3.5-plus` |
| `prefix` | string | 创建时必填，列表查询时可选 | 音色名称前缀（仅数字/字母，≤10 字符），生成格式为 `{target_model}-{prefix}-{uuid}`（复刻）或 `{target_model}-vd-{prefix}-{uuid}`（设计） |
| `audio` 或 `url` | string | 创建/更新时必填（复刻） | 参考音频地址（公网 URL）或 Base64 Data URI（如 `data:audio/wav;base64,...`）。HTTP API 中 `audio` 为推荐字段，`url` 将逐步废弃 |
| `voice_prompt` | string | 创建时必填（设计） | 声音描述文本（中/英文，≤500 字符），例如 `"沉稳的中年男性，音色低沉浑厚"` |
| `preview_text` | string | 创建时必填（设计） | 用于生成预览音频的文本（中/英文，15–200 字符） |
| `language_hints` | string[] | 可选 | 语种提示（长度必须为 1），如 `["zh"]`、`["en"]`；若与实际音频不符则被忽略。默认 `["zh"]` |
| `max_prompt_audio_length` | float | 可选（复刻） | 参考音频最大处理时长（秒），范围 `[3.0, 30.0]`，默认 `10.0` |
| `enable_preprocess` | bool / boolean | 可选（复刻） | 是否开启降噪/增强/音量规整，默认 `false`；嘈杂环境建议设为 `true` |
| `enable_volume_normalization` | string / boolean | 可选（复刻） | HTTP API 传 `"true"`/`"false"`，SDK 传 `boolean`；影响合成音量一致性，默认 `"false"` |

## 使用方式

### 接口地址与认证
- **域名**：使用业务空间专属域名（强烈推荐），格式为：  
  `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`（华北2）  
  `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`（新加坡）  
  `{WorkspaceId}` 需替换为控制台获取的真实 ID（见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)）。
- **鉴权**：请求头 `Authorization: Bearer <your_api_key>`，API Key 需与地域匹配。

### SDK 快速接入
- **Python**：使用 `dashscope.Client(audio.voices)` 操作，详见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。
- **Java**：使用 `VoiceEnrollmentService` 类，通过 `VoiceEnrollmentParam.builder()` 设置扩展参数，详见 [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)。

### 核心流程示例（HTTP）
```bash
# 创建复刻音色
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voice-enrollment",
    "input": {
      "action": "create_voice",
      "target_model": "cosyvoice-v3.5-plus",
      "prefix": "myvoice",
      "audio": "https://example.com/ref.wav",
      "language_hints": ["zh"]
    }
  }'
```

## 限制和注意事项

- **地域隔离**：华北2（北京）与新加坡地域的 Workspace ID 和 API Key **完全独立**，不可混用。
- **配额与计费**：Qwen-Audio-Realtime 复刻免费，但模型调用按目标模型计费；Qwen-Audio-TTS/CosyVoice 复刻与设计均计入配额，详情见 [声音复刻用户指南](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)。
- **音色状态**：创建后音色处于 `DEPLOYING` 状态，审核通过后变为 `OK` 才可使用；`UNDEPLOYED` 表示审核失败。
- **参数兼容性**：`language_hints`、`max_prompt_audio_length`、`enable_preprocess` 等参数**仅对明确列出的模型生效**（见各 SDK 文档），对未列模型传入将被忽略。
- **命名冲突**：同一 `target_model + prefix` 组合多次调用 `create_voice` 会生成多个不同 `voice_id` 的音色，不会覆盖；请自行管理生命周期。
- **设计 vs 复刻**：音色设计（`voice_prompt`）与音色复刻（`audio`）**不可在同一请求中混用**，二者使用场景与参数集严格分离。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)


