# 万相2.7-视频编辑API参考

万相2.7-视频编辑模型，支持输入多模态（文本/图像/视频），可完成**指令编辑和视频迁移**任务。

**相关文档**：[指南文档](https://help.aliyun.com/zh/model-studio/wan-video-editing-guide)

## 适用范围

为确保调用成功，请务必保证模型、endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://help.aliyun.com/zh/model-studio/use-video-generation#d18108de05ayp)：确认模型所属的地域。
    
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
    
-   **配置 API Key**：获取该地域的[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    

**说明**

本文的示例代码适用于**北京地域**。

## HTTP调用

视频编辑任务耗时较长（通常为1-5分钟），API采用异步调用的方式。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

### **步骤1：创建任务获取任务ID**

## **北京**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

## **新加坡**

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

**说明**

-   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
    
-   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。
    

#### 请求参数

## 纯指令编辑（修改视频风格）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-videoedit",
    "input": {
        "prompt": "将整个画面转换为黏土风格",
        "media": [
            {
                "type": "video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true
    }
}'
```

## **指令+参考图编辑（局部替换）**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.7-videoedit",
    "input": {
        "prompt": "将视频中女孩的衣服替换为图片中的衣服",
        "media": [
            {
                "type": "video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"
            }
        ]
    },
    "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true
    }
}'
```

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

模型名称。

示例值：wan2.7-videoedit。

**input** `_object_` **（必选）**

输入的基本信息，如提示词等。

**属性**

**prompt** `_string_` （可选）

文本提示词。用来描述生成视频中期望包含的元素和视觉特点。

支持中英文，每个汉字/字母占一个字符，超过部分会自动截断。

-   wan2.7-videoedit：长度不超过5000个字符。
    

示例值：为人物换上酷闪的衣服，再戴参考图里的帽子。

**negative\_prompt** `_string_` （可选）

反向提示词，用来描述不希望在视频画面中出现的内容，可以对视频画面进行限制。

支持中英文，长度不超过500个字符，超过部分会自动截断。

示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。

**media** `_array_` **（必选）**

媒体素材列表，用于指定视频生成所需的参考素材（图像、视频）。

数组的每个元素为一个媒体对象，包含 `type` 与 `url` 字段。

**属性**

**type** `_string_` **（必选）**

媒体素材类型。可选值为：

-   `video`：必传。待编辑的视频。
    
-   `reference_image`：可选。参考图像。
    

素材限制：

-   视频有且仅有1个。
    
-   参考图像最多传入4张。
    

**url** `_string_` **（必选）**

媒体素材URL或 Base64 编码数据。素材包括视频和图像。

传入视频（type=video）

待编辑的视频文件的 URL。

视频限制：

-   格式：mp4、mov。
    
-   时长：2～10s。
    
-   分辨率：宽度和高度范围为\[240,4096\]像素。
    
-   宽高比：1:8～8:1。
    
-   文件大小：不超过100MB。
    

支持输入的格式：

1.  公网URL：
    
    -   支持 HTTP 和 HTTPS 协议。
        
    -   示例值：https://xxx/xxx.mp4。
        
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
        
    -   示例值：oss://dashscope-instant/xxx/xxx.mp4。
        

传入图像（type=reference\_image）

参考图像URL或 Base64 编码数据。

图像限制：

-   格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
    
-   分辨率：宽度和高度范围为\[240, 8000\]像素。
    
-   宽高比：1:8～8:1。
    
-   文件大小：不超过20MB。
    

支持输入的格式：

1.  公网URL:
    
    -   支持 HTTP 或 HTTPS 协议。
        
    -   示例值：https://xxx/xxx.png。
        
2.  临时URL：
    
    -   支持OSS协议，必须通过[上传文件获取临时 URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)。
        
    -   示例值：oss://dashscope-instant/xxx/xxx.png。
        
3.  Base64 编码字符串：
    
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
    
    BMP
    
    image/bmp
    
    WEBP
    
    image/webp
    

**parameters** `_object_` （可选）

视频处理参数，如设置视频分辨率、设置视频时长、开启prompt智能改写、添加水印等。

**属性**

**resolution** `_string_` （可选）

生成视频的分辨率档位，用于控制视频的清晰度（总像素）。

-   wan2.7-videoedit：可选值：720P、1080P。默认值为`1080P`。
    

**ratio** `_string_` （可选）

生成视频的宽高比。

生效逻辑：

-   不传 `ratio` 参数：以输入视频的宽高比生成近似比例的视频。
    
-   传入`ratio`参数：按指定的 `ratio` 生成视频。
    

可选值为：

-   `16:9`
    
-   `9:16`
    
-   `1:1`
    
-   `4:3`
    
-   `3:4`
    

不同宽高比对应的输出视频分辨率（宽高像素值）见下方表格。

分辨率档位

宽高比

输出视频分辨率（宽\*高）

720P

16:9

1280\*720

9:16

720\*1280

1:1

960\*960

4:3

1104\*832

3:4

832\*1104

1080P

16:9

1920\*1080

9:16

1080\*1920

1:1

1440\*1440

4:3

1648\*1248

3:4

1248\*1648

**duration** `_integer_` （可选）

生成视频的时长，单位为秒。

使用建议：此参数仅在需要“截断视频”时才需配置。如果希望输出视频与输入视频时长一致，无需设置（或传入默认值 0）。

使用规则：

-   默认行为：默认值为 0，代表直接使用输入视频的时长，不进行截断。
    
-   截断生效：当传入指定时长时，系统会从原视频的 0 秒起，截取至 duration 设置的长度。
    
-   取值范围：支持 \[2, 10\] 之间的整数。
    

**audio\_setting** `_string_` （可选）

视频声音设置。

-   `auto` （默认）：模型根据 `prompt` 内容智能判断。若提示词涉及声音描述，可能重新生成音频；否则可能保留输入素材的原声。
    
-   `origin`：强制保留输入视频的原声，不重新生成。
    

**prompt\_extend** `_boolean_` （可选）

是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。

-   `true`：默认值，开启智能改写。
    
-   `false`：不开启智能改写。
    

**watermark** `_boolean_` （可选）

是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。

-   `false`：默认值，不添加水印。
    
-   `true`：添加水印。
    

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

### **步骤2：根据任务ID查询结果**

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

## 任务执行成功

视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。

```
{
    "request_id": "f16ae7e9-d518-92f8-a02c-xxxxxx",
    "output": {
        "task_id": "05e68c7e-850c-49e4-b866-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-04-03 00:08:03.576",
        "scheduled_time": "2026-04-03 00:08:13.408",
        "end_time": "2026-04-03 00:11:57.286",
        "orig_prompt": "将视频中女孩的衣服替换为图片中的衣服",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?xxxx"
    },
    "usage": {
        "duration": 10.04,
        "input_video_duration": 5.02,
        "output_video_duration": 5.02,
        "video_count": 1,
        "SR": 720
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

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计，只对成功的结果计数。

**属性**

**input\_video\_duration** `_float_`

输入视频的时长，单位秒。

**output\_video\_duration** `_float_`

输出视频的时长，单位秒。

**duration** `_float_`

总的视频时长，用于计费。

计费公式：`duration=input_video_duration+output_video_duration`。

**SR** `_integer_`

输出视频的分辨率档位。示例值：720。

**video\_count** `_integer_`

生成视频的数量。固定为1。

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](#e9e21dd3a6945)基本一致，参数结构根据语言特性进行封装。

由于视频编辑任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

### Python SDK调用

**重要**

请确保 DashScope Python SDK 版本**不低于** `**1.25.16**`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。

根据模型所在地域设置 `**base_http_api_url**`:

## **北京**

`dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'`

## **新加坡**

`dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'`

## 同步调用

##### 请求示例

```
import base64
import mimetypes
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 以下为北京地域URL，各地域的URL不同
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

# 参考图像URL，支持以下三种输入方式

# 【方式一】使用公网图片URL
reference_image_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# reference_image_url = "file://" + "/path/to/image.png"     # Linux/macOS
# reference_image_url = "file://" + "C:/path/to/image.png"    # Windows
# 示例（相对路径）：
# reference_image_url = "file://" + "./image.png"             # 相对当前执行文件的路径

# 【方式三】使用Base64编码
# reference_image_url = encode_file("/path/to/image.png")

def sample_sync_call_videoedit():
    # call sync api, will return the result
    print('please wait...')
    rsp = VideoSynthesis.call(
        api_key=api_key,
        model='wan2.7-videoedit',
        prompt='将视频中女孩的衣服替换为图片中的衣服',
        media=[
            {
                "type": "video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
            },
            {
                "type": "reference_image",
                "url": reference_image_url
            }
        ],
        resolution='720P',
        prompt_extend=True,
        watermark=True)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_sync_call_videoedit()
```

##### 响应示例

> `video_url` 有效期24小时，请及时下载视频。

```
{
    "status_code": 200,
    "request_id": "d6c3c865-34e9-98a9-a53d-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "1de7c853-755a-454a-91bc-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxxx",
        "submit_time": "2026-04-10 17:16:30.821",
        "scheduled_time": "2026-04-10 17:16:46.379",
        "end_time": "2026-04-10 17:24:59.352",
        "orig_prompt": "将视频中女孩的衣服替换为图片中的衣服"
    },
    "usage": {
        "video_count": 1,
        "video_duration": 0,
        "video_ratio": "",
        "duration": 10.08,
        "input_video_duration": 5.04,
        "output_video_duration": 5.04,
        "SR": 720
    }
}
```

## 异步调用

##### 请求示例

```
import base64
import mimetypes
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 以下为北京地域URL，各地域的URL不同
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

# 参考图像URL，支持以下三种输入方式

# 【方式一】使用公网图片URL
reference_image_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# reference_image_url = "file://" + "/path/to/image.png"     # Linux/macOS
# reference_image_url = "file://" + "C:/path/to/image.png"    # Windows
# 示例（相对路径）：
# reference_image_url = "file://" + "./image.png"             # 相对当前执行文件的路径

# 【方式三】使用Base64编码
# reference_image_url = encode_file("/path/to/image.png")

def sample_async_call_videoedit():
    # call async api, will return the task information
    # you can get task status with the returned task id.
    rsp = VideoSynthesis.async_call(
        api_key=api_key,
        model='wan2.7-videoedit',
        prompt='将视频中女孩的衣服替换为图片中的衣服',
        media=[
            {
                "type": "video",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
            },
            {
                "type": "reference_image",
                "url": reference_image_url
            }
        ],
        resolution='720P',
        prompt_extend=True,
        watermark=True)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # get the task information include the task status.
    status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)  # check the task status
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # wait the task complete, will call fetch interval, and check it's in finished status.
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call_videoedit()
```

##### 响应示例

1、创建任务的响应示例

```
{
    "status_code": 200,
    "request_id": "f16ae7e9-d518-92f8-a02c-xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "task_id": "05e68c7e-850c-49e4-b866-xxxxxx",
        "task_status": "PENDING",
        "video_url": ""
    },
    "usage": null
}
```

2、查询任务结果的响应示例

> `video_url` 有效期24小时，请及时下载视频。

```
{
    "status_code": 200,
    "request_id": "d6c3c865-34e9-98a9-a53d-xxxxxx",
    "code": null,
    "message": "",
    "output": {
        "task_id": "1de7c853-755a-454a-91bc-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxxx",
        "submit_time": "2026-04-10 17:16:30.821",
        "scheduled_time": "2026-04-10 17:16:46.379",
        "end_time": "2026-04-10 17:24:59.352",
        "orig_prompt": "将视频中女孩的衣服替换为图片中的衣服"
    },
    "usage": {
        "video_count": 1,
        "video_duration": 0,
        "video_ratio": "",
        "duration": 10.08,
        "input_video_duration": 5.04,
        "output_video_duration": 5.04,
        "SR": 720
    }
}
```

### Java SDK调用

**重要**

请确保 DashScope Java SDK 版本**不低于** `**2.22.14**`，再运行以下代码。

若版本过低，可能会触发 "url error, please check url!" 等错误。请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)进行更新。

根据模型所在地域设置 `**Constants.baseHttpApiUrl**`:

## **北京**

`Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";`

## **新加坡**

`Constants.baseHttpApiUrl = "https://dashscope-intl.aliyuncs.com/api/v1";`

## 同步调用

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

public class VideoEdit {

    static {
        // 以下为北京地域url，各地域的url不同
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // 参考图像URL，支持以下三种输入方式

    // 【方式一】使用公网图片URL
    static String referenceImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png";

    // 【方式二】使用本地文件（支持绝对路径和相对路径）
    // 格式要求：file:// + 文件路径
    // 示例（绝对路径）：
    // static String referenceImageUrl = "file://" + "/path/to/image.png";     // Linux/macOS
    // static String referenceImageUrl = "file://" + "C:/path/to/image.png";   // Windows
    // 示例（相对路径）：
    // static String referenceImageUrl = "file://" + "./image.png";             // 相对当前执行文件的路径

    // 【方式三】使用Base64编码
    // static String referenceImageUrl = encodeFile("/path/to/image.png");

    // 格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        byte[] fileBytes = null;
        try {
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }
        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void videoEdit() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4")
                    .type("video")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url(referenceImageUrl)
                    .type("reference_image")
                    .build());
        }};
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("resolution", "720P");
        parameters.put("prompt_extend", true);
        parameters.put("watermark", true);

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt("将视频中女孩的衣服替换为图片中的衣服")
                        .media(media)
                        .parameters(parameters)
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            videoEdit();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

##### 响应示例

> `video_url` 有效期24小时，请及时下载视频。

```
{
    "request_id": "0a15ad3c-cde7-9f7e-b8d2-xxxxxx",
    "output": {
        "task_id": "0025d1e1-009a-4f53-9c27-xxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "将视频中女孩的衣服替换为图片中的衣服",
        "submit_time": "2026-04-10 17:21:01.719",
        "scheduled_time": "2026-04-10 17:21:13.182",
        "end_time": "2026-04-10 17:31:41.286"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.08,
        "input_video_duration": 5.04,
        "output_video_duration": 5.04,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

## 异步调用

##### 请求示例

```
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisListResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

public class VideoEdit {

    static {
        // 以下为北京地域url，各地域的url不同
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // 参考图像URL，支持以下三种输入方式

    // 【方式一】使用公网图片URL
    static String referenceImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png";

    // 【方式二】使用本地文件（支持绝对路径和相对路径）
    // 格式要求：file:// + 文件路径
    // 示例（绝对路径）：
    // static String referenceImageUrl = "file://" + "/path/to/image.png";     // Linux/macOS
    // static String referenceImageUrl = "file://" + "C:/path/to/image.png";   // Windows
    // 示例（相对路径）：
    // static String referenceImageUrl = "file://" + "./image.png";             // 相对当前执行文件的路径

    // 【方式三】使用Base64编码
    // static String referenceImageUrl = encodeFile("/path/to/image.png");

    // 格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        byte[] fileBytes = null;
        try {
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }
        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void videoEdit() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4")
                    .type("video")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url(referenceImageUrl)
                    .type("reference_image")
                    .build());
        }};
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("resolution", "720P");
        parameters.put("prompt_extend", true);
        parameters.put("watermark", true);

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt("将视频中女孩的衣服替换为图片中的衣服")
                        .media(media)
                        .parameters(parameters)
                        .build();

        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        // 获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
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

    public static void main(String[] args) {
        try {
            videoEdit();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

##### 响应示例

1、创建任务的响应示例

```
{
    "request_id": "f16ae7e9-d518-92f8-a02c-xxxxxx",
    "output": {
        "task_id": "05e68c7e-850c-49e4-b866-xxxxxx",
        "task_status": "PENDING",
        "video_url": ""
    },
    "usage": null,
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> `video_url` 有效期24小时，请及时下载视频。

```
{
    "request_id": "0a15ad3c-cde7-9f7e-b8d2-xxxxxx",
    "output": {
        "task_id": "0025d1e1-009a-4f53-9c27-xxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "将视频中女孩的衣服替换为图片中的衣服",
        "submit_time": "2026-04-10 17:21:01.719",
        "scheduled_time": "2026-04-10 17:21:13.182",
        "end_time": "2026-04-10 17:31:41.286"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.08,
        "input_video_duration": 5.04,
        "output_video_duration": 5.04,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
