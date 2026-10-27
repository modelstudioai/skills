# 多模态生成能力对比：图像、视频与3D生成

本对比旨在为开发者提供百炼平台多模态AIGC能力的系统性技术选型参考。随着文生图、图生视频、文本/图像到3D等生成式AI技术快速演进，不同模态在输入表达力、输出复杂度、计算资源消耗、工程集成方式及业务适配性上存在显著差异。本文基于当前（2024Q3）百炼平台正式发布的API能力，从**技术实现维度**出发，客观梳理图像、视频、3D三类核心生成能力的关键特性、约束条件与适用边界，帮助团队在产品设计、架构选型与成本规划阶段做出高效、稳健的技术决策。

---

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **核心输入格式** | 文本（`prompt`） + 可选1–14张参考图（URL/Base64）；支持多图融合、局部重绘指令 | 文本（`prompt`）<br>或首帧/首尾帧图像（`first_frame`/`last_frame`）<br>或参考媒体数组（`media`: image/video/audio URL混合）<br>或数字人语音+图像（`lip_sync_tts_content` + `image_url`） | 文本（`prompt`，≤1024字符）<br>或单张图像（JPEG/PNG，≤20MB）<br>或严格4视角图像数组（前/左/后/右）<br>或已有3D模型（GLB/FBX/OBJ，≤150MB） |
| **核心输出格式** | JPEG/PNG（同步返回二进制或Base64）；部分模型支持WebP；分辨率支持语义值（`2K`/`4K`）或宽×高（如`1024*1024`） | MP4（H.264编码）；分辨率最高支持4K；时长3–30秒；输出为公网可访问直链（`output.video_url`） | GLB（默认）、FBX、OBJ、USDZ、PLY等；支持Gaussian Splatting（`.splat`）；贴图支持PNG/JPG；网格精度可控（面数50–2,000,000） |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/vidu-image-pro_reference2image`, `z-image-turbo`, `facechain-finetune` | `wan2.7-videoedit`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`, `kling/kling-v3-omni-video-generation`, `minimax/minimax-t2v`, `happyhorse/happyhorse-t2v` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-ImageToSplat`, `Tripo/Tripo-Segmentation`, `Tripo/Tripo-AutoRig`, `Tripo/Tripo-AnimationRetarget` |
| **API调用模式** | **混合模式**：<br>• 同步调用（`qwen-image-3.0-pro`, `wan2.7-image-pro`, `z-image-turbo`等）→ 单次POST直接返回结果<br>• 异步调用（`kling`, `vidu`, `wan2.5-i2i-preview`等）→ 先POST获取`task_id`，再GET轮询 | **强制异步**：<br>所有模型必须设置请求头 `X-DashScope-Async: enable`；<br>统一两步流程：`POST /video-synthesis` → `GET /tasks/{task_id}`；<br>`task_id`有效期24小时 | **强制异步**：<br>统一两步流程：`POST /3d-generation` → `GET /tasks/{task_id}`；<br>`task_id`有效期24小时；<br>**仅支持华北2（北京）地域** |
| **地域绑定要求** | ✅ 强绑定：API Key、Endpoint、Workspace ID 必须同地域（华北2/新加坡/美东等） | ✅ 强绑定：API Key、Endpoint、Workspace ID 必须同地域；各模型支持地域略有差异（如Vidu暂未开放美东） | ⚠️ **超严格绑定**：**仅支持华北2（北京）地域**；API Key、Endpoint、Workspace ID 必须为北京地域，跨地域调用必然失败 |
| **计费方式** | • 按**调用次数**（per call）计费（主流模型如`qwen-image-3.0-pro`）<br>• 部分轻量模型（`z-image-turbo`）按**Token量**计费<br>• 创意工具类（`shoemodel-v1`, `image-erase-completion`）仅限**免费额度**，用尽即停 | • 统一按**任务（per task）** 计费<br>• 不同模型单价差异大（如`wan2.7-videoedit` vs `viduq3-pro`）<br>• 高清/长时长/多参考媒体等高级参数可能触发**阶梯加价** | • 按**任务（per task）** 计费<br>• 基础生成（文/图生3D）为标准单价<br>• 后处理任务（贴图/分割/绑骨）单独计费<br>• 高级参数（如`texture_quality=extreme`, `face_limit=2000000`, `quad=true`）触发**高级转换费用** |
| **典型端到端耗时** | • 同步模型：3–15秒（取决于分辨率与模型）<br>• 异步模型：10–60秒（`kling`平均30s，`vidu-pro`平均45s） | 30秒 – 8分钟（取决于时长、分辨率、模型负载）：<br>• `pixverse-turbo`：约30–90秒（10s@720P）<br>• `viduq3-pro`：3–8分钟（30s@4K） | 1–15分钟（取决于输入复杂度与参数）：<br>• 文生3D（`Tripo-H3.1`）：2–6分钟<br>• 图生3D（4视角）：3–8分钟<br>• Gaussian Splat生成：1–3分钟<br>• 自动绑骨（`AutoRig`）：4–12分钟 |
| **输入/输出文件限制** | • 图像URL需公网可访问、无中文路径<br>• 单图≤10MB（`kling`）/ ≤20MB（`vidu`）<br>• 分辨率：300–8000px（宽高） | • 所有媒体（图/视/音）必须为HTTP/HTTPS公网URL<br>• OSS临时URL需额外声明头 `X-DashScope-OssResourceResolve`<br>• 视频输入≤500MB（`minimax`），音频≤100MB | • 输入图≤20MB；3D模型≤150MB<br>• 多图生3D：`images`数组**必须且仅能为4个元素**，缺失视角需用`{}`占位<br>• 输出GLB默认压缩，FBX/USDZ等格式体积较大 |
| **特殊能力亮点** | • 局部重绘（mask引导）、风格迁移、图文混排、UI像素级还原（`vidu`）<br>• 虚拟模特、海报生成、鞋靴试穿等垂直创意工具<br>• 支持最多10张参考图融合（`qwen-image-3.0-pro`） | • 首尾帧控制运动轨迹（`pixverse`, `wan2.7`）<br>• 对口型驱动（`pixverse`, `wan2.2-s2v`）<br>• 主体ID预设（`kling`：如“雷电”“魔法法阵”）<br>• 广告级长时序一致性（`viduq3-pro`） | • 端到端3D工作流：生成→分割→贴图→重拓扑→绑骨→动画重定向<br>• Gaussian Splatting原生支持（`Tripo-ImageToSplat`）<br>• 智能部件分割（`Tripo-SmartSegmentation`）<br>• Mixamo兼容自动绑骨（`Tripo-AutoRig`） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高并发、低延迟、强可控」场景  
- **推荐场景**：  
  - 电商商品图批量生成（海报、白底图、场景图）  
  - UI/UX设计稿辅助（图标、Banner、组件渲染，尤其`vidu`对中英文字精准支持）  
  - 社交内容创作（头像、壁纸、表情包、虚拟模特写真）  
  - A/B测试素材快速产出（多风格/多尺寸并行生成）  
- **慎用场景**：  
  - 需要严格物理运动逻辑或时序连贯性的内容（应选视频）  
  - 需三维空间结构理解与交互（如AR/VR资产、游戏建模）  

### ✅ 视频生成 —— 适合「动态表达、叙事驱动、人机交互」场景  
- **推荐场景**：  
  - 短视频营销（广告片、产品演示、AI漫剧）  
  - 数字人直播/客服（语音驱动口型+表情，`pixverse`/`wan2.2-s2v`）  
  - 教育/培训动画（步骤演示、原理可视化）  
  - 游戏过场动画原型（快速验证镜头语言与节奏）  
- **慎用场景**：  
  - 超高精度物理仿真（如流体、布料动力学）——当前模型仍以视觉合理性优先  
  - 需精确帧级编辑或复杂时间线合成（建议导出后使用专业NLE工具）  

### ✅ 3D生成 —— 适合「空间构建、工业应用、元宇宙基建」场景  
- **推荐场景**：  
  - 游戏/AR/VR资产快速原型（文生基础模型 → 分割部件 → 贴图 → 绑骨 → 动画）  
  - 电商3D商品展示（单图生成带PBR材质的GLB，嵌入WebGL查看器）  
  - 工业设计辅助（草图→3D模型→重拓扑→CAD兼容导出）  
  - AI内容平台3D素材库建设（批量图生3D+智能分割+格式标准化）  
- **慎用场景**：  
  - 实时渲染级性能要求（如大型开放世界LOD流式加载）——需后处理优化  
  - 高精度机械结构/公差级建模（当前仍属CAD范畴，非AIGC替代）  

---

## 面向开发者的选型建议

1. **优先确认地域合规性**  
   - 若业务已部署于**新加坡或美东**：图像与视频生成可自由选用；**3D生成不可用**（仅限北京）。  
   - 若必须使用3D能力：全栈服务（含API Key、Workspace、下游渲染服务）**必须统一部署在北京地域**。

2. **根据响应时效选择调用模式**  
   - 需实时反馈（如用户点击即见图）→ 选用**同步图像模型**（`qwen-image-3.0-pro`, `wan2.7-image-pro`）；  
   - 可接受排队等待（如后台批量任务）→ 统一采用**异步范式**（视频/3D必选，图像中`kling`/`vidu`也推荐）；  
   - **切勿尝试视频/3D同步调用**：会明确报错 `"current user api does not support synchronous calls"`。

3. **输入设计决定能力上限**  
   - 图像：善用**多图参考+局部重绘指令**（如 `"将红色沙发替换为蓝色天鹅绒，保留背景不变"`）提升可控性；  
   - 视频：**首尾帧比单首帧更能约束运动终点**，对动作类生成（舞蹈、手势）效果显著提升；  
   - 3D：**4视角输入质量远高于单图**；若仅有一张图，优先使用`Tripo-H3.1`（支持`generate_parts`与高级贴图）而非`P1.0`。

4. **成本优化关键点**  
   - 图像：轻量需求选`z-image-turbo`（Token计费）；高质需求选`wan2.7-image-pro`（固定call价+4K输出）；  
   - 视频：短时长（5–10s）+ 720P → 选`pixverse-turbo`或`wan2.7-videoedit`；长时序一致性要求 → `viduq3-pro`虽贵但不可替代；

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


