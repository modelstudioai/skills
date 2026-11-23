# 3d generation

百炼平台的3D生成能力基于Tripo模型系列，提供从文本/图像到3D资产的一站式生成与后处理流水线，覆盖3D模型生成、Gaussian Splatting、网格分割、贴图、重拓扑、格式转换及动画绑定等核心环节。所有接口均采用异步调用模式，需通过任务ID轮询获取结果，且当前全部功能仅支持华北2（北京）地域。

## 支持的模型/功能

- **基础生成**：支持文生3D（`Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`）、单图生3D、多图生3D，输出GLB格式高精度模型；同时提供[图片生成Gaussian Splat](raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)（`Tripo/Tripo-ImageToSplat`），输出`.splat`文件用于实时渲染。
- **后处理**：包含网格分割（`Tripo/Tripo-Segmentation`, `Tripo/Tripo-SmartSegmentation`）、贴图（`Tripo/Tripo-Texture`）、网格补全（`Tripo/Tripo-MeshCompletion`）、重拓扑（`Tripo/Tripo-Retopology`）、格式转换（`Tripo/Tripo-ConvertFormat`）等完整工具链。
- **动画支持**：提供可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`）三步流程，支持人形与非人形生物骨骼类型。

> **注意**：文档中多次强调“本文档仅适用于华北2（北京）地域”，但[Tripo-文生/图生3D模型](raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)未明确说明地域限制，而其他14篇文档（如文档2、4、5等）均强制要求北京地域及对应API Key。实际开发中应统一使用北京地域，避免因地域不一致导致调用失败。

## 关键参数

- **通用必填头**：所有请求必须携带 `Content-Type: application/json`、`Authorization: Bearer <key>` 和 `X-DashScope-Async: enable`。
- **输入控制**：
  - 文生3D：通过 `prompt` 字符串（≤1024字符）描述目标模型；
  - 图生3D：`image`（单图URL）或 `images`（4元素数组，按前/左/后/右顺序）；
  - Gaussian Splat：仅支持 `image` 单图输入，格式为PNG/JPEG/WebP，分辨率建议≥256×256。
- **质量与性能**：
  - `geometry_quality`（`H3.1`专属）：`standard`（≤150万面）或 `ultra`（≤200万面）；
  - `texture_quality`：`standard`/`detailed`/`extreme`（8K），影响贴图分辨率与生成耗时；
  - `face_limit`：在重拓扑、格式转换及H3.1生成中控制目标面数，取值范围依模型版本严格限定。
- **种子控制**：`model_seed`（几何）、`texture_seed`（贴图）、`image_seed`（文生图阶段）均支持固定随机性，便于结果复现与AB测试。

## 使用方式

1. **开通与配置**：在百炼控制台[华北2（北京）地域](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索并开通Tripo服务，配置对应地域的API Key至环境变量。
2. **异步任务流**：
   - **步骤1（创建）**：向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 提交请求，获取 `task_id`；
   - **步骤2（轮询）**：使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，建议首次查询延迟10秒，后续间隔15–30秒；
   - **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`，`task_id`有效期为24小时。
3. **输入依赖管理**：后处理类接口（如贴图、分割、重拓扑）普遍支持两种输入方式：
   - 通过 `original_model_task_id` 引用前序任务输出（需同账号、任务已成功）；
   - 直接传入 `model_url`（公网可访问的GLB/FBX/OBJ等，≤150MB）。

## 限制和注意事项

- **地域强约束**：除[3D模型生成](raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)主文档外，其余14篇原始文档（如文档2、4、5、6等）均明确要求“仅适用于华北2（北京）地域”。开发者必须确保Workspace ID、API Key、请求Endpoint三者地域一致，否则返回400或认证失败。
- **文件与格式限制**：
  - 图像输入：PNG/JPEG/WebP，≤20MB，分辨率宽高∈[20, 6000]；
  - 3D模型输入：GLB/GLTF/FBX/OBJ/STL，≤150MB；
  - Gaussian Splat输出仅支持`.splat`，不可直接用于传统引擎，需专用查看器。
- **参数兼容性冲突**：
  - `Tripo/Tripo-H3.1` 的 `generate_parts` 与 `texture`/`pbr`/`quad`/`smart_low_poly` 互斥，开启部件生成时必须禁用贴图与PBR；
  - `Tripo/Tripo-AutoRig` 中 `spec: mixamo` 绑定的模型**不可用于**[Tripo-动画重定向](raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)，此限制在文档14中明确指出；
  - `Tripo/Tripo-Retopology` 的 `v1.0` 版本不支持 `part_names` 和 `bake` 参数，而 `v2.0` 支持。
- **计费与资源**：高级操作（如`quad=true`、`face_limit`自定义、非默认`texture_quality`）按更高积分计费；轮询查询接口RPS默认为20，高频轮询需配置异步回调。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)


