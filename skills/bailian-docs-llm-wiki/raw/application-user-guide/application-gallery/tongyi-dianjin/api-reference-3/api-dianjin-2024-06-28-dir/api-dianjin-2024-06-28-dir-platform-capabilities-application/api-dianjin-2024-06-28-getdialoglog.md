# GetDialogLog - 获取对话日志

用于获取实时对话的记录及意图分析结果。

## 接口说明

## [](#请求说明)请求说明

该 API 旨在提供客户与客服之间的对话记录以及通过模型分析得出的客户意图内容。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetDialogLog)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetDialogLog)

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

dianjin:GetDialogLog

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/dialog/log HTTP/1.1
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

业务空间 Id

llm-xxxx

body

object

否

请求体内容

id

string

是

实时对话接口返回参数中 id 字段

175600129454077743fb03ac54955a4be72ec08f9c216

sessionId

string

是

会话 ID

1758010668S001w4paq82azm

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

2024-01-01 00:00:00

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

recallList

string

召回列表

\## Example:\\n- 对话内容为：\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:暂时没有了。谢谢。\\"时，用户意图为：\\"客户想要挂断电话\\"\\n- 对话内容为：\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:哎你好。\\"时，用户意图为：\\"客户询问来电目的\\"\\n- 对话内容为：\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:我现在财务状况很好，谢谢关心。\\"时，用户意图为：\\"客户拒绝贷款\\"\\n- 对话内容为：\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:不用了，谢谢，不要再打电话了，谢谢。\\"时，用户意图为：\\"投诉/退订/不要打电话/骂人\\"\\n- 对话内容为：\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:你好。\\"时，用户意图为：\\"客户询问来电目的\\"

intentionList

array<object>

意图列表

intentionList

object

意图

intentionName

string

意图名称

客户明确表示拒绝营销

intentionScript

string

`intentionScript` 字段包含了针对不同用户意图的客服回复脚本。

非常抱歉，给您带来了不好的体验。如您无需再接受我们的官方来电，请回复“我要退订”四个字！

description

string

`description` 字段提供了对用户意图的详细描述。

客户明确表示投诉/退订/不要打电话/骂人等拒绝营销

conversationList

string

`conversationList` 字段记录了对话内容。

##客服##:您好，请问是张三先生是吧？\\n ##客户##:人工客服\\n ##客服##:您好，我是2804，很高兴为您服务！\\n ##客服##:您好，请问有什么可以帮到您？\\n ##客户##:好的 谢谢\\n

hitIntentionList

array<object>

命中意图列表

hitIntentionList

object

命中意图

intentionName

string

意图名称

客户要求转人工

intentionScript

string

根据客户意图提供的脚本回复内容。

很抱歉，我这里无法直接为您转接，您可以拨打我司客服热线进行咨询。

description

string

客户意图的描述信息。

客户希望与真人接触，不想和AI客服继续对话。

analysisProcess

string

分析过程(实时对话时开启分析过程开关则有值)

客户回答的内容与提供的意图列表描述均不匹配，没有表达出对账单、还款、天气或其他服务的具体需求或问题。

modelCostTime

long

模型处理时间（毫秒）。

1382

requestId

string

请求 ID。

051EEB18-049A-17FF-A5E0-14A5B127C798

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
  "time": "2024-01-01 00:00:00",
  "errCode": 0,
  "message": "ok",
  "data": {
    "recallList": "## Example:\\n- 对话内容为：\\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:暂时没有了。谢谢。\\\"时，用户意图为：\\\"客户想要挂断电话\\\"\\n- 对话内容为：\\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:哎你好。\\\"时，用户意图为：\\\"客户询问来电目的\\\"\\n- 对话内容为：\\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:我现在财务状况很好，谢谢关心。\\\"时，用户意图为：\\\"客户拒绝贷款\\\"\\n- 对话内容为：\\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:不用了，谢谢，不要再打电话了，谢谢。\\\"时，用户意图为：\\\"投诉/退订/不要打电话/骂人\\\"\\n- 对话内容为：\\\"##客服##:您好，请问有什么可以帮到您？\\n ##客户##:你好。\\\"时，用户意图为：\\\"客户询问来电目的\\\"",
    "intentionList": [
      {
        "intentionName": "客户明确表示拒绝营销",
        "intentionScript": "非常抱歉，给您带来了不好的体验。如您无需再接受我们的官方来电，请回复“我要退订”四个字！",
        "description": "客户明确表示投诉/退订/不要打电话/骂人等拒绝营销"
      }
    ],
    "conversationList": "##客服##:您好，请问是张三先生是吧？\\n ##客户##:人工客服\\n ##客服##:您好，我是2804，很高兴为您服务！\\n ##客服##:您好，请问有什么可以帮到您？\\n ##客户##:好的 谢谢\\n ",
    "hitIntentionList": [
      {
        "intentionName": "客户要求转人工",
        "intentionScript": "很抱歉，我这里无法直接为您转接，您可以拨打我司客服热线进行咨询。\n",
        "description": "客户希望与真人接触，不想和AI客服继续对话。"
      }
    ],
    "analysisProcess": "客户回答的内容与提供的意图列表描述均不匹配，没有表达出对账单、还款、天气或其他服务的具体需求或问题。",
    "modelCostTime": 1382
  },
  "requestId": "051EEB18-049A-17FF-A5E0-14A5B127C798",
  "cost": 0
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
