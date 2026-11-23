# voice customization api directory

音色定制 API 提供语音克隆与合成能力，支持基于少量音频样本复刻目标音色（Sound Reengraving），以及通过文本描述生成全新音色（Voice Design）。所有接口均通过 HTTPS 调用，需携带有效 API Key 与模型标识。该能力当前仅面向已开通权限的白名单用户开放。

## 支持的模型/功能

- **音色复刻（Sound Reengraving）**：输入 30–60 秒高质量单人语音样本（无背景音、无混响），生成可调用的复刻音色 ID；支持中文、英文及中英混合语种。详见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。
- **音色设计（Voice Design）**：通过自然语言描述（如“沉稳男声，语速偏慢，带轻微磁性”）生成音色，无需原始音频；输出为可复用的音色 ID。详见 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。
- 当前仅支持 `qwen-audio-2.5-vc` 模型版本，不兼容旧版 `qwen-audio-2.0-vc` 的请求参数格式。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-audio-2.5-vc` |
| `input.audio`（复刻） | base64 或 URL | 是 | 音频数据，WAV/MP3 格式，采样率 ≥16kHz，单声道 |
| `input.text_description`（设计） | string | 是 | 音色描述文本，长度 10–100 字，须含性别、风格、语感等维度 |
| `voice_id` | string | 否 | 复用已有音色时指定；首次创建留空，由服务返回 |

> **注意**：原始文档 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 中提及支持 FLAC 格式，但实测 v2.5 接口仅接受 WAV/MP3；FLAC 将被静默转码并可能引入失真，请主动转换后再上传。

## 使用方式

1. 调用 `/v1/voice-customization/create` 创建音色（POST）  
2. 获取返回的 `voice_id`，用于后续 TTS 合成请求的 `voice` 字段  
3. 所有请求需在 Header 中携带：  
   - `Authorization: Bearer <api_key>`  
   - `Content-Type: application/json`  
详细请求示例与响应结构见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 和 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

## 限制和注意事项

- 单次复刻音频时长上限为 60 秒；超时样本将被截断，可能导致音色还原度下降  
- 每个 `voice_id` 默认有效期为 90 天，过期后需重新创建  
- 音色设计不支持实时微调参数（如 pitch、speed），如需控制需在描述中明确体现（例如“语调上扬”“语速加快”）  
- 白名单权限需通过百炼控制台「语音服务」模块单独申请，API Key 权限不自动继承  

> **注意**：[音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 文档中“支持多轮迭代优化”描述已过时；当前版本仅支持单次生成，暂无迭代接口。

## 来源文档

- [音色定制](../../raw/model-api-reference/voice-customization-api-directory.md)


