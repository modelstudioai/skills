# 数字人wan2.2-s2v视频生成API参考

数字人wan2.2-s2v模型能基于 单张图片和音频 ，生成动作自然的说话、唱歌或表演视频。

-   **音频驱动**: 通过输入的人声音频，驱动静态图片中的人物实现口型、表情和动作与音频同步。
-   **场景丰富**: 支持 "说话"、"唱歌" 、“表演”三种对口型场景
-   **人物形象多样化**：支持真人（肖像、半身、全身）及卡通人物。
-   **输出视频分辨率**：提供480P、720P两档分辨率选项。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型与价格

**模型名称**

**计费单价**

**限流（主账号与RAM子账号共用）**

**免费额度**[（查看）](raw/model-user-guide/test-1/new-free-quota.md)

**任务下发接口RPS限制**

**同时处理中任务数量**

wan2.2-s2v

480P：0.5元/秒

720P：0.9元/秒

5

1

100秒

## HTTP调用接口

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   配置环境变量：[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

### 步骤1：创建任务获取任务ID

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

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

API-Key，格式为 Bearer sk-xxx。

Bearer sk-1a\*\*2b

X-DashScope-Async

String

Header

是

固定值为 enable，表示使用异步调用方式。

enable

model

String

Body

是

指明需要调用的模型。

wan2.2-s2v

input.image\_url

String

Body

是

上传的图片 URL。

-   图像格式：支持jpg，jpeg，png，bmp，webp。
-   图像分辨率：图像的宽度和高度范围为\[400, 7000\]像素。
-   上传图片仅支持公网可访问的 HTTP/HTTPS 链接。本地文件可通过[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

[http://aaa/bbb.jpg](http://aaa/bbb.jpg)

input.audio\_url

String

Body

是

上传的音频文件 URL。

-   音频格式：格式为wav、mp3。
-   音频限制：文件<15M，时长＜20s。
-   音频内容：音频中需包含清晰、响亮的人声语音，并去除了环境噪音、背景音乐等声音干扰信息。
-   上传音频仅支持公网可访问的 HTTP/HTTPS 链接。本地文件可通过[上传文件获取临时URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

[http://aaa/bbb.mp3](http://aaa/bbb.mp3)

parameters.resolution

String

Body

否

视频分辨率档位。

可选值为480P、720P。默认值为480P。

模型会尽量保持输出视频与输入图像的宽高比一致，在宽高比不变的基础上，将视频总像素调整到所选档位附近。

示例

480P：视频分辨率通常指 640×480（约 31万像素），视频宽高比为4:3。

720P：视频分辨率通常指 1280×720（约 92万像素），视频宽高比为16:9。

**示例**：若输入图像的宽高比例为 4:5，且选择 480P 档位，则输出视频的宽高比会保持4:5，分辨率调整为接近 31万像素。例如，输出视频的分辨率为 480×600，总像素 28.8万（此数据仅做参考，以实际输出为准）。

480P

**说明**生成视频的时长与输入音频的时长一致，因此单次生成的视频时长同样受音频时长限制（须小于 20 秒）；若输入音频超过 20 秒，会导致任务报错。如需生成更长的视频，可将长音频按小于 20 秒切分为多段，分别调用本接口生成对应的视频片段，再使用剪辑工具将多段视频拼接合并为一个完整的长视频。

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

提交异步任务后的 作业状态。

PENDING

request\_id

String

本次请求的唯一ID。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### curl

```
curl 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
 --header 'X-DashScope-Async: enable' \
 --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
 --header 'Content-Type: application/json' \
 --data '{
     "model": "wan2.2-s2v",
     "input": {
            "image_url": "https://img.alicdn.com/imgextra/i3/O1CN011FObkp1T7Ttowoq4F_!!6000000002335-0-tps-1440-1797.jpg",
            "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/iaqpio/input_audio.MP3"
        },
        "parameters": {
            "resolution": "480P"
        }
    }'
```

#### Python SDK

```
from http import HTTPStatus
from dashscope import VideoSynthesis
import dashscope
import os

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
api_key = os.getenv("DASHSCOPE_API_KEY")

def sample_async_call():
    # 异步提交视频生成任务
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                model='wan2.2-s2v',
                                img_url='https://img.alicdn.com/imgextra/i3/O1CN011FObkp1T7Ttowoq4F_!!6000000002335-0-tps-1440-1797.jpg',
                                audio_url='https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250825/iaqpio/input_audio.MP3',
                                resolution='480P')
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # 查询任务状态
    status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # 等待任务完成
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

if __name__ == '__main__':
    sample_async_call()
```

#### 响应示例

```
{
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-xxxxxx",
        "task_status": "PENDING"
    }
    "request_id": "7574ee8f-38a3-4b1e-9280-xxxxxx"
}
```

### 步骤2：根据任务ID查询结果

使用上一步获取的 `task_id`，发送 GET 请求查询任务状态和结果。请将 URL 中的`{task_id}` 替换为您的实际任务ID，并将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}
```

**说明**

-   视频生成任务耗时较长（约5-10分钟），建议采用轮询机制，并设置合理的查询间隔（如 15秒）来获取结果。
-   任务成功后返回的 `video_url`有效期为**24小时**，请及时下载并保存视频。
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
    
-   RUNNING 处理中
    
-   SUCCEEDED 成功
    
-   FAILED 失败
    
-   UNKNOWN 作业不存在或状态未知
    
-   CANCELED：任务取消成功
    

SUCCEEDED

output.submit\_time

String

任务提交时间。

2025-09-01 09:37:27.468

output.scheduled\_time

String

任务执行时间。

2025-09-01 09:37:34.885

output.end\_time

String

任务完成时间。

2025-09-01 09:40:20.734

output.results.video\_url

String

生成的视频文件。

**video\_url有效期为24小时**，请及时下载。

https://xxx/1.mp4?Expires=xxx

usage.duration

Float

视频时长（秒），用于计费，按秒计费。

10.23

usage.video\_count

Integer

生成视频的数量。

1

usage.SR

Integer

生成视频分辨率档位。

480

usage.size

String

本次请求生成视频的分辨率

"size": "640\*480"

usage.fps

Integer

本次请求生成视频的帧率

"fps": 16

output.code

String

错误码。任务失败时返回此参数。

InvalidParameter

output.message

String

错误详情。任务失败时返回此参数。

The request is missing required parameters or in a wrong format

request\_id

String

本次请求的唯一ID。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id，将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**说明**task\_id 仅支持在**24小时内**查询任务结果，超时会被系统自动清除。

#### 响应示例

#### 成功响应

任务数据（如任务状态、视频URL等）仅保留24小时，超时后自动清除，请及时保存结果。

```
{
    "output": {
        "task_id": "bcae8761-f242-4775-a11e-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-09-01 09:37:27.468",
        "scheduled_time": "2025-09-01 09:37:34.885",
        "end_time": "2025-09-01 09:40:20.734",
        "results": {
            "video_url": "http://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/1d/xxx.mp4?Expires=xxxxxx"
        }
    },
    "usage": {
        "duration": 18.13,
        "size": "512*640",
        "fps": 16,
        "video_count": 1,
        "SR": 480
    },
    "request_id": "28cfedb1-cd60-9e0c-b920-xxxxxx"
}
```

#### 失败响应

```
{
    "request_id": "8d49f522-f6a4-9eed-b322-xxxxxx",
    "output": {
        "task_id": "101ad32f-7653-4ae9-8f22-xxxxxx",
        "task_status": "FAILED",
        "submit_time": "2025-09-01 11:43:41.174",
        "scheduled_time": "2025-09-01 11:43:48.937",
        "end_time": "2025-09-01 11:43:49.802",
        "code": "InvalidURL",
        "message": "Required URL is missing or invalid, please check the request URL."
    }
}
```

## 计费与限流

-   模型免费额度和计费单价请参见[万相-数字人](https://help.aliyun.com/zh/model-studio/model-pricing#6fa00e4db0qlz)。
    
-   模型限流请参见[万相系列](raw/model-user-guide/get-started-with-models/rate-limit.md)。
    
-   计费说明：
    
    -   输入不计费，输出计费。按成功生成的 视频秒数 计费。
    -   模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
