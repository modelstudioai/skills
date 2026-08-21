# RealtimeDialogAssist - 实时会话辅助

实时会话辅助，使用CreateDialog创建会话后，可进行实时的会话辅助。注意：与实时会话不同，会话辅助可返回多个意图、标签和SOP流程等，但不支持流式返回。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和[价格](https://help.aliyun.com/zh/model-studio/tongyi-dianjin-overview)。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/RealtimeDialogAssist)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/RealtimeDialogAssist)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

dianjin:RealtimeDialogAssist

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/realtime/dialog/assist HTTP/1.1
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

业务空间 id

llm-xxxxx

body

object

否

请求体参数。

requestId

string

是

请求 ID

0FC6636E-380A-5369-AE01-D1C15BB9B254

bizType

string

是

业务类型，目前只支持 dialogAssist。

dialogAssist

analysis

boolean

否

是否分析

false

metaData

object

否

metaData

{ "phoneTailNumber": "机主尾号：98X1", "preScreeningQuota": "预审额度：3万", "generalInterest": "平台一般利息：20.4%" }

conversationModel

array<object>

是

对话列表

conversationModel

object

否

对话

role

integer

是

角色。0 表示客户，1 表示坐席。

0

customerServiceType

string

否

坐席类型，0: 机器人，1: 人工。

0

customerServiceId

string

否

客服 ID

1374683645635

customerId

string

否

对话角色的唯一标识

98457834685635

content

string

是

对话的具体内容

你好

type

string

否

对话内容的类型，目前只支持 text。

text

beginTime

string

否

这句话的开始时间

2025-12-12 09:00:00

begin

integer

否

本句话的开始时间，相对于会话开始点的偏移时间 ms

1

end

integer

否

本句话的结束时间，相对于会话开始点的偏移时间 ms

1

sessionId

string

是

会话 ID

1915593248420413441

dialogMemoryTurns

integer

否

携带的会话历史轮数

0

userVad

boolean

否

是否用户打断

true

scriptContentPlayed

string

否

上一句客服话术已经播报的部分

你好

hangUpDialog

boolean

否

挂断会话

false

## 返回参数

名称

类型

描述

示例值

object

ResultCode

success

boolean

是否成功

true

dataType

string

数据类型

null

time

string

时间戳

2024-04-24 11:54:34

errCode

string

错误码

0

message

string

错误信息

ok

data

object

响应数据

requestId

string

请求唯一 ID。该请求 ID 与入参中的请求 ID 一致。

0FC6636E-380A-5369-AE01-D1C15BB9B254

sessionId

string

会话 ID

"1915593248420413441"

interrupt

boolean

是否打断

true

conversationModel

array<object>

本轮对话内容

conversationModel

object

对话的具体内容

role

string

角色。0 表示客户，1 表示坐席。

"0"

customerServiceType

string

坐席类型，0: 机器人，1: 人工。

"0"

customerServiceId

string

客服 ID

"1374683645635"

customerId

string

对话角色的唯一标识

"98457834685635"

content

string

对话的具体内容

你好

type

string

对话内容的类型

text

assistScripts

array<object>

话术辅助结果列表

assistScript

object

话术辅助结果

intentCode

string

意图编码

"1920005488515465216"

intentName

string

意图名称

礼貌问答

intentLabels

string

意图标签

null

assistScript

string

推荐话术

可按照SOP流程回应。

isDefault

boolean

是否意图逃逸

true

assistSop

array<object>

流程辅助结果列表

assistSop

object

流程辅助结果

intentCode

string

意图编码

XXX

intentName

string

意图名称

XXX

assistSop

string

推荐流程

XXX

isDefault

boolean

是否意图逃逸

true

analysisProcess

string

分析过程

客户回答的内容与提供的意图列表描述均不匹配，没有表达出对账单、还款、天气或其他服务的具体需求或问题。

requestId

string

请求 id，该请求 ID 为系统记录请求 ID，有问题时可提供该 ID 给点金研发进行定位排查。

67C7021A-D268-553D-8C15-A087B9604028

cost

long

耗时

null

## 示例

正常返回示例

`JSON`格式

```
{
  "success": true,
  "dataType": null,
  "time": "2024-04-24 11:54:34",
  "errCode": 0,
  "message": "ok",
  "data": {
    "requestId": "0FC6636E-380A-5369-AE01-D1C15BB9B254",
    "sessionId": 1915593248420413400,
    "interrupt": true,
    "conversationModel": [
      {
        "role": 0,
        "customerServiceType": 0,
        "customerServiceId": 1374683645635,
        "customerId": 98457834685635,
        "content": "你好",
        "type": "text"
      }
    ],
    "assistScripts": [
      {
        "intentCode": 1920005488515465200,
        "intentName": "礼貌问答",
        "intentLabels": null,
        "assistScript": "可按照SOP流程回应。",
        "isDefault": true
      }
    ],
    "assistSop": [
      {
        "intentCode": "XXX",
        "intentName": "XXX",
        "assistSop": "XXX",
        "isDefault": true
      }
    ],
    "analysisProcess": "客户回答的内容与提供的意图列表描述均不匹配，没有表达出对账单、还款、天气或其他服务的具体需求或问题。"
  },
  "requestId": "67C7021A-D268-553D-8C15-A087B9604028",
  "cost": 0
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-01-07

OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/DianJin/2024-06-28/RealtimeDialogAssist?updateTime=2026-01-07#workbench-doc-change-demo)
