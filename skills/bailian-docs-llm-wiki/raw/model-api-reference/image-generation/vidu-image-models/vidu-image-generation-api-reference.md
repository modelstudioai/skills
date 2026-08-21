# Vidu-图像生成API参考

Vidu-参考生图模型支持**文生图**、**图片编辑、参考图生图等**任务。

**重要**

本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **模型概览**

**模型名称**

**能力支持**

**输入模态**

**输出图像规格**

vidu/vidu-image\_reference2image

支持参考生图、文生图、图片编辑，对中英文字的精准渲染、UI/图表等设计细节的像素级还原，适合制作海报、信息图等。

文本、图像

图像分辨率：1K、2K、4K

图像张数：1

图像格式：PNG

vidu/viduq3-fast\_reference2image

支持参考生图、文生图、图片编辑，主打高速高质与低成本，成本比Pro降低约50%。

文本、图像

图像分辨率：1K、2K、4K

图像张数：1

图像格式：PNG

vidu/viduq2-pro\_reference2image

支持参考生图、文生图、图片编辑，擅长处理复杂逻辑，具备超强上下文一致性和工业级稳定性。适合专业设计、漫剧制作等。

文本、图像

图像分辨率：1K、2K、4K

图像张数：1

图像格式：PNG

vidu/viduq2-fast\_reference2image

支持参考生图、文生图、图片编辑，语义理解能力大幅提升，支持更多风格。

文本、图像

图像分辨率：1K

图像张数：1

图像格式：PNG

## **前提条件**

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)，搜索"Vidu"，找到对应模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
    
2.  **配置API Key**：选择地域并[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    

## HTTP调用

图像生成任务有一定耗时，API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

### 步骤一：提交图像生成任务

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

#### 请求参数

## 文生图

支持所有Vidu模型。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "vidu/vidu-image_reference2image",
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
        "size": "1024*1024",
        "n": 1,
        "watermark": false
    }
}'
```

## 参考图生图

支持所有Vidu模型，最多可传入14张参考图。

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "vidu/vidu-image_reference2image",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": "参考图片的风格，生成一只坐着的橘黄色的猫"
                    },
                    {
                        "image": "https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png"
                    }
                ]
            }
        ]
    },
    "parameters": {
        "size": "2048*2048",
        "n": 1,
        "watermark": false
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

模型名称。可选值：

-   `vidu/vidu-image_reference2image`
    
-   `vidu/viduq3-fast_reference2image`
    
-   `vidu/viduq2-pro_reference2image`
    
-   `vidu/viduq2-fast_reference2image`
    

**input** `_object_` **（必选）**

输入参数对象，包含以下字段：

**属性**

**messages** `_array_` **（必选）**

多轮消息列表。服务端会提取第一个非空`text`作为提示词，并提取全部`image`作为参考图。数组内**有且只有一个对象**，该对象包含`role`和`content`两个属性。

**属性**

**role** `_string_` （可选）

消息的角色，建议设置为`user`。

**content** `_array_` **（必选）**

消息内容，包含文本提示词（text）和可选的参考图像（image，支持多张）。

**属性**

**text** `_string_` **（条件必选）**

正向提示词，用于描述期望生成的图像内容、风格和构图。

支持中英文，长度不超过5000个字符，每个汉字、字母、数字或符号计为一个字符。

示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。

**注意**：整个messages中至少需要一个非空文本。

**image** `_string_` （可选）

参考图像的URL。支持传多张，所有模型最多支持输入14张。

-   支持 HTTP 或 HTTPS 协议。
    
-   示例值：https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png。
    

图像限制：

-   格式：PNG、JPG、WEBP。
    
-   宽高比：在1:4 ~ 4:1之间。
    
-   文件大小：所有图片总和不超过50MB。
    
-   数量限制：最多14张参考图片。
    

**parameters** `_object_` （可选）

控制图像生成参数。

**属性**

**size** `_string_` （可选）

图片尺寸，格式为`宽*高`（如`2048*2048`）。不传时默认`1024*1024`。

不同模型支持的尺寸列表请参见下方[可用尺寸列表](#vidu-sizes-h2)。

**n** `_integer_` （可选）

生成图片数量，当前仅支持`1`。传其他值会返回参数错误。

**seed** `_integer_` （可选）

随机数种子，取值范围`[0,2147483647]`，`0`表示随机。

使用相同的`seed`参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。

**watermark** `_bool_` （可选）

是否添加水印标识。

-   `false`：默认值，不添加水印。
    
-   `true`：添加水印。
    

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

创建任务失败，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "code": "InvalidApiKey",
    "message": "No API-key provided.",
    "request_id": "7438d53d-6eb8-4596-8835-xxxxxx"
}
```

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

### 步骤二：查询任务结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**说明**

-   **轮询建议**：图像生成过程需一定时间，建议采用**轮询**机制，并设置合理的查询间隔（如5秒）来获取结果。
    
-   **任务状态流转**：PENDING（等待中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **图片链接有效期**：生成图像的下载链接**24小时**内有效，请及时下载并保存图像。
    

#### 请求参数

## 查询任务结果

```
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location --request GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

**task\_id** `_string_`**（必选）**

任务ID。

#### 响应参数

## 任务执行成功

```
{
    "request_id": "f584a817-6e00-9841-961a-49f7382a03d4",
    "output": {
        "task_id": "6404d4ec-4cdf-45b5-8d7d-3d429c6baed5",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-07-13 20:27:41.291",
        "scheduled_time": "2026-07-13 20:27:41.320",
        "end_time": "2026-07-13 20:28:39.767",
        "finished": true,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://example.com/generated-image.png",
                            "type": "image"
                        }
                    ]
                }
            }
        ]
    },
    "usage": {
        "SR": "2K",
        "size": "2048*2048",
        "image_count": 1
    }
}
```

## 任务执行异常

如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

```
{
    "request_id": "1f015514-b04c-9190-b4dd-8ba11bb15708",
    "output": {
        "task_id": "ccae6c03-fe9f-48fd-b3d6-a524c4707f17",
        "task_status": "FAILED",
        "submit_time": "2026-07-13 20:27:50.654",
        "scheduled_time": "2026-07-13 20:27:50.689",
        "end_time": "2026-07-13 20:27:51.090",
        "code": "InvalidParameter",
        "message": "Missing required field 'parameters.n' in request body"
    }
}
```

**output** `_object_`

任务输出信息。

**属性**

**task\_id** `_string_`

任务ID。

**choices** `_array_`

图片输出候选列表，仅在task\_status=SUCCEEDED时返回。

**属性**

**finish\_reason** `_string_`

结束原因，成功时通常为`stop`。

**message** `_object_`

模型返回的消息。

**属性**

**role** `_string_`

消息的角色，固定为`assistant`。

**content** `_array_`

**属性**

**type** `_string_`

输出内容的类型，固定为`image`。

**image** `_string_`

生成图像的下载链接，图像格式为PNG。**链接有效期为24小时**，请及时下载并保存图像。

**finished** `_bool_`

是否完成，仅在task\_status=SUCCEEDED时返回。

**usage** `_object_`

资源用量信息。只对成功的结果计数。

**属性**

**image\_count** `_integer_`

生成图像的数量。

**size** `_string_`

生成图片的分辨率，格式为`宽*高`。示例值：2048\*2048。

**SR** `_string_`

生成图像的分辨率档位。示例值：2K。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误码](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **可用尺寸列表**

### vidu-image

**分辨率**

**支持尺寸**

1K

1024\*1024、720\*1440、1440\*720、1024\*768、768\*1024、1920\*1088、1088\*1920、1536\*1024、1024\*1536、1920\*816、816\*1920

2K

2048\*2048、1088\*2160、2160\*1088、2736\*2048、2048\*2736、2560\*1440、1440\*2560、3072\*2048、2048\*3072、2560\*1104、1104\*2560

4K

2880\*2880、1440\*2880、2880\*1440、3312\*2480、2480\*3312、3840\*2160、2160\*3840、3520\*2352、2352\*3520、3840\*1648、1648\*3840

### viduq3-fast

**分辨率**

**支持尺寸**

1K

1024\*1024、768\*1376、848\*1264、896\*1200、928\*1152、1152\*928、1200\*896、1264\*848、1376\*768、1584\*672、512\*2064、2064\*512、352\*2928、2928\*352

2K

2048\*2048、1536\*2752、1696\*2528、1792\*2400、1856\*2304、2304\*1856、2400\*1792、2528\*1696、2752\*1536、3168\*1344、1024\*4128、4128\*1024、704\*5856、5856\*704

4K

4096\*4096、3072\*5504、3392\*5056、3584\*4800、3712\*4608、4608\*3712、4800\*3584、5056\*3392、5504\*3072、6336\*2688、2048\*8256、8256\*2048、1408\*11712、11712\*1408

### viduq2-pro

**分辨率**

**支持尺寸**

1K

1024\*1024、768\*1376、848\*1264、896\*1200、928\*1152、1152\*928、1200\*896、1264\*848、1376\*768、1584\*672

2K

2048\*2048、1536\*2752、1696\*2528、1792\*2400、1856\*2304、2304\*1856、2400\*1792、2528\*1696、2752\*1536、3168\*1344

4K

4096\*4096、3072\*5504、3392\*5056、3584\*4800、3712\*4608、4608\*3712、4800\*3584、5056\*3392、5504\*3072、6336\*2688

### viduq2-fast

**分辨率**

**支持尺寸**

1K

1024\*1024、768\*1376、848\*1264、896\*1200、928\*1152、1152\*928、1200\*896、1264\*848、1376\*768、1584\*672
