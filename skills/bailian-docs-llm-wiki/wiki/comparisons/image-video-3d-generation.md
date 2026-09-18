# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术边界与工程适配性，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比基于当前（2024年Q3）正式上线的API能力，聚焦**可用性、调用范式、模型生态、部署约束及商业化就绪度**等关键维度，旨在为产品设计、技术选型与架构决策提供客观、可落地的参考依据。

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|-------------------------------|--------------------------|
| **输入格式** | 支持混合输入：纯文本（`text`）、单图/多图 URL 或 Base64（`image`），部分模型支持图文交错 `messages` 数组（如 Vidu/Kling）；FaceChain 等垂直工具对人脸图像有严格尺寸/姿态要求。 | 依模型而异：<br>• 文生视频：纯文本 `prompt`；<br>• 图生/参考生视频：单图/双图 URL（首帧/首尾帧）；<br>• 数字人/人像驱动：需前置检测返回的 `face_bbox` + `ext_bbox` 坐标 + 图像/音频 URL；<br>• 风格重绘：视频 URL + 风格码。 | 二选一：<br>• 文本：`input.text`（≤200字符，需具象化）；<br>• 图像：单张正面视角 `input.image_url`（推荐512×512–1024×1024，PNG/JPEG）；<br>• 不支持图文混合或多视角输入。 |
| **输出格式** | 多样化：<br>• 主流：JPEG/PNG（Base64 或下载 URL）；<br>• 特殊：WordArt 输出 SVG；FaceChain 输出带Alpha通道PNG；AI试衣输出含透明背景合成图；<br>• 分辨率灵活（512×512 至 4K）。 | 统一为 MP4 视频文件（H.264编码），通过 `output.video_url` 提供下载链接（有效期24小时）；<br>分辨率由 `parameters.resolution` 控制（如 `"720P"`、`"480P"`），部分模型支持自定义宽高比。 | 仅支持 `.glb` 格式（GL Transmission Format Binary），包含网格、材质与基础纹理；<br>不支持 `.obj`、`.fbx`、`.usdz` 等其他3D格式；<br>无动画、骨骼、物理属性。 |
| **支持模型** | 丰富且分层：<br>• 通用：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling-v3-omni-image-generation`、`vidu-image-pro_reference2image`、`z-image-turbo`；<br>• 编辑增强：`qwen-image-edit-max`、`image-out-painting`、`wanx-style-repaint-v1`；<br>• 垂直工具：`facechain-generation`、`aitryon-plus`、`virtualmodel-v2` 等超15个专用模型。 | 按能力域组织：<br>• 通用生成：`HappyHorse`、`wan3.0-video`（All-in-One）、`pixverse-v6-it2v`；<br>• 人像驱动：`emo-v1`、`liveportrait-v2`、`animateanyone-v1`、`video-retalk`；<br>• 数字人：`wan2.2-s2v`；<br>• 专用：`video-style-transform`（8种风格）、`wan2.1-i2v-turbo`（旧版特效）。 | 单一模型：<br>• `tripo-3d`（公测阶段），仅支持 text-to-3D 与 image-to-3D 两种模式；<br>• 无编辑、重绘、多视角重建等衍生能力。 |
| **API 端点** | 多端点并存：<br>• 同步主路径：`/api/v1/services/aigc/image-generation/generation`（DashScope协议）；<br>• OpenAI兼容路径：仅限 `qwen-image-3.0*` 系列；<br>• 垂直工具独立路径（如 `/facechain-generation`）。 | 统一端点：<br>• `POST /api/v1/services/aigc/video-generation/video-synthesis`（所有模型共用）；<br>• 检测类前置API独立（如 `/emo-detect-v1`）。 | 统一端点：<br>• `POST /v1/models/tripo-3d:generate`（非 `/services/aigc/` 下）；<br>• 任务查询：`GET /v1/tasks/{task_id}`（与视频共用任务系统）。 |
| **调用模式** | **同步与异步混合**：<br>• T2I/I2I（如 `wan2.7-image-pro`、`z-image-turbo`）推荐同步调用（低延迟）；<br>• 复杂编辑（扩图、背景生成、海报）必须异步；<br>• 所有调用需显式声明 `X-DashScope-Async: enable`（否则报错）。 | **强制异步**：<br>• 全部模型均不支持同步响应；<br>• 必须“创建任务 → 轮询结果”，典型耗时1–5分钟（数字人/Retalk可达10分钟）；<br>• `X-DashScope-Async: enable` 为必需请求头。 | **强制异步**：<br>• 仅支持任务式调用；<br>• 创建后需轮询 `status`，超时阈值300秒；<br>• 成功后通过 `output.model_url` 下载 `.glb`（有效期24小时）。 |
| **计费方式** | 分模型计费：<br>• 按 token（文本）+ pixel（图像）综合计量；<br>• 高清模型（4K/Pro）单价高于基础模型（如 `z-image-turbo`）；<br>• 垂直工具独立计费（如 `aitryon-plus` 按次，`facechain` 按生成张数）；<br>• 部分工具（`shoemodel-v1`、`wanx-poster-generation-v1`）仅限免费体验，额度用尽即停用。 | 按模型+时长计费：<br>• 视频生成按“模型类型 × 分辨率 × 时长（秒）”计费；<br>• 人像驱动类（EMO/LivePortrait）按“检测+生成”双计费；<br>• 数字人 `wan2.2-s2v` 按“音频时长秒数”计费；<br>• 无免费额度，全部付费使用。 | 按次计费（公测期可能有体验额度）：<br>• 每次成功生成（`status=succeeded`）计1次；<br>• 失败/超时不计费；<br>• 当前无分档定价，暂未开放企业级用量包。 |
| **典型场景** | • 社媒内容批量生产（海报、Banner、信息图）<br>• 电商素材生成（商品图、模特图、AI试衣）<br>• 创意设计辅助（文字艺术、风格迁移、局部重绘）<br>• 个性化头像/写真（FaceChain、VirtualModel） | • 短视频营销（文生剧情短视频、产品演示视频）<br>• 数字人播报（新闻、客服、培训）<br>• 口型同步视频（课程配音、多语种本地化）<br>• 动作迁移/表情驱动（虚拟偶像、游戏NPC）<br>• 视频风格化（艺术短片、品牌视觉统一） | • 游戏/AR快速原型（低多边形道具、场景组件）<br>• 电商3D商品展示（单图生成可交互3D模型）<br>• 工业设计概念验证（简单机械结构、家居摆件）<br>• 教育可视化（分子模型、解剖结构示意） |

## 各方案的适用场景建议

- **选择图像生成，当您需要**：  
  ✅ 快速产出高质量静态视觉资产（<5秒响应）；  
  ✅ 对分辨率、风格、构图有精细控制需求（如UI像素级还原、人像皮肤质感）；  
  ✅ 构建高频调用服务（如A/B测试图生成、个性化营销图）；  
  ❌ 不适合：需要时间维度表达（运动、叙事）、动态交互或三维空间理解的场景。

- **选择视频生成，当您需要**：  
  ✅ 表达时间序列信息（人物动作、镜头运镜、口型同步）；  
  ✅ 构建数字人应用（智能客服、虚拟主播、培训讲师）；  
  ✅ 将静态内容升级为沉浸式体验（产品演示视频、教育动画）；  
  ❌ 不适合：对首帧精度要求极高（如需逐帧手绘级控制）、或需实时交互（如WebGL实时渲染）的场景；注意人像类模型强依赖前置检测，需预留额外RTT。

- **选择3D生成，当您需要**：  
  ✅ 从零快速构建轻量级3D资产（无需建模师介入）；  
  ✅ 实现“单图→可旋转3D”工作流（如电商商品3D化、AR试戴基础模型）；  
  ✅ 在Unity/Blender中进行二次开发（`.glb` 可直接导入）；  
  ❌ 不适合：需要高精度拓扑、UV展开、绑定骨骼、物理模拟或PBR材质精调的工业级应用；当前Tripo模型对复杂有机体（如动物毛发、流体）和抽象概念（如“时间流逝”）生成效果有限。

## 面向开发者的技术选型参考

1. **优先评估输入/输出契约**：  
   - 若业务输入天然为视频（如用户上传短视频），勿强行转为图像处理；若输出需嵌入WebGL，`.glb` 是唯一选择；若需微信/钉钉内直接预览，图像（JPEG/PNG）兼容性远优于视频（MP4）和3D（需额外渲染器）。

2. **警惕地域与域名耦合风险**：  
   - 三类能力均强制要求 **模型、Endpoint、API Key 三者同地域**（北京/新加坡/弗吉尼亚），跨地域调用100%失败；  
   - **务必迁移至业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已逐步限流，新项目禁止使用。

3. **异步任务治理是关键工程能力**：  
   - 视频与3D生成必须实现健壮的任务轮询机制（含指数退避、超时熔断、失败重试）；  
   - 图像生成虽支持同步，但复杂编辑仍需异步——建议**统一采用任务中心模式**，简化客户端逻辑，便于监控与审计。

4. **模型演进策略**：  
   - 图像：优先选用带 `-pro`、`-v3`、`2.7+` 后缀模型（如 `qwen-image-3.0-pro`），避免 `wanx-v1` 等已归档模型；  
   - 视频：万相3.0为统一入口，替代分散的2.7子模型；HappyHorse 与 PixVerse 适合特定场景（前者强于文生，后者强于图生）；  
   - 3D：当前仅 Tripo，密切关注后续是否开放多模型（如 Luma、Meshy 接入）及格式扩展（`.usdz` for AR）。

5. **成本与体验平衡**：  
   - 高频低质场景（如草稿图）用 `z-image-turbo`；  
   - 商业级交付（电商主图）必用 `wan2.7-image-pro` 或 `qwen-image-3.0-pro`；  
   - 视频生成中，`HappyHorse` 性价比最优，`EMO` 适合高表现力数字人；  
   - 3D生成尚处公测，建议小批量验证后再规模化接入。

> **最后提醒**：所有能力均受《百炼平台服务协议》及各模型《使用条款》约束。涉及人脸生成（FaceChain、EMO、LivePortrait）的应用，必须履行用户明确授权、数据脱敏及合规审核义务，严禁用于身份冒用或深度伪造。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


