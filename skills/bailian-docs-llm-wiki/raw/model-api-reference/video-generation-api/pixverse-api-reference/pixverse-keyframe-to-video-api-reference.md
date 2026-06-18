# 爱诗-图生视频-基于首尾帧API参考

爱诗-首尾帧生视频模型基于**首帧图像**、**尾帧图像和文本提示词**，生成一段平滑过渡的视频。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **服务开通**

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
    
2.  在弹窗内确认开通及授权。
    

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://help.aliyun.com/zh/model-studio/use-video-generation#f32f686472enw)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
    
-   **配置 API Key**：选择地域并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    

## HTTP调用

由于首尾帧生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### **步骤1：创建任务获取任务ID**

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 首尾帧生视频

支持模型：pixverse/pixverse-c1-kf2v、pixverse/pixverse-v6-kf2v、pixverse/pixverse-v5.6-kf2v。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "pixverse/pixverse-c1-kf2v",
    "input": {
        "media": [
            {
                "type": "first_frame",
                "url": "https://wanx.alicdn.com/material/20250318/first_frame.png"
            },
            {
                "type": "last_frame",
                "url": "https://wanx.alicdn.com/material/20250318/last_frame.png"
            }
        ],
        "prompt": "一只小猫从窗台向下跳跃，轻盈地落在沙发上，然后好奇地环顾四周。"
    },
    "parameters": {
        "resolution": "720P",
        "duration": 5,
        "watermark": true
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称。模型输出规格请参见[模型列表](https://help.aliyun.com/zh/model-studio/use-video-generation#f32f686472enw)。

可选值：

-   pixverse/pixverse-c1-kf2v
    
-   pixverse/pixverse-v6-kf2v
    
-   pixverse/pixverse-v5.6-kf2v
    

**模型选型**

-   针对打斗、法术特效及高速运动等动态场景，推荐选用 **c1**。
    
-   通用场景推荐使用**v6**，**v5.6**建议直接升级至**v6**。
    

**input** `_object_` **（必选）**

输入的基本信息，包含首帧、尾帧图像和提示词。

**属性**

**prompt** `_string_` **（必选）**

文本提示词。用来描述首帧到尾帧之间的变化过程。

支持中英文，每个汉字/字母占一个字符，字符编码为UTF-8，超过部分会自动截断。

-   pixverse/pixverse-c1-kf2v：不超过5000个字符。
    
-   pixverse/pixverse-v6-kf2v：不超过5000个字符。
    
-   pixverse/pixverse-v5.6-kf2v：不超过2048个字符。
    

**media** `_array_` **（必选）**

媒体资源列表，包含首帧和尾帧图像。

数组的每个元素为一个媒体对象，包含 `type` 与 `url` 字段。

**属性**

**type** `_string_` **（必选）**

媒体类型。

-   `first_frame`：首帧图像。
    
-   `last_frame`：尾帧图像。
    

素材限制：

-   首帧图像：有且仅有1张。
    
-   尾帧图像：有且仅有1张。
    

**url** `_string_` **（必选）**

图像的公网可访问URL。

-   支持 HTTP 或 HTTPS 协议。
    
-   示例值：https://xxx/xxx.png。
    

图像限制：

-   格式：JPG、PNG、WEBP。
    
-   分辨率：宽度和高度均不超过10000像素。
    
-   文件大小：不超过20MB。
    

**parameters** `_object_` **（必选）**

视频生成参数。如设置视频分辨率、时长、是否生成音频等。

**属性**

**resolution** `_string_` **（必选）**

**重要**

resolution直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#pxk001a0sec01)。

生成视频的分辨率。

可选值：`360P`、`540P`、`720P`、`1080P`。

**duration** `_integer_` **（必选）**

**重要**

duration直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#pxk001a0sec01)。

生成视频的时长，单位为秒。

-   pixverse/pixverse-c1-kf2v：取值范围为\[1, 15\]之间的整数。
    
-   pixverse/pixverse-v6-kf2v：取值范围为\[1, 15\]之间的整数。
    
-   pixverse/pixverse-v5.6-kf2v：
    
    -   当 resolution 为 360P / 540P / 720P 对应的所有分辨率时：取值为5、8、10。
        
    -   当resolution为1080P对应的所有分辨率时：取值为5、8。
        

**audio** `_boolean_` （可选）

**重要**

audio直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#pxk001a0sec01)。

是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。

-   `false`：默认值，输出无声视频。
    
-   `true`：输出有声视频。
    

**watermark** `_boolean_` （可选）

是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。

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

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

#### **任务执行成功**

```
{
    "request_id": "40799260-689c-4c44-9d7c-xxxxxx",
    "output": {
        "task_id": "408b6c3b-27c9-43dd-b928-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-20 13:47:42.916",
        "scheduled_time": "2026-03-20 13:47:42.949",
        "end_time": "2026-03-20 13:48:41.896",
        "orig_prompt": "一只小猫从窗台向下跳跃，轻盈地落在沙发上，然后好奇地环顾四周。",
        "video_url": "https://media.pixverseai.cn/xxx.mp4"
    },
    "usage": {
        "duration": 5,
        "size": "1280*960",
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
    
-   当状态变为 SUCCEEDED 时，响应中将包含生成的视频url。
    
-   若状态为 FAILED，请检查错误信息并重试。
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**video\_url** `_string_`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储，请及时下载。

**orig\_prompt** `_string_`

原始输入的prompt，对应请求参数`prompt`。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**duration** `_integer_`

生成视频的总视频时长，用于计费。

**size** `_string_`

生成视频的分辨率。

**fps** `_integer_`

生成视频的帧率。

**SR** `_string_`

生成视频的分辨率档位。

**audio** `_boolean_`

生成视频是否为有声视频。

**video\_count** `_integer_`

生成视频的数量。固定为1。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

#### **Q: media数组中首帧和尾帧的顺序是否有要求？**

A: `media`数组中需要包含两个对象，分别设置`type`为`first_frame`（首帧）和`last_frame`（尾帧），顺序不影响结果，系统会根据type字段自动识别。

#### **Q: 首帧和尾帧图像的分辨率是否需要一致？**

A: 不需要。首帧和尾帧图像的分辨率可以不同，系统会自动处理。

输出视频的宽高比将以首帧图像为基准（近似），分辨率将根据所选 `resolution` 档位（如 `720P`）自动适配至相近总像素。
