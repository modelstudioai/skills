# music generation references

百炼平台 Fun-Music 系列模型提供基于文本描述或歌词的音乐生成 API，支持非流式和 SSE 流式两种输出模式。本页汇总了 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md) 中的服务端点、关键参数与返回结构，便于开发者快速集成。

> **注意**：该模型目前处于邀测阶段，需在模型广场申请开通后才能使用，且仅在中国内地（北京地域）部署范围下可用。

## 支持的模型与服务端点

- 服务端点：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation`
- 通信协议：HTTPS；[流式输出](../concepts/streaming.md)走 SSE（Server-Sent Events）
- 可选模型（`model` 字段必填）：
  - `fun-music-preview`
  - `fun-music-v1`

详细的服务端点定义见 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)。

## 请求头

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `Authorization` | string | 是 | `Bearer {api-key}`，需替换为实际 API Key |
| `Content-Type` | string | 是 | 固定为 `application/json` |
| `X-DashScope-SSE` | string | 否 | 设为 `enable` 时启用 SSE [流式输出](../concepts/streaming.md) |

API Key 获取方式参见百炼文档；请求头要求与示例完整说明见 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)。

## 请求体关键参数

请求体顶层包含 `model` 和 `input` 两个必填字段。`input` 内部参数如下：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `lyrics` | string | 与 `prompt` 二选一 | - | 自定义歌词；同时传入 `lyrics` 与 `prompt` 时仅 `lyrics` 生效 |
| `prompt` | string | 与 `lyrics` 二选一 | - | 文本提示词，模型据此自动创作歌词并生成歌曲 |
| `gender` | string | 否 | `female` | 演唱声音性别：`male` / `female` |
| `format` | string | 否 | `mp3` | 输出音频编码：`mp3`（适合传输/存储）或 `wav`（适合后期处理） |
| `enable_aigc_watermark` | boolean | 否 | `false` | 开启后在音频末尾追加表示「AI」的摩尔斯电码（·— ··）水印，开启会增加音频时长 |

### 字符长度限制

`lyrics` 与 `prompt` 在两种输出模式下的长度限制不同：

- `lyrics`
  - 非流式：中文 5~350 字符，英文 5~2000 字符
  - 流式：中文 300~350 字，英文 200~250 词
- `prompt`
  - 非流式：1~2000 字符
  - 流式：5~1000 个中文汉字或英文单词

## 使用方式

### 非[流式输出](../concepts/streaming.md)

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "fun-music-v1",
    "input": {
      "prompt": "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐",
      "gender": "female"
    }
  }'
```

返回体中 `output.audio.url` 直接给出完整音频文件的 OSS 下载链接（有效期 24 小时），`output.extra_info.lyrics` 给出最终歌词，`usage.duration` 给出音乐时长（秒，用于计费）。

### [流式输出](../concepts/streaming-output.md)（SSE）

请求时额外加上 `X-DashScope-SSE: enable`：

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: enable" \
  -d '{
    "model": "fun-music-v1",
    "input": {
      "prompt": "节奏感强的电子舞曲，合成器音效，充满能量，适合健身运动场景",
      "gender": "male"
    }
  }'
```

[流式输出](../concepts/streaming-output.md)特点：

- 中间消息：`output.audio.data` 为 Base64 音频数据片段，`finish_reason` 为字符串 `"null"`
- 最终消息：`output.audio.data` 为空字符串，`output.audio.url` 给出完整音频 OSS URL，`extra_info` 补齐 `lyrics`、`sample_rate`、`channels`，`finish_reason` 为 `stop`

## 返回结构

顶层字段：

- `request_id` (string)：请求唯一标识，便于排查与日志追踪
- `output` (object)：模型输出
  - `audio.url` (string)：完整音频 OSS URL，有效期 24 小时
  - `audio.data` (string)：流式中间消息为 Base64 片段，非流式或最终消息为空
  - `audio.id` (string)：音频文件 ID
  - `audio.expires_at` (integer)：URL 过期时间戳（Unix）
  - `extra_info.channels` (integer)：声道数，如 2 表示立体声
  - `extra_info.sample_rate`：采样率（如 48000）
  - `extra_info.lyrics` (string)：生成的歌词内容
  - `finish_reason` (string)：`null` 表示生成中，`stop` 表示自然结束
- `usage.duration` (integer)：音乐时长（秒），作为计费单位

> **注意**：示例中 `extra_info.sample_rate` 在非流式返回里以整数形式（`48000`）出现，而流式最终消息以字符串形式（`"48000"`）出现，解析时建议做兼容处理。

## 限制与注意事项

- 邀测阶段：需先在模型广场为 `fun-music-v1` 申请开通；地域上仅支持北京。
- 文本字段二选一：`lyrics` 与 `prompt` 必须至少传一个；二者同传时 `prompt` 被忽略。
- 输出模式与长度限制需匹配：流式模式对 `lyrics` 和 `prompt` 的长度有更严格区间，超出会导致请求失败。
- 音频 URL 有效期仅 24 小时，需要长期保存的场景请及时转存。
- AIGC 水印开启会在音频末尾增加摩尔斯电码信号，从而拉长音频时长，进而影响 `usage.duration` 的计费值。
- `format` 选择 `wav` 时文件体积明显大于 `mp3`，请按业务带宽与存储成本权衡。

完整字段定义、错误码与最新示例以官方文档 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md) 为准。

## 来源文档

- [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)









