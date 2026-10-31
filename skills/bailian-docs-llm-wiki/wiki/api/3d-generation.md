# 3d generation

百炼平台的 3D generation 能力基于 Tripo 模型提供端到端的 3D 内容生成与后处理服务，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、网格分割、重拓扑、格式转换、自动绑骨及动画重定向等核心流程。所有接口均采用[异步任务](../concepts/asynchronous-task.md)模式（创建任务 → 轮询查询），且当前仅支持华北2（北京）地域。

## 支持的模型/功能

Tripo 提供两类基础生成能力与丰富的后处理模块：

- **基础生成**：
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `geometry_quality=ultra`、`quad`、`smart_low_poly`、`generate_parts` 等高级参数。
  - `Tripo/Tripo-P1.0`：专业级快速生成（最高 2 万面），适用于对速度敏感的场景，不支持 `geometry_quality`、`quad`、`smart_low_poly`、`generate_parts` 等参数。
  - `Tripo/Tripo-ImageToSplat`：单图生成 `.splat` 文件，适用于实时渲染与真实感重建，[详见 Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**（均需前置 3D 模型任务或公网 URL）：
  - **分割类**：`Tripo/Tripo-Segmentation`（几何/语义分割）、`Tripo/Tripo-SmartSegmentation`（端到端图像/模型输入分割）。
  - **优化类**：`Tripo/Tripo-Retopology`（智能减面）、`Tripo/Tripo-MeshCompletion`（AI 补全/快速封口）、`Tripo/Tripo-Texture`（PBR/8K 贴图生成）。
  - **转换类**：`Tripo/Tripo-ConvertFormat`（GLTF/USDZ/FBX 等多格式导出，含烘焙、UV 合并、朝向控制等）。
  - **动画类**：`Tripo/Tripo-RigCheck`（可绑骨检查）、`Tripo/Tripo-AutoRig`（自动绑骨）、`Tripo/Tripo-AnimationRetarget`（预设动画应用），[详见 Tripo-动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：`Tripo/Tripo-ImageToSplat` 与 `Tripo/Tripo-3D-Generation` 的目标产物本质不同（点云 vs 网格），不可互换使用；前者不输出 GLB/FBX，后者不支持直接生成 `.splat`。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `texture_quality` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Texture` | 贴图质量等级 | `"standard"` / `"detailed"` / `"extreme"` |
| `geometry_quality` | `Tripo/Tripo-H3.1` only | 几何精度（`P1.0` 忽略） | `"standard"` / `"ultra"` |
| `quad` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 输出四边面（强制 FBX 格式） | `true` |
| `generate_parts` | `Tripo/Tripo-H3.1` only | 输出可编辑部件（禁用 `texture`/`pbr`） | `true` |
| `face_limit` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 面数上限（取值范围因模型而异） | `50000`（游戏资产推荐） |
| `model_version` | 多个后处理模型 | 算法版本（如 `v2.0-20260430` for Segmentation） | `"v2.0-20260430"` |
| `rig_type` | `Tripo/Tripo-AutoRig`, `Tripo/Tripo-AnimationRetarget` | 骨骼类型（必须与 `RigCheck` 结果一致） | `"biped"` / `"quadruped"` |

> **注意**：`Tripo/Tripo-H3.1` 的 `face_limit` 在 `geometry_quality=ultra` 时上限为 2,000,000；而 `Tripo/Tripo-P1.0` 严格限制在 50–20,000，超出即返回 400 错误，[参见 Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。

## 使用方式

1. **前提条件**：
   - 在华北2（北京）地域开通 Tripo 服务（控制台搜索“Tripo”）。
   - 配置该地域的 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。
   - 所有请求头必须包含：`Content-Type: application/json`、`Authorization: Bearer <key>`、`X-DashScope-Async: enable`。

2. **通用调用流程（异步）**：
   - **步骤1（创建）**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
     - 请求体中指定 `model`（如 `"Tripo/Tripo-H3.1"`）、`input`（`prompt`/`image`/`images` 三选一）和 `parameters`。
     - 成功响应返回 `task_id`（24 小时有效）。
   - **步骤2（轮询）**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
     - 建议首次查询延迟 10 秒，之后每 15–30 秒轮询一次。
     - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`。

3. **输入方式约束**：
   - 文生3D：仅填 `prompt`（≤1024 字符）。
   - 单图生3D：仅填 `image`（JPEG/PNG，≤20MB，建议 ≥256×256）。
   - 多图生3D：仅填 `images`（长度为 4 的数组，顺序为前/左/后/右，至少 2 张有效）。
   - 后处理任务：通过 `original_model_task_id`（同账号、已成功）或 `model_url`（GLB/GLTF/FBX/OBJ/STL，≤150MB）传入源模型。

## 限制和注意事项

- **地域与认证**：全部接口**仅限华北2（北京）地域**，且必须使用该地域的 API Key；跨地域调用或 Key 不匹配将报错。
- **任务依赖**：
  - 后处理任务（如 `Tripo/Tripo-Texture`、`Tripo/Tripo-Retopology`）引用 `original_model_task_id` 时，要求前序任务**已成功执行**且**由同一账号发起**，否则返回 400。
  - `Tripo/Tripo-AnimationRetarget` 要求前序 `AutoRig` 任务的 `spec` **不能为 `mixamo`**，否则无法重定向。
- **参数兼容性**：
  - `generate_parts=true` 时，`texture` 和 `pbr` 必须为 `false`，且不得传入 `texture_quality`、`quad`、`smart_low_poly`，否则返回 400。
  - `Tripo/Tripo-P1.0` 传入 `geometry_quality`、`quad` 等 H3.1 专属参数会被忽略（不报错），但实际无效。
- **文件与格式**：
  - 输入图像：JPEG/PNG/WebP（`ImageToSplat` 支持 WebP；`3D-Generation` 仅支持 JPEG/PNG）。
  - 输入模型：GLB/GLTF/FBX/OBJ/STL（≤150MB）。
  - 输出格式：`quad=true` 时强制 FBX；`out_format=glb` 为默认值。
- **计费与性能**：
  - `face_limit`、`texture_quality=extreme`、`quad=true`、`animate_in_place=true` 等选项可能触发高级计费。
  - Gaussian Splatting 任务耗时通常短于高面数网格生成；`smart_low_poly` 对复杂模型可能失败。

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


