# 3d generation

百炼平台的 3D generation 能力基于 Tripo 模型系列，提供从文本/图像生成基础 3D 模型、Gaussian Splatting 表示，以及完整的后处理与动画工作流。所有接口均采用异步调用模式，需通过任务 ID 轮询获取结果，且当前**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供两类核心能力：**基础生成**与**后处理/增强**。

- **基础生成**：
  - `Tripo/Tripo-H3.1` 与 `Tripo/Tripo-P1.0`：支持文生3D、单图生3D、多图生3D，输出带贴图或PBR材质的GLB/FBX模型 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。
  - `Tripo/Tripo-ImageToSplat`：根据单张图片直接生成 `.splat` 文件，适用于实时渲染与真实感重建，**不输出网格** [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理与增强**（均需以已有3D模型为输入）：
  - **分割类**：`Tripo-Segmentation`（对已有模型语义分割）、`Tripo-SmartSegmentation`（端到端图像/模型输入→分割模型），二者定位不同，后者包含建模环节 [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)。
  - **几何处理类**：`Tripo-MeshCompletion`（AI补全或快速封口）、`Tripo-Retopology`（减面与重拓扑）、`Tripo-ConvertFormat`（格式转换与导出设置）。
  - **材质与纹理类**：`Tripo-Texture`（为模型生成PBR贴图，最高8K）。
  - **动画类**：`Tripo-RigCheck`（判断可绑骨性）、`Tripo-AutoRig`（自动添加骨骼）、`Tripo-AnimationRetarget`（应用预设动画）。

> **注意**：文档中 `Tripo-智能分割` 与 `Tripo-网格分割` 的适用场景存在明确区分——前者是端到端流程（输入图像即可得分割模型），后者仅对已有模型进行分割。二者不可混用，详见 [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md) 和 [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)。

## 关键参数

所有 Tripo 3D 接口共用以下关键参数结构：

- **必填请求头**：`Content-Type: application/json`、`Authorization: Bearer <API_KEY>`、`X-DashScope-Async: enable`（缺失将报错）。
- **模型标识**：`model` 字段为固定字符串，如 `"Tripo/Tripo-H3.1"` 或 `"Tripo/Tripo-Texture"`。
- **输入方式**：统一通过 `input` 对象指定，支持 `prompt`（文本）、`image`（单图URL）、`images`（多图数组）或 `original_model_task_id`/`model_url`（模型引用）。
- **核心可选参数**：
  - `texture_quality`: `standard`/`detailed`/`extreme`（影响贴图分辨率与耗时）。
  - `geometry_quality`: 仅 `H3.1` 支持 `standard`/`ultra`（控制面数上限）。
  - `face_limit`: 显式控制输出模型面数（单位：三角面），各模型取值范围不同（如 `H3.1` 最高200万，`P1.0` 最高2万）。
  - `quad`: 启用四边面输出（强制FBX格式）。
  - `pbr`: 是否启用PBR材质（含metallic/roughness/normal贴图）。
  - `model_seed`/`texture_seed`: 控制几何与贴图的确定性生成。

## 使用方式

1. **开通与配置**：在百炼控制台（华北2地域）开通 Tripo 服务，并配置对应地域的 API Key。
2. **创建任务**：向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，传入 `model`、`input` 及必要 `parameters`，获取 `task_id`。
3. **轮询结果**：使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，建议首次查询延迟10秒，后续每15–30秒轮询一次。任务状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`，`task_id` 有效期为24小时。
4. **链式调用**：后处理任务（如贴图、分割）常需前序任务的 `task_id` 作为 `original_model_task_id` 输入，确保账号一致且前序任务已成功。

## 限制和注意事项

- **地域强约束**：所有 Tripo 3D 接口**仅支持华北2（北京）地域**，API Key、Workspace ID、Endpoint URL 必须严格匹配该地域，跨地域调用必然失败。
- **文件限制**：
  - 输入图像：≤20MB，格式为 JPEG/PNG/WebP，建议分辨率 ≥256×256。
  - 输入3D模型（GLB/FBX/OBJ等）：≤150MB。
- **计费与兼容性**：
  - `Tripo-AnimationRetarget` 要求前序 `AutoRig` 任务的 `spec` 参数**不能为 `mixamo`**，否则任务失败。
  - `Tripo-ConvertFormat` 中 `quad=true` 或 `face_limit` 非默认值时按“高级转换”计费；`Tripo-Texture` 的 `texture_quality=extreme` 消耗更多积分。
- **模型版本兼容性**：
  - `Tripo-Texture` 的 `model_version`（如 `v3.0-20250812`）需与源模型生成版本匹配，否则效果下降。
  - `Tripo-AutoRig` 的 `model_version` 与 `rig_type` 强相关：`v1.0-20240301` 仅推荐用于 `biped`，非人形骨骼应使用 `v2.5-20260210`。
- **任务依赖**：后处理任务（如 `Tripo-Texture`, `Tripo-Retopology`）若需指定部件（`part_names`），必须以前序 `Tripo-Segmentation` 或 `Tripo-SmartSegmentation` 任务的 `task_id` 为输入，且部件名需从其输出 GLB 的节点名中提取（如 `tripo_part_0`）。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)


