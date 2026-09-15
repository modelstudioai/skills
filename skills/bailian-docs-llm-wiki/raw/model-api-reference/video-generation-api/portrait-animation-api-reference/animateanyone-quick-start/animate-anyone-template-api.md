# AnimateAnyone动作模板生成API参考

AnimateAnyone动作模板生成模型，可基于人物运动视频提取人物动作，并生成可供AnimateAnyone视频生成模型使用的人物动作模板。本文档介绍了该模型提供的动作模板生成能力的API调用方法。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

**模型名**

**模型简介**

animate-anyone-template-gen2

animate-anyone-template-gen2是一个人物动作模板生成模型，可基于人物运动视频提取人物动作并制作模板。

## 模型输入要求

#### 正确示例：

**符合动作模板制作要求的视频示例**

**说明**

-   上传的视频中人物应全身入镜、身体无遮挡、保持人脸清晰。
-   人物应从画面首帧开始出现，动作连贯，一镜到底（有场景切换的视频建议拆分成多段）。
-   建议：画面首帧人物正面朝向镜头；避免人物运动中出现大幅弯腰、下蹲、身体蜷缩等动作。

#### 错误示例：

**身体蜷缩、遮挡**

**画面有多人**

**人物模糊**

**人物过小**

**（人脸不清晰）**

**人物过大**

**（人物不完整）**

![身体遮挡@3x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0759193371/p886350.png)

![多人物@3x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0759193371/p886352.png)

![f3e2df6643d44db7a7d65d4571609bff\_3 (1)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0759193371/p886586.png)

![人物过小@3x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0759193371/p886354.png)

![人物过大@3x](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0759193371/p886570.png)

**说明**

-   为保障模板制作效果，应避免上传视频中的任一帧画面出现上述错误情形。
-   当**视频首帧画面**出现上述错误情形时，当次提交的任务可能报错并中止。

**重要**

-   请确保上传的视频文件来源符合相关法律法规。
-   生成的动作模板的音频，与上传的视频文件中的音频一致。若不希望使用该音频，或尚未取得该音频（如音乐等）的使用许可，请在上传视频文件前，消除其中的音频信息。

## HTTP调用接口

### 功能描述

用于生成人物动作模板，该模板可作[AnimateAnyone 视频生成 API](raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animateanyone-video-generation-api.md)的输入物，以生成人物动作视频。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

### 输入限制

-   视频格式：支持mp4、avi、mov。
-   视频文件不大于200MB。
-   视频边长不低于200，不大于2048；视频帧率≥24fps，视频编码采用H.264或H.265。
-   视频时长不小于2s且不大于60s。
-   视频长宽比介于1:3到3:1。
-   上传的视频文件支持HTTP链接，不支持本地路径。也可使用平台提供的[文件存储API](https://help.aliyun.com/zh/model-studio/data-connection)，上传本地文件并创建链接。

### 步骤1：创建任务获取任务ID

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/aa-template-generation
```

**说明**

-   因该算法调用耗时较长，故采用异步调用的方式提交任务。
-   任务提交之后，系统会返回对应的任务ID，后续可通过“根据任务ID查询结果接口”获取任务状态及对应结果。

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

请求类型：application/json

application/json

Authorization

String

Header

是

API-Key，例如：Bearer d1\*\*2a

Bearer d1\*\*2a

X-DashScope-Async

String

Header

是

使用 enable，表明使用异步方式提交任务。

enable

model

String

Body

是

指明需要调用的模型，此处用animate-anyone-template-gen2

animate-anyone-template-gen2

input.video\_url

String

Body

否

用户上传的视频 URL，用于生成基于指定视频的动作模板。

-   视频文件不大于200MB
    
-   视频边长不低于200，不大于2048
    
-   视频帧率≥24fps，视频编码采用H.264或H.265
    
-   视频时长不小于2s且不大于60s
    
-   视频长宽比介于1:3到3:1
    
-   视频格式支持：mp4、avi、mov
    

上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

http://aaa/bbb.mp4

#### 出参描述：

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

提交异步任务的任务 id，实际任务结果需要通过异步任务查询接口获取

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

提交异步任务后的 任务状态

“PENDING”

request\_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2video/aa-template-generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "animate-anyone-template-gen2",
    "input": {
        "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241210/cwjmsz/1.mp4"
    }
  }'
```

#### 响应示例

```
{
    "output": {
	"task_id": "a8532587-fa8c-4ef8-82be-xxxxxx",
        "task_status": "PENDING"
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-xxxxxx"
}
```

### 步骤2：根据任务ID查询结果

```
GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}
```

**说明**

-   异步任务查询接口提供 20 QPS 的访问流量限制。若有更高频次的查询需求，可通过EventBridge配置事件转发，详见[EventBridge配置事件转发](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
-   已提交的异步任务列表查询，及异步任务的取消管理，详见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

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

需要查询任务的task\_id。

a8532587-fa8c-4ef8-82be-0c46b17950d1

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

查询任务的 task\_id

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

被查询任务的任务状态

任务状态：

PENDING 排队中

RUNNING 处理中

SUCCEEDED 成功

FAILED 失败

UNKNOWN 任务不存在或状态未知

output.template\_id

String

平台输出的动作模板ID，可作为“Animate-Anyone 视频生成接口”的入参。

动作模板ID会进行权限校验，请确保使用template\_id的云账号与当前生产该动作模板的云账号一致。

AACT.xxx.xxx-xxx.xxx

usage.video\_duration

Float

本次请求生成模板时长计量，单位：秒

"video\_duration": 10.23

usage.video\_ratio

String

本次请求生成视频模板的画幅类型，该值为standard

"video\_ratio": "standard"

request\_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

```
curl -X GET \
--header 'Authorization: Bearer <YOUR_API_KEY>' \
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/<YOUR_TASK_ID>
```

#### 响应示例

```
{
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51",
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "SUCCEEDED",
        "template_id": "AACT.xxx.xxx-xxx.xxx"
    },
    "usage": {
        "video_duration": 10.23,
        "video_ratio": "standard"
    }
}
```

##### 异常响应示例

```
{
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51",
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "FAILED",
        "code": "xxx",
        "message": "xxxxxx"
    }
}
```

## 状态码说明

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)。
