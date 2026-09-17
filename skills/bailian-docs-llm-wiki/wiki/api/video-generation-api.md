# video generation api

百炼平台的 video generation api 提供多种视频生成能力，包括文生视频、图生视频、人像驱动动画等。所有模型均通过统一 RESTful 接口调用，支持[异步任务](../concepts/asynchronous-task.md)提交与结果轮询。开发者需根据具体场景选择适配的模型，并注意各模型在输入格式、时长、分辨率等方面的差异化约束。

## 支持的模型/功能

当前支持以下视频生成模型（按功能分类）：
- **文生视频（Text-to-Video）**：`HappyHorse`、`万相`、`爱诗`、`可灵`、`Vidu`  
- **图生视频（Image-to-Video）**：`万相`、`可灵`、`Vidu`  
- **人像驱动（Portrait Animation）**：`人像驱动`（仅支持单张人像图+语音/文本驱动生成口型同步视频）  
- **[多模态](../concepts/multi-modal.md)视频生成（Text+Image+Audio）**：`MiniMax`（需同时提供 [prompt](../guides/prompt.md)、reference image 和 audio URL）  

各模型能力细节详见 [原文标题](../../raw/model-api-reference/video-generation-api.md)。完整参数说明和示例请参考对应子文档，例如 `万相` 的图像控制参数见 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)，`人像驱动` 的音频对齐要求见 [原文标题](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)。

## 关键参数

通用必填参数：
- `model`: 模型标识符（如 `"wanxiang"`、`"kling"`），必须与 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中列出的名称严格一致  
- `input.prompt`: 文本提示词（UTF-8 编码，长度 ≤ 512 字符）  
- `input.image_url`（可选）：用于图生视频或控制帧，需为公网可访问的 HTTPS 图片 URL（支持 JPG/PNG，≤ 10 MB）  
- `input.audio_url`（仅 `MiniMax` 和 `人像驱动` 必填）：WAV/MP3 格式，采样率 ≥ 16kHz，时长 ≤ 30 秒  

> **注意**：`可灵`（kling）模型在 [原文标题](../../raw/model-api-reference/video-generation-api/kling-api-reference.md) 中声明支持 `input.negative_prompt`，但实际 API 返回 `400 Bad Request` 并提示该字段不被识别——该字段已废弃，请勿使用。

## 使用方式

1. 发送 `POST /v1/videos/generations` 请求，携带 JSON body  
2. 响应中获取 `id` 字段，用于后续轮询：`GET /v1/videos/generations/{id}`  
3. 当 `status` 变为 `"succeeded"` 时，从 `output.video_url` 下载 MP4 成品（有效期 24 小时）  
4. 所有请求需携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  

错误响应遵循标准 HTTP 状态码，常见错误包括：`400`（参数校验失败）、`401`（鉴权失败）、`429`（超出速率限制）。详细错误码说明见 [原文标题](../../raw/model-api-reference/video-generation-api.md)。

## 限制和注意事项

- 单次请求最大视频时长：`万相`/`可灵`/`Vidu` 为 8 秒；`HappyHorse` 为 4 秒；`人像驱动` 为 15 秒（受音频时长限制）  
- 输出分辨率固定：除 `MiniMax` 支持 `1080x1920` 外，其余模型默认输出 `720x1280`（竖屏）  
- 不支持跨模型参数混用（例如向 `wanxiang` 传 `input.voice_style`）  
- 视频内容需符合中国法律法规及百炼平台《内容安全规范》，禁止生成违法、暴力、成人相关内容  
- [异步任务](../concepts/asynchronous-task.md)最长保留 72 小时，超时后 `video_url` 失效且不可恢复

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


