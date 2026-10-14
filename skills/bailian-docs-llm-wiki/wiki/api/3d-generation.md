# 3d generation

百炼平台提供基于 Tripo 模型的 3D 内容生成能力，支持文本、单图及多图三种输入方式生成 GLB 格式的 3D 模型。该能力为异步任务型 API，需通过“创建任务 → 轮询查询”两阶段完成，适用于华北2（北京）地域。所有调用均需配置有效的 API Key 并显式声明 `X-DashScope-Async: enable` 请求头。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合高频调试；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D（`prompt`）：支持中英文提示词，最大长度 1024 字符；
  - 单图生3D（`image`）：接受 JPEG/PNG 公网 URL，分辨率 [20, 6000] 像素，文件 ≤20MB；
  - 多图生3D（`images`）：严格按 `[前, 左, 后, 右]` 顺序传入 2–4 张图，空视角用 `{}` 占位；每张图限制同单图。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求仅支持华北2（北京）地域，且必须使用该地域的 API Key —— 若在其他地域调用将直接报错，此限制未在通用模型接入文档中体现，开发者需特别注意。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `texture_quality` | `string` | 可选 | 贴图质量，取值 `"standard"`（默认）或 `"detailed"` |
| `geometry_quality` | `string` | 可选 | 仅 `Tripo/Tripo-H3.1` 支持，取值 `"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `pbr` | `boolean` | 可选 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图 |
| `texture` | `boolean` | 可选 | 是否生成贴图（默认 `true`）；**若需无贴图模型，必须同时设置 `texture: false` 且 `pbr: false`** |

> **注意**：当 `pbr: true` 时，`texture` 将被强制置为 `true`，无法单独关闭贴图；该行为与部分旧版文档描述存在偏差，以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的最新说明为准。

## 使用方式

1. **开通与准备**  
   在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索并开通 “Tripo” 模型服务；按 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 文档完成密钥配置，并确保环境变量 `DASHSCOPE_API_KEY` 已就绪。

2. **创建任务（POST）**  
   调用地址（北京地域）：  
   `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   **必需请求头**：`Content-Type: application/json`、`Authorization: Bearer <key>`、`X-DashScope-Async: enable`  
   成功响应返回 `task_id`（有效期 24 小时），**禁止重复提交相同任务**。

3. **轮询查询结果（GET）**  
   调用地址：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议轮询间隔 ≥15 秒；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`；成功时 `results` 中返回 `pbr_model_url`（PBR 模型）或 `base_model_url`（无贴图模型），所有 URL 有效期均为 2 小时。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，跨地域调用将失败，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **异步强制性**：不支持同步调用，缺失 `X-DashScope-Async: enable` 头将返回错误 `"current user api does not support synchronous calls"`。
- **任务生命周期**：`task_id` 有效期 24 小时，超时后查询返回 `task_status: "UNKNOWN"`；生成结果 URL 有效期 2 小时，需及时下载。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频率轮询场景建议配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **图像规范**：多图输入必须严格按 `[前, 左, 后, 右]` 顺序排列，缺失视角须显式传 `{}`，不可省略或错序。
- **错误处理**：所有错误码及含义请参考统一 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


