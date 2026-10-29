# 多模态生成能力对比：图像、视频与3D生成

本页旨在为开发者提供百炼平台多模态生成能力的横向技术对比，聚焦**图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）**三大核心模态。随着AIGC应用从静态内容向动态、空间化演进，准确理解各模态在输入表达力、输出可控性、工程集成复杂度及商业落地路径上的差异，是构建高质量AI原生应用的关键前提。本文基于当前（2024年Q3）平台正式发布的API能力，从技术实现、服务协议、资源约束与业务适配性四个维度展开客观分析，不涉及模型内部架构或训练细节，仅面向生产环境选型决策。

---

## 关键能力维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|-------------------------------|--------------------------|
| **核心输入格式** | 文本（[prompt](../guides/prompt.md)）、单图/多图URL（支持最多14张）、掩码（局部编辑）、参考图+文本（分镜/融合） | 文本、单图（首帧）、双图（首尾帧）、视频URL、音频URL、混合媒体数组（image/video/audio） | 文本（[prompt](../guides/prompt.md)）、单图、四视图数组（前/左/后/右）、已有3D模型URL（GLB/GLTF/FBX等） |
| **核心输出格式** | PNG（默认）、JPEG（部分模型）、Base64（同步调用可选）；支持水印开关 | MP4（H.264编码，主流分辨率）、WebM（部分模型）；无原始帧序列输出 | GLB（默认）、FBX、OBJ、USDZ、STL、3MF、Splat（`.splat`）；支持PBR贴图、UV、骨骼绑定等元数据 |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `z-image-turbo`, `kling/kling-v3-omni-image-generation`, `vidu/viduq2-pro_reference2image`, `facechain-finetune` | `wan3-video-generation`, `happyhorse/t2v`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`, `kling/kling-v3-omni-video-generation`, `wan2.2-s2v`（遗留） | `Tripo/Tripo-H3.1`（高精网格）、`Tripo/Tripo-P1.0`（快速低模）、`Tripo/Tripo-ImageToSplat`, `Tripo/Tripo-Texture`, `Tripo/Tripo-AutoRig` |
| **API端点（统一路径）** | `/api/v1/services/aigc/image-generation/text-to-image`（T2I）<br>`/api/v1/services/aigc/image-generation/image-to-image`（I2I）<br>（部分模型如`qwen-image-*`支持OpenAI兼容`/v1/images/generations`） | `/api/v1/services/aigc/video-generation/video-synthesis`（主端点，覆盖HappyHorse/WanX/PixVerse/Vidu/Kling）<br>（少数旧模型仍用`/image2video/...`） | `/api/v1/services/aigc/video-generation/3d-generation`（注意：路径含`video-generation`但实际为3D专属） |
| **调用模式** | **混合模式**：<br>• 同步：`qwen-image-3.0-pro`, `wan2.7-image-pro`, `z-image-turbo`, `wan2.6-t2i`（毫秒级返回URL/Base64）<br>• 异步：`kling/*`, `vidu/*`, `facechain-finetune`, `wan2.5-i2i-preview`（需轮询`/tasks/{id}`） | **强制异步**：<br>所有模型均需 `POST /video-synthesis` → 获取 `task_id` → 轮询 `GET /tasks/{id}`（24小时有效期） | **强制异步**：<br>所有接口均需 `POST /3d-generation` → 轮询 `GET /tasks/{id}`（24小时有效期） |
| **地域支持** | **多地域**：华北2（北京）、华东1（杭州）、华南1（深圳）、新加坡、弗吉尼亚等（具体模型支持范围不同，如`qwen-mt-image-2.0`仅限北京/新加坡） | **多地域**：北京、新加坡、弗吉尼亚等（需严格同地域Key+Endpoint+Workspace ID） | **单地域**：**仅华北2（北京）**，跨地域调用直接失败 |
| **计费方式** | • 按**调用次数**（如`wan2.6-t2i`）<br>• 按**输出分辨率/像素量**（如`qwen-image-3.0-pro`按总像素计费）<br>• 部分工具类模型（如`image-erase-completion`）免费额度用尽即停用 | • 按**生成视频时长×分辨率档位**（如`720P`/`1080P`/`4K`）<br>• 部分模型按**输入媒体复杂度**（如参考视频帧数、音频时长）计费<br>• 视频检测类API（如`s2v-detect`）无论结果均计费 | • 按**任务类型+参数组合**计费（如`Tripo-H3.1` + `geometry_quality=ultra` > `standard`）<br>• 后处理任务（贴图/重拓扑/动画）单独计费，与前序生成任务解耦<br>• `texture_quality=extreme`（8K）消耗积分显著高于`standard` |
| **典型端到端延迟** | 同步：300ms–2s（`z-image-turbo`最快）<br>异步：5s–90s（`kling`/`vidu`复杂提示词可达2–5分钟） | 通常 30s–5分钟（`HappyHorse`基础T2V），复杂参考生视频/特效可达10–20分钟 | 生成任务：2–8分钟（`Tripo-P1.0`快于`H3.1`）<br>后处理任务：贴图/重拓扑约1–3分钟，动画重定向约30–120秒 |
| **输入长度/尺寸限制** | • 文本：`kling` ≤2500字符，`vidu` ≤5000字符<br>• 图像：宽高 `[300, 8000]` 像素（`kling`），`[512, 4096]`（擦除补全） | • 文本：5000–7000字符<br>• 图像：建议400×400–1920×1080，公网可访问URL<br>• 视频：≤30秒，≤300MB<br>• 音频：≤120秒，需清晰人声 | • 图像：≤20MB，分辨率 `[20, 6000]` 像素<br>• 3D模型：≤150MB，支持GLB/GLTF/FBX/OBJ/STL<br>• 四视图：必须严格4张，空视角用`{}`占位 |
| **输出可控性亮点** | • 局部重绘（mask驱动）<br>• 多图融合与分镜组图（`kling-v3-omni`）<br>• 风格迁移/去水印/扩图（`wanx2.1-imageedit`）<br>• 图像翻译（55语种排版保留） | • 首尾帧精准运动控制（`wan2.2`）<br>• 动作模仿/口型同步（`PixVerse`, `VideoRetalk`）<br>• 视频特效模板（`wanx` flying/hanfu等）<br>• 多档性能模型（`vidu turbo/pro/4k`） | • 四边面强制输出（`quad=true`）<br>• 部件级分割与贴图（`part_names`）<br>• 自动绑骨+动画重定向流水线<br>• Gaussian Splatting实时渲染就绪输出 |

---

## 各方案适用场景建议

| 场景类型 | 推荐模态 | 理由说明 |
|----------|-----------|-----------|
| **营销与电商内容快速生产** | ✅ 图像生成 | 同步调用低延迟、支持批量生成（`n=6`）、本地化强（图像翻译）、模板化工具丰富（海报/虚拟模特/鞋靴试穿），适合日更千图级运营需求。`wan2.7-image-pro` + `thinking_mode` 可辅助提示词优化。 |
| **短视频创作与社交内容** | ✅ 视频生成 | 首帧/首尾帧控制满足脚本分镜需求，`PixVerse`高动态表现力适配舞蹈/特效，`HappyHorse`物理真实感提升产品展示质感。异步模式天然匹配创作者“提交→等待→下载”工作流。 |
| **游戏/AR/VR资产管线** | ✅ 3D生成 | `Tripo-H3.1`百万面精度+`Tripo-Texture` 8K PBR贴图+`Tripo-AutoRig`自动骨骼，构成完整资产生产链；`Tripo-ImageToSplat`直出实时渲染格式，大幅缩短美术制作周期。 |
| **工业设计与数字孪生** | ⚠️ 3D生成（首选） + 图像生成（辅助） | `Tripo`支持精确几何重建与格式转换（USDZ用于AR，FBX用于CAD集成），`qwen-mt-image-2.0`可将多语言说明书图像化，但视频生成在此类场景中价值有限。 |
| **教育/科普可视化** | ✅ 图像生成 + ⚠️ 视频生成 | 图像生成快速产出概念图、流程图、分子结构图（`qwen-image-3.0-pro`多参考图能力）；视频生成适用于原理动画（如`HappyHorse`流体模拟），但需权衡生成时长与教学节奏。 |
| **个性化头像/虚拟人形象定制** | ✅ 图像生成（FaceChain） + ⚠️ 3D生成（Tripo） | `facechain-finetune`基于2–10张人脸训练专属LoRA，5分钟生成高保真2D头像；`Tripo`可进一步生成3D头像模型并绑定表情动画，但成本与周期显著增加。 |

> **不推荐交叉替代的典型反例**：  
> - ❌ 用视频生成替代图像生成做Banner设计：延迟高、成本高、分辨率控制粒度粗，且无法保证单帧构图稳定性。  
> - ❌ 用图像生成替代3D生成做产品建模：缺乏深度与拓扑信息，无法导出可编辑网格或用于物理仿真。  
> - ❌ 用3D生成替代视频生成做社交媒体短视频：无时间轴控制、无音频同步、无运镜逻辑，本质是静态空间建模。

---

## 面向开发者的选型参考指南

### 1. **优先选择同步调用的场景**
- **适用**：实时交互应用（如设计工具插件、在线作图平台、A/B测试图片生成）、低延迟要求服务（如电商搜索结果即时配图）。  
- **推荐**：`qwen-image-3.0-pro`（T2I/I2I全能）、`wan2.7-image-pro`（高分辨率+推理过程可选）、`z-image-turbo`（极致速度）。  
- **规避**：`kling`/`vidu`图像模型（纯异步）、`facechain-finetune`（训练耗时分钟级）。

### 2. **需强地域合规与多云部署的场景**
- **适用**：金融、政务、跨国企业客户，要求数据不出域、API Key与Endpoint严格隔离。  
- **推荐**：图像生成（多地域支持最全）、视频生成（北京/新加坡/弗吉尼亚三地覆盖）。  
- **规避**：3D生成（仅北京），若业务需部署于新加坡或弗吉尼亚，需规划代理或数据中转方案。

### 3. **构建长链路AI工作流的场景**
- **适用**：自动化3D资产工厂、视频内容工业化生产流水线。  
- **关键实践**：  
> - **视频链路**：使用`wan3-video-generation`统一端点 + `parameters.style`控制风格，避免混用`/image2video/`旧路径。  
> - **3D链路**：严格遵循依赖顺序（生成→分割→贴图/重拓扑→绑骨→动画），利用`part_names`实现部件级精细化控制；所有任务ID需在24小时内完成轮询。  
> - **图像链路**：对需多步编辑（如先扩图再风格迁移）的任务，优先选用`qwen-image-3.0-pro`（单次请求支持I2I+参数组合），减少HTTP往返。

### 4.

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


