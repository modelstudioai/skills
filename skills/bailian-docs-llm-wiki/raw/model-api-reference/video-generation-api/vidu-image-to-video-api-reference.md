# Vidu-图生视频-基于首帧API参考

Vidu-图生视频模型根据**输入图像**和**文本提示词**，生成一段流畅的视频。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **服务开通**

请前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 **Vidu**，找到 **Vidu** 模型卡片，单击**立即开通**；在弹窗内确认开通及授权。

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
    
-   **配置 API Key**：选择地域并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    

## HTTP调用

图生视频任务耗时较长（通常为1-5分钟），API采用异步调用的方式。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### **步骤1：创建任务获取任务ID**

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 图生视频

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "vidu/viduq3-pro_img2video",
    "input": {
        "media": [
            {
                "type": "image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
            }
        ],
        "prompt": "镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。"
    },
    "parameters": {
        "duration": 5,
        "resolution": "720P",
        "watermark": true
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称。可选值为：

-   `vidu/viduq3-pro_img2video`
    
-   `vidu/viduq3-turbo_img2video`
    
-   `vidu/viduq2-pro-fast_img2video`
    
-   `vidu/viduq2-pro_img2video`
    
-   `vidu/viduq2-turbo_img2video`
    

**input** `_object_` **（必选）**

输入的基本信息，如提示词、媒体素材等。

**属性**

**prompt** `_string_` （可选）

文本提示词。用来描述生成视频中期望包含的元素和视觉特点。

支持中英文，每个汉字/字母占一个字符，字符长度不能超过 5000 个字符，超过部分会自动截断。

提示词编写请参见[Vidu视频生成Prompt指南](https://help.aliyun.com/zh/model-studio/vidu-video-generation-prompt-guide)。

**media** `_array_` **（必选）**

媒体素材列表，用于指定图生视频所需的图像。

数组的每个元素为一个媒体对象，包含 `type` 与 `url` 字段。

**属性**

**type** `_string_` **（必选）**

媒体素材类型。固定值为：

-   `image`：图像URL。
    

素材限制：图像素材有且只有**1张**。

**url** `_string_` **（必选）**

图像文件的URL地址，必须为公网可访问的URL。

-   支持 HTTP 或 HTTPS 协议。
    
-   示例值：https://xxx/xxx.jpg。
    

图像限制：

-   格式：JPG、JPEG、PNG、WEBP。
    
-   宽高比：1:4～4:1。
    
-   文件大小：不超过50MB。
    

**parameters** `_object_` （可选）

视频处理参数，如设置视频分辨率、设置视频时长等。

**属性**

**resolution** `_string_` （可选）

**重要**

resolution直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#e5d1761f12xq3)。

指定生成的视频分辨率档位。

模型根据选择的分辨率档位，自动缩放至相近总像素，视频宽高比将尽量接近输入图像的宽高比。

-   vidu/viduq3-pro\_img2video：可选值：540P、720P、1080P。默认值为`720P`。
    
-   vidu/viduq3-turbo\_img2video：可选值：540P、720P、1080P。默认值为`720P`。
    
-   vidu/viduq2-pro-fast\_img2video：可选值：720P、1080P。默认值为`720P`。
    
-   vidu/viduq2-pro\_img2video：可选值：540P、720P、1080P。默认值为`720P`。
    
-   vidu/viduq2-turbo\_img2video：可选值：540P、720P、1080P。默认值为`720P`。
    

**duration** `_integer_` （可选）

**重要**

duration直接影响费用，按秒计费，时间越长费用越高，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#e5d1761f12xq3)。

生成视频的时长，单位为秒。

-   vidu/viduq3-pro\_img2video：取值为\[1, 16\]之间的整数，默认值为5。
    
-   vidu/viduq3-turbo\_img2video：取值为\[1, 16\]之间的整数，默认值为5。
    
-   vidu/viduq2-pro-fast\_img2video：取值为\[1, 10\]之间的整数，默认值为5。
    
-   vidu/viduq2-pro\_img2video：取值为\[1, 10\]之间的整数，默认值为5。
    
-   vidu/viduq2-turbo\_img2video：取值为\[1, 10\]之间的整数，默认值为5。
    

**audio** `_boolean_` （可选）

**支持模型**：vidu/viduq3-pro\_img2video、vidu/viduq3-turbo\_img2video。

是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。

-   `false`：默认值，输出无声视频。
    
-   `true`：输出有声视频。
    

**watermark** `_boolean_` （可选）

是否添加水印标识，水印位于视频右下角，文案固定为“内容由AI生成”。

-   `false`：默认值，不添加水印。
    
-   `true`：添加水印。
    

**seed** `_integer_` （可选）

随机数种子，取值范围为`[0, 2147483647]`。

未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。

请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。

#### 响应参数

### 成功响应

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

### 异常响应

创建任务失败，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

**output** `_object_`

任务输出信息。

属性

**task\_id** `_string_`

任务ID。查询有效期24小时。

**task\_status** `_string_`

任务状态。

**枚举值**

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务已取消
    
-   UNKNOWN：任务不存在或状态未知
    

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

### **步骤2：根据任务ID查询结果**

**北京地域**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
    
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

#### 请求参数

## 查询任务结果

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

## 任务执行成功

```
{
    "request_id": "3606f9f4-b833-44ec-8385-xxxxxx",
    "output": {
        "task_id": "2846881f-0496-4288-947f-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-27 14:25:32.057",
        "scheduled_time": "2026-03-27 14:25:32.084",
        "end_time": "2026-03-27 14:28:29.600",
        "orig_prompt": "镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。",
        "video_url": "https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxxx"
    },
    "usage": {
        "duration": 5,
        "size": "990*932",
        "output_video_duration": 5,
        "fps": 24,
        "video_count": 1,
        "audio": false,
        "SR": "720"
    }
}
```

## 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-a0c6a421c010",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "The size is not match xxxxxx"
    }
}
```

## 任务查询过期

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

**output** `_object_`

任务输出信息。

**属性**

**task\_id** `_string_`

任务ID。查询有效期24小时。

**task\_status** `_string_`

任务状态。

**枚举值**

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务已取消
    
-   UNKNOWN：任务不存在或状态未知
    

**轮询过程中的状态流转：**

-   PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。
    
-   当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。
    
-   若状态为 FAILED，请检查错误信息并重试。
    
-   若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。
    
-   若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task\_id 不存在或超过 24 小时有效期后出现。
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**video\_url** `_string_`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

视频格式为MP4（H.264 编码）。视频链接**有效期24小时**，请及时下载。

**orig\_prompt** `_string_`

原始输入的prompt，对应请求参数`prompt`。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计，只对成功的结果计数。

**属性**

**duration** `_integer_`

总的视频计费时长（秒）。

**output\_video\_duration** `_integer_`

输出视频的时长（秒）。

**size** `_string_`

输出视频的分辨率。

**fps** `_integer_`

输出视频的帧率。固定为24。

**SR** `_string_`

输出视频的分辨率档位。

**audio** `_boolean_`

输出视频是否为有声视频。

**video\_count** `_integer_`

输出视频的数量。固定为1。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
