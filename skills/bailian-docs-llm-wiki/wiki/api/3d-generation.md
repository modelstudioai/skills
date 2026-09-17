# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像及多张图像（前/左/后/右四视角）三种输入方式。该服务为异步任务模式，需通过任务创建与轮询两步完成，适用于华北2（北京）地域。所有调用均需配置有效的 API Key 并显式声明 `X-DashScope-Async: enable` 请求头。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合对延迟敏感的场景。
- **输入模态**（三者互斥）：
  - 文生3D：通过 `input.prompt` 提供中文或英文提示词（≤1024 字符）；
  - 单图生3D：通过 `input.image` 提供单张 JPEG/PNG 图像 URL（分辨率 20–6000px，≤20MB）；
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，按**前、左、后、右**顺序填入图像对象（空视角可用 `{}` 占位），实际有效图数需 ≥2。

> **注意**：文档中明确要求“仅适用于华北2（北京）地域”，且必须使用该地域的 API Key；若在其他地域调用将失败。请务必参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的地域与鉴权说明。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `texture_quality` | string | 否 | 贴图质量，可选 `standard`（默认）、`detailed`；影响 `pbr_model_url` 输出效果。 |
| `geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持，可选 `standard`（≤150 万面）、`ultra`（≤200 万面）。 |
| `pbr` | boolean | 否 | 是否启用 PBR 材质（默认 `true`）；设为 `true` 时自动启用贴图，返回 `pbr_model_url`。 |
| `texture` | boolean | 否 | 是否生成贴图（默认 `true`）；如需无贴图模型，**必须同时设置 `texture=false` 且 `pbr=false`**，此时返回 `base_model_url`。 |

## 使用方式

1. **开通与准备**：  
   在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索并开通 Tripo 模型；按 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 要求获取并配置 API Key 到环境变量。

2. **创建任务（POST）**：  
   调用 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`，请求头必须包含：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer <API_KEY>`  
   - `X-DashScope-Async: enable`（缺失将报错：“current user api does not [support](../guides/support.md) synchronous calls”）

3. **轮询结果（GET）**：  
   使用返回的 `task_id` 轮询 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`；建议间隔 ≥15 秒，`task_id` 有效期为 24 小时。

4. **结果解析**：  
   - 成功（`task_status=SUCCEEDED`）时，`output.results` 中包含 `pbr_model_url`（PBR GLB）、`base_model_url`（无贴图 GLB）或 `rendered_image_url`（预览图）；所有 URL 有效期 2 小时。  
   - 失败时检查 `output.code` 和 `output.message`，对照 [错误码](../../raw/model-api-reference/preparations/error-code.md) 排查。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，URL、API Key、控制台操作均须匹配该地域；跨地域调用必然失败。
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将返回参数校验错误。
- **多图格式要求**：`images` 数组长度固定为 4，顺序不可变更；无效项必须显式传 `{}`，不可省略或传 `null`。
- **无贴图模型配置**：必须同时设置 `"texture": false, "pbr": false`，仅设其一无效。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询建议改用[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **任务生命周期**：`task_id` 24 小时后失效，超期查询返回 `task_status=UNKNOWN`；任务不可重复提交，应复用 `task_id` 轮询。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


