# 3d generation

百炼平台提供基于 Tripo 模型的 3D 内容生成能力，支持文本、单图及多图三种输入方式生成 GLB 格式的 3D 模型。该能力为[异步任务](../concepts/asynchronous-task.md)型 API，需通过“创建任务 → 轮询查询”两阶段完成，适用于华北2（北京）地域。所有调用均需配置有效的 API Key 并显式声明 `X-DashScope-Async: enable` 请求头。

## 支持的模型/功能

- **模型列表**：
  - `Tripo/Tripo-H3.1`：高精度生成，输出模型最高 200 万面，支持 `geometry_quality=ultra`；详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
  - `Tripo/Tripo-P1.0`：专业级快速生成，输出模型最高 2 万面，适合对延迟敏感的场景。
- **输入模式（三者互斥）**：
  - 文生3D（`input.prompt`）：支持中英文提示词，最大长度 1024 字符；
  - 单图生3D（`input.image`）：接受 JPEG/PNG 公网 URL，分辨率 20–6000px，文件 ≤20MB；
  - 多图生3D（`input.images`）：固定 4 元素数组，顺序为前/左/后/右，允许空对象占位，有效图数为 2–4 张。

> **注意**：多图输入中各图像宽高比不要求一致，但建议保持相近视角与光照一致性，否则可能影响几何重建质量 —— 此约束未在 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的“图像限制”小节明确说明，仅隐含于示例和最佳实践描述中。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `texture_quality` | string | 否 | 贴图质量：`standard`（默认）、`detailed`；影响 `pbr_model_url` 输出效果 |
| `geometry_quality` | string | 否 | 仅 `Tripo/Tripo-H3.1` 支持：`standard`（≤150 万面）、`ultra`（≤200 万面） |
| `pbr` | boolean | 否 | 默认 `true`；设为 `true` 时强制启用贴图，并返回 `pbr_model_url` |
| `texture` | boolean | 否 | 默认 `true`；如需无贴图模型，**必须同时设 `texture=false` 且 `pbr=false`**，返回 `base_model_url` |

所有下载 URL（如 `pbr_model_url`、`base_model_url`、`rendered_image_url`）有效期均为 **2 小时**，需及时持久化。

## 使用方式

1. **开通与准备**：  
   在[华北2（北京）地域控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)搜索并开通 Tripo 模型服务；配置对应地域的 [API Key](https://bailian.console.aliyun.com/model/settings/api-key)，并确保环境变量 `DASHSCOPE_API_KEY` 已设置 —— 参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的“适用范围”章节。

2. **异步调用流程**：  
   - **步骤1（创建任务）**：`POST /api/v1/services/aigc/video-generation/3d-generation`，必须携带 `X-DashScope-Async: enable`，返回 `task_id`（24 小时有效）；  
   - **步骤2（轮询结果）**：`GET /api/v1/tasks/{task_id}`，建议间隔 ≥15 秒；状态流转为 `PENDING` → `RUNNING` → `SUCCEEDED`/`FAILED`。

3. **典型请求体示例（文生3D）**：
   ```json
   {
     "model": "Tripo/Tripo-P1.0",
     "input": { "prompt": "一只可爱的猫" },
     "parameters": { "texture_quality": "detailed" }
   }
   ```

## 限制和注意事项

- **地域强绑定**：仅支持华北2（北京）地域，URL 域名为 `cn-beijing.maas.aliyuncs.com`，其他地域不可用；
- **异步强制性**：同步调用被明确禁止，缺失 `X-DashScope-Async: enable` 将返回错误 `current user api does not support synchronous calls`；
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超时后查询返回 `task_status=UNKNOWN`，无法恢复；
- **RPS 限制**：任务查询接口默认限流 20 RPS，高频轮询需改用[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)机制；
- **输入互斥性**：`prompt`、`image`、`images` 三者不可共存，同时传入将导致 `InvalidParameter` 错误；
- **无贴图模型生成**：必须同时设置 `texture=false` 和 `pbr=false`，单独设置任一参数无效。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


