# video generation api

视频生成 API 提供多种模型能力，支持文生视频、图生视频、人像驱动动画等场景。开发者可通过统一接口调用不同后端模型，按需选择适合任务的模型实例。所有模型均通过百炼平台统一鉴权与计费，具体能力边界和输入格式以各模型官方文档为准。

## 支持的模型/功能

当前支持以下视频生成模型：
- **HappyHorse**：面向创意内容的文生视频模型，支持 4 秒标准时长输出  
- **万相**：侧重艺术风格化视频生成，支持图像提示（image [prompt](../guides/prompt.md)）输入  
- **人像驱动**：基于单张人像图+音频/文本驱动生成口型同步动画，适用于数字人场景  
- **爱诗（PixVerse）**：强调高动态细节与运镜控制，支持 motion strength 参数调节  
- **可灵（Kling）**：支持长时序连贯视频生成（最长 120 秒），需分段请求与拼接  
- **Vidu**：国产自研多模态视频模型，对中文提示词理解优化明显  
- **MiniMax**：提供低延迟轻量级视频生成选项，适用于实时交互场景  

> **注意**：`可灵（Kling）` 的最大时长在 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中标注为 120 秒，但实际调用中受 `max_frames` 和 `fps` 参数共同约束；请以 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中列出的模型链接跳转至对应帮助中心获取最新规格限制。

## 关键参数

通用必填参数：
- `model`: 模型标识符（如 `"kling-v1"`, `"vidu-1.0"`），必须与 [原文标题](../../raw/model-api-reference/video-generation-api.md) 中所列模型名称严格一致  
- `input`: 包含 `prompt`（字符串）及可选 `image_url`（图生视频）、`audio_url`（人像驱动）等字段  
- `parameters`: 控制生成质量与时长，常见字段包括 `duration`（秒）、`fps`（默认 8）、`seed`（可复现）、`motion_strength`（仅部分模型支持）  

## 使用方式

1. 通过 `POST /v1/videos/generations` 发起请求  
2. 请求头携带 `Authorization: Bearer <api_key>`  
3. 响应返回 `id`，用于轮询 `GET /v1/videos/generations/{id}` 获取结果（状态为 `succeeded` 后返回 `video_url`）  
4. 所有模型均遵循该统一流程，差异仅体现在 `input` 和 `parameters` 结构上  

## 限制和注意事项

- 单次请求最大 `duration` 因模型而异：`kling-v1` 最高 120 秒，`vidu-1.0` 限 8 秒，`happyhorse-1.0` 限 4 秒  
- 输入图像需为公网可访问 URL，且尺寸建议 ≥ 512×512（人像驱动要求正面清晰人像）  
- 视频生成不支持跨模型参数混用（例如向 `wanxiang-1.0` 传 `audio_url` 将被忽略）  
- 输出视频为 MP4 格式，H.264 编码，分辨率固定为 720p（部分模型支持 1080p，需显式指定 `parameters.resolution`）

## 来源文档

- [视频生成](../../raw/model-api-reference/video-generation-api.md)


