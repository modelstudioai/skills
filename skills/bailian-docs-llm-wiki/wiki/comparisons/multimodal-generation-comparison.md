# 图像、视频与 3D 生成对比

百炼平台的多模态生成 API 覆盖图像、视频与 3D 三类媒体产出，分别对应不同的模型家族（千问/万相/可灵/Z-Image、万相/爱诗/Vidu/可灵、Tripo）和不同的调用模式。本页将三者放在同一维度下横向对比，帮助开发者根据产出形态、输入素材、调用方式与计费关注点完成技术选型。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
| --- | --- | --- | --- |
| 产出形态 | 静态图片（PNG） | 动态视频（带音视频） | 3D 模型（GLB，可选 PBR 贴图） |
| 主要输入 | 文本、参考图、待编辑图 | 文本、首帧/首尾帧图、参考图/视频、音频 | 文本、单图、多图（前/左/后/右四视角） |
| 支持模型 | 千问 image 2.0/Max/Plus、万相 2.7/2.6/2.5/2.2/2.1、Z-Image、可灵 v3/omni | 万相 HappyHorse/2.7/2.6/2.2/wanx2.1、爱诗 PixVerse、Vidu、可灵 | Tripo-H3.1（高精度）、Tripo-P1.0（专业快速） |
| 调用模式 | 同步（推荐，新版模型）+ 异步（V1/编辑/创意类） | 仅异步 | 仅异步 |
| 创建任务端点 | `POST /api/v1/services/aigc/multimodal-generation/generation`（同步）/ 同左异步 | `POST /api/v1/services/aigc/video-generation/video-synthesis`（部分走 `image2video/video-synthesis`） | `POST /api/v1/services/aigc/video-generation/3d-generation` |
| 轮询端点 | `GET /api/v1/tasks/{task_id}`（异步时） | `GET /api/v1/tasks/{task_id}` | `GET /api/v1/tasks/{task_id}` |
| 异步头要求 | [异步调用](../concepts/async-invocation.md)必带 `X-DashScope-Async: enable` | 必带 `X-DashScope-Async: enable` | 必带 `X-DashScope-Async: enable` |
| 典型耗时 | 同步秒级；异步 1–2 分钟 | 1–5 分钟（万相2.1 编辑 5–10 分钟） | 较长，建议轮询间隔约 15 秒 |
| task_id 有效期 | 24 小时 | 24 小时 | 24 小时 |
| 产物下载链接有效期 | — | 见对应模型文档 | 2 小时 |
| 地域可用性 | 华北2/新加坡/美国弗吉尼亚等多地域，地域间独立 Key；千问图像翻译仅华北2 | 华北2（北京）为主，部分模型支持新加坡/弗吉尼亚/法兰克福 | 仅华北2（北京） |
| 专属域名 | `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` / `.ap-southeast-1.maas.aliyuncs.com` | 同左（按地域） | 走 dashscope 默认域名 |
| 开通前置 | 千问/万相默认可用；可灵需控制台搜索「可灵」开通 | 万相默认；PixVerse/Vidu 需控制台开通 | 需控制台搜索「Tripo」开通并授权 |
| 输出规格控制 | 自由宽高/总像素范围、1–6 张、可指定分辨率 | 视频时长/分辨率/帧率因模型而异 | 面数（最高 200 万/2 万）、贴图质量（标清/高清）、是否 PBR |
| 计费关注 | 按张或按次；部分老模型仅免费体验额度（用尽不可付费） | 按次/时长；不同模型差异大 | 按任务类型（text/image/multi-image-to-3d）计数 |
| 典型场景 | 文生图、图生图、图像编辑、翻译、虚拟模特、试衣、海报、扩图、擦除补全 | 文生视频、图生视频、首尾帧、参考生视频、视频编辑、换人、数字人、动作生成 | 文生 3D、单图生 3D、多图生 3D、PBR 资产、无贴图基础模型 |

## 调用模式与共性约定

三者均通过 DashScope HTTP 接口调用，统一使用百炼 [API Key](../concepts/api-key.md) 鉴权，并遵循「模型/Endpoint/Key 必须同地域」的约束。[异步调用](../concepts/async-invocation.md)（视频、3D 全部，图像部分）都要求带 `X-DashScope-Async: enable`，缺少该头会报错 `current user api does not support synchronous calls`；任务创建后拿到 `task_id`（24 小时有效），**请勿重复创建任务**，直接轮询 `GET /api/v1/tasks/{task_id}` 即可。

差异点在于：图像生成的新版模型（千问 image 2.0 系列、万相 2.6/2.7、Z-Image）支持同步一次返回，流程最简；视频与 3D 因耗时较长，统一异步。3D 额外要求轮询间隔约 15 秒、查询 RPS 默认 20，高频需求建议走异步任务回调。

## 适用场景建议

- **选图像生成**：目标是静态画面——营销海报、虚拟模特/试衣、图文混排、复杂文字渲染（千问图像系列擅长）、风格重绘、图像编辑（增删物体、改动作、迁移风格）。需要秒级返回或对单张画面质量要求高时，优先千问 image 2.0-pro/max 与万相 2.7。
- **选视频生成**：目标是动态内容——文生/图生短视频、首尾帧续写、参考生视频（保持角色/音色一致）、视频编辑、数字人/换人/动作生成。可灵/万相 HappyHorse/2.7 适合高质量叙事，PixVerse/Vidu 适合华北2地域内的多模态参考生成。
- **选 3D 生成**：目标是可交互的三维资产——游戏/电商/工业设计的 GLB 模型，需要 PBR 材质或多视角重建。Tripo-H3.1 适合高精度（最高 200 万面），Tripo-P1.0 适合快速产出（最高 2 万面）。

## 技术选型参考

1. **按产出形态定大类**：静态图 → 图像 API；动态视频 → 视频 API；可旋转/导入引擎的 3D 资产 → 3D API。三者产出不互通，选型先定形态。
2. **按地域定模型池**：华北2（北京）模型最全（含图像翻译、PixVerse、Vidu、Tripo）；新加坡/弗吉尼亚/法兰克福仅支持部分图像与视频模型；3D 仅限华北2。跨地域 Key 不可混用。
3. **按调用复杂度定架构**：图像同步模型可一次返回，适合低延迟交互；视频/3D 必须异步 + 轮询（或回调），后端需设计任务状态机与产物下载（注意 3D 链接仅 2 小时有效）。
4. **按成本与额度定模型**：图像中部分老模型（局部重绘、虚拟模特、试衣、海报、实例分割、擦除补全等）仅提供免费体验额度，用尽不可付费，官方推荐迁移到千问/万相 2.1 编辑；视频与 3D 按任务计费，高精度 3D（H3.1 ultra）成本高于快速版（P1.0）。
5. **按输入素材定子能力**：有首帧/首尾帧选图生视频；有多视角图选多图生 3D（前/左/后/右固定 4 槽，2–4 张有效）；需保持角色一致选万相 2.7 参考生或可灵参考图生图。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


