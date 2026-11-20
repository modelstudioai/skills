# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供端到端的 3D 内容创作流水线，覆盖从文/图生 3D 模型、Gaussian Splatting 生成，到模型后处理（分割、补全、重拓扑、格式转换）及动画绑定与重定向等完整环节。所有接口均采用[异步调用](../concepts/asynchronous-invocation.md)模式，需通过任务 ID 轮询获取结果，且当前**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供三大类核心能力：

- **基础生成**：  
  - `Tripo/Tripo-H3.1`（高精度网格，最高 200 万面）和 `Tripo/Tripo-P1.0`（专业级，最高 2 万面）支持文生 3D、单图生 3D 和多图生 3D [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)；  
  - `Tripo/Tripo-ImageToSplat` 专用于单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与场景重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：  
  包括网格分割（`Tripo/Tripo-Segmentation` / `Tripo/Tripo-SmartSegmentation`）、贴图生成（`Tripo/Tripo-Texture`）、网格补全（`Tripo/Tripo-MeshCompletion`）、重拓扑（`Tripo/Tripo-Retopology`）、格式转换（`Tripo/Tripo-ConvertFormat`）等，均支持基于前序任务 ID 或直接传入公网模型 URL 的输入方式。

- **动画**：  
  提供可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`）三步流程，支持人形（biped）及多种非人形骨骼类型（如 quadruped、avian）。

> **注意**：文档中 `Tripo/Tripo-AutoRig` 的 `spec: mixamo` 绑骨结果明确禁止用于 `Tripo-AnimationRetarget`，但部分旧版示例未强调此限制，实际集成时须严格校验前序任务的 `spec` 参数。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `model_seed` | 所有生成类（H3.1/P1.0/ImageToSplat/Texture/Retopology 等） | 几何体生成随机种子，相同种子+输入保证网格一致 | `12345` |
| `texture_seed` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Texture` | 贴图生成随机种子，用于控制贴图变体 | `67890` |
| `face_limit` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 输出模型面数上限；`H3.1` 默认自适应，`P1.0` 必填（50–20,000） | `50000` |
| `quad` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 启用四边面输出（强制 FBX 格式） | `true` |
| `generate_parts` | `Tripo/Tripo-H3.1` | 是否生成可编辑部件；开启后 `texture`/`pbr` 必须为 `false`，否则返回 400 错误 | `true` |
| `part_names` | `Tripo/Tripo-Texture`, `Tripo/Tripo-MeshCompletion`, `Tripo/Tripo-ConvertFormat`, `Tripo/Tripo-Retopology` | 指定处理的部件名（如 `tripo_part_0`），需从前序分割任务 GLB 中读取节点名 | `["tripo_part_0"]` |

## 使用方式

所有 3D 相关 API 均遵循统一异步流程：

1. **创建任务**：向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，必须携带：
   - 请求头：`Content-Type: application/json`, `Authorization: Bearer <API_KEY>`, `X-DashScope-Async: enable`
   - 请求体：`model`（固定值）、`input`（含 `prompt`/`image`/`images`/`original_model_task_id`/`model_url` 等）、`parameters`（可选）

2. **轮询结果**：使用返回的 `task_id` 调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，建议间隔 15–30 秒。任务状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`，`task_id` 有效期为 **24 小时**。

> **注意**：文档中 `Tripo-网格分割`（v1.0）与 `Tripo-智能分割`（v2.0）均支持 `ref_image`，但前者明确声明“传入将返回 400 错误”，而后者未提及该限制。实际调用 `Tripo/Tripo-Segmentation` 时若传入 `ref_image`，应预期失败而非静默忽略。

## 限制和注意事项

- **地域与认证**：全部接口**仅限华北2（北京）地域**，且必须使用该地域生成的 API Key；开通服务需在百炼控制台搜索 “Tripo” 并完成授权。
- **输入约束**：
  - 图像输入：JPEG/PNG/WebP，≤20MB，建议分辨率 ≥256×256；
  - 模型输入（GLB/FBX/OBJ 等）：≤150MB；
  - 文本提示词（`prompt`）：≤1024 字符；反向提示词（`negative_prompt`）：≤255 字符。
- **兼容性限制**：
  - `Tripo/Tripo-P1.0` 不支持 `geometry_quality`、`quad`、`smart_low_poly`、`generate_parts` 等参数，传入将被忽略；
  - `Tripo/Tripo-AutoRig` 使用 `spec: mixamo` 时，生成的模型**不可用于** `Tripo-AnimationRetarget`；
  - `Tripo/Tripo-ConvertFormat` 的 `fbx_preset: mixamo` 仅影响导入兼容性，不改变骨骼结构。
- **计费与性能**：高级参数（如 `texture_quality: extreme`、`face_limit` 非默认值、`quad: true`）通常触发更高积分消耗；智能分割、AI 补全等任务耗时较长，建议按文档推荐轮询策略避免超时。

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
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)


