# 万相-首尾帧生视频API参考（2.2）

万相2.2-首尾帧生视频模型基于**首帧图像**、**尾帧图像和文本提示词**，生成一段平滑过渡的视频。

**相关文档**：[使用指南](https://help.aliyun.com/zh/model-studio/image-to-video-first-and-last-frames-guide)

## 适用范围

为确保调用成功，请务必保证模型、Endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://help.aliyun.com/zh/model-studio/image-to-video-first-and-last-frames-guide#06f39eafa2dwt)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
    
-   **配置 API Key**：选择地域并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   **安装 SDK**：如需通过SDK进行调用，请[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

**说明**

本文的示例代码适用于**北京地域**。

## HTTP调用

由于图生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

### 步骤1：创建任务获取任务ID

## **北京**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

## **新加坡**

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 首尾帧生视频

根据首帧、尾帧和prompt生成视频。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.2-kf2v-flash",
    "input": {
        "first_frame_url": "https://wanx.alicdn.com/material/20250318/first_frame.png",
        "last_frame_url": "https://wanx.alicdn.com/material/20250318/last_frame.png",
        "prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。"
    },
    "parameters": {
        "resolution": "480P",
        "prompt_extend": true
    }
}'
```

## 使用Base64

首帧first\_frame\_url和尾帧last\_frame\_url参数支持传入图像的 Base64 编码字符串。先下载[first\_frame\_base64](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250722/vzjwiv/first_frame_base64.txt)和[last\_frame\_base64](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250722/qbtevh/last_frame_base64.txt)文件，并将完整内容粘贴至对应参数中。

格式参见[如何输入图像](https://help.aliyun.com/zh/model-studio/image-to-video-first-and-last-frames-guide#69308edfbebnx)。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-kf2v-plus",
    "input": {
        "first_frame_url": "data:image/png;base64,GDU7MtCZzEbTbmRZ......",
        "last_frame_url": "data:image/png;base64,VBORw0KGgoAAAANSUh......",
        "prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true
    }
}'
```

## 使用视频特效

必须传入`first_frame_url`和`template`，无需传入prompt和last\_frame\_url。

不同模型支持不同的特效模板。调用前请查阅[万相-图生视频-视频特效](https://help.aliyun.com/zh/model-studio/wanx-video-effects)，以免调用失败。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-kf2v-plus",
    "input": {
        "first_frame_url": "https://ty-yuanfang.oss-cn-hangzhou.aliyuncs.com/lizhengjia.lzj/tmp/11.png",
        "template": "hanfu-1"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true
    }
}'
```

## 使用反向提示词

通过 negative\_prompt 指定生成的视频避免出现“人物”元素。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-kf2v-plus",
    "input": {
        "first_frame_url": "https://wanx.alicdn.com/material/20250318/first_frame.png",
        "last_frame_url": "https://wanx.alicdn.com/material/20250318/last_frame.png",
        "prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
        "negative_prompt": "人物"
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true
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

模型名称。示例值：wan2.2-kf2v-flash。

详情参见百炼控制台。

**input** `_object_` **（必选）**

输入的基本信息，如提示词等。

**属性**

**prompt** `_string_` （可选）

文本提示词。支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。

如果首尾帧的主体和场景变化较大，建议描写变化过程，例如运镜过程（镜头向左移动）或者主体运动过程（人向前奔跑）。

示例值：一只黑色小猫好奇地看向天空，**镜头从平视逐渐上升**，最后**俯拍**它的好奇的眼神。

提示词的使用技巧请参见[文生视频/图生视频Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-video-prompt)。

**negative\_prompt** `_string_` （可选）

反向提示词，用来描述不希望在视频画面中看到的内容，可以对视频画面进行限制。

支持中英文，长度不超过500个字符，超过部分会自动截断。

示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。

**first\_frame\_url** `_string_` **（必选）**

首帧图像的URL或 Base64 编码数据。**输出视频的宽高比将以此图像为基准。**

图像限制：

-   图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
    
-   图像分辨率：图像的宽度和高度范围为\[240,8000\]，单位为像素。
    
-   文件大小：不超过10MB。
    

支持输入的格式：

1.  公网URL:
    
    -   支持 HTTP 或 HTTPS 协议。
        
    -   示例值：https://wanx.alicdn.com/xxx/first\_frame.png。
        
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
        
    -   示例值：oss://dashscope-instant/xxx/xxx.png。
        
3.  Base64 编码图像后的字符串：
    
    -   数据格式：`data:{MIME_type};base64,{base64_data}`。
        
    -   示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......。（编码字符串过长，仅展示片段）
        
    -   详情请参见[如何输入图像](https://help.aliyun.com/zh/model-studio/image-to-video-first-and-last-frames-guide#69308edfbebnx)。
        

**last\_frame\_url** `_string_` （可选）

尾帧图像的URL或 Base64 编码数据。

图像限制：

-   图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
    
-   图像分辨率：图像的宽度和高度范围为\[240,8000\]，单位为像素。尾帧图像分辨率可与首帧不同，无需强制对齐。
    
-   文件大小：不超过10MB。
    

支持输入的格式：

1.  公网URL:
    
    -   支持 HTTP 或 HTTPS 协议。
        
    -   示例值：https://wanx.alicdn.com/xxxx/last\_frame.png。
        
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
        
    -   示例值：oss://dashscope-instant/xxx/xxx.png。
        
3.  Base64 编码图像后的字符串：
    
    -   数据格式：`data:{MIME_type};base64,{base64_data}`。
        
    -   示例值：data:image/png;base64,GDU7MtCZ......。（编码字符串过长，仅展示片段）
        
    -   详情请参见[如何输入图像](https://help.aliyun.com/zh/model-studio/image-to-video-first-and-last-frames-guide#69308edfbebnx)。
        

**template** `_string_` （可选）

视频特效模板的名称。使用此参数时，仅需传入 `first_frame_url`。

不同模型支持不同的特效模板。调用前请查阅[万相-图生视频-视频特效](https://help.aliyun.com/zh/model-studio/wanx-video-effects)，以免调用失败。

示例值：hufu-1，表示使用“唐韵翩然”特效。

**parameters** `_object_` （可选）

视频处理参数。

**属性**

**resolution** `_string_` （可选）

**重要**

**resolution**直接影响费用，同一模型：1080P > 720P > 480P，调用前请确认百炼控制台。

生成的视频分辨率档位。仅用于调整视频的清晰度（总像素），不改变视频的宽高比，**视频宽高比将与首帧图像 first\_frame\_url 的宽高比保持一致**。

此参数的默认值和可用枚举值依赖于 model 参数，规则如下：

-   wan2.2-kf2v-flash：可选值：480P、720P、1080P。默认值为`720P`。
    
-   wanx2.1-kf2v-plus：可选值：720P。默认值为`720P`。
    

示例值：720P。

**duration** `_integer_` （可选）

**重要**

duration直接影响费用，按秒计费，调用前请确认百炼控制台。

视频生成时长，单位为秒。当前参数值固定为5，且不支持修改。模型将始终生成5秒时长的视频。

**prompt\_extend** `_bool_` （可选）

是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。

-   true：默认值，开启智能改写。
    
-   false：不开启智能改写。
    

示例值：true。

**watermark** `_bool_` （可选）

是否添加水印标识，水印位于图片右下角，文案为“AI生成”。

-   false：默认值，不添加水印。
    
-   true：添加水印。
    

示例值：false。

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

### 步骤2：根据任务ID查询结果

## **北京**

`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

## **新加坡**

`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

**说明**

-   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
    
-   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
    
-   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
    
-   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
    
-   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](https://help.aliyun.com/zh/model-studio/async-task-api)。
    
-   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks#f26499d72adsl)。
    

#### 请求参数

## 查询任务结果

请将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

> 若使用新加坡地域的模型，需将base\_url替换为https://dashscope-intl.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx

```
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_`**（必选）**

任务ID。

#### **响应参数**

## 任务执行成功

视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。

```
{
    "request_id": "ec016349-6b14-9ad6-8009-xxxxxx",
    "output": {
        "task_id": "3f21a745-9f4b-4588-b643-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-04-18 10:36:58.394",
        "scheduled_time": "2025-04-18 10:37:13.802",
        "end_time": "2025-04-18 10:45:23.004",
        "video_url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?xxxxx",
        "orig_prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
        "actual_prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。小猫的黄色眼睛明亮有神，毛发光滑，胡须清晰可见。背景是简单的浅色墙面，突显小猫的黑色身影。近景特写，强调小猫的表情变化和眼神细节。"
    },
    "usage": {
        "video_duration": 5,
        "video_count": 1,
        "SR": 480
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

链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。

**orig\_prompt** `_string_`

原始输入的prompt，对应请求参数`prompt`。

**actual\_prompt** `_string_`

开启 prompt 智能改写后，返回实际使用的优化后 prompt。若未开启该功能，则不返回此字段。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计。只对成功的结果计数。

**属性**

**video\_duration** `_integer_`

生成视频的时长，单位秒。枚举值为5。计费公式：费用 = 视频秒数 × 单价。

**video\_count** `_integer_`

生成视频的数量。固定为1。

**video\_ratio** `_string_`

当前仅当2.1模型返回该值。生成视频的比例，固定为standard。

**SR** `_integer_`

当前仅当2.2模型返回该值。生成视频的分辨率档位，枚举值为480、720、1080。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference#42703589880ts)基本一致，参数结构根据语言特性进行封装。

由于图生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

### Python SDK调用

**重要**

请确保 DashScope Python SDK 版本**不低于** `**1.23.8**`，再运行以下代码。

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。

根据模型所在地域设置 `**base_http_api_url**`:

## **北京**

`dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'`

## **新加坡**

`dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'`

#### **示例代码**

## 同步调用

本示例展示三种图像输入方式：公网URL、Base64编码、本地文件路径。

##### 请求示例

```
import base64
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import mimetypes
import dashscope

# 以下为北京地域URL，各地域的URL不同，获取URL：https://help.aliyun.com/zh/model-studio/text-to-video-api-reference
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# --- 辅助函数：用于 Base64 编码 ---
# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可

1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""

# 【方式一】使用公网图片 URL
first_frame_url = "https://wanx.alicdn.com/material/20250318/first_frame.png"
last_frame_url = "https://wanx.alicdn.com/material/20250318/last_frame.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# first_frame_url = "file://" + "/path/to/your/first_frame.png"  # Linux/macOS
# last_frame_url = "file://" + "C:/path/to/your/last_frame.png"  # Windows
# 示例（相对路径）：
# first_frame_url = "file://" + "./first_frame.png"              # 以实际路径为准
# last_frame_url = "file://" + "./last_frame.png"                # 以实际路径为准

# 【方式三】使用Base64编码的图片
# first_frame_url = encode_file("./first_frame.png")            # 以实际路径为准
# last_frame_url = encode_file("./last_frame.png")              # 以实际路径为准

def sample_sync_call_kf2v():
    print('please wait...')
    rsp = VideoSynthesis.call(api_key=api_key,
                              model="wan2.2-kf2v-flash",
                              prompt="写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
                              first_frame_url=first_frame_url,
                              last_frame_url=last_frame_url,
                              resolution="720P",
                              prompt_extend=True)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_sync_call_kf2v()
```

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

```
{
    "status_code": 200,
    "request_id": "efa545b3-f95c-9e3a-a3b6-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "721164c6-8619-4a35-a6d9-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?xxxxx",
        "submit_time": "2025-02-12 11:03:30.701",
        "scheduled_time": "2025-02-12 11:06:05.378",
        "end_time": "2025-02-12 11:12:18.853",
        "orig_prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
        "actual_prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。小猫毛发乌黑光亮，眼睛大而明亮，瞳孔呈金黄色。它抬头仰望，耳朵竖立，显得格外专注。镜头上移后，小猫转头直视镜头，眼神中充满好奇与警觉。背景简洁，突出小猫的细节特征。近景特写，自然光线柔和。"
    },
    "usage": {
        "video_count": 1,
        "video_duration": 5,
        "video_ratio": "standard"
    }
}
```

## 异步调用

本示例展示异步调用方式。该方式会立即返回任务ID，需要自行轮询或等待任务完成。

##### 请求示例

```
import os
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

"""
环境要求：
    dashscope python SDK >= 1.23.8
安装/升级SDK:
    pip install -U dashscope
"""

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 使用公网可访问的图片URL
first_frame_url = "https://wanx.alicdn.com/material/20250318/first_frame.png"
last_frame_url = "https://wanx.alicdn.com/material/20250318/last_frame.png"

def sample_async_call_kf2v():
    # 异步调用，返回一个task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                    model="wan2.2-kf2v-flash",
                                    prompt="写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
                                    first_frame_url=first_frame_url,
                                    last_frame_url=last_frame_url,
                                    resolution="720P",
                                    prompt_extend=True)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # 获取异步任务信息
    status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)  # check the task status
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # 等待异步任务结束
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_kf2v()
```

##### 响应示例

1、创建任务的响应示例

```
{
    "status_code": 200,
    "request_id": "c86ff7ba-8377-917a-90ed-xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "task_id": "721164c6-8619-4a35-a6d9-xxxxxx",
        "task_status": "PENDING",
        "video_url": ""
    },
    "usage": null
}
```

2、查询任务结果的响应示例

> video\_url 有效期24小时，请及时下载视频。

```
{
    "status_code": 200,
    "request_id": "efa545b3-f95c-9e3a-a3b6-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "721164c6-8619-4a35-a6d9-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?xxxxx",
        "submit_time": "2025-02-12 11:03:30.701",
        "scheduled_time": "2025-02-12 11:06:05.378",
        "end_time": "2025-02-12 11:12:18.853",
        "orig_prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。",
        "actual_prompt": "写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。小猫毛发乌黑光亮，眼睛大而明亮，瞳孔呈金黄色。它抬头仰望，耳朵竖立，显得格外专注。镜头上移后，小猫转头直视镜头，眼神中充满好奇与警觉。背景简洁，突出小猫的细节特征。近景特写，自然光线柔和。"
    },
    "usage": {
        "video_count": 1,
        "video_duration": 5,
        "video_ratio": "standard"
    }
}
```

### Java SDK调用

**重要**

请确保 DashScope Java SDK 版本**不低于** `**2.20.9**`，再运行以下代码。

若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。

#### **示例代码**

## 同步调用

本示例展示同步调用方式，并支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

/**
 * 环境要求
 *      dashscope java SDK >= 2.20.9
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */
public class Kf2vSync {

    static {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String firstFrameUrl = "https://wanx.alicdn.com/material/20250318/first_frame.png";
    static String lastFrameUrl = "https://wanx.alicdn.com/material/20250318/last_frame.png";

    //【方式二】本地文件路径（file://+绝对路径 or file:///+绝对路径）
    // static String firstFrameUrl = "file://" + "/your/path/to/first_frame.png";   // Linux/macOS
    // static String lastFrameUrl = "file:///" + "C:/path/to/your/img.png";        // Windows

    //【方式三】Base64编码
    // static String firstFrameUrl = Kf2vSync.encodeFile("/your/path/to/first_frame.png");
    // static String lastFrameUrl = Kf2vSync.encodeFile("/your/path/to/last_frame.png");

    public static void syncCall() {

        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("resolution", "720P");

        VideoSynthesis videoSynthesis = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.2-kf2v-flash")
                        .prompt("写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。")
                        .firstFrameUrl(firstFrameUrl)
                        .lastFrameUrl(lastFrameUrl)
                        .parameters(parameters)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = videoSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));
    }

    /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
     */
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        // 检测MIME类型
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        // 读取文件内容并编码
        byte[] fileBytes = null;
        try{
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }

        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

##### 响应示例

> video\_url 有效期24小时，请及时下载视频。

```
{
    "request_id": "e6bb4517-c073-9c10-b748-dedb8c11bb41",
    "output": {
        "task_id": "984784fe-83c1-4fc4-88c7-52c2c1fa92a2",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.mp4?xxxxx"
    },
    "usage": {
        "video_count": 1,
        "video_duration": 5,
        "video_ratio": "standard"
    }
}
```

## 异步调用

本示例展示异步调用方式。该方式会立即返回任务ID，需要自行轮询或等待任务完成。

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisListResult;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;
import java.util.HashMap;
import java.util.Map;

/**
 * 环境要求
 *      dashscope java SDK >= 2.20.9
 * 更新maven依赖:
 *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
 */

public class Kf2vAsync {

    static {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // 公网URL
    static String firstFrameUrl = "https://wanx.alicdn.com/material/20250318/first_frame.png";
    static String lastFrameUrl = "https://wanx.alicdn.com/material/20250318/last_frame.png";

    public static void asyncCall(){

        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("resolution", "720P");

        VideoSynthesis videoSynthesis = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.2-kf2v-flash")
                        .prompt("写实风格，一只黑色小猫好奇地看向天空，镜头从平视逐渐上升，最后俯拍它的好奇的眼神。")
                        .firstFrameUrl(firstFrameUrl)
                        .lastFrameUrl(lastFrameUrl)
                        .parameters(parameters)
                        .build();
        VideoSynthesisResult result = null;
        try {
            System.out.println("---async call, please wait a moment----");
            result = videoSynthesis.asyncCall(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        } catch (InputRequiredException e) {
            throw new RuntimeException(e);
        }
        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();

        System.out.println("taskId=" + taskId);

        try {
            result = videoSynthesis.wait(taskId, apiKey);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        System.out.println(JsonUtils.toJson(result.getOutput()));
    }

    // 获取任务列表
    public static void listTask() throws ApiException, NoApiKeyException {
        VideoSynthesis is = new VideoSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        VideoSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    // 获取单个任务结果
    public static void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        VideoSynthesis is = new VideoSynthesis();
        // 如果已设置 DASHSCOPE_API_KEY 为环境变量，apiKey 可为空
        VideoSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args){
        asyncCall();
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
    "request_id": "5dbf9dc5-4f4c-9605-85ea-xxxxxxxx",
    "output": {
        "task_id": "7277e20e-aa01-4709-xxxxxxxx",
        "task_status": "PENDING"
    }
}
```

2、查询任务结果的响应示例

> video\_url 有效期24小时，请及时下载视频。

```
{
    "request_id": "1625235c-c13e-93ec-aff7-xxxxxxxx",
    "output": {
        "task_id": "464a5e46-79a6-46fd-9823-xxxxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?xxxxxx"
    },
    "usage": {
        "video_count": 1,
        "video_duration": 5,
        "video_ratio": "standard"
    }
}
```

## **使用限制**

-   **数据时效**：任务`task_id`和 视频`video_url`均只保留 24 小时，过期后将无法查询或下载。
    
-   **音频支持**：当前仅支持生成无声视频，不支持音频输出。如有需要，可通过[语音合成](https://help.aliyun.com/zh/model-studio/speech-recognition-api-reference/)生成音频。
    
-   **内容审核**：输入prompt 和图像、输出视频均会经过内容安全审核，含违规内容将返回 “IPInfringementSuspect”或“DataInspectionFailed”错误，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。
    

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## **常见问题**

#### **Q：如何生成特定宽高比（如3:4）的视频？**

**A：** 输出视频的宽高比由**输入首帧图像（first\_frame\_url）**决定，但**无法保证精确比例**（如严格3:4），会存在一定偏差。

-   **为什么会有偏差？**
    
    模型会以输入图像的比例为基准，结合设置的分辨率档位（resolution）总像素，自动计算出最接近的合法分辨率。由于要求视频的长和宽必须是 16 的倍数，模型会对最终分辨率做微调，因此无法保证输出比例严格等于 3:4，但会非常接近。
    
    -   例如：输入图像750×1000（宽高比 3:4 = 0.75），并设置 resolution = "720P"（目标总像素约 92 万），实际输出816×1104（宽高比 ≈ 0.739，总像素约90万）。
        
-   **实践建议**：
    
    -   **输入控制**：尽量使用与目标比例一致的图片作为首帧输入。
        
    -   **后期处理**：如果您对比例有严格要求，建议在视频生成后，使用编辑工具进行简单的裁剪或黑边填充。
        

### **Q：如何获取视频存储的访问域名白名单？**

A： 模型生成的视频存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。
