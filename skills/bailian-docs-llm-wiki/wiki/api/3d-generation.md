# 3d generation

百炼平台提供基于 Tripo 模型的 3D 模型生成能力，支持文本、单张图像及多张图像（前/左/后/右四视角）作为输入源，异步返回 GLB 格式的 3D 模型及预览图。该能力仅在华北2（北京）地域可用，需使用对应地域的 API Key 调用 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D（`input.prompt`）：支持中英文，最大 1024 字符；
  - 单图生3D（`input.image`）：JPEG/PNG，分辨率 [20, 6000] 像素，≤20MB；
  - 多图生3D（`input.images`）：固定长度为 4 的数组，顺序为前/左/后/右；允许空对象 `{}` 占位，有效图数须为 2~4 张；各图限制同单图。

> **注意**：文档中明确要求“`prompt`、`image`、`images` 三者互斥”，但部分示例代码未显式排除其他字段（如多图请求体中未清空 `prompt`）。实际调用时必须严格遵循互斥规则，否则将返回 `InvalidParameter` 错误 —— 详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“请求体”说明。

## 关键参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `X-DashScope-Async` | string | 必填 | 必须设为 `"enable"`，同步调用不被支持；缺失将报错 `current user api does not support synchronous calls`。 |
| `model` | string | 必填 | 仅支持 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0`。 |
| `input.prompt` / `input.image` / `input.images` | string / object / array | 条件必填 | 三者严格互斥，不可共存。 |
| `parameters.texture_quality` | string | 可选 | `"standard"`（默认）或 `"detailed"`。 |
| `parameters.geometry_quality` | string | 可选 | 仅 `Tripo-H3.1` 支持；`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面）。 |
| `parameters.pbr` | boolean | 可选 | 默认 `true`；设为 `true` 时强制启用贴图，并返回 `pbr_model_url`。 |
| `parameters.texture` | boolean | 可选 | 默认 `true`；若需无贴图模型，**必须同时设置 `texture: false` 和 `pbr: false`**，否则行为未定义。 |

## 使用方式

采用标准异步两步流程：

1. **创建任务**：`POST /api/v1/services/aigc/video-generation/3d-generation`（北京地域专属 URL），获取 `task_id`；
2. **轮询结果**：`GET /api/v1/tasks/{task_id}`，建议间隔 ≥15 秒，`task_id` 有效期为 24 小时。

完整调用链路与各模式示例（文生、单图、多图、无贴图）请参考原始文档中的 cURL 示例 —— [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，控制台开通、API Key 获取、Endpoint 均需匹配该地域；跨地域调用将失败。
- **认证要求**：必须配置北京地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，且通过 `Authorization: Bearer sk-xxx` 传入请求头。
- **任务管理**：
  - `task_id` 24 小时后失效，查询返回 `UNKNOWN`；
  - 查询接口 RPS 默认为 20，高频轮询建议改用[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)；
  - 不支持重复提交相同任务，应复用 `task_id` 轮询。
- **资源限制**：
  - 图像 URL 需公网可访问，HTTPS/HTTP 均可；
  - 返回的 `pbr_model_url` 和 `base_model_url` 有效期仅 2 小时，需及时下载；
  - 多图输入中，各图宽高比不要求一致，但建议保持相近以提升重建质量。

> **注意**：文档中“适用范围”章节强调“本文档仅适用于华北2（北京）地域”，但未说明是否支持其他地域未来扩展。当前所有接口路径、错误码、地域绑定逻辑均与北京强耦合，开发者不应假设其在其他地域可用 —— 此结论依据 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 全文一致性得出。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


