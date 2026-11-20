# voice customization api directory

本目录汇总百炼平台支持的语音定制化核心 API，涵盖音色复刻（voice cloning）与音色设计（voice design）两类能力。所有接口均基于 `voice-enrollment` 模型统一接入，支持 Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 系列模型。开发者可通过 HTTP API 或官方 SDK（Python/Java）完成音色全生命周期管理（创建、查询、更新、删除）。

## 支持的模型/功能

当前支持两类语音定制化能力：

- **音色复刻**：基于参考音频（3–30 秒）克隆目标说话人音色，适用于已有高质量录音样本的场景。  
  支持模型包括：  
  `qwen-audio-3.1-tts-plus`、`qwen-audio-3.1-tts-flash`、`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`、  
  `qwen-audio-3.1-realtime-plus`、`qwen-audio-3.1-realtime-flash`、`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-realtime-flash`、  
  `cosyvoice-v3-plus`、`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-flash`。  
  详见 [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)。

- **音色设计**：通过文本描述（如“沉稳的中年男性，音色低沉浑厚”）生成全新音色，无需原始音频。  
  同样支持上述 Qwen-Audio-TTS 与 CosyVoice 模型，但音色 ID 命名格式为 `{target_model}-vd-{prefix}-{uuid}`，且返回预览音频（Base64 编码）。  
  该能力文档见 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

> **注意**：文档 2 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已失效或迁移至外部文档；其接口不归属本 `voice-enrollment` 统一路径，且无对应 SDK 封装，**不推荐新项目接入**。请以 [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md) 和 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 适用场景 |
|------|------|------|------|----------|
| `target_model` | string | 是 | 目标语音合成/实时对话模型 ID，必须与后续 TTS 调用时一致，否则失败。 | 所有操作（create/list/query/update/delete） |
| `prefix` | string | 是（create）<br>否（list） | 音色名称前缀（仅数字+字母，≤10 字符）；列表查询时可选作筛选条件。生成名格式：<br>- 复刻：`{target_model}-{prefix}-{uuid}`<br>- 设计：`{target_model}-vd-{prefix}-{uuid}` | create, list |
| `audio` / `url` | string | 是（create/update） | 参考音频源：公网 URL 或 `data:audio/wav;base64,...` Data URI。<br>**HTTP API 优先使用 `audio` 字段；`url` 已标记为兼容旧参数，将逐步废弃**。 | 音色复刻（create/update） |
| `voice_prompt` | string | 是（design） | 声音描述文本（中/英文，≤500 字符），用于音色设计。 | 音色设计（create） |
| `preview_text` | string | 是（design） | 用于生成预览音频的文本（15–200 字符，中/英文）。 | 音色设计（create） |
| `language_hints` | string[] | 否 | 语种提示（如 `["zh"]`），长度必须为 1；若与实际音频/文本不符则被忽略。默认 `["zh"]`。 | 复刻 & 设计（create） |
| `max_prompt_audio_length` | float | 否 | 复刻音频最大有效时长（秒），范围 `[3.0, 30.0]`，默认 `10.0`。 | 音色复刻（create） |
| `enable_preprocess` | bool (SDK) / boolean (HTTP) | 否 | 是否开启降噪/增强/音量规整预处理；嘈杂环境建议开启，安静环境建议关闭。默认 `false`。 | 音色复刻（create） |
| `enable_volume_normalization` | string (HTTP) / bool (SDK) | 否 | 音量归一化开关：HTTP 传 `"true"`/`"false"`；SDK 传 `boolean`。默认 `"false"`（HTTP）或 `false`（SDK）。 | 音色复刻（create） |

## 使用方式

### 接口地址（统一域名）
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
  > **务必替换 `{WorkspaceId}` 为控制台获取的真实业务空间 ID**，并使用对应地域的 API Key。[迁移指南](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain) 强烈建议使用专属域名替代旧版 `dashscope.aliyuncs.com`。

### SDK 初始化（示例：Python）
```python
import dashscope
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",  # 替换为真实 ID
    region="cn-beijing"          # 或 "ap-southeast-1"
)
# 音色复刻操作
voices = client.audio.voices
# 音色设计需调用 tts 接口并指定 voice_id，不通过 voices 子模块
```

### 核心操作映射
| 功能 | HTTP `input.action` | Python SDK 方法 | Java SDK 方法 |
|------|---------------------|------------------|----------------|
| 创建音色 | `create_voice` | `client.audio.voices.create(...)` | `VoiceEnrollmentService.createVoice(...)` |
| 查询列表 | `list_voice` | `client.audio.voices.list(...)` | `VoiceEnrollmentService.listVoice(...)` |
| 查询详情 | `query_voice` | `client.audio.voices.get(...)` | `VoiceEnrollmentService.queryVoice(...)` |
| 更新音色 | `update_voice` | `client.audio.voices.update(...)` | `VoiceEnrollmentService.updateVoice(...)` |
| 删除音色 | `delete_voice` | `client.audio.voices.delete(...)` | `VoiceEnrollmentService.deleteVoice(...)` |

> **注意**：音色设计（`voice_prompt` + `preview_text`）**仅支持 HTTP API**，Python/Java SDK 当前未封装该模式。详见 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

## 限制和注意事项

- **配额与计费**：Qwen-Audio-Realtime 复刻创建免费，但模型调用按目标模型计费；Qwen-Audio-TTS/CosyVoice 复刻与设计均按次计费。具体配额见 [配额说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。
- **音频要求**：复刻参考音频需为清晰人声（无严重混响/失真），采样率建议 16–48 kHz，格式支持 WAV/MP3/OGG。设计无音频输入要求。
- **状态流转**：新建音色初始状态为 `DEPLOYING`（审核中），成功后变为 `OK`；失败为 `UNDEPLOYED`。仅 `OK` 状态音色可用于 TTS 合成。
- **地域隔离**：API Key、Workspace ID、接口域名三者必须同地域（北京/新加坡），跨地域调用将失败。
- **参数兼容性**：HTTP API 中 `url` 字段已标记为兼容旧参数，**新集成请统一使用 `audio` 字段**；Java SDK 的 `enable_volume_normalization` 接收 `boolean`，而 HTTP API 要求字符串 `"true"`/`"false"`，需注意类型差异。

## 来源文档

- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)


