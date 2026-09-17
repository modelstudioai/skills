# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文生3D、单图生3D 和多图生3D 三种输入模式。该能力为[异步任务](../concepts/asynchronous-task.md)型 API，需通过“创建任务 → 轮询查询”两步完成，适用于华北2（北京）地域。所有调用均需配置有效的 API Key 并显式声明 `X-DashScope-Async: enable` 请求头。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度模型，输出面数最高 200 万，支持 `geometry_quality=ultra`；详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
  - `Tripo/Tripo-P1.0`：专业级模型，输出面数最高 2 万，推理速度更快，适合快速原型验证。
- **输入模式（三者互斥）**：
  - 文生3D：通过 `input.prompt` 提供中文/英文提示词（≤1024 字符）；
  - 单图生3D：通过 `input.image` 提供单张 JPEG/PNG 图像 URL（分辨率 20–6000px，≤20MB）；
  - 多图生3D：通过 `input.images` 提供长度为 4 的数组，按**前、左、后、右**顺序传入图像对象（空视角可填 `{}`），有效图像数须为 2–4 张。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求仅支持华北2（北京）地域，且 URL 中的 `{WorkspaceId}` 必须与该地域绑定；跨地域调用将失败，不可复用其他地域的 Workspace ID。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `texture_quality` | string | 否 | 贴图质量：`standard`（默认）、`detailed`；影响 `pbr_model_url` 输出效果 |
| `geometry_quality` | string | 否 | 仅 `Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面） |
| `pbr` | boolean | 否 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图 |
| `texture` | boolean | 否 | 是否生成贴图（默认 `true`）；**如需无贴图模型，必须同时设 `texture=false` 且 `pbr=false`**，此时返回 `base_model_url` |

所有结果 URL（如 `pbr_model_url`、`base_model_url`、`rendered_image_url`）有效期均为 **2 小时**，请务必及时下载。任务 ID（`task_id`）有效期为 **24 小时**，超期后查询返回 `UNKNOWN` 状态。

## 使用方式

1. **前置准备**：
   - 在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market) 开通 Tripo 服务；
   - 配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md) 至环境变量或请求头；
2. **创建任务（POST）**：
   - 地域专属 URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须携带请求头：`Content-Type: application/json`、`Authorization: Bearer <key>`、`X-DashScope-Async: enable`
   - 响应中提取 `output.task_id`，用于后续轮询；
3. **轮询查询（GET）**：
   - URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议轮询间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`
   - 成功响应中，`output.results` 包含 `pbr_model_url` 或 `base_model_url`（取决于参数组合）

完整调用示例（文生3D）见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的 cURL 片段。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域调用将报错，且 Workspace ID 不可跨地域复用；
- **异步强制性**：同步调用不被支持，缺失 `X-DashScope-Async: enable` 头将返回 `"current user api does not support synchronous calls"` 错误；
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将导致 `InvalidParameter` 错误；
- **多图格式要求**：`images` 数组长度必须为 4，视角顺序固定为【前、左、后、右】；空视角必须显式传 `{}`，不可省略或传 `null`；
- **RPS 限制**：任务查询接口默认限流 20 RPS，高频轮询建议改用 [异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md) 机制；
- **资源时效性**：所有结果 URL 2 小时过期，`task_id` 24 小时过期，超期后无法重试或补查。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


