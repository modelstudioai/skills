# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供端到端的 3D 内容创作流水线，覆盖从文/图生 3D 模型、Gaussian Splatting 生成，到模型后处理（分割、贴图、重拓扑、补全、格式转换）及动画绑定与重定向等完整工作流。所有接口均采用异步调用模式，需通过任务 ID 轮询获取结果。

## 支持的模型/功能

- **基础生成**：
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `geometry_quality=ultra`、`quad`、`smart_low_poly`、`generate_parts` 等高级参数 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。
  - `Tripo/Tripo-P1.0`：专业级快速生成（最高 2 万面），适用于对速度敏感的场景。
  - `Tripo/Tripo-ImageToSplat`：单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与真实感重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**（均需输入已有模型）：
  - 分割：`Tripo/Tripo-Segmentation`（基于几何/语义）、`Tripo/Tripo-SmartSegmentation`（端到端图像/模型输入）；
  - 贴图：`Tripo/Tripo-Texture`（支持 PBR、8K、风格引导）；
  - 重拓扑：`Tripo/Tripo-Retopology`（v2.0 智能低模 / v1.0 基础减面）；
  - 补全：`Tripo/Tripo-MeshCompletion`（AI 扩散补全或快速封口）；
  - 格式转换：`Tripo/Tripo-ConvertFormat`（支持 GLTF/USDZ/FBX/OBJ/STL/3MF 及烘焙、UV 合并、朝向控制等）。

- **动画**：
  - 绑骨检查：`Tripo/Tripo-RigCheck`（判断可绑骨性并推荐 `rig_type`）；
  - 自动绑骨：`Tripo/Tripo-AutoRig`（支持 biped/quadruped 等 7 类骨骼类型）；
  - 动画重定向：`Tripo/Tripo-AnimationRetarget`（应用预设动画，最多 5 个）。

> **注意**：文档中 `Tripo/Tripo-AnimationRetarget` 明确要求前序任务必须为 `Tripo/Tripo-AutoRig` 且 `spec != 'mixamo'`；但 `Tripo/Tripo-AutoRig` 文档本身未明确禁止 `mixamo` 用于后续流程，仅说明“使用此规范绑骨的模型不能用于动画重定向”。此处以动画重定向文档为准，开发者须严格规避 `spec=mixamo` 的绑骨任务作为其输入。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `model_seed` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-ImageToSplat` | 几何生成随机种子，相同种子+输入产出一致网格 | `42` |
| `texture_seed` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Texture` | 贴图生成随机种子，用于控制贴图变体 | `123` |
| `face_limit` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 目标面数上限（三角面），`Tripo-H3.1` 默认自适应，`Tripo-P1.0` 必填（50–20,000） | `50000` |
| `geometry_quality` | `Tripo-H3.1` only | `standard`（≤150 万面）或 `ultra`（≤200 万面）；`Tripo-P1.0` 忽略该参数 | `"ultra"` |
| `quad` | `Tripo-H3.1`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 输出四边面网格（强制 FBX 格式）；`Tripo-P1.0` 忽略 | `true` |
| `generate_parts` | `Tripo-H3.1` only | 生成可编辑部件，启用时自动禁用 `texture`/`pbr`/`quad`/`smart_low_poly` | `true` |
| `model_version` | 多个后处理模型 | 指定算法版本（如 `Tripo-Texture` 的 `v3.0-20250812`），版本不匹配可能导致效果下降或失败 | `"v3.0-20250812"` |

## 使用方式

1. **地域与认证**：所有接口**仅支持华北2（北京）地域**，必须使用该地域的 API Key，并配置 `X-DashScope-Async: enable` 请求头。
2. **异步流程**：统一采用两步式调用：
   - **步骤1（创建）**：`POST /api/v1/services/aigc/video-generation/3d-generation`，传入 `model`、`input` 和 `parameters`，获取 `task_id`（有效期 24 小时）。
   - **步骤2（轮询）**：`GET /api/v1/tasks/{task_id}`，建议首次查询延迟 10 秒，之后每 15–30 秒轮询一次，直至 `task_status = SUCCEEDED`。
3. **输入方式**：
   - 生成类：三选一 — `prompt`（文本）、`image`（单图）、`images`（4 视角数组，顺序为前/左/后/右）。
   - 后处理类：二选一 — `original_model_task_id`（引用前序任务输出）或 `model_url`（公网可访问的 GLB/GLTF/FBX/OBJ/STL）。
4. **参数兼容性**：部分参数互斥或有条件生效（如 `generate_parts` 与 `pbr` 不兼容），详见各模型文档，错误配置将返回 400 错误。

## 限制和注意事项

- **地域强约束**：全部接口仅限北京地域，跨地域调用必然失败，且 API Key 必须在该地域开通并配置 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。
- **文件限制**：
  - 输入图像：JPEG/PNG/WebP，≤20 MB，分辨率 [20, 6000] 像素；
  - 输入 3D 模型（后处理）：GLB/GLTF/FBX/OBJ/STL，≤150 MB；
  - 输出模型：`Tripo-H3.1` 最高 200 万面，`Tripo-P1.0` 最高 2 万面。
- **任务依赖**：后处理任务（如贴图、分割、重拓扑）若依赖前序任务，必须确保：
  - 前序任务已 `SUCCEEDED`；
  - `original_model_task_id` 由同一账号创建；
  - 部件操作（`part_names`）需配合 `Tripo-Segmentation` 或 `Tripo-SmartSegmentation` 任务输出的 GLB 节点名使用。
- **计费差异**：高级参数（如 `quad=true`、`face_limit` 非默认值、非 JPEG 贴图）可能触发更高积分消耗，具体见各接口文档。
- **模型兼容性**：`Tripo-AnimationRetarget` 严格禁止使用 `spec=mixamo` 的绑骨结果；`Tripo-Texture` 若输入非 Tripo 生成的模型，必须传入 `texture_prompt`，否则任务失败。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)


