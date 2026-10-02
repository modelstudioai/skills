# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像或多张图像作为输入，异步返回 GLB 格式的 3D 模型（含 PBR 材质或无贴图基础模型）及预览渲染图。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key 调用 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合高频调试。
- **输入模式（三者互斥）**：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大 1024 字符；
  - 单图生3D（`input.image`）：接受 JPEG/PNG 公网 URL，分辨率 20–6000px，≤20MB；
  - 多图生3D（`input.images`）：严格按 `[前, 左, 后, 右]` 顺序传入 2–4 张图，空视角用 `{}` 占位。

> **注意**：文档中明确说明“`prompt`、`image`、`images` 三者互斥”，但部分旧版示例未加校验注释；实际调用时若同时传入将返回 `InvalidParameter` 错误 —— 请以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的参数定义为准。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `texture_quality` | string | 否 | 贴图质量：`standard`（默认）、`detailed` |
| `geometry_quality` | string | 否 | 仅 `Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面） |
| `pbr` | boolean | 否 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图 |
| `texture` | boolean | 否 | 是否生成贴图（默认 `true`）；**如需无贴图模型，必须同时设 `texture=false` 且 `pbr=false`** |

成功响应中通过 `results` 返回不同产物 URL：
- `pbr_model_url`：PBR 材质 GLB（当 `pbr=true` 时返回）；
- `base_model_url`：无贴图基础 GLB（仅当 `texture=false && pbr=false` 时返回）；
- `rendered_image_url`：1 张预览渲染图（WebP）。

所有下载链接有效期均为 **2 小时**，需及时保存。

## 使用方式

采用标准异步两步流程（详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)）：

1. **创建任务**（POST）：
   - Endpoint（北京地域）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
   - 必须携带请求头：`X-DashScope-Async: enable`、`Authorization: Bearer <API_KEY>`、`Content-Type: application/json`
   - 响应返回 `task_id`（24 小时有效），**禁止重复提交相同任务**

2. **轮询结果**（GET）：
   - Endpoint：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`
   - 建议轮询间隔 ≥15 秒；RPS 默认限流 20，高频场景请配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；`UNKNOWN` 表示 task_id 过期或不存在

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，控制台开通、API Key 获取、Endpoint 均需匹配该地域；
- **输入互斥性**：`prompt` / `image` / `images` 三者不可共存，否则返回 `InvalidParameter`；
- **图片规范**：单图/多图均要求公网可访问、格式为 JPEG/PNG、单图 ≤20MB；多图数组长度固定为 4，缺失视角必须显式填 `{}`；
- **产物时效性**：`pbr_model_url` 和 `base_model_url` 有效期 2 小时，`task_id` 查询有效期 24 小时；
- **错误排查**：所有错误码及含义详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)，常见错误包括 `InvalidApiKey`、`InvalidParameter`、`TaskExpired`。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


