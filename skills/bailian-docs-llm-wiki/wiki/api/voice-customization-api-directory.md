# voice customization api directory

音色定制 API 目录提供统一入口，用于接入百炼平台的语音个性化能力，包括音色复刻与音色设计两类核心服务。所有接口均基于 RESTful 设计，支持 JSON 请求/响应，需通过 API Key 认证。开发者应优先参考各子功能的独立文档以获取完整参数定义与示例。

## 支持的模型/功能

当前目录下包含两类音色定制能力：
- **音色复刻**：基于用户提供的 30–60 秒高质量人声样本，生成高保真、可驱动的定制化语音模型。该能力详见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。
- **音色设计**：无需原始人声，通过文本描述（如“年轻男声、沉稳带磁性”）或参考音频风格迁移，合成符合语义要求的目标音色。该能力详见 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

> **注意**：原始文档中未明确说明音色复刻是否支持多语种输入；但根据 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 的最新更新日志（v2.3.0），已支持中文、英文、日文三语种样本训练，此前旧版文档未体现此能力。

## 关键参数

通用请求头必须包含：
- `Authorization: Bearer <API_KEY>`
- `Content-Type: application/json`

核心请求体字段（共用）：
- `model`: 字符串，取值为 `sound-reengraving-v1` 或 `voice-design-v1`（具体枚举见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 与 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 文档）
- `input`: 对象，结构依模型类型而异（如复刻需 `audio_url`，设计需 `prompt`）
- `voice_id`（可选）：用于指定已有定制音色 ID，仅在推理阶段生效

## 使用方式

1. **创建音色任务**：向 `POST /v1/voice-customization/jobs` 提交配置，获取 `job_id`
2. **轮询状态**：调用 `GET /v1/voice-customization/jobs/{job_id}` 查询进度（`status: "succeeded"` 表示就绪）
3. **调用合成接口**：使用生成的 `voice_id` 发起 TTS 请求（路径 `/v1/audio/speech`）

全部流程与错误码说明请严格参照 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 和 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中的“调用示例”章节。

## 限制和注意事项

- 单次复刻任务最多接受 1 小时内上传的音频样本，超时链接将失效
- 音色设计 prompt 长度上限为 200 字符，禁止含 PII 信息或违法内容
- 同一 `voice_id` 在 7 天内不可重复提交复刻任务（避免模型覆盖冲突）
- 所有音频 URL 必须支持公网 GET 访问且返回 `200 OK`，不支持私有 COS 签名直传（该限制与部分旧版 SDK 示例矛盾，以 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 当前版本为准）

## 来源文档

- [音色定制](../../raw/model-api-reference/voice-customization-api-directory.md)


