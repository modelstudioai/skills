# voice customization api directory

音色定制 API 提供语音克隆与合成能力，支持基于少量音频样本复刻目标音色（Sound Reengraving），以及通过文本描述生成全新音色（Voice Design）。所有接口均通过 HTTPS 调用，需携带有效 API Key 与模型标识。该能力当前仅对已开通权限的白名单用户开放。

## 支持的模型/功能

- **音色复刻（Sound Reengraving）**：输入 30–60 秒高质量单人语音样本（无背景音、无混响），生成可调用的复刻音色 ID；支持中文、英文及中英混合语种。详情见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。
- **音色设计（Voice Design）**：通过自然语言描述（如“30 岁女性，沉稳带磁性，语速适中”）生成全新音色，无需原始音频；输出为可直接用于 TTS 的音色 ID。详情见 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。
- > **注意**：[音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 文档中提及支持“5 秒极短样本”，但最新服务端已将最低时长强制提升至 30 秒，该处文档尚未同步更新。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定值：`sound-reengraving-v1` 或 `voice-design-v1` |
| `audio_url` | string | 仅复刻必填 | 音频文件公网可访问 URL（HTTPS，WAV/MP3，≤10MB） |
| `prompt` | string | 仅设计必填 | 音色描述文本（20–200 字，中文优先） |
| `voice_name` | string | 否 | 自定义音色名称（仅用于管理，不参与合成） |

## 使用方式

1. 发起 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/voice-customization`  
2. Header 中设置 `Authorization: Bearer YOUR_API_KEY` 和 `Content-Type: application/json`  
3. Body 按模型类型传参（参考上表），例如音色复刻请求体：
```json
{
  "model": "sound-reengraving-v1",
  "audio_url": "https://example.com/sample.wav"
}
```
4. 成功响应返回 `voice_id`，后续 TTS 请求中通过 `voice_id` 引用该音色。完整调用示例见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。

## 限制和注意事项

- 单个账号最多保存 50 个定制音色（含复刻与设计），超出后需删除旧音色；
- 复刻音色生成耗时约 60–120 秒，设计音色约 20–40 秒，超时未完成将返回失败；
- 所有上传音频须为单声道、16kHz 采样率，否则可能触发静音检测失败；
- > **注意**：原始文档 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) 中列出的 `style` 参数（如 `emotional`, `narrative`）已于 v1.2 版本移除，当前版本忽略该字段，勿在请求中传入。

## 来源文档

- [音色定制](../../raw/model-api-reference/voice-customization-api-directory.md)


