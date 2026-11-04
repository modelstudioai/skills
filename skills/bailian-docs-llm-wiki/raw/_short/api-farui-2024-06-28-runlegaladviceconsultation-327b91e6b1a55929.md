# RunLegalAdviceConsultation - 法律咨询

法律咨询。

## 接口说明

请确保在使用该接口前，已充分了解法睿产品的收费方式和[价格](https://help.aliyun.com/zh/model-studio/user-guide/billing-for-tongyi-farui-1)。

-   该接口需要开通法睿商品相关的后付费服务（开通免费），可以使用该账号的 AccessKey 和 AccessSecret 来调用我们的 OpenApi 服务
-   服务的响应结果是以流式的形式来返回（SSE）。
-   接口的调用需要阿里云百炼平台的工作空间权限。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/FaRui/2024-06-28/RunLegalAdviceConsultation)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/farui/legalAdvice/consult HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

appId

string

否

应用 ID

枚举值：

-   farui：farui。

farui

stream

boolean

否

是否是流式请求

枚举值：

-   true：true。
-   false：false。

true

workspaceId

string

否

阿里云百炼平台工作空间 ID

llm-9w5y60lseff0jiqm

assistant

object

否

智能体

id

string

否

智能体 ID

assitant\_abc\_123

metaData

object

否

智能体元数据

string

否

自定义 Meta 信息

meta

type

string

否

智能体类型

legal\_advice\_consult

version

string

否

智能体版本

1.0.0

thread

object

否

线程

messages

array<object>

否

请求上下文

object

否

content

string

否

对话内容

朋友借了我10万块钱，约定两个月归还且不需要利息。已经半年过去了但他一直没有还，我可以要求增加利息吗？

role

string

否

对话角色

枚举值：

-   assistant：助手。
-   system：系统。
-   user：用户。

user

extra

object

否

深度思考相关设置，不传则保持原先版本的返回

deepThink

boolean

否

是否进行深度思考

true

onlineSearch

boolean

否

是否进行联网检索

true

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Code

string

错误 Code 码

null

Message

string

请求异常，返回具体异常错误信息。

null

RequestId

string

阿里云为该请求生成的唯一标识符。

744419D0-671A-5997-9840-E8AE48356194

ResponseMarkdown

string

响应回答｜非深度思考链路返回

在您与朋友之间的借贷关系中，具体的计算方法可以参照一年期贷款市场报价利率（LPR）或根据公平原则和诚实信用原则确定。如协商不成，您可以通过法律诉讼途径维护自己的权益。在行动前，建议咨询专业法律人士以获取更具体的法律建议。

Round

integer

当前请求轮次

1

Status

string

响应回答状态

正在回答

Success

boolean

是否调用成功。true：调用成功。 false：调用失败。

True

contents

string

深度思考返回的内容，共三部分，按 type 来区分， type=deepThink 为深度思考部分， type=text 为回答部分，type=referenceList 为相关案例、法规、网络资料引用部分， caseList（案例），lawList(法规),searchList(网络资料，需要网络检索开关打开)

\[{"id":"50b231e343f348209023259575cf5be7","contentType":"deepThink","content":"好的，用户问的是在社交媒体上发布他人照片需要注意哪些法律风险。首先，我需要回顾法睿提供的资料，看看相关的法律条文和案例。\\n\\n首先想到的是民法典里的肖像权规定，","status":"stop"},{"searchList":\[\],"lawList":\[{"lawId":"f6a8ac8d16677fe501ccabd235d77229","lawItemId":"8a838a988a5ec2aee647e7296a602966"}","caseList":\["（2020）湘0281民初3082号"},{"id":"50b231e343f348209023259575cf5be7","contentType":"text","content":"在社交媒体上发布他人照片需注意以下法律风险及应对措施，。","status":"正在为您生成回答..."}\]

extra

string

用户输入的检索类型信息

"{\\"deepThink\\":true,\\"onlineSearch\\":true}"

Usage

object

本次调用的使用量

InputTokens

integer

输入使用的 Token 数量

500

OutputTokens

integer

输出使用的 Token 数量

700

TotalTokens

integer

本次调用使用的所有 Token 数总和

1200

httpStatusCode

string

HTTP 状态码

200

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": null,
  "Message": null,
  "RequestId": "744419D0-671A-5997-9840-E8AE48356194",
  "ResponseMarkdown": "在您与朋友之间的借贷关系中，具体的计算方法可以参照一年期贷款市场报价利率（LPR）或根据公平原则和诚实信用原则确定。如协商不成，您可以通过法律诉讼途径维护自己的权益。在行动前，建议咨询专业法律人士以获取更具体的法律建议。\n",
  "Round": 1,
  "Status": "正在回答",
  "Success": true,
  "contents": "[{\"id\":\"50b231e343f348209023259575cf5be7\",\"contentType\":\"deepThink\",\"content\":\"好的，用户问的是在社交媒体上发布他人照片需要注意哪些法律风险。首先，我需要回顾法睿提供的资料，看看相关的法律条文和案例。\\n\\n首先想到的是民法典里的肖像权规定，\",\"status\":\"stop\"},{\"searchList\":[],\"lawList\":[{\"lawId\":\"f6a8ac8d16677fe501ccabd235d77229\",\"lawItemId\":\"8a838a988a5ec2aee647e7296a602966\"}\",\"caseList\":[\"（2020）湘0281民初3082号\"},{\"id\":\"50b231e343f348209023259575cf5be7\",\"contentType\":\"text\",\"content\":\"在社交媒体上发布他人照片需注意以下法律风险及应对措施，。\",\"status\":\"正在为您生成回答...\"}]\n",
  "extra": {
    "deepThink": true,
    "onlineSearch": true
  },
  "Usage": {
    "InputTokens": 500,
    "OutputTokens": 700,
    "TotalTokens": 1200
  },
  "httpStatusCode": 200
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/FaRui/2024-06-28/errorCode)查看更多错误码。
