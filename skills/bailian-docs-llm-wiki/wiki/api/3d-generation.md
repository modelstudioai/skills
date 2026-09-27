# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像或多张图像作为输入，异步返回 GLB 格式的 3D 模型（含 PBR 材质或无贴图基础模型）及预览渲染图。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合高频调用；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大 1024 字符；
  - 单图生3D（`input.image`）：接受 JPEG/PNG 公网 URL，分辨率 20–6000px，≤20MB；
  - 多图生3D（`input.images`）：固定 4 元素数组，顺序为【前、左、后、右】，允许空对象占位，有效图数为 2–4 张。

> **注意**：多图输入中各图宽高比不要求一致，但建议保持相近视角一致性以提升重建质量；该约束在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确说明，与部分旧版用户指南存在表述差异，请以本文档为准。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `texture_quality` | `string` | 可选 | 贴图质量：`standard`（默认）、`detailed` |
| `geometry_quality` | `string` | 可选 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面） |
| `pbr` | `boolean` | 可选 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图 |
| `texture` | `boolean` | 可选 | 是否生成贴图（默认 `true`）；**如需无贴图模型，必须同时设 `texture=false` 且 `pbr=false`** |

详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“parameters”章节的完整定义。

## 使用方式

采用标准异步流程：**创建任务 → 轮询查询结果**。

1. **创建任务（POST）**  
   URL（华北2）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   必须携带请求头：
   - `Content-Type: application/json`
   - `Authorization: Bearer <API_KEY>`
   - `X-DashScope-Async: enable`（**缺失将报错**）

2. **轮询查询（GET）**  
   URL（华北2）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - `task_id` 有效期 **24 小时**；
   - 建议轮询间隔 ≥15 秒；
   - RPS 默认限流 20，高频场景请配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。

成功响应中，`output.results` 包含：
- `pbr_model_url`（GLB，含材质，`pbr=true` 时返回）；
- `base_model_url`（GLB，无贴图，`texture=false && pbr=false` 时返回）；
- `rendered_image_url`（WebP 预览图）。

## 限制和注意事项

- **地域强绑定**：仅支持华北2（北京）地域，控制台开通、API Key 获取、Endpoint 均需匹配该地域；
- **输入互斥性**：`prompt` / `image` / `images` 三者不可共存，同时传入将直接报错；
- **URL 时效性**：所有返回的下载链接（`pbr_model_url` 等）有效期仅 **2 小时**，需及时下载；
- **任务生命周期**：`task_id` 查询有效期为 24 小时，超期后状态返回 `UNKNOWN`；
- **错误处理**：失败任务的 `code` 和 `message` 字段需结合 [错误码文档](../../raw/model-api-reference/preparations/error-code.md) 排查，常见错误包括 `InvalidApiKey`、`InvalidParameter` 等。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


