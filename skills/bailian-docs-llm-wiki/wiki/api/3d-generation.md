# 3d generation

百炼平台提供基于 Tripo 模型的端到端 3D 内容生成与后处理能力，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、网格分割、重拓扑、贴图生成、格式转换及动画绑定等全链路功能。所有接口均采用[异步任务](../concepts/asynchronous-task.md)模式，需通过 `task_id` 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

- **基础生成**：
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `geometry_quality=ultra`、`quad`、`smart_low_poly`、`generate_parts` 等高级参数 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
  - `Tripo/Tripo-P1.0`：专业级快速生成（最高 2 万面），适合对速度敏感的场景
  - `Tripo/Tripo-ImageToSplat`：单图生成 `.splat` 文件，适用于实时渲染与真实感重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)

- **后处理**：
  - **分割类**：`Tripo/Tripo-Segmentation`（几何/语义分割）、`Tripo/Tripo-SmartSegmentation`（端到端图像/模型输入分割）
  - **优化类**：`Tripo/Tripo-Retopology`（减面与拓扑优化）、`Tripo/Tripo-MeshCompletion`（AI 补全或快速封口）
  - **材质与导出**：`Tripo/Tripo-Texture`（PBR/8K 贴图生成）、`Tripo/Tripo-ConvertFormat`（GLTF/USDZ/FBX 等多格式转换与烘焙）
  - **动画**：`Tripo/Tripo-RigCheck` → `Tripo/Tripo-AutoRig` → `Tripo/Tripo-AnimationRetarget` 三步流程，支持人形与非人形骨骼 [Tripo-动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)

> **注意**：`Tripo/Tripo-AnimationRetarget` 明确要求前序绑骨任务 `spec` 不能为 `mixamo`，而 `Tripo/Tripo-AutoRig` 文档中却将 `mixamo` 列为合法 `spec` 值且注明“使用此规范绑骨的模型不能用于动画重定向”——二者逻辑一致，但 `Tripo-动画重定向` 文档未强调该限制在调用前必须校验，开发者需主动规避。

## 关键参数

| 参数名 | 适用模型 | 说明 |
|--------|----------|------|
| `X-DashScope-Async: enable` | 全部 | **强制请求头**，缺失将报错 `"current user api does not support synchronous calls"` |
| `model_version` | `Tripo/Tripo-Segmentation`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-AutoRig` 等 | 版本控制关键字段，如 `v2.0-20260430`（分割）、`v2.5-20260210`（非人形绑骨），传入不支持版本将返回 400 错误 |
| `face_limit` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 面数上限，取值范围因模型和参数组合差异大（如 `H3.1` + `ultra` 最高 200 万面，`P1.0` 仅限 50–20,000），超限直接报错 |
| `part_names` | `Tripo/Tripo-Texture`, `Tripo/Tripo-MeshCompletion`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 部件名称列表，需从 GLB 节点名中提取（如 `tripo_part_0`），传入不存在名称不报错但照常计费 |
| `quad` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 开启后强制输出 FBX 格式，影响 `face_limit` 默认值及计费等级 |

## 使用方式

1. **前提准备**：
   - 在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务
   - 获取并配置北京地域的 API Key（`DASHSCOPE_API_KEY`）

2. **异步调用流程（统一）**：
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     必须携带 `Content-Type: application/json`、`Authorization: Bearer <key>`、`X-DashScope-Async: enable`
   - **步骤2：轮询结果**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议首次查询延迟 10 秒，后续每 15–30 秒轮询一次；`task_id` 有效期严格为 **24 小时**

3. **输入方式选择**：
   - 生成类：`prompt`（文生）、`image`（单图）、`images`（4 视角数组，顺序为前/左/后/右）
   - 后处理类：优先使用 `original_model_task_id`（引用前序任务输出），或 `model_url`（公网可访问的 GLB/FBX/OBJ 等，≤150MB）

## 限制和注意事项

- **地域强约束**：所有接口**仅支持华北2（北京）地域**，URL、API Key、控制台开通入口均需匹配该地域，跨地域调用必然失败。
- **任务依赖性**：后处理任务（如贴图、分割、绑骨）必须引用同一账号下已成功执行的前序任务 `task_id`；引用其他账号任务或失败任务均返回 400。
- **文件限制**：
  - 输入图像：JPEG/PNG/WebP，≤20MB，建议 ≥256×256 像素
  - 输入模型：GLB/GLTF/FBX/OBJ/STL，≤150MB
- **参数互斥与兼容性**：
  - `Tripo/Tripo-H3.1` 的 `generate_parts=true` 与 `texture=true` / `pbr=true` / `quad=true` / `smart_low_poly=true` **互斥**，同时启用将返回 400 错误
  - `Tripo/Tripo-AnimationRetarget` 的 `animations` 与 `animation` 参数互斥，且 `animations` 中每个元素必须带 `preset:` 前缀（如 `"preset:walk"`）
- **计费提示**：`face_limit` 非默认值、`quad=true`、`texture_quality=extreme`、`animations` 多于 1 个等操作均触发高级计费，详见各文档说明。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


