# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供端到端的 3D 内容创作流水线，覆盖从文本/图像输入生成基础 3D 网格、高保真贴图与 Gaussian Splatting 表示，到模型后处理（分割、补全、重拓扑、格式转换）及动画绑定与重定向的完整工作流。所有接口均采用[异步任务](../concepts/asynchronous-task.md)模式，需通过 `task_id` 轮询获取结果。

## 支持的模型/功能

Tripo 提供三大类核心能力：

- **基础生成**：支持文生 3D、单图生 3D、多图生 3D 三种输入方式，对应模型 `Tripo/Tripo-H3.1`（高精度，最高 200 万面）和 `Tripo/Tripo-P1.0`（专业级，最高 2 万面）；另提供专用的 `Tripo/Tripo-ImageToSplat` 模型用于生成 Gaussian Splatting 文件（`.splat`）[Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。
- **后处理**：涵盖网格分割（`Tripo/Tripo-Segmentation`, `Tripo/Tripo-SmartSegmentation`）、贴图生成（`Tripo/Tripo-Texture`）、网格补全（`Tripo/Tripo-MeshCompletion`）、重拓扑（`Tripo/Tripo-Retopology`）和格式转换（`Tripo/Tripo-ConvertFormat`）等 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md) 功能。
- **动画**：提供可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`）三步流程，支持人形与多种非人形生物骨骼类型 [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：所有 Tripo 相关 API 当前**仅支持华北2（北京）地域**，且必须使用该地域的 API Key。跨地域调用或使用其他地域 API Key 将失败。

## 关键参数

- **通用必填头**：`Content-Type: application/json`、`Authorization: Bearer <API_KEY>`、`X-DashScope-Async: enable`（同步调用不被支持）。
- **输入控制**：
  - 文生 3D：`input.prompt`（最大 1024 字符）；
  - 单图生 3D：`input.image`（JPEG/PNG，≤20MB，建议 ≥256px）；
  - 多图生 3D：`input.images`（长度为 4 的数组，顺序为前/左/后/右，至少提供前视角）；
  - Gaussian Splat：`input.image`（支持 WebP，其余同上）。
- **质量与几何控制**：
  - `texture_quality`: `standard`/`detailed`/`extreme`（8K）；
  - `geometry_quality`: `standard`/`ultra`（仅 `Tripo-H3.1` 支持）；
  - `face_limit`: 面数上限（`Tripo-H3.1` 最高 2,000,000，`Tripo-P1.0` 为 50–20,000）；
  - `quad`: 是否输出四边面（启用后强制 FBX 格式）；
  - `smart_low_poly`: 是否启用智能低模（仅 `Tripo-H3.1`，面数范围 500–20,000）。
- **种子参数**：`model_seed`（几何）、`texture_seed`（贴图）、`image_seed`（文生 3D 的中间图）均支持确定性复现，取值范围 `-2147483648` 至 `2147483647`。

## 使用方式

1. **开通与配置**：在百炼控制台 [华北2（北京）地域](https://bailian.console.aliyun.com/cn-beijing/model/market) 搜索并开通 Tripo 服务；获取并配置该地域的 API Key [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
2. **异步调用流程**：
   - **步骤一（创建任务）**：向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，获取 `task_id`（有效期 24 小时）；
   - **步骤二（轮询结果）**：使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 定期查询，建议首次延迟 10 秒，后续间隔 15–30 秒，直至 `task_status` 为 `SUCCEEDED` 或 `FAILED`。
3. **链式调用**：后处理任务（如贴图、分割、绑骨）通常需引用前序任务的 `task_id`（通过 `input.original_model_task_id`），且要求账号一致；也可直接传入公网可访问的模型 URL（`input.model_url`）。

## 限制和注意事项

- **地域与认证强约束**：全部 Tripo 接口严格限定于华北2（北京）地域，且 API Key 必须为该地域生成。尝试在其他地域调用或混用 API Key 将返回明确错误（如 `InvalidApiKey`）。
- **输入互斥性**：文生/图生 3D 的 `prompt`、`image`、`images` 三者严格互斥，同时传入将导致 400 错误；同样，`original_model_task_id` 与 `model_url` 在后处理任务中亦为二选一。
- **参数兼容性冲突**：
  - `generate_parts` 与 `texture`/`pbr`/`quad`/`smart_low_poly` 不兼容，同时启用将返回 400 错误；
  - `Tripo-P1.0` 模型忽略 `geometry_quality`、`quad`、`smart_low_poly`、`generate_parts` 等高级参数（不报错但无效）；
  - `Tripo/Tripo-RigCheck` 和 `Tripo/Tripo-AutoRig` 的 `rig_type` 参数若未按 [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md) 返回值指定，可能导致绑骨失败或动画重定向不兼容。
- **文件与格式限制**：输入图像 ≤20MB；3D 模型文件（GLB/FBX/OBJ 等）≤150MB；Gaussian Splat 输出为 `.splat`，不可直接用于传统渲染管线。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)


