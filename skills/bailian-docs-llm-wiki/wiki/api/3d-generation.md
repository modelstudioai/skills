# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供端到端的 3D 内容生产流水线，覆盖从文/图生 3D 网格、Gaussian Splatting 表示，到模型后处理（分割、重拓扑、贴图、格式转换）及动画绑定与重定向等全链路功能。所有接口均采用[异步任务](../concepts/asynchronous-task.md)模式，需通过 `task_id` 轮询获取结果，且当前**仅支持华北2（北京）地域**。

## 支持的模型/功能

- **基础生成**：
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `geometry_quality=ultra`、`quad`、`smart_low_poly`、`generate_parts` 等高级参数 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。
  - `Tripo/Tripo-P1.0`：专业级快速生成（最高 2 万面），适合对速度敏感的场景。
  - `Tripo/Tripo-ImageToSplat`：单图生成 `.splat` 文件，适用于实时渲染与真实感重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**（均需前序任务输出或公网可访问的模型 URL）：
  - 分割：`Tripo/Tripo-Segmentation`（几何拓扑分割）、`Tripo/Tripo-SmartSegmentation`（端到端图像/模型输入分割）。
  - 重拓扑：`Tripo/Tripo-Retopology`（v1.0 基础减面 / v2.0 智能低模）。
  - 贴图：`Tripo/Tripo-Texture`（支持 PBR、8K 贴图、文本/图像引导）[Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)。
  - 格式转换：`Tripo/Tripo-ConvertFormat`（GLTF/USDZ/FBX/OBJ/STL/3MF，支持烘焙、UV 合并、朝向控制等）。
  - 网格补全：`Tripo/Tripo-MeshCompletion`（AI 补全或快速封口）。

- **动画**：
  - `Tripo/Tripo-RigCheck`：判断模型可绑骨性并推荐骨骼类型。
  - `Tripo/Tripo-AutoRig`：自动添加骨骼（支持 biped/quadruped 等 7 类 `rig_type`）。
  - `Tripo/Tripo-AnimationRetarget`：将预设动画应用至已绑骨模型（最多 5 个动画，`spec=mixamo` 的模型不支持）。

> **注意**：文档中 `Tripo/Tripo-AnimationRetarget` 明确要求前序 `Tripo-AutoRig` 任务的 `spec` 参数**不能为 `mixamo`**，但 `Tripo-AutoRig` 文档本身未强调此限制为硬性约束，仅说明“使用此规范绑骨的模型不能用于动画重定向”。此处以动画重定向文档为准，视为强制限制。

## 关键参数

| 参数名 | 适用模型 | 说明 |
|--------|----------|------|
| `X-DashScope-Async: enable` | 所有 3D 接口 | **必填请求头**，缺失将报错 `"current user api does not support synchronous calls"`。 |
| `model` | 所有接口 | 模型标识符，如 `Tripo/Tripo-H3.1`、`Tripo/Tripo-Texture` 等，不可省略或拼写错误。 |
| `input.image` / `input.images` / `input.prompt` | `Tripo-H3.1/P1.0` | 三者互斥，仅能选其一；`images` 数组长度固定为 4（前/左/后/右），空视角用 `{}` 占位。 |
| `parameters.texture_quality` | `Tripo-H3.1/P1.0`, `Tripo-Texture`, `Tripo-ConvertFormat` | 取值 `standard`/`detailed`/`extreme`；`extreme`（8K）在 `Tripo-Texture` 中消耗更多积分。 |
| `parameters.face_limit` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 面数上限，取值范围因模型和版本而异（如 `Tripo-P1.0` 为 50–20,000，`Tripo-H3.1` `ultra` 模式下可达 2,000,000）。 |
| `parameters.quad` | `Tripo-H3.1`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 开启后强制输出 FBX 格式（GLB 不支持四边面），且默认面数为 10,000（`ConvertFormat`）或 150,000（`Retopology` v1.0）。 |
| `parameters.part_names` | `Tripo-Texture`, `Tripo-MeshCompletion`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 部件名称列表（如 `["tripo_part_0", "tripo_part_1"]`），需从前序分割任务的 GLB 模型节点中提取，非任务返回字段。 |

## 使用方式

1. **前提条件**：
   - 在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务（仅限华北2）。
   - 获取并配置北京地域的 API Key（环境变量 `DASHSCOPE_API_KEY`）。

2. **通用调用流程（所有接口）**：
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     设置请求头 `Content-Type: application/json`, `Authorization: Bearer <key>`, `X-DashScope-Async: enable`，并在请求体中指定 `model` 和 `input`。
   - **步骤2：轮询查询结果**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议首次查询延迟 10 秒，之后每 15–30 秒轮询一次；`task_id` 有效期为 24 小时。

3. **典型依赖链示例**：
   ```mermaid
   graph LR
   A[文/图生3D] -->|task_id| B[网格分割]
   B -->|task_id| C[贴图]
   B -->|task_id| D[网格补全]
   A -->|task_id| E[重拓扑]
   A -->|task_id| F[可绑骨检查]
   F -->|推荐 rig_type| G[自动绑骨]
   G -->|task_id| H[动画重定向]
   ```

## 限制和注意事项

- **地域与认证强绑定**：所有接口**仅支持华北2（北京）地域**，且必须使用该地域的 API Key。跨地域调用或使用其他地域 Key 将失败 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。
- **输入文件限制**：
  - 图像（`image`/`images`）：JPEG/PNG/WebP，≤20MB，分辨率 [20, 6000] 像素。
  - 3D 模型（`model_url`）：GLB/GLTF/FBX/OBJ/STL，≤150MB。
- **任务状态与生命周期**：`task_id` 有效期严格为 **24 小时**，超时后查询返回 `UNKNOWN`；轮询 RPS 默认为 20，高频需求应配置[异步回调](raw/model-api-reference/more-about-models/async-task-api.md)。
- **参数兼容性冲突**（关键矛盾点）：
  > **注意**：`Tripo-H3.1` 的 `generate_parts=true` 与 `texture=true`/`pbr=true`/`texture_quality`/`quad`/`smart_low_poly` **互斥**，同时设置将返回 400 错误；而 `Tripo-P1.0` 完全不支持 `generate_parts`、`geometry_quality`、`quad`、`smart_low_poly` 等参数，传入会被忽略。开发者需严格按模型能力表选用参数，不可跨模型复用配置。
- **计费与兼容性**：
  - `Tripo-ConvertFormat` 中 `texture_size≠4096`、`texture_format≠JPEG`、`scale_factor≠1.0` 等选项按“高级转换”计费。
  - `Tripo-AnimationRetarget` **明确禁止**使用 `spec=mixamo` 的绑骨模型，否则任务失败。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)


