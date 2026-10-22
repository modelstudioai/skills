# 3d generation

3D generation 是百炼平台提供的异步式 3D 模型生成服务，支持文本、单张图像或多张图像作为输入，输出 GLB 格式的 3D 模型（含 PBR 材质或无贴图基础模型）及预览图。该能力由 Tripo 模型提供，当前仅在华北2（北京）地域可用，且需使用对应地域的 API Key。完整调用流程包含任务创建与轮询查询两阶段，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，最高支持 200 万面，支持 `geometry_quality: "ultra"`；对应 Tripo 官方 API 版本 `v3.1-20260211`。
  - `Tripo/Tripo-P1.0`：专业级快速生成，最高 2 万面，适合对速度敏感的场景；对应 Tripo 官方 API 版本 `P1-20260311`。
- **输入模式（三者互斥）**：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大 1024 字符；
  - 单图生3D（`input.image`）：接受 JPEG/PNG 公网 URL，分辨率 20–6000px，≤20MB；
  - 多图生3D（`input.images`）：严格按 `[前, 左, 后, 右]` 顺序传入 2–4 张图（空对象 `{}` 表示跳过某视角），各图独立满足单图限制。

> **注意**：文档中明确要求多图必须为 4 个元素数组，但实际允许传入空对象占位；若传入非 4 元素数组（如长度为 3 或 5），将返回 `InvalidParameter` 错误。该行为与部分旧版 SDK 示例不一致，请以 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中“多图生3D模型（传入2张图）”示例为准。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `X-DashScope-Async` | string | 必填 | **必须设为 `"enable"`**，同步调用不被支持，缺失将报错 `current user api does not support synchronous calls` |
| `model` | string | 必填 | 仅支持 `Tripo/Tripo-H3.1` 或 `Tripo/Tripo-P1.0` |
| `input.prompt` / `input.image` / `input.images` | string / object / array | 条件必填 | 三者互斥，不可共存 |
| `parameters.texture_quality` | string | 可选 | `"standard"`（默认）或 `"detailed"` |
| `parameters.geometry_quality` | string | 可选 | 仅 `Tripo-H3.1` 支持：`"standard"`（≤150 万面）或 `"ultra"`（≤200 万面） |
| `parameters.pbr` | boolean | 可选 | 默认 `true`；设为 `true` 时自动启用贴图，返回 `pbr_model_url` |
| `parameters.texture` | boolean | 可选 | 默认 `true`；**如需无贴图模型，必须同时设 `texture: false` 且 `pbr: false`**，返回 `base_model_url` |

所有 URL 响应字段（如 `pbr_model_url`, `base_model_url`, `rendered_image_url`）有效期均为 **2 小时**，需及时下载。更多参数细节请参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 使用方式

1. **前置准备**：
   - 在[百炼控制台（华北2）](https://bailian.console.aliyun.com/cn-beijing/model/market)开通 Tripo 服务；
   - 配置对应地域的 API Key 到环境变量（如 `DASHSCOPE_API_KEY`），参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

2. **异步调用流程**：
   - **步骤1：创建任务**  
     向 `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` 发送请求，获取 `task_id`（有效期 24 小时）。
   - **步骤2：轮询结果**  
     使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，建议间隔 ≥15 秒；状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`。

3. **结果解析**：
   - 成功（`SUCCEEDED`）时，`output.results[]` 包含 `pbr_model_url`（默认）或 `base_model_url`（当 `texture=false && pbr=false`）及 `rendered_image_url`；
   - 失败（`FAILED`）时，检查 `output.code` 和 `output.message`，对照 [错误码](../../raw/model-api-reference/preparations/error-code.md) 排查。

## 限制和注意事项

- **地域强约束**：仅支持华北2（北京）地域，其他地域 URL 调用将失败；业务空间 ID（`{WorkspaceId}`）须与地域匹配。
- **任务生命周期**：
  - `task_id` 有效期为 **24 小时**，超时后查询返回 `task_status: "UNKNOWN"`；
  - 下载 URL（`pbr_model_url` 等）有效期为 **2 小时**，不可续期。
- **调用频率**：
  - 查询接口默认 RPS 限流为 20；高频轮询建议改用[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)；
  - 创建任务请勿重复提交相同请求，应复用 `task_id` 轮询。
- **输入校验**：
  - `prompt`、`image`、`images` 三者严格互斥，同时存在任两个即报 `InvalidParameter`；
  - `images` 数组长度必须为 4，缺失视角需用 `{}` 占位，不可省略或缩短数组。
- **模型能力边界**：Tripo 当前不支持视频/点云/3D 扫描数据输入，仅支持上述三种模态；复杂拓扑或细长结构（如极细杆件、薄壁）可能生成失真，建议通过 `geometry_quality: "ultra"` 提升精度。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


