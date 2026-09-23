# AnimateAnyone 视频生成API参考

AnimateAnyone模型，可基于AnimateAnyone-template模型生成的动作模板，以及通过AnimateAnyone-detect模型检测的人物图像生成人物动作视频。本文档介绍了该模型提供的视频生成能力的API调用方法。

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 模型概览

#### 模型简介

模型名

模型简介

animate-anyone-gen2

animate-anyone-gen2是一个人物动作视频生成模型，可基于人物图片和人物动作模板生成人物动作视频。

#### 模型效果示例

**人物图片**

**动作模板**

**输出（按图片背景生成）**

**输出（按视频背景生成）**

![05-9\_16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5770383371/p885845.png)

![04-9\_16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9239161571/p885846.png)

**说明**

-   以上示例，由集成了“舞动人像AnimateAnyone”的千问APP生成。
-   动作模板需先通过[AnimateAnyone 动作模板生成API](raw/_short/animate-anyone-template-api-e8864f515e08488f.md)制作，请确保动作模板视频的来源符合相关法律法规，且已获得该视频内容（包含音频）的使用许可。

## HTTP调用接口

### 功能描述

用于生成人物动作视频。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   输入的动作模板由[AnimateAnyone 动作模板生成API](raw/_short/animate-anyone-template-api-e8864f515e08488f.md)生成；
-   输入的图像已通过[AnimateAnyone 图像检测API](raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)检测。

### 输入限制

-   图像格式：格式为jpg、png、jpeg、bmp。
    
-   图像要求：图像文件＜5M，宽高比≤2，最大边长≤4096像素。
    
-   上传的图像文件支持HTTP链接，不支持本地路径。也可使用平台提供的[临时存储空间](raw/model-api-reference/more-about-models/get-temporary-file-url.md)，上传本地文件并创建链接。
    
-   输入图像与视频生成类型的适用关系：
    
    **输入图片**
    
    **按图片背景生成**
    
    **（即use\_ref\_img\_bg设为true）**
    
    **按视频背景生成**
    
    **（即use\_ref\_img\_bg设为false）**
    
    全身人像
    
    支持
    
    支持
    
    半身人像
    
    支持
    
    **不推荐**
    
    **说明**按视频背景生成时，需将图片中人像匹配到视频中人像的对应位置。对于半身人像图中未出现的区域（如腿部），模型将随机生成补全，有较大不确定性，故不推荐在该条件下做视频生成。
    

### 步骤1：创建任务获取任务ID

```
POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis
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

使用 enable，表明使用异步方式提交任务。

enable

model

String

Body

是

指明需要调用的模型。

animate-anyone-gen2

input.image\_url

String

Body

是

用户上传的图片 URL，该图应先通过[AnimateAnyone 图像检测API](raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)，并结合所需生成的画幅进行适当裁剪。

-   图像文件＜5M，宽高比≤2，最大边长≤4096
-   格式支持jpg、png、jpeg、bmp。

**说明**上传文件支持HTTP或HTTPS链接方式，不支持本地链接方式。您也可在此[获取临时公网URL](raw/model-api-reference/more-about-models/get-temporary-file-url.md)。

[http://aaa/bbb.jpg](http://aaa/bbb.jpg)

input.template\_id

String

Body

是

动作模板ID，用于指明所需使用的动作模板。应输入[AnimateAnyone 动作模板生成API](raw/_short/animate-anyone-template-api-e8864f515e08488f.md)生成的template\_id。

**说明**动作模板ID会进行权限校验，请确保所使用的template\_id是由当前的云账号创建得到的。

> 使用建议：提高模板视频的分辨率和帧率，可有效提升生成视频的画质效果。

AACT.xxx.xxx-xxx.xxx

parameters.use\_ref\_img\_bg

Boolean

Body

否

生成视频的背景控制，可设值为true或false。

-   设true时将以输入图片的画面为背景生成视频。
-   设false时将以模板文件的原视频画面为背景生成视频。默认值为false。

false

parameters.video\_ratio

String

Body

否

选择按图片背景生成视频时，可选画幅为 "9:16"或"3:4"，默认为"9:16"。

**说明**选择按视频背景生成时，即use\_ref\_img\_bg设false时，该参数不生效。将按模板视频的比例生成新视频。

**说明**应确保输入图像的画幅与所选画幅一致，以避免生成视频的画面变形

"9:16"

#### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

提交异步任务的任务ID，实际任务结果需要通过异步任务查询接口获取。

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

String

提交异步任务后的任务状态。

“PENDING”

request\_id

String

本次请求的系统唯一码。

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

#### curl

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "animate-anyone-gen2",
    "input": {
        "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251224/pkswoc/p883941.png",
        "template_id": "AACT.xxx.xxx-xxx.xxx"
    },
    "parameters": {
        "use_ref_img_bg": false,
        "video_ratio": "9:16"
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
                                model='animate-anyone-gen2',
                                img_url='https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251224/pkswoc/p883941.png',
                                template_id='AACT.xxx.xxx-xxx.xxx',
                                use_ref_img_bg=False,
                                video_ratio='9:16')
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
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-xxxxxx"
}
```

### 步骤2：根据任务ID查询结果

```
GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}
```

**说明**

-   异步任务查询接口提供 20 QPS 的访问流量限制。若有更高频次的查询需求，可通过EventBridge配置事件转发，详见[EventBridge配置事件转发](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。
-   已提交的异步任务列表查询和异步任务的取消管理，详见[管理异步任务](raw/model-api-reference/more-about-models/manage-asynchronous-tasks.md)。

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

-   PENDING 排队中
    
-   PRE-PROCESSING 前置处理中
    
-   RUNNING 处理中
    
-   POST-PROCESSING 后置处理中
    
-   SUCCEEDED 成功
    
-   FAILED 失败
    
-   UNKNOWN 任务不存在或状态未知
    

output.video\_url

String

平台输出的视频结果，**video\_url有效期为任务完成后24小时**

[https://xxx/1.mp4](https://xxx/1.mp4)"

usage.video\_duration

Float

本次请求生成视频时长计量，单位：秒

"video\_duration": 10.23

usage.video\_ratio

String

本次请求生成视频的画幅类型，该值为standard

"video\_ratio": "standard"

request\_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

#### 请求示例

```
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### 响应示例

```
{
    "request_id": "7574ee8f-38a3-4b1e-9280-xxxxxx",
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://xxx/1.mp4"
    },
    "usage": {
        "video_duration": 10.23,
        "video_ratio": "standard"
    }
}
```

#### 异常响应示例

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
