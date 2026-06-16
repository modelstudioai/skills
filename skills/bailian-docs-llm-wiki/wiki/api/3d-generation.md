# 3d generation

百炼平台通过 Tripo 模型提供 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种模式。API 采用异步调用方式，通过"创建任务 → 轮询获取结果"的流程完成 3D 模型的生成与下载。

## 支持的模型

根据 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 文档，当前可选模型如下：

| 模型名称 | 说明 | 输出面数 | 对应 Tripo 官方版本 |
|---------|------|---------|-------------------|
| `Tripo/Tripo-H3.1` | 高精度 3D 模型生成 | 最高 200 万面 | v3.1-20260211 |
| `Tripo/Tripo-P1.0` | 专业 3D 模型生成，速度更快 | 最高 2 万面 | P1-20260311 |

## 功能模式

- **文生 3D 模型**：通过 `prompt` 文本描述生成 3D 模型
- **单图生 3D 模型**：通过 `image` 单张图片 URL 生成 3D 模型
- **多图生 3D 模型**：通过 `images` 数组（固定 4 个元素，对应前、左、后、右视角）生成 3D 模型，有效图片 2~4 张，不需要的视角传空对象 `{}`

三种输入方式互斥，同时传入多个会报错。

## 关键参数

### 输入参数（input）

| 参数 | 类型 | 说明 |
|------|------|------|
| `prompt` | string | 文本提示词，最大 1024 字符，支持中英文 |
| `image` | string | 单张图片 URL（JPEG/PNG，分辨率 20~6000px，≤20MB） |
| `images` | array[object] | 多图对象列表，每个对象含 `type`（jpeg/png）和 `file_token`（URL） |

### 生成参数（parameters）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `texture_quality` | string | `standard` | 贴图质量：`standard`（标清）/ `detailed`（高清） |
| `geometry_quality` | string | `standard` | 几何精度（仅 Tripo-H3.1）：`standard`（最高 150 万面）/ `ultra`（最高 200 万面） |
| `pbr` | boolean | `true` | 是否生成 PBR 材质，设为 true 时强制启用贴图 |
| `texture` | boolean | `true` | 是否生成贴图。无贴图模型需同时设 `texture` 和 `pbr` 为 `false` |

## 使用方式

### 步骤 1：创建任务

**请求地址**（北京地域）：

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation
```

**必需请求头**：

```
X-DashScope-Async: enable
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json
```

> **注意**：缺少 `X-DashScope-Async: enable` 请求头将报错 "current user api does not [support](../guides/support.md) synchronous calls"。

文生 3D 示例：

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-P1.0",
    "input": {
        "prompt": "一只可爱的猫"
    },
    "parameters": {
        "texture_quality": "standard"
    }
}'
```

成功响应将返回 `task_id`，有效期 24 小时。

### 步骤 2：轮询查询结果

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

建议轮询间隔 15 秒。任务状态流转：`PENDING` → `RUNNING` → `SUCCEEDED` / `FAILED`。

成功后返回的 `results` 中包含：

- `pbr_model_url`：PBR 材质模型（GLB 格式），`pbr=true` 时返回
- `base_model_url`：无贴图基础模型（GLB 格式），`texture=false` 且 `pbr=false` 时返回
- `rendered_image_url`：3D 模型预览渲染图

所有下载链接有效期为 **2 小时**。

## 限制和注意事项

如 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 所述，使用时需注意以下限制：

- **地域限制**：仅适用于"中国内地（北京）"地域，必须使用该地域的 API Key
- **开通要求**：需在百炼控制台搜索"Tripo"并开通服务
- **task_id 有效期**：24 小时，超时后返回 `UNKNOWN` 状态
- **查询 RPS 限制**：默认 20，如需更高频建议配置[异步任务](../concepts/async-task.md)回调
- **请勿重复创建任务**：获取 task_id 后轮询即可
- **图片要求**：JPEG/PNG 格式，分辨率 20~6000px，文件 ≤20MB
- **多图模式**：数组固定 4 个元素（前、左、后、右），多图分辨率和宽高比无需一致

关于 `usage` 返回中的 `3d_task_type` 枚举值包括：`text-to-3d`、`image-to-3d`、`multi-image-to-3d`，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 的响应参数说明。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)












