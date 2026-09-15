# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像及多张图像（前/左/后/右视角）三种输入方式。该服务为异步任务模式，需通过任务创建与轮询查询两步完成，适用于华北2（北京）地域。详细实现细节请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **生成模式**（三者互斥，不可同时指定）：
  - 文生3D（`input.prompt`）
  - 单图生3D（`input.image`，需公网可访问 JPEG/PNG URL）
  - 多图生3D（`input.images`，固定长度为 4 的数组，顺序为前/左/后/右；空视角用 `{}` 占位，有效图数须为 2–4 张）

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求仅支持华北2（北京）地域，且必须使用该地域的 API Key；其他地域 URL 或密钥配置将导致 `InvalidApiKey` 或 `UnsupportedRegion` 类错误。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `X-DashScope-Async` | string | 是 | **必须设为 `"enable"`**，同步调用不被支持，缺失将报错 `"current user api does not support synchronous calls"` |
| `model` | string | 是 | 取值为 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` | string | 条件必填 | 文生3D时必填；≤1024 字符，支持中英文等多语言 |
| `input.image` | string | 条件必填 | 单图生3D时必填；JPEG/PNG，宽高 ∈ [20, 6000] 像素，≤20MB |
| `input.images` | array[object] | 条件必填 | 多图生3D时必填；每项含 `type`（`jpeg`/`png`）和 `file_token`（公网 URL） |
| `parameters.texture_quality` | string | 否 | `"standard"`（默认）或 `"detailed"` |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `true` 时强制启用贴图，返回 `pbr_model_url` |
| `parameters.texture` | boolean | 否 | 默认 `true`；如需无贴图模型，**必须同时设 `texture: false` 且 `pbr: false`**，返回 `base_model_url` |

## 使用方式

1. **开通与准备**  
   - 在 [百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market) 搜索并开通 “Tripo” 模型；  
   - 获取并配置 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，确保环境变量 `DASHSCOPE_API_KEY` 已设置；  
   - 替换请求 URL 中的 `{WorkspaceId}` 为实际业务空间 ID（参见 [获取 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)）。

2. **发起异步任务**  
   向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 提交请求，示例（文生3D）：
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
   成功响应含 `task_id`（有效期 24 小时），**禁止重复创建任务**。

3. **轮询查询结果**  
   使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询，建议间隔 ≥15 秒。状态流转为：`PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`。成功时 `output.results` 返回 `pbr_model_url`（PBR 材质 GLB）、`base_model_url`（无贴图 GLB）或 `rendered_image_url`（预览图）。所有 URL 有效期均为 **2 小时**，需及时下载。

更多操作（如批量查询、取消任务、回调配置）详见 [管理异步任务](../../raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md) 和 [异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，跨地域调用必然失败；该限制在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中被多次强调，开发者务必核对 endpoint 与 API Key 地域一致性。
- **输入互斥性**：`prompt`、`image`、`images` 三者严格互斥，同时传入任两个将直接返回参数错误（`InvalidParameter`）。
- **多图视角规范**：`images` 数组长度必须为 4，顺序固定为【前、左、后、右】；缺失视角必须显式传 `{}`，不可省略或缩短数组。
- **无贴图模型条件**：仅当 `texture: false` **且** `pbr: false` 同时成立时，才返回 `base_model_url`；单独设 `texture: false` 仍会生成 PBR 贴图。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询场景请改用 [异步回调](../../raw/model-api-reference/more-about-models/async-task-api.md) 避免触发限流。
- **超时处理**：`task_id` 24 小时后失效，查询返回 `task_status: "UNKNOWN"`；生成结果 URL 2 小时后过期，需在有效期内完成下载。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


