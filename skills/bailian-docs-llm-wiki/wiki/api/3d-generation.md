# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像或多张图像作为输入，异步返回 GLB 格式的 3D 模型（含 PBR 材质或无贴图基础模型）及预览渲染图。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key 调用 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **支持的模型**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；
  - `Tripo/Tripo-P1.0`：专业级生成，输出模型最高 2 万面，推理更快，适合快速验证。
- **输入模式（三者互斥）**：
  - 文生3D（`prompt`）：支持中英文提示词，最大 1024 字符；
  - 单图生3D（`image`）：接受 JPEG/PNG 格式公网 URL，分辨率 20–6000 像素，≤20MB；
  - 多图生3D（`images`）：固定 4 元素数组，顺序为前/左/后/右；允许传入空对象 `{}` 占位，有效图片数须为 2–4 张。

> **注意**：多图输入中各图宽高比不要求一致，但建议视角覆盖完整，否则可能影响几何重建质量 —— 具体约束详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `texture_quality` | `string` | 可选 | 贴图质量：`standard`（默认）、`detailed` |
| `geometry_quality` | `string` | 可选 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面） |
| `pbr` | `boolean` | 可选 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图 |
| `texture` | `boolean` | 可选 | 是否生成贴图（默认 `true`）；**若需无贴图模型，必须同时设置 `texture=false` 且 `pbr=false`** |

生成结果通过 `pbr_model_url`（含材质）或 `base_model_url`（无贴图）返回，所有 URL 有效期均为 **2 小时**，请及时下载。更多参数语义与取值范围，请参考原始文档 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 使用方式

采用标准异步流程：**创建任务 → 轮询查询结果**。

1. **创建任务**（POST）  
   URL（华北2）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   必填请求头：`Content-Type: application/json`、`Authorization: Bearer <API_KEY>`、`X-DashScope-Async: enable`  
   成功响应返回 `task_id`（24 小时有效），**禁止重复提交相同任务**。

2. **轮询查询**（GET）  
   URL（华北2）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议轮询间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`；RPS 默认限 20，高频轮询请配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。

示例调用（文生3D）：
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

- **地域强绑定**：仅支持华北2（北京）地域，其他地域调用将失败；业务空间 ID 和 API Key 必须同地域。
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将报错 `InvalidParameter`。
- **多图格式要求**：`images` 数组长度必须为 4，缺失视角需显式传 `{}`，不可省略或缩短数组。
- **URL 时效性**：所有返回的 `pbr_model_url`、`base_model_url`、`rendered_image_url` 有效期仅 **2 小时**，超时链接失效。
- **任务生命周期**：`task_id` 查询有效期为 **24 小时**，超时后查询返回 `task_status=UNKNOWN`。
- **错误排查**：常见错误（如 `InvalidApiKey`、`InvalidParameter`）含义及解决方案见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。首次调试建议结合 [Postman 新手指引](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 快速验证。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


