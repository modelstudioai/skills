# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供端到端的 3D 内容创作流水线，覆盖从文本/图像生成基础 3D 网格、Gaussian Splatting 表示，到后处理（分割、重拓扑、贴图、格式转换）及动画绑定与重定向等全链路功能。所有接口均采用[异步任务](../concepts/asynchronous-task.md)模式，需通过 `task_id` 轮询获取结果，且当前**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供三大类核心能力：

- **基础生成**：  
  - 文生/图生/多图生 3D 网格（`Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`），输出 GLB/FBX 等可编辑资产；  
  - 单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与场景重建，详见 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：  
  包括网格分割（`Tripo/Tripo-Segmentation`, `Tripo/Tripo-SmartSegmentation`）、重拓扑（`Tripo/Tripo-Retopology`）、贴图生成（`Tripo/Tripo-Texture`）、网格补全（`Tripo/Tripo-MeshCompletion`）、格式转换（`Tripo/Tripo-ConvertFormat`）等，均支持基于前序任务 ID 或直接传入模型 URL 的输入方式。

- **动画**：  
  提供可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`）三步流程，其中绑骨类型需严格匹配（如 `quadruped` 骨骼须使用对应 `preset:quadruped:walk` 动画），详见 [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)。

> **注意**：文档中 `Tripo/Tripo-ImageToSplat` 接口明确说明“如需网格、贴图或可编辑的3D资产，请使用[Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)”，二者定位互斥，不可混用。

## 关键参数

所有 API 均需在请求头中设置 `X-DashScope-Async: enable`，否则返回错误。关键参数按功能分类如下：

- **通用参数**：  
  `model`（必填，如 `Tripo/Tripo-H3.1`）、`input`（含 `prompt`/`image`/`images` 三者互斥）、`parameters`（可选对象）。

- **生成类参数**：  
  - `texture_quality`: `standard`/`detailed`/`extreme`（影响贴图分辨率与耗时）；  
  - `geometry_quality`: 仅 `H3.1` 支持，`ultra` 对应最高 200 万面；  
  - `pbr` 与 `texture`: 均为布尔值，默认 `true`；若需无贴图模型，**必须同时设为 `false`**；  
  - `face_limit`: 面数上限，`H3.1` 默认自适应，`P1.0` 必须在 50–20,000 范围内。

- **后处理类参数**：  
  - `part_names`: 所有部件操作（分割、补全、重拓扑、格式转换）均支持按部件名（如 `tripo_part_0`）指定处理范围；  
  - `quad`: 开启后强制输出 FBX 格式（四边面），影响 `Retopology` 和 `ConvertFormat`；  
  - `model_version`: 各模块均有版本控制（如 `v2.0-20260430` 分割、`v2.0` 重拓扑），不兼容版本传入将返回 400 错误。

- **动画类参数**：  
  `rig_type`（`biped`/`quadruped` 等）必须与前序 `RigCheck` 结果一致；`animations` 数组最多 5 个 `preset:` 前缀动画名，非人形骨骼需带体型前缀（如 `preset:quadruped:walk`）。

## 使用方式

1. **开通与配置**：  
   在百炼控制台 [Tripo 模型市场页](https://bailian.console.aliyun.com/cn-beijing/model/market) 开通服务，并确保 API Key 已配置至北京地域环境变量。

2. **异步调用流程**（所有接口统一）：  
   - **步骤1（创建任务）**：`POST /api/v1/services/aigc/video-generation/3d-generation`，传入 `model`、`input` 及必要 `parameters`，获取 `task_id`；  
   - **步骤2（轮询结果）**：`GET /api/v1/tasks/{task_id}`，建议首次查询延迟 10 秒，后续每 15–30 秒轮询一次，`task_id` 有效期 24 小时。

3. **输入方式选择**：  
   - 生成类任务：支持 `prompt`（文本）、`image`（单图）、`images`（4 视角数组）；  
   - 后处理/动画类任务：支持 `original_model_task_id`（引用前序任务）或 `model_url`（公网模型 URL），但部分功能有格式限制（如 `AutoRig` 不支持 STL）。

## 限制和注意事项

- **地域与认证**：所有接口**仅限华北2（北京）地域**，且必须使用该地域的 API Key，跨地域调用将失败。  
- **输入约束**：  
  - 图像：PNG/JPEG/WebP，≤20MB，建议 ≥256×256 像素；  
  - 3D 模型：GLB/GLTF/FBX/OBJ/STL，≤150MB；  
  - 多图输入：`images` 数组长度固定为 4（前/左/后/右），缺失视角用 `{}` 占位，前视角必填。  
- **参数兼容性**：  
  - `generate_parts` 与 `texture`/`pbr`/`quad`/`smart_low_poly` **互斥**，开启前者时后四者必须为 `false` 或不传；  
  - `Tripo/Tripo-P1.0` 忽略 `geometry_quality`、`quad`、`smart_low_poly` 等参数，传入不报错但无效；  
  - `Tripo/Tripo-AutoRig` 中 `spec: mixamo` 绑骨的模型**不可用于动画重定向**。  
- **计费与性能**：  
  - `face_limit`、`texture_quality`、`quad`、`flatten_bottom` 等高级参数会触发更高积分计费；  
  - 智能分割（`Tripo-SmartSegmentation`）和 Gaussian Splatting 任务耗时较长，需合理设置轮询间隔。  
- **错误处理**：  
  创建任务失败时，响应含 `code` 和 `message`（见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)）；查询 `task_id` 超期将返回 `UNKNOWN` 状态。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


