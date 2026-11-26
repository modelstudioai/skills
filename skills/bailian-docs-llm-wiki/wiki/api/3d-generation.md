# 3d generation

百炼平台的 3D generation 能力基于 Tripo 模型提供端到端的 3D 内容生成与后处理服务，覆盖从文/图生 3D 模型、Gaussian Splatting 生成，到网格分割、重拓扑、贴图、动画绑定与重定向等完整工作流。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果。

## 支持的模型/功能

3D generation 当前由 Tripo 系列模型提供，分为三大类能力：

- **基础生成**  
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `texture_quality`、`geometry_quality`、`pbr`、`quad`、`smart_low_poly` 等精细控制 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)  
  - `Tripo/Tripo-P1.0`：快速专业生成（最高 2 万面），适合对延迟敏感的场景  
  - `Tripo/Tripo-ImageToSplat`：单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与真实感重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)

- **后处理**  
  包括网格分割（`Tripo-Segmentation` / `Tripo-SmartSegmentation`）、重拓扑（`Tripo-Retopology`）、格式转换（`Tripo-ConvertFormat`）、贴图生成（`Tripo-Texture`）、网格补全（`Tripo-MeshCompletion`）等，均支持通过 `original_model_task_id` 或 `model_url` 接入前序任务输出 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)

- **动画**  
  提供可绑骨检查（`Tripo-RigCheck`）、自动绑骨（`Tripo-AutoRig`）和动画重定向（`Tripo-AnimationRetarget`）三步流程，其中绑骨需使用 `spec: tripo`（非 `mixamo`）才能用于后续重定向 [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)

> **注意**：文档 12 明确指出 `Tripo-自动绑骨` 的 `spec` 参数若设为 `mixamo`，则生成的模型**不可用于** `Tripo-动画重定向`；而文档 13 在适用范围中再次强调“`spec`不能为`mixamo`”，二者一致，但开发者易忽略该强约束，务必在绑骨阶段确认。

## 关键参数

| 参数名 | 所属模型 | 类型 | 说明 |
|--------|----------|------|------|
| `X-DashScope-Async` | 全部 | header（必填） | 必须设为 `"enable"`，同步调用不被支持 |
| `model` | 全部 | body（必填） | 如 `"Tripo/Tripo-H3.1"`、`"Tripo/Tripo-ImageToSplat"` 等，值严格固定，大小写敏感 |
| `input.image` / `input.images` / `input.prompt` | `Tripo-H3.1/P1.0` | body（互斥） | 文生/单图生/多图生 3D 的输入方式；多图生要求 `images` 数组长度为 4（前/左/后/右），空视角用 `{}` 占位 |
| `parameters.texture_quality` | `Tripo-H3.1/P1.0`, `Tripo-Texture` | body（可选） | 取值 `standard`/`detailed`/`extreme`；`extreme` 对应 8K 贴图，积分消耗更高 |
| `parameters.model_version` | 多个后处理模型 | body（可选） | 如 `Tripo-Segmentation` 支持 `v1.0-20250506`（几何分割）与 `v2.0-20260430`（语义+几何），版本不匹配将返回 400 错误 |
| `parameters.animations` | `Tripo-AnimationRetarget` | body（条件必填） | 数组形式，最多 5 个，每个必须带 `preset:` 前缀（如 `"preset:walk"`），名称区分大小写 |

## 使用方式

1. **地域与认证**：所有接口**仅支持华北2（北京）地域**，必须使用该地域的 API Key，并配置 `Authorization: Bearer sk-xxx` 与 `X-DashScope-Async: enable` 请求头。  
2. **异步流程**：统一采用两步法：  
   - **步骤1（创建任务）**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`，传入 `model`、`input` 和 `parameters`，获取 `task_id`（24 小时有效）；  
   - **步骤2（轮询结果）**：调用 `GET /api/v1/tasks/{task_id}` 查询状态，直到 `task_status == "SUCCEEDED"`，响应中 `output.result_url` 或类似字段提供产物下载地址。  
3. **输入链路**：后处理类接口（如分割、重拓扑、贴图）普遍支持两种输入源：  
   - `original_model_task_id`：引用同一账号下已成功执行的前序任务 ID（如 `Tripo-H3.1` 生成任务）；  
   - `model_url`：直接传入公网可访问的模型文件 URL（GLB/GLTF/FBX/OBJ/STL，≤150MB）。  

## 限制和注意事项

- **地域硬约束**：全部 3D generation 接口仅限华北2（北京）地域调用，跨地域请求会失败，且 API Key 必须为该地域开通 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。  
- **模型兼容性**：  
  - `Tripo-动画重定向` 仅接受 `Tripo-自动绑骨` 输出的模型，且 `spec` 必须为 `tripo`（非 `mixamo`）；  
  - `Tripo-重拓扑` 的 `part_names` 参数仅在前序任务为 `Tripo-网格分割` 或 `Tripo-智能分割` 时生效，部件名需从 GLB 文件节点中提取（如 `tripo_part_0`），而非 API 响应字段；  
  - `Tripo-贴图` 的 `texture_prompt` 在前序任务**不是** `Tripo-文生/图生3D模型` 时为必填项，否则任务失败。  
- **格式与计费**：  
  - `quad: true`（四边面）在 `Tripo-Retopology`、`Tripo-ConvertFormat` 中强制输出 FBX，且按高级转换计费；  
  - `Tripo-格式转换` 中 `texture_size ≠ 4096`、`texture_format ≠ JPEG`、`flatten_bottom: true` 等均触发高级转换计费；  
  - `Tripo-动画重定向` 按 `animations` 数组长度计费（最多 5 个），`animation` 单值参数已废弃，仅作兼容。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)


