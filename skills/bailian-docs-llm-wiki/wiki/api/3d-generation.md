# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像和多张图像三种输入方式。该服务采用[异步任务](../concepts/asynchronous-task.md)模式，需先创建任务获取 `task_id`，再轮询查询结果。所有调用必须在华北2（北京）地域进行，并使用对应地域的 API Key。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: ultra`；详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合对时效性要求较高的场景。
- **输入模式（三者互斥）**：
  - 文生3D（`prompt`）：支持中英文，最大长度 1024 字符；
  - 单图生3D（`image`）：接受 JPEG/PNG 格式公网 URL，分辨率 [20, 6000] 像素，文件 ≤20MB；
  - 多图生3D（`images`）：固定 4 元素数组，顺序为前/左/后/右，允许传入空对象 `{}` 占位，有效图片数须为 2–4 张。

> **注意**：多图输入中各图像宽高比不要求一致，但建议视角覆盖完整，否则可能影响几何重建质量 —— 此说明与部分旧版用户指南存在表述差异，以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“多张图像的分辨率和宽高比不要求一致”为准。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `X-DashScope-Async` | string | 必填 | 必须设为 `"enable"`，同步调用不被支持；缺失将报错 `current user api does not support synchronous calls`。 |
| `model` | string | 必填 | 仅支持 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0`。 |
| `input.prompt` / `input.image` / `input.images` | string / string / array | 条件必填 | 三者互斥，不可共存。 |
| `parameters.texture_quality` | string | 可选 | `"standard"`（默认）或 `"detailed"`；影响贴图分辨率。 |
| `parameters.geometry_quality` | string | 可选 | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面）。 |
| `parameters.pbr` | boolean | 可选 | 默认 `true`；设为 `true` 时自动启用贴图并返回 `pbr_model_url`。 |
| `parameters.texture` | boolean | 可选 | 默认 `true`；如需无贴图模型，**必须同时设置 `texture: false` 和 `pbr: false`**，否则行为未定义。 |

## 使用方式

1. **开通与配置**：  
   在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索 “Tripo” 并开通服务；按 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 文档完成密钥配置。

2. **创建任务（POST）**：  
   调用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`，携带必要请求头（`Content-Type`, `Authorization`, `X-DashScope-Async`）及 JSON body。成功响应含 `task_id`（有效期 24 小时）。

3. **轮询查询结果（GET）**：  
   定期调用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`，建议间隔 ≥15 秒。状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`。成功时 `output.results` 包含 `pbr_model_url`（PBR GLB）、`base_model_url`（无贴图 GLB）或 `rendered_image_url`（预览图），所有 URL 有效期均为 2 小时。

示例（文生3D）：
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

- **地域强约束**：仅支持华北2（北京）地域，其他地域调用将失败；API Endpoint、API Key、业务空间 ID 均需严格匹配该地域。
- **任务生命周期**：`task_id` 有效期为 24 小时，超时后查询返回 `task_status: UNKNOWN`；生成结果 URL（如 `pbr_model_url`）有效期仅 2 小时，需及时下载。
- **RPS 限制**：任务查询接口默认限流 20 RPS；高频轮询场景请改用[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)机制。
- **输入校验**：`prompt`、`image`、`images` 三者严格互斥；同时传入多个将直接报错，不进入排队流程。
- **错误排查**：所有错误码及含义详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)，常见错误包括 `InvalidApiKey`、`InvalidParameter` 等。首次调用建议参考 [Postman 新手指引](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


