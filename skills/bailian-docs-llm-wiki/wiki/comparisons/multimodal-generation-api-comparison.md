# [多模态](../concepts/multimodal.md)生成 API 对比（图像/视频/3D）

百炼平台提供图像、视频、3D 三类[多模态](../concepts/multimodal.md)生成 API，分别面向不同的内容产出形态。三者都通过 DashScope HTTP 接口调用，统一使用 API Key 鉴权，并遵循"创建任务 → 轮询结果"的异步任务模式（部分图像模型支持同步调用）。本页从输入格式、输出格式、支持模型、API 端点、调用模式、[计费](../concepts/billing.md)与典型场景等维度做横向对比，帮助开发者根据产出目标与技术约束做选型。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
| --- | --- | --- | --- |
| 产出形态 | 静态图片（PNG） | 视频文件 | GLB 模型 + 预览渲染图 |
| 输入格式 | 文本、图像（图生图/编辑）、参考图 | 文本、图像（首帧/首尾帧）、参考图、视频、音频 | 文本、单图、多图（前/左/后/右 4 视角，固定数组长度 4） |
| 输出格式 | PNG，1–6 张或多图组图 | 视频 URL | PBR 材质 GLB（`pbr_model_url`）或无贴图基础模型（`base_model_url`），含 1 张预览渲染图 |
| 调用模式 | 同步（千问/万相2.6+/Z-Image 等新版）或异步（V1 及部分编辑/创意类） | 仅异步 | 仅异步 |
| API 端点 | 同步：`POST /api/v1/services/aigc/multimodal-generation/generation`；异步轮询：`GET /api/v1/tasks/{task_id}` | `POST /api/v1/services/aigc/video-generation/video-synthesis`（部分走 `image2video/video-synthesis`）；轮询：`GET /api/v1/tasks/{task_id}` | `POST /api/v1/services/aigc/video-generation/3d-generation`；轮询：`GET /api/v1/tasks/{task_id}` |
| 必需请求头 | `Authorization`；异步需 `X-DashScope-Async: enable` | `Content-Type`、`Authorization`、`X-DashScope-Async: enable` | `X-DashScope-Async: enable`（缺少报 `current user api does not support synchronous calls`） |
| 典型耗时 | 同步秒级返回；异步 1–2 分钟 | 1–5 分钟，万相2.1 视频编辑 5–10 分钟 | 较长，轮询建议间隔约 15 秒 |
| task_id 有效期 | 24 小时 | 24 小时 | 24 小时，超时返回 `UNKNOWN` |
| 产物下载链接有效期 | 随接口返回 | 随接口返回 | 2 小时，需及时下载 |
| 支持模型系列 | 千问图像、万相（Wan/wanx）、Z-Image、可灵 | 万相（HappyHorse/Wan/wanx）、爱诗 PixVerse、Vidu、可灵 | Tripo（`Tripo/Tripo-H3.1` 高精度、`Tripo/Tripo-P1.0` 专业快速） |
| 地域可用性 | 北京/新加坡/弗吉尼亚等多地域，地域独立鉴权不可混用；千问-图像翻译仅北京 | 同地域约束，模型/Endpoint/API Key 必须同地域；PixVerse、Vidu 仅北京 | 仅华北2（北京） |
| 业务空间专属域名 | 支持（`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` 等） | 支持（北京 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等） | 走默认 dashscope 域名 |
| SDK 支持 | 部分模型支持 DashScope SDK（Python/Java） | HTTP 为主 | HTTP |
| [计费](../concepts/billing.md)方式 | 按张数/模型[计费](../concepts/billing.md) | 按任务/时长计费 | 按任务计费（`usage` 记录任务类型与生成数量） |
| 典型场景 | 文生图、图生图、图像编辑、虚拟模特、试衣、海报、背景生成、擦除补全、画面扩展、人物写真 | 文生视频、图生视频、参考生视频、视频编辑、视频换人、数字人、肖像动态视频 | 文生 3D、单图生 3D、多图生 3D，游戏/电商/工业设计资产 |

## 调用模式差异

三类 API 在调用流程上高度一致，均采用"创建任务 → 轮询查询"模式，但图像 API 额外提供**同步调用**能力：

- **图像生成**：千问图像系列（qwen-image-2.0-pro/max/plus）、万相 2.6/2.7 文生图与编辑、Z-Image 等新版模型支持一次请求即返回结果的同步调用，走 `multimodal-generation/generation` 端点；V1 版及部分编辑/创意类模型仍需异步。同步模式流程更简单，适合交互式场景。
- **视频生成 / 3D 生成**：因耗时较长（视频 1–10 分钟，3D 资产更久），统一仅支持异步。请求必须携带 `X-DashScope-Async: enable`，缺少该头会报错 `current user api does not support synchronous calls`。

三者都强调"请勿重复创建任务"，`task_id` 有效期 24 小时，直接轮询即可。

## 输入能力对比

| 输入方式 | 图像 | 视频 | 3D |
| --- | --- | --- | --- |
| 纯文本 | 支持，复杂文字渲染能力强（千问系列） | 支持（文生视频） | 支持，中英文等多语言，最大 1024 字符 |
| 单图输入 | 支持（图生图、图像编辑） | 支持（首帧生视频） | 支持，JPEG/PNG，宽高 [20,6000]，≤20MB |
| 多图输入 | 部分编辑模型支持多图输入/输出 | 支持（参考生、首尾帧） | 支持，固定 4 视角（前/左/后/右），有效 2–4 张 |
| 视频输入 | 不适用 | 支持（视频编辑、参考生视频） | 不适用 |
| 音频输入 | 不适用 | 万相2.7 支持[多模态](../concepts/multimodal.md)输入含音频 | 不适用 |

3D 生成的多图输入有严格的视角顺序约束（前/左/后/右），不需要的视角传空对象 `{}`，这与图像/视频的"多图作为参考"语义不同。

## 产物与质量参数

| 项 | 图像 | 视频 | 3D |
| --- | --- | --- | --- |
| 输出规格 | 总像素 512×512~2048×2048，宽高比 1:4~4:1，1–6 张；万相2.7 支持 4K | 视频文件 URL | 面数：H3.1 最高 200 万面，P1.0 最高 2 万面 |
| 质量参数 | 分辨率、张数、宽高比 | 分辨率、时长、镜头叙事（`shot_type: multi`） | `texture_quality`（标清/高清）、`geometry_quality`（standard/ultra）、`pbr`、`texture` |
| 一致性能力 | 千问编辑支持角色一致性 | 万相2.7 参考生支持角色形象与音色一致性 | 多图视角约束保证几何一致性 |
| 预览能力 | 直接返回图片 | 直接返回视频 | 额外返回 `rendered_image_url` 预览渲染图 |

## 适用场景建议

- **选图像生成 API**：需要静态视觉产出，强调文字渲染、风格化、精确编辑（增删移动物体、改动作）、虚拟模特/试衣/海报等电商与营销场景。优先用同步调用模型（千问图像、万相2.6+/2.7、Z-Image）以简化流程；批量或创意类任务再用异步。
- **选视频生成 API**：需要动态叙事、数字人、肖像动态视频、视频编辑/换人。文生视频、图生视频（首帧/首尾帧）、参考生视频均可，万相2.7 是推荐的新版协议，支持多模态输入与角色/音色一致性。注意 PixVerse、Vidu 仅北京地域可用且需单独开通。
- **选 3D 生成 API**：需要可直接导入引擎/3D 软件的 GLB 资产，适用于游戏、电商商品 3D 展示、工业设计。仅北京地域可用，需开通 Tripo。高精度选 `Tripo/Tripo-H3.1`（最高 200 万面），追求速度选 `Tripo/Tripo-P1.0`。

## 技术选型参考

1. **产出形态决定大类**：图片→图像 API；视频→视频 API；3D 模型→3D API。三者端点不同，不可混用。
2. **延迟敏感优先同步**：仅图像 API 提供同步调用，适合交互式产品；视频与 3D 必须异步，需在业务侧实现轮询或配置异步任务回调（3D 查询接口默认 RPS 20）。
3. **地域与鉴权**：三类均要求模型、Endpoint、API Key 同地域。3D 仅北京可用；千问-图像翻译、PixVerse、Vidu 也仅北京。建议迁移到业务空间专属域名以获得更好性能与稳定性。
4. **任务复用**：`task_id` 24 小时有效，三类都要求轮询而非重复创建任务；3D 产物下载链接仅 2 小时，需及时落盘。
5. **输入约束**：3D 多图必须按前/左/后/右 4 视角顺序；图像图文混排需开启 `enable_interleave=true` 并配合 SSE 流式；视频首尾帧、参考生有专属模型变体。
6. **模型开通**：可灵、PixVerse、Vidu、Tripo 均需先在控制台搜索并开通授权，再调用 API。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


