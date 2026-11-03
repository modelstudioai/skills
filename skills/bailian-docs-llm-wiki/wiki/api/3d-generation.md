# 3d generation

百炼平台的 3D generation 能力基于 Tripo 模型提供端到端的 3D 内容生成与后处理服务，覆盖从文本/图像输入生成基础 3D 网格、Gaussian Splatting 表示，到贴图、分割、重拓扑、格式转换及动画绑定等完整工作流。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果。

## 支持的模型/功能

Tripo 提供三类核心能力：

- **3D 模型生成**：支持文生 3D（`Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`）、单图/多图生 3D，以及专用的 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)（`Tripo/Tripo-ImageToSplat`），适用于实时渲染场景。
- **模型后处理**：涵盖 [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)、[Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)、[Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)、[Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)、[Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md) 和 [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)。
- **动画能力**：包括 [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)、[Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md) 和 [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)，形成完整的骨骼绑定与动画应用链路。

> **注意**：文档中多次强调“仅适用于华北2（北京）地域”，但 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md) 与 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md) 均明确要求使用北京地域 API Key 和 Endpoint；而部分后处理文档（如 [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)）虽未重复声明地域限制，但其请求 URL 和前提条件与前者完全一致，因此所有 Tripo 3D 接口当前均强制限定于华北2（北京）地域。

## 关键参数

- **通用必填头**：所有请求必须包含 `Content-Type: application/json`、`Authorization: Bearer <API_KEY>` 和 `X-DashScope-Async: enable`。
- **输入方式**：生成类接口（如 `Tripo-H3.1`）的 `input` 中 `prompt`、`image`、`images` 三者互斥；后处理类接口（如 `Tripo-Texture`）通常支持 `original_model_task_id` 或 `model_url` 二选一。
- **面数控制**：
  - `face_limit` 在 `Tripo-H3.1` 中默认自适应，取值范围为 500–2,000,000（`ultra` 模式）；在 `Tripo-P1.0` 中为 50–20,000。
  - `Tripo-Retopology` 的 `face_limit` 在 `v1.0` 版本下为必填，`v2.0` 下可选。
- **贴图与材质**：`pbr` 和 `texture` 默认均为 `true`；若需无贴图模型，必须同时设为 `false`。`bake` 参数在 `Tripo-ConvertFormat` 和 `Tripo-Retopology`（v2.0）中用于烘焙材质。
- **部件操作**：`part_names` 在 `Tripo-Segmentation`、`Tripo-MeshCompletion`、`Tripo-Retopology`、`Tripo-ConvertFormat` 等接口中用于指定目标部件，名称需从 GLB 节点中读取（如 `tripo_part_0`）。
- **种子控制**：`model_seed`（几何）、`texture_seed`（贴图）、`image_seed`（图像生成环节）均支持确定性复现，取值范围为 `-2147483648` 至 `2147483647`。

## 使用方式

1. **开通与配置**：在百炼控制台华北2（北京）地域开通 Tripo 服务，并配置对应地域的 API Key 到环境变量或请求头。
2. **异步任务流程**：
   - **步骤1（创建）**：向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 提交请求，获取 `task_id`（有效期 24 小时）。
   - **步骤2（轮询）**：使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 定期查询状态，建议首次延迟 10 秒后开始，后续间隔 15–30 秒。
3. **输入准备**：
   - 图像 URL 需公网可访问，格式为 JPEG/PNG/WebP，大小 ≤20MB，分辨率建议 ≥256×256。
   - 3D 模型文件（GLB/FBX/OBJ 等）URL 大小 ≤150MB。
   - 多视角输入（如 `images` 数组）须按 `front`/`left`/`back`/`right` 顺序，缺失视角可用 `null` 或空对象占位。
4. **后处理依赖**：多数后处理接口（如贴图、分割、重拓扑）需以生成任务的 `task_id` 作为 `original_model_task_id` 输入，且前序任务必须已成功执行。

## 限制和注意事项

- **地域强约束**：所有 Tripo 3D 接口当前仅支持华北2（北京）地域，跨地域调用将失败。请务必确认 Workspace ID 与 API Key 均为北京地域。
- **模型兼容性**：`Tripo-AnimationRetarget` 明确要求前序 `Tripo-AutoRig` 任务的 `spec` 不能为 `mixamo`；`Tripo-Retopology v1.0` 不支持 `part_names` 和 `bake` 参数。
- **参数冲突**：在 `Tripo-H3.1` 中启用 `generate_parts` 时，`texture`、`pbr`、`quad`、`smart_low_poly` 均不兼容，传入将返回 400 错误；`smart_low_poly` 开启时 `face_limit` 取值范围收缩至 500–20,000（三角面）。
- **计费差异**：`Tripo-ConvertFormat` 中启用 `quad`、`force_symmetry`、`flatten_bottom`、非默认 `texture_size`/`texture_format`/`scale_factor` 等均按“高级转换”计费；`Tripo-MeshCompletion` 的 `ai_completion` 与 `quick_cap` 模式计费不同。
- **任务管理**：`task_id` 有效期严格为 24 小时，超时后查询返回 `UNKNOWN`；轮询 RPS 默认为 20，高频需求应配置异步回调。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
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
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


