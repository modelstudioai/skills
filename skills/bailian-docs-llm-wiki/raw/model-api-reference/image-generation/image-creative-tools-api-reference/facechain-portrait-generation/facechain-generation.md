# 人物写真生成API详情

**重要**本文档仅适用于华北2（北京）地域。

## 人物写真生成

**说明**支持的领域 / 任务：aigc /facechain人物写真生成

人物写真2.0支持人物形象训练lora模式和人物形象免训练trainfree模式。

1）人物形象训练lora模式：基于人物形象训练模型已经得到的人物形象lora，可以继续通过人物生成写真模型完成该形象的高保真写真生成，支持多种预设风格，包括证件照、商务写真、复古风、夏日运动等风格，同时支持客户自定义风格模板上传方式生成自定义人物写真照。

2）人物形象免训练trainfree模式【推荐】：同时上传一组包含用户正脸单人照（至少一张）和客户自定义风格模板，通过人物生成写真模型直接一键免训练极速生成人物写真照，仅支持客户自定义风格模板上传方式免训练trainfree生成写真。

人物形象训练lora方式说明：

-   人物形象训练lora方式流程图：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792627.png)

人物形象训练lora方式上，人物写真基于扩散模型的图像生成能力，结合LoRA训练实现人像和风格融合，并叠加一系列后处理能力，实现兼具相似度、真实感、美观度的写真生成能力，人物写真可以实现高度个性化、高保真、高品质水位。

关于该接口功能的示例图如下：

-   输入图像

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792626.png)

-   生成结果（商务写真）

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792633.png)

-   预设风格模板

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792634.png)

-   客户自定义模板：
-   输入图像

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792631.png)

-   自定义模板

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792632.jpeg)

-   生成结果

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792630.jpeg)

人物形象免训练trainfree方式说明：

-   人物形象免训练trainfree方式流程图：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792624.png)

人物形象免训练trainfree方式上，基于内置强大的人物写真照预训练大模型技术，实现人物写真扩散模型的图像极速生成能力，一键免训练极速生成人物写真照，并叠加一系列后处理能力，实现兼具相似度、真实感、美观度的写真生成能力，人物写真可以实现高度个性化、高品质、高丰富度、极速出图能力。

关于该接口功能的示例图如下：

-   输入图像

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792625.jpeg)

-   自定义模板

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792629.jpeg)

-   生成结果

![image.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5751143171/p792628.jpeg)

## 应用场景

-   职场证件照制作：一键训练证件照人物形象风格，专为用户打造符合各类企业招聘、求职简历等场景的高质量、规范化的职场证件照，轻松完成高质量的职场证件照制作，节省时间、精力和成本。
-   AI写真照相馆应用：通过构建智能写真照相馆应用程序，为用户提供便捷、高效且高度个性化的在线摄影体验，让用户无论何时何地都能拍出媲美专业摄影师水准的高品质多样化风格个人写真照片。
-   环球旅拍写真生成：线上数字化创新旅拍写真生成应用，为用户提供仿佛亲身游历世界各地拍摄专业级旅行写真的体验。用户无需实际出行，即可在家中或任何地方轻松获得全球各地风景、著名景点下的精美个人写真照片。
-   商业人物写真创作：一键批量生成商业人物写真，对于商业人物、模特、网红或企业高管群体高质量的人物写真批量生成，可用于社交媒体展示、宣传资料、杂志封面等商业推广活动。

## 特色优势

-   高保真画质写真创作：人物写真融合后的人脸无违和感，写真生成效果自然，实现融合后的人脸面目表情、细节特征、肤色高度一致性，同时确保成像清晰度高、色彩还原准确，输出的人物写真照画质上乘。
-   个性化人物风格定制：人物写真拍摄可以高度个性化定制，支持场景选择、拍摄风格等不同模板风格。
-   人物形象生成设计：与传统摄影相比，AIGC技术无需实际拍摄过程，节省了时间成本和人力成本。它能够在短时间内生成大量不同风格的人物肖像，满足C端客户对多元化、快速化的需求响应。
-   人物写真训练人脸质量评估：判断真实上传人脸图片是否符合人物写真生成微调所需的标准，人脸数量、大小、角度、光照、清晰度等多维度质量评估检测。
-   稳定、易用平台服务：提供在高并发、大流量下的稳定写真图片生成响应和99.99%的可靠性保障，可直接调用的简单训练和推理API 接口，服务简单易用，易被集成，兼容性强。

## 模型概览

模型名

模型简介

facechain-generation

基于人物形象训练已经得到的形象，可以继续通过人物生成写真模型完成该形象的写真生成，支持多种预设风格，包括证件照、商务写真等。

## 输入限制

人物单人照输入限制：

-   图像格式：JPEG、JPG、PNG。
-   图像大小：不超过3MB。
-   图像分辨率：大于256×256像素，小于2048×2048像素，人脸占比不低于128×128像素。
-   URL地址中不能包含中文字符。
-   包含清晰正脸单人人物照，人脸角度不超过15度。
-   输入人物图像至少1张，最多5张，需要事先通过人物图像检测API（facechain-facedetect）判断符合要求。

客户自定义模板输入限制：

-   图像格式：JPEG、JPG、PNG。
-   图像大小：不超过5MB。
-   图像分辨率：大于512_512像素，小于1680_1260像素。
-   URL地址中不能包含中文字符。
-   单人的，清晰且高质量的风格模板图，人脸无遮挡和模糊。

## HTTP调用接口

### 功能描述

本模型需要相对较长的算法调用时间，所以在接口层面采用了异步调用的方式进行任务提交，在通过任务接口提交作业之后，系统会返回对应的作业ID，随后可以通过对应的异步作业查询接口获取任务的状态并且在作业到达最终完成态后取回对应的作业结果。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   已经通过人物形象训练API，完成定制形象的模型训练，并获取其相应的resource\_id。详情参考[人物形象训练API详情](raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-finetune-api.md)。

**说明**接口限制：对单账户（含主账号与RAM子账号）任务下发接口限制QPS为2，并发任务数量限制为1。

### 作业提交接口调用

POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/album/gen\_potrait

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

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

X-DashScope-Async

_String_

是

使用 enable，表明使用异步方式提交作业。

enable

Body

model

_String_

是

指明需要调用的模型，此处用facechain-generation

facechain-generation

resources\[list\]

_Array_

否

指明之前通过模型定制得到的 lora 层对应的数据。当进行非免训练生成时此参数为必选参数。

当进行免训练生成时，不需要填写此参数，且此参数的输入会被忽略。

"resources": \[

{

"resource\_id": "realistic\_v1\_12345",

"resource\_type": "facelora"

}

\]

resources\[0\].resource\_type

_String_

否

模型定制的相关数据类型，此处使用 facelora。当进行非免训练生成时为必选参数。

当进行免训练生成时，不需要填写此参数，且此参数的输入会被忽略。

resources\[0\].resource\_id

_String_

否

模型定制得到的 lora 层的数据 id，从模型定制的成功任务的 finetuned\_output 处获取；比如facechain-png-ft-202308291948-edc2。当进行非免训练生成时为必选参数。

当进行免训练生成时，不需要填写此参数，且此参数的输入会被忽略。

parameters.style

_String_

否

选择输出图像的预设风格或者选择自定义模板模式以及自定义模板免训练模式

预设风格：

目前支持以下预设风格：

f\_idcard\_male（证件照男） f\_business\_male（商务写真男） f\_idcard\_female（证件照女）

f\_business\_female（商务写真女）

m\_springflower\_female（春日花园）

f\_summersport\_female（夏日运动）

f\_autumnleaf\_female（秋日印象）

m\_winterchinese\_female（冬日国风）

f\_hongkongvintage\_female（港风复古）

f\_lightportray\_female（轻写真）

自定义模板写真生成：

portrait\_url\_template

自定义模板免训练写真生成：

train\_free\_portrait\_url\_template

"style": "f\_business\_female"

parameters.size

_String_

否

生成图像的分辨率，目前支持 '768\*1024'

自定义模板模式以及自定义模板免训练模式时，不需要该参数。

"parameters": {

"size": "768\*1024",

"n": 4,

"skin\_retouch": true

}

parameters.n

_Integer_

否

图片生成的数量，目前支持 1~5 张，默认值 4。

parameters.skin\_retouch

_Bool_

否

免训练写真生成时是否对输入用户图进行自动美颜处理。默认为'true'，进行自动美颜；可设置为'false'，不进行自动美颜，用户可以自己进行美颜前后处理。

input.template\_url

_String_

否

当parameters.stytle为"portrait\_url\_template"和"train\_free\_portrait\_url\_template"时，需要由用户上传自定义模板进行写真生成。此时该参数为必选参数，传入用户自定义模板的url链接。

template\_url: "[](http://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-left3.png)[http://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-left3.png](http://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-left3.png)"

input.user\_urls

_Array_

否

当parameters.stytle为"train\_free\_portrait\_url\_template"时，表示进行用户自定义模板的免训练写真生成，此时该参数为必选参数，传入一组包含用户正脸单人照的url链接。至少1张最多5张，且是通过人物图像检测API（facechain-facedetect）验证通过的人物图像。

user\_urls:\[ "[](http://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-right1.png)[http://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-right1.png](http://viapi-test.oss-cn-shanghai.aliyuncs.com/viapi-3.0domepic/facebody/CompareFace/CompareFace-right1.png)"\]

### 出参描述

**字段**

**类型**

**描述**

**示例值**

output.task\_id

_String_

提交异步任务的作业 id，实际作业结果需要通过异步任务查询接口获取。

xxxxxxxxx

output.task\_status

_String_

提交异步任务后的 作业状态。

“PENDING”

request\_id

_String_

本次请求的系统唯一码

7574ee8f-38a3-4b1e-9280-11c33ab46e51

### 请求示例

以下示例展示通过CURL命令来调用本模型的脚本。

**说明**需要使用您的API-KEY替换示例中的_your-dashscope-api-key_，代码才能正常运行。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/album/gen_potrait' \
--header 'X-DashScope-Async: enable' \
--header 'Authorization: Bearer <your-dashscope-api-key>' \
--header 'Content-Type: application/json' \
--data '{
"model": "facechain-generation",
"parameters": {
"style": "f_idcard_female",
"size": "768*1024",
"n":4
},
"resources": [
{
"resource_id": "women_model",
"resource_type": "facelora"
}
]
}'
```

以下示例展示通过CURL命令来调用本模型进行用户自定义模板写真生成的脚本。

**说明**需要使用您的API-KEY替换示例中的_your-dashscope-api-key_，用实际用户指定模板图片对应的url链接地址代替template\_pic\_url，代码才能正常运行。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/album/gen_potrait' \
--header 'X-DashScope-Async: enable' \
--header 'Authorization: Bearer <your-dashscope-api-key>' \
--header 'Content-Type: application/json' \
--data '{
"model": "facechain-generation",
"parameters": {
"style": "portrait_url_template",
"n":1
},
"input":
{
"template_url": "<template_pic_url>"
},
"resources": [
{
"resource_id": "women_model",
"resource_type": "facelora"
}
]
}'
```

以下示例展示通过CURL命令来调用本模型进行用户自定义模板免训练写真生成的脚本。

**说明**需要使用您的API-KEY替换示例中的_your-dashscope-api-key_，用实际用户指定模板图片对应的url链接地址代替template\_pic\_url，用包含用户正面人脸单人图片对应的url链接地址代替user\_pic\_url，代码才能正常运行。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/album/gen_potrait' \
--header 'Authorization: Bearer <your-dashscope-api-key>' \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--data '{
    "model": "facechain-generation",
    "parameters":
    {
        "style": "train_free_portrait_url_template",
        "n": 1
    },
    "input":
    {
      "template_url": "<template_pic_url>",
      "user_urls": ["<user_pic_url>"]
    }
}'
```

### 响应示例

```
{
  "request_id": "0b6a411a-56e6-9028-84eb-6852183248d8",
  "output": {
    "task_id": "7eb1032e-09a1-4df5-96ed-14091859ad57",
    "task_status": "SUCCEEDED",
    "submit_time": "2025-08-15 10:20:22.629",
    "scheduled_time": "2025-08-15 10:20:22.655",
    "end_time": "2025-08-15 10:20:50.540",
    "results": [
      {
        "url": "https://example.com/image1.jpg"
      },
      {
        "url": "https://example.com/image2.jpg"
      },
      {
        "url": "https://example.com/image3.jpg"
      },
      {
        "url": "https://example.com/image4.jpg"
      }
    ],
    "task_metrics": {
      "TOTAL": 4,
      "SUCCEEDED": 4,
      "FAILED": 0
    }
  },
  "usage": {
    "image_count": 4
  }
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

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

### 入参描述

**传参方式**

**字段**

**类型**

**必选**

**描述**

**示例值**

Url Path

task\_id

_String_

是

需要查询作业的 task\_id

13b1848b-5493-4c0e-8c44-68d038b492af

Header

Authorization

_String_

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

本次请求的异步任务的作业 id，实际作业结果需要通过异步任务查询接口获取。

13b1848b-5493-4c0e-8c44-68d038b492af

output.task\_status

_String_

被查询作业的作业状态

任务状态：

PENDING 排队中

RUNNING 处理中

SUCCEEDED 成功

FAILED 失败

UNKNOWN 作业不存在或状态未知

output.result\_url

_String_

如果作业成功，包含模型生成的结果图像的 URL，可以在 24 小时之内随时下载。

输出图像分辨率为768\*1024

"result\_url": "[](http://oss.aliyuncs.com/xxx/abc.jpg)[http://oss.aliyuncs.com/xxx/abc.jpg](http://oss.aliyuncs.com/xxx/abc.jpg)"

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
--header 'Authorization: Bearer <your-dashscope-api-key>' \
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-af6e-a0c6a421c010
```

### 响应示例（作业执行中）

作业提交后将处于排队状态，在得到调度之后将转为运行状态，此时作业的状态为RUNNING，task\_metrics将给出具体batch状态；

```
{
    "request_id":"e5d70b02-ebd3-98ce-9fe8-759d7d7b107d",
    "output":{
        "task_id":"86ecf553-d340-4e21-af6e-a0c6a421c010",
        "task_status":"RUNNING",
        "task_metrics":{
            "TOTAL":1,
            "SUCCEEDED":1,
            "FAILED":0
        }
    }
}
```

### 响应示例（作业成功执行完毕）

如果作业执行完成并成功之后，再次查询作业状态，接口将在告知作业状态的同时，一并将作业的结果返回。对于本模型，作业在结束之后的状态会持续保留24小时以备客户随时查询，24小时之后，作业将从系统中清除，相关的结果也将一并清除；对应的，作业生成的结果为图像的URL地址，出于安全考虑，该URL的下载有效期也是24小时，需要用户在获取作业结果后根据需要及时使用或者转存。

```
{
  "request_id": "<your request id>",
  "output": {
    "task_id": "<your task id>",
    "task_status": "SUCCEEDED",
    "submit_time": "xxx",
    "scheduled_time": "xxx",
    "end_time": "xxx",
    "results": [
      {"url": "http://oss.aliyuncs.com/xxx/abc1.jpg"},
      {"url": "http://oss.aliyuncs.com/xxx/abc2.jpg"},
      {"url": "http://oss.aliyuncs.com/xxx/abc3.jpg"},
      {"url": "http://oss.aliyuncs.com/xxx/abc4.jpg"}
    ],
    "task_metrics": {
      "TOTAL": 4,
      "SUCCEEDED": 4,
      "FAILED": 0
    }
  },
  "usage": {
    "image_count": 4
  }
}
```

### 响应示例（作业失败）

如果因为某种原因作业失败，则作业状态会设置为FAILED，并且通过code和message字段指明错误原因。

```
{
  "request_id": "<your request id>",
  "output": {
    "task_id": "<your task id>",
    "task_status": "FAILED",
    "submit_time": "xxx",
    "scheduled_time": "xxx",
    "end_time": "xxx",
    "code": "InvalidImageResolution",
    "message": "The input image resolution is too large or small"
  },
  "usage": {
    "image_num": 0
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

**400**

**InvalidURL**

The request URL is invalid, make sure the url is correct and is an image

输入url错误，请确保url链接的正确性

**400**

**InvalidImageResolution**

The input image resolution is too large or small

输入图像分辨率过大或过小

**500**

**InternalError:Algo**

An internal error occurs during computation, please try this model later

算法内部错误，请稍后重试

**500**

**InternalError:Algo**

Inference error: Inference error

请检查输入的图片文件是否有损坏或检查人物图片的质量（需包含完整清晰的人脸）

**400**

**InvalidParameter.DataInspection**

Don't have authorization to access the media resource during the data inspection process.

数据安全审查过程中无法访问媒体资源

**403**

**Resource.AccessDenied**

Resource {resource\_id} access denied.

指定的资源无访问权限，请检查resource\_id是否正确

**400**

**BadRequest.EmptyModel**

Required parameter "model" missing from request.

请求中缺少必选参数model

## 常见问题

**调用人物写真接口报错**`"code": "InternalError.Algo","message": "Inference error: Inference error"`**？**

-   处理建议1：请检查输入的图片文件是否有损坏。
-   处理建议2：检查人物图片的质量（需包含完整清晰的人脸）。
