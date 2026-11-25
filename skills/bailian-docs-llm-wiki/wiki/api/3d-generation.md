# 3d generation

百炼平台的 3D generation 能力基于 Tripo 模型提供端到端的 3D 内容生成与后处理服务，覆盖从文本/图像输入生成基础 3D 模型，到高保真 Gaussian Splatting、网格分割、重拓扑、格式转换及动画绑定等完整工作流。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果。

## 支持的模型/功能

3D generation 功能分为三大类：

- **基础生成**：支持文生 3D、单图生 3D、多图生 3D（前/左/后/右四视角），以及单图生成 Gaussian Splat（`.splat`）文件。后者适用于实时渲染与场景重建，而前者输出可编辑网格（GLB/FBX）[Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。
- **后处理**：包括贴图生成（支持 PBR 与 8K）、网格分割（语义/连通域）、智能分割（端到端建模+分割）、网格补全（AI 补洞/快速封口）、重拓扑（v1.0 减面 / v2.0 智能低模）及格式转换（GLTF/USDZ/FBX/STL 等，含烘焙、UV、轴心点控制）[模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。
- **动画**：提供可绑骨检查 → 自动绑骨 → 动画重定向三级流水线，支持 biped、quadruped 等 7 类骨骼类型及预设动画应用 [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：文档中多次强调“仅适用于华北2（北京）地域”，但 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md) 与 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md) 均明确要求使用北京地域 API Key 和 Endpoint；而部分后处理文档（如 [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)）虽未在 URL 示例中显式标注地域，但其前提条件与 HTTP 调用节均复用同一北京地域 Endpoint 模板，因此全域统一强制北京地域，无矛盾。

## 关键参数

- **通用必填头**：`Content-Type: application/json`、`Authorization: Bearer <API_KEY>`、`X-DashScope-Async: enable`（缺失将报错）。
- **输入方式互斥**：`prompt`（文生）、`image`（单图）、`images`（多图）三者不可共存；`original_model_task_id` 与 `model_url` 在后处理接口中亦为二选一。
- **核心生成参数**：
  - `texture_quality`: `standard`/`detailed`/`extreme`（8K）
  - `geometry_quality`: 仅 `Tripo/Tripo-H3.1` 支持，`standard`（≤150万面）或 `ultra`（≤200万面）
  - `pbr`: `true`（默认）时强制启用贴图并返回 `pbr_model_url`
- **后处理特有参数**：
  - 分割：`model_version`（`v1.0`/`v2.0`）、`segmentation_granularity`
  - 重拓扑：`model_version`（`v1.0`/`v2.0`）、`face_limit`（v1.0 必填）、`quad`
  - 格式转换：`format`（`GLTF`/`USDZ`/`FBX` 等）、`quad`、`face_limit`、`texture_size`

## 使用方式

1. **开通与认证**：在百炼控制台华北2（北京）地域开通 Tripo 服务，并配置对应地域的 API Key 到环境变量（如 `DASHSCOPE_API_KEY`）。
2. **异步调用流程**：
   - **步骤1（创建任务）**：向 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送 POST 请求，传入 `model`、`input` 和 `parameters`，获取 `task_id`（有效期 24 小时）。
   - **步骤2（轮询结果）**：使用 `task_id` 调用轮询接口（文档未给出具体路径，需参考通用轮询规范）直至 `task_status` 为 `SUCCEEDED`。
3. **输入准备**：
   - 图像 URL 需公网可访问，格式为 JPEG/PNG/WebP，大小 ≤20MB；
   - 3D 模型 URL（后处理）支持 GLB/GLTF/FBX/OBJ/STL，大小 ≤150MB；
   - 多图输入（`images`）必须为长度为 4 的数组，按 `[front, left, back, right]` 顺序，空视角用 `{}` 占位。

## 限制和注意事项

- **地域强约束**：所有接口均**仅支持华北2（北京）地域**，跨地域调用将失败，且 API Key 必须为该地域生成。
- **任务依赖严格**：后处理任务（如贴图、分割、重拓扑）的 `original_model_task_id` 必须来自同账号、已成功执行的前序任务（如生成或分割任务），引用其他账号或失败任务将返回 400 错误。
- **模型兼容性**：`Tripo/Tripo-P1.0` 不支持 `geometry_quality`、`quad`、`smart_low_poly` 等参数；`Tripo/Tripo-ImageToSplat` 仅接受 `image` 输入，不支持 `prompt` 或 `images`。
- **计费与高级功能**：`quad=true`、`face_limit` 非默认值、`texture_size` ≠4096、`scale_factor` ≠1.0 等操作均触发高级转换计费；动画重定向要求前序绑骨任务 `spec` 不能为 `mixamo`，否则无法使用 [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)。
- **安全与调试**：`task_id` 有效期仅 24 小时，务必及时轮询；所有请求需携带 `request_id` 用于问题溯源；首次调用建议使用 Postman 参考示例验证环境。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


