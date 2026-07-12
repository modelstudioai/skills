# 3d generation

百炼平台基于 Tripo 模型提供 3D 资产生成能力，支持文生 3D、单图生 3D 与多图生 3D 三种输入方式，产出带贴图的 PBR 材质 GLB 模型或无贴图基础模型。由于生成耗时较长，API 采用[异步调用](../concepts/async-invocation.md)，整体流程为「创建任务 → 轮询获取结果」。详细接口与参数见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 适用范围

- 仅适用于**华北2（北京）**地域，且必须使用该地域的 [API Key](../concepts/api-key.md)。
- 需先在百炼控制台模型市场搜索「Tripo」并开通服务、完成授权，再配置好 [API Key](../concepts/api-key.md) 环境变量。具体开通与配置步骤见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 调用流程

API 仅支持[异步调用](../concepts/async-invocation.md)，包含两个步骤：

1. **创建任务**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`
2. **轮询查询结果**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

创建任务时必须携带 `X-DashScope-Async: enable` 请求头，否则会报错 `current user api does not support synchronous calls`。成功创建后返回 `task_id`，有效期 24 小时，**请勿重复创建任务**，轮询获取即可。

轮询建议间隔约 15 秒，任务状态流转为 `PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED` / `FAILED`。查询接口默认 RPS 为 20，如需更高频查询或事件通知建议配置异步任务回调。

## 支持的模型

| 模型名 | 定位 | 输出面数 | 对应官方 API 版本 |
| --- | --- | --- | --- |
| `Tripo/Tripo-H3.1` | 高精度生成 | 最高 200 万面 | `v3.1-20260211` |
| `Tripo/Tripo-P1.0` | 专业生成，速度更快 | 最高 2 万面 | `P1-20260311` |

## 输入方式

`input` 中 `prompt`、`image`、`images` 三者**互斥**，只能选其一，同时传多个将报错。

- **文生 3D**：`prompt` 必填，支持中英文等多语言，每个字符计 1 个字符，最大 1024 字符。
- **单图生 3D**：`image` 必填，传入单张图像公网 URL。图像格式限 JPEG/PNG，宽高范围 [20, 6000] 像素（建议边长大于 256），文件不超过 20MB，支持 HTTP/HTTPS。
- **多图生 3D**：`images` 必填，数组长度固定为 4，对应视角顺序为**前、左、后、右**；不需要的视角传空对象 `{}`。实际有效图片数为 2~4 张，多张图像的分辨率和宽高比不要求一致。每个对象含 `type`（`jpeg` 或 `png`）与 `file_token`（公网 URL）字段。

## 关键参数（parameters）

| 参数 | 适用模型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `texture_quality` | 全部 | `standard` | 贴图质量，可选 `standard`（标清）/`detailed`（高清） |
| `geometry_quality` | `Tripo/Tripo-H3.1` | `standard` | 几何精度，`standard` 最高 150 万面，`ultra` 最高 200 万面 |
| `pbr` | 全部 | `true` | 是否生成 PBR 材质模型。设为 `true` 时强制启用贴图，返回 `pbr_model_url` |
| `texture` | 全部 | `true` | 是否生成贴图。生成无贴图模型需**同时**将 `texture` 和 `pbr` 设为 `false`，返回 `base_model_url` |

## 响应与产物

成功响应的 `output.results` 仅在 `task_status` 为 `SUCCEEDED` 时返回，包含以下字段：

- `pbr_model_url`：PBR 材质模型（GLB）下载 URL，当 `pbr` 为 `true`（默认）时返回。
- `base_model_url`：无贴图基础模型（GLB）下载 URL，当 `texture` 与 `pbr` 均为 `false` 时返回。
- `rendered_image_url`：3D 模型预览渲染图（1 张）URL。

> **注意**：以上下载链接有效期均为 **2 小时**，请及时下载。

`usage` 字段记录任务类型（`text-to-3d` / `image-to-3d` / `multi-image-to-3d`）、生成数量 `count`、贴图质量与几何精度，仅对成功结果计数。任务状态 `task_status` 的完整枚举为 `PENDING` / `RUNNING` / `SUCCEEDED` / `FAILED` / `CANCELED` / `UNKNOWN`，其中 `UNKNOWN` 表示任务不存在或超过 24 小时有效期。更多响应字段说明见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 限制与注意事项

- 仅限北京地域 [API Key](../concepts/api-key.md) 调用，地域不匹配将无法使用。
- `task_id` 查询有效期 24 小时，超时返回 `UNKNOWN` 且无法再查询。
- 查询接口默认 RPS 限制为 20，建议通过异步任务回调获取更高频通知。
- 产物下载链接有效期仅 2 小时。
- 调用失败时响应中会返回 `code` 与 `message`，可参照百炼错误码文档排查。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)

















