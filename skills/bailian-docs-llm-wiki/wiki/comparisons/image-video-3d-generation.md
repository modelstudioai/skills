# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在[多模态](../concepts/multi-modal.md)内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比基于当前（2024年Q3）正式发布的API服务，聚焦**技术实现一致性、调用范式差异、模型生态覆盖度及生产就绪度**，旨在为产品设计、架构选型与成本规划提供客观、可落地的技术决策依据。

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|---------------------------|
| **输入格式** | 支持纯文本（[prompt](../guides/prompt.md)）、单图/多图URL（最多14张）、图文混合；支持中英日韩等55语种图像翻译输入 | 支持纯文本（[prompt](../guides/prompt.md)）、单图（首帧）、双图（首尾帧）、参考视频（`reference_media`数组）、图文混合；不支持纯音频输入 | 支持纯文本（[prompt](../guides/prompt.md)）、单图/多图URL（按视角命名顺序）、已有3D模型URL（GLB/FBX/OBJ等）；多图需严格按 `front/left/back/right` 顺序提交 |
| **输出格式** | JPG/PNG（主流）、WEBP/BMP/TIFF（部分模型）；输出为静态图像URL（有效期24小时）；支持水印开关（`watermark: false`） | MP4（H.264编码，标准封装）；输出为视频直链URL（有效期24小时）；暂不支持GIF、ProRes等专业格式 | GLB（默认，含PBR材质）、OBJ+MTL、FBX、USDZ、PLY；Gaussian Splatting 输出为 `.splat` 文件；所有格式均带纹理贴图（可选关闭） |
| **核心支持模型** | `qwen-image-3.0-pro`、`wan2.7-image-pro`、`vidu/vidu-image-pro_reference2image`、`kling/kling-v3-image-generation`、`z-image-turbo`、`qwen-mt-image-2.0`（翻译）等 | `wanx3.0-video-generation`、`vidu/viduq3-pro_text2video`、`pixverse/pixverse-v6-t2v`、`kling/kling-v3-omni`、`happyhorse/happyhorse-t2v`、`MiniMax-H3` | `Tripo/Tripo-H3.1`（通用文生3D）、`Tripo/Tripo-P1.0`（轻量级）、`Tripo/Tripo-ImageToSplat`（高保真渲染）、`Tripo-Texture`/`Tripo-Retopology`/`Tripo-AutoRig`（后处理全栈） |
| **API端点（统一入口）** | 多入口：<br>• 同步：`/image-generation/generation`（DashScope协议）<br>• 异步：`/api/v1/services/aigc/multimodal-generation/generation`（带 `X-DashScope-Async: enable`） | **统一异步入口**：<br>`/api/v1/services/aigc/video-generation/video-synthesis`<br>（强制 `X-DashScope-Async: enable`） | **统一异步入口**：<br>`/api/v1/services/aigc/video-generation/3d-generation`<br>（强制 `X-DashScope-Async: enable`，仅限华北2北京地域） |
| **调用模式** | **同步为主，异步为辅**：<br>• 简单T2I/I2I推荐同步调用（秒级返回）<br>• FaceChain训练、复杂编辑等长耗时任务需异步 | **强制异步**：<br>所有请求必须携带 `X-DashScope-Async: enable`，无同步通道；典型任务耗时 30s–5min | **强制异步**：<br>所有请求必须携带 `X-DashScope-Async: enable`；基础3D生成耗时 1–8min，后处理任务（如重拓扑、自动绑骨）可达 5–15min |
| **地域约束** | 严格地域绑定：API Key、Endpoint、Workspace ID 必须同地域（北京/新加坡/弗吉尼亚等） | 严格地域绑定：同图像生成，且各模型在不同地域的可用性可能不同（如Vidu部分模型仅限北京） | **强地域锁定**：**仅支持华北2（北京）地域**；API Key、Endpoint、Workspace ID 必须为北京地域，跨地域调用直接失败 |
| **计费方式** | 按**生成张数**计费（`n` 或 `series_amount`）；部分模型（如 `wan2.7-image-pro`）支持无水印输出但单价略高；免费模型（如 `wanx-poster-generation-v1`）无付费通道，额度耗尽即停用 | 按**视频秒数 × 分辨率系数**计费（如 720P=1x，1080P=2x，4K=6x）；部分模型（如 `pixverse-motioncontrol`）按“动作指令次数”额外计费；无免费额度模型 | 按**任务类型分层计费**：<br>• 基础生成（Tripo-H3.1）：按面数区间（500–2M faces）阶梯定价<br>• 后处理（贴图/重拓扑/绑骨）：按输入模型复杂度与操作类型单独计费<br>• 所有任务均无免费额度 |
| **典型场景** | • 营销海报/电商主图批量生成<br>• UI界面原型渲染与像素级还原<br>• 多语言图文本地化（含排版保留）<br>• 虚拟模特试穿、人像风格迁移<br>• 图像擦除补全与局部重绘 | • 短视频广告创意生成（15–60s）<br>• 教育/培训类动态演示视频（首帧→动画）<br>• 数字人播报视频（图生视频+对口型）<br>• 游戏过场动画分镜生成（`series_amount` 多图联动）<br>• 视频风格迁移与超清增强 | • 游戏/AR应用3D资产快速建模（文生/图生）<br>• 工业设计概念验证（单图→可编辑网格）<br>• 实时渲染管线构建（Gaussian Splatting 输出）<br>• 3D打印前处理（重拓扑+分割+格式转换）<br>• 虚拟偶像骨骼绑定与动作迁移（AutoRig + Retarget） |
| **输入限制重点** | • 图像URL：≤10 MB，宽高∈[512, 8192]，总像素≤400万<br>• 文本prompt：`kling`限2500字符，`vidu`限5000字符<br>• 不支持透明通道（除 `qwen-image-2.1-pro` 明确声明） | • 媒体URL：必须公网可访问，无中文路径<br>• 视频参考：单个参考视频≤500MB，时长≤30s<br>• prompt长度：`Vidu`限5000字符，`MiniMax`限7000字符 | • 图像：≤20 MB，分辨率≥256×256<br>• 3D模型：≤150 MB（GLB/FBX/OBJ）<br>• 多视角图：必须按 `front/left/back/right` 顺序，缺失需显式填 `null` |
| **开发者友好性** | ★★★★☆<br>• OpenAI兼容接口可用<br>• 同步调用降低集成门槛<br>• 参数命名统一（`size`, `n`, `watermark`） | ★★★☆☆<br>• 统一入口简化路由管理<br>• 但所有模型共用同一端点，需靠 `model` 字段精确路由<br>• 缺少OpenAI兼容模式 | ★★☆☆☆<br>• 全异步+强地域锁定增加调试成本<br>• 后处理依赖 `task_id` 链式调用，流程编排复杂<br>• 无OpenAI兼容支持，需完全适配DashScope协议 |

## 各方案适用场景建议

### ✅ 优先选择图像生成（Image Generation）当：
- 需要**毫秒级响应**的轻量级内容（如A/B测试图、UI占位符、社交头像）；
- 任务以**静态视觉表达为核心**（海报、Banner、商品图、信息图），无需时间维度；
- 需要**多语言图文本地化**且严格保留原始排版（`qwen-mt-image-2.0` 是唯一支持方案）；
- 开发团队已集成 OpenAI SDK，希望最小改造接入（通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)）。

### ✅ 优先选择视频生成（Video Generation）当：
- 内容本质是**时间序列表达**（广告、教程、数字人播报、分镜脚本）；
- 需要**首帧/首尾帧控制**或**参考视频驱动**（如将PPT转为讲解视频、将线稿转为动画）；
- 对**运动物理真实感**或**长时序一致性**有明确要求（`HappyHorse` / `Vidu-q3-pro` 为优选）；
- 接入方具备基础异步任务轮询能力，且能接受 30s–3min 的平均等待延迟。

### ✅ 优先选择3D生成（3D Generation）当：
- 目标是构建**可交互、可渲染、可动画的3D资产**（非仅图片预览）；
- 流程需覆盖**生成→后处理→交付全链路**（如：图生模型 → 自动贴图 → 重拓扑 → 绑骨 → 导出FBX供Unity使用）；
- 应用场景明确限定于**北京地域部署环境**（如政企私有云、北京IDC集群）；
- 团队具备3D工作流基础（理解GLB/PBR/拓扑/骨骼等概念），能处理 `.splat` 或 `.fbx` 等专业格式。

## 技术选型参考（面向开发者）

| 选型维度 | 关键判断依据 | 推荐动作 |
|----------|--------------|----------|
| **实时性要求** | 若端到端延迟需 <2s（如实时UI预览），选图像生成（同步）；若可接受 ≥30s 延迟，视频/3D均可评估 | ✅ 图像生成：启用 `qwen-image-3.0-pro` 同步调用<br>❌ 视频/3D：不适用于实时交互场景 |
| **内容维度需求** | 若需表达“变化”“过程”“运动”，必须选视频；若需“空间结构”“可旋转观察”“可导入引擎”，必须选3D；其余静态呈现场景，图像生成性价比最高 | ✅ 单帧效果验证 → 图像<br>✅ 动态叙事 → 视频<br>✅ 可交互资产 → 3D |
| **基础设施约束** | 若业务系统部署在新加坡或弗吉尼亚，**3D生成不可用**；若需多地域容灾，视频/图像更灵活 | ✅ 图像/视频：按需选择对应地域模型<br>❌ 3D：仅北京可用，需评估架构合规性 |
| **成本敏感度** | 图像生成单次成本最低（≈0.01–0.1元/张）；视频按秒计费（720P约0.3–1.5元/秒）；3D生成起步价高（H3.1基础任务≈5–20元/次），后处理叠加费用 | ✅ 小批量、高并发 → 图像<br>✅ 中长视频、低频生成 → 视频<br>✅ 一次性高质量资产构建 → 3D（长期看ROI更高） |
| **技术栈成熟度** | 若团队无3D引擎经验，强行接入Tripo易陷入格式解析/材质调试困境；若已有Unity/Unreal管线，Tripo可无缝嵌入 | ✅ 新团队起步 → 从图像→视频→3D渐进式引入<br>✅ 3D原生团队 → 直接启用Tripo全栈能力（尤其 `AutoRig` + `Retarget`） |

> **重要提醒**：所有能力均遵循**地域强隔离原则**。开发者在初始化SDK或配置HTTP客户端时，必须确保 `API Key`、`Endpoint URL`、`Workspace ID` 三者地域完全一致——这是百炼平台最常见且最易被忽视的调用失败原因。建议在CI/CD流程中加入地域校验脚本，避免线上环境因配置漂移导致服务中断。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


