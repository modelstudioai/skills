# 视频风格重绘API参考

视频风格重绘 API 可将输入视频转换为多种预设艺术风格，并保证画面动态流畅、内容连贯。支持8种预设风格：日式漫画、美式漫画、清新漫画、3D卡通、国风卡通、纸艺风格、简易插画、国风水墨。

**重要**

本文档仅适用于“中国内地（北京）”地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## **效果示意**

**输入视频**

**输出视频（日式漫画）**

更多案例请参见[附录：更多风格效果示意](#a45f4df85e6h7)。

## **前提条件**

在调用前，您需要[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，再[配置API Key为环境变量DASHSCOPE\_API\_KEY](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## **HTTP调用**

因视频处理耗时长，为避免同步请求超时，视频风格重绘采用异步调用，分为以下两步：

1.  **提交异步任务**：通过 `POST` 请求提交原始视频 URL 和期望的风格参数，获取一个唯一的 `task_id`。
    
2.  **查询任务结果**：使用 `task_id` 通过 `GET` 请求轮询任务状态，直至任务完成并获取结果视频的 URL。
    

### 步骤1：提交视频风格重绘任务

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

#### **请求**

##### **生成720P视频**

curl

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "video-style-transform",
    "input": {
        "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4"
    },
    "parameters": {
        "style": 0,
        "video_fps": 15
    }
}'
```

Python

```
import requests
import os

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
# 替换为你的视频 URL
video_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4"

response = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis",
            headers={
                "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
                "X-DashScope-Async": "enable",
            },
            json={
            "model": "video-style-transform",
            "input": {
                "video_url": video_url
            },
            "parameters": {
                "style": 0,
                "video_fps": 15
            }
        }
        )
print(response.json())
```

##### **生成540P视频**

curl

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "video-style-transform",
    "input": {
        "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4"
    },
    "parameters": {
        "style": 0,
        "video_fps": 15,
        "min_len": 540
    }
}'
```

Python

```
import requests
import os

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
# 替换为你的视频 URL
video_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4"

response = requests.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis",
            headers={
                "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
                "X-DashScope-Async": "enable",
            },
            json={
            "model": "video-style-transform",
            "input": {
                "video_url": video_url
            },
            "parameters": {
                "style": 0,
                "video_fps": 15,
                "min_len": 540
            }
        }
        )
print(response.json())
```

##### **请求头（Headers）**

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

**X-DashScope-Async** `_string_` **（必选）**

异步处理配置参数。HTTP请求只支持异步，**必须设置为**`**enable**`。

**重要**

缺少此请求头将报错：“current user api does not support synchronous calls”。

##### **请求体（Request Body）**

**model** `_string_`**（必选）**

模型名称。设置为`video-style-transform`。

**input** `_object_` **（必选）**

输入内容。

**属性**

**video\_url** `_string_`**（必选）**

输入视频公网URL。例如：`https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4`。

输入视频要求：

-   **分辨率**：视频单边尺寸不小于 256 像素，不超过 4096 像素。长边与短边的比例不超过 1.8。
    
-   **格式**：支持 MP4、AVI、MKV、MOV、FLV、TS、MPG、MXF。
    
-   **时长**：不超过 30 秒。
    
-   **大小**：不超过 100 MB。
    
-   **URL**：若原始URL包含中文字符等非ASCII字符，请先进行URL编码。
    

**parameters** `_object_` **（可选）**

视频处理参数。

**属性**

**style** `_int_`**（可选）**

风格类型，预设类型如下：

-   0：日式漫画，默认值
    
-   1：美式漫画
    
-   2：清新漫画
    
-   3：3D卡通
    
-   4：国风卡通（古装输入最佳）
    
-   5：纸艺风格
    
-   6：简易插画
    
-   7：国风水墨
    

**video\_fps** `_int_`**（可选）**

生成视频的帧率，默认为15，范围区间为\[15, 25\]。

**animate\_emotion** `_bool_`**（可选）**

是否进行面部表情优化。默认为`true`。

开启后，通常能提升口型与表情同步精度。在人脸区域占比较小时，关闭此项可能效果更佳。

**min\_len** `_int_` **（可选）**

指定输出视频的短边像素，用于控制分辨率。可选值为`720`或`540`，默认为`720`。

**说明**

此参数值影响计费，720P视频的费用会高于540P。详情请参见[计费与限流](#34ab17504ad65)。

**use\_SR** `_bool_` **（可选）**

是否对风格重绘后视频进行超分辨率（Super-Resolution，SR）处理。默认为`false`。设置为`true`，将免费提升画质。

**说明**

若`min_len`设置为540，开启此项后，输出视频将提升至1080P画质，但计费仍按照540P标准。这会增加处理耗时，推荐在需要高画质输出时开启。

#### **响应**

##### **成功响应**

```
{
    "output": {
	  "task_id": "xxxxxxxx", 
    	  "task_status": "PENDING"
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
```

##### **异常响应**

```
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-xxxxxxxxxxxx"
}
```

**output** `_object_`

任务输出信息。

**属性**

**task\_id** `_string_`

任务id，任务的唯一标识，用于后续查询。

**task\_status** `_string_`

任务状态。

-   PENDING：排队中
    
-   RUNNING：处理中
    
-   SUSPENDED：挂起
    
-   SUCCEEDED：执行成功
    
-   FAILED：执行失败
    

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

### 步骤2：查询任务执行状态和结果

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

**重要**

任务结果数据（如任务状态、生成的视频URL等）有效期为24小时，超时后会被自动清除。请务必及时查询并保存结果。

#### **请求**

##### **获取任务结果**

您需要将`{task_id}`替换为真实的`task_id`。

curl

```
curl -X GET \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

Python

```
import requests
import os

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
# task_id 请替换为你的 task_id
task_id = "0c9c33e6-b2e7-41e5-*********"

task_response = requests.get(
        f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {DASHSCOPE_API_KEY}"
        })
print(task_response.json())
```

##### **请求头（Headers）**

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API-Key进行身份认证。示例值：Bearer sk-xxxx。

##### **URL路径参数（Path parameters）**

**task\_id** `_string_` **（必选）**

任务id。

#### **响应**

##### **任务执行成功**

```
{
    "request_id": "b67df059-ca6a-9d51-afcd-xxxxxxxxxxxx",
    "output": {
        "task_id": "d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2024-05-16 13:50:01.247",
        "scheduled_time": "2024-05-16 13:50:01.354",
        "end_time": "2024-05-16 13:50:27.795",
        "output_video_url": "http://xxx/result.mp4"
    },
    "usage": {
        "duration": 3,
        "SR": 720 
    }
}
```

##### **任务执行中**

任务提交后将处于排队状态，在得到调度之后将转为运行状态，此时任务的状态为RUNNING；

```
{
    "request_id":"e5d70b02-ebd3-98ce-9fe8-xxxxxxxxxxxx",
    "output":{
        "task_id":"13b1848b-5493-4c0e-xxxxxxxxxxxx",
        "task_status":"RUNNING",
        "submit_time":"2025-09-08 15:53:13.143",
        "scheduled_time":"2025-09-08 15:53:13.169"
    }
}
```

##### **任务执行失败**

```
{
    "request_id": "dccfdf23-b38e-97a6-a07b-xxxxxxxxxxxx",
    "output": {
        "task_id": "4cbabbdf-2c1f-43f4-b983-xxxxxxxxxxxx",
        "task_status": "FAILED",
        "submit_time": "2024-05-16 14:15:14.103",
        "scheduled_time": "2024-05-16 14:15:14.154",
        "end_time": "2024-05-16 14:15:14.694",
        "code": "InvalidParameter.FileDownload",
        "message": "download for input video error"
    }
}
```

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**output** `_object_`

任务输出信息。

**属性**

**output\_video\_url** `_string_`

结果视频URL地址。例如：`http://xxx/result.mp4`。

**task\_id** `_string_`

任务ID。查询有效期24小时。

**task\_status** `_string_`

任务状态。

-   PENDING：排队中
    
-   RUNNING：处理中
    
-   SUSPENDED：挂起
    
-   SUCCEEDED：执行成功
    
-   FAILED：执行失败
    
-   UNKNOWN：任务不存在或状态未知。
    

**submit\_time** `_string_`

任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**scheduled\_time** `_string_`

任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**end\_time** `_string_`

任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**usage** `_object_`

输出信息统计。

**属性**

**duration** `_float_`

生成视频时长（秒）。

**SR** `_int_`

用于计费的视频短边像素值（该值与您请求中设置的**min\_len**值相同）。

## **计费与限流**

仅对**执行成功**的任务计费，费用根据输出视频的实际时长（秒）和所选分辨率计算。

**计费公式**：`总费用 = 输出视频时长 (秒) × 对应分辨率的单价`（**最终费用将严格按照任务成功后返回的** `**usage**` **对象中的** `**duration**` **和** `**SR**` **字段进行结算**）

免费额度按输出视频时长进行抵扣，不区分视频分辨率。

**模型名**

**免费额度**[（查看）](https://help.aliyun.com/zh/model-studio/new-free-quota)

**计费单价**

**限流（主账号与RAM子账号共用）**

**任务下发接口QPS限制**

**同时处理中任务数量**

video-style-transform

600秒

720P

0.5元/秒

2

1

540P

0.2元/秒

**计费示例**

假设您提交一个 10 秒的视频，选择 720P 分辨率进行风格转换，任务成功后生成的视频时长为 10 秒。则本次任务费用为：`10 秒 × 0.5 元/秒 = 5 元`。

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## 附录：更多风格效果示意

**风格名称**

**原始视频**

**重绘效果**

**日式漫画（style=0）**

**美式漫画（style=1）**

**清新漫画（style=2）**

**3D卡通（style=3）**

**国风卡通（style=4）**

**纸艺风格（style=5）**

**简易插画（style=6）**

**国风水墨（style=7）**
