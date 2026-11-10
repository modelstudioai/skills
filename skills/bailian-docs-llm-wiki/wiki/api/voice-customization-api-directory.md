# voice customization api directory

本目录汇总百炼平台支持的音色定制化能力 API，涵盖音色复刻（voice cloning）与音色设计（voice design）两类核心功能。所有接口均通过统一的 `/api/v1/services/audio/tts/customization` 路径提供，由 `model=voice-enrollment` 标识，并按 `target_model` 和操作类型（`create_voice`/`list_voice` 等）区分行为。开发者需先[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并配置地域专属 Workspace ID。

## 支持的模型与功能

当前支持两大类音色定制方式：

- **音色复刻**：基于参考音频生成高度相似的个性化音色，适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime 及 CosyVoice 系列模型。具体支持型号包括：
  - `qwen-audio-3.0/3.1-tts-plus/flash`
  - `qwen-audio-3.0/3.1-realtime-plus/flash`
  - `cosyvoice-v3/v3.5-plus/flash`
  
  详细支持列表见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)。

- **音色设计**：通过文本描述（`voice_prompt`）和预览文本（`preview_text`）生成全新音色，目前仅支持 CosyVoice 和 Qwen-Audio-TTS 模型（如 `cosyvoice-v3.5-plus`），不依赖参考音频。该能力在 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中完整定义。

> **注意**：文档 1 中列出的 `Qwen-Omni/Livetranslate` 和 `MiniMax` 链接已过时或迁移。`Qwen-Omni/Livetranslate` 的音色复刻能力已整合至 Qwen-Audio-Realtime 流程；`MiniMax` 接口已下线，其历史说明已归档至 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md) 底部备注，不再作为主推路径。

## 关键参数

所有操作共用以下核心参数结构（`input` 对象内）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | 是 | 操作类型：`create_voice`、`list_voice`、`query_voice`、`update_voice`、`delete_voice` |
| `target_model` | string | 创建/更新时必填 | 目标语音模型 ID，**必须与后续合成调用时一致**，否则失败 |
| `prefix` | string | 创建时必填 | 音色名称前缀（字母+数字，≤10 字符）；查询时可选作筛选条件 |
| `voice_id` | string | 查询/更新/删除时必填 | 音色唯一标识符 |

**创建专用参数**：
- **复刻模式**：`audio`（Base64 Data URI 或公网 URL）为必填；`url` 为兼容旧参数，**已标记为逐步废弃**（见 [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)）。
- **设计模式**：`voice_prompt`（≤500 字符）、`preview_text`（15–200 字符）为必填；`language_hints` 仅影响发音倾向，且**必须与 `preview_text` 语种一致**。
- **通用可选参数**：`language_hints`（单元素数组，默认 `["zh"]`）、`max_prompt_audio_length`（3.0–30.0 秒）、`enable_preprocess`（bool）、`enable_volume_normalization`（string `"true"`/`"false"`，注意 Java SDK 传字符串，Python SDK 传 bool）。

## 使用方式

### 1. 统一接入点
所有请求均使用 POST 方法，地址格式为：  
`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
其中 `{WorkspaceId}` 需替换为控制台业务空间详情页中的真实 ID，`{region}` 为 `cn-beijing` 或 `ap-southeast-1`。

### 2. 鉴权与头信息
- `Authorization: Bearer <your_api_key>`（API Key 来自对应地域）
- `Content-Type: application/json`

### 3. SDK 快速集成
- **Python**：使用 `dashscope.Client(audio.voices)` 操作，详见 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。
- **Java**：使用 `VoiceEnrollmentService` 类，注意需全局设置 `Constants.baseHttpApiUrl`，详见 [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)。

### 4. 地域与域名迁移
华北2（北京）和新加坡地域**强烈建议**使用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等），以获得更高性能与稳定性。旧域名（`dashscope.aliyuncs.com`）仍可用，但属过渡期。

## 限制和注意事项

- **配额与计费**：音色创建免费，但模型调用（TTS/Realtime）按目标模型单独计费；具体配额限制见 [声音复刻用户指南](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。
- **音频要求**：复刻模式要求参考音频清晰、无强背景噪音；推荐时长 10–30 秒；格式支持 WAV/MP3/FLAC（详见 [声音复刻用户指南](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc02_audio_h2)）。
- **状态流转**：新创建音色初始状态为 `DEPLOYING`（审核中），仅当 `status == "OK"` 时方可用于合成；`UNDEPLOYED` 表示审核失败，不可用。
- **跨模型约束**：`target_model` 在创建时指定后不可更改，且后续 TTS/Realtime 请求必须使用完全相同的模型 ID，否则报错。
- **语言提示一致性**：`language_hints` 若设置，其值必须与实际音频（复刻）或 `preview_text`（设计）语种严格匹配，否则被忽略。
- **SDK 参数差异**：`enable_volume_normalization` 在 HTTP API 和 Java SDK 中为字符串（`"true"`/`"false"`），而在 Python SDK 中为布尔值（`True`/`False`），调用时需注意类型匹配。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)


