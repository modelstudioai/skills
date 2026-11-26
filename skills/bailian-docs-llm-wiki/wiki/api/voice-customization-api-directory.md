# voice customization api directory

本目录汇总百炼平台支持的音色定制（Voice Customization）相关 API，涵盖音色复刻（Voice Cloning）与音色设计（Voice Design）两大能力。所有接口均通过统一的 `/api/v1/services/audio/tts/customization` 端点提供，采用 `model=voice-enrollment` 标识音色定制任务。开发者需使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）并配置对应地域的 API Key。

## 支持的模型/功能

当前支持两类音色定制方式：

- **音色复刻**：基于参考音频生成高度还原的个性化音色，适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 系列模型。具体支持型号包括 `qwen-audio-3.1-tts-plus`、`qwen-audio-3.0-realtime-flash`、`cosyvoice-v3.5-plus` 等（详见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 中“点击查看各模型支持的语言”章节）。  
- **音色设计**：通过文本描述（`voice_prompt`）和预览文本（`preview_text`）生成全新音色，仅支持 Qwen-Audio-TTS 和 CosyVoice 模型（如 `cosyvoice-v3.5-plus`），不依赖参考音频。该能力在 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中详细说明。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已失效或迁移；其中 MiniMax 接口明确标注为“旧版”，且 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 明确指出其说明已移至外部链接，**不在本平台当前维护范围内**。实际开发请以 Qwen-Audio 和 CosyVoice 系列为唯一支持对象。

## 关键参数

所有音色定制请求共用以下核心参数结构（`input` 对象内）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | 是 | 操作类型：`create_voice`、`list_voice`、`query_voice`、`update_voice`、`delete_voice`。音色设计仅支持前四种（无 `update_voice`）。 |
| `target_model` | string | 是（创建时） | 目标语音合成模型 ID，必须与后续 TTS 调用时一致。例如 `cosyvoice-v3.5-plus`。 |
| `prefix` | string | 是（创建时） | 音色名称前缀（≤10 字母/数字），生成格式为 `{target_model}-{prefix}-{id}`（复刻）或 `{target_model}-vd-{prefix}-{id}`（设计）。 |
| `audio` / `url` | string | 复刻创建/更新时必选 | 参考音频源：公网 URL 或 `data:audio/wav;base64,...` Base64 Data URI。`url` 参数兼容但将废弃，推荐用 `audio`。 |
| `voice_prompt` | string | 设计创建时必选 | 声音描述文本（中/英文，≤500 字符），如 `"沉稳的中年男性，音色低沉浑厚"`。 |
| `preview_text` | string | 设计创建时必选 | 用于生成预览音频的文本（中/英文，15–200 字符）。 |
| `language_hints` | array[string] | 否 | 语种提示（如 `["zh"]`），长度必须为 1。复刻与设计均支持，但设计要求其与 `preview_text` 语种一致。 |
| `max_prompt_audio_length` | float | 否（复刻） | 参考音频最大处理时长（秒），范围 [3.0, 30.0]，默认 10.0。 |
| `enable_preprocess` | boolean | 否（复刻） | 是否开启降噪/增强等预处理，默认 `false`。 |
| `enable_volume_normalization` | string / boolean | 否（复刻/设计） | 音量归一化开关（`"true"`/`"false"` 或 `true`/`false`），默认 `"false"`（HTTP）或 `false`（SDK）。 |

## 使用方式

### 1. 统一端点与鉴权
- **接口地址**：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
  （`{WorkspaceId}` 从控制台获取；`{region}` 如 `cn-beijing` 或 `ap-southeast-1`）  
- **请求头**：`Authorization: Bearer <your_api_key>` + `Content-Type: application/json`  
- **API Key**：必须与业务空间所在地域匹配（北京与新加坡 Key 不互通）。

### 2. SDK 快速接入
- **Python SDK**：使用 `dashscope.Client(workspace="...", region="...")` 初始化，调用 `client.audio.voices.create()` 等方法。[Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md) 提供完整参数映射与示例。
- **Java SDK**：设置 `Constants.baseHttpApiUrl` 后，使用 `VoiceEnrollmentService` 类。[Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md) 包含 Builder 模式构建 `VoiceEnrollmentParam` 的细节。

### 3. 音色设计特有流程
音色设计创建后，响应体 `output.preview_audio.data` 直接返回 Base64 编码的预览音频（如 WAV），无需额外查询。此能力在 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中定义。

## 限制和注意事项

- **地域隔离**：北京与新加坡地域的 Workspace ID、API Key、Endpoint 均独立，不可混用。
- **配额与计费**：音色创建免费，但模型调用（TTS 合成）按目标模型计费；具体配额见用户指南（文档 3 中提及的 `vc07_quota_h2` 链接）。  
- **音色状态**：复刻音色创建后需审核，状态为 `DEPLOYING`（处理中）、`OK`（可用）或 `UNDEPLOYED`（失败）。设计音色无审核流程，创建即 `OK`。  
- **参数兼容性**：`url` 参数在 HTTP API 中仍可用，但文档 3 明确提示“将逐步废弃”，**强烈建议新项目统一使用 `audio` 字段**。  
- **语言支持差异**：CosyVoice-v3-plus 仅支持 7 种语言，而 v3.5 系列及 Qwen-Audio 全系列支持 16 种（含阿拉伯语、菲律宾语等），选型时需核对 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 中的详细列表。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)


