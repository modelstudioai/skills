# 爱诗-视频超清API参考

爱诗-视频超清模型支持将输入视频进行超分辨率处理，固定输出4K（3840×2160）分辨率视频。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## 服务开通

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
2.  在弹窗内确认开通及授权。

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

**说明**本文的视频超清示例适用于**华北2（北京）地域**。

## HTTP调用

由于视频超清任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

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

模型名称。固定值：`pixverse/pixverse-upscale`。

**input** `object` **（必选）**

输入的基本信息，包括待超分的视频。

属性

**media** `array` **（必选）**

媒体资源列表。必须包含 1 个视频元素。

元素属性

**type** `string` **（必选）**

媒体素材类型。固定值为：

-   `video_url`：视频URL。

**url** `string` **（必选）**

输入视频的URL地址，必须为公网可访问的URL。

-   支持 HTTP 或 HTTPS 协议。
-   示例值：[](https://xxx/xxx.mp4)[https://xxx/xxx.mp4](https://xxx/xxx.mp4)。

视频限制：

-   格式：MP4、MOV、WebM。
-   分辨率：不支持 4K 及以上分辨率。
-   文件大小：不超过 100MB。
-   时长：不超过 30 秒。

**parameters** `object` （可选）

视频生成参数。如设置是否添加水印、随机种子等。

属性

**watermark** `boolean` （可选）

是否添加水印标识，水印位于视频右下角，文案固定为"AI生成"。

-   `false`：默认值，不添加水印。
-   `true`：添加水印。

**seed**`integer`（可选）

随机数种子，取值范围为`[0, 2147483647]`。

未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。

请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。

#### 视频超清

传入视频文件，输出超分辨率视频。

```
# 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "pixverse/pixverse-upscale",
    "input": {
        "media": [
            {
                "type": "video_url",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/wqefue/mix_input_video.mp4"
            }
        ]
    },
    "parameters": {
        "seed": 12345,
        "watermark": true
    }
}'
```

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
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

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

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
-   当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。
-   若状态为 FAILED，请检查错误信息并重试。
-   若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。
-   若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task\_id 不存在或超过 24 小时有效期后出现。

**submit\_time** `string`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `string`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `string`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**video\_url**`string`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储，请及时下载。

**orig\_prompt** `string`

原始输入的prompt，对应请求参数`prompt`。

**code**`string`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**message**`string`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](raw/model-api-reference/preparations/error-code.md)。

**usage** `object`

输出信息统计。只对成功的结果计数。

属性

**duration** `integer`

计费时长（秒）。为用户上传视频时长向上取整。

**size** `string`

输出视频的分辨率。

**fps** `integer`

输出视频的帧率。

**SR** `string`

输出视频的分辨率档位。

**video\_count** `integer`

视频数量，固定为 1。

#### 任务执行成功

```
{
    "request_id": "19171ea5-9efb-4d35-93a1-xxxxxx",
    "output": {
        "task_id": "7ed706b7-a9a9-4319-820c-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-07-14 10:34:41.630",
        "scheduled_time": "2026-07-14 10:34:41.655",
        "end_time": "2026-07-14 10:35:12.725",
        "video_url": "https://media.pixverseai.cn/xxxx.mp4"
    },
    "usage": {
        "duration": 6,
        "size": "3840*2156",
        "fps": 24,
        "video_count": 1,
        "SR": "4K"
    }
}
```

#### 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

```
{
    "request_id": "e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-a0c6a421c010",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "Invalid field type or value. Please verify your input data."
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

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
