# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供端到端的 3D 内容创作流水线，覆盖从文/图生模型、Gaussian Splatting、后处理（分割、补全、重拓扑、格式转换等）到动画绑定与重定向的完整链路。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供三大类核心能力：

- **基础生成**：  
  - `Tripo/Tripo-H3.1`（高精度网格，最高 200 万面）和 `Tripo/Tripo-P1.0`（专业级，最高 2 万面）支持文生 3D、单图生 3D 和多图生 3D [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)；  
  - `Tripo/Tripo-ImageToSplat` 支持单图生成 Gaussian Splat（`.splat` 格式），适用于实时渲染与场景重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**：  
  包括网格分割（`Tripo/Tripo-Segmentation`）、智能分割（`Tripo/Tripo-SmartSegmentation`）、网格补全（`Tripo/Tripo-MeshCompletion`）、重拓扑（`Tripo/Tripo-Retopology`）、贴图生成（`Tripo/Tripo-Texture`）、格式转换（`Tripo/Tripo-ConvertFormat`）等，详见 [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。

- **动画**：  
  提供可绑骨检查（`Tripo/Tripo-RigCheck`）、自动绑骨（`Tripo/Tripo-AutoRig`）和动画重定向（`Tripo/Tripo-AnimationRetarget`）三步流程，构成完整的动画工作流 [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)。

> **注意**：文档中多次强调“仅适用于华北2（北京）地域”，但部分示例 URL（如文档 4 的 `curl` 示例）未显式声明地域前缀，而实际请求必须使用 `cn-beijing.maas.aliyuncs.com` 域名。开发者应以文档正文中的 URL 模板为准，而非示例代码中的占位符注释。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|------|----------|------|--------|
| `model_seed` | 所有生成类（H3.1/P1.0/ImageToSplat） | 控制几何体生成随机性；相同 seed + 相同输入 → 相同网格 | `12345` |
| `texture_seed` | H3.1、Texture、Splat | 控制贴图或 Splat 随机性；用于生成几何一致、外观不同的变体 | `67890` |
| `face_limit` | H3.1、P1.0、Retopology、ConvertFormat | 面数上限；H3.1 默认 150 万面（`ultra` 时 200 万），P1.0 为 50–20,000 | `50000` |
| `geometry_quality` | 仅 `Tripo/Tripo-H3.1` | `standard`（默认）或 `ultra`；P1.0 传入将被忽略 | `"ultra"` |
| `quad` | H3.1、Retopology、ConvertFormat | 是否输出四边面；启用后强制输出 FBX 格式 | `true` |
| `generate_parts` | 仅 `Tripo/Tripo-H3.1` | 启用后生成可编辑部件，但与 `texture`/`pbr`/`quad`/`smart_low_poly` 不兼容 | `true` |

## 使用方式

1. **前提条件**：  
   - 在[百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务；  
   - 获取并配置北京地域的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)；  
   - 确保业务空间 ID（`{WorkspaceId}`）与北京地域匹配。

2. **调用流程（统一异步）**：  
   - **步骤1（创建任务）**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`，必须携带 `X-DashScope-Async: enable` 请求头；  
   - **步骤2（轮询结果）**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`，建议首次查询延迟 10 秒，后续间隔 15–30 秒；  
   - `task_id` 有效期为 **24 小时**，超时后返回 `UNKNOWN` 状态。

3. **输入方式约束**：  
   - 文生 3D：仅填 `prompt`；  
   - 单图生 3D：仅填 `image`（URL）；  
   - 多图生 3D：仅填 `images`（长度为 4 的数组，按 front/left/back/right 顺序，空视角填 `{}`）；  
   - 三者互斥，同时传入将报错。

## 限制和注意事项

- **地域强绑定**：所有接口仅支持华北2（北京）地域，跨地域调用必然失败。API Key、Workspace ID、Endpoint 均需严格对应北京地域。
- **文件限制**：  
  - 输入图像：JPEG/PNG/WebP，≤20MB，分辨率 [20, 6000] 像素；  
  - 输入 3D 模型（GLB/FBX/OBJ 等）：≤150MB；  
  - 输出模型：`base_model_url`（无贴图）和 `pbr_model_url`（含 PBR）分别返回，需根据 `pbr` 和 `texture` 参数组合判断响应字段。
- **参数兼容性冲突**（高频易错点）：  
  - `generate_parts=true` 时，`texture` 和 `pbr` 必须为 `false`，且不可传 `texture_quality`、`quad`、`smart_low_poly`，否则返回 400 错误；  
  - `Tripo/Tripo-P1.0` 不支持 `geometry_quality`、`quad`、`smart_low_poly`、`generate_parts`，传入将被静默忽略（不报错）；  
  - `Tripo/Tripo-AutoRig` 中 `spec=mixamo` 绑骨的模型**不可用于** `Tripo/Tripo-AnimationRetarget`，文档 14 明确要求前序任务 `spec` 不能为 `mixamo`。
- **计费与版本**：  
  - `model_version`（如 `v2.0-20260430`）通常为 Beta 版本，需关注文档中标注的适用范围；  
  - 高级参数（如 `quad=true`、`face_limit` 非默认值、`texture_format!=JPEG`）可能触发高级计费，详见各后处理文档。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)


