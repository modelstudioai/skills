# 多模态生成 API 对比：图像、视频与 3D 生成

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术能力边界与工程适配要点，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）和 3D 生成（3D Generation）三类核心 API。对比聚焦实际开发中高频关注的**调用范式、输入输出约束、模型生态、地域/环境依赖、计费逻辑及典型落地场景**，旨在提供可操作的技术选型依据，避免因协议差异、参数冲突或地域错配导致集成失败。

---

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D 生成（3D Generation） |
|------|------------------------------|------------------------------|---------------------------|
| **核心调用范式** | 同步 RESTful（请求即响应，通常 < 10s） | **强制异步**（`X-DashScope-Async: enable` 必填，需轮询 `task_id`） | **强制异步**（同视频，`task_id` 有效期 24 小时） |
| **输入格式** | 文本（`prompt`）、Base64 图像、图像 URL（支持 `image_url` / `image` 二选一）；局部重绘需额外传 `mask`（灰度图 Base64） | 结构化 JSON：<br>• 文生视频：`{ "prompt": "..." }`<br>• 图生视频：`{ "img_url": "...", "prompt": "..." }` 或首尾帧双 URL<br>• 参考生视频：`{ "reference_images": [...] }` 或混合媒体数组 | 三者互斥：<br>• 文生：仅 `prompt`<br>• 单图生：仅 `image`（URL）<br>• 多图生：仅 `images`（长度为 4 的 front/left/back/right 数组） |
| **输出格式** | 同步返回 `output.results[]`，含 `url`（1 小时有效期）和 `base64` 字段；支持 JPEG/PNG | 异步返回 `output.video_url`（MP4/H.264，通常 3–30 秒，分辨率最高 4K）；部分编辑类模型返回多段 URL（如对口型输出音频+视频） | 异步返回 `output.base_model_url`（无贴图网格）、`output.pbr_model_url`（含 PBR 贴图）、`output.splat_url`（Gaussian Splat）等；格式含 GLB/FBX/OBJ/SPLAT |
| **主流支持模型** | 万相（WanX）、可灵（Kling）、千问-VL 分支、Z-Image、Vidu（`type=image`）、创意工具（inpainting/scribble/style-transfer） | 万相（Wan2.7+）、PixVerse（t2v/it2v/r2v/lipsync）、Vidu（Q3-Pro）、HappyHorse、Kling、MiniMax；数字人 `wan2.2-s2v` 使用独立旧路径 | Tripo 全系：<br>• 生成：`Tripo/Tripo-H3.1`（高精）、`Tripo/Tripo-P1.0`（专业）、`Tripo/Tripo-ImageToSplat`<br>• 后处理：分割/补全/重拓扑/贴图/格式转换<br>• 动画：绑骨（AutoRig）、重定向（Retarget） |
| **API 端点（标准路径）** | `https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation`（全局统一域名） | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（**地域强绑定**，需匹配 Workspace ID） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`（**仅华北2（北京）地域有效**，硬性限制） |
| **计费方式** | 按**成功生成图片数量**计费（`n` 参数值），单次请求最多 4 张；高分辨率（如 2048×2048）不额外加价 | 按**任务成功执行次数**计费；不同模型单价差异显著（如 PixVerse 高帧率模式 > Wan2.7 基础版）；视频编辑类功能（超清/风格重绘/动作模仿）单独计费 | 按**任务类型分层计费**：<br>• 基础生成（H3.1/P1.0）按面数/精度档位计费<br>• 后处理（如 Retopology/Texture）按输入模型复杂度计费<br>• 动画流程（AutoRig + Retarget）按步骤分别计费；`quad=true`、`face_limit` 非默认值等高级参数触发溢价 |
| **典型场景** | UI 原型草图（Z-Image）、广告海报生成（万相）、高保真艺术创作（可灵）、图文混合提示推理（千问-VL）、局部编辑（创意工具） | 短视频营销（文生视频）、产品动态展示（图生视频）、虚拟主播口播（lipsync）、跨模态内容复用（参考生视频）、数字人驱动（wan2.2-s2v） | 游戏资产快速建模（文/图生3D）、AR 场景重建（ImageToSplat）、工业零件逆向建模（多图生3D）、动画角色管线（AutoRig → Retarget） |

---

## 适用场景建议（面向开发者）

| 场景需求 | 推荐方案 | 关键理由与避坑提示 |
|----------|----------|---------------------|
| **低延迟、轻量级图像产出**（如设计稿占位符、A/B 测试图） | ✅ Z-Image（`zimage-v1`） | 512×512 固定分辨率，响应最快（平均 < 2s）；但仅支持简体中文提示词，且不支持图生图。避免在需要高分辨率或跨语言场景误用。 |
| **高质量中文语义图像生成**（电商主图、国风海报、文旅宣传） | ✅ 万相（`wanx-v1`） | 对古风、水墨、广告文案类提示词优化最佳；默认 768×768，支持 up to 1024×1024；图生图与局部重绘能力成熟。⚠️ 注意：Vidu 的 `type=image` 模式稳定性差，生产环境禁用。 |
| **高分辨率构图控制需求**（建筑可视化、产品精修） | ✅ 可灵（`kling-v2`） | 支持 1024×1024 至 2048×2048，构图逻辑强；但**不支持图生图**，需纯文本驱动。若需编辑，须先用万相生成初稿，再转至创意工具处理。 |
| **短视频内容批量生成**（信息流广告、社媒运营） | ✅ Wan2.7-text2video 或 PixVerse-v6-max-t2v | Wan2.7 生态完善、中文提示鲁棒性强；PixVerse 在运动连贯性与光影表现上更优。⚠️ 必须启用 `X-DashScope-Async`，且轮询间隔 ≥15s；避免在非北京地域 Workspace 调用万相 2.7+（旧版 `image2video` 路径除外）。 |
| **虚拟人/数字人驱动场景**（直播、客服） | ✅ Wan2.2-s2v（数字人） + PixVerse-lipsync（对口型） | Wan2.2-s2v 专为数字人优化，但**必须使用北京专属域名**（`cn-beijing.maas.aliyuncs.com`），且不支持 WorkspaceId；对口型需搭配 PixVerse 独立调用。二者不可混用同一 task_id。 |
| **3D 内容从零构建**（游戏原型、教育模型） | ✅ Tripo/Tripo-H3.1（文/图生） + Tripo-AutoRig（绑骨） | H3.1 支持 200 万面高精网格，`generate_parts=true` 可输出模块化部件；AutoRig 支持 Mixamo/UE 标准骨架。⚠️ `generate_parts=true` 时**禁止启用 `texture`/`pbr`/`quad`**，否则 400 报错。 |
| **实时渲染与 Web3D 集成**（WebGL/Three.js 应用） | ✅ Tripo/Tripo-ImageToSplat | 直接输出 `.splat` 文件，体积小、加载快、支持动态光照；无需后处理即可嵌入前端。⚠️ 输入图需清晰正视，模糊或多视角会导致 splat 破碎。 |
| **工业级 3D 编辑与交付**（CAD 协同、制造准备） | ✅ Tripo-P1.0（生成） + Tripo-Retopology（重拓扑） + Tripo-ConvertFormat（FBX） | P1.0 输出面数可控（50–20,000），适合下游 CAD 软件导入；Retopology 生成四边面（`quad=true`）后，ConvertFormat 可导出 FBX 供 Unity/Unreal 使用。⚠️ P1.0 **不支持 `geometry_quality` 等高级参数**，传入将被忽略。 |

---

## 技术选型决策指南

开发者在启动多模态项目前，请按以下顺序自查：

1. **确认调用范式一致性**  
   - 若业务要求“请求-响应”即时性（如交互式设计工具），**优先选图像生成**；视频与 3D 必须接受异步延迟（典型耗时：图像 < 10s，视频 30s–5min，3D 1–15min）。
   
2. **严格校验地域与环境配置**  
   - 视频生成：确保 `WorkspaceId`、API Key、Endpoint 中的 `{region}`（如 `cn-beijing`）三者完全一致；  
   - 3D 生成：**强制华北2（北京）** —— 即使 Workspace 在其他地域，也必须使用北京专属域名与北京 API Key，否则 404 或 403。

3. **规避参数兼容性陷阱**  
   - 图像：`image_url` 优先级高于 `image`；图生图缺失 `mask` 会被降级为文生图；  
   - 视频：万相 2.7+ 与 2.1–2.6 接口路径不兼容，调用前务必核对文档版本；  
   - 3D：`Tripo/Tripo-H3.1` 与 `Tripo/Tripo-P1.0` 参数集不互通，`generate_parts` 与 `texture` 是互斥开关。

4. **成本敏感型选型建议**  
   - 图像：Z-Image 单图成本最低，适合海量草图；万相/可灵适合精品图；  
   - 视频：基础文生视频（Wan2.7）性价比最优；高帧率/4K/多参考需评估预算；  
   - 3D：P1.0（≤2 万面）成本约为 H3.1（150 万面）的 1/5，精度要求不高时首选。

5. **生产环境红线**  
   - 禁用 Vidu 的 `type=image` 作为主力图像模型（文档明确标注其为视频模型副产物，稳定性不足）；  
   - 禁用万相 2.1–2.6 旧版接口（`/image2video/...`）于新项目，已进入维护期；  
   - 3D 生成中，`Tripo/Tripo-AutoRig` 若指定 `spec=mixamo`，则后续不可调用 `Tripo-AnimationRetarget`（文档硬性约束）。

> **最后提醒**：所有多模态 API 均遵循百炼平台统一鉴权机制（`Authorization: Bearer YOUR_API_KEY`），但**图像生成使用 `dashscope.aliyuncs.com` 域名，视频与 3D 必须使用 `maas.aliyuncs.com` 域名**。混用域名将导致 401 或 404 错误，此为最常见集成故障点。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


