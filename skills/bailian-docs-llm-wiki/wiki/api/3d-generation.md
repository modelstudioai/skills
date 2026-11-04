# 3d generation

百炼平台提供基于Tripo模型的3D生成能力，支持从文本、单图或多图生成高精度网格模型，以及生成Gaussian Splatting等新型3D表示。所有3D生成与后处理任务均采用[异步调用](../concepts/asynchronous-invocation.md)模式，需通过“创建任务 → 轮询查询”两步完成，且当前**仅限华北2（北京）地域可用**。

## 支持的模型/功能

3D生成能力分为三大类：**基础生成**、**后处理**和**动画**，均由Tripo系列模型提供：

- **基础生成**
  - `Tripo/Tripo-H3.1`：高精度网格生成（最高200万面），支持`geometry_quality=ultra`、`quad`、`smart_low_poly`、`generate_parts`等高级参数。
  - `Tripo/Tripo-P1.0`：专业级快速生成（最高2万面），适合对速度敏感的场景，不支持几何精度与拓扑控制类参数。
  - `Tripo/Tripo-ImageToSplat`：单图生成`.splat`文件，适用于实时渲染与真实感重建，[详见文档](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)。

- **后处理**（均需已有3D模型输入）
  - 网格处理：重拓扑（`Tripo/Tripo-Retopology`）、网格补全（`Tripo/Tripo-MeshCompletion`）、格式转换（`Tripo/Tripo-ConvertFormat`）。
  - 材质与分割：贴图生成（`Tripo/Tripo-Texture`）、网格分割（`Tripo/Tripo-Segmentation`）、智能分割（`Tripo/Tripo-SmartSegmentation`）。
  - 所有后处理接口均支持通过`original_model_task_id`引用前序任务输出，或直接传入`model_url`，[参考模型后处理总览](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)。

- **动画**
  - 绑骨流程：先调用`Tripo/Tripo-RigCheck`验证兼容性并获取`rig_type`，再使用`Tripo/Tripo-AutoRig`自动绑骨；最后通过`Tripo/Tripo-AnimationRetarget`应用预设动画。
  - 注意：`Tripo/Tripo-AutoRig`中`spec=mixamo`生成的模型**不支持**动画重定向，[详见Tripo-动画重定向说明](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)。

> **注意**：文档中多处提及“前序任务必须已执行成功”，但[Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)明确要求“前序任务不是Tripo-文生/图生3D模型任务时，须同时传入`texture_prompt`”，而[Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)未作此限制——实际调用时若引用非Tripo原生生成的任务（如第三方OBJ），仍需按贴图文档要求补充提示词，否则可能失败。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `X-DashScope-Async` | 全部 | **必填请求头**，必须设为`enable`，同步调用不被支持 | `"enable"` |
| `model` | 全部 | 模型标识符，区分大小写且不可省略 | `"Tripo/Tripo-H3.1"`, `"Tripo/Tripo-ImageToSplat"` |
| `face_limit` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 目标面数上限。`H3.1`默认自适应（150万面），`P1.0`范围为50–20,000；`Retopology`中`v1.0`与`v2.0`取值范围不同 | `50000` |
| `texture_quality` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Texture` | 贴图质量等级：`standard`（默认）、`detailed`、`extreme`（8K） | `"extreme"` |
| `quad` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat` | 是否输出四边面网格（启用后强制输出FBX格式） | `true` |
| `generate_parts` | `Tripo/Tripo-H3.1` | 是否生成可编辑的分割部件；**与`texture`/`pbr`/`quad`/`smart_low_poly`互斥** | `true` |
| `part_names` | `Tripo/Tripo-Texture`, `Tripo/Tripo-Retopology`, `Tripo/Tripo-ConvertFormat`, `Tripo/Tripo-MeshCompletion` | 指定处理的部件名列表（如`["tripo_part_0"]`），需从前序分割任务GLB中读取节点名 | `["tripo_part_0", "tripo_part_1"]` |

## 使用方式

1. **开通与认证**  
   - 在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索并开通Tripo服务；
   - 获取API Key并配置至环境变量（如`DASHSCOPE_API_KEY`），[参见密钥配置指南](../../raw/model-api-reference/preparations/get-api-key.md)。

2. **[异步调用](../concepts/asynchronous-invocation.md)流程（统一）**  
   - **步骤1：创建任务**  
     向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，携带`X-DashScope-Async: enable`及完整参数体，获取`task_id`（有效期24小时）。
   - **步骤2：轮询结果**  
     定期调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，建议首次延迟10秒，之后每15–30秒一次；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`。

3. **输入方式选择**  
   - 文生3D：传`input.prompt`（≤1024字符）；
   - 单图生3D：传`input.image`（JPEG/PNG，≤20MB，建议≥256px）；
   - 多图生3D：传`input.images`（长度为4的数组，顺序为前/左/后/右）；
   - Gaussian Splat：仅支持`input.image`（PNG/JPEG/WebP）；
   - 后处理任务：二选一——`input.original_model_task_id`（引用前序任务）或`input.model_url`（公网URL，支持GLB/FBX/OBJ等，≤150MB）。

## 限制和注意事项

- **地域与认证强约束**：所有接口**仅支持华北2（北京）地域**，且必须使用该地域的API Key，跨地域调用将失败。
- **任务ID时效性**：`task_id`有效期严格为24小时，超时后查询返回`UNKNOWN`，无法恢复结果。
- **模型兼容性限制**：
  - `Tripo/Tripo-P1.0` 不支持 `geometry_quality`、`quad`、`smart_low_poly`、`generate_parts` 等参数（传入会被忽略）；
  - `Tripo/Tripo-AutoRig` 中 `spec=mixamo` 的输出**禁止用于** `Tripo/Tripo-AnimationRetarget`；
  - `Tripo/Tripo-Segmentation` 的 `v1.0` 版本不支持 `ref_image` 参数，传入将返回400错误。
- **计费与资源**：
  - `face_limit` 非空、`quad=true`、`texture_quality=extreme`、`part_names` 非空等均触发高级计费；
  - `Tripo/Tripo-AnimationRetarget` 按动画数量计费（最多5个），`animations` 数组长度即计费数。
- **调试建议**：首次调用推荐使用Postman验证流程，[参见新手指引](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

## 来源文档

- [Tripo](../../raw/model-api-reference/3d-generation/tripo-api-reference.md)
- [Tripo-文生/图生3D模型](../../raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)
- [Tripo-图片生成Gaussian Splat](../../raw/_short/tripo-image-to-splat-api-reference-6c649387c51a1d90.md)
- [模型后处理](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-post-processing-api-reference.md)
- [Tripo-贴图](../../raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)
- [Tripo-网格分割](../../raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)
- [Tripo-智能分割](../../raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)
- [Tripo-重拓扑](../../raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)
- [Tripo-网格补全](../../raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)
- [动画](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference.md)
- [Tripo-格式转换](../../raw/_short/tripo-convert-format-api-reference-cd6936a75ce8dce3.md)
- [Tripo-自动绑骨](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)
- [Tripo-可绑骨检查](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)
- [Tripo-动画重定向](../../raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)
- [3D模型生成](../../raw/model-api-reference/3d-generation/tripo-api-reference/tripo-generation-api-reference.md)


