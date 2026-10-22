# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文档系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心AIGC能力。对比聚焦于**工程落地关键维度**，涵盖调用方式、模型生态、输入输出约束、计费逻辑及适用场景，旨在为技术选型提供客观、可操作的决策依据。

---

## 关键能力维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **核心定位** | 静态视觉内容生成与编辑 | 动态时序内容生成与操控 | 空间结构建模与几何重建 |
| **输入格式** | 文本（`prompt`）、Base64 或公网 URL 图像（图生图/局部重绘）、可选 `mask` | 文本、单帧/首尾帧图像 URL、参考视频 URL、音频 URL、TTS 内容；支持多模态组合输入 | 文本（`prompt`）、单张图像 URL（单图生3D）、或严格顺序的 2–4 张视角图 URL（前/左/后/右） |
| **输出格式** | Base64 编码图像或临时下载 URL（有效期 1 小时），返回 `data: [{ "url": "...", "b64_json": "..." }]` | 异步返回 `output.video_url`（MP4/H.264，有效期 24 小时）；部分模型额外返回预览图、关键帧序列 | 异步返回 `results` 数组，含 `pbr_model_url`（GLB + PBR 材质）、`base_model_url`（无贴图 GLB）、`rendered_image_url`（渲染预览图）；所有 URL 有效期 2 小时 |
| **支持模型（代表性）** | `wanx-v1`（万相）、`kling-v2`（可灵）、`zimage-pro`（Z-Image）、`vidu/viduq3-pro_image_generation`（Vidu 图像模式） | `wan3.0-video-generation`（万相3.0）、`kling-v3-omni-video-generation`（可灵）、`pixverse/pixverse-v6-t2v`（爱诗）、`videoretalk`（口型替换） | `Tripo/Tripo-H3.1`（高精度）、`Tripo/Tripo-P1.0`（轻量快速） |
| **API 端点** | 同步 RESTful：`POST /v1/images/generations` | [异步任务](../concepts/asynchronous-task.md)式：`POST {WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` | [异步任务](../concepts/asynchronous-task.md)式：`POST {WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`（仅华北2北京） |
| **调用模式** | **同步响应**（典型耗时 1–8 秒），请求即得结果 | **强制异步**（创建任务 + 轮询查询），任务生命周期 ≤24 小时；需处理 `task_id` 状态轮询 | **强制异步**（创建任务 + 轮询查询），任务生命周期 ≤24 小时；轮询间隔建议 ≥15 秒 |
| **地域约束** | 无强绑定，支持多地域通用 API 域名（如 `dashscope.aliyuncs.com`） | **强地域绑定**：模型、Endpoint、API Key 必须同属一个地域（如 `cn-beijing`）；推荐使用 Workspace 专属域名 | **强地域锁定**：**仅支持华北2（北京）地域**；Endpoint 固定为 `cn-beijing.maas.aliyuncs.com` |
| **计费方式** | 按**成功请求数**计费（例：1 次请求生成 4 张图 = 4 次计费）；部分模型含免费额度 | 按**任务次数**或**视频秒数**计费（如 `videoretalk` 0.08 元/秒）；多数模型含基础免费额度 | 按**成功任务数**计费（无论输出面数或质量等级）；`Tripo-H3.1` 与 `Tripo-P1.0` 单价不同，详见控制台定价页 |
| **典型延迟** | 低延迟（<5s）：适合实时交互场景（如设计工具即时预览） | 中高延迟（30s–10min+）：取决于视频长度、分辨率与模型负载（如 4K 30 秒视频常需 3–5 分钟） | 高延迟（2–15 分钟）：受几何复杂度影响显著（`H3.1-ultra` 通常 >8 分钟） |
| **关键限制** | • `prompt` ≤500 字符<br>• `size` 必须为模型明确支持的尺寸组合（如 `1024x1536`）<br>• Z-Image 不支持 `negative_prompt` | • 输入媒体 URL 必须公网可访问；OSS URL 需加 `X-DashScope-OssResourceResolve: enable`<br>• `wan2.6` 及更早模型与 `wan2.7+` 参数协议不兼容<br>• 并发任务数受账号等级限制 | • `prompt`/`image`/`images` 三者**严格互斥**<br>• 多图输入必须按 `[前, 左, 后, 右]` 顺序，缺位填 `{}`<br>• `task_id` 与结果 URL 时效性要求高（24h / 2h） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「轻量、高频、实时反馈」场景  
- **推荐场景**：电商主图生成、营销海报批量制作、UI 设计稿草图转高清、AIGC 辅助绘画、社交媒体配图、图像增强（去背景/扩图/超分）  
- **慎用场景**：需严格时间一致性（如角色动作连贯性）、需三维空间理解（如物体遮挡关系推理）、对动态构图无需求的静态图生成（此时应优先选用专用图像模型而非 Vidu 的降级模式）  

### ✅ 视频生成 —— 适合「时序表达、行为驱动、跨模态协同」场景  
- **推荐场景**：短视频广告自动成片、数字人直播/课程视频生成、产品演示动画（图→视频）、口型同步配音（视频+音频）、老视频风格迁移（如胶片感/赛博朋克）、4K 视频超分增强  
- **慎用场景**：毫秒级响应要求（如游戏内实时生成）、超长视频（>60 秒）批量生产（建议分段合成）、需精确物理仿真（如流体/布料动力学）的工业级视频  

### ✅ 3D生成 —— 适合「空间建模、资产复用、跨平台部署」场景  
- **推荐场景**：游戏/元宇宙 3D 资产快速原型（文生模型）、电商商品 360° 展示建模（单图→3D）、工业零件逆向建模（多视角图→精准网格）、AR 应用轻量化模型生成（`P1.0` 适配移动端）  
- **慎用场景**：需要真实物理材质与光照交互（当前 PBR 材质为静态烘焙，非实时渲染管线）、微米级精度医疗建模（`H3.1-ultra` 最高 200 万面仍属中等精度）、非结构化场景（如自然景观、毛发/烟雾等不可拓扑表示对象）  

---

## 开发者技术选型参考指南

| 选型目标 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| **追求最低接入成本 & 快速验证** | 图像生成（`wanx-v1` 或 `zimage-pro`） | 同步 API、无需轮询、文档成熟、错误反馈直接；`zimage-pro` 支持 `1:1`/`4:3` 即开即用 | 避免在 `zimage-pro` 中传 `negative_prompt`；注意 `size` 合法值范围 |
| **需构建带状态的生成工作流（如视频剪辑平台）** | 视频生成（`wan3.0-video-generation`） | 统一模型覆盖文/图/参考/编辑全链路；任务状态机清晰（`QUEUED`→`RUNNING`→`SUCCEEDED`）；支持回调通知 | 必须实现健壮的轮询逻辑（含退避重试）；务必校验 `X-DashScope-Async: enable` 请求头 |
| **面向 Web/APP 的 3D 内容服务（如在线家具预览）** | 3D生成（`Tripo/Tripo-P1.0`） | 输出轻量 GLB（≤2 万面），加载快、兼容 Three.js/Babylon.js；北京地域稳定性高 | 仅限华北2；需预热 CDN 缓存 `pbr_model_url`；避免高频重复提交相同任务 |
| **高保真工业/影视级资产生成** | 3D生成（`Tripo/Tripo-H3.1` + `geometry_quality: "ultra"`） | 支持 200 万面精细网格，满足中等复杂度机械结构、角色模型需求 | 生成耗时长（常 >8 分钟），需前端友好 Loading 提示；结果需二次优化（如法线重计算） |
| **需多模态混合生成（如“生成一张图，再转成 5 秒视频，最后建模”）** | **组合调用**：<br>① `/v1/images/generations` → 获取高质量首帧<br>② `/video-generation/video-synthesis` → 图生视频<br>③ `/3d-generation` → 单图生3D | 百炼平台各模块解耦清晰，URL 格式与鉴权机制统一（均用 `Authorization: Bearer <key>`） | 注意各环节地域一致性（视频/3D 均需北京）；结果 URL 时效性差异大（图像 1h / 视频 24h / 3D 2h），需及时下载并持久化 |

> **重要提醒**：  
> - **不要混用旧版与新版协议**：`wan2.6` 视频模型与 `wan3.0`、`viduq2` 与 `viduq3`、`zimage` 与 `zimage-pro` 在参数名、字段结构、Endpoint 上均不兼容，请严格对照对应子文档；  
> - **安全合规是前提**：所有生成接口均内置内容安全策略，违规提示词将触发 HTTP 400；建议在生产环境前置部署提示词过滤器；  
> - **监控与告警必做**：对[异步任务](../concepts/asynchronous-task.md)（视频/3D）务必监听 `task_id` 状态异常（如 `FAILED`/`TIMEOUT`），并配置失败重试（非重复创建）与人工兜底通道。  

---  
*本文档基于百炼平台 2024Q3 正式版 API 规范编写，最新变更请以 [API 参考文档](https://help.aliyun.com/zh/model-studio) 为准。*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


