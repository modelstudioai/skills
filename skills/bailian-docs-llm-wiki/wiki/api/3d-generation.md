# 3d generation

百炼平台提供基于 Tripo 模型的端到端 3D 内容生成与后处理能力，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、网格分割、重拓扑、格式转换、贴图生成、自动绑骨及动画重定向等核心链路。所有接口均采用异步调用模式，需通过任务 ID 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

- **基础生成**：  
  - `Tripo/Tripo-H3.1`（高精度，最高200万面）与 `Tripo/Tripo-P1.0`（专业级，最高2万面）支持文生3D、单图生3D、多图生3D [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)；  
  - `Tripo/Tripo-ImageToSplat` 专用于单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与场景重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：  
  - **分割类**：`Tripo/Tripo-Segmentation`（几何/语义分割）、`Tripo/Tripo-SmartSegmentation`（端到端图像/模型输入分割）；  
  - **优化类**：`Tripo/Tripo-Retopology`（智能低模重拓扑）、`Tripo/Tripo-MeshCompletion`（AI补全/快速封口）；  
  - **材质与格式**：`Tripo/Tripo-Texture`（PBR贴图生成）、`Tripo/Tripo-ConvertFormat`（GLTF/USDZ/FBX等格式转换与烘焙）；  
  - **动画管线**：`Tripo/Tripo-RigCheck` → `Tripo/Tripo-AutoRig` → `Tripo/Tripo-AnimationRetarget`，形成完整可绑定、可驱动的动画工作流。

> **注意**：文档中 `Tripo/Tripo-ImageToSplat` 的输入图像格式明确支持 WebP（见[文档 4](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)），但 `Tripo/Tripo-纹理生成`（文档 6）和 `Tripo/Tripo-网格分割`（文档 8）的 `ref_image` 参数说明中仅列出 PNG/JPEG，未提 WebP。实际调用时建议优先使用 PNG/JPEG，避免兼容性风险。

## 关键参数

| 参数名 | 适用模型 | 说明 |
|--------|----------|------|
| `X-DashScope-Async: enable` | 全部 | **强制必填请求头**，缺失将报错“current user api does not [support](../guides/support.md) synchronous calls” |
| `model` | 全部 | 模型标识符，如 `Tripo/Tripo-H3.1`、`Tripo/Tripo-Texture` 等，不可省略或拼写错误 |
| `face_limit` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 面数上限，取值范围因模型而异（如 `H3.1` 最高200万面，`P1.0` 仅50–20,000），超限返回 400 错误 |
| `quad` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 控制输出四边面（FBX）或三角面（GLB），开启后默认面数为 10,000（`ConvertFormat`）或忽略 `face_limit`（`H3.1`） |
| `pbr` / `texture` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Texture` | PBR材质与贴图开关，二者联动：设 `pbr=true` 会强制启用贴图；如需无贴图模型，须同时设 `pbr=false` 和 `texture=false` |
| `part_names` | `Tripo/Tripo-Texture`, `Tripo/Tripo-MeshCompletion`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 指定部件名称列表（如 `["tripo_part_0"]`），名称需从 GLB 节点中提取，传入不存在名称不报错但照常计费 |

## 使用方式

1. **前置准备**：  
   - 在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务；  
   - 获取并配置北京地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，推荐通过环境变量 `DASHSCOPE_API_KEY` 设置。

2. **异步调用流程（统一）**：  
   - **步骤1（创建任务）**：向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 提交请求，携带 `X-DashScope-Async: enable`、`Authorization`、`Content-Type` 及完整 `input`/`parameters`；  
   - **步骤2（轮询结果）**：用返回的 `task_id` 调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`，建议首次查询延迟 10 秒，后续每 15–30 秒轮询一次；  
   - **状态判断**：`SUCCEEDED` 时响应体 `output` 中包含结果 URL（如 `base_model_url`, `pbr_model_url`, `splat_url` 等）；`FAILED` 时检查 `code`/`message` 排查错误。

3. **输入约束**：  
   - 图像 URL 必须公网可访问，格式为 JPEG/PNG/WebP（Gaussian Splat 支持 WebP，其余建议 JPEG/PNG），单图 ≤20MB；  
   - 3D 模型 URL（如 GLB/FBX）≤150MB，仅支持指定格式；  
   - 多图输入（`images` 数组）必须严格按 `[front, left, back, right]` 顺序，长度固定为 4，空视角用 `{}` 占位。

## 限制和注意事项

- **地域强绑定**：所有接口**仅支持华北2（北京）地域**，Workspace ID、API Key、控制台开通均需对应此地域，跨地域调用必然失败。
- **任务生命周期**：`task_id` 有效期严格为 **24 小时**，超时后查询返回 `UNKNOWN` 状态，无法恢复结果。
- **模型兼容性**：  
  - `Tripo/Tripo-AnimationRetarget` **不支持** `spec=mixamo` 的绑骨模型（见[文档 15](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)）；  
  - `Tripo/Tripo-Retopology` 的 `v1.0` 版本不支持 `part_names` 和 `bake` 参数（见[文档 10](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)），而 `v2.0` 支持；  
  - `Tripo/Tripo-Segmentation` 的 `ref_image` 仅对 `v2.0-20260430` 版本有效，传给 `v1.0` 将返回 400 错误（见[文档 8](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)）。
- **计费与性能**：  
  - `generate_parts=true` 与 `texture=true`/`pbr=true` 不兼容（见[文档 3](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)），强行组合将返回 400；  
  - `Tripo/Tripo-ConvertFormat` 中 `texture_size≠4096`、`texture_format≠JPEG`、`scale_factor≠1.0` 等均触发“高级转换”计费，需谨慎配置。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)


