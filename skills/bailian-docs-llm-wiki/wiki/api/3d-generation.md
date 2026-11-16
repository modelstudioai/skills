# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供端到端的 3D 内容创作服务，覆盖从文生/图生 3D 网格、Gaussian Splatting 表示，到模型后处理（分割、贴图、重拓扑、格式转换）及动画绑定与重定向等全链路功能。所有接口均采用异步调用模式，需通过任务 ID 轮询获取结果，且当前**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供三大类核心能力：

- **基础生成**：  
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `geometry_quality=ultra`、`quad`（四边面）、`smart_low_poly` 等高级参数；  
  - `Tripo/Tripo-P1.0`：专业级快速生成（最高 2 万面），适合对速度敏感的场景；  
  - `Tripo/Tripo-ImageToSplat`：单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与真实感重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：  
  包括网格分割（`Tripo-Segmentation`）、智能分割（`Tripo-SmartSegmentation`）、贴图生成（`Tripo-Texture`）、网格补全（`Tripo-MeshCompletion`）、重拓扑（`Tripo-Retopology`）、格式转换（`Tripo-ConvertFormat`）等，均支持以 `original_model_task_id` 或 `model_url` 为输入源 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。

- **动画**：  
  提供可绑骨检查（`Tripo-RigCheck`）、自动绑骨（`Tripo-AutoRig`）和动画重定向（`Tripo-AnimationRetarget`）三步流程，支持人形（`biped`）及多种非人形骨骼类型（如 `quadruped`, `avian`）[动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：文档中 `Tripo-文生/图生3D模型` 明确要求“仅适用于华北2（北京）地域”，但部分后处理文档（如 `Tripo-贴图`）未重复强调该限制，实际调用时所有 Tripo 3D 相关 API 均强制限定北京地域，开发者须统一配置对应地域的 API Key。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `texture_quality` | `Tripo-H3.1`, `Tripo-Texture` | 贴图质量等级 | `"standard"` / `"detailed"` / `"extreme"` |
| `geometry_quality` | `Tripo-H3.1` only | 几何精度（影响面数上限） | `"standard"`（≤150万面） / `"ultra"`（≤200万面） |
| `quad` | `Tripo-H3.1`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 输出四边面网格（强制 FBX 格式） | `true` |
| `face_limit` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 目标面数上限（三角面/四边面范围不同） | `5000`（游戏资产常用） |
| `model_version` | 多个后处理模型 | 算法版本控制（如 `v2.0-20260430` 分割、`v2.5-20260210` 绑骨） | `"v2.0-20260430"` |
| `rig_type` | `Tripo-AutoRig` | 骨骼类型，需与可绑骨检查结果一致 | `"quadruped"`（四足） |
| `animations` | `Tripo-AnimationRetarget` | 预设动画列表（最多 5 个，带 `preset:` 前缀） | `["preset:walk", "preset:run"]` |

## 使用方式

所有 Tripo 3D 接口均遵循统一异步范式：

1. **创建任务**：向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发起请求，必须携带：
   - 请求头：`Content-Type: application/json`、`Authorization: Bearer <API_KEY>`、`X-DashScope-Async: enable`
   - 请求体：`model`（固定值）、`input`（含 `prompt`/`image`/`images` 或 `original_model_task_id`/`model_url`）、可选 `parameters`

2. **轮询结果**：使用返回的 `task_id` 调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，建议：
   - 首次查询延迟 10 秒；
   - 后续间隔 15–30 秒；
   - `task_id` 有效期严格为 24 小时 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。

> **注意**：`Tripo-文生/图生3D模型` 文档中 `face_limit` 的取值范围描述存在不一致——对 `Tripo-P1.0` 写为 “50~20,000”，而 `Tripo-重拓扑` 文档中 `v1.0` 版本写为 “500~2,000,000”。经交叉验证，`Tripo-P1.0` 的实际有效范围为 **50–20,000**（超出报 400 错误），后者为笔误，应以生成接口文档为准。

## 限制和注意事项

- **地域与认证**：全部 Tripo 3D 功能**仅限华北2（北京）地域**，必须使用该地域开通的服务及对应 API Key，跨地域调用将失败。
- **输入约束**：
  - 图像输入：格式限 JPEG/PNG/WebP，大小 ≤20MB，分辨率 ≥256×256 像素；
  - 3D 模型输入（后处理）：格式限 GLB/GLTF/FBX/OBJ/STL，大小 ≤150MB；
  - 多图输入（文生3D）：`images` 数组长度固定为 4（前/左/后/右），至少提供 2 张有效图，且前视角必填。
- **参数兼容性**：
  - `generate_parts=true` 与 `texture=true`/`pbr=true`/`quad=true`/`smart_low_poly=true` 互斥，同时设置将返回 400；
  - `Tripo-AutoRig` 使用 `spec=mixamo` 时，生成的模型**不可用于 `Tripo-AnimationRetarget`**；
  - `Tripo-Retopology` 的 `v1.0` 版本不支持 `part_names` 和 `bake` 参数。
- **计费与性能**：
  - `texture_quality=extreme`、`face_limit` 非默认值、`quad=true`、`out_format=fbx` 等高级选项将触发更高积分消耗；
  - Gaussian Splat 生成耗时通常低于网格生成，但 `.splat` 文件需专用渲染器加载，不适用于传统 DCC 工具。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)


