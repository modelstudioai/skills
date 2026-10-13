# 多模态生成 API 对比

为帮助开发者快速理解百炼平台多模态生成能力的技术边界与工程适配要点，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）和 3D 模型生成（3D Generation）三类核心 API。对比聚焦于**生产环境可落地的关键技术维度**，涵盖调用范式、模型能力、输入输出约束、计费与运维特性等，旨在为技术选型提供客观、可执行的参考依据。

---

## 关键维度对比表

| 维度 | 图像生成（`api/image-generation.md`） | 视频生成（`api/video-generation-api.md`） | 3D 生成（`api/3d-generation.md`） |
|------|----------------------------------------|------------------------------------------|------------------------------------|
| **核心能力类型** | 文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、垂直工具（虚拟模特/海报/UI渲染） | 文生视频（T2V）、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人驱动、对口型/动作模仿 | 文生3D（T23D）、图生3D（I23D），输出带PBR材质的GLB模型 |
| **支持模型（主力）** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling-v3-omni-image-generation`, `vidu-image-pro_reference2image`, `z-image-turbo` | `wan2.7-videoedit`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`, `kling/kling-v3-omni-video-generation`, `happyhorse` | `tripo-1.0`（唯一支持模型） |
| **输入格式** | • 文本：`prompt`（长度上限因模型而异，如可灵≤2500字符，Vidu≤5000）<br>• 图像：单图或多图 URL（JPG/PNG，需公网可访问、无中文路径）<br>• 支持参考图融合（如可灵 `element_list`）、辅助参数（如海报 `auxiliary_parameters`） | • 文本：`prompt`（通常≤500字符）<br>• 图像：首帧/尾帧/首尾帧 URL（JPG/PNG/WebP/BMP）<br>• 视频：参考视频 URL（MP4/AVI/MOV，≤300MB，2–120秒）<br>• 音频：数字人驱动需清晰人声 WAV/MP3 | • 文本：`input.text`（≤512 Unicode 字符）<br>• 图像：`input.image_url`（单张 RGB 图，≤1024×1024 像素，JPG/PNG）<br>• **二者互斥，不可共存** |
| **输出格式** | • 同步模型：直接返回 JSON，含 `output.results[]`（每项为图像 Base64 或 `url`）<br>• 异步模型：返回 `task_id`，需轮询 `/result?task_id=xxx` 获取 `output.results[]`（含 `url`） | • **全部强制异步**：返回 `task_id` → 轮询 `/api/v1/tasks/{task_id}` → `output.video_url`（直链 MP4，有效期24h） | • 同步响应（逻辑上）：返回 JSON，含 `output.result_url`（临时 GLB 文件直链，有效期24h）<br>• 实际耗时较长（最长180s），建议按异步流程处理超时 |
| **调用范式** | • **混合范式**：<br> ✓ 同步：千问、Z-Image、万相 V2.6+/V2.7（单请求返回）<br> ✗ 异步强制：万相 V2.5 及以下、可灵、Vidu、全部创意工具类模型（虚拟模特/海报等） | • **统一异步范式**：<br> ✓ 必须携带 `X-DashScope-Async: enable`<br> ✓ 创建任务 → 轮询结果<br> ✗ 不支持任何同步调用，缺失 header 将报错 | • **伪同步接口**：<br> ✓ 单次 HTTP POST 请求<br> ⚠ 实际为长耗时任务（非即时返回），需客户端主动处理超时与重试（推荐指数退避） |
| **API 端点（典型）** | • 同步：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`<br>• 异步：同上（但响应结构不同） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（所有模型共用） | `https://dashscope.aliyuncs.com/api/v1/models/tripo-1.0/generate`（**不支持业务空间专属域名**，仅旧版全局 endpoint） |
| **计费方式** | • 按**生成图像张数**计费（`n` 参数）<br>• 部分模型（如 `wan2.7-image-pro`）支持 `watermark=false`（可能影响计费策略）<br>• 创意工具类模型（虚拟模特/海报等）多数仅限免费体验，**不支持付费开通** | • 按**生成视频时长（秒）或任务次数**计费（依模型而异，如 Vidu 按分辨率与时长阶梯计费，可灵按任务计费）<br>• 所有模型均支持商用付费，无免费额度限制（除部分检测类辅助接口） | • 按**单次任务**计费（无论文本或图像输入）<br>• 无免费额度，无按面数/分辨率分级计费，统一单价 |
| **地域与隔离性** | • **强地域绑定**：API Key、Endpoint、Workspace ID 必须同地域（北京/新加坡/弗吉尼亚）<br>• 跨地域调用直接鉴权失败 | • **强地域绑定**：同图像生成，且所有视频模型 endpoint 均要求严格匹配地域 | • **弱地域绑定**：仅依赖全局 `dashscope.aliyuncs.com`，不校验 Workspace ID；但实际调用仍受 API Key 所属地域限制（如北京 Key 无法调用新加坡 Tripo 服务，因 Tripo 当前仅部署在北京） |
| **典型场景** | • 高频轻量生成：UI 设计稿、电商主图、AIGC 社媒配图<br>• 精细编辑：商品图局部重绘、证件照背景替换、风格化海报<br>• 垂直提效：虚拟模特换装、中英文字精准渲染（Vidu） | • 内容营销：短视频脚本可视化、广告分镜生成、产品演示动画<br>• 影视辅助：剧集概念视频、角色动作预演<br>• 交互应用：数字人播报、AI 教师口型同步、AR 场景动态内容生成 | • 游戏开发：低多边形（Low-Poly）道具/场景原型生成<br>• 电商展示：商品 3D 展示页快速建模（如陶瓷杯、家具）<br>• AR/VR 应用：轻量化可交互 3D 资产构建 |

---

## 适用场景建议（面向开发者）

| 场景需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| **需要毫秒级响应、高并发生成图标/小图** | `z-image-turbo`（图像生成） | 轻量模型，同步调用，延迟最低；适合前端实时预览、A/B 测试图批量生成 |
| **强调中文文本/复杂 UI 元素像素级还原（如带 Logo 的海报、信息图）** | `vidu/vidu-image-pro_reference2image`（图像生成） | Vidu 在中英文混排、矢量图形、图表结构理解上表现最优，支持高保真参考图融合 |
| **需生成叙事性强、多镜头连贯的短视频（如产品故事片）** | `kling/kling-v3-omni-video-generation` 或 `vidu/viduq3-pro_text2video`（视频生成） | 可灵支持预置主体ID保障关键元素一致性；Vidu 在长时序运动连贯性与画质稳定性上更优 |
| **构建数字人播报系统（需音频驱动+口型同步）** | `pixverse/pixverse-v6-lipsync` + `wan2.2-s2v`（视频生成） | 爱诗 Lipsync 专精口型精度；万相 S2V 提供成熟数字人驱动管线，二者组合成熟度高 |
| **快速生成可嵌入 Web 的轻量 3D 模型（无需专业建模师）** | `tripo-1.0`（3D 生成） | 唯一开箱即用的 3D API，输出标准 GLB，Three.js/Babylon.js 开箱兼容；适合 MVP 验证与原型迭代 |
| **需在单次请求中完成“文→图→视频”链路（如文案→配图→短视频）** | **组合调用**：<br>① `qwen-image-3.0-pro` 生成高质量首帧图<br>② `kling/kling-v3-omni-video-generation` 以该图为输入生成视频 | 千问图像模型支持 OpenAI 兼容模式，便于集成到现有 LLM 工作流；可灵视频模型对首帧图鲁棒性强，链路稳定 |

---

## 技术选型参考要点（给开发者的提醒）

- ✅ **优先使用业务空间专属域名**：图像与视频生成务必迁移到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，旧域名 `dashscope.aliyuncs.com` 存在性能瓶颈与未来下线风险；3D 生成暂不支持，但需关注后续升级计划。
- ✅ **异步是常态，同步是例外**：除千问、Z-Image、万相 V2.6+/V2.7 外，**所有图像编辑类、全部视频、全部 3D 任务均需轮询机制**。请在 SDK 封装或业务代码中统一实现健壮的轮询器（含超时、重试、状态码判断）。
- ⚠️ **模型弃用风险高**：避免使用 `wanx-v1`、`qwen-image-2.0`、`wanx2.1-vace-plus` 等已归档模型——其文档明确标注“不推荐新项目使用”，且无功能更新与 SLA 保障。
- ⚠️ **输入 URL 是高频故障点**：确保图像/视频 URL 公网可达、无中文路径（需 `encodeURIComponent`）、格式合规（如可灵不支持 PNG 透明通道）。建议在调用前增加 URL 可访问性预检。
- ⚠️ **计费敏感场景需精确控制参数**：图像生成注意 `n`（张数）和 `watermark`（水印开关）；视频生成关注 `resolution` 和 `aspect_ratio`（直接影响费用）；3D 生成虽单价固定，但 `resolution: "high"` 会显著延长耗时，需权衡体验与成本。
- 📌 **调试建议**：  
  - 使用 DashScope SDK（Python/Java）而非裸 HTTP，自动处理认证、重试、轮询；  
  - 开启 `debug=True` 或日志级别为 `DEBUG`，捕获完整请求/响应体；  
  - 对异步任务，记录 `task_id` 与时间戳，便于问题追溯。

---  
*本文档基于百炼平台 2024 年 Q3 发布的 API 文档版本编写，模型能力与参数细节请以各模型最新 API 参考文档为准。*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


