# 多模态生成能力对比：图像、视频与3D生成

本页旨在为开发者提供百炼平台多模态生成能力的横向技术对比，聚焦**图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）** 三大核心能力。随着AIGC应用场景从静态内容向动态表达与空间建模纵深演进，准确理解各模态在输入约束、输出特性、工程集成方式及成本模型上的差异，是构建稳定、可扩展、符合业务预期的AI工作流的关键前提。本文基于当前（2024年Q3）平台正式发布的API能力与官方文档规范撰写，所有信息均经交叉验证，不包含内测或灰度功能。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **核心输入格式** | 文本（prompt）、单图/多图URL或Base64；支持参考图融合（最多14张）、局部掩码、擦除区域等结构化输入 | 文本（prompt）、单帧图（首帧/首尾帧）、视频片段、音频（数字人s2v）、多模态参考（image/video混合数组）；所有URL需公网可访问 | 文本（prompt）**或** 单张图像URL（PNG/JPEG，建议512×512+，近似1:1宽高比）；二者**二选一，不可共存** |
| **核心输出格式** | PNG/JPEG（含透明通道支持）、WebP；部分模型支持带推理过程的JSON（如`thinking_mode`） | MP4（H.264编码，标准分辨率如720p/1080p）；输出含元数据（时长、帧率、尺寸）；无原始帧序列或中间表示 | GLB（glTF Binary）；标准3D网格格式，含几何、PBR材质、基础光照；**不输出OBJ/FBX/USDZ等其他格式** |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/viduq2-pro_reference2image`, `facechain-finetune` 等（>15个活跃模型） | `wan2.7-i2v`, `happyhorse/happyhorse-t2v`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`, `kling/kling-v3-omni-video-generation` 等（覆盖4大主力系列） | 仅 `Tripo`（text-to-3D / image-to-3D）；**无替代模型或备选方案** |
| **API端点（统一范式）** | 同步：`POST /api/v1/services/aigc/image-generation/generation`<br>异步：`POST /api/v1/services/aigc/image-generation/async-generation`（编辑/创意类强制） | **全量异步**：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis`（创建任务）<br>`GET /api/v1/tasks/{task_id}`（轮询） | **全量异步**：<br>`POST /v1/3d/generation`（提交）<br>`GET /v1/3d/generation/{task_id}`（轮询） |
| **调用协议支持** | ✅ DashScope 同步/异步<br>✅ OpenAI 兼容模式（仅同步路径）<br>❌ 不支持纯WebSocket流式响应 | ❌ 无同步调用能力<br>✅ DashScope 异步（唯一支持方式）<br>❌ 不支持OpenAI兼容协议 | ❌ 无同步调用能力<br>✅ DashScope 异步（唯一支持方式）<br>❌ 不支持OpenAI兼容协议 |
| **地域与域名要求** | 严格隔离：华北2（北京）、新加坡、美国（弗吉尼亚）三地独立Key与Endpoint；<br>**必须使用业务空间专属域名**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com` | 严格隔离：同图像生成；<br>**必须使用业务空间专属域名**；<br>跨地域混用必然鉴权失败 | 严格隔离：同图像/视频；<br>**必须使用业务空间专属域名**；<br>未明确支持旧域名（`dashscope.aliyuncs.com`） |
| **计费方式** | ✅ 按调用次数计费（不同模型单价不同）<br>✅ 支持按[Token](../concepts/token.md)计费（部分模型如`qwen-image-3.0`）<br>⚠️ 部分模型（如`wanx-x-painting`）仅限免费额度，**无付费通道** | ✅ 全量按任务计费（1次请求=1个任务）<br>✅ 部分模型（如`VideoRetalk`）叠加RPS/并发数限制<br>⚠️ 无[Token](../concepts/token.md)计费模式 | ✅ 按成功任务计费（失败任务不扣费）<br>⚠️ 无免费额度；**无按分辨率/面数等细粒度计费项** |
| **典型场景** | 文生图营销素材、电商主图生成、AI修图、虚拟模特试穿、LoRA人像微调、局部重绘、风格迁移、像素级人像分割 | 短视频广告生成、数字人播报、产品演示动画、参考视频风格迁移、口型同步（s2v）、动作模仿、视频超清增强 | 游戏低多边形资产快速原型、电商3D商品展示模型、AR/VR内容轻量化建模、工业设计概念草模 |

## 各方案适用场景建议

- **选择图像生成，当您需要**：  
  ✅ 快速产出高质量静态视觉内容（秒级响应，同步调用友好）；  
  ✅ 对输出格式有强控制需求（透明通道、指定分辨率、水印开关）；  
  ✅ 进行精细化编辑（擦除补全、局部重绘、多图融合）；  
  ❌ 避免用于需物理运动、时间序列或空间深度表达的场景。

- **选择视频生成，当您需要**：  
  ✅ 构建具备时间维度的动态内容（广告、教学、数字人交互）；  
  ✅ 复用现有视觉资产（图/视频/音频）驱动新内容生成；  
  ✅ 要求运动物理真实感（HappyHorse）或特效表现力（PixVerse）；  
  ❌ 避免用于对首帧到末帧间过渡逻辑有精确帧控需求的场景（当前不支持关键帧编辑）；  
  ❌ 避免在无公网URL托管能力的私有环境直接调用（所有媒体输入需公网可访问）。

- **选择3D生成，当您需要**：  
  ✅ 从文本或单图快速获得可直接导入引擎的GLB模型（零建模门槛）；  
  ✅ 构建轻量级3D资产用于Web AR、小程序或游戏原型验证；  
  ✅ 接受中等几何精度与基础材质（非影视级PBR或高模拓扑）；  
  ❌ 避免用于需多视角输入、视频序列重建、物理仿真或CAD级精度的工业场景；  
  ❌ 避免依赖多模型选型——Tripo是当前唯一且不可替代的方案。

## 技术选型参考（面向开发者）

作为平台开发者，请依据以下原则进行决策：

1. **优先确认模态本质需求**：  
   - 若业务目标是“一张图解决”，选**图像生成**；  
   - 若目标是“一段动起来的视频”，选**视频生成**；  
   - 若目标是“一个能旋转缩放的3D对象”，选**3D生成**。  
   *切勿因“视频更酷”而强行用视频生成替代图像生成——成本高3–10倍，延迟高2–5倍，且不必要。*

2. **严格校验输入输出链路**：  
   - 所有模态均**强依赖公网可访问的媒体URL**。若您的图像/视频/3D输入源在内网或OSS私有Bucket，请务必前置调用[获取临时文件URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)接口；  
   - 视频与3D生成**强制异步**，需自行实现健壮的轮询逻辑（建议指数退避+最大重试次数限制）；图像生成中编辑类模型同样强制异步，切勿遗漏`X-DashScope-Async: enable` Header。

3. **地域与认证必须“三位一体”**：  
   API Key、Workspace ID、Endpoint URL 的地域（`cn-beijing`/`ap-southeast-1`/`us-east-1`）**必须完全一致**。这是百炼平台最常见集成失败原因，建议在初始化SDK时即做校验断言。

4. **生产环境规避风险模型**：  
   - 图像生成中，`wanx-x-painting`、`shoemodel-v1`、`image-erase-completion` 等模型**无付费通道，额度用尽即失效**，严禁用于生产服务；  
   - 视频生成中，万相2.1–2.6系列已进入维护期，新项目请统一选用 `wan2.7-*` 及以上版本；  
   - 3D生成无替代模型，但Tripo对输入质量敏感，务必遵循“单物体、白底、正面清晰”最佳实践。

5. **成本与性能平衡建议**：  
   - 图像生成：高吞吐场景（如批量生成Banner）优先选 `z-image-turbo` 或 `qwen-image-3.0`；高画质场景（如4K海报）选 `wan2.7-image-pro`；  
   - 视频生成：对首帧保真度要求高选 `wan2.7-i2v`；对运动生成自然度要求高选 `happyhorse/happyhorse-t2v`；  
   - 3D生成：无模型选择余地，但可通过优化prompt（具体名词+简洁描述）和输入图（干净、居中、单物体）显著提升成功率与质量。

> 最后提醒：所有多模态生成能力均处于快速迭代中。建议订阅[百炼平台变更日志](../../raw/platform-changelog.md)，并定期核查模型状态页（如[图像模型状态](../../raw/model-api-reference/image-generation/status.md)），避免因模型下线或协议变更导致服务中断。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


