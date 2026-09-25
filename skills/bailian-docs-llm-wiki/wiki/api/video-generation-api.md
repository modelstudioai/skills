# video generation api

百炼平台的 video generation API 提供多种视频生成能力，包括文生视频、图生视频、人像驱动动画等。所有模型均通过统一的 RESTful 接口调用，支持异步任务提交与结果轮询。开发者需根据具体场景选择适配的模型，并严格遵循各模型的输入约束与计费规则。

## 支持的模型/功能

当前支持以下视频生成模型（按功能分类）：

- **文生视频（Text-to-Video）**：`HappyHorse`、`万相`、`爱诗`、`可灵`、`Vidu`  
- **图生视频（Image-to-Video）**：`万相`、`可灵`、`Vidu`  
- **人像驱动（Portrait Animation）**：`人像驱动`（仅支持单张人像图+语音/文本驱动）  
- **多模态视频生成（含运镜/结构化控制）**：`可灵`、`Vidu`、`MiniMax`

各模型能力细节详见其独立文档，例如 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md) 支持最长 4 秒 1080p 输出，而 [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md) 支持 8 秒 4K 分辨率及镜头语言提示词。[人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md) 模型不支持文生视频，仅接受 base64 编码的人像图与驱动文本。

> **注意**：原始文档中 `万相` 的图生视频最大输入图尺寸标注为 1024×1024（见 [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)），但最新 SDK v2.3.0 已放宽至 1280×1280；请以实际 API 响应的 `400 Bad Request` 错误提示为准。

## 关键参数

所有 video generation 请求共用以下核心字段（`POST /v1/videos/generations`）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"wanxiang"`、`"kling"`、`"portrait-animation"` |
| `prompt` | string | 是（除 portrait-animation 外） | 中文或英文提示词，长度 ≤ 512 字符 |
| `image_url` 或 `image` | string / string(base64) | 部分模型必填 | 图生视频必需；`portrait-animation` 仅接受 `image`（base64） |
| `duration` | number | 否 | 视频时长（秒），取值范围依模型而异（如 `kling`: 2–8，`vidu`: 2–8，`portrait-animation`: 固定 3） |
| `seed` | integer | 否 | 随机种子，用于结果复现 |

> **注意**：`portrait-animation` 模型不接受 `prompt` 字段，驱动文本需置于 `input.text`（见 [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)），该设计与其他模型不一致，调用前务必校验 schema。

## 使用方式

1. **提交任务**：`POST https://dashscope.aliyuncs.com/api/v1/videos/generations`，携带认证头 `Authorization: Bearer <api_key>`  
2. **获取任务 ID**：响应体含 `"id": "vt_abc123..."` 和 `"status": "queued"`  
3. **轮询结果**：`GET /v1/videos/generations/{id}`，直到 `status` 变为 `"succeeded"` 或 `"failed"`  
4. **下载视频**：成功响应中 `output.video_url` 为临时直链（有效期 24 小时）

示例请求（可灵文生视频）：
```json
{
  "model": "kling",
  "prompt": "一只橘猫在秋日森林里跳跃，落叶纷飞，电影感运镜",
  "duration": 6
}
```

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 512 字符；超长将被截断且不报错（见 [可灵](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md) 文档说明）  
- 所有模型输出视频均为 MP4 格式，H.264 编码，无音频轨道（`portrait-animation` 除外，其支持 TTS 音频合成）  
- 免费额度仅覆盖 `HappyHorse` 和 `万相` 的基础分辨率（720p）；`Vidu`、`kling`、`MiniMax` 默认启用高分辨率，需确认配额或开通付费  
- 异步任务最长保留 7 天，超时后 `video_url` 失效，不可重试  

> **注意**：原始文档 [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md) 中声明支持 `fps` 参数，但当前 API 实际忽略该字段，固定输出 24fps；此行为已在 v2024.07.15 版本变更日志中确认。

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


