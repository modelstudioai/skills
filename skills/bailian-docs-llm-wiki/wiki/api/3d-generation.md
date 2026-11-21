# 3d generation

百炼平台的 3d generation 能力基于 Tripo 模型提供端到端的 3D 内容生成与后处理服务，覆盖从文/图生 3D 网格、Gaussian Splatting 表示，到网格分割、重拓扑、格式转换、自动绑骨及动画重定向等完整工作流。所有接口均采用[异步调用](../concepts/asynchronous-invocation.md)模式，需通过 `task_id` 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

- **基础生成**：  
  - 文生 3D、单图生 3D、多图生 3D（[Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)）  
  - 图片生成 Gaussian Splat（.splat 格式，适用于实时渲染）（[Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)）

- **后处理能力**：  
  - 网格分割（`Tripo/Tripo-Segmentation`）、智能分割（`Tripo/Tripo-SmartSegmentation`）  
  - 网格补全（AI 补全 / 快速封口）、重拓扑（v1.0 基础减面 / v2.0 智能低模）、贴图生成（PBR/8K）、格式转换（GLTF/USDZ/FBX/STL 等）  
  - 动画管线：可绑骨检查 → 自动绑骨 → 动画重定向（[Tripo-动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)）

> **注意**：文档中多次强调“仅适用于华北2（北京）地域”，但部分后处理接口（如 `Tripo-贴图`、`Tripo-网格分割`）在参数说明中未明确重复该限制，实际调用时仍须严格使用北京地域 API Key 和 endpoint，否则返回鉴权失败。

## 关键参数

| 参数名 | 适用模型 | 说明 |
|--------|----------|------|
| `model` | 所有接口必填 | 固定值，如 `Tripo/Tripo-H3.1`、`Tripo/Tripo-ImageToSplat`、`Tripo/Tripo-Retopology` 等，不可省略或拼写错误 |
| `X-DashScope-Async: enable` | 所有请求头必填 | 异步标识，缺失将报错 `"current user api does not support synchronous calls"` |
| `input.image` / `input.images` / `input.prompt` | 生成类接口互斥 | 文生 3D 用 `prompt`；单图用 `image`（URL）；多图用 `images`（4 元素数组，顺序为前/左/后/右） |
| `parameters.texture_quality` | 生成/贴图类接口 | 取值 `standard`/`detailed`/`extreme`（8K），影响质量与耗时 |
| `parameters.geometry_quality` | 仅 `Tripo/Tripo-H3.1` | `standard`（≤150万面）或 `ultra`（≤200万面）；`Tripo/Tripo-P1.0` 传入被忽略 |
| `parameters.face_limit` | 多个后处理接口 | 面数上限，但不同接口取值范围不一致（如重拓扑 v2.0 为 500–20,000，而生成类 H3.1 为 500–2,000,000），需按具体文档校验 |

## 使用方式

1. **前提条件**：  
   - 在 [百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/model/market) 开通 Tripo 服务；  
   - 获取并配置北京地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，推荐设为环境变量 `DASHSCOPE_API_KEY`；  
   - 准备业务空间 ID（WorkspaceId），用于构造 endpoint。

2. **标准异步流程**：  
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     请求体含 `model`、`input`、`parameters`，返回 `task_id`（有效期 24 小时）。  
   - **步骤2：轮询结果**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议首次查询延迟 10 秒，后续间隔 15–30 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`。

3. **输入复用**：  
   - 后处理任务（如贴图、分割、重拓扑）支持 `original_model_task_id`（引用前序任务输出）或 `model_url`（直接传公网 URL）；  
   - `original_model_task_id` 必须与当前账号一致，且前序任务状态为 `SUCCEEDED`。

## 限制和注意事项

- **地域强绑定**：全部接口仅支持华北2（北京）地域，endpoint、API Key、控制台开通均需在北京地域操作，跨地域调用必然失败。
- **文件限制**：  
  - 输入图像：JPEG/PNG/WebP，≤20MB，建议分辨率 ≥256×256；  
  - 输入 3D 模型（GLB/FBX/OBJ 等）：≤150MB；  
  - 输出模型面数：`Tripo/Tripo-P1.0` 严格限制为 50–20,000 面，超限返回 400 错误。
- **参数兼容性冲突**：  
  > **注意**：`Tripo/Tripo-H3.1` 的 `generate_parts` 参数与 `texture`、`pbr`、`quad`、`smart_low_poly` 不兼容；若同时启用，将返回 400 错误。文档 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md) 明确要求“如需生成部件，`texture` 和 `pbr` 可不传或设为 `false`，且不要传入 `texture_quality`、`quad` 和 `smart_low_poly`”。
- **计费与版本差异**：  
  - `model_version`（如 `v2.0-20260430` 分割、`v2.5-20260210` 绑骨）影响算法能力与计费等级，旧版参数（如 `animation`）已废弃但向后兼容；  
  - 高级转换（如 `quad=true`、`texture_size≠4096`）按高级规格计费，需留意成本。

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
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


