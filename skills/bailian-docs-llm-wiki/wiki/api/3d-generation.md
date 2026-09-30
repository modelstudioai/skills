# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像或多张图像作为输入，异步生成 GLB 格式的 3D 模型（含 PBR 材质或无贴图基础模型）。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key，并遵循严格的异步任务流程（创建任务 → 轮询查询结果）[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合对时延敏感场景；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D（`prompt`）：支持中英文提示词，最大 1024 字符；
  - 单图生3D（`image`）：接受 JPEG/PNG 格式公网 URL，分辨率 [20, 6000] 像素，文件 ≤20MB；
  - 多图生3D（`images`）：严格按 `[前, 左, 后, 右]` 顺序传入 2~4 张图（空对象 `{}` 表示跳过某视角），每张图限制同单图。

> **注意**：文档中明确要求 `input` 的三个字段（`prompt`/`image`/`images`）**互斥且仅能选其一**，但部分旧版 SDK 示例曾允许混合传参，该行为已被废弃，以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `texture_quality` | string | 否 | 贴图质量：`standard`（默认）、`detailed`；仅当 `texture: true`（默认）时生效。 |
| `geometry_quality` | string | 否 | 几何精度：仅 `Tripo/Tripo-H3.1` 支持；`standard`（≤150 万面，默认）、`ultra`（≤200 万面）。 |
| `pbr` | boolean | 否 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图（即 `texture` 强制为 `true`）。 |
| `texture` | boolean | 否 | 是否生成贴图（默认 `true`）；如需无贴图模型，**必须同时设置 `texture: false` 和 `pbr: false`**，否则行为未定义 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。 |

## 使用方式

1. **前置准备**：
   - 在华北2（北京）地域开通 Tripo 服务：[阿里云百炼控制台 → 模型市场 → 搜索“Tripo” → 立即开通](https://bailian.console.aliyun.com/cn-beijing/model/market)；
   - 配置该地域专用的 API Key 到环境变量（如 `DASHSCOPE_API_KEY`），详见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

2. **异步调用流程（两步）**：
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     必须携带请求头：`X-DashScope-Async: enable`、`Authorization: Bearer <key>`、`Content-Type: application/json`；  
     成功响应返回 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。
   - **步骤2：轮询查询**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议轮询间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；  
     成功时 `output.results` 包含 `pbr_model_url`（PBR GLB）、`base_model_url`（无贴图 GLB）或 `rendered_image_url`（预览图），所有 URL 有效期均为 2 小时。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 或 API Key 均不可用；
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超时后查询返回 `task_status: "UNKNOWN"`，无法恢复；
- **RPS 限制**：任务查询接口默认限流 20 RPS，高频轮询建议改用 [异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)；
- **图像要求**：多图输入必须严格按 `[前, 左, 后, 右]` 顺序，缺失视角需显式传 `{}`，不可省略数组元素；
- **错误处理**：所有失败响应均含 `code` 和 `message`，应结合 [错误码文档](../../raw/model-api-reference/preparations/error-code.md) 排查，常见错误包括 `InvalidApiKey`、`InvalidParameter` 等。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


