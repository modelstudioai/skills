# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单图及多图三种输入方式生成 GLB 格式 3D 模型。该能力采用异步任务模式，适用于华北2（北京）地域，需配合有效的 API Key 使用。详细服务开通与配置流程请参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **生成模式**（三者互斥）：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大长度 1024 字符；
  - 单图生3D（`input.image`）：接受 JPEG/PNG 格式公网 URL，分辨率 20–6000px，文件 ≤20MB；
  - 多图生3D（`input.images`）：固定 4 元素数组，顺序为前/左/后/右；允许空对象占位，有效图数为 2–4 张。

> **注意**：多图输入中各图像宽高比不要求一致，但建议保持相近视角一致性以提升重建质量；该约束在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中明确说明，与其他未标注多图兼容性的文档存在隐含差异。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `X-DashScope-Async` | string | 是 | 必须设为 `"enable"`，同步调用不被支持；缺失将报错 `current user api does not support synchronous calls` |
| `model` | string | 是 | 仅支持 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | 条件必填 | 三者互斥，不可共存 |
| `parameters.texture_quality` | string | 否 | 可选 `"standard"`（默认）或 `"detailed"` |
| `parameters.geometry_quality` | string | 否 | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 否 | 默认 `true`；设为 `true` 时自动启用贴图并返回 `pbr_model_url` |
| `parameters.texture` | boolean | 否 | 默认 `true`；如需无贴图模型，**必须同时设 `texture: false` 且 `pbr: false`**，否则行为未定义 |

## 使用方式

1. **开通与认证**：  
   - 在[华北2（北京）地域控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索并开通 Tripo 服务；  
   - 配置地域匹配的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，并设置为环境变量 `DASHSCOPE_API_KEY`（参考 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。

2. **异步任务流程**（两步）：  
   - **步骤1：创建任务**  
     向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 提交请求，获取 `task_id`（有效期 24 小时）。  
   - **步骤2：轮询结果**  
     使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态；建议间隔 ≥15 秒轮询，直至 `task_status === "SUCCEEDED"`。成功响应中 `results` 字段包含 `pbr_model_url`（PBR 模型）、`base_model_url`（无贴图模型）或 `rendered_image_url`（预览图），所有 URL 有效期均为 2 小时。

完整调用示例（文生3D）详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强绑定**：仅支持华北2（北京）地域，其他地域 URL 不可用；
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超时后查询返回 `task_status: "UNKNOWN"`；
- **RPS 限制**：任务查询接口默认限流 20 QPS，高频轮询场景建议配置[异步回调](../../raw/model-api-reference/more-about-models/async-task-api.md)；
- **输入校验**：`prompt`、`image`、`images` 三者严格互斥，同时传入将直接报错；
- **无贴图模型生成**：必须显式设置 `"texture": false, "pbr": false`，仅设其一无效；
- **错误排查**：所有错误码及含义统一归档于 [错误码](../../raw/model-api-reference/preparations/error-code.md)，创建/查询失败时优先查阅该文档。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


