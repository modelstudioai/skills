# Tripo-格式转换

Tripo格式转换可将3D模型转换为GLTF、USDZ、FBX、OBJ、STL、3MF等格式，并支持网格处理、贴图烘焙和导出设置。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 适用范围

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“**Tripo**”，找到Tripo模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
3.  **准备前序任务**：先创建可产出3D模型的任务（如[Tripo-文生/图生3D模型](raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)），待任务执行成功后，将其`task_id`传入`original_model_task_id`。

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

模型名称。固定值：`Tripo/Tripo-ConvertFormat`。

**input** `object` **（必选）**

输入信息。

属性

**original\_model\_task\_id** `string` **（必选）**

前序任务ID。传入前序任务创建时返回的`task_id`，系统会自动使用该任务输出的3D模型。

前序任务可为任意产出3D模型文件（如GLB）的任务，例如[Tripo-文生/图生3D模型](raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)。需满足以下条件：

-   前序任务必须已执行成功。
-   发起本次调用的账号须与前序任务的账号一致，引用其他账号创建的任务将返回400错误。
-   使用`part_names`时，须传入[Tripo-网格分割](raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)任务的`task_id`。

模型限制：

-   支持格式：GLB、GLTF、FBX、OBJ、STL。
-   文件大小：不超过150MB。

**format** `string` **（必选）**

目标导出格式。可选值：

-   `GLTF`：适用于Web查看器、WebGL引擎（如Three.js、Babylon.js）。
-   `USDZ`：适用于Apple AR Quick Look、RealityKit。
-   `FBX`：适用于Unreal、Unity及Maya、Blender等DCC工具。
-   `OBJ`：传统交换格式，不支持动画。
-   `STL`：适用于3D打印，仅包含几何体。
-   `3MF`：适用于3D打印。

兼容写法：`format`也可传入`glb`，效果与传入`GLTF`相同。

**parameters** `object` （可选）

格式转换参数。

属性

**quad** `boolean` （可选）

是否输出四边面网格（而非三角面）。默认值为`false`。

开启后，输出格式强制为FBX；未设置`face_limit`时，默认面数为10,000。

设置为`true`时按高级转换计费。

**force\_symmetry** `boolean` （可选）

是否强制模型对称。默认值为`false`。仅当`quad`为`true`时生效。

**face\_limit** `integer` （可选）

输出模型的最大面数。建议不低于100。

默认值为`null`，即不限制面数，保持原模型面数；开启`quad`时默认面数为10,000。

传入非`null`的值时按高级转换计费。

**flatten\_bottom** `boolean` （可选）

是否将模型底部压平。默认值为`false`。设置为`true`时按高级转换计费。

**flatten\_bottom\_threshold** `number` （可选）

底部压平的深度阈值。默认值为`0.01`。仅当`flatten_bottom`为`true`时生效。取值不为`0.01`时按高级转换计费。

**texture\_size** `integer` （可选）

漫反射贴图的尺寸，单位为像素。建议取值512~8192，不要求为2的幂。

默认值为`4096`。取值不为`4096`时按高级转换计费。

**texture\_format** `string` （可选）

贴图格式。取值不为`JPEG`时按高级转换计费。可选值：

-   `JPEG`：默认值，文件体积最小。
-   `PNG`：无损格式，支持透明度。
-   `WEBP`：现代Web格式。
-   `BMP`、`DPX`、`HDR`、`OPEN_EXR`、`TARGA`、`TIFF`：适用于专业用途。

**pivot\_to\_center\_bottom** `boolean` （可选）

是否将模型轴心点移至底部中心。默认值为`false`。设置为`true`时按高级转换计费。

**scale\_factor** `number` （可选）

导出模型的缩放系数。取值须大于0。

默认值为`1.0`。传入0或负数不会报错，但无法保证转换结果。取值不为`1.0`时按高级转换计费。

**bake** `boolean` （可选）

是否将高级材质烘焙为基础贴图。默认值为`true`。

**pack\_uv** `boolean` （可选）

是否将所有UV合并到统一布局。默认值为`false`。

**with\_animation** `boolean` （可选）

是否包含骨骼和动画数据。默认值为`true`。

**animate\_in\_place** `boolean` （可选）

是否导出原地动画（无根骨骼位移）。默认值为`false`。

**part\_names** `array[string]` （可选）

要导出的部件名称列表。

-   部件名取自前序网格分割任务结果模型（GLB）中的部件节点名，形如`tripo_part_0`、`tripo_part_1`；任务结果字段不单独返回部件名，且编号可能不连续，请读取 GLB 的节点名获取。
-   仅当前序任务为[Tripo-网格分割](raw/_short/tripo-segmentation-api-reference-cec9c68cea8a90f7.md)任务（或[Tripo-智能分割](raw/_short/tripo-smart-segmentation-api-reference-f1e96e6bbd63884a.md)返回的`seg_task_id`）时有效。
-   不传则处理全部部件。
-   传入不存在的名称不报错、照常计费。

**export\_vertex\_colors** `boolean` （可选）

是否导出顶点色。默认值为`false`。仅对`OBJ`和`GLTF`格式生效。

**export\_orientation** `string` （可选）

导出模型的朝向（前向轴）。可选值：

-   `+x`：默认值，X轴正方向朝前。
-   `-x`：X轴负方向朝前。
-   `+y`：Y轴正方向朝前。
-   `-y`：Y轴负方向朝前。

**fbx\_preset** `string` （可选）

FBX格式的兼容预设。可选值：

-   `blender`：默认值，针对Blender导入优化。
-   `3dsmax`：针对3ds Max导入优化。
-   `mixamo`：兼容Mixamo绑骨。
-   `bake_scale`：导出FBX时将缩放变换烘焙进几何体，而不保留在节点transform上。

#### 基础转换

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-ConvertFormat",
    "input": {
        "original_model_task_id": "ca51d54a-ffba-4ecc-8e42-xxxxxx",
        "format": "GLTF"
    }
}'
```

#### 高级转换（四边面）

设置`quad`、`face_limit`等参数后按高级转换计费。开启`quad`后输出格式强制为FBX。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "Tripo/Tripo-ConvertFormat",
    "input": {
        "original_model_task_id": "ca51d54a-ffba-4ecc-8e42-xxxxxx",
        "format": "FBX"
    },
    "parameters": {
        "quad": true,
        "face_limit": 5000,
        "fbx_preset": "blender"
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

-   **轮询建议**：格式转换通常需要10~30秒，建议采用**轮询**机制获取结果：首次在提交任务10秒后查询，之后每15~30秒查询一次。
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
-   当状态变为 SUCCEEDED 时，响应中将包含转换后的3D模型URL。
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

转换结果列表。仅在 task\_status 为 SUCCEEDED 时返回。各URL均为带签名的临时链接，有效期2小时，请及时下载。

属性

**model\_url** `string`

转换后3D模型的URL。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计。仅在任务成功时返回，任务失败时不返回。

属性

**3d\_task\_type** `string`

任务类型。格式转换固定为`convert-3d-format`。

**credits\_consumed** `integer`

本次任务消耗的积分，等于`convert_level`。

**convert\_level** `integer`

格式转换消耗的积分，按转换复杂度（基础转换或高级转换）计算。判定条件见[计费与参数说明](#tcf801h2bill)。

#### 任务执行成功

```
{
    "request_id": "cc451f5a-fdd7-9d9e-a3a9-xxxxxx",
    "output": {
        "task_id": "2ea046a6-d7bd-4c26-af70-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-10-21 12:59:21.869",
        "scheduled_time": "2026-10-21 12:59:21.908",
        "end_time": "2026-10-21 12:59:30.384",
        "results": [
            {
                "model_url": "https://openapi.cdn.tripo3d.com/xxxx/tripo_convert_xxxx.glb?auth_key=xxxx"
            }
        ]
    },
    "usage": {
        "3d_task_type": "convert-3d-format",
        "credits_consumed": 5,
        "convert_level": 5
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

## 计费与参数说明

-   **计费档位**：格式转换分为基础转换和高级转换两档计费，高级转换消耗更多积分。满足以下任一条件即按高级转换计费，均不满足时按基础转换计费。实际消耗的积分见查询结果中的`usage.convert_level`。
    -   `quad`为`true`
    -   `face_limit`为非`null`的值
    -   `flatten_bottom`为`true`
    -   `flatten_bottom_threshold`不为`0.01`
    -   `texture_size`不为`4096`
    -   `texture_format`不为`JPEG`
    -   `pivot_to_center_bottom`为`true`
    -   `scale_factor`不为`1.0`
-   **不支持的参数**：`smart_low_poly`（智能低模）是[Tripo-文生/图生3D模型](raw/_short/tripo-3d-generation-api-reference-a4c298b3ddebaa99.md)接口的参数，格式转换接口不支持。如果请求中带了该参数（例如沿用生成任务的参数），会被忽略，不报错也不计费。
-   **未列出的参数**：除`smart_low_poly`外，传入本文未列出的参数将返回400错误（`InvalidParameter`）。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)进行解决。
