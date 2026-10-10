# 3d generation

百炼平台提供基于 Tripo 模型的 3D 内容生成能力，支持文本、单图及多图三种输入方式生成高质量 3D 模型（GLB 格式），适用于游戏资产、电商展示、AR/VR 等开发场景。该能力为异步任务模式，需通过任务 ID 轮询获取结果，且**仅在华北2（北京）地域可用**。详细实现细节请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合原型验证；对应 Tripo 官方 API 版本 `P1-20260311`。
- **生成模式（互斥）**：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大 1024 字符。
  - 单图生3D（`input.image`）：接受 JPEG/PNG 公网 URL，分辨率 20–6000px，单图 ≤20MB。
  - 多图生3D（`input.images`）：严格按 `[前, 左, 后, 右]` 顺序传入 2–4 张图（空对象 `{}` 表示跳过某视角）。

> **注意**：文档中明确要求所有调用必须使用华北2（北京）地域的 API Key 和 Endpoint，其他地域暂不支持。若在非北京地域调用失败，请确认 [API Key 配置](../../raw/model-api-reference/preparations/get-api-key.md) 是否指向正确地域。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `X-DashScope-Async` | string | 是 | **必须设为 `"enable"`**，同步调用将报错 `"current user api does not support synchronous calls"`。 |
| `model` | string | 是 | 仅支持 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0`。 |
| `input.prompt` / `input.image` / `input.images` | string / object / array | 条件必填 | 三者互斥，不可共存。多图数组长度固定为 4，无效项填 `{}`。 |
| `parameters.texture_quality` | string | 否 | `standard`（默认）或 `detailed`；影响贴图分辨率。 |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持；`standard`（≤150 万面）或 `ultra`（≤200 万面）。 |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `true` 时强制启用贴图，并返回 `pbr_model_url`。 |
| `parameters.texture` | boolean | 否 | 默认 `true`；如需无贴图模型，**必须同时设 `texture=false` 且 `pbr=false`**，返回 `base_model_url`。 |

## 使用方式

1. **开通与认证**  
   - 在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索 “Tripo” 并开通服务。  
   - 获取并配置北京地域的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐通过环境变量注入（如 `DASHSCOPE_API_KEY`）。

2. **异步任务流程（两步）**  
   - **步骤1：创建任务**  
     `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`  
     返回 `task_id`（有效期 24 小时），**禁止重复提交相同请求**。  
   - **步骤2：轮询结果**  
     `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     建议间隔 ≥15 秒轮询；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`；超时返回 `UNKNOWN`。  

3. **结果解析**  
   - 成功（`SUCCEEDED`）时，`output.results[]` 包含：  
     - `pbr_model_url`（PBR 材质 GLB，当 `pbr=true`）  
     - `base_model_url`（无贴图 GLB，当 `texture=false && pbr=false`）  
     - `rendered_image_url`（预览图，WebP 格式）  
     - 所有下载链接有效期 **2 小时**，需及时保存。  
   - 失败时检查 `code` 和 `message`，详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，Endpoint、API Key、业务空间均需匹配该地域。跨地域调用将失败。
- **任务生命周期**：`task_id` 有效期 24 小时；结果下载链接有效期 2 小时；超时后无法重试，需重新提交任务。
- **输入校验**：`prompt`、`image`、`images` 三者严格互斥；多图 `images` 数组长度必须为 4；图像 URL 必须可公开访问且协议为 HTTP/HTTPS。
- **资源限制**：查询接口默认 RPS 为 20；高频轮询建议改用 [异步回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **模型能力边界**：`Tripo/Tripo-P1.0` 不支持 `geometry_quality=ultra`；`geometry_quality` 仅对 `Tripo/Tripo-H3.1` 生效。  
- > **注意**：原始文档中 `multi-image-to-3d` 的图片顺序定义为 `[前, 左, 后, 右]`，但部分旧版 SDK 示例曾误标为 `[前, 右, 后, 左]`，请以本文档及 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的顺序为准。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


