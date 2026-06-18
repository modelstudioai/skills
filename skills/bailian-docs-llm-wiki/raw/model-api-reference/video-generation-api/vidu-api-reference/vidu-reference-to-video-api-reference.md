# Vidu-参考生视频 API 参考

Vidu-参考生视频模型支持传入**参考图片**和**文本提示词**，将图片中的主体角色融合到提示词描述的场景中，生成流畅的视频内容。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **服务开通**

请前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索 **Vidu**，找到 **Vidu** 模型卡片，单击**立即开通**；在弹窗内确认开通及授权。

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
    
-   **配置 API Key**：选择地域并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    

## HTTP 调用

由于参考生视频任务耗时较长（通常为 1-5 分钟），API 采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### **步骤 1：创建任务获取任务 ID**

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 参考生视频（仅参考图像）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
   -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "vidu/viduq3-mix_reference2video",
       "input": {
        "media": [
            {
                "type": "image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260320/knsple/wan-r2v-role-frame.jpg"
            },
            {
                "type": "image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
            },
            {
                "type": "image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
            }
        ],
        "prompt": "男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣"
    },
    "parameters": {
        "duration": 5,
        "size": "1280*720",
        "resolution": "720P",
        "watermark": true
    }
}'
```

## 参考生视频（参考图像+视频）

支持模型：vidu/viduq2-pro\_reference2video。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
   -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "vidu/viduq2-pro_reference2video",
       "input": {
        "media": [
            {
                "type": "video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"
            },
            {
                "type": "image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
            },
            {
                "type": "image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
            }
        ],
        "prompt": "男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣"
    },
    "parameters": {
        "duration": 5,
        "size": "1280*720",
        "resolution": "720P",
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

模型名称。可选值为：

-   `vidu/viduq3-mix_reference2video`
    
-   `vidu/viduq3_reference2video`
    
-   `vidu/viduq3-turbo_reference2video`
    
-   `vidu/viduq2-pro_reference2video`
    
-   `vidu/viduq2_reference2video`
    

**input** `_object_` **（必选）**

输入的基本信息，包括参考图片和提示词。

**属性**

**prompt** `_string_` **（必选）**

文本提示词。用来描述生成视频中期望包含的元素和视觉特点。

支持中英文，不超过 5000 个字符，超过部分会自动截断。

示例值：男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣。

提示词编写请参见[Vidu视频生成Prompt指南](https://help.aliyun.com/zh/model-studio/vidu-video-generation-prompt-guide)。

**media** `_array_` **（必选）**

媒体素材列表，用于指定视频生成所需的参考图像。

数组的每个元素为一个媒体对象，包含 `type`和 `url` 字段。

**元素属性**

**type** `_string_` **（必选）**

媒体素材类型。可选值与模型有关：

仅传入参考图像

支持模型：vidu/viduq3-mix\_reference2video、vidu/viduq3\_reference2video、vidu/viduq3-turbo\_reference2video、vidu/viduq2\_reference2video

固定为：

-   `image`：参考图像。
    

素材限制：图像数量为1～7张。

传入参考图像和视频

支持模型：vidu/viduq2-pro\_reference2video

可选值为：

-   `image`：参考图像。必选。
    
-   `video`：参考视频。可选。
    

素材限制：

-   仅参考图像：图像数量为1～7张。
    
-   参考图像和视频：
    
    -   图像数量为1～4张。
        
    -   视频数量为1～2个。
        

**url** `_string_` **（必选）**

媒体素材URL。素材包括图像、视频。

传入图像（type=image）

参考图像URL，必须为公网可访问的 URL。

-   支持 HTTP 或 HTTPS 协议。
    
-   示例值：https://xxx/xxx.png。
    

图像限制：

-   格式：JPEG、JPG、PNG、WEBP。
    
-   宽高比：1:4～4:1。
    
-   文件大小：不超过 50MB。
    

传入视频（type=video）

参考视频URL，必须为公网可访问的 URL。

-   支持 HTTP 或 HTTPS 协议。
    
-   示例值：https://xxx/xxx.mp4。
    

视频限制：

-   格式：mp4、avi、mov。
    
-   分辨率：总像素值不小于128\*128。
    
-   宽高比：1:4～4:1。
    
-   时长：传入1个参考视频时为1～8秒；传入2个参考视频时各为1～5秒。
    
-   文件大小：不超过 50MB。
    

**parameters** `_object_` **（必选）**

视频生成参数。如设置视频分辨率、时长等。

**属性**

**resolution** `_string_` （可选）

**重要**

resolution直接影响费用，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#69993500dc6mi)。

生成视频的分辨率。可选值与模型有关：

-   vidu/viduq3-mix\_reference2video：可选720P、1080P。默认值为720P。
    
-   vidu/viduq3\_reference2video：可选540P、720P、1080P。默认值为720P。
    
-   vidu/viduq3-turbo\_reference2video：可选540P、720P、1080P。默认值为720P。
    
-   vidu/viduq2-pro\_reference2video：可选540P、720P、1080P。默认值为720P。
    
-   vidu/viduq2\_reference2video：可选540P、720P、1080P。默认值为720P。
    

**size** `_string_` （可选）

生成视频的分辨率，格式为`宽*高`的像素值。

默认值根据`resolution`而定：

-   当 resolution=540P 时，size 默认为 `1024*576`。
    
-   当 resolution=720P 时，size 默认为 `1280*720`。
    
-   当 resolution=1080P 时，size 默认为 `1920*1080`。
    

分辨率档位

宽高比

**size 取值（宽\*高）**

540P

16:9

1024\*576

4:3

1024\*768

1:1

1024\*1024

3:4

768\*1024

9:16

576\*1024

720P

16:9

1280\*720

4:3

1280\*960

1:1

1280\*1280

3:4

960\*1280

9:16

720\*1280

1080P

16:9

1920\*1080

4:3

1920\*1440

1:1

1808\*1808

3:4

1440\*1920

9:16

1080\*1920

**duration** `_integer_` **（必选）**

**重要**

duration直接影响费用，按秒计费，请在调用前确认[模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#69993500dc6mi)。

生成视频的时长，单位为秒。

-   vidu/viduq3-mix\_reference2video：取值为\[1, 16\]之间的整数。默认值为`5`。
    
-   vidu/viduq3\_reference2video：取值为\[1, 16\]之间的整数。默认值为`5`。
    
-   vidu/viduq3-turbo\_reference2video：取值为\[1, 16\]之间的整数。默认值为`5`。
    
-   vidu/viduq2-pro\_reference2video：取值为\[1, 10\]之间的整数。默认值为`5`。
    
    -   特殊设置：支持设置为0，表示自动规划时长，上限不超过 10 秒。
        
        -   若上传 1 个参考视频：生成视频时长通常等于该参考视频时长。
            
        -   若上传 2 个参考视频：模型结合提示词，生成视频时长通常等于”主要参考视频”的时长。
            
-   vidu/viduq2\_reference2video：取值为\[1, 10\]之间的整数。默认值为`5`。
    

**audio** `_boolean_` （可选）

**支持模型**：vidu/viduq3-mix\_reference2video、vidu/viduq3\_reference2video、vidu/viduq3-turbo\_reference2video。

是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。

-   `false`：默认值，输出无声视频。
    
-   `true`：输出无声视频。
    

**watermark** `_boolean_` （可选）

是否添加水印标识，水印位于视频右下角，文案固定为“内容由AI生成”。

-   `false`：默认值，不添加水印。
    
-   `true`：添加水印。
    

**seed** `_integer_` （可选）

随机数种子，取值范围为`[0, 2147483647]`。

未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。

请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。

示例值：12345。

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

### **步骤 2：根据任务 ID 查询结果**

**北京地域**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **task\_id 有效期**：**24 小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
    
-   **RPS 限制**：查询接口默认 RPS 为 20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
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

##### **URL 路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

#### **任务执行成功**

视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。

```
{
    "request_id": "8f240644-efe8-43bf-86ff-xxxxxx",
    "output": {
        "task_id": "b7e05baa-c318-440d-b293-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-27 15:10:42.723",
        "scheduled_time": "2026-03-27 15:10:42.754",
        "end_time": "2026-03-27 15:11:17.388",
        "orig_prompt": "男人坐在靠窗的椅子上，手持吉他，在咖啡厅旁演奏一首舒缓的美国乡村民谣",
        "video_url": "https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx"
    },
    "usage": {
        "duration": 5,
        "size": "960*528",
        "output_video_duration": 5,
        "fps": 24,
        "video_count": 1,
        "audio": false,
        "reference_type": "image,video",
        "SR": "540"
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

**video\_url** `_string_`

视频 URL。仅在 task\_status 为 SUCCEEDED 时返回。

视频格式为 MP4（H.264 编码）。视频链接有效期24 小时，请及时下载。

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

生成视频的帧率。固定为 24。

**SR** `_string_`

生成视频的分辨率档位。

**audio** `_boolean_`

生成视频是否为有声视频。

**video\_count** `_integer_`

生成视频的数量。固定为 1。

**reference\_type** `_string_`

参考素材类型。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

#### **Q：size 与 resolution 必须同时传入吗？**

**A：** 不必。二者均为可选参数，但**推荐同时传入**。同时传入可精准控制生成视频的宽高比，具体参见[size取值](#pvr219a0tblsiz)。

若不同时传入，系统将按以下两种场景处理：

-   **仅传 size**：size参数会被忽略，系统强制按默认的 `resolution=720P` 及其对应的`size`默认值（`1280*720`）处理。
    
    > 例如：接口返回为size="1280\*720", SR=720。
    
-   **仅传 resolution**：按指定分辨率档位及该档位对应的 16:9 比例输出。
    
    > 例如：当resolution=540P时，接口返回 size="960\*528", SR=540；当resolution=1080P时，接口返回 size="1920\*1080", SR=1080。
