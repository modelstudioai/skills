# 3d generation

百炼平台的 3d generation 能力基于 Tripo 模型提供文生3D、单图生3D 和多图生3D 三种生成模式，适用于快速构建可交付的 GLB 格式三维模型。该能力为异步任务型 API，需通过 `task_id` 轮询获取结果，不支持同步调用。所有调用必须在华北2（北京）地域发起，并使用该地域绑定的 API Key。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级生成，输出模型最高 2 万面，推理更快；对应 Tripo 官方 API 版本 `P1-20260311`。

- **输入模式（三者互斥）**：
  - 文生3D：通过 `input.prompt` 描述目标模型（最大 1024 字符，支持中英文）；
  - 单图生3D：通过 `input.image` 提供单张 JPEG/PNG 图像 URL（分辨率 20–6000px，≤20MB）；
  - 多图生3D：通过 `input.images` 提供 2~4 张图像，顺序固定为「前、左、后、右」，空视角传 `{}` 即可。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求多图输入数组长度**固定为 4**，但实际有效图片数为 2~4 张；若传入少于 2 张有效图（如仅 1 张非空），将返回 `InvalidParameter` 错误。该行为与部分旧版用户指南描述存在偏差，以本 API 文档为准。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `texture_quality` | string | 否 | 贴图质量：`standard`（默认）、`detailed` |
| `geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面） |
| `pbr` | boolean | 否 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图 |
| `texture` | boolean | 否 | 是否生成贴图（默认 `true`）；**无贴图模型需同时设 `texture=false` 且 `pbr=false`** |

生成结果字段取决于参数组合：
- `pbr=true` → 返回 `pbr_model_url`（GLB，含 PBR 材质与贴图）；
- `texture=false && pbr=false` → 返回 `base_model_url`（纯几何 GLB）；
- 所有成功任务均返回 `rendered_image_url`（预览图，WebP 格式）。

## 使用方式

采用标准异步两步流程：

1. **创建任务**（POST）  
   URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
   必须携带请求头：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer <API_KEY>`  
   - `X-DashScope-Async: enable`（缺此头将报错 `"current user api does not support synchronous calls"`）  

   示例（文生3D）：
   ```bash
   curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
     -H 'X-DashScope-Async: enable' \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H 'Content-Type: application/json' \
     -d '{
       "model": "Tripo/Tripo-P1.0",
       "input": {"prompt": "一只可爱的猫"},
       "parameters": {"texture_quality": "standard"}
     }'
   ```
   成功响应含 `task_id`（有效期 24 小时），用于下一步查询。

2. **轮询结果**（GET）  
   URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   建议轮询间隔 ≥15 秒；RPS 限制为 20；超时（24h）后状态为 `UNKNOWN`。  
   详细状态流转见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“步骤2：根据任务ID查询结果”章节。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 不可用；业务空间 ID 和 API Key 必须同地域配对。详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) “适用范围”部分。
- **输入互斥性**：`prompt` / `image` / `images` 三者不可共存，同时传入将直接报错 `InvalidParameter`。
- **图像要求**：单图/多图均要求公网可访问 URL（HTTP/HTTPS），禁止内网地址或临时签名过期链接；多图中各图宽高比不要求一致，但建议统一构图逻辑。
- **结果时效性**：`pbr_model_url`、`base_model_url`、`rendered_image_url` 等下载链接有效期均为 **2 小时**，需及时保存。
- **错误处理**：所有错误码及含义请查阅 [错误码](../../raw/model-api-reference/preparations/error-code.md)，常见错误包括 `InvalidApiKey`、`InvalidParameter`、`ResourceNotReady` 等。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


