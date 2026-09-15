# AI试衣-图片精修API参考

AI 试衣-图片精修是一个后处理模型，可增强 AI 试衣生成图片的真实感与清晰度。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

**快速入口：** [在线体验](https://bailian.console.aliyun.com/model/experience/vision/imageGenerate) ｜ [AI试衣模型总览](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md) ｜ [计费与限流](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md) ｜ [免费额度](raw/model-user-guide/test-1/new-free-quota.md) ｜ [API调用入门指南](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)

**相关API：**![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)｜![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-Plus版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)｜![api](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6710872271/p824099.png) [AI试衣-图片分割](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)

## 模型概览

#### 模型简介

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共用）**

**免费额度**[（查看）](raw/model-user-guide/test-1/new-free-quota.md)

**任务下发接口RPS限制**

**同时处理中任务数量**

aitryon-refiner

[阶梯计价](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)

10

5

400张

#### 模型效果示意

**AI试衣生成效果（精修前）**

**图片精修生成效果（精修后）**

![test\_client\_tryon](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4435919171/p812703.png)

![result\_refiner](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4435919171/p812705.png)

## 前提条件

AI试衣-图片精修API仅支持通过HTTP进行调用。在调用前，您需要：

-   已开通阿里云百炼服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   已成功调用[AI试衣-Plus版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)或[AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)并获得试衣效果图。

> 在调用 AI试衣API 时，建议设置参数 resolution 为 -1，restore\_face 为 true，以获得最佳的精修前置素材。

## HTTP调用接口

API提供一个异步接口，调用分为两步：

1.  **创建任务**：通过 `POST` 请求创建图片生成任务，获取一个唯一的 task\_id。
2.  **查询结果**：使用 task\_id 通过 `GET` 请求轮询任务状态，直到任务完成并获取结果。

### 步骤1：创建任务

发送 POST 请求来创建一个新的图片精修任务。

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/
```

**说明**

-   因该模型调用耗时较长，故采用异步调用的方式创建任务。
-   任务创建后，系统会立即返回一个 `task_id`。在下一步中，您需要使用此 task\_id 在**24小时内**查询任务结果。

#### 入参描述

**字段**

**类型**

**传参方式**

**必选**

**描述**

**示例值**

Content-Type

String

Header

是

请求类型：application/json。

application/json

Authorization

String

Header

是

API-KEY，例如：Bearer sk-xxxx。

Bearer sk-xxxx

X-DashScope-Async

String

Header

是

使用 enable，表明使用异步方式提交作业。

enable

model

String

Body

是

指明需要调用的模型。

aitryon-refiner

input.top\_garment\_url

String

Body

是

上衣图片 URL。

应与调用[AI试衣-Plus版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)或[AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)时使用的 top\_garment\_url **保持一致**。

-   5KB≤图像文件≤5M
    
-   150≤图像边长≤4096
    
-   格式支持：jpg、png、jpeg、bmp、heic
    
-   需上传服饰平拍图，保持服饰是单一主体且完整，背景干净，四周不宜留白过多
    
-   仅支持HTTP/HTTPS链接，不支持本地路径
    

http://aaa/bbb.jpg

input.bottom\_garment\_url

String

Body

否

下衣图片 URL。

应与调用[AI试衣-Plus版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)或[AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)时使用的 bottom\_garment\_url **保持一致**。

-   5KB≤图像文件≤5M
    
-   150≤图像边长≤4096
    
-   格式支持：jpg、png、jpeg、bmp、heic
    
-   需上传服饰平拍图，保持服饰是单一主体且完整，背景干净，四周不宜留白过多
    
-   仅支持HTTP/HTTPS链接，不支持本地路径
    

http://aaa/bbb.jpg

input.person\_image\_url

String

Body

是

模特图片 URL。

应与调用[AI试衣-Plus版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)或[AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)时使用的 person\_image\_url **保持一致**。

-   5KB≤图像文件≤5M
    
-   150≤图像边长≤4096
    
-   格式支持：jpg、png、jpeg、bmp、heic
    
-   需保持图片中有且仅有一个完整的人
    
-   仅支持HTTP/HTTPS链接，不支持本地路径
    

http://aaa/bbb.jpg

input.coarse\_image\_url

String

Body

是

[AI试衣-Plus版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)或[AI试衣-基础版](raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)生成的试衣效果图URL。

-   5KB≤图像文件≤5M
    
-   150≤图像边长≤4096
    
-   格式支持：jpg、png、jpeg、bmp、heic
    
-   仅支持HTTP/HTTPS链接，不支持本地路径
    

使用试衣精修功能，需在调用AI试衣API时，设参数resolution为-1，restore\_face为true。

http://aaa/bbb.jpg

parameters.gender

String

Body

是

模特性别。用于辅助提升精修效果。

可选值: "woman", "man"。

man

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

异步任务的唯一ID。

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

任务提交后的状态。

PENDING

request\_id

String

本次请求的唯一ID。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

#### 精修图片

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "aitryon-refiner",
    "input": {
        "top_garment_url": "https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/sample-top.jpg",
        "bottom_garment_url": "https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/sample-bottom.jpg",
        "person_image_url": "https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/sample-person.png",
        "coarse_image_url": "https://dashscope-swap.oss-cn-beijing.aliyuncs.com/aa-test/result.png"
    },
    "parameters": {
        "gender": "woman"
    }
 }'
```

#### 响应示例

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

使用上一步获取的 `task_id`，发送 GET 请求查询任务状态和结果。请将 URL 中的`{task_id}` 替换为您的实际任务ID。

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

**说明**

-   图片精修任务耗时约5～15秒不等，建议采用轮询机制，并设置合理的查询间隔（如 3-5 秒）来获取结果。
-   任务成功后返回的 `image_url`有效期为**24小时**，请及时下载并保存图片。
-   此查询接口的默认QPS为20。如需更高频次的查询或事件通知，请[配置异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)。
-   如需批量查询或取消任务，请参见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

#### 入参描述

**字段**

**类型**

**传参方式**

**必选**

**描述**

**示例值**

Authorization

String

Header

是

API-Key，例如：Bearer sk-xxx。

Bearer sk-xxx

task\_id

String

Url Path

是

需要查询任务的ID。

a8532587-fa8c-4ef8-82be-0c46b17950d1

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

查询的任务ID。

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

任务状态。可能的值包括：

-   PENDING 排队中
    
-   PRE-PROCESSING 前置处理中
    
-   RUNNING 处理中
    
-   POST-PROCESSING 后置处理中
    
-   SUCCEEDED 成功
    
-   FAILED 失败
    
-   UNKNOWN 作业不存在或状态未知
    
-   CANCELED：任务取消成功
    

SUCCEEDED

output.image\_url

Array

生成的精修试衣图地址。

**image\_url有效期为24小时**，请及时下载。

[https://.../result.jpg?Expires=xxx](https://.../result.jpg?Expires=xxx)

output.submit\_time

String

任务提交时间。

2024-07-30 15:39:39.918

output.scheduled\_time

String

任务执行时间。

2024-07-30 15:39:39.941

output.end\_time

String

任务完成时间。

2024-07-30 15:39:55.080

output.code

String

错误码。任务失败时返回此参数。

InvalidParameter

output.message

String

错误详情。任务失败时返回此参数。

The request is missing required parameters or in a wrong format

usage.image\_count

Int

本次请求生成的图片张数。

1

request\_id

String

本次请求的唯一ID。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

您需要将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**说明**task\_id 仅支持在**24小时内**查询任务结果，超时会被系统自动清除。

#### 响应示例

#### 成功响应

任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图片。

```
{
    "request_id": "98d46cd0-1f90-9231-9a6c-xxxxxx",
    "output": {
        "task_id": "15991992-1487-40d4-ae66-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-06-30 14:37:53.838",
        "scheduled_time": "2025-06-30 14:37:53.858",
        "end_time": "2025-06-30 14:38:11.472",
        "image_url": "http://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/tryon.jpg?Expires=xxx"
    },
    "usage": {
        "image_count": 1
    }
}
```

#### 失败响应

```
{
    "request_id": "6bf4693b-c6d0-933a-b7b7-xxxxxx",
    "output": {
        "task_id": "e32bd911-5a3d-4687-bf53-xxxxxx",
        "task_status": "FAILED",
        "code": "InvalidParameter",
        "message": "The request is missing required parameters xxxxx"
  }
}
```

## 错误码

大模型服务通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)

同时本模型还有如下特定错误码：

**HTTP 返回码**

**错误码（code）**

**错误信息（message）**

**含义说明**

400

InvalidParameter

The request is missing required parameters or in a wrong format, please check the parameters that you send.

入参格式不对

400

InvalidURL

The request URL is invalid, please check the request URL is available and the request image format is one of the following types: JPEG, JPG, PNG, BMP, and WEBP.

图片URL访问失败，请检查URL或文件格式

400

InvalidPerson

The input image has no human body or multi human bodies. Please upload other image with single person.

输入图片中没有人或多人主体

400

InvalidInputLength

The image resolution is invalid, please make sure that the largest length of image is smaller than 4096, and the smallest length of image is larger than 150. and the size of image ranges from 5KB to 5MB.

上传图片大小不符合要求

400

InvalidParameter

The size of person image and coarse\_image are not the same.

coarse\_image分辨率和person\_image不一致，应保持一致

## 常见问题

### 计费与限流

AI试衣的计费与限流问题请参见[常见问题](https://help.aliyun.com/zh/model-studio/billing-for-outfitanyone#ab05817cca0ws)。
