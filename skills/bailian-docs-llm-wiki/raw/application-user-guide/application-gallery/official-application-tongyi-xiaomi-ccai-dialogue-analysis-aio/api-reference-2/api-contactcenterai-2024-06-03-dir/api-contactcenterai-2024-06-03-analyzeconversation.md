# AnalyzeConversation - 通过任务类型调用通义晓蜜CCAI-对话分析AIO应用

获取对话摘要、标题生成、关键词、字段信息抽取、问题及解决方案、服务质检、代办事项、满意度、情绪检测、QA抽取、用户画像、标签分类等对话分析结果，应用调用支持 HTTP 调用来完成客户的响应。

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

前提条件

1.  已开通通义晓蜜 CCAI-对话分析 AIO 服务。
2.  已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：获取[APP-ID 和 WORKSPACE-ID](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.41df281fWNMfrx)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/AnalyzeConversation)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/AnalyzeConversation)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/ccai/app/{appId}/analyze_conversation HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

工作空间 ID

llm-368\*\*\*\*\*\*3ifum

appId

string

是

应用 id。

a070a49c681f4a95a0f0\*\*\*\*\*\*\*\*\*35c

body

object

否

请求体。

categoryTags

array<object>

否

标签分类列表

object

否

tagDesc

string

否

标签描述

客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为

tagName

string

否

标签名称

客服过度承诺

dialogue

object

否

对话内容列表

sentences

array<object>

是

对话内容

object

是

role

string

是

通话角色：

-   user-客户
    
-   agent-客服
    
-   system-系统消息
    

user

text

string

是

对话文本

请问怎么申请新卡

sessionId

string

否

客服会话 sessionId

session-01

examples

array<object>

否

指令示例列表

object

是

指令示例

output

string

是

输出示例

问题描述：询问2.2更新时间，处理方案：已告知

sentences

array<object>

是

对话内容示例列表

object

是

对话内容示例

chatId

string

否

每一轮对话 id

chat-01

role

string

是

通话角色：

-   user-客户
    
-   agent-客服
    
-   system-系统消息
    

user

text

string

是

对话文本

什么时候更新

fields

array<object>

否

信息抽取时，需要抽取的字段列表

object

是

字段结构信息

code

string

否

字段编码

phoneNumber

desc

string

是

字段描述

用户来电咨询的原因分类，主要有投诉、咨询、政策建议等。

enumValues

array<object>

否

枚举值列表

object

是

desc

string

是

枚举描述

客户有新的需求/新的场景，客服跟进沟通需求细节

enumValue

string

是

枚举值

新业务拓展

name

string

是

字段名称

来电原因类型

modelCode

string

否

模型 code

tyxmTurbo

resultTypes

array

是

指令任务类型

string

是

summary-对话摘要，title-标题生成、fields-字段信息抽取、keywords -关键字抽取，service\_inspection-服务质检、question\_solution-问题和解决方案、actions-代办事项、satisfaction-满意度、emotion\_detection-情绪检测、questions\_and\_answer-QA 抽取、user\_profile-用户画像、category\_tag-标签分类

summary

sceneName

string

否

场景名称

阿里云工单质检场景

serviceInspection

object

否

服务质检结构信息

inspectionContents

array<object>

是

服务质检维度结构列表

object

是

服务质检维度结构

content

string

是

服务质检维度描述

客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为，如：最快到货时间是12小时，无法给客户承诺更快的到货时间。

title

string

是

服务质检维度名称

客服是否过度承诺

inspectionIntroduction

string

是

服务质检场景详细介绍及描述

请检测客服是否存在服务不当的行为，包括：过度承诺、故意套取客户隐私信息等

sceneIntroduction

string

是

服务质检场景

保险销售场景

stream

boolean

是

必填。是否流式：true，流式返回答案；false，全量返回答案。

false

userProfiles

array<object>

否

用户画像列表

object

否

name

string

否

名称

sex

value

string

否

描述

表示客户的性别，从列表\[“男”, “女”\]中选择一个值

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

errorCode

string

错误码

success

errorInfo

string

错误信息

success

finishReason

string

如果是流式输出，正在生成时为 null，生成结束时如果由于停止 token 导致则为 stop。

stop

requestId

string

系统生成的标志本次请求的唯一性 ID

968A8634-FA2C-5381-9B3E-C552DED7E8BF

success

boolean

请求是否成功

True

text

string

应用返回的结果。

这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。

## 示例

正常返回示例

`JSON`格式

```
{
  "errorCode": "success",
  "errorInfo": "success",
  "finishReason": "stop",
  "requestId": "968A8634-FA2C-5381-9B3E-C552DED7E8BF",
  "success": true,
  "text": "这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。",
  "inputTokens": "",
  "outputTokens": "",
  "totalTokens": ""
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

400

CCAI.Throttling.Qps

Trigger current QPS limit, pay API please buy higher QPS, the free API if you have special requirements, please contact us through the DingTalk group (62730018475).

触发限流，付费API请购买更高QPS，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。

400

CCAI.Throttling.Qpm

Trigger QPM flow restriction. Please purchase higher QPM for paid API. If free API has special requirements, please contact us through DingTalk group (62730018475).

触发QPM限流，付费API请购买更高QPM，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。

400

CCAI.InvalidParam.NotExist

The specified parameter %s is not valid.

请求API的参数不存在

400

CCAI.ParamInvalid.IllegalParamValue

The parameter value of the request API is illegal %s.

请求API的参数不合法

403

CCAI.TenantPermission.NoAuth

The current account does not have the permission to specify the business space. Please authorize the business space permission.

当前账号没有指定业务空间的权限，请进行业务空间权限授权。

403

CCAI.ParamNotfound.MissParam

Parameter verification failed, The specified parameter %s is missing.

参数校验失败，指定参数缺失。

403

CCAI.IllegalPermission.NoAuth

User not authorized to operate on the specified resource %s .

该用户未被授权可操作指定资源

500

CCAI.InternalError

The request processing has failed due to some unknown error, exception or failure.

系统内部错误，请稍后重试

访问[错误中心](< https://api.aliyun.com/document/ContactCenterAI/2024-06-03/errorCode>)查看更多错误码。
