# 3d generation

百炼平台通过集成 Tripo 模型，提供 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种输入方式。API 采用异步调用模式，通过"创建任务 -> 轮询获取"两步完成生成流程，适用于需要将文本描述或图片转化为 3D 模型（GLB 格式）的场景。

## 支持的模型

当前提供两个可选模型，适用于不同精度和速度需求：

| 模型名称 | 特点 | 最高面数 | 对应 Tripo 官方版本 |
|---|---|---|---|
| `Tripo/Tripo-H3.1` | 高精度 3D 模型生成 | 200 万面 | v3.1-20260211 |
| `Tripo/Tripo-P1.0` | 专业 3D 模型生成，速度更快 | 2 万面 | P1-20260311 |

详细的模型参数和调用方式请参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 三种输入方式

三种输入方式互斥，仅能选择其中一种，同时传入多个将报错：

- **文生 3D**：通过 `input.prompt` 传入文本描述，支持中英文，最大 1024 个字符。
- **单图生 3D**：通过 `input.image` 传入单张图片 URL（JPEG/PNG，分辨率 20~6000 像素，不超过 20MB）。
- **多图生 3D**：通过 `input.images` 传入 4 个元素的数组，对应前、左、后、右四个视角，不需要的视角传空对象 `{}`，有效图片数量为 2~4 张。

## 调用流程

由于 3D 生成耗时较长，API 仅支持异步调用，必须在请求头设置 `X-DashScope-Async: enable`。

### 步骤 1：创建任务

**请求地址**（北京地域）：

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation
```

**必需请求头**：

| Header | 说明 |
|---|---|
| `Content-Type` | 必须为 `application/json` |
| `Authorization` | `Bearer $DASHSCOPE_API_KEY` |
| `X-DashScope-Async` | 必须为 `enable`，否则报错 |

**请求体示例**（文生 3D）：

```json
{
    "model": "Tripo/Tripo-P1.0",
    "input": {
        "prompt": "一只可爱的猫"
    },
    "parameters": {
        "texture_quality": "standard"
    }
}
```

创建成功后返回 `task_id`（有效期 24 小时），请勿重复创建任务。

### 步骤 2：轮询查询结果

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔约 15 秒。任务状态流转为：`PENDING` -> `RUNNING` -> `SUCCEEDED` / `FAILED`。如需更高频查询或事件通知，可配置异步任务回调。

成功响应中 `results` 包含模型下载 URL（链接有效期 2 小时），根据参数配置返回不同字段：

| 返回字段 | 条件 |
|---|---|
| `pbr_model_url` | `pbr` 为 `true`（默认） |
| `base_model_url` | `texture` 和 `pbr` 均为 `false` |
| `rendered_image_url` | 始终返回，3D 模型预览渲染图 |

## 关键参数

`parameters` 对象中可配置以下选项：

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `texture_quality` | string | `standard` | 贴图质量：`standard`（标清）或 `detailed`（高清） |
| `geometry_quality` | string | `standard` | 几何精度（仅 `Tripo-H3.1`）：`standard`（最高 150 万面）或 `ultra`（最高 200 万面） |
| `pbr` | boolean | `true` | 是否生成 PBR 材质模型；设为 `true` 时强制启用贴图 |
| `texture` | boolean | `true` | 是否生成贴图；生成无贴图模型需同时设 `texture` 和 `pbr` 为 `false` |

更多参数细节参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 使用限制和注意事项

- **仅限北京地域**：必须使用"中国内地（北京）"地域的 API Key，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 中的适用范围说明。
- **开通服务**：需在百炼控制台搜索"Tripo"并开通模型。
- **task_id 有效期**：24 小时，超时后查询返回 `UNKNOWN` 状态。
- **下载链接有效期**：生成的模型和渲染图 URL 有效期为 2 小时，请及时下载。
- **查询 RPS 限制**：默认为 20，更高频需求建议配置异步任务回调。
- **输出格式**：3D 模型统一为 GLB 格式。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)


