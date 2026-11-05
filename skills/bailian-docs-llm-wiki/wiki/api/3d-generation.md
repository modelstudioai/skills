# 3d generation

百炼平台的 3D generation 能力基于 Tripo 模型提供端到端的 3D 内容生成与后处理服务，覆盖从文/图生模型、Gaussian Splatting 到网格分割、贴图、重拓扑、动画绑定等完整工作流。所有接口均采用[异步调用](../concepts/asynchronous-invocation.md)模式，需通过任务 ID 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供三大类核心能力：

- **基础生成**：  
  - `Tripo/Tripo-H3.1`（高精度网格，最高 200 万面）与 `Tripo/Tripo-P1.0`（专业级，最高 2 万面）支持文生 3D、单图生 3D 和多图（前/左/后/右）生 3D [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)；  
  - `Tripo/Tripo-ImageToSplat` 专用于单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与真实感重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：  
  包含贴图（`Tripo/Tripo-Texture`）、网格分割（`Tripo/Tripo-Segmentation`）、智能分割（`Tripo/Tripo-SmartSegmentation`）、网格补全（`Tripo/Tripo-MeshCompletion`）、重拓扑（`Tripo/Tripo-Retopology`）、格式转换（`Tripo/Tripo-ConvertFormat`）等，详见 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。

- **动画**：  
  提供可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`）三步流程，支持 biped、quadruped 等多种骨骼类型 [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：文档中 `Tripo/Tripo-ImageToSplat` 的输入图像格式支持 PNG/JPEG/WebP（见[文档 4](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)），但 `Tripo-文生/图生3D模型` 的 `image` 参数仅支持 JPEG/PNG（见[文档 3](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)）。实际调用时请严格按各接口文档要求传入格式。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `model` | 所有接口 | 必填，固定模型标识符 | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Texture` |
| `X-DashScope-Async` | 所有接口 | 请求头必填，必须设为 `"enable"` | `"enable"` |
| `texture_quality` | `Tripo-H3.1`, `Tripo-Texture` | 贴图质量：`standard`（默认）、`detailed`、`extreme`（8K） | `"detailed"` |
| `geometry_quality` | 仅 `Tripo-H3.1` | 几何精度：`standard`（≤150 万面）、`ultra`（≤200 万面） | `"ultra"` |
| `face_limit` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 面数上限，取值范围因模型和版本而异（如 `Tripo-P1.0` 为 50–20,000） | `50000` |
| `quad` | `Tripo-H3.1`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 是否输出四边面（启用后强制 FBX 格式） | `true` |
| `pbr` / `texture` | `Tripo-H3.1`, `Tripo-Texture` | 控制是否生成 PBR 材质或基础贴图；二者均为 `false` 时返回无贴图模型 | `false` |
| `part_names` | `Tripo-Texture`, `Tripo-MeshCompletion`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 指定部件名称列表（如 `["tripo_part_0"]`），需从前序分割任务 GLB 中读取节点名 | `["tripo_part_0"]` |

## 使用方式

1. **前提准备**：  
   - 在华北2（北京）地域的[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务；  
   - 获取并配置该地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，推荐通过环境变量 `DASHSCOPE_API_KEY` 设置。

2. **[异步调用](../concepts/asynchronous-invocation.md)流程（统一）**：  
   - **步骤1：创建任务**  
     向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，携带 `model`、`input` 和 `parameters`。务必设置 `X-DashScope-Async: enable` 请求头。  
     > **注意**：文档 3、4、5、6 等均明确要求“请勿重复创建任务”，应复用 `task_id` 轮询，而非重发创建请求。

   - **步骤2：轮询查询结果**  
     使用返回的 `task_id` 调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`。建议首次查询延迟 10 秒，之后每 15–30 秒轮询一次，直至 `task_status` 为 `SUCCEEDED` 或 `FAILED`。`task_id` 有效期为 24 小时。

3. **输入方式选择**：  
   - 文生 3D：传 `prompt` 字符串（≤1024 字符）；  
   - 单图生 3D：传 `image` URL（JPEG/PNG，≤20MB）；  
   - 多图生 3D：传 `images` 数组（长度固定为 4，顺序为前/左/后/右）；  
   - 后处理任务：优先使用 `original_model_task_id` 引用前序任务，或直接传 `model_url`（GLB/FBX/OBJ 等，≤150MB）。

## 限制和注意事项

- **地域与认证强约束**：所有 3D generation 接口**仅支持华北2（北京）地域**，且必须使用该地域的 API Key。跨地域调用或使用其他地域 Key 将失败 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。
- **任务依赖链**：后处理任务（如贴图、分割、重拓扑）通常依赖前序任务输出。例如 `Tripo-Texture` 可接受 `original_model_task_id` 或 `model_url`，但若引用前序任务，要求账号一致且前序任务状态为 `SUCCEEDED`；`Tripo-MeshCompletion` 仅接受 `Tripo-Segmentation` 或 `Tripo-SmartSegmentation` 的 `task_id`。
- **参数兼容性冲突**：部分参数在不同模型间互斥或被忽略。例如：  
  - `geometry_quality`、`smart_low_poly`、`generate_parts` 仅对 `Tripo-H3.1` 生效，传给 `Tripo-P1.0` 会被静默忽略；  
  - `generate_parts` 开启时，`texture` 和 `pbr` 必须为 `false`，否则返回 400 错误；  
  - `Tripo-AnimationRetarget` 明确禁止使用 `spec: mixamo` 绑骨的模型，否则任务失败。
- **文件与格式限制**：  
  - 输入图像：分辨率 [20, 6000] 像素，建议 ≥256×256；  
  - 3D 模型文件：支持 GLB/GLTF/FBX/OBJ/STL，大小 ≤150MB；  
  - 输出格式：`quad=true` 时强制 FBX；`out_format` 为 `glb` 或 `fbx` 时需匹配下游引擎需求（如 Web 用 GLB，Unity/Unreal 用 FBX）。
- **计费与性能提示**：  
  - `texture_quality: extreme`、`face_limit` 非默认值、`quad=true`、`bake=true` 等高级参数将触发更高积分消耗；  
  - `Tripo-ImageToSplat` 和 `Tripo-SmartSegmentation` 任务耗时较长，需合理设置轮询间隔；  
  - `Tripo-Retopology` 的 `v2.0`（智能低模）比 `v1.0`（基础减面）更注重拓扑质量，适合需手工编辑的场景。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


