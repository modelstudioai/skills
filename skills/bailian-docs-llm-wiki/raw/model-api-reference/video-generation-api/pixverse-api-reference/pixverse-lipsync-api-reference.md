# 爱诗-视频对口型API参考

爱诗-视频对口型模型支持输入**视频**和**音频**（或 TTS 文本），生成与音频同步的对口型视频。

**重要**

本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **服务开通**

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
    
2.  在弹窗内确认开通及授权。
    

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL。
    
-   **配置 API Key**：选择地域并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    

**说明**

本文的视频对口型示例适用于**华北2（北京）地域**。

## HTTP调用

由于视频对口型任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### **步骤1：创建任务获取任务ID**

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 音频驱动

传入视频和音频文件，生成对口型视频。

```
# 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "pixverse/pixverse-lipsync",
    "input": {
        "media": [
            {
                "type": "video_url",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4"
            },
            {
                "type": "audio_url",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/aumwir/stella2-%E6%9C%89%E5%A3%B0%E4%B9%A67.wav"
            }
        ]
    },
    "parameters": {
        "watermark": true
    }
}'
```

## TTS 文本驱动

传入视频和 TTS 文本，由模型合成语音并生成对口型视频。

```
# 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "pixverse/pixverse-lipsync",
    "input": {
        "media": [
            {
                "type": "video_url",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4"
            },
            {
                "type": "lip_sync_tts_speaker_id",
                "id": "auto"
            },
            {
                "type": "lip_sync_tts_content",
                "content": "保持热爱持续开心，琐碎小事不值得烦心"
            }
        ]
    },
    "parameters": {
        "watermark": true
    }
}'
```

##### 请求头（Headers）

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

##### 请求体（Request Body）

**model** `_string_` **（必选）**

模型名称。固定值：`pixverse/pixverse-lipsync`。

**input** `_object_` **（必选）**

输入的基本信息，包括人脸视频和音频来源。

**属性**

**media** `_array_` **（必选）**

媒体资源列表。必须包含一个 `video_url` 类型的视频，以及音频来源（二选一）：

-   **方式一（音频驱动）**：传入 `audio_url` 类型的音频文件。
    
-   **方式二（TTS 合成）**：同时传入 `lip_sync_tts_speaker_id` 和 `lip_sync_tts_content`。
    

**重要**

`audio_url` 与 `lip_sync_tts_speaker_id` + `lip_sync_tts_content` 二选一，不允许同时传入。

**元素属性**

**type** `_string_` **（必选）**

媒体类型标识符。取值范围：

-   `video_url`：人脸视频。
    
-   `audio_url`：音频文件。
    
-   `lip_sync_tts_speaker_id`：TTS 音色 ID。
    
-   `lip_sync_tts_content`：TTS 文本内容。
    

**url** `_string_` **（条件必选）**

当 type 为 `video_url` 或 `audio_url` 时必填。媒体资源的 URL 地址。

-   `video_url`：输入视频的 URL。视频需包含可用于对口型的人脸画面。
    
    -   文件大小：不超过 250MB。
        
    -   时长：不超过 300 秒。
        
    -   支持格式：MP4、MOV、WebM。
        
-   `audio_url`：音频文件的 URL。
    
    -   文件大小：不超过 100MB。
        
    -   时长：不超过 300 秒。
        
    -   支持格式：MP3、WAV、M4A、AAC。
        

**id** `_string_` **（条件必选）**

当 type 为 `lip_sync_tts_speaker_id` 时必填。TTS 音色 ID。取值为 `auto` 时随机选择音色，取值为数字字符串时按音色 ID 指定。支持的取值见下表。

**音色取值表**

**id 取值**

**音色名称**

auto

随机

2

詹有鱼

4

外国阿利

6

李解

10

姜姜好

11

老森

12

李杰克

13

钱多多

14

呆萌王小拍

16

屯里大嗓

18

豫语汉子

19

宝岛囡囡

20

陕西掌柜

21

港风阿sir

**content** `_string_` **（条件必选）**

当 type 为 `lip_sync_tts_content` 时必填。需要驱动口型的文本内容，支持中英文，不超过 200 字（UTF-8 编码）。

**parameters** `_object_` **（可选）**

视频生成参数。如设置是否添加水印等。

**属性**

**watermark** `_boolean_` （可选）

是否添加水印标识，水印位于视频右下角，文案固定为"AI生成"。

-   `false`：默认值，不添加水印。
    
-   `true`：添加水印。
    

### **步骤2：根据任务ID查询结果**

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
    
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

#### 请求参数

## 查询任务结果

将`{task_id}`完整替换为上一步接口返回的`task_id`的值。`task_id`查询有效期为24小时，并请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

#### **任务执行成功**

```
{
    "request_id": "ddf8140e-67c6-9e70-8953-xxxxxx",
    "output": {
        "task_id": "1acb9d0c-7a63-4ff6-a198-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-07-15 17:01:49.352",
        "scheduled_time": "2026-07-15 17:01:49.398",
        "end_time": "2026-07-15 17:02:29.724",
        "video_url": "https://media.pixverseai.cn/xxxx.mp4"
    },
    "usage": {
        "duration": 7,
        "size": "1080*1920",
        "fps": 24,
        "video_count": 1,
        "SR": ""
    }
}
```

## 任务执行失败

若任务执行失败，task\_status将置为 FAILED，并提供错误码和信息。请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

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

**video\_url** `_string_`

视频URL。仅在 task\_status 为 SUCCEEDED 时返回。

视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储，请及时下载。

**orig\_prompt** `_string_`

原始输入的prompt，对应请求参数`prompt`。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**duration** `_integer_`

计费时长（秒）。音频驱动方式为音频时长向上取整；TTS 方式为文本字节数（UTF-8）÷ 15 向上取整。

**size** `_string_`

输出视频的分辨率。

**fps** `_integer_`

输出视频的帧率。

**SR** `_string_`

输出视频的分辨率档位。

**video\_count** `_integer_`

视频数量，固定为 1。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
