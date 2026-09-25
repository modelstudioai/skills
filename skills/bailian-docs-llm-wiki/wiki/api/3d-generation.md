# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像或多张图像作为输入，异步返回 GLB 格式的 3D 模型（含 PBR 材质或无贴图基础模型）及预览渲染图。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key 调用 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D（`prompt`）：支持中英文等多语言，最大长度 1024 字符；
  - 单图生3D（`image`）：接受 JPEG/PNG 格式公网 URL，分辨率 20–6000 像素，文件 ≤20MB；
  - 多图生3D（`images`）：固定 4 元素数组，顺序为【前、左、后、右】；允许空对象 `{}` 占位，有效图片数需 ≥2；各图独立满足单图限制。

> **注意**：文档中明确要求“`prompt`、`image`、`images` 三者互斥”，但未说明当 `input` 中同时缺失三者时的行为。实际调用将返回 `InvalidParameter` 错误，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的请求体说明。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `texture_quality` | string | 否 | 贴图质量：`standard`（默认）、`detailed` |
| `geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面） |
| `pbr` | boolean | 否 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图 |
| `texture` | boolean | 否 | 是否生成贴图（默认 `true`）；如需无贴图模型，**必须同时设置 `texture=false` 且 `pbr=false`** |

> **注意**：`pbr` 和 `texture` 的组合逻辑存在隐式依赖——当 `pbr=true` 时，系统强制启用贴图（即忽略 `texture=false`）。该行为在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的 `pbr` 参数描述中有明确说明，开发者需严格遵循此约束。

## 使用方式

采用标准异步流程：**创建任务 → 轮询查询结果**。

1. **创建任务（POST）**  
   地域专属 URL（华北2）：  
   `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   必须携带以下请求头：
   - `Content-Type: application/json`
   - `Authorization: Bearer <API_KEY>`
   - `X-DashScope-Async: enable`（**缺失将报错**）

2. **轮询查询（GET）**  
   URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - `task_id` 有效期 **24 小时**；
   - 建议轮询间隔 ≥15 秒；
   - RPS 限制为 20，高频场景请配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。

成功响应中，`output.results` 包含：
- `pbr_model_url`：PBR 材质 GLB 模型（`pbr=true` 时返回）；
- `base_model_url`：无贴图基础 GLB 模型（`texture=false && pbr=false` 时返回）；
- `rendered_image_url`：1 张预览渲染图（WebP 格式）。

详细调用示例（含文生、单图、多图、无贴图）见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，其他地域 URL 不可用；
- **开通前提**：需在百炼控制台 [开通 Tripo 服务](https://bailian.console.aliyun.com/cn-beijing/model/market) 并完成授权；
- **API Key 配置**：必须使用北京地域生成的 API Key，并正确配置至环境变量或请求头；
- **任务生命周期**：
  - `task_id` 有效期 24 小时，超期后查询返回 `task_status=UNKNOWN`；
  - 所有下载 URL（`pbr_model_url` 等）有效期仅 **2 小时**，需及时下载；
- **输入校验**：`prompt`/`image`/`images` 严格互斥；多图模式下 `images` 数组长度必须为 4，空视角须显式传 `{}`；
- **错误处理**：所有错误码及含义详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)，创建失败常见原因包括 `InvalidApiKey`、`InvalidParameter`。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


