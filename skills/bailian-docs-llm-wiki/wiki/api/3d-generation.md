# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像及多张图像（前/左/后/右四视角）作为输入源，异步返回 GLB 格式的 3D 模型及预览图。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key 调用 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D（`prompt`）：支持中英文，最大 1024 字符；
  - 单图生3D（`image`）：JPEG/PNG，分辨率 20–6000px，≤20MB；
  - 多图生3D（`images`）：固定长度为 4 的数组，按「前、左、后、右」顺序填充，空视角传 `{}`，有效图数需 ≥2。

> **注意**：原始文档中 `images` 数组描述为“长度固定为4”，但实际允许部分元素为空对象 `{}`；该行为与 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中示例一致，属合法用法，非 Bug。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `X-DashScope-Async` | string | 必填 | 必须设为 `"enable"`，同步调用将报错 `"current user api does not support synchronous calls"` |
| `model` | string | 必填 | 仅支持 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | 条件必填 | 三者互斥，详见上节输入模式 |
| `parameters.texture_quality` | string | 可选 | `"standard"`（默认）或 `"detailed"` |
| `parameters.geometry_quality` | string | 可选 | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 可选 | 默认 `true`；设为 `true` 时强制启用贴图，返回 `pbr_model_url` |
| `parameters.texture` | boolean | 可选 | 默认 `true`；如需无贴图模型，**必须同时设 `texture=false` 且 `pbr=false`**，返回 `base_model_url` |

所有 URL 均需替换 `{WorkspaceId}` 为真实业务空间 ID，并确保使用华北2（北京）地域 endpoint —— 此限制在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确强调。

## 使用方式

采用标准异步两步流程：

1. **创建任务**：`POST /api/v1/services/aigc/video-generation/3d-generation`  
   返回 `task_id`（有效期 24 小时），**禁止重复提交相同请求**，应轮询获取结果。

2. **轮询查询**：`GET /api/v1/tasks/{task_id}`  
   - 建议轮询间隔 ≥15 秒；
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；
   - 成功响应中 `results` 包含 `pbr_model_url`（PBR 材质）、`base_model_url`（无贴图）或 `rendered_image_url`（预览图），所有 URL 有效期均为 **2 小时**，需及时下载。

完整调用链路与各模式示例（文生、单图、多图、无贴图）详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，控制台开通、API Key 获取、Endpoint 均需匹配该地域。
- **任务生命周期**：
  - `task_id` 有效期：24 小时（超时查询返回 `task_status=UNKNOWN`）；
  - 结果 URL（`pbr_model_url` 等）有效期：2 小时；
  - 查询接口 RPS 限流：默认 20，高频轮询建议配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **输入校验**：
  - `prompt`、`image`、`images` 三者严格互斥，同时传入任两个将直接报错；
  - `images` 数组必须为长度 4，缺失视角必须显式传 `{}`，不可省略或传 `null`。
- **资源要求**：多图输入建议各图分辨率 ≥256px 且内容视角差异明显，否则几何重建质量下降显著。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


