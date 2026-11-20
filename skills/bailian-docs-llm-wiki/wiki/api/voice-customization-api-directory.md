# voice customization api directory

音色定制 API 提供语音模型的个性化音色生成能力，支持从真实人声复刻到完全原创音色设计的全链路控制。该目录涵盖当前可用的音色定制模型、核心调用参数、标准使用流程及关键约束条件。所有接口均需通过百炼平台认证授权后调用。

## 支持的模型/功能

当前开放两类音色定制能力：
- **音色复刻（Sound Reengraving）**：基于少量参考音频（≥30 秒）重建目标说话人音色，适用于语音克隆类场景；详情见 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。
- **音色设计（Voice Design）**：通过文本描述（如“年轻女声、温和语调、略带粤语口音”）或参数组合生成全新音色，无需原始音频；详情见 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

> **注意**：文档 1 中未明确说明音色复刻是否支持中文方言微调，但 [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md) 的最新版本已补充粤语、川渝话等方言适配参数，旧版文档可能遗漏此能力。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `voice_id` | string | 否 | 复刻任务中返回的音色唯一标识；音色设计任务中可为空，由系统生成 |
| `prompt` | string | 是（音色设计）/ 否（复刻） | 文本化音色描述，长度 ≤ 200 字符；详见 [音色设计](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md) |
| `audio_url` | string | 是（复刻）/ 否（设计） | 参考音频直链（HTTPS，WAV/MP3，≤60 秒），需公网可访问 |

## 使用方式

1. 调用 `/v1/voice/customize` 接口提交定制请求（POST）；
2. 获取 `task_id`，轮询 `/v1/voice/task/{task_id}` 查询状态；
3. 状态为 `success` 后，从响应中提取 `voice_id`，用于后续 TTS 合成；
4. 所有请求需携带 `Authorization: Bearer <api_key>` 及 `Content-Type: application/json`。

## 限制和注意事项

- 单次复刻任务最多支持 3 段参考音频（总时长 ≤ 60 秒）；
- 音色设计 prompt 不得包含真实人物姓名、品牌名或违法信息；
- 复刻音色仅限本人或获得明确授权的语音数据，严禁用于身份冒用；
- 免费试用额度为每月 5 次复刻 + 10 次设计，超出后按量计费；
- 音色复刻结果不可跨项目迁移，如需复用需重新提交音频并获取新 `voice_id`。

## 来源文档

- [音色定制](../../raw/model-api-reference/voice-customization-api-directory.md)


