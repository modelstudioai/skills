# 3d generation

百炼平台通过集成 Tripo 系列模型，提供 3D 模型生成能力，支持**文生3D**、**单图生3D**和**多图生3D**三种输入方式，输出 GLB 格式的带贴图或无贴图三维模型。API 采用[异步调用](../concepts/async-invocation.md)模式，整体流程分为"创建任务 → 轮询查询"两步。详细接口规范参见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

> **注意**：本接口**仅适用于华北2（北京）地域**，必须使用北京地域的 [API Key](../concepts/api-key.md)，其他地域的 Key 将无法调用成功。

## 支持的模型

| 模型名称 | 说明 | 最高面数 |
| --- | --- | --- |
| `Tripo/Tripo-H3.1` | 高精度3D模型，对应 Tripo 官方 API `v3.1-20260211` | 200 万面（ultra 模式） |
| `Tripo/Tripo-P1.0` | 专业3D模型，速度更快，对应 Tripo 官方 API `P1-20260311` | 2 万面 |

## 前置配置

1. 在[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)搜索"Tripo"并开通服务。
2. 获取**北京地域** [API Key](../concepts/api-key.md) 并配置到环境变量 `DASHSCOPE_API_KEY`。

## 调用方式

所有请求均为异步 HTTP，需在请求头加 `X-DashScope-Async: enable`，否则报错 `"current user api does not support synchronous calls"`。

### 步骤一：创建任务

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation
```

请将 `{WorkspaceId}` 替换为真实的[业务空间](../concepts/workspace.md) ID。

#### input 参数（三选一）

| 字段 | 类型 | 使用场景 | 限制 |
| --- | --- | --- | --- |
| `prompt` | string | 文生3D | 最大 1024 字符，支持中英文 |
| `image` | string（URL） | 单图生3D | JPEG/PNG，宽高 [20, 6000]px，≤ 20MB |
| `images` | array[object] | 多图生3D | 固定长度 4，对应前/左/后/右，有效图片 2～4 张 |

`prompt`、`image`、`images` 三者互斥，同时传入多个将报错。

多图模式下，`images` 数组长度固定为 4，不需要的视角传入空对象 `{}` 即可，顺序为**前、左、后、右**。

#### parameters 参数

| 字段 | 默认值 | 说明 | 适用模型 |
| --- | --- | --- | --- |
| `texture_quality` | `standard` | 贴图质量：`standard`（标清）/ `detailed`（高清） | 全部 |
| `geometry_quality` | `standard` | 几何精度：`standard`（最高150万面）/ `ultra`（最高200万面） | 仅 `Tripo/Tripo-H3.1` |
| `pbr` | `true` | 是否生成 PBR 材质，设为 `true` 时强制启用贴图 | 全部 |
| `texture` | `true` | 是否生成贴图；无贴图时需同时设 `texture=false` 和 `pbr=false` | 全部 |

#### 创建成功响应示例

```json
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

保存 `task_id`，有效期 **24 小时**，切勿重复创建任务。

### 步骤二：查询任务结果

```
GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}
```

建议每隔 **15 秒**轮询一次，查询接口默认 RPS 为 20。任务状态流转：

```
PENDING → RUNNING → SUCCEEDED / FAILED
```

| 状态 | 说明 |
| --- | --- |
| `PENDING` | 排队中 |
| `RUNNING` | 处理中 |
| `SUCCEEDED` | 成功，返回模型 URL |
| `FAILED` | 失败，返回错误码和信息 |
| `CANCELED` | 已取消 |
| `UNKNOWN` | 不存在或超过 24 小时有效期 |

#### 成功响应中的 results 字段

| 字段 | 说明 | 返回条件 |
| --- | --- | --- |
| `pbr_model_url` | PBR 材质模型（GLB），有效期 2 小时 | `pbr=true`（默认） |
| `base_model_url` | 无贴图基础模型（GLB），有效期 2 小时 | `texture=false` 且 `pbr=false` |
| `rendered_image_url` | 模型预览渲染图（1张），有效期 2 小时 | 始终返回 |
| `orig_prompt` | 原始 [prompt](../guides/prompt.md) 输入 | 文生3D 模式 |

> **注意**：模型文件和渲染图 URL **有效期仅 2 小时**，请及时下载，过期后需重新生成任务。

## 示例代码

以下示例均来自 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)，仅展示关键差异。

**文生3D（有贴图）**

```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-P1.0",
    "input": { "prompt": "一只可爱的猫" },
    "parameters": { "texture_quality": "standard" }
}'
```

**无贴图生成**（需同时设 `texture` 和 `pbr` 为 `false`）

```bash
# 参数中同时设置 texture 和 pbr 为 false
-d '{
    "model": "Tripo/Tripo-P1.0",
    "input": { "prompt": "一只可爱的猫" },
    "parameters": { "texture": false, "pbr": false }
}'
```

## 限制与注意事项

- **地域限制**：仅支持华北2（北京）地域，[API Key](../concepts/api-key.md) 也必须是北京地域的，详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
- **异步强制**：HTTP 调用必须携带 `X-DashScope-Async: enable`，不支持同步调用。
- **task_id 有效期**：24 小时，超时后状态返回 `UNKNOWN`，无法补查结果。
- **input 互斥**：`prompt`、`image`、`images` 三者只能选其一，混用会报错。
- **多图视角顺序**：`images` 数组固定长度为 4，顺序为前、左、后、右，缺省视角传 `{}`。
- **模型 URL 时效**：生成结果 URL（模型文件、渲染图）有效期仅 2 小时，请及时下载。
- **错误排查**：调用失败可参考[错误码文档](https://help.aliyun.com/zh/model-studio/error-code)。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)







