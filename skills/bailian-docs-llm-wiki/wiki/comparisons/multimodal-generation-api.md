# [多模态](../concepts/multimodal.md)生成 API 对比

百炼平台提供图像、3D 和视频三类[多模态](../concepts/multimodal.md)生成能力，均通过 DashScope 网关以 REST / SDK 方式调用。三者共享「异步创建任务 → 轮询 task_id」的基础调用模式，但在输入模态、输出产物、支持模型矩阵、地域限制和计费粒度上存在显著差异。本页旨在帮助开发者快速理解三者的技术边界，为方案选型提供参考。

## 关键维度对比

| 对比维度 | 图像生成（Image Generation） | 3D 生成（3D Generation） | 视频生成（Video Generation） |
| --- | --- | --- | --- |
| **输入格式** | 文本提示词；参考图（图生图 / 图像编辑）；多图参考（部分模型支持最多 14 张） | `prompt`（文生 3D，≤1024 字符）；`image`（单图生 3D）；`images`（多图生 3D，固定 4 视角：前/左/后/右） | `prompt` 文本；`media` [多模态](../concepts/multimodal.md)数组（首帧/尾帧/参考图/视频/音频）；旧版协议直接 URL 字段 |
| **输出格式** | 单张或多张图像（1~6 张），JPEG/PNG 格式 | PBR 材质 GLB 模型或无贴图基础 GLB 模型 + 预览渲染图 | 视频文件，支持 480P~4K 分辨率，时长常见 5/8 秒，部分模型可生成音频 |
| **支持模型** | Qwen-Image / Qwen-Image-Edit、万相 wan2.7/wan2.6/wan2.5/wanx-v1、Z-Image、Kling、Vidu 等多家系列 + 多项创意工具 | Tripo-H3.1（高精度，最高 200 万面）、Tripo-P1.0（专业，速度更快，最高 2 万面） | 万相 wan2.7/wan2.6/早期版本、HappyHorse、PixVerse、Vidu、Kling、人像动画系列、万相动作/换人/数字人 |
| **API 端点** | 各模型独立端点，多数为异步 `X-DashScope-Async: enable`；wan2.6/2.7/z-image/qwen-image 部分支持 HTTP 同步调用 | `POST /api/v1/services/aigc/video-generation/3d-generation`（创建）+ `GET /api/v1/tasks/{task_id}`（轮询），**仅异步** | `POST /api/v1/services/aigc/video-generation/video-synthesis`（创建）+ `GET /api/v1/tasks/{task_id}`（轮询），**仅异步**；部分模型用 `image2video/video-synthesis` 路径 |
| **地域限制** | 多数模型多地可用；部分创意工具（图像翻译、涂鸦作画、虚拟模特等）为北京地域独占 | **仅限华北2（北京）**，必须使用北京地域 [API Key](../concepts/api-key.md) | 需模型/Endpoint URL/[API Key](../concepts/api-key.md) 同一地域；北京/新加坡/美国/德国多地域支持，跨地域调用失败 |
| **调用模式** | 异步为主，部分支持同步 | 纯异步（`X-DashScope-Async: enable` 必选） | 纯异步（`X-DashScope-Async: enable` 必选） |
| **轮询间隔建议** | 取决于具体模型，多数秒级完成 | 约 15 秒，查询接口默认 RPS 20 | 取决于模型和时长，任务有效期 24 小时 |
| **产物有效期** | 视具体接口而定 | 下载链接有效期 **2 小时** | 下载链接有效期视具体接口而定 |
| **典型场景** | 营销素材、创意海报、虚拟模特、图像编辑、翻译、局部重绘 | 游戏资产、电商 3D 展示、工业设计原型 | 短视频创作、广告视频、数字人播报、视频编辑、对口型/动作模仿 |

## 调用模式对比

| 特性 | 图像生成 | 3D 生成 | 视频生成 |
| --- | --- | --- | --- |
| 同步调用 | 部分支持（wan2.6/2.7、z-image、qwen-image 等） | 不支持 | 不支持 |
| 异步创建 + 轮询 | 大多数模型 | 唯一方式 | 唯一方式 |
| `X-DashScope-Async` 必选 | 仅异步模型 | 必选 | 必选 |
| task_id 有效期 | 视接口而定 | 24 小时 | 24 小时 |

## 输入灵活性对比

| 能力 | 图像生成 | 3D 生成 | 视频生成 |
| --- | --- | --- | --- |
| 纯文本输入 | 支持 | 支持（≤1024 字符） | 支持 |
| 单图输入 | 支持（图生图 / 图像编辑） | 支持（单图生 3D，JPEG/PNG，≤20MB） | 支持（首帧 / 尾帧） |
| 多图输入 | 支持（最多 14 张参考图，Vidu 等） | 支持（固定 4 视角：前/左/后/右） | 支持（多参考图、首尾帧组合） |
| 视频输入 | 不支持 | 不支持 | 支持（部分模型接收视频 URL 作为输入） |
| 音频输入 | 不支持 | 不支持 | 支持（数字人、对口型等模型） |
| 多输出 | 支持（1~6 张） | 支持（PBR 模型 + 渲染图） | 单个视频文件 |

## 适用场景建议

- **图像生成**：适合需要快速产出高质量静态视觉内容的场景，如电商商品图、营销海报、虚拟模特展示、图像编辑与翻译。当需要文本渲染能力强（Qwen-Image）、高性价比批量出图（Z-Image Turbo）、或多图参考融合（Kling / Vidu）时优先选用。部分创意工具（涂鸦作画、局部重绘、人像风格重绘）适合特定创意需求。
- **3D 生成**：适合需要将文本或少量参考图转化为可直接使用的 3D 模型资产的场景，如游戏道具、电商 3D 展示、工业设计快速原型。**仅限北京地域**，需提前开通 Tripo 服务。追求精度选 Tripo-H3.1（可设 `ultra` 几何精度，最高 200 万面），追求速度选 Tripo-P1.0。
- **视频生成**：适合需要动态视觉内容的场景，如短视频创作、广告视频、数字人播报与口型同步。万相 wan2.7 为新版协议首选（支持多主体参考生视频 + 音色），需要 4K 超清或动作模仿选 PixVerse，需要智能分镜或首尾帧控制选 Kling。人像动画系列（animate-anyone / emo / liveportrait）适合舞蹈、唱演、播报等人物驱动场景。

## 选型决策流程

1. **确定输出模态**：静态图像 → 图像生成；3D 模型 → 3D 生成；动态视频 → 视频生成。
2. **确认地域**：3D 生成仅限北京；视频生成需确保模型/Endpoint/[API Key](../concepts/api-key.md) 同地域；图像生成多数多地可用但部分创意工具限北京。
3. **评估输入素材**：是否有参考图、多视角图、首尾帧或音视频素材，据此筛选支持的模型。
4. **权衡同步/异步**：如需快速同步响应，图像生成中的 wan2.6/2.7、z-image、qwen-image 系列支持 HTTP 同步；3D 和视频生成均为异步，需规划轮询或回调机制。
5. **关注产物有效期**：3D 生成下载链接仅 2 小时有效，视频和图像产物有效期视接口而定，均需及时下载。

## 来源文档

- [image generation](../api/image-generation.md)（api/image-generation.md）
- [3d generation](../api/3d-generation.md)（api/3d-generation.md）
- [video generation api](../api/video-generation-api.md)（api/video-generation-api.md）

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


