# RecognizeIntention - 意图识别

意图识别，支持意图识别（全局+分层）、态度识别、企业识别。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/RecognizeIntention)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/RecognizeIntention)

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

dianjin:RecognizeIntention

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/recog/intent HTTP/1.1
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

llm-xxxx

body

object

否

请求体。

analysis

boolean

否

是否分析

false

bizType

string

是

业务类型。

枚举值：

-   common：意图识别。
-   business：企业识别。
-   attitude：态度识别。

common

conversation

string

是

对话内容。

##客服##：您好，请问是朱杰先生吗？这里是诚信财务的周莉。我们发现您有一项款项昨天是账单日，但您还没还款，这很可能是一个小小的疏忽。来电是提醒您尽快完成还款，避免影响您的信用记录。\\n ##客户##：今天天气怎么样呢？

globalIntentionList

array<object>

否

全局意图列表，当操作类型 opType 为分层 hierarchical 时，必填。

globalIntentionList

object

否

全局意图

description

string

否

意图描述

正常付款3

intention

string

否

意图名称

正常付款3

intentionCode

string

否

意图 code

1810566978021232640

intentionScript

string

否

意图话术

好的，那先不打扰您了，祝您生活愉快！再见！

hierarchicalIntentionList

array<object>

否

分层意图列表，当操作类型 opType 为分层 hierarchical 时，必填。

hierarchicalIntentionList

object

否

分层意图

description

string

否

意图描述

询问股票价格

intention

string

否

意图名称

询问股票价格

intentionCode

string

否

意图 code

1810929291010150400

intentionScript

string

否

意图话术

好的，那先不打扰您了，祝您生活愉快！再见！

intentionList

array<object>

否

意图列表，当业务类型**不为**态度识别时，必填。

intentionList

object

否

意图

description

string

否

意图描述

客户表示忘记还款

intention

string

否

意图名称

客户表示忘记还款

intentionCode

string

否

意图 code

1808766224000262144

intentionScript

string

否

意图话术

好的，那先不打扰您了，祝您生活愉快！再见！

opType

string

否

操作类型。

枚举值：

-   common：通用。
-   hierarchical：分层。

common

recommend

boolean

否

推荐意图

false

intentionDomainCode

string

否

意图库: 本地意图库 code

collection

## 返回参数

名称

类型

描述

示例值

object

ResultCode

cost

long

耗时

null

data

object

响应数据

analysisProcess

string

分析过程

客户回答的内容与提供的意图列表描述均不匹配，没有表达出对账单、还款、天气或其他服务的具体需求或问题。

intentionCode

string

意图 code

\-1

intentionName

string

意图名称

其它

recommendIntention

string

推荐意图

客户试图回避谈论逾期还款的话题

recommendScript

string

推荐话术

朱先生，理解您可能对天气感兴趣，但更重要的是您的账户情况。请让我们专注于您未偿还的款项，这对您的信用健康至关重要。

intentionScript

string

意图话术

朱先生，理解您可能对天气感兴趣，但更重要的是您的账户情况。请让我们专注于您未偿还的款项，这对您的信用健康至关重要。

dataType

string

数据类型

null

errCode

string

错误码

0

message

string

错误信息

ok

requestId

string

请求 id

003D019A-1BB3-53EC-A0D2-CE76DA5D73B1

success

boolean

是否成功

true

time

string

时间戳

2024-04-24 11:54:34

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 0,
  "data": {
    "analysisProcess": "客户回答的内容与提供的意图列表描述均不匹配，没有表达出对账单、还款、天气或其他服务的具体需求或问题。",
    "intentionCode": -1,
    "intentionName": "其它",
    "recommendIntention": "客户试图回避谈论逾期还款的话题",
    "recommendScript": "朱先生，理解您可能对天气感兴趣，但更重要的是您的账户情况。请让我们专注于您未偿还的款项，这对您的信用健康至关重要。",
    "intentionScript": "朱先生，理解您可能对天气感兴趣，但更重要的是您的账户情况。请让我们专注于您未偿还的款项，这对您的信用健康至关重要。"
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "003D019A-1BB3-53EC-A0D2-CE76DA5D73B1",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
