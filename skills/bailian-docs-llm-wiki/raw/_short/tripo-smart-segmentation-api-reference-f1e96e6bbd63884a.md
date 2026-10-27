# Tripo-智能分割

Tripo智能分割提供端到端的分割流程，支持以图像或GLB格式的3D模型为输入，输出分割后的3D模型。与仅对已有模型进行分割的网格分割不同，智能分割包含自动建模。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## HTTP调用

API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
-   新手指引请参见[Postman](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。

#### 请求参数

##### 请求头（Headers）

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async**`string`**（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`enable`。

**重要**缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `string` **（必选）**

模型名称。固定值：`Tripo/Tripo-SmartSegmentation`。

**input** `object` **（必选）**

输入信息。

属性

**seg\_type** `string` **（必选）**

输入类型。可选值：

-   `image`：以图像为输入，需同时传入`image`。支持PNG、JPEG、WebP格式。
-   `model`：以3D模型为输入，需同时传入`model_url`和`parameters.transform`。仅支持GLB格式。

**image** `string` （条件必填）

输入图像的公网URL，支持PNG、JPEG、WebP格式，图片不超过20MB，不限制分辨率。**仅在`seg_type`为`image`时必填。**

**model\_url** `string` （条件必填）

模型文件的公网URL，仅支持GLB格式，非GLB文件返回400错误。文件不超过150MB。**仅在`seg_type`为`model`时必填。**

**parameters** `object` （可选）

分割参数。

属性

**granularity** `string` （可选）

分割粒度。可选值：

-   `coarse`：粗粒度，输出2~3个大类，如人物、衣物。
-   `medium`：默认值，输出4~8个物体或部件，如人物、上衣、裤子、鞋、包。
-   `fine`：细粒度，输出9~52个细部件，如脸、头发、左臂、右臂。

**hint** `string` （可选）

提示词，用于辅助识别需要分割的部件。不限制长度和语言，建议简短明确，例如“把杯身和杯盖分开”。

**transform** `array[number]` （条件必填）

4×4列主序变换矩阵，必须由16个浮点数组成，元素不限取值范围。**仅在`seg_type`为`model`时必填。**

不传或元素个数不是16时返回400错误。`seg_type`为`image`时忽略该参数。

单位矩阵示例：`[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]`。

#### 以图像为输入

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-SmartSegmentation",
    "input": {
        "seg_type": "image",
        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/liafix/tripo-images-1.png"
    },
    "parameters": {
        "hint": "wheel"
    }
}'
```

#### 以模型为输入

需同时传入`parameters.transform`。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-SmartSegmentation",
    "input": {
        "seg_type": "model",
        "model_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/ffaaxt/tripo-text-to-3d-result.glb"
    },
    "parameters": {
        "transform": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    }
}'
```

#### 响应参数

**output** `object`

任务输出信息。

属性

**task\_id** `string`

任务ID。查询有效期24小时。

**task\_status** `string`

任务状态。

枚举值

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   CANCELED：任务已取消
-   UNKNOWN：任务不存在或状态未知

**request\_id**`string`

请求唯一标识。可用于请求明细溯源和问题排查。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

#### 成功响应

请保存 task\_id，用于查询任务状态与结果。

```
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

#### 异常响应

创建任务失败，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：智能分割可能需要数分钟，建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
-   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)。
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

#### 请求参数

##### 请求头（Headers）

**Authorization**`string`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### URL路径参数（Path parameters）

**task\_id** `string`**（必选）**

任务ID。

#### 查询任务结果

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### 响应参数

**output**`object`

任务输出信息。

属性

**task\_id** `string`

任务ID。查询有效期24小时。

**task\_status** `string`

任务状态。

枚举值

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   CANCELED：任务已取消
-   UNKNOWN：任务不存在或状态未知

**轮询过程中的状态流转：**

-   PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
-   初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。
-   当状态变为 SUCCEEDED 时，响应中将包含分割后的3D模型URL。
-   若状态为 FAILED，请检查错误信息并重试。
-   若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。
-   若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task\_id 不存在或超过 24 小时有效期后出现。

**submit\_time** `string`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `string`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `string`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**results**`array`

分割结果列表。仅在 task\_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。

属性

**seg\_model\_url** `string`

分割后3D模型的URL。

**mask\_url** `string`

2D分割mask图的URL。

**prompt** `string`

识别出的部件名称，多个部件以英文逗号分隔。

**model\_task\_id** `string`

内部3D模型子任务的ID。`seg_type`为`image`时为图生3D子任务，为`model`时为模型导入子任务。可作为同一账号下[Tripo-贴图](raw/_short/tripo-texture-api-reference-4bba6c052f4d945b.md)、[Tripo-重拓扑](raw/_short/tripo-retopology-api-reference-41eecbead5b85b83.md)、[Tripo-自动绑骨](raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-auto-rig-api-reference.md)等模型的`original_model_task_id`。

**seg\_task\_id** `string`

内部网格分割子任务的ID。可作为同一账号下[Tripo-网格补全](raw/_short/tripo-mesh-completion-api-reference-2b47e6cb5ff8ed91.md)的`original_model_task_id`，也可在Tripo-贴图、Tripo-重拓扑中配合`part_names`使用。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计。仅在任务成功时返回，任务失败时不返回。

属性

**3d\_task\_type** `string`

任务类型。智能分割固定为`smart-segmentation`。

**credits\_consumed** `integer`

本次任务消耗的积分，等于`seg_type`。

**seg\_type** `integer`

智能分割消耗的积分，按输入类型（图像或模型）计算。

#### 任务执行成功

```
{
    "request_id": "486ab449-fbdc-9cae-a14f-xxxxxx",
    "output": {
        "task_id": "1b690d69-87df-4237-a023-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-10-19 10:02:22.318",
        "scheduled_time": "2026-10-19 10:02:22.368",
        "end_time": "2026-10-19 10:06:27.092",
        "results": [
            {
                "model_task_id": "2bf3a129-220d-461b-b996-xxxxxx",
                "mask_url": "https://openapi.cdn.tripo3d.com/xxxx/mask.png?auth_key=xxxx",
                "seg_task_id": "9a060088-0280-4c62-ac58-xxxxxx",
                "seg_model_url": "https://openapi.cdn.tripo3d.com/xxxx/segment/tripo_mesh_seg_xxxx.glb?auth_key=xxxx",
                "prompt": "face, hair, ears, armor, cloak, quiver, arrows"
            }
        ]
    },
    "usage": {
        "3d_task_type": "smart-segmentation",
        "credits_consumed": 85,
        "seg_type": 85
    }
}
```

#### 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "request_id": "e5d70b02-ebd3-98ce-9fe8-xxxxxx",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-xxxxxx",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "The parameter is invalid xxxxxx"
    }
}
```

#### 任务查询过期

task\_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。

```
{
    "request_id": "a4de7c32-7057-9f82-8581-xxxxxx",
    "output": {
        "task_id": "502a00b1-19d9-4839-a82f-xxxxxx",
        "task_status": "UNKNOWN"
    }
}
```

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)进行解决。
