# 3d generation

百炼平台的 3D generation 能力基于 Tripo 模型提供端到端的 3D 内容生成与后处理服务，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、网格分割、重拓扑、格式转换、自动绑骨及动画重定向等核心链路。所有接口均采用[异步任务模式](../concepts/asynchronous-task.md)，需通过 `task_id` 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供三大类能力：

- **基础生成**：  
  - `Tripo/Tripo-H3.1`（高精度网格，最高 200 万面）和 `Tripo/Tripo-P1.0`（专业级低面模型，最高 2 万面）支持文生/单图生/多图生 3D 网格 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)；  
  - `Tripo/Tripo-ImageToSplat` 专用于单图生成 `.splat` 文件，适用于实时渲染与场景重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：  
  包括贴图生成（`Tripo/Tripo-Texture`）、网格分割（`Tripo/Tripo-Segmentation`）、智能分割（`Tripo/Tripo-SmartSegmentation`）、网格补全（`Tripo/Tripo-MeshCompletion`）、重拓扑（`Tripo/Tripo-Retopology`）和格式转换（`Tripo/Tripo-ConvertFormat`）等，详见 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。

- **动画**：  
  支持可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`），构成完整骨骼驱动工作流 [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：文档中 `Tripo/Tripo-ImageToSplat` 的输入图像格式明确支持 WebP（见[原文标题](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)），但 `Tripo-文生/图生3D模型` 的 `image` 参数未列出 WebP（仅写明 JPEG/PNG）。实际调用时若需使用 WebP，请优先参考 `ImageToSplat` 的兼容性说明。

## 关键参数

| 参数名 | 适用模型 | 说明 |
|--------|----------|------|
| `model_seed` / `texture_seed` | `Tripo-H3.1`, `Tripo-P1.0`, `ImageToSplat`, `Texture` 等 | 控制几何或贴图生成的确定性；`model_seed` 相同则网格一致，`texture_seed` 相同则贴图一致 |
| `face_limit` | `Tripo-H3.1`, `Tripo-P1.0`, `Retopology`, `ConvertFormat` | 面数上限；`H3.1` 默认自适应（`ultra` 下≤200万），`P1.0` 严格限定为 50–20,000；`Retopology` 中 `v1.0` 必填，`v2.0` 可选 |
| `quad` | `Tripo-H3.1`, `Retopology`, `ConvertFormat` | 启用四边面输出；启用后强制输出 FBX 格式，且 `face_limit` 默认值变为 10,000（`ConvertFormat`）或 150,000（`Retopology v1.0`） |
| `generate_parts` | `Tripo-H3.1` 仅 | 开启后禁用 `texture`/`pbr`/`quad`/`smart_low_poly`；如需部件分割，请改用 [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md) 或 [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md) |
| `part_names` | `Texture`, `MeshCompletion`, `Retopology`, `ConvertFormat` | 指定处理部件；名称需从 GLB 节点中提取（如 `tripo_part_0`），传入不存在名称不报错但照常计费 |

## 使用方式

1. **前提条件**：  
   - 在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务；  
   - 获取并配置华北2（北京）地域的 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；  
   - 所有请求必须携带 `X-DashScope-Async: enable` 请求头，否则报错。

2. **通用调用流程（异步）**：  
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     返回 `task_id`（24 小时有效）；  
   - **步骤2：轮询结果**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议首次查询延迟 10 秒，后续每 15–30 秒轮询一次；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`。

3. **输入方式选择**：  
   - 生成类接口（如 `Tripo-3D-Generation`）：`prompt`（文生）、`image`（单图）、`images`（多图，固定 4 视角）三者互斥；  
   - 后处理类接口（如 `Texture`, `Retopology`）：通过 `original_model_task_id`（推荐）或 `model_url` 引入前序模型；  
   - 动画类接口（如 `AutoRig`, `AnimationRetarget`）：必须以前序任务 `task_id` 为输入，且 `AutoRig` 输出不可直接用于 `AnimationRetarget`（若 `spec=mixamo` 则明确不支持）。

## 限制和注意事项

- **地域与认证强约束**：所有接口仅支持华北2（北京）地域，且必须使用该地域的 API Key；跨地域调用或 Key 不匹配将返回 `InvalidApiKey` 等错误。
- **文件限制**：  
  - 输入图像：≤20 MB，JPEG/PNG/WebP（`ImageToSplat`），建议 ≥256×256 像素；  
  - 输入 3D 模型（GLB/FBX/OBJ 等）：≤150 MB；  
  - 多图生 3D：`images` 数组长度固定为 4，视角顺序为前/左/后/右，至少提供 2 张有效图（前视角必填）。
- **参数兼容性冲突**：  
  > **注意**：`Tripo/Tripo-H3.1` 的 `generate_parts` 参数与 `texture`/`pbr`/`quad`/`smart_low_poly` 互斥；而 [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md) 和 [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md) 是生产级部件分割的推荐方案，无此限制。
- **计费与版本差异**：  
  - `Retopology` 的 `v1.0`（基础减面）与 `v2.0`（智能低模）计费不同；`v1.0` 必须传 `face_limit`，`v2.0` 可不传；  
  - `ConvertFormat` 中启用 `quad`/`flatten_bottom`/`texture_size≠4096`/`scale_factor≠1.0` 等均触发高级转换计费；  
  - `AnimationRetarget` 按动画个数计费（最多 5 个），`animation`（单个）与 `animations`（数组）计费规则一致。

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
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)


