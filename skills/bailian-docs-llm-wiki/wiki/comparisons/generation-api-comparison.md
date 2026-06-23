# 多模态生成 API 对比：图像、视频与 3D

百炼平台将图像、视频、3D 三类多模态生成能力统一沉淀在 DashScope 异步任务框架下，但三者面向的创作对象、输入素材、输出格式、典型耗时与适用场景差异显著。本页围绕开发者最关心的接入方式、模型族、请求结构、地域限制、计费与结果获取等维度做横向对比，帮助你在文生图、文生视频与文生 3D 之间做出快速选型决策。

## 关键维度对比

| 维度 | 图像生成 API | 视频生成 API | 3D 生成 API |
|------|--------------|--------------|-------------|
| 创作对象 | 静态 2D 图像 | 时序视频帧 | 可旋转/可导出的 3D 模型 |
| 主要模型族 | 千问 Qwen-Image、万相 Wan/Wanx、Z-Image、可灵 Kling | 万相 wan2.7 / legacy、HappyHorse、可灵、爱诗 PixVerse、Vidu、人像动画类 | Tripo（`Tripo-H3.1`、`Tripo-P1.0`） |
| 输入方式 | 文本 [prompt](../guides/prompt.md)（必选），可选参考图、掩码、多图 | 文本 [prompt](../guides/prompt.md) + 媒体 URL（首帧/首尾帧/参考图/参考视频/音频） | 三选一且互斥：`prompt`（文生 3D）、`image`（单图生 3D）、`images`（多图生 3D，固定 4 视角） |
| 输出格式 | PNG/JPG 图像 URL，可批量返回 1–4 张 | 视频文件 URL | GLB 格式 3D 模型（PBR 或无贴图） + 预览渲染图 |
| 创建任务 Endpoint | `/services/aigc/text2image/image-synthesis`、`/services/aigc/multimodal-generation/generation`、`/services/aigc/image2image/image-synthesis`（路径因模型而异） | `/services/aigc/video-generation/video-synthesis`（部分人像动画走 `/services/aigc/image2video/video-synthesis`） | `/services/aigc/video-generation/3d-generation` |
| 查询任务 Endpoint | `GET /api/v1/tasks/{task_id}` | `GET /api/v1/tasks/{task_id}` | `GET /api/v1/tasks/{task_id}` |
| 调用模式 | 异步，`X-DashScope-Async: enable` 必选 | 异步，`X-DashScope-Async: enable` 必选 | 异步，`X-DashScope-Async: enable` 必选，缺失会报同步调用错误 |
| 典型耗时 | 秒级（Z-Image turbo 更快） | 1–5 分钟，长视频更久 | 较长，建议轮询间隔 15 秒 |
| `task_id` 有效期 | 24 小时 | 24 小时，过期返回 `UNKNOWN` | 24 小时，过期返回 `UNKNOWN` |
| 结果下载有效期 | 图像 URL 需及时下载 | 视频 URL 需及时下载 | 下载链接有效期仅 2 小时 |
| 地域支持 | 多数模型北京；千问文生图、万相 V2、Z-Image 支持新加坡 | 北京、新加坡、美国（弗吉尼亚）、德国（法兰克福）；可灵、风格重绘限北京 | 仅"中国内地（北京）"地域 |
| 关键差异化参数 | `size`、`n`、`negative_prompt`、`seed` | `resolution`、`ratio`、`duration`、`prompt_extend`、`watermark`；可灵用 `mode`/`aspect_ratio` | `texture_quality`、`geometry_quality`、`pbr`、`texture` |
| 计费方式 | 按生成图像张数/模型计费，部分创意工具仅免费体验额度 | 按视频时长（秒）与模型计费 | 按模型与精度档位计费 |

## 三类 API 的共同点

1. **统一异步两段式**：三类 API 均要求 `X-DashScope-Async: enable`，先 POST 创建任务拿到 `task_id`，再 GET 轮询同一 `/api/v1/tasks/{task_id}` 查询结果。
2. **同一鉴权**：请求头 `Authorization: Bearer $DASHSCOPE_API_KEY`，API Key 必须与目标地域一致。
3. **请求体三段式**：`{"model", "input", "parameters"}` 结构统一，但字段命名（如 `media` vs `image_url` vs `images`）因模型族而异，需以各模型 API 文档为准。
4. **不要重复创建任务**：`task_id` 24 小时内可重复查询，重复提交任务会浪费配额并可能触发限流。

## 三类 API 的差异点

- **输入维度**：图像生成以文本为主、可选少量参考图；视频生成强调多模态时序输入（首帧/尾帧/参考视频/音频）；3D 生成则在"文本/单图/多视角图"三种输入间互斥，多图模式还要求固定 4 视角顺序（前/左/后/右），未用到的视角需传空对象 `{}`。
- **输出产物**：图像是 2D 像素文件；视频是时序帧序列；3D 是带拓扑与贴图的 GLB 模型，可选择 PBR 材质或无贴图基础模型，且额外提供预览渲染图。
- **Endpoint 路径**：图像与视频的创建路径分布最杂，需按模型族区分；3D 则固定为 `/services/aigc/video-generation/3d-generation`。
- **地域收敛度**：3D 最严格（仅北京）；图像次之（部分模型支持新加坡）；视频覆盖最广（四地域），但可灵、风格重绘等仍限北京。
- **结果时效**：3D 下载链接仅 2 小时，明显短于图像/视频，对落盘与转存要求更紧迫。
- **参数体系**：图像侧重输出控制（尺寸、张数、反向提示词、种子）；视频侧重时序与画面控制（分辨率、宽高比、时长、水印、分镜）；3D 侧重模型质量档位（贴图质量、几何精度、PBR 开关）。

## 适用场景建议

### 图像生成 API

- **首选**：营销海报、电商主图、插画素材、虚拟试衣、风格迁移、图中文字翻译等**静态视觉产出**场景。
- **选型提示**：追求复杂文本渲染与多行布局选千问 `qwen-image-2.0-pro`；追求 4K 高清与多图参考选万相 `wan2.7-image-pro`；追求速度与性价比选 `z-image-turbo`；虚拟试衣/人像风格化等垂类工具按场景匹配，注意部分仅免费体验额度。
- **慎用**：需要可交互、可旋转或可导出到 3D 引擎的资产——请走 3D 生成。

### 视频生成 API

- **首选**：广告短视频、影视分镜、数字人播报、唱演动画、视频风格迁移、参考生视频等**时序动态内容**场景。
- **选型提示**：新项目优先选万相 2.7 新版协议（多模态输入、指令编辑、视频续写）；追求物理真实与运动流畅选 HappyHorse；需要智能分镜与首尾帧控制选可灵；海外/多地域部署优先 HappyHorse（四地域支持）。
- **注意**：任务耗时 1–5 分钟，前端需做好轮询与超时兜底；可灵、风格重绘限北京地域，海外项目需回避。

### 3D 生成 API

- **首选**：游戏资产、电商 3D 展示、AR/VR 内容、工业建模预演等**需要可旋转/可导出 3D 模型**的场景。
- **选型提示**：追求高精度（最高 200 万面）选 `Tripo/Tripo-H3.1`，可开启 `geometry_quality=ultra`；追求速度与轻量（最高 2 万面）选 `Tripo/Tripo-P1.0`。
- **注意**：仅北京地域可用，使用前需在控制台开通 Tripo 服务；下载链接仅 2 小时，务必及时落盘；多图模式必须按前/左/后/右顺序传足 4 视角。

## 技术选型决策建议

1. **产物形态决定主路径**：先确定你需要 2D 静态图、时序视频，还是可导出 3D 模型，三类 API 不可互相替代。
2. **地域优先**：海外或多地域业务回避 3D 与可灵图像/视频，优先选 HappyHorse 等多地域模型族。
3. **新项目首选新版协议**：图像选万相 2.7 / 千问 2.0 系列，视频选万相 2.7 新版协议，避免使用仅免费体验或已推荐迁移的 legacy 模型。
4. **统一接入层**：三类 API 共享同一查询接口与鉴权方式，可在客户端封装统一的"创建任务 → 轮询 → 下载"调度器，按 `model` 字段路由到不同创建 Endpoint。
5. **结果转存**：所有产物 URL 均有时效（3D 最短仅 2 小时），生产环境应配置 OSS/对象存储转存，避免链接过期。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


