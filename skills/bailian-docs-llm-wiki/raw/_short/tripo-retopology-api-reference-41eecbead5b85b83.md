# Tripo-重拓扑

Tripo重拓扑可减少3D模型的面数，支持v2.0智能低模重拓扑（默认，保留干净的拓扑结构）和v1.0基础减面，可输出三角面或四边面网格。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **准备前序任务**：先创建可产出3D模型的任务（如[Tripo-文生/图生3D模型](raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)），待任务执行成功后，将其`task_id`传入`original_model_task_id`；也可不创建前序任务，通过`model_url`直接传入模型文件的公网URL。

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

模型名称。固定值：`Tripo/Tripo-Retopology`。

**input** `object` **（必选）**

输入信息。

属性

**original\_model\_task\_id** `string` （条件必填）

前序任务ID。传入前序任务创建时返回的`task_id`，系统会自动使用该任务输出的3D模型。与`model_url`二选一。

前序任务可为任意产出3D模型文件（如GLB）的任务，例如[Tripo-文生/图生3D模型](raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。需满足以下条件：

-   前序任务必须已执行成功。
-   发起本次调用的账号须与前序任务的账号一致，引用其他账号创建的任务将返回400错误。
-   使用`part_names`时，须传入[Tripo-网格分割](raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)任务的`task_id`。

**model\_url** `string` （条件必填）

模型文件的公网URL。与`original_model_task_id`二选一。

模型限制：

-   支持格式：GLB、GLTF、FBX、OBJ、STL。
-   文件大小：不超过150MB。

**parameters** `object` （可选）

重拓扑参数。

属性

**model\_version** `string` （可选）

重拓扑算法版本，按不同积分计费。可选值：

-   `v2.0`：默认值，智能低模重拓扑，保留干净的拓扑结构。
-   `v1.0`：基础减面。

**face\_limit** `integer` （条件必填）

目标面数。**`model_version`为`v1.0`时必填**；`v2.0`下不传时由模型自适应决定。取值范围：

-   `v2.0`：三角面500~20,000，四边面500~10,000。
-   `v1.0`：三角面500~2,000,000，四边面500~150,000。

**quad** `boolean` （可选）

是否输出四边面网格（而非三角面）。默认值为`false`。

输出格式由此参数决定：未开启时输出GLB格式，开启后输出FBX格式（GLB无法保留四边面）。

**bake** `boolean` （可选）

是否将贴图烘焙到减面后的模型上。默认值为`true`。`v1.0`不支持此参数。

**part\_names** `array[string]` （可选）

需要减面的部件名称列表。

-   部件名取自前序网格分割任务结果模型（GLB）中的部件节点名，形如`tripo_part_0`、`tripo_part_1`；任务结果字段不单独返回部件名，且编号可能不连续，请读取 GLB 的节点名获取。
-   仅当前序任务为[Tripo-网格分割](raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)任务（或[Tripo-智能分割](raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)返回的`seg_task_id`）时有效。
-   不传则处理全部部件。
-   传入不存在的名称不报错、照常计费。
-   `v1.0`不支持此参数。

#### v1.0（三角面）

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-Retopology",
    "input": {
        "original_model_task_id": "6e7916d1-235f-4754-83c3-xxxxxx"
    },
    "parameters": {
        "model_version": "v1.0",
        "face_limit": 5000,
        "quad": false
    }
}'
```

#### v2.0（四边面）

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-Retopology",
    "input": {
        "model_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/ffaaxt/tripo-text-to-3d-result.glb"
    },
    "parameters": {
        "model_version": "v2.0",
        "face_limit": 5000,
        "quad": true
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

-   **轮询建议**：重拓扑可能需要数分钟，建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
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
-   当状态变为 SUCCEEDED 时，响应中将包含重拓扑后的3D模型URL。
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

重拓扑结果列表。仅在 task\_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。

属性

**model\_url** `string`

重拓扑后3D模型的URL。未开启`quad`时为GLB格式，开启`quad`时为FBX格式。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计。仅在任务成功时返回，任务失败时不返回。

属性

**3d\_task\_type** `string`

任务类型。重拓扑固定为`retopology`。

**credits\_consumed** `integer`

本次任务消耗的积分，等于`retopology_version`。

**retopology\_version** `integer`

重拓扑消耗的积分，按算法版本（请求参数`model_version`）计算。

#### 任务执行成功

```
{
    "request_id": "362fa5f5-2c6d-975f-b7f3-xxxxxx",
    "output": {
        "task_id": "cc716927-1f22-44d9-af00-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-10-19 11:35:48.919",
        "scheduled_time": "2026-10-19 11:35:48.966",
        "end_time": "2026-10-19 11:36:29.499",
        "results": [
            {
                "model_url": "https://openapi.cdn.tripo3d.com/xxxx/tripo_convert_xxxx.fbx?auth_key=xxxx"
            }
        ]
    },
    "usage": {
        "3d_task_type": "retopology",
        "retopology_version": 10,
        "credits_consumed": 10
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
