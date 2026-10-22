# 3d generation

3D generation 是百炼平台提供的异步式 3D 模型生成服务，支持文本、单图及多图三种输入方式，底层由 Tripo 模型提供能力。该服务仅在华北2（北京）地域可用，需配合专用 API Key 调用。所有任务均采用“创建任务 → 轮询查询”两阶段流程，不支持同步调用。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合高频轻量场景；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式**（三者互斥）：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大 1024 字符；
  - 单图生3D（`input.image`）：接受 JPEG/PNG 格式公网 URL，分辨率 [20, 6000] 像素，≤20MB；
  - 多图生3D（`input.images`）：严格按 **前、左、后、右** 顺序传入 2~4 张图（空对象 `{}` 表示跳过某视角），每张图约束同单图。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 明确要求必须使用 `X-DashScope-Async: enable` 请求头，否则报错 “current user api does not [support](../guides/support.md) synchronous calls”。该限制在其他 3D 相关文档中未被一致强调，以本文档为准。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `texture_quality` | string | 否 | 贴图质量，可选 `standard`（默认）、`detailed`；影响 `pbr_model_url` 输出效果 |
| `geometry_quality` | string | 否 | 仅对 `Tripo/Tripo-H3.1` 有效，可选 `standard`（≤150 万面）、`ultra`（≤200 万面） |
| `pbr` | boolean | 否 | 是否生成 PBR 材质模型（默认 `true`）；设为 `true` 时自动启用贴图 |
| `texture` | boolean | 否 | 是否生成贴图（默认 `true`）；**若需无贴图模型，必须同时设置 `texture: false` 和 `pbr: false`** |

生成结果通过 `results` 数组返回，包含 `pbr_model_url`（GLB，含材质贴图）、`base_model_url`（GLB，无贴图）或 `rendered_image_url`（预览图），所有 URL 有效期均为 **2 小时**，需及时下载。

## 使用方式

1. **前置准备**：  
   - 在[华北2（北京）地域控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务；  
   - 配置对应地域的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并确保环境变量或请求头中正确传递；  
   - 替换请求 URL 中的 `{WorkspaceId}` 为实际业务空间 ID（参见 [地域与域名迁移说明](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。

2. **创建任务（POST）**：  
   调用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`，必须携带：  
   - `Content-Type: application/json`  
   - `Authorization: Bearer <your_api_key>`  
   - `X-DashScope-Async: enable`  

3. **轮询查询（GET）**：  
   使用上一步返回的 `task_id`，调用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`；  
   - 建议轮询间隔 ≥15 秒；  
   - `task_id` 有效期为 **24 小时**，超时后状态返回 `UNKNOWN`；  
   - 更高频率查询或事件驱动场景，请参考 [异步任务回调配置](../../raw/model-api-reference/more-about-models/async-task-api.md)。

完整调用示例（文生3D）见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的 curl 示例。

## 限制和注意事项

- **地域强绑定**：服务仅支持华北2（北京）地域，跨地域调用将失败；  
- **异步强制性**：所有请求必须启用 `X-DashScope-Async: enable`，同步调用不被支持；  
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将触发 `InvalidParameter` 错误；  
- **多图顺序刚性**：`images` 数组长度固定为 4，索引 0~3 分别代表前、左、后、右视角，缺失视角须显式填 `{}`；  
- **资源时效性**：`task_id` 有效期 24 小时，结果 URL（`pbr_model_url` 等）有效期 2 小时；  
- **错误排查**：所有错误码定义与解释请查阅 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)；  
- **新手指引**：首次调用建议参考 [Postman 快速入门](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

> **注意**：[Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确指出“请勿重复创建任务”，而部分旧版用户指南未强调此点。重复提交相同请求可能导致计费异常或任务队列阻塞，务必依赖轮询而非重试创建。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


