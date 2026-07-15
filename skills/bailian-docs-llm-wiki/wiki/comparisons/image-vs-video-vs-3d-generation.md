# 图像、视频与 3D 生成对比

百炼平台的多媒体生成能力覆盖三条主线：**图像生成**（文生图、图像编辑、翻译、创意工具）、**视频生成**（文生/图生/参考生视频、数字人与人像动画）、**3D 生成**（基于 Tripo 的文生/图生 3D 资产）。三者都构建在 DashScope 兼容接口之上，共享「创建任务 → 轮询结果」的异步范式和统一的鉴权/地域约束，但在输入输出形态、可用模型、调用协议、耗时、地域覆盖和计费产物上差异明显。本文汇总关键维度对比，帮助开发者按业务场景快速选型与集成。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
| --- | --- | --- | --- |
| 输入格式 | 文本 `prompt`、图像（`image_url`/`images`/`base_image_url`/`mask_image_url`）、多模态 `messages`；图像翻译需 `source_lang`+`target_lang` | 文本 `prompt` + 多模态 `media`（首帧/尾帧/图像/视频/参考图/音色） | 三选一互斥：文本 `prompt`（≤1024 字符）、单图 `image`、多图 `images`（固定 4 元素，前/左/后/右） |
| 输出格式 | 图片 URL（有效期 24 小时） | 视频 URL | GLB 模型（`pbr_model_url` 或 `base_model_url`）+ 预览渲染图，链接有效期仅 **2 小时** |
| 主要模型系列 | 千问 Qwen-Image、万相 Wan/Wanx、Z-Image、可灵 Kling、Vidu | 万相 Wan、HappyHorse、爱诗 PixVerse、Vidu、可灵，及数字人/EMO/LivePortrait/AnimateAnyone | Tripo（`Tripo/Tripo-H3.1` 高精度、`Tripo/Tripo-P1.0` 快速专业） |
| 调用协议 | 多数异步（两步式），新版万相 2.6/2.7、Z-Image 支持 HTTP 同步 | 全部异步（两步式） | 全部异步（两步式） |
| 典型 API 端点 | `.../aigc/text2image/image-synthesis`、`.../aigc/image2image/image-synthesis`、`.../aigc/image-generation/generation`；同步走 `.../aigc/multimodal-generation/generation` | `POST .../aigc/video-generation/video-synthesis`（部分数字人/首尾帧走 `.../image2video/video-synthesis`） | `POST .../aigc/video-generation/3d-generation` |
| 轮询查询 | `GET .../api/v1/tasks/{task_id}` | `GET .../api/v1/tasks/{task_id}` | `GET .../api/v1/tasks/{task_id}`（建议间隔约 15 秒，RPS 默认 20） |
| 典型耗时 | 秒级至 1-2 分钟（编辑类偏长） | 1-5 分钟（VACE 约 5-10 分钟） | 较长（面数越高越久） |
| 关键异步头 | `X-DashScope-Async: enable`（同步模型除外） | `X-DashScope-Async: enable`（必选） | `X-DashScope-Async: enable`（必选） |
| 地域覆盖 | 华北2（北京）、新加坡、美国（弗吉尼亚）；多数创意工具/翻译/可灵/Vidu 仅北京 | 华北2（北京）、新加坡为主，部分模型另有美国、德国 Endpoint | **仅华北2（北京）** |
| 计费产物 | 仅对成功生成的输出图片计费，输入图/失败任务不计费 | 按成功生成的视频计费 | 仅对成功结果计数（`text-to-3d`/`image-to-3d`/`multi-image-to-3d`） |
| 典型场景 | 海报/电商主图、创意设计、图文编辑、图像翻译、试衣/虚拟模特 | 短视频/广告、动态营销、数字人播报、人像动画 | 游戏/电商 3D 资产、AR/VR 素材、工业设计原型 |

## 各方案适用场景建议

- **图像生成**：需求量大、迭代快、单次成本低的静态视觉内容首选。文本渲染复杂选千问系列，通用文生图与创意工具选万相，追求低延迟同步返回选 Z-Image / 万相 2.6/2.7。电商场景可直接用试衣、虚拟模特、创意海报等垂直工具，减少自研成本。
- **视频生成**：需要动态叙事、营销短视频或数字人播报时采用。纯创意用文生视频（`wan2.7-t2v` 等），有首帧素材用图生视频，需精确控制起止画面用首尾帧，多素材融合用参考生视频；口播/唱歌数字人用 `wan2.2-s2v` 系列。注意其耗时最长，需设计好轮询与超时重试。
- **3D 生成**：面向游戏、电商展示、AR/VR 与设计原型的三维资产生产。有明确外观参考用单图/多图生 3D（多图按前/左/后/右提供更稳定），只有创意描述用文生 3D；对面数与贴图有要求时用 `Tripo-H3.1` + `geometry_quality: ultra`，追求速度用 `Tripo-P1.0`。务必在 2 小时内下载产物。

## 面向开发者的技术选型参考

1. **地域与鉴权先行**：三者都要求「模型 + Endpoint + API Key 同地域」。3D 生成及大量图像创意工具仅限北京地域，跨国部署需评估地域可用性；北京/新加坡建议迁移到业务空间专属域名以提升性能。
2. **统一异步框架，复用轮询逻辑**：三条线均以 `X-DashScope-Async: enable` 创建任务并轮询 `tasks/{task_id}`，`task_id` 有效期 24 小时，切勿重复创建。可封装统一的任务提交/轮询/状态机（`PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED` 等）模块复用。
3. **同步 vs 异步权衡**：仅图像生成部分新版模型支持 HTTP 同步（低延迟、实现简单）；视频与 3D 强制异步，需引入队列与回调（3D 支持异步任务回调）。
4. **产物时效差异**：图像/视频链接有效期 24 小时，3D 下载链接仅 2 小时，务必在生成成功后尽快转存到自有 OSS。
5. **成本控制**：三者均只对成功产物计费，失败与输入不计费；主账号与子账号共享额度与限流，注意统一配额规划。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


