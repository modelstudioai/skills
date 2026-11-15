# 3d generation

百炼平台提供基于 Tripo 模型的端到端 3D 内容生成与后处理能力，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、贴图生成、网格分割、重拓扑、格式转换及动画绑定等核心链路。所有接口均采用[异步调用](../concepts/asynchronous-invocation.md)模式，需通过任务 ID 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

- **基础生成**：`Tripo/Tripo-H3.1`（高精度，最高200万面）、`Tripo/Tripo-P1.0`（专业级，最高2万面）支持文生3D、单图生3D、多图生3D；`Tripo/Tripo-ImageToSplat` 专用于单图生成 Gaussian Splat（`.splat` 格式）[Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。
- **后处理**：包括贴图生成（`Tripo/Tripo-Texture`）、网格分割（`Tripo/Tripo-Segmentation`）、智能分割（`Tripo/Tripo-SmartSegmentation`）、网格补全（`Tripo/Tripo-MeshCompletion`）、重拓扑（`Tripo/Tripo-Retopology`）、格式转换（`Tripo/Tripo-ConvertFormat`）等 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。
- **动画管线**：包含可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`）三阶段能力 [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：`Tripo/Tripo-ImageToSplat` 与 `Tripo/Tripo-3D-Generation` 功能定位不同——前者输出不可编辑的 `.splat` 渲染资产，后者输出可编辑的网格（GLB/FBX）及贴图，二者不可互换使用。

## 关键参数

| 参数名 | 适用模型 | 说明 |
|--------|----------|------|
| `texture_quality` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Texture` | 取值 `standard`/`detailed`/`extreme`，控制贴图分辨率（最高8K） |
| `geometry_quality` | `Tripo-H3.1` only | `standard`（≤150万面）或 `ultra`（≤200万面），`Tripo-P1.0` 忽略此参数 |
| `face_limit` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 面数上限，取值范围因模型而异（如 `Tripo-P1.0` 为 50–20,000） |
| `quad` | `Tripo-H3.1`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 是否输出四边面（启用后强制输出 FBX） |
| `pbr` & `texture` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Texture` | 控制是否生成 PBR 材质及基础贴图；二者需同时设为 `false` 才输出无贴图模型 |
| `model_version` | `Tripo-Texture`, `Tripo-Segmentation`, `Tripo-Retopology`, `Tripo-AutoRig` | 指定算法版本（如 `v2.0-20260430`），版本不匹配将返回 400 错误 |

## 使用方式

1. **前提条件**：  
   - 在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务；  
   - 获取并配置华北2（北京）地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，且必须通过环境变量或请求头 `Authorization: Bearer sk-xxx` 传入；  
   - 所有接口 URL 均为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`（创建任务）和 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`（轮询结果）。

2. **调用流程（统一异步）**：  
   - **步骤1（创建）**：`POST /3d-generation`，必须携带请求头 `X-DashScope-Async: enable`，否则报错“current user api does not [support](../guides/support.md) synchronous calls”；  
   - **步骤2（轮询）**：使用返回的 `task_id` 调用 `GET /tasks/{task_id}`，建议首次查询延迟 10 秒，后续间隔 15–30 秒；`task_id` 有效期为 24 小时，超时返回 `UNKNOWN` 状态。

3. **输入约束**：  
   - 图像输入：支持 JPEG/PNG/WebP，≤20MB，建议分辨率 ≥256×256；  
   - 3D 模型输入（如 GLB/FBX）：≤150MB，仅支持公网可访问 URL；  
   - 多图输入（`images` 字段）：严格按 `[front, left, back, right]` 顺序，至少提供 front 视角。

## 限制和注意事项

- **地域强绑定**：所有文档明确强调“仅适用于华北2（北京）地域”，跨地域调用必然失败，且 API Key 必须与该地域匹配 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。  
- **任务依赖关系**：后处理类接口（如 `Tripo-Texture`, `Tripo-Retopology`）常需引用前序任务 `task_id`，且要求**账号一致**；引用其他账号任务或前序任务未成功，均返回 400 错误。  
- **参数兼容性冲突**：  
  > **注意**：`generate_parts` 与 `texture`/`pbr`/`quad`/`smart_low_poly` 不兼容——若同时开启，将返回 400 错误；`Tripo-P1.0` 模型传入 `geometry_quality` 或 `quad` 参数会被静默忽略，但 `face_limit` 仍生效。  
- **计费与高级功能**：`quad=true`、`face_limit` 非默认值、`texture_size≠4096`、`texture_format≠JPEG` 等操作均触发“高级转换”计费，需在调用前确认配额。  
- **模型兼容性**：`Tripo-AnimationRetarget` 明确禁止使用 `spec=mixamo` 的绑骨结果；`Tripo-RigCheck` 是 `Tripo-AutoRig` 的前置推荐步骤，避免因骨骼类型不匹配导致失败。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


