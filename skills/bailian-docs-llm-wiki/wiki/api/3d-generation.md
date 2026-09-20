# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像及多张图像三种输入方式生成 GLB 格式的 3D 模型。该服务为异步任务型 API，需通过“创建任务 → 轮询查询”两步完成调用，适用于华北2（北京）地域。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合对速度敏感的场景；对应 Tripo 官方 API 版本 `P1-20260311`。

- **生成模式**（三者互斥，不可同时指定）：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大长度 1024 字符；
  - 单图生3D（`input.image`）：接受 JPEG/PNG 公网 URL，分辨率 [20, 6000] 像素，单图 ≤20MB；
  - 多图生3D（`input.images`）：固定长度为 4 的数组，顺序为【前、左、后、右】，允许部分为空对象 `{}`，有效图数需 ≥2；每张图限制同单图。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求所有调用必须使用华北2（北京）地域的 API Key 和 Endpoint，其他地域暂不支持 —— 若在非北京地域配置了 API Key 但未切换 Endpoint，将返回 `InvalidApiKey` 或 `UnsupportedRegion` 类错误。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `X-DashScope-Async` | string | 必填 | **必须设为 `"enable"`**，否则报错 `current user api does not support synchronous calls` |
| `model` | string | 必填 | 取值为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | 条件必填 | 三者仅可选其一；详见[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) |
| `parameters.texture_quality` | string | 可选 | `"standard"`（默认）或 `"detailed"` |
| `parameters.geometry_quality` | string | 可选 | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 可选 | 默认 `true`；设为 `true` 时强制启用贴图，并返回 `pbr_model_url` |
| `parameters.texture` | boolean | 可选 | 默认 `true`；若需无贴图模型，**必须同时设 `texture: false` 且 `pbr: false`**，此时返回 `base_model_url` |

## 使用方式

1. **前置准备**：
   - 在[百炼控制台（北京地域）](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 模型服务；
   - 获取并配置北京地域专用的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，推荐通过环境变量注入（参见[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。

2. **[异步调用](../concepts/asynchronous-invocation.md)流程**：
   - **步骤1：创建任务**  
     向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，获取 `task_id`（有效期 24 小时）。
   - **步骤2：轮询结果**  
     定期（建议间隔 ≥15 秒）调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，直至 `task_status === "SUCCEEDED"`。成功响应中 `output.results` 包含 `pbr_model_url`（默认）或 `base_model_url`（无贴图时），所有 URL 有效期均为 **2 小时**，须及时下载。

3. **示例（文生3D）**：
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
     -H 'X-DashScope-Async: enable' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H 'Content-Type: application/json' \
     -d '{
       "model": "Tripo/Tripo-P1.0",
       "input": { "prompt": "一只可爱的猫" },
       "parameters": { "texture_quality": "standard" }
     }'
   ```

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，Endpoint、API Key、控制台开通入口均需匹配该地域 —— 此限制在[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)中多次强调，跨地域调用必然失败。
- **任务生命周期**：`task_id` 有效期严格为 24 小时；超时后查询返回 `task_status: "UNKNOWN"`，无法恢复。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询场景请改用[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)机制。
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将直接报错 `InvalidParameter`。
- **无贴图模型生成**：必须显式设置 `"texture": false, "pbr": false`，仅设 `texture: false` 不生效（因 `pbr: true` 默认强制启用贴图）。
- **多图视角规范**：`images` 数组长度必须为 4，缺失视角需填空对象 `{}`，不可省略或缩短数组 —— 违反此规则将导致 `InvalidParameter` 错误。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


