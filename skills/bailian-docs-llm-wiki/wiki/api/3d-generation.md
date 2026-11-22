# 3d generation

百炼平台的 3D 生成能力基于 Tripo 模型提供端到端的 3D 内容生产流水线，覆盖从文/图生模型、Gaussian Splatting、后处理（贴图、分割、补全、重拓扑、格式转换）到动画绑定与重定向的完整链路。所有接口均采用异步调用模式，需通过任务 ID 轮询获取结果，且当前**仅支持华北2（北京）地域**。

## 支持的模型/功能

Tripo 提供三类核心能力：

- **基础生成**：支持文生3D、单图生3D、多图生3D（[Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)），以及单图生成 Gaussian Splat（[Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)）。
- **后处理**：包括贴图生成（[Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)）、网格分割（[Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)）、智能分割（[Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)）、网格补全（[Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)）、重拓扑（[Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)）和格式转换（[Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)）。
- **动画**：包含可绑骨检查（[Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)）、自动绑骨（[Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)）和动画重定向（[Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)）。

> **注意**：文档中多次强调“仅适用于华北2（北京）地域”，但部分示例 URL 和参数说明未明确排除其他地域可能性；实际调用时必须使用北京地域的 Workspace ID 和 API Key，否则将返回地域不匹配错误。

## 关键参数

各接口共性参数如下（详见各子文档）：

- **必选请求头**：`Content-Type: application/json`、`Authorization: Bearer <API_KEY>`、`X-DashScope-Async: enable`（缺失任一将报错）。
- **模型标识**：`model` 字段为固定字符串，如 `Tripo/Tripo-H3.1`（高精度网格）、`Tripo/Tripo-P1.0`（快速专业版）、`Tripo/Tripo-ImageToSplat`（Gaussian Splat）、`Tripo/Tripo-Texture`（贴图）等。
- **输入方式**：
  - 文生3D：`input.prompt`（最大1024字符）；
  - 单图生3D：`input.image`（JPEG/PNG，≤20MB，建议≥256px）；
  - 多图生3D：`input.images`（长度为4的数组，顺序为前/左/后/右）；
  - 后处理/动画：通常通过 `input.original_model_task_id` 引用前序任务，或 `input.model_url` 直接传入公网 URL。
- **关键可选参数**：
  - `texture_quality`：`standard`/`detailed`/`extreme`（影响贴图分辨率与耗时）；
  - `geometry_quality`：仅 `Tripo-H3.1` 支持 `standard`/`ultra`；
  - `face_limit`：面数上限（`Tripo-H3.1` 最高200万面，`Tripo-P1.0` 限2万面）；
  - `quad`：启用四边面输出（强制 FBX 格式）；
  - `pbr` 与 `texture`：控制 PBR 材质与贴图生成逻辑（二者均为 `false` 时输出无贴图模型）；
  - `part_names`：用于部件级操作（如分割、补全、导出），需从 GLB 节点名中提取（如 `tripo_part_0`）。

## 使用方式

所有 3D 接口均遵循统一异步流程：

1. **创建任务**：向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 提交请求，获取 `task_id`（有效期24小时）；
2. **轮询结果**：调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，建议首次查询延迟10秒，后续间隔15–30秒；
3. **状态流转**：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；`UNKNOWN` 表示 task_id 过期或不存在。

> **注意**：文档 3、4、6、7、8、9、11、12、13、14、15 均明确要求“请勿重复创建任务”，且轮询时需严格遵守 RPS 限制（默认20）。若需更高频通知，应配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)，而非暴力轮询。

## 限制和注意事项

- **地域强约束**：全部接口仅支持华北2（北京）地域，Workspace ID、API Key、服务开通均须在北京地域完成，跨地域调用必然失败。
- **输入格式与大小**：
  - 图像：JPEG/PNG/WebP，≤20MB，分辨率 [20, 6000] 像素；
  - 3D 模型（GLB/FBX/OBJ 等）：≤150MB；
  - 多图输入：`images` 数组长度必须为4，缺失视角用空对象 `{}` 占位，前视角（索引0）不可为空。
- **兼容性与依赖**：
  - 后处理任务（如贴图、分割、重拓扑）依赖前序任务成功执行，且账号必须一致；
  - `Tripo-动画重定向` 明确禁止使用 `spec: mixamo` 绑骨的模型（见文档 13）；
  - `Tripo-重拓扑` 的 `v1.0` 版本不支持 `part_names` 和 `bake` 参数（见文档 14），而 `v2.0` 支持；
  - `Tripo-网格分割` 的 `v2.0` 版本支持 `ref_image`，但传入该参数时 `segmentation_granularity` 和 `split_by_connectivity` 将失效（见文档 12）。
- **计费与性能**：
  - `face_limit`、`quad`、`texture_quality=extreme`、非默认 `out_format` 等高级参数会触发额外积分消耗；
  - Gaussian Splat 任务（文档 4）与智能分割（文档 8）耗时较长，需预留足够轮询时间；
  - `smart_low_poly`（文档 3）与 `generate_parts`（文档 3）互斥，同时开启时 `smart_low_poly` 优先生效。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)


