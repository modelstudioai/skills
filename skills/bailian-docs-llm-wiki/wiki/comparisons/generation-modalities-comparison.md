# 图像、视频与3D生成对比

百炼平台把图像、视频、3D 三类生成能力统一收口在模型推理网关下，使用相同的 `Authorization: Bearer <API_KEY>` 鉴权与 JSON 承载的输入输出协议，但三者在输入模态、输出形态、调用模式、耗时、计费维度与典型场景上差异显著。本文面向需要做多模态生成技术选型的开发者，横向对比三类能力的关键维度，帮助快速锁定适合业务的接口族。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
| --- | --- | --- | --- |
| 输入格式 | 文本 [prompt](../guides/prompt.md)；参考图/蒙版（URL 或 Base64） | 文本；首帧/首尾帧图像；参考多图；视频；音频 | 文本 [prompt](../guides/prompt.md)（≤1024 字符）；单图 URL；多图（前/左/后/右 4 视角，固定数组） |
| 输出格式 | 单张或多张静态图像（临时 URL） | 视频文件（临时 URL） | GLB 模型（PBR 材质或无贴图基础模型）+ 预览渲染图 |
| 支持模型族 | 通义千问图像、万相（Wan）、Z-Image、可灵、创意工具系列 | 万相（HappyHorse/Wan/wanx）、爱诗 PixVerse、Vidu、可灵 | Tripo（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`） |
| API 端点 | OpenAI 兼容 `/compatible-mode/v1/images/generations`；或 DashScope 原生 `/services/aigc/text2image/image-synthesis` | `/services/aigc/video-generation/video-synthesis`（万相2.7 等）；或 `/services/aigc/image2video/video-synthesis`（动作/换人/数字人/旧版首尾帧） | `/services/aigc/video-generation/3d-generation` |
| 调用模式 | 同步（兼容模式）或异步轮询（万相/创意工具，返回 task_id） | 全部异步：创建任务得 task_id → 轮询 `GET /tasks/{task_id}` | 全部异步：创建任务得 task_id → 轮询 `GET /tasks/{task_id}` |
| 必要请求头 | `Authorization`；异步任务需 `X-DashScope-Async: enable` | `Authorization`、`Content-Type: application/json`、`X-DashScope-Async: enable`（缺异步头报 `does not support synchronous calls`） | `Authorization`、`X-DashScope-Async: enable` |
| 典型耗时 | 秒级（同步）到数十秒（异步） | 1–5 分钟；视频编辑 5–10 分钟 | 较长，轮询建议间隔约 15 秒 |
| task_id 有效期 | 异步任务 24 小时 | 24 小时 | 24 小时；超时返回 `UNKNOWN` |
| 产物下载链接有效期 | 临时 URL，需及时下载/转存 OSS | 临时 URL | 2 小时 |
| 地域约束 | 各地域通用，按模型开通 | 模型/Endpoint/API Key 须同地域；PixVerse、Vidu 仅华北2（北京） | 仅华北2（北京），且须用北京 API Key |
| 内容安全 | 内置审核，违规返回 `DataInspectionFailed` | 内置审核 | 内置审核，失败返回 `code`/`message` |
| 计费方式 | 按张/按次（视模型） | 按任务/时长 | 按任务类型（`text-to-3d` / `image-to-3d` / `multi-image-to-3d`）计数，`usage` 含生成数量 |
| 典型场景 | 文生图、图像编辑、电商/营销垂类、人像玩法、艺术文字 | 文生视频、图生视频、视频编辑、数字人、肖像动态、风格重绘 | 文生 3D、单图生 3D、多图生 3D，产出可二次加工的 GLB 资产 |

## 调用模式差异

图像生成是三类中唯一支持**同步调用**的：千问-文生图等可走 OpenAI 兼容 `images/generations` 直接拿结果。万相与创意工具则多用 DashScope 原生异步协议，提交后拿 `task_id` 轮询。

视频与 3D 一律异步，且都强制 `X-DashScope-Async: enable` 头。视频接口明确要求"同地域"约束（模型、Endpoint、API Key 必须同地域），3D 则更严格——仅华北2（北京）可用。两者都强调"请勿重复创建任务，直接轮询"。

## 输入模态对比

- **图像生成**：以文本 [prompt](../guides/prompt.md) 为主，部分编辑接口接受参考图与蒙版，输入图支持公网 URL 或 Base64。
- **视频生成**：多模态输入最丰富，万相2.7 支持文本/图像/音频/视频混合输入，参考生视频可保持角色与音色一致性；首尾帧、参考多图等模式扩展了可控性。
- **3D 生成**：`prompt`、`image`、`images` 三者互斥。多图模式视角顺序固定为前/左/后/右，数组长度固定 4，不需要的视角传空对象 `{}`，这是 3D 独有的约束。

## 输出与产物处理

图像与视频输出都是临时 URL，文档建议及时下载或转存 OSS。3D 输出更结构化：根据 `pbr`/`texture` 参数组合返回 `pbr_model_url`（PBR 材质 GLB）或 `base_model_url`（无贴图基础模型），并附 `rendered_image_url` 预览图，链接有效期仅 2 小时，短于图像/视频的临时 URL 生命周期。

## 选型建议

- **静态视觉物料（海报、商品图、人像）**：选图像生成。中文语义优先千问-文生图或万相-文生图 V2；按指令改图用万相-图像生成与编辑 2.7；电商/营销垂类用虚拟模特、AI 试衣、创意海报；高美感/艺术风格用 Z-Image 或可灵。
- **动态视频内容（短剧、营销视频、数字人播报）**：选视频生成。通用文生/图生优先万相2.7（`wan2.7-t2v`/`wan2.7-i2v`）；多镜头叙事用万相2.6 `shot_type: multi`；数字人/换人用 `wan2.2-s2v`、`wan2.2-animate-mix`；北京地域可按需选 PixVerse、Vidu。
- **可复用 3D 资产（游戏、电商 3D 展示、工业建模）**：选 3D 生成，仅限北京地域。高精度需求用 `Tripo/Tripo-H3.1`（最高 200 万面，`geometry_quality: ultra`）；追求速度用 `Tripo/Tripo-P1.0`（最高 2 万面）。需要 PBR 材质保留默认 `pbr: true`，仅需白模则同时关 `texture` 与 `pbr`。
- **跨模态组合**：可先用图像生成产出关键帧，再喂给视频生成的图生/首尾帧接口生成动态内容；3D 则更适合独立资产管线，与图像/视频管线并行而非串行。

新接入一律优先最新版本（万相 2.7、通用图像编辑 2.5、wan2.7、Tripo-H3.1/P1.0），旧版接口保留兼容但不再增强。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


