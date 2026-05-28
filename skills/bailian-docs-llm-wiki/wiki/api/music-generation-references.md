# music generation references

本文档提供百炼平台音乐生成服务的 API 技术参考。开发者可通过 DashScope 标准接口调用音频生成模型，支持非流式与流式（SSE）两种输出模式，适用于背景音乐生成与有声内容创作场景。如需快速接入或了解能力边界，建议结合 [[music-generation]] 指南与本文档对照使用。

## 支持的模型与功能
当前平台开放的音乐生成模型为 `fun-music-v1`，核心能力如下：
* **双模式输入**：支持通过 `[[prompt|prompt]]`（提示词）自动作词并生成歌曲，或通过 `lyrics` 直接输入指定歌词谱曲。
* **流式传输**：基于 SSE 协议实现音频分片实时下发，降低首字节延迟。
* **音频定制**：支持演唱性别切换、输出编码格式选择及 AIGC 防伪水印。
完整功能定义与版本变更日志请以官方说明为准：[音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)。

## 关键参数
请求端点：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation`（HTTPS）。认证凭证获取方式见 [[api-key]]。

### 请求头 (Headers)
| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `Authorization` | string | 是 | `Bearer {api-key}` |
| `Content-Type` | string | 是 | `application/json` |
| `X-DashScope-SSE` | string | 否 | 设为 `enable` 启用[[streaming-output|流式输出]] |

### 请求体 (Body)
| 参数路径 | 类型 | 必填 | 说明与默认值 |
|---|---|---|---|
| `model` | string | 是 | 固定为 `fun-music-v1` |
| `input.[[prompt|prompt]]` | string | 条件 | 提示词，与 `lyrics` 二选一。长度限制见下方注意事项 |
| `input.lyrics` | string | 条件 | 歌词内容，与 `[[prompt|prompt]]` 二选一。长度限制见下方注意事项 |
| `input.gender` | string | 否 | `female`（默认）或 `male` |
| `input.format` | string | 否 | `mp3`（默认）或 `wav` |
| `input.enable_aigc_watermark` | boolean | 否 | 是否追加 AI 摩尔斯电码水印。默认 `false` |

> **注意**：当 `lyrics` 与 `prompt` 同时传入时，系统仅处理 `lyrics`，`prompt` 将被静默忽略。详细字段类型与枚举值请参考 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)。

## 使用方式
根据业务对实时性的要求，选择同步阻塞调用或流式传输。

### 非[[streaming-output|流式输出]]
等待模型完整生成后一次性返回结果，适用于离线任务或批量处理。
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

### [[streaming-output|流式输出]]
在 Header 中添加 `X-DashScope-SSE: enable`。服务端将分批次返回 Base64 音频片段，最终消息包含完整下载 URL 与歌词信息。
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
完整请求/响应 JSON 结构体示例可查阅 [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)。

## 限制与注意事项
* **开通与地域限制**：模型目前处于邀测阶段，需前往 [[model-market]] 申请开通。服务仅在中国内地（北京）地域可用，其他区域调用将返回网络或权限错误。
* **输入长度限制**：
  * **非流式**：`prompt` 1~2000 字符；`lyrics` 中文 5~350 字 / 英文 5~2000 词。
  * **流式**：`prompt` 5~1000 个汉字或英文词；`lyrics` 中文 300~350 字 / 英文 200~250 词。
  > **注意**：流式模式对输入长度要求更严格，超出阈值或过短均会导致校验失败。
* **结果与计费处理**：
  * `output.audio.url` 有效期仅为 24 小时，生产环境建议在接收后立即下载或同步至自有对象存储。
  * 计费依据为 `usage.duration`（秒）。开启水印或静音段会导致实际计费时长与感知时长存在微小差异。

## 来源文档

- [音乐生成Fun-Music API参考](../../raw/model-api-reference/music-generation-references/fun-music-api.md)

