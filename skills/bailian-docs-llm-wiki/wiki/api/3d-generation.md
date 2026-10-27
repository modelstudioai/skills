# 3d generation

百炼平台的3D生成能力基于Tripo模型，提供从文本/图像到3D资产的一站式生成与后处理服务，覆盖文生3D、图生3D、Gaussian Splatting、网格分割、贴图生成、格式转换、自动绑骨及动画重定向等完整工作流。所有接口均采用异步调用模式，需通过任务ID轮询获取结果。

## 支持的模型/功能

- **基础生成**：支持文生3D（`Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`）、单图/多图生3D，以及单图生成Gaussian Splat（`Tripo/Tripo-ImageToSplat`）[Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。
- **后处理**：包括网格分割（`Tripo/Tripo-Segmentation`, `Tripo/Tripo-SmartSegmentation`）、贴图生成（`Tripo/Tripo-Texture`）、重拓扑（`Tripo/Tripo-Retopology`）、网格补全（`Tripo/Tripo-MeshCompletion`）、格式转换（`Tripo/Tripo-ConvertFormat`）等 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。
- **动画管线**：支持可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`）[动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：`Tripo/Tripo-P1.0`不支持`geometry_quality`、`quad`、`smart_low_poly`、`generate_parts`等参数，传入将被忽略；而`Tripo/Tripo-H3.1`支持全部高级参数，但部分组合互斥（如`generate_parts`与`pbr`同时启用会返回400错误）。

## 关键参数

| 参数名 | 适用模型 | 说明 |
|--------|----------|------|
| `texture_quality` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Texture` | 取值`standard`/`detailed`/`extreme`，控制贴图分辨率与保真度。`extreme`对应8K贴图。 |
| `face_limit` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 面数上限。`Tripo-P1.0`范围为50–20,000；`Tripo-H3.1`在`ultra`精度下最高支持2,000,000面。 |
| `quad` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 是否输出四边面网格。启用后强制输出FBX格式，且默认面数为10,000（未设`face_limit`时）。 |
| `generate_parts` | `Tripo/Tripo-H3.1` | 是否生成可编辑部件。启用后`texture`和`pbr`必须为`false`，否则返回400错误 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。 |
| `model_version` | 多个后处理接口 | 如`Tripo/Tripo-Segmentation`支持`v1.0-20250506`（几何分割）与`v2.0-20260430`（语义+几何），版本不匹配将返回400错误。 |

## 使用方式

1. **地域与认证**：所有3D接口**仅支持华北2（北京）地域**，必须使用该地域的API Key，并配置`X-DashScope-Async: enable`请求头。
2. **异步流程**：统一采用“创建任务 → 轮询查询”两步法：
   - 步骤1：`POST /api/v1/services/aigc/video-generation/3d-generation`，获取`task_id`（有效期24小时）；
   - 步骤2：`GET /api/v1/tasks/{task_id}`，建议首次查询延迟10秒，后续每15–30秒轮询一次。
3. **输入方式**：
   - 文生3D：传`prompt`（≤1024字符）；
   - 单图生3D：传`image`（JPEG/PNG，≤20MB，建议≥256px）；
   - 多图生3D：传`images`数组（长度固定为4，顺序为前/左/后/右）；
   - 后处理任务：通过`original_model_task_id`引用前序任务，或直接传`model_url`（GLB/FBX/OBJ等，≤150MB）。

## 限制和注意事项

- **地域强约束**：所有文档明确要求“仅适用于华北2（北京）地域”，跨地域调用必然失败，且API Key必须与地域匹配。
- **任务依赖**：后处理类接口（如贴图、分割、重拓扑）均要求前序任务已成功执行，且`original_model_task_id`必须由同一账号创建，跨账号引用返回400错误。
- **文件限制**：输入图像≤20MB，3D模型文件≤150MB；多图生3D的`images`数组必须严格为4元素，缺失视角需用空对象`{}`占位。
- **参数兼容性**：`generate_parts`与`pbr`/`texture`互斥；`quad=true`时`Tripo/Tripo-ConvertFormat`强制输出FBX；`Tripo/Tripo-AutoRig`中`spec=mixamo`的模型无法用于后续动画重定向。
- **计费提示**：高级参数（如非默认`texture_size`、`face_limit`、`quad`）可能触发高级转换计费，详见各接口文档。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)


