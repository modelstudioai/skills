# Tripo-自动绑骨

Tripo自动绑骨可自动为3D模型添加骨骼绑定，支持多种骨骼类型。建议先进行可绑骨检查，验证模型兼容性。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **准备前序任务**：先创建可产出3D模型的任务（如[Tripo-文生/图生3D模型](raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)），待任务执行成功后，将其`task_id`传入`original_model_task_id`；也可不创建前序任务，通过`model_url`直接传入模型文件的公网URL。建议先通过[Tripo-可绑骨检查](raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)确认模型可绑骨并获取骨骼类型。

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

模型名称。固定值：`Tripo/Tripo-AutoRig`。

**input** `object` **（必选）**

输入信息。

属性

**original\_model\_task\_id** `string` （条件必填）

前序任务ID。传入前序任务创建时返回的`task_id`，系统会自动使用该任务输出的3D模型。与`model_url`二选一。

前序任务可为任意产出3D模型文件（如GLB）的任务，例如[Tripo-文生/图生3D模型](raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。需满足以下条件：

-   前序任务必须已执行成功。
-   发起本次调用的账号须与前序任务的账号一致，引用其他账号创建的任务将返回400错误。

**model\_url** `string` （条件必填）

模型文件的公网URL。与`original_model_task_id`二选一。

模型限制：

-   支持格式：GLB、FBX、OBJ、STL。
-   文件大小：不超过150MB。

**parameters** `object` （可选）

绑骨参数。传入未列出的字段将返回400错误。

属性

**out\_format** `string` （可选）

输出格式。默认值为`glb`。可选值：

-   `glb`：二进制glTF格式，适用于Web。
-   `fbx`：FBX格式，适用于DCC工具和游戏引擎。

传入其他值返回400错误。

**spec** `string` （可选）

绑骨规范，即骨骼的命名规范。仅在`rig_type`为`biped`时生效。默认值为`tripo`。可选值：

-   `tripo`：Tripo原生骨骼命名。
-   `mixamo`：兼容Mixamo的骨骼命名。使用此规范绑骨的模型不能用于[Tripo-动画重定向](raw/_short/tripo-animation-retarget-api-reference-63dd4c8b61a39d8b.md)。

**rig\_type** `string` （可选）

骨骼类型。默认值为`biped`。建议先调用[Tripo-可绑骨检查](raw/model-api-reference/3d-generation/tripo-api-reference/tripo-animation-api-reference/tripo-rig-check-api-reference.md)，使用其返回的`rig_type`。可选值：

-   `biped`：双足人形。
-   `quadruped`：四足动物。
-   `hexapod`：六足生物。
-   `octopod`：八足生物。
-   `avian`：鸟类或有翼生物。
-   `serpentine`：蛇形生物。
-   `aquatic`：鱼类或水生生物。

**model\_version** `string` （可选）

绑骨算法版本。默认值为`v1.0-20240301`。可选值：

-   `v1.0-20240301`：仅适用于（且推荐用于）双足人形绑骨，支持90多种预设动画。
-   `v2.5-20260210`：适用于非人形的动物绑骨，包括四足、六足、八足、蛇形、水生和鸟类。

#### 传入前序任务ID

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-AutoRig",
    "input": {
        "original_model_task_id": "ca51d54a-ffba-4ecc-8e42-xxxxxx"
    },
    "parameters": {
        "rig_type": "biped"
    }
}'
```

#### 传入模型URL

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-AutoRig",
    "input": {
        "model_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260507/ffaaxt/tripo-text-to-3d-result.glb"
    },
    "parameters": {
        "out_format": "fbx",
        "rig_type": "quadruped"
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

-   **轮询建议**：自动绑骨可能需要数分钟，建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
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
-   当状态变为 SUCCEEDED 时，响应中将包含绑骨后的3D模型URL。
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

绑骨结果列表。仅在 task\_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。

属性

**rendered\_image\_url** `string`

3D模型预览渲染图的URL。

**model\_url** `string`

绑骨后3D模型的URL。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计。仅在任务成功时返回，任务失败时不返回。

属性

**3d\_task\_type** `string`

任务类型。自动绑骨固定为`auto-rig`。

**credits\_consumed** `integer`

本次任务消耗的积分。自动绑骨按次计费，无额外计费参数。

#### 任务执行成功

```
{
    "request_id": "6b8db7b5-c8bb-95ec-86fc-xxxxxx",
    "output": {
        "task_id": "0a0d7d32-3e9c-4888-8057-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-10-19 12:22:09.204",
        "scheduled_time": "2026-10-19 12:22:09.255",
        "end_time": "2026-10-19 12:23:46.598",
        "results": [
            {
                "rendered_image_url": "https://openapi.cdn.tripo3d.com/xxxx/legacy_mesh.webp?auth_key=xxxx",
                "model_url": "https://openapi.cdn.tripo3d.com/xxxx/tripo_rigging_xxxx.glb?auth_key=xxxx"
            }
        ]
    },
    "usage": {
        "3d_task_type": "auto-rig",
        "credits_consumed": 25
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
