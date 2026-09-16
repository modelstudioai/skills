# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像及多张图像（前/左/后/右视角）三种输入方式。该服务为异步任务模式，需通过创建任务 + 轮询结果两步完成调用，适用于华北2（北京）地域。所有请求必须配置有效的 API Key 并显式声明 `X-DashScope-Async: enable` 头。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: ultra`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合对速度敏感的场景；对应 Tripo 官方 API 版本 `P1-20260311`。

- **输入模式（三者互斥）**：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大长度 1024 字符。
  - 单图生3D（`input.image`）：接受 JPEG/PNG 格式公网 URL，分辨率 [20, 6000] 像素，文件 ≤20MB。
  - 多图生3D（`input.images`）：固定长度为 4 的数组，顺序为前/左/后/右；允许传入空对象 `{}` 占位，有效图片数需 ≥2。各图格式与单图要求一致。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求仅华北2（北京）地域可用，且未提及其它地域支持计划；若在其它地域调用将失败，此限制在[使用指南](../../raw/model-user-guide/model-experience/tripo-3d-generation-guide.md)中亦被同步强调。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `texture_quality` | string | 可选 | 贴图质量，取值 `standard`（默认）或 `detailed`。影响 `pbr_model_url` 输出效果。 |
| `geometry_quality` | string | 可选 | 仅 `Tripo/Tripo-H3.1` 支持；`standard`（≤150 万面）或 `ultra`（≤200 万面）。 |
| `pbr` | boolean | 可选 | 是否生成 PBR 材质模型（默认 `true`）。设为 `true` 时自动启用贴图（即强制 `texture=true`）。 |
| `texture` | boolean | 可选 | 是否生成贴图（默认 `true`）。**如需无贴图模型，必须同时设置 `texture=false` 且 `pbr=false`**，此时返回 `base_model_url`。 |

详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“parameters”章节的完整定义。

## 使用方式

采用标准异步流程：

1. **创建任务**（POST）  
   URL（华北2）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   必须携带以下请求头：
   - `Content-Type: application/json`
   - `Authorization: Bearer <API_KEY>`
   - `X-DashScope-Async: enable`（**缺失将报错**：“current user api does not [support](../guides/support.md) synchronous calls”）

   成功响应含 `task_id`（有效期 24 小时），**禁止重复提交相同任务**，应复用该 ID 轮询。

2. **轮询结果**（GET）  
   URL（华北2）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议轮询间隔 ≥15 秒；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`。  
   成功时 `output.results` 包含：
   - `pbr_model_url`（GLB，含 PBR 材质，2 小时有效）
   - `base_model_url`（GLB，无贴图，仅当 `texture=false && pbr=false` 时返回）
   - `rendered_image_url`（预览图，WebP 格式，2 小时有效）

详细调用示例（含文生、单图、多图、无贴图等场景）见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“HTTP调用”部分。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，控制台开通、API Key 配置、请求 URL 均需匹配该地域。跨地域调用将失败。
- **任务生命周期**：
  - `task_id` 有效期严格为 **24 小时**，超时后查询返回 `task_status: UNKNOWN`。
  - 结果 URL（`pbr_model_url` 等）有效期仅 **2 小时**，需及时下载。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询建议改用[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **输入校验**：
  - `prompt`、`image`、`images` 三者严格互斥，同时传入任两者将导致 `InvalidParameter` 错误。
  - `images` 数组长度必须为 4；无效项（如非空但缺少 `file_token`）将触发校验失败。
- **模型能力边界**：`Tripo/Tripo-P1.0` 不支持 `geometry_quality` 参数；若误传将被忽略或报错，具体行为以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 实际响应为准。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


