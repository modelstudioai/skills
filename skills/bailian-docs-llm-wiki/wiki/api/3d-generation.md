# 3d generation

百炼平台提供基于 Tripo 模型的端到端 3D 内容生成与后处理能力，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、网格分割、重拓扑、格式转换、自动绑骨及动画重定向等完整工作流。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供三类核心能力：

- **基础生成**：  
  - `Tripo/Tripo-H3.1`（高精度，最高 200 万面）和 `Tripo/Tripo-P1.0`（专业级，最高 2 万面）支持文生/单图生/多图生 3D 模型 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)；  
  - `Tripo/Tripo-ImageToSplat` 支持单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与真实感重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：  
  包括贴图生成（PBR/8K）、网格分割（v1.0/v2.0）、智能分割（端到端建模+分割）、网格补全（AI 补全/快速封口）、重拓扑（v1.0 基础减面 / v2.0 智能低模）、格式转换（GLTF/USDZ/FBX/STL 等）等，详见 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。

- **动画**：  
  支持可绑骨检查、自动绑骨（biped/quadruped 等 7 类骨骼类型）及动画重定向（预设 walk/run 等动作），要求前序任务为 Tripo 自动绑骨且 `spec` 不为 `mixamo` [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：文档中 `Tripo/Tripo-SmartSegmentation` 的 `transform` 参数要求为 16 元素数组（列主序），而部分示例未明确说明顺序；实际使用请严格按 `[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]` 格式传入，避免因行列序混淆导致失败。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `model_seed` | 所有生成类（H3.1/P1.0/ImageToSplat） | 控制几何体随机性，相同 seed + 输入 = 相同网格 | `42` |
| `texture_seed` | H3.1/P1.0/Texture | 控制贴图随机性，可用于固定几何体、迭代贴图 | `123` |
| `face_limit` | H3.1/P1.0/Retopology/ConvertFormat | 面数上限，H3.1 默认 150 万面，P1.0 为 50–20,000 | `50000` |
| `quad` | H3.1/Retopology/ConvertFormat | 启用四边面输出（强制 FBX 格式） | `true` |
| `pbr` & `texture` | H3.1/P1.0/Texture | 控制 PBR 材质与贴图生成，二者需协同设置（如 `pbr=true` 时 `texture` 自动生效） | `true` |
| `part_names` | Segmentation/MeshCompletion/Retopology/ConvertFormat | 指定部件名称列表（如 `["tripo_part_0"]`），需从 GLB 节点名提取 | `["tripo_part_0", "tripo_part_1"]` |

> **注意**：`generate_parts`（部件生成）与 `pbr`/`texture`/`quad`/`smart_low_poly` 互斥；若同时启用，将返回 400 错误 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。务必按文档约束组合参数。

## 使用方式

所有接口均遵循统一异步流程：

1. **创建任务**：  
   - 请求方法：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   - 必须携带请求头：`Content-Type: application/json`、`Authorization: Bearer <API_KEY>`、`X-DashScope-Async: enable`  
   - 请求体中 `model` 字段指定模型标识（如 `"Tripo/Tripo-H3.1"`），`input` 和 `parameters` 按各模型要求填充。

2. **轮询结果**：  
   - 请求方法：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议轮询策略：首次提交后 10 秒查询，后续每 15–30 秒一次；`task_id` 有效期为 **24 小时**。  
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；`SUCCEEDED` 响应中 `output` 字段包含产物 URL（如 `base_model_url`、`pbr_model_url` 或 `splat_url`）。

- **地域与密钥**：必须使用华北2（北京）地域的 API Key，并在控制台开通 Tripo 服务 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

## 限制和注意事项

- **地域强绑定**：全部 3D 接口仅支持华北2（北京）地域，跨地域调用将失败。
- **输入限制**：  
  - 图像：PNG/JPEG/WebP，≤20MB，建议 ≥256×256 像素；  
  - 3D 模型（GLB/FBX/OBJ 等）：≤150MB；  
  - 多图输入（`images`）：严格 4 元素数组，顺序为 `[front, left, back, right]`，缺失视角填 `null`。
- **兼容性约束**：  
  - `Tripo-动画重定向` 仅接受 `spec=tripo` 的绑骨结果，`spec=mixamo` 不可用；  
  - `Tripo-重拓扑` 的 `v1.0` 版本不支持 `part_names` 和 `bake` 参数；  
  - `Tripo-格式转换` 中 `quad=true` 时强制输出 FBX，且 `face_limit` 默认为 10,000。
- **计费提示**：`face_limit` 非默认值、`quad=true`、`texture_size≠4096`、`texture_format≠JPEG` 等高级参数将触发额外计费，详见各接口文档。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
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


