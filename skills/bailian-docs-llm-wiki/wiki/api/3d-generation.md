# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像及多张图像（前/左/后/右四视角）作为输入源，异步返回 GLB 格式的 3D 模型及预览图。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key 调用 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **生成模式**（三者互斥）：
  - 文生3D（`input.prompt`）
  - 单图生3D（`input.image`，支持 JPEG/PNG，≤20MB，分辨率 20–6000px）
  - 多图生3D（`input.images`，固定长度为 4 的数组，顺序为前/左/后/右；允许传入空对象 `{}` 占位，有效图数需 ≥2）

> **注意**：文档中明确要求“`prompt`、`image`、`images` 三者互斥”，但未说明是否支持 `input` 中混用字段（如同时传 `prompt` 和 `image`）。实际调用时若混用将报错，此行为与 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“同时传入多个将会报错”的描述一致，无需额外兼容。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `X-DashScope-Async` | string | 必填 | 必须设为 `"enable"`，否则返回 `current user api does not support synchronous calls` 错误 |
| `model` | string | 必填 | 取值为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 条件必填 | 文生3D时必填，≤1024 字符，支持中英文 |
| `input.image` | string | 条件必填 | 单图生3D时必填，公网可访问的 JPEG/PNG URL |
| `input.images` | array[object] | 条件必填 | 多图生3D时必填，每项含 `type`（`jpeg`/`png`）和 `file_token`（URL） |
| `parameters.texture_quality` | string | 可选 | `"standard"`（默认）或 `"detailed"` |
| `parameters.geometry_quality` | string | 可选 | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 可选 | 默认 `true`；设为 `true` 时强制启用贴图，返回 `pbr_model_url` |
| `parameters.texture` | boolean | 可选 | 默认 `true`；如需无贴图模型，**必须同时设 `texture=false` 且 `pbr=false`**，返回 `base_model_url` |

## 使用方式

采用标准异步两步流程：

1. **创建任务**：  
   `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   成功响应返回 `task_id`（有效期 24 小时），**禁止重复创建相同任务**，应轮询获取结果。

2. **轮询查询**：  
   `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议轮询间隔 ≥15 秒；  
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；  
   - `SUCCEEDED` 时 `output.results` 包含 `pbr_model_url`（PBR 材质）、`base_model_url`（无贴图）或 `rendered_image_url`（预览图）；所有 URL 有效期均为 **2 小时**，需及时下载。  
   更多管理操作（如取消、批量查询）见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“管理异步任务”章节。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，API Endpoint、API Key、业务空间 ID 均需与该地域匹配，跨地域调用必然失败。
- **认证要求**：必须配置北京地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，且通过 `Authorization: Bearer sk-xxx` 传递；环境变量配置方式参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询建议配置 [异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **输入校验**：图像 URL 必须公网可访问、协议为 HTTP/HTTPS；多图模式下 `images` 数组长度必须为 4，缺失视角需显式传 `{}`，不可省略或缩短数组。
- **产物时效性**：`task_id` 有效期 24 小时，模型下载 URL 有效期 2 小时，超时即失效，无自动续期机制。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


