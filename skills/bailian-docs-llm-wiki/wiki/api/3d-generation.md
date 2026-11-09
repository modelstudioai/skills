# 3d generation

百炼平台的 3D generation 能力基于 Tripo 模型提供端到端的 3D 内容生成与后处理服务，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、网格分割、贴图生成、重拓扑、格式转换及动画绑定等核心链路。所有接口均采用[异步任务](../concepts/asynchronous-task.md)模式，需通过 `task_id` 轮询获取结果，且**当前全部功能仅支持华北2（北京）地域** [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。

## 支持的模型/功能

- **基础生成**：
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `geometry_quality=ultra`、`quad`、`smart_low_poly`、`generate_parts` 等高级参数。
  - `Tripo/Tripo-P1.0`：专业级快速生成（最高 2 万面），适合对速度敏感的场景。
  - `Tripo/Tripo-ImageToSplat`：单图生成 Gaussian Splat（`.splat`），适用于实时渲染与重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：
  - **分割类**：`Tripo/Tripo-Segmentation`（基于已有模型）、`Tripo/Tripo-SmartSegmentation`（端到端图像/模型输入）。
  - **修复与优化**：`Tripo/Tripo-MeshCompletion`（AI 补全/快速封口）、`Tripo/Tripo-Retopology`（v2.0 智能低模 / v1.0 基础减面）。
  - **材质与导出**：`Tripo/Tripo-Texture`（PBR/8K 贴图）、`Tripo/Tripo-ConvertFormat`（GLTF/USDZ/FBX/STL 等格式转换及烘焙）。
  - **动画**：`Tripo/Tripo-RigCheck` → `Tripo/Tripo-AutoRig` → `Tripo/Tripo-AnimationRetarget` 三步流程，支持人形与非人形骨骼 [Tripo-动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：`Tripo/Tripo-ImageToSplat` 与 `Tripo/Tripo-3D-Generation` 是两类独立输出（Splat vs Mesh），不可混用参数；文档中 `Tripo/Tripo-P1.0` 的 `face_limit` 取值范围（50–20,000）与 `Tripo/Tripo-H3.1` 的默认上限（150 万面）存在量级差异，开发者需按模型选型严格匹配参数约束。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `texture_quality` | `H3.1`, `P1.0`, `Texture` | 贴图质量等级 | `"standard"` / `"detailed"` / `"extreme"` |
| `geometry_quality` | `H3.1` only | 几何精度（`P1.0` 忽略） | `"standard"` / `"ultra"` |
| `quad` | `H3.1`, `Retopology`, `ConvertFormat` | 输出四边面（强制 FBX 格式） | `true` |
| `generate_parts` | `H3.1` only | 输出可编辑部件（禁用 `texture`/`pbr`） | `true` |
| `model_version` | `Segmentation`, `Texture`, `Retopology`, `AutoRig` | 算法版本控制（如 `v2.0-20260430`, `v2.5-20260210`） | `"v2.0-20260430"` |
| `face_limit` | `H3.1`, `P1.0`, `Retopology`, `ConvertFormat` | 面数上限（取值范围因模型而异，详见各文档） | `5000` |

- 所有随机种子（`model_seed`/`image_seed`/`texture_seed`）取值范围：`-2147483648` 至 `2147483647`。
- `input` 中 `prompt`/`image`/`images` 三者互斥；`original_model_task_id` 与 `model_url` 在后处理接口中互斥。

## 使用方式

1. **前提条件**：
   - 在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务（华北2地域）。
   - 获取并配置北京地域的 API Key（环境变量 `DASHSCOPE_API_KEY`）。

2. **调用流程（统一异步）**：
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     请求头必须包含：`Content-Type: application/json`、`Authorization: Bearer <key>`、`X-DashScope-Async: enable`。  
     请求体含 `model`（如 `"Tripo/Tripo-H3.1"`）和 `input`（根据模型类型填 `prompt`/`image`/`images` 或 `original_model_task_id`）。
   - **步骤2：轮询结果**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议首次查询延迟 10 秒，后续每 15–30 秒轮询一次；`task_id` 有效期为 24 小时。

3. **输入规范**：
   - 图像：JPEG/PNG/WebP，≤20MB，建议 ≥256×256 像素。
   - 3D 模型文件（后处理）：GLB/GLTF/FBX/OBJ/STL，≤150MB。
   - 多视角图像（`images`）：数组长度固定为 4，顺序为 `[front, left, back, right]`，缺失视角传 `null`。

## 限制和注意事项

- **地域强约束**：所有接口仅支持华北2（北京）地域，跨地域调用将失败 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。
- **任务依赖**：后处理任务（如 `Segmentation`、`Texture`、`AutoRig`）需引用前序成功任务的 `task_id`，且账号必须一致；引用其他账号任务返回 400 错误。
- **参数兼容性**：
  - `generate_parts=true` 时，`texture` 和 `pbr` 必须为 `false`，否则返回 400。
  - `Tripo/Tripo-P1.0` 不支持 `geometry_quality`、`quad`、`smart_low_poly` 等参数（传入被忽略）。
  - `Tripo/Tripo-AnimationRetarget` 要求前序 `AutoRig` 的 `spec` 不能为 `"mixamo"`。
- **计费提示**：`face_limit`、`texture_quality=extreme`、`quad=true`、`part_names` 非空、`out_format=fbx` 等操作可能触发高级计费，详见各接口文档。
- **错误处理**：`X-DashScope-Async: enable` 缺失必报错；`task_id` 超期（24h）后查询返回 `UNKNOWN` 状态。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


