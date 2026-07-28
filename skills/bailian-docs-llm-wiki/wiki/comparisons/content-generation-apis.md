# [多模态](../concepts/multimodal.md)生成 API 对比

百炼平台提供图像生成、3D 资产生成和视频生成三大类[多模态](../concepts/multimodal.md)生成 API，分别覆盖静态视觉内容、三维空间资产和动态视频内容的生产需求。三者底层模型、调用模式、输入输出格式各有差异，本文从关键维度进行横向对比，帮助开发者在技术选型时快速定位合适的 API 方案。

## 关键维度对比

| 对比维度 | 图像生成 API | 3D 生成 API | 视频生成 API |
| --- | --- | --- | --- |
| **输入格式** | 文本（[prompt](../guides/prompt.md)）、图像 URL（图生图/编辑）、涂抹区域、手绘涂鸦 | 文本（[prompt](../guides/prompt.md)，最大1024字符）、单张图像 URL、多图（固定4视角，前/左/后/右） | 文本（[prompt](../guides/prompt.md)）、图像 URL（首帧/首尾帧/参考图）、视频 URL、音频 URL |
| **输出格式** | PNG 图像（1-9张，分辨率512×512~4K） | GLB 格式 3D 模型（PBR材质/无贴图基础模型）+ 预览渲染图 | 视频（分辨率480P~4K，时长5/8秒等） |
| **支持模型** | 千问图像（Qwen-Image）、万相（Wan）、Z-Image、可灵（Kling）、Vidu，及多个创意工具模型 | Tripo/Tripo-H3.1（高精度）、Tripo/Tripo-P1.0（专业，速度更快） | 万相（wan2.7/wan2.6/早期）、HappyHorse、PixVerse、Vidu、可灵（Kling）、人像动画系列、万相动作/数字人 |
| **调用模式** | 同步（千问/万相2.6+/Z-Image）+ 异步（万相2.5及以下/可灵/Vidu/创意工具） | 仅异步 | 仅异步 |
| **API 端点** | 同步：`/api/v1/services/aigc/multimodal-generation/generation`；异步：`/api/v1/services/aigc/text2image/image-synthesis` 等多路径 | 创建：`/api/v1/services/aigc/video-generation/3d-generation`；查询：`/api/v1/tasks/{task_id}` | 创建：`/api/v1/services/aigc/video-generation/video-synthesis`；查询：`/api/v1/tasks/{task_id}` |
| **地域要求** | 支持多地域（北京、新加坡、弗吉尼亚、法兰克福） | 仅限华北2（北京），须使用北京地域 API Key | 支持多地域，但模型、Endpoint、API Key 必须属同一地域 |
| **异步任务有效期** | task_id 有效期24小时，图像 URL 有效期24小时 | task_id 有效期24小时，产物下载链接有效期仅2小时 | task_id 有效期24小时，过期返回 UNKNOWN |
| **轮询间隔建议** | — | 约15秒，查询 RPS 限制为20 | 约15秒，状态流转 PENDING→RUNNING→SUCCEEDED/FAILED |
| **典型场景** | 文生图、图像编辑、虚拟模特、海报生成、试衣、背景生成、创意文字等 | 文生3D、单图生3D、多图生3D，输出可编辑 GLB 模型 | 文生视频、图生视频、参考生视频、视频编辑、视频超分、对口型、数字人 |

## 调用模式差异

三者最显著的技术差异在于调用模式：

- **图像生成**：部分模型支持同步调用（千问图像、万相2.6+、Z-Image），一次请求即可获得结果，开发体验最佳；旧版模型及创意工具仍需异步轮询。
- **3D 生成**和**视频生成**：由于生成耗时较长，均采用纯异步模式。创建任务时必须携带 `X-DashScope-Async: enable` 请求头，否则报错 `current user api does not support synchronous calls`。

异步流程统一为「创建任务获取 task_id → 轮询查询结果」，但产物有效期差异较大：3D 生成的下载链接仅2小时，远短于图像和视频的24小时，需特别注意及时下载。

## 模型丰富度与功能覆盖

| 能力类别 | 图像生成 | 3D 生成 | 视频生成 |
| --- | --- | --- | --- |
| 文生内容 | 支持 | 支持 | 支持 |
| 图生内容 | 支持（图生图/编辑/局部重绘） | 支持（单图生3D/多图生3D） | 支持（首帧/首尾帧/参考生视频） |
| 内容编辑/增强 | 支持（风格迁移、超分、去水印、扩图） | 不支持 | 支持（视频编辑、超清、对口型、动作模仿） |
| 文字渲染 | 支持（千问擅长复杂文字） | 不适用 | 部分支持（Vidu 中英文字精准渲染） |
| 模型数量 | 最多（5+系列，十余个创意工具） | 最少（2个模型） | 较多（7+家族） |

## 选型建议

- **静态视觉内容生产**（海报、模特图、产品图、创意设计）→ 优先选择图像生成 API。千问图像擅长文字渲染和真实质感，万相支持多种艺术风格，Z-Image 适合轻量快速生图。
- **三维空间资产生产**（游戏道具、电商3D展示、AR/VR内容）→ 选择 3D 生成 API。需要北京地域 API Key，且注意产物下载链接仅2小时有效期。
- **动态视频内容生产**（短视频、广告、数字人播报、视频编辑增强）→ 选择视频生成 API。万相2.7为新版协议推荐使用，可灵支持智能分镜，PixVerse 支持4K超清和动作模仿，人像动画系列适合舞蹈/唱演等场景。
- **混合需求**：若需先生成静态素材再制作动态内容，可组合使用。例如先用图像生成 API 产出首帧图，再用视频生成 API 做图生视频；或用3D生成 API 产出模型后截图作为视频参考素材。

## 来源文档

- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


