# 文字变形API详情

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 文字变形

**说明**支持的领域 / 任务：aigc /创意文字生成

WordArt锦书-文字变形可以对输入的文字边缘轮廓进行创意变形，根据提示词内容进行边缘变化，实现一种字体的更多种创意用法，返回带有文字内容的黑底白色蒙版图。

#### 输入内容&效果示意

输入文字 (input.text) ：桂林山水

描述提示词 (input.prompt) ：山峦叠嶂、漓江蜿蜒、岩石奇秀

返回结果：

![20231117173455.jpg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2179320071/p739205.jpg)

## 模型概览

模型名

模型简介

wordart-semantic

WordArt锦书-文字变形可以对输入的文字边缘轮廓进行创意变形，根据提示词内容进行边缘变化，实现一种字体的更多种创意用法，返回带有文字内容的黑底白色mask图。

## HTTP调用接口

### 功能描述

本模型需要相对较长的算法调用时间，所以在接口层面采用了异步调用的方式进行任务提交，在通过任务接口提交作业之后，系统会返回对应的作业ID，随后可以通过对应的异步作业查询接口获取任务的状态并且在作业到达最终完成态后取回对应的作业结果。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

### 作业提交接口调用

POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/wordart/semantic

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

### 入参描述

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Header

Content-Type

_String_

是

请求类型：application/json

application/json

Authorization

_String_

是

API-Key，例如：Bearer d1\*\*2a

Bearer d1\*\*2a

X-DashScope-WorkSpace

_String_

否

指明本次调用需要使用的workspace；需要注意的是，对于子账号Apikey调用，此参数为必选项，子账号必须归属于某个workspace才能调用；对于主账号Apikey此项为可选项，添加则使用对应的workspace身份，不添加则使用主账号身份。

ws\_QTggmeAxxxxx

X-DashScope-Async

_String_

是

固定使用 enable，表明使用异步方式提交作业。

enable

Body

model

_String_

是

指明需要调用的模型，固定值

wordart-semantic

input.text

_String_

否

用户输入的文字内容；

"text": "文字创意"

input.prompt

_String_

是

用户输入的文字内容；1-200 个字

"prompt": "春暖花开"

parameters.steps

_Integer_

否

变形迭代次数，数字越大文字变化程度越大

取值范围\[10, 100\]，默认30

60

parameters.n

_Integer_

是

生成的图片数量，默认为 4，取值范围为\[1, 4\]

2

parameters.font\_name

_String_

否

指定需要使用的字体类型。不带该参数则使用默认字体，默认字体为方正楷体

可选预设字体范围：

'dongfangdakai'：阿里妈妈东方大楷

'puhuiti\_m'：阿里巴巴普惠体

'shuheiti'：阿里妈妈数黑体

'jinbuti'：钉钉进步体

'kuheiti'：站酷酷黑体

'kuaileti'：站酷快乐体

'wenyiti'：站酷文艺体

'logoti'：站酷小薇LOGO体

'cangeryuyangti\_m'：站酷仓耳渔阳体

'siyuansongti\_b'：思源宋体

'siyuanheiti\_m'：思源黑体

'fangzhengkaiti'：方正楷体

"font\_name": "dongfangdakai"

parameters.ttf\_url

_String_

否

用户传入的ttf文件；

标准的ttf文件，文件大小小于30M；

与input.text.font\_name不能同时使用

"ttf\_url":"[https://xxxxx](https://xxxxx)"

parameters.output\_image\_ratio

_String_

否

图像比例，可选参数为：{"1280x720", "720x1280", "1024x1024"}，默认"1280x720"

"1280x720"

### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

String

本次请求的异步任务的作业 id，实际作业结果需要通过异步任务查询接口获取。

13b1848b-5493-4c0e-8c44-68d038b492af

output.task\_status

String

提交异步任务后的作业状态。

PENDING

request\_id

String

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

### 请求示例

以下示例展示通过CURL命令来调用本模型的脚本

**说明**需要使用您的API-KEY替换示例中的_your-dashscope-api-key_，代码才能正常运行。

```
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/wordart/semantic' \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Authorization: Bearer  <YOUR-DASHSCOPE-API-KEY>' \
--data-raw '{
    "model": "wordart-semantic",
    "input": {
        "text": "文字创意",
        "prompt": "水果，蔬菜，温暖的色彩空间"
    },
    "parameters": {
        "steps": 80,
        "n": 2,
        "output_image_ratio": "1024x1024",
        "font_name": "dongfangdakai"
    }
}'
```

### 响应示例

```
{
    "output": {
	"task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "PENDING"
    },
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51"
}
```

### 异常响应示例

在提交作业请求出错的情况下，输出的结果中会通过 code 和 message 指明出错原因。

```
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1"
}
```

### 作业任务状态查询和结果获取接口

GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task\_id}

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

### 入参描述

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Url Path

task\_id

String

是

需要查询作业的 task\_id

13b1848b-5493-4c0e-8c44-68d038b492af

Header

Authorization

String

是

API-Key，例如：Bearer d1\*\*2a

Bearer d1\*\*2a

### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

_String_

查询作业的 task\_id

a8532587-fa8c-4ef8-82be-0c46b17950d1

output.task\_status

_String_

被查询作业的作业状态

任务状态：

PENDING 排队中

RUNNING 处理中

SUCCEEDED 成功

FAILED 失败

UNKNOWN 作业不存在或状态未知

output.results

_Array_

如果作业成功，包含模型生成的结果 object，然后每个 object 中包含按照要求生成的结果地址

\[ {"png\_url":"[https://xxx/1.png](https://xxx/1.png)"},

{"svg\_url":"[https://xxx/1.svg](https://xxx/1.svg)"} \]

usage.image\_count

_Int_

本次请求生成图像计量

"image\_count": 1

request\_id

_String_

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

### 请求示例

以下示例展示通过CURL命令来调用本模型的脚本

**说明**需要使用您的API-KEY替换示例中的_your-dashscope-api-key_，代码才能正常运行。

```
curl -X GET \
--header 'Authorization: Bearer <YOUR-DASHSCOPE-API-KEY>' \
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-af6e-a0c6a421c010
```

### 响应示例（作业执行中）

作业提交后将处于排队状态，在得到调度之后将转为运行状态，此时作业的状态为RUNNING，task\_metrics将给出具体batch状态；

```
{
    "request_id": "e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output": {
        "task_id": "86ecf553-d340-4e21-af6e-a0c6a421c010",
        "task_status": "RUNNING",
        "submit_time": "2025-12-05 13:22:10.653",
        "scheduled_time": "2025-12-05 13:22:10.680"
    }
}
```

### 响应示例（作业成功执行完毕）

如果作业执行完成并成功之后，再次查询作业状态，接口将在告知作业状态的同时，一并将作业的结果返回。对于本模型，作业在结束之后的状态会持续保留24小时以备客户随时查询，24小时之后，作业将从系统中清除，相关的结果也将一并清除；对应的，作业生成的结果为图像的URL地址，出于安全考虑，该URL的下载有效期也是24小时，需要用户在获取作业结果后根据需要及时使用或者转存。

```
{
    "request_id": "7574ee8f-38a3-4b1e-9280-11c33ab46e51",
    "output": {
        "task_id": "a8532587-fa8c-4ef8-82be-0c46b17950d1",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-12-05 13:20:54.787",
        "scheduled_time": "2025-12-05 13:20:59.841",
        "end_time": "2025-12-05 13:21:21.489",
        "results": [
            {
                "png_url": "https://xxx/1.png",
                "svg_url": "https://xxx/1.svg"
            }
        ],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

### 响应示例（作业失败）

如果因为某种原因作业失败，则作业状态会设置为FAILED，并且通过code和message字段指明错误原因。

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

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)

同时本模型还有如下特定错误码：

http 返回码\*

错误码（code）

错误信息（message）

含义说明

**400**

**InvalidParameter**

The request is missing required parameters or the parameters are out of the specified range, please check the parameters that you send

缺少必要的接口调用参数或参数越界
