# video generation api

百炼平台的 video generation api 提供多种视频生成能力，包括文生视频、图生视频、人像驱动动画等。所有模型均通过统一的 RESTful 接口调用，支持异步任务提交与结果轮询。开发者需根据具体场景选择适配的模型，并严格遵循各模型的输入约束与计费规则。

## 支持的模型/功能

当前支持以下视频生成模型（按功能分类）：

- **文生视频（Text-to-Video）**：`HappyHorse`、`万相`、`爱诗`、`可灵`、`Vidu`  
- **图生视频（Image-to-Video）**：`万相`、`可灵`、`Vidu`（部分模型需指定 `input_image` 参数）  
- **人像驱动（Portrait Animation）**：`人像驱动`（仅支持上传单张正脸人像 + 驱动音频或文本）  
- **多模态视频生成**：`MiniMax` 支持文本+图像+语音三模态联合输入（详见 [原文标题](../../raw/model-api-reference/video-generation-api.md)）

> **注意**：`爱诗`（PixVerse）模型在 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中列为支持图生视频，但其最新 API 文档 [原文标题](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md) 明确说明仅支持文生视频（`text_to_video` 模式），图生视频调用将返回 `400 Bad Request`。请以具体模型子文档为准。

## 关键参数

通用必填参数：
- `model`: 模型标识符（如 `"wanxiang"`、`"kling"`），必须与 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中列出的模型名完全一致  
- `input`: JSON 对象，结构因模型而异（例如 `万相` 要求 `prompt` + `size`，`人像驱动` 要求 `image_url` + `audio_url`）  
- `parameters`: 可选，用于控制生成质量、时长、帧率等（如 `kling` 支持 `duration: 5`，`vidu` 支持 `aspect_ratio: "16:9"`）

所有模型均不支持 `stream: true`；视频生成均为异步任务，响应中返回 `task_id` 用于后续查询。

## 使用方式

1. **提交任务**：`POST /api/v1/video-generation`，携带 `model` 和 `input`  
2. **轮询结果**：`GET /api/v1/video-generation/tasks/{task_id}`，直到 `status` 变为 `"succeeded"` 或 `"failed"`  
3. **获取视频**：成功后响应中 `output.video_url` 为直链（有效期 24 小时）

示例（万相文生视频）：
```json
{
  "model": "wanxiang",
  "input": {
    "prompt": "一只橘猫在太空舱里打太极，赛博朋克风格",
    "size": "720p"
  }
}
```

## 限制和注意事项

- 单次请求最大 `prompt` 长度：`万相`/`可灵` 为 200 字符，`Vidu` 为 100 字符，`kling` 为 500 字符  
- 视频时长限制：`HappyHorse` 最长 4 秒，`kling` 默认 5 秒（可扩展至 10 秒需申请白名单）  
- 所有模型禁止生成含暴力、政治敏感、成人内容的视频，违规请求将被拦截并计入风控处罚  
- `人像驱动` 模型对输入人像有严格要求：必须为正面、清晰、无遮挡人脸，背景纯色更佳；不支持多人像或侧脸（参见 [原文标题](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)）

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


