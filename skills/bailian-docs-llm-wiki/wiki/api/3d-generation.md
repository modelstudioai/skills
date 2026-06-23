# 3d generation

百炼平台通过集成 Tripo 模型，提供 3D 模型生成能力，支持文生 3D、单图生 3D 和多图生 3D 三种模式。API 采用异步调用方式，流程为"创建任务 -> 轮询获取结果"。详细接口说明参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型

| 模型名称 | 特点 | 最高面数 |
|---------|------|---------|
| `Tripo/Tripo-H3.1` | 高精度 3D 模型生成 | 200 万面 |
| `Tripo/Tripo-P1.0` | 专业 3D 模型生成，速度更快 | 2 万面 |

## 输入方式

三种输入方式互斥，仅能选择其中一种，同时传入多个将报错：

- **文生 3D**（`prompt`）：通过文本描述生成 3D 模型，支持中英文，最大 1024 字符。
- **单图生 3D**（`image`）：传入单张图片 URL 生成 3D 模型。图片格式支持 JPEG/PNG，分辨率范围 [20, 6000] 像素，文件不超过 20MB。
- **多图生 3D**（`images`）：传入 2~4 张图片生成 3D 模型。数组长度固定为 4，顺序为前、左、后、右，不需要的视角传入空对象 `{}`。

## 关键参数

根据 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md) 文档，`parameters` 对象支持以下可选参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| `texture_quality` | string | 贴图质量：`standard`（默认，标清）或 `detailed`（高清） |
| `geometry_quality` | string | 几何精度（仅 `Tripo-H3.1`）：`standard`（默认，最高 150 万面）或 `ultra`（最高 200 万面） |
| `pbr` | boolean | 是否生成 PBR 材质模型，默认 `true`。启用时强制开启贴图，结果包含 `pbr_model_url` |
| `texture` | boolean | 是否生成贴图，默认 `true`。生成无贴图模型需同时将 `texture` 和 `pbr` 设为 `false` |

## 调用流程

### 步骤 1：创建任务

发送 POST 请求到北京地域端点：

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation
```

必须设置以下请求头：

- `Content-Type: application/json`
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `X-DashScope-Async: enable`（必须，否则报错 "current user api does not [support](../guides/support.md) synchronous calls"）

成功响应返回 `task_id`，有效期 24 小时，请勿重复创建任务。

### 步骤 2：轮询查询结果

使用 GET 请求查询任务状态：

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

任务状态流转：`PENDING` -> `RUNNING` -> `SUCCEEDED` / `FAILED`。建议轮询间隔 15 秒，查询接口默认 RPS 为 20。

任务成功后，根据参数配置返回不同的结果字段：

- `pbr_model_url`：PBR 材质模型（GLB 格式），`pbr=true` 时返回
- `base_model_url`：无贴图基础模型（GLB 格式），`texture` 和 `pbr` 均为 `false` 时返回
- `rendered_image_url`：3D 模型预览渲染图

> **注意**：下载链接有效期仅 2 小时，请及时下载。

## 使用限制

- 仅适用于"中国内地（北京）"地域，必须使用该地域的 API Key。
- `task_id` 有效期 24 小时，超时后无法查询结果，状态返回 `UNKNOWN`。
- 使用前需在百炼控制台搜索"Tripo"并开通服务。

## 示例

以文生 3D 为例，如需了解单图、多图等完整示例，请参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

```bash
# 创建任务
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

# 查询结果
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)




