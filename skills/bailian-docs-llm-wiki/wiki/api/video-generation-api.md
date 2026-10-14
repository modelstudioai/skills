# video generation api

百炼平台的 video generation API 提供多种视频生成能力，包括文生视频、图生视频、人像驱动动画等。所有模型均通过统一的 RESTful 接口调用，支持异步任务提交与结果轮询。开发者需根据具体场景选择适配的模型，并严格遵循各模型的输入约束与计费规则。

## 支持的模型/功能

当前支持以下视频生成模型，各自具备不同能力边界与适用场景：

- **HappyHorse**：专注高质量文生视频，支持 4s/8s 两种时长，推荐用于广告创意与短视频脚本可视化  
- **万相**：支持文生视频与图生视频，对中文提示词理解优化，适合电商与泛娱乐场景  
- **人像驱动**：基于单张人像图生成口型/表情同步的说话视频，需提供音频或文本驱动 [原文标题](../../raw/model-api-reference/video-generation-api.md)  
- **爱诗（PixVerse）**：强调艺术风格迁移与运镜控制，支持 SDXL 风格提示词语法  
- **可灵（Kling）**：支持最长 120 秒视频生成，具备多镜头分镜能力，但仅限企业客户开通 [原文标题](../../raw/model-api-reference/video-generation-api.md)  
- **Vidu**：国产自研模型，对中文语义与本土文化元素适配更强，支持 512×512 至 1024×1024 分辨率输出  
- **MiniMax**：提供轻量级实时视频生成接口，延迟低于 3s，适用于互动直播场景  

> **注意**：可灵（Kling）的 120 秒生成能力在 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中被列为标准功能，但实际调用时若未开通企业权限，API 将返回 `403 Forbidden` 并提示“max_duration_exceeded”，请务必提前申请权限。

## 关键参数

所有模型共用基础参数，部分模型扩展专属字段：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"kling"`, `"vidu"`, `"portrait-animation"` |
| `input` | object | 是 | 输入内容，结构依模型而异（如 `text`, `image_url`, `audio_url`） |
| `parameters` | object | 否 | 控制参数，常见字段：`duration`（秒）、`aspect_ratio`（如 `"16:9"`）、`seed`（整数） |
| `callback_url` | string | 否 | 异步结果回调地址，若不提供则需轮询 `GET /v1/tasks/{task_id}` |

人像驱动模型要求 `input` 中必须包含 `image_url` 和 `text` 或 `audio_url`；Vidu 模型不支持 `seed` 参数，设置将被忽略。

## 使用方式

1. **提交任务**：`POST /v1/videos/generate`，携带 JSON body  
2. **获取任务 ID**：响应含 `task_id` 与 `status`（`queued` / `running` / `succeeded` / `failed`）  
3. **查询结果**：轮询 `GET /v1/tasks/{task_id}`，成功时返回 `output.video_url`（有效期 24 小时）  
4. **错误处理**：检查 `error.code`（如 `invalid_input`, `quota_exhausted`, `model_unavailable`）  

示例请求（Vidu 文生视频）：
```json
{
  "model": "vidu",
  "input": {"text": "一只机械猫在樱花树下跳跃，赛博朋克风格"},
  "parameters": {"duration": 4, "aspect_ratio": "9:16"}
}
```

## 限制和注意事项

- 所有模型均**不支持**输入含敏感人物、暴力、违法内容的提示词或图像，违规请求将直接拒绝并计入风控日志  
- 视频分辨率与帧率由模型固定，不可通过参数覆盖（例如 HappyHorse 固定为 720p@24fps）  
- 人像驱动模型对输入人像图有明确要求：正脸、无遮挡、光照均匀、背景简洁，否则合成效果显著下降 [原文标题](../../raw/model-api-reference/video-generation-api.md)  
- 免费试用额度仅适用于 HappyHorse、万相、Vidu 三款模型；MiniMax 与可灵需单独购买配额  
- `video_url` 返回的视频为 MP4 格式，H.264 编码，无水印；但 Vidu 输出默认带平台标识角标（可通过 `parameters.hide_watermark=true` 去除，仅限付费用户）

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


