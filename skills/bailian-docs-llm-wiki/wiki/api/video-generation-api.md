# video generation api

百炼平台的 video generation API 提供多种视频生成能力，包括文生视频、图生视频、人像驱动动画等。所有模型均通过统一的 RESTful 接口调用，支持[异步任务](../concepts/asynchronous-task.md)提交与结果轮询。开发者需根据具体场景选择适配的模型，并严格遵循各模型的输入约束与计费规则。

## 支持的模型/功能

当前支持以下视频生成模型（按功能分类）：

- **文生视频（Text-to-Video）**：`HappyHorse`、`万相`、`爱诗`、`可灵`、`Vidu`  
- **图生视频（Image-to-Video）**：`万相`、`可灵`、`Vidu`  
- **人像驱动（Portrait Animation）**：`人像驱动`（仅支持单张人像图+语音/文本驱动生成口型同步视频）  
- **多模态视频生成（含运镜/结构化控制）**：`MiniMax`（需额外申请权限）

各模型能力细节请参阅对应文档，例如 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md) 的帧率与分辨率限制、[万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md) 的中文 prompt 优化建议，以及 [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md) 的人脸检测要求。

## 关键参数

通用必填参数（所有模型共用）：
- `model`: 模型标识符，如 `"wanxiang-v1"`、`"kling-1.5"`（见各模型文档命名规范）  
- `input`: JSON 对象，结构因模型而异；例如 `text_to_video` 类型需含 `prompt` 字段，`portrait_animation` 类型需含 `image_url` 和 `audio_url` 或 `text`  
- `parameters`: 可选对象，常见字段包括 `size`（如 `"1080x1920"`）、`duration`（秒，范围 2–8）、`seed`（整数）  

> **注意**：`duration` 参数在 [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md) 中最大支持 8 秒，但 [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md) 当前仅开放 4 秒上限（v1.5 版本），实际值以最新文档为准。

## 使用方式

1. 发送 `POST /api/v1/video/generation` 请求，携带认证 `Authorization: Bearer <api_key>`  
2. 响应返回 `task_id`，用于后续轮询：`GET /api/v1/video/generation/tasks/{task_id}`  
3. 状态为 `succeeded` 后，`output.video_url` 提供直连播放地址（有效期 24 小时）  

示例请求体（万相文生视频）：
```json
{
  "model": "wanxiang-v1",
  "input": {
    "prompt": "一只机械猫在月球表面跳跃，赛博朋克风格"
  },
  "parameters": {
    "size": "720x1280",
    "duration": 4
  }
}
```

## 限制和注意事项

- 所有模型均禁止生成违法、暴力、成人或侵犯肖像权的内容；违规请求将触发风控拦截并冻结调用配额  
- 输入图像需为 JPG/PNG 格式，尺寸 ≥ 512×512，且人脸区域清晰（尤其对 [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md) 模型）  
- 单次请求最大 `prompt` 长度为 200 字符（`万相`、`可灵`、`Vidu`）；`HappyHorse` 支持至 300 字符，详见 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)  
- [异步任务](../concepts/asynchronous-task.md)最长保留 7 天，超时后 `task_id` 不再可查  

> **注意**：`MiniMax` 视频模型当前未接入统一 `/video/generation` 路由，需调用独立 endpoint（见 [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)），该差异将在下个平台版本中收敛。

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


