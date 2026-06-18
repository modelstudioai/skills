# 可灵-图像生成API参考

可灵-图像生成模型支持**文生图**、**参考图生图**两种任务。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **模型概览**

**模型名称**

**能力支持**

**输入模态**

**输出图像规格**

kling/kling-v3-image-generation

-   文生图
    
-   参考图生图：仅单图输入。
    

文本、图像

图像分辨率：1k、2k

宽高比：16:9、9:16、1:1

图像张数：通过参数n指定（1～9）

图像格式：png

kling/kling-v3-omni-image-generation

-   文生图
    
-   参考图生图：支持多图输入，支持生成分镜组图。
    

文本、图像

图像分辨率：1k、2k、4k

宽高比：16:9、9:16、1:1

图像张数：

-   单图模式通过参数`n`指定：1～9
    
-   组图模式通过`series_amount`指定：2～9
    

图像格式：png

## **前提条件**

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索“可灵”，找到**可灵AI** 模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
    
2.  **配置API Key**：选择地域并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    

## HTTP调用

图像生成任务有一定耗时（通常为1-2分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### 步骤一：提交图像生成任务

**北京地域**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

#### 请求参数

## 文生图

支持模型：`kling/kling-v3-omni-image-generation`、`kling/kling-v3-image-generation`。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "kling/kling-v3-image-generation",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "一间有着精致窗户的花店,漂亮的木质门,摆放着花朵"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "n": 2,
        "aspect_ratio": "1:1",
        "resolution": "1k"
    }
}'
```

## 图生图（组图模式）

支持模型：`kling/kling-v3-omni-image-generation`。

支持以下模式：

-   **单图**（`result_type=single`）：独立生成，批量时仅风格相似。
    
-   **组图**（`result_type=series`）：分镜序列生成，保持角色/场景/叙事连续性。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "kling/kling-v3-omni-image-generation",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "参考图1的风格和图2的背景，生成番茄炒蛋"
                    },
                    {
                        "image": "https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png"
                    },
                    {
                        "image": "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "n": 4,
        "result_type": "series",
        "aspect_ratio": "1:1",
        "resolution": "1k"
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

模型名称。可选值：

-   `kling/kling-v3-image-generation`
    
-   `kling/kling-v3-omni-image-generation`
    

**input** `_object_` **（必选）**

输入参数对象，包含以下字段：

**属性**

**messages** `_array_` **（必选）**

请求内容数组。**当前仅支持单轮对话**，因此数组内**有且只有一个对象**，该对象包含`role`和`content`两个属性。

**属性**

**role** `_string_` （可选）

消息的角色。此参数必须设置为`user`。

**content** `_array_` **（必选）**

消息内容，包含文本提示词（text）和可选的参考图像（image，支持多张）。

**属性**

**text** `_string_` **（条件必选）**

正向提示词，用于描述期望生成的图像内容、风格和构图。

支持中英文，长度不超过2500个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。

示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。

**注意**：仅支持传入一个text，不传或传入多个将报错。

**image** `_string_` （可选）

参考图像的URL。

-   支持 HTTP 或 HTTPS 协议。
    
-   示例值：https://xxx/xxx.png。
    

图像限制：

-   格式：JPEG、JPG、PNG（不支持透明通道）。
    
-   分辨率：宽和高的范围为\[300, 8000\]像素。
    
-   宽高比：在1:2.5 ~ 2.5:1之间。
    
-   文件大小：不超过10MB。
    
-   数量限制：参考图片数量和参考主体数量（element\_list数组长度）之和**不得超过10**。
    

**element\_list** `_array_` （可选）

主体列表，用于指定需要保持的主体。

**属性**

**element\_id** `_integer_` （条件必填）

传`element_list`时必填，表示主体ID。请在[可灵-主体ID列表](https://help.aliyun.com/zh/model-studio/kling-object-ids)获取主体ID。

数量限制：参考图片数量和参考主体数量（element\_list数组长度）之和**不得超过10**。

**parameters** `_object_` （可选）

控制图像生成，比如图像张数、宽高比等。

**属性**

**n** `_integer_` （可选）

生成的图像张数。

-   kling/kling-v3-image-generation：取值范围为1～9。默认值为1。
    
-   kling/kling-v3-omni-image-generation：
    
    -   当且仅当`result_type=single`时生效。
        
    -   取值范围为1～9。默认值为1。
        

**result\_type** `_string_` （可选）

支持模型：kling/kling-v3-omni-image-generation。

生成图像的类型。

-   `single`（ 默认值）：单图。批量生成时仅风格相似，无分镜关联。
    
-   `series`：组图。生成具有叙事/视觉连续性的分镜系列图像。
    

**series\_amount** `_integer_` （可选）

支持模型：kling/kling-v3-omni-image-generation。

组图模式下的输出张数。取值范围为2～9，默认值为4。

生效条件：当且仅当`result_type=series`时生效。

**aspect\_ratio** `_string_` （可选）

输出图像的宽高比。

-   `16:9`：默认值。
    
-   `9:16`
    
-   `1:1`
    

示例值：16:9。

**resolution** `_string_` （可选）

输出图像分辨率。

-   kling/kling-v3-image-generation：可选值为`1k`、`2k`，默认值为`1k`。
    
-   kling/kling-v3-omni-image-generation：可选值为`1k`、`2k`、`4k`，默认值为`1k`。
    

示例值：1k。

**watermark** `_bool_` （可选）

是否添加水印标识。水印位于图像右下角，文案固定为“可灵AI”。

-   `false`：默认值，不添加水印。
    
-   `true`：添加水印。
    

示例值：false。

#### 响应参数

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

### 步骤二：查询任务结果

**北京地域**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：图像生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 5 秒）来获取结果。
    
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

#### 响应参数

## 任务执行成功

```
{
    "request_id": "95146d89-9d70-481a-8c16-xxxxxx",
    "output": {
        "task_id": "2c502d25-12a9-4517-8972-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-27 22:46:01.536",
        "scheduled_time": "2026-03-27 22:46:01.580",
        "end_time": "2026-03-27 22:46:24.831",
        "finished": true,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://p4-fdl.klingai.com/xxx.png?xxx",
                            "type": "image"
                        },
                        {
                            "image": "https://p4-fdl.klingai.com/xxx.png?xxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "size": "1024*1024",
        "image_count": 2,
        "SR": "1080"
    }
}
```

## 任务执行异常

如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "a4d78a5f-655f-9639-8437-xxxxxx",
    "code": "InvalidParameter",
    "message": "num_images_per_prompt must be 1"
}
```

**output** `_object_`

任务输出信息。

**属性**

**choices** `_array_`

模型生成的输出内容。此数组仅包含一个元素。

**属性**

**finish\_reason** `_string_`

任务停止原因，自然停止时为`stop`。

**message** `_object_`

模型返回的消息。

**属性**

**role** `_string_`

消息的角色，固定为`assistant`。

**content** `_array_`

**属性**

**type** `_string_`

输出内容的类型。固定为`image`。

**image** `_string_`

生成图像的 URL，图像格式为PNG。**链接有效期为30天**，请及时下载并保存图像。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**image\_count** `_integer_`

生成图像的数量。

**size** `_string_`

生成图片的分辨率，格式为`宽*高`。示例值：1360\*768。

**SR** `_string_`

生成图像的分辨率档位。示例值：1080。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
