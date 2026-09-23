# LivePortrait 视频生成API参考

LivePortrait模型，可基于通过LivePortrait-detect模型检测的人物肖像图片和人声音频文件，快速、轻量化地生成人像动态视频。本文档介绍了该模型提供的视频生成能力的API调用方法。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

**模型名**

**模型简介**

liveportrait

liveportrait是一个人物视频生成模型，可基于人物肖像图片和人声音频文件，快速、轻量化地生成人物肖像动态视频。

## HTTP调用接口

### 功能描述

用于生成人物肖像动态视频。

### 前提条件

-   已开通阿里云百炼服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   输入图像已通过[LivePortrait 图像检测](raw/_short/liveportrait-detect-api-21701ab5bd145794.md)检测。

### 输入限制

-   图像格式：格式为jpeg、jpg、png、bmp、webp。
-   图像分辨率：图像文件<10M，宽高比≤2，最大边长≤4096像素。
-   音频格式：格式为wav、mp3。
-   音频限制：文件＜15M，1s＜时长＜3min。
-   音频内容：音频中需包含清晰、响亮的人声语音，并去除了环境噪音、背景音乐等声音干扰信息。
-   上传图片、音频链接仅支持HTTP链接方式，不支持本地链接方式。

### 作业提交接口

```
POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis
```

**说明**

-   因该算法调用耗时较长，故采用异步调用的方式提交任务。
-   任务提交之后，系统会返回对应的作业ID，后续可通过“作业任务状态查询和结果获取接口”获取任务状态及对应结果。

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

API-Key，例如：Bearer d1\*\*2a。

Bearer d1\*\*2a

X-DashScope-Async

String

Header

是

使用enable，表明使用异步方式提交作业。

enable

model

String

Body

是

指明需要调用的模型，此处用liveportrait。

liveportrait

input.image\_url

String

Body

是

用户上传的图片 URL，该图应先通过[LivePortrait图像检测API](raw/_short/liveportrait-detect-api-21701ab5bd145794.md)。

-   图像文件<10M，宽高比≤2，最大边长≤4096。
    
-   格式支持：jpeg、jpg、png、bmp、webp。
    

上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

"image\_url": "[http://a/a.jpg](http://a/a.jpg)"

input.audio\_url

String

Body

是

用户上传的音频文件 URL。

-   音频文件＜15M，1s＜时长＜3min。
    
-   格式支持：wav、mp3。
    

上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

http://aaa/bbb.wav

parameters.template\_id

String

Body

否

可按模板控制人物头部的运动姿态和幅度，当前支持3种模板：normal、calm、active。默认为normal。

"normal"

parameters.eye\_move\_freq

Float

Body

否

每秒眨眼次数，可设值为0-1，值越大眨眼频率越高。默认值为0.5。

0.5

parameters.video\_fps

Integer

Body

否

输出视频帧率，可设值为15-30。默认值为24。

24

parameters.mouth\_move\_strength

Float

Body

否

嘴部动作的幅度大小，可设值为0-1.5，值越大嘴型越大。若设为0则嘴部无动作。默认值为1。

1

parameters.paste\_back

Boolean

Body

否

生成的人脸是否贴回原图，可设值为true或false。若设为false则仅输出生成的人脸，忽略人物身体。默认值为true。

true

parameters.head\_move\_strength

Float

Body

否

头部动作幅度，可设值为0-1，值越大头部动作幅度越大。默认值为0.7。

0.7

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

提交异步任务的作业id，实际作业结果需要通过异步任务查询接口获取。

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

提交异步任务后的作业状态。

“PENDING”

request\_id

String

本次请求的系统唯一码。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 可选用的动作模板

**template\_id**

**效果说明**

normal

默认动作模板，头部动作幅度适中。适用于多种场景。

calm

人物表现平静，头部动作幅度较小。推荐用于播报等场景。

active

人物表现活泼，头部动作幅度较大。推荐用于演唱等场景。

#### 请求示例

#### curl

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "liveportrait",
    "input": {
        "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/ynhjrg/p874909.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251226/fwnqyq/liveportrait_boy.mp3"
    },
      "parameters": {
         "template_id": "normal",
         "eye_move_freq": 0.5,
         "video_fps":30,
         "mouth_move_strength":1,
         "paste_back": true,
         "head_move_strength":0.7
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
                                model='liveportrait',
                                img_url='https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/ynhjrg/p874909.png',
                                audio_url='https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251226/fwnqyq/liveportrait_boy.mp3',
                                template_id='normal',
                                eye_move_freq=0.5,
                                video_fps=30,
                                mouth_move_strength=1,
                                paste_back=True,
                                head_move_strength=0.7)
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
	"task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "PENDING"
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
```

### 作业任务状态查询和结果获取接口

```
GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}
```

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

API-Key，例如：Bearer d1\*\*2a。

Bearer d1\*\*2a

task\_id

String

Url Path

是

需要查询作业的 task\_id。

a8532587-fa8c-4ef8-82be-0c46b17950d1

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

查询作业的 task\_id。

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

被查询作业的作业状态。

任务状态：

PENDING 排队中

RUNNING 处理中

SUCCEEDED 成功

FAILED 失败

UNKNOWN 作业不存在或状态未知

output.results.video\_url

String

如果作业成功，包含模型生成的结果 object，然后每个 object 中包含按照要求生成的结果地址。**video\_url有效期为作业完成后24小时**。

https://xxx/1.mp4

usage.video\_duration

Float

本次请求生成视频时长计量，单位：秒。

10.23

usage.video\_ratio

String

本次请求生成视频的画幅类型，该值为standard。

"video\_ratio": "standard"

request\_id

String

本次请求的系统唯一码。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的task\_id。

```
curl -X GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### 响应示例（作业成功执行完毕）

```
{
    "request_id": "b64e9c68-3923-462d-b25a-xxxxxx",
    "output": {
        "task_id": "a1c69ca5-810b-49ae-8b20-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-12-26 11:33:03.146",
        "scheduled_time": "2025-12-26 11:33:13.312",
        "end_time": "2025-12-26 11:33:22.455",
        "results": {
            "video_url": "http://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxx"
        }
    },
    "usage": {
        "video_duration": 2.79,
        "video_ratio": "standard"
    }
}
```

#### 响应示例（作业失败）

```
{
    "request_id": "7574ee8f-38a3-4b1e-9280-xxxxxx",
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-xxxxxx",
        "task_status": "FAILED",
        "code": "xxx",
        "message": "xxxxxx"
    }
}
```

## 状态码说明

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)。
