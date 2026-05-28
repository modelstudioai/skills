# HappyHorse-参考生视频API参考

HappyHorse-参考生视频模型支持传入**多张参考图像**，通过**文本提示词**描述场景，将图像中的主体角色融合生成一段流畅的视频。

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
    
-   **配置 API Key**：选择地域并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    

**说明**

本文的示例代码适用于**华北2（北京）地域**。

## HTTP调用

由于参考生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### **步骤1：创建任务获取任务ID**

## **华北2（北京）**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

## **新加坡**

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

## **美国（弗吉尼亚）**

`POST https://dashscope-us.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

## **德国（法兰克福）**

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 参考生视频（多图像）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "happyhorse-1.0-r2v",
    "input": {
        "prompt": "[Image 1]中身着红色旗袍的女性，镜头先以侧面中景勾勒旗袍修身剪裁与S型曲线，随即切换至低角度仰拍，捕捉她轻抬玉手展开[Image 2]中的折扇的同时，[Image 3]中的流苏耳坠随头部转动轻盈摆动的细节，最后推近至面部特写，定格在她指尖轻点扇骨、眼波流转间的含蓄风情，多视角全方位展现东方韵味。",
        "media": [
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/mvzfud/hh-v2v-girl.jpg"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/fvuihk/hh-v2v2-folding-fan.jpg"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/imerii/hh-v2v-earrings.jpg"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "ratio": "16:9",
        "duration": 5
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

模型名称。

固定值：happyhorse-1.0-r2v。

**input** `_object_` **（必选）**

输入的基本信息，包括参考图像和提示词。

**属性**

**prompt** `_string_` **（必选）**

文本提示词。用来描述生成视频中期望包含的元素和视觉特点。

支持任何语言输入，长度不超过5000个非中文字符或2500个中文字符，超过部分会自动截断。

**参考指代**：在prompt中通过“**\[Image 1\]、\[Image 2\]**”标识指代`media`数组中对应位置的参考图像，顺序与`media`数组顺序一致。使用时需要指明参考图中的具体对象，例如“\[Image 1\]中身着红色旗袍的女性”。

**media** `_array_` **（必选）**

媒体素材列表，用于指定参考图像。

数组的每个元素为一个媒体对象，包含 `type`和 `url`字段。

-   按照数组顺序定义`prompt`中角色引用的顺序。
    
-   数组中的第 1 个`reference_image`对应 **\[Image 1\]**，第 2 个对应 **\[Image 2\]**，以此类推。
    

**元素属性**

**type** `_string_` **（必选）**

媒体素材类型。固定值为：

-   `reference_image`：参考图像。
    

素材限制：

-   参考图像数量：1～9张。
    

**url** `_string_` **（必选）**

参考图像URL或 Base64 编码数据。

图像限制：

-   格式：JPEG、JPG、PNG、WEBP。
    
-   分辨率：短边不低于400像素，推荐720P以上清晰图。避免传入过小、模糊或压缩过度的图像，影响效果。
    
-   文件大小：不超过20MB。
    

支持输入的格式：

1.  公网URL：
    
    -   支持 HTTP 或 HTTPS 协议。
        
    -   示例值：https://xxx/xxx.jpg。
        
2.  Base64 编码图像后的字符串：
    
    -   数据格式：`data:{MIME_type};base64,{base64_data}`。
        
    -   示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......（示例已截断，仅做演示）。
        
        **Base64编码数据格式**
        
        格式： `data:{MIME_type};base64,{base64_data}` 。
        
        -   {base64\_data}：图像文件经过 Base64 编码后的字符串。
            
        -   {MIME\_type}：图像的媒体类型，需与文件格式对应。
            
        
        图像格式
        
        MIME Type
        
        JPEG
        
        image/jpeg
        
        JPG
        
        image/jpeg
        
        PNG
        
        image/png
        
        WEBP
        
        image/webp
        

**parameters** `_object_` （可选）

视频生成参数。如设置视频分辨率、宽高比、时长等。

**属性**

**resolution** `_string_` （可选）

生成视频的分辨率档位。

可选值：

-   `1080P`：默认值。
    
-   `720P`
    

**ratio** `_string_` （可选）

生成视频的宽高比。

可选值：

-   `16:9`：默认值。
    
-   `9:16`
    
-   `3:4`
    
-   `4:3`
    
-   `4:5`
    
-   `5:4`
    
-   `1:1`
    
-   `9:21`
    
-   `21:9`
    

**duration** `_integer_` （可选）

生成视频的时长，单位为秒。

取值范围：`3~15`之间的整数。

默认值：`5`。

**watermark** `_boolean_` （可选）

是否在生成的视频上添加水印标识。水印位于视频右下角，文案固定为“Happy Horse”。

-   `true`：默认值，添加水印。
    
-   `false`：不添加水印。
    

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

## **华北2（北京）**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

## **新加坡**

`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

## **美国（弗吉尼亚）**

`GET https://dashscope-us.aliyuncs.com/api/v1/tasks/{task_id}`

## **德国（法兰克福）**

`GET https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

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

#### **任务执行成功**

视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。

```
{
    "request_id": "35137489-2862-96cb-b6f2-xxxxxx",
    "output": {
        "task_id": "1469cfc3-3004-4d9e-ab10-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-04-25 15:03:25.848",
        "scheduled_time": "2026-04-25 15:03:25.884",
        "end_time": "2026-04-25 15:04:05.882",
        "orig_prompt": "[Image 1]中身着红色旗袍的女性，镜头先以侧面中景勾勒旗袍修身剪裁与S型曲线，随即切换至低角度仰拍，捕捉她轻抬玉手展开[Image 2]中的折扇的同时，[Image 3]中的流苏耳坠随头部转动轻盈摆动的细节，最后推近至面部特写，定格在她指尖轻点扇骨、眼波流转间的含蓄风情，多视角全方位展现东方韵味。",
        "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxxx.mp4"
    },
    "usage": {
        "duration": 5,
        "input_video_duration": 0,
        "output_video_duration": 5,
        "video_count": 1,
        "SR": 720,
        "ratio": "16:9"
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
        "message": "The resolution is not valid xxxxxx"
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

链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。

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

**input\_video\_duration** `_integer_`

输入视频的总时长，单位为秒。参考生视频中固定为0。

**output\_video\_duration** `_integer_`

输出视频的总时长，单位为秒。

**ratio** `_string_`

生成视频的宽高比。

**SR** `_integer_`

生成视频的分辨率档位。

**video\_count** `_integer_`

生成视频的数量。固定为1。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
