# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像或多张图像作为输入，异步返回 GLB 格式的 3D 模型（含 PBR 材质或无贴图基础模型）及预览渲染图。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合高频调试；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大 1024 字符；
  - 单图生3D（`input.image`）：接受 JPEG/PNG 公网 URL，分辨率 20–6000px，≤20MB；
  - 多图生3D（`input.images`）：严格按 `[前, 左, 后, 右]` 顺序传入 2–4 张图（空对象 `{}` 表示跳过某视角）。

> **注意**：多图输入中各图宽高比不要求一致，但建议保持主体居中、光照均匀；该约束在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确说明，与部分旧版用户指南存在表述差异，请以本文档为准。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `texture_quality` | `string` | 可选 | 贴图质量：`standard`（默认）、`detailed`；仅当 `texture: true` 时生效。 |
| `geometry_quality` | `string` | 可选 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面）。 |
| `pbr` | `boolean` | 可选 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图。 |
| `texture` | `boolean` | 可选 | 是否生成贴图（默认 `true`）；**若需无贴图模型，必须同时设置 `texture: false` 且 `pbr: false`**，否则将忽略 `texture` 设置。 |

所有参数均在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的 `parameters` 小节中明确定义，开发者应严格遵循该文档的组合规则。

## 使用方式

采用标准异步两步流程：

1. **创建任务**（`POST /api/v1/services/aigc/video-generation/3d-generation`）：
   - 必须携带请求头：`X-DashScope-Async: enable`、`Authorization: Bearer <API_KEY>`、`Content-Type: application/json`；
   - 响应中提取 `output.task_id`，有效期 **24 小时**；
   - 示例见原始文档中各类输入模式的 curl 调用片段。

2. **轮询查询结果**（`GET /api/v1/tasks/{task_id}`）：
   - 建议轮询间隔 ≥15 秒；
   - 状态流转：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；
   - 成功响应中 `output.results` 包含 `pbr_model_url`（PBR 模型）、`base_model_url`（无贴图模型）或 `rendered_image_url`（预览图），所有 URL 有效期 **2 小时**，需及时下载。

详细调用链路、错误码及回调配置请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强绑定**：仅支持华北2（北京）地域，URL 域名为 `cn-beijing.maas.aliyuncs.com`，且 API Key 必须在该地域开通并配置；
- **任务生命周期**：`task_id` 有效期 24 小时，结果 URL 有效期 2 小时，超时后链接失效；
- **RPS 限制**：任务查询接口默认限流 20 RPS，高频轮询场景建议配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)；
- **输入校验**：`prompt`/`image`/`images` 三者严格互斥，同时传入将直接报错 `InvalidParameter`；
- **模型面数与性能权衡**：`Tripo-P1.0` 速度更快但面数上限低（2 万），`Tripo-H3.1` 面数高但耗时更长，需按业务需求选择；
- **开通前提**：需在百炼控制台 [开通 Tripo 服务](https://bailian.console.aliyun.com/cn-beijing/model/market) 并完成 API Key 授权。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


