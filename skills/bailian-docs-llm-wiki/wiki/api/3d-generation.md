# 3d generation

百炼平台提供基于 Tripo 模型的端到端 3D 内容生成与后处理能力，覆盖文生/图生/多图生 3D 网格、Gaussian Splatting、网格分割、贴图生成、重拓扑、格式转换及动画绑定等核心链路。所有接口均采用异步调用模式，需通过 `task_id` 轮询获取结果，且**仅支持华北2（北京）地域**。

## 支持的模型/功能

- **基础生成**：  
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高 200 万面），支持 `geometry_quality=ultra`、`quad`、`smart_low_poly`、`generate_parts` 等高级参数；  
  - `Tripo/Tripo-P1.0`：快速专业生成（最高 2 万面），适合对速度敏感的场景；  
  - `Tripo/Tripo-ImageToSplat`：单图生成 `.splat` 文件，适用于实时渲染与场景重建 [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理能力**：  
  - **分割类**：`Tripo/Tripo-Segmentation`（几何/语义分割）、`Tripo/Tripo-SmartSegmentation`（端到端图像/模型输入分割）；  
  - **修复与优化类**：`Tripo/Tripo-MeshCompletion`（AI 补全/快速封口）、`Tripo/Tripo-Retopology`（智能低模重拓扑）、`Tripo/Tripo-Texture`（PBR 贴图生成，最高 8K）；  
  - **工程化工具类**：`Tripo/Tripo-ConvertFormat`（多格式导出+烘焙/对称/压平等）、`Tripo/Tripo-RigCheck` / `Tripo/Tripo-AutoRig` / `Tripo/Tripo-AnimationRetarget`（完整动画管线）[Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)。

> **注意**：文档中 `Tripo/Tripo-H3.1` 的 `face_limit` 上限描述存在不一致——文档2称 `geometry_quality=ultra` 时“不超过2,000,000”，而文档10在重拓扑 v2.0 中限定为“三角面500~20,000”。该差异源于功能边界：前者指**生成阶段原始面数上限**，后者指**重拓扑目标面数范围**，二者无冲突，但开发者需严格按功能上下文选用参数。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `texture_quality` | `Tripo-H3.1`, `Tripo-Texture` | 贴图质量等级 | `"standard"` / `"detailed"` / `"extreme"` |
| `geometry_quality` | `Tripo-H3.1` only | 几何精度（影响面数上限） | `"standard"` / `"ultra"` |
| `quad` | `Tripo-H3.1`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 输出四边面网格（强制 FBX 格式） | `true` |
| `generate_parts` | `Tripo-H3.1` only | 输出可编辑部件（与 `texture`/`pbr`/`quad`/`smart_low_poly` 互斥） | `true` |
| `model_version` | 多个后处理模型 | 算法版本控制（如 `v2.0-20260430` 分割、`v2.0` 重拓扑） | `"v2.0"` |
| `face_limit` | `Tripo-H3.1`, `Tripo-P1.0`, `Tripo-Retopology`, `Tripo-ConvertFormat` | 面数硬性限制，**取值范围因模型和版本差异极大**，务必查阅对应文档 | `10000` |

> **注意**：`face_limit` 在不同模型中含义与范围不同：`Tripo-P1.0` 为 50–20,000；`Tripo-H3.1` 在 `geometry_quality=ultra` 下可达 2,000,000；而 `Tripo-Retopology v2.0` 仅支持 500–20,000。混用将导致 400 错误 [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。

## 使用方式

1. **前提条件**：  
   - 在华北2（北京）地域开通 Tripo 服务；  
   - 获取并配置北京地域的 API Key（环境变量或 Header）；  
   - 所有请求必须携带 `X-DashScope-Async: enable`，否则报错。

2. **通用流程（异步）**：  
   - **步骤1（创建任务）**：`POST /api/v1/services/aigc/video-generation/3d-generation`，传入 `model`、`input`、`parameters`；  
   - **步骤2（轮询结果）**：`GET /api/v1/tasks/{task_id}`，建议首次查询延迟 10 秒，后续间隔 15–30 秒；  
   - `task_id` 有效期为 24 小时，超时返回 `UNKNOWN`。

3. **输入方式选择**：  
   - 文生3D：`input.prompt`（≤1024 字符）；  
   - 单图生3D：`input.image`（JPEG/PNG，≤20MB）；  
   - 多图生3D：`input.images`（长度为4的数组，视角顺序：前/左/后/右）；  
   - 后处理任务：通过 `original_model_task_id` 引用前序任务，或直接传 `model_url`（GLB/FBX/OBJ/STL，≤150MB）。

## 限制和注意事项

- **地域强约束**：全部接口仅支持华北2（北京），URL 域名为 `cn-beijing.maas.aliyuncs.com`，API Key 必须为北京地域生成；
- **异步强制要求**：所有请求头必须含 `X-DashScope-Async: enable`，同步调用不被支持；
- **资源限制**：  
  - 图像输入：分辨率 [20, 6000] 像素，格式 JPEG/PNG/WebP；  
  - 模型文件：后处理任务最大 150MB（GLB/FBX/OBJ/STL）；  
  - `task_id` 查询有效期：严格 24 小时；
- **兼容性警告**：  
  - `Tripo-AutoRig` 若使用 `spec=mixamo`，则无法用于 `Tripo-AnimationRetarget`；  
  - `Tripo-Retopology v1.0` 不支持 `part_names` 和 `bake` 参数，而 `v2.0` 支持；  
  - `Tripo-ConvertFormat` 中 `quad=true` 时强制输出 FBX，且 `face_limit` 默认为 10,000。
- **计费提示**：高级参数（如 `texture_quality=extreme`、`quad=true`、非默认 `face_limit`）通常触发更高积分消耗，具体以控制台计费说明为准。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
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


