# video generation api

百炼平台的 video generation api 提供多种视频生成能力，包括文生视频、图生视频、人像驱动动画等。所有模型均通过统一的 RESTful 接口调用，支持[异步任务](../concepts/asynchronous-task.md)提交与结果轮询。开发者需根据具体场景选择适配的模型，并严格遵循各模型的输入约束与计费规则。

## 支持的模型/功能

当前支持以下视频生成模型（按功能分类）：

- **文生视频（Text-to-Video）**：`HappyHorse`、`万相`、`爱诗`、`可灵`、`Vidu`  
- **图生视频（Image-to-Video）**：`万相`、`可灵`、`Vidu`（部分模型需指定 `input_image` 参数）  
- **人像驱动（Portrait Animation）**：`人像驱动`（仅支持上传单张正脸人像 + 驱动音频或文本）  
- **多模态视频生成**：`MiniMax` 支持文本+图像+音频联合输入（详见 [原文标题](../../raw/model-api-reference/video-generation-api.md)）

> **注意**：`爱诗`（PixVerse）在 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中列为支持图生视频，但其最新 API 文档 [原文标题](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md) 明确说明 v2.1 起已暂停图生视频功能，仅保留文生视频。请以后者为准。

## 关键参数

所有视频生成请求共用以下顶层参数（模型特有参数见对应子文档）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"kling"`、`"wanxiang"`、`"portrait-animation"` |
| `input` | object | 是 | 输入内容，结构因模型而异（如 `text`、`image_url`、`audio_url`） |
| `parameters` | object | 否 | 控制参数，如 `duration`（秒，默认 4）、`aspect_ratio`（如 `"16:9"`）、`seed` |
| `callback_url` | string | 否 | 异步完成回调地址（若未提供则需轮询 `GET /jobs/{id}`） |

完整参数定义请参考各模型专属文档，例如 `可灵` 的 `parameters` 支持 `motion_intensity` 和 `style_preset`，详见 [原文标题](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)。

## 使用方式

1. **提交任务**：`POST /api/v1/video-generation`，携带 JSON body  
2. **获取任务 ID**：响应含 `"job_id"` 字段  
3. **查询状态**：`GET /api/v1/jobs/{job_id}`，`status` 可为 `queued` / `running` / `succeeded` / `failed`  
4. **获取结果**：`status === "succeeded"` 时，响应中 `output.video_url` 为直链（有效期 24 小时）

所有模型均不支持同步返回视频二进制流，必须通过异步流程获取结果。

## 限制和注意事项

- 单次请求最大 `input.text` 长度：`可灵` 限 512 字符，`万相` 限 200 字符，`人像驱动` 限 100 字符（含标点）  
- 视频时长统一限制为 2–8 秒；超出将被截断或报错  
- `input.image_url` 必须为公网可访问的 HTTPS 地址，且图片尺寸建议 ≥ 512×512，格式为 JPG/PNG  
- `人像驱动` 模型对人脸角度、光照、遮挡敏感，失败率高于其他模型，建议预处理校验（参见 [原文标题](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)）  
- 所有模型均不支持跨区域调用（如华东节点调用华北部署的 `Vidu` 实例），需确认 endpoint 与模型部署区域一致

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


