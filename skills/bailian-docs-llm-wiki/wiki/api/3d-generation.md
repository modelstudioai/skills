# 3d generation

百炼平台提供基于 Tripo 模型的端到端 3D 内容生成与后处理能力，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、网格分割、重拓扑、格式转换、自动绑骨及动画重定向等完整工作流。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

- **基础生成**：
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `geometry_quality=ultra`、`quad`、`smart_low_poly`、`generate_parts` 等高级参数。
  - `Tripo/Tripo-P1.0`：专业级快速生成（最高 2 万面），适合对速度敏感的场景，不支持 `geometry_quality`、`quad`、`smart_low_poly`、`generate_parts` 等参数。
  - `Tripo/Tripo-ImageToSplat`：单图生成 `.splat` 文件，适用于实时渲染与真实感重建，详见 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：
  - **分割类**：`Tripo/Tripo-Segmentation`（基于已有模型的几何/语义分割）、`Tripo/Tripo-SmartSegmentation`（端到端图像或模型输入的智能分割）。
  - **修复与优化**：`Tripo/Tripo-MeshCompletion`（AI 补全或快速封口）、`Tripo/Tripo-Retopology`（智能低模或基础减面）、`Tripo/Tripo-Texture`（PBR/8K 贴图生成）。
  - **导出与兼容**：`Tripo/Tripo-ConvertFormat`（GLTF/USDZ/FBX 等多格式转换，支持 UV 合并、轴心调整、贴图烘焙等）。
  - **动画管线**：`Tripo/Tripo-RigCheck` → `Tripo/Tripo-AutoRig` → `Tripo/Tripo-AnimationRetarget`，形成完整的可绑定、可驱动、可重定向动画流程。

> **注意**：文档中 `Tripo/Tripo-AnimationRetarget` 明确要求前序绑骨任务不能使用 `spec=mixamo`（见[原文标题](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)），但 `Tripo/Tripo-AutoRig` 文档中却将 `mixamo` 列为合法 `spec` 值且未标注此限制。开发者在组合使用时务必遵循重定向接口的约束，避免因规格不匹配导致任务失败。

## 关键参数

| 参数名 | 适用模型 | 说明 |
|--------|----------|------|
| `texture_quality` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Texture` | 取值 `standard`/`detailed`/`extreme`；`extreme` 对应 8K 贴图，显著增加耗时与积分消耗。 |
| `geometry_quality` | `Tripo/Tripo-H3.1` only | `standard`（≤150 万面）或 `ultra`（≤200 万面）；`Tripo/Tripo-P1.0` 传入该参数会被忽略。 |
| `quad` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 开启后强制输出 FBX 格式（非 GLB），且默认面数为 10,000；`Tripo/Tripo-P1.0` 不支持。 |
| `generate_parts` | `Tripo/Tripo-H3.1` only | 开启后生成可编辑部件，但会强制禁用 `texture`/`pbr`/`quad`/`smart_low_poly`；与 `smart_low_poly` 同时开启时后者优先。 |
| `face_limit` | 多模型通用 | 面数上限，取值范围因模型和参数组合而异（如 `Tripo/Tripo-H3.1` + `ultra` ≤2,000,000；`Tripo/Tripo-P1.0` 为 50–20,000）。建议游戏资产 50k–100k，Web/移动端 10k–50k。 |
| `model_seed` / `texture_seed` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-ImageToSplat`, `Tripo/Tripo-Texture` | 分别控制几何体与贴图的随机性；相同种子+相同输入 = 相同输出，用于结果复现与可控迭代。 |

## 使用方式

1. **前提条件**：
   - 在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务（仅限华北2）。
   - 获取并配置北京地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，推荐通过环境变量 `DASHSCOPE_API_KEY` 设置。
   - 所有请求必须携带 `X-DashScope-Async: enable` 请求头，同步调用不被支持。

2. **标准异步流程**：
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     返回 `task_id`（有效期 24 小时），**切勿重复提交同一任务**。
   - **步骤2：轮询结果**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议首次查询延迟 10 秒，之后每 15–30 秒轮询一次；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`。

3. **输入方式选择**（以生成模型为例）：
   - 文生3D：`input.prompt`（≤1024 字符）。
   - 单图生3D：`input.image`（JPEG/PNG，≤20MB，建议 ≥256px）。
   - 多图生3D：`input.images`（固定长度 4 的数组，按前/左/后/右顺序，至少含前视角）。
   - 注意：`prompt`、`image`、`images` 三者互斥，同时传入将返回 400 错误。

## 限制和注意事项

- **地域与认证强绑定**：所有接口仅支持华北2（北京）地域，且 API Key 必须为该地域生成，跨地域调用必然失败。
- **任务依赖链严格**：后处理任务（如 `Tripo/Tripo-Texture`、`Tripo/Tripo-Retopology`）通常要求 `original_model_task_id` 来自同一账号、已成功执行的前序任务；引用其他账号或失败任务将返回 400 错误。
- **文件格式与大小限制**：
  - 输入图像：JPEG/PNG/WebP，≤20MB，分辨率 [20, 6000] px。
  - 输入 3D 模型（GLB/GLTF/FBX/OBJ/STL）：≤150MB。
  - 输出模型：`generate_parts` 开启时返回 GLB；`quad=true` 时强制 FBX。
- **参数兼容性陷阱**：
  - `Tripo/Tripo-P1.0` 不支持 `geometry_quality`、`quad`、`smart_low_poly`、`generate_parts`，传入会被忽略（不报错），但可能产生不符合预期的结果。
  - `Tripo/Tripo-Retopology` 的 `v1.0` 版本不支持 `part_names` 和 `bake` 参数；`v2.0`（默认）则支持。
- **计费与性能权衡**：`texture_quality=extreme`、`geometry_quality=ultra`、`quad=true`、`face_limit` 过低（需配合 `smart_low_poly`）等均显著增加计算资源消耗与耗时，需根据下游用途（如 Web 渲染 vs 游戏引擎导入）合理选型。详细计费规则请参考 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md) 文档。

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
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


