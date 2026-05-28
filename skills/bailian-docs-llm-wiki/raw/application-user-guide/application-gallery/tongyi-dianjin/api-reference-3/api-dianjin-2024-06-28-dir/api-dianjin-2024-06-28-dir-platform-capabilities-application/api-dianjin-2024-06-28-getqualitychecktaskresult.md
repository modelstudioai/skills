# GetQualityCheckTaskResult - 获取质检结果

获取质检结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetQualityCheckTaskResult)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetQualityCheckTaskResult)

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

dianjin:GetQualityCheckTaskResult

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/api/qualitycheck/task/query HTTP/1.1
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

llm-xxxxx

taskId

string

是

任务 ID

17071319

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

conversationList

object

原始会话内容

callType

string

呼叫类型:

枚举值：

-   1：呼入。
-   2：呼出。

1

customerId

string

客户 ID

234234

customerName

string

客户名称

张三

customerServiceId

string

客服 ID

23984763826

customerServiceName

string

客服名称

李四

dialogueList

array<object>

对话明细列表

dialogueList

object

对话明细

begin

integer

本句话的开始时间，相对于会话开始点的偏移时间 ms

0

beginTime

string

这句话的开始时间

2024-09-27 11:23:20

content

string

对话的具体内容

您好，我是2001，很高兴为您服务！

customerId

string

对话角色的唯一标识

null

customerServiceId

string

客服 ID

李四

customerServiceType

string

坐席类型

枚举值：

-   0：机器人。
-   1：人工。

0

end

integer

本句话的结束时间，相对于会话开始点的偏移时间 ms

0

id

integer

本句话的唯一标识,内部赋值

1

role

string

角色

枚举值：

-   0：客户。
-   1：坐席。

0

type

string

对话内容的类型

枚举值：

-   IMAGE：图片。
-   TEXT：文本。
-   AUDIO：语音。

TEXT

gmtService

string

会话时间

2024-09-27 11:23:20

gmtCreate

string

任务创建时间，提交任务的时间

2024-09-27 11:23:20

gmtEnd

string

系统执行结束时间

2024-09-27 11:23:20

gmtStart

string

系统执行开始时间

2024-09-27 11:23:20

qualityCheckList

array<object>

质检结果集

qualityCheckList

object

质检结果

checkExplanation

string

通过或者不通过的原因解释

暂无

checkPassed

string

是否质检通过

枚举值：

-   NOT\_PASSED：不通过。
-   PASSED：通过。

PASSED

checkProcess

string

质检过程描述

暂无

checked

string

是否命中

枚举值：

-   HIT：命中。
-   NOT\_HIT：未命中。

HIT

gmtEnd

string

质检完成时间

2024-05-23 14:57:50

gmtStart

string

质检开始时间

2024-05-23 14:57:50

mode

string

内部质检模式

枚举值：

-   0：大模型质检。

0

originDialogue

array<object>

原始对话列表

originDialogue

object

原始对话

begin

integer

本句话的开始时间，相对于会话开始点的偏移时间 ms

0

beginTime

string

这句话的开始时间

2024-05-23 14:57:50

content

string

对话的具体内容

您好，我是2001，很高兴为您服务！

customerId

string

对话角色的唯一标识

xxx

customerServiceId

string

客服 ID

23876432

customerServiceType

string

坐席类型

枚举值：

-   0：机器人。
-   1：人工。

0

end

integer

本句话的结束时间，相对于会话开始点的偏移时间 ms

0

id

integer

本句话的唯一标识，内部赋值

1

role

string

角色

枚举值：

-   0：客户。
-   1：坐席。

0

type

string

对话内容的类型

枚举值：

-   IMAGE：图片。
-   TEXT：文本。
-   AUDIO：语音。

TEXT

qualityGroupId

string

质检组 ID

warning\_customers

ruleDescription

string

质检项描述

进入检测预警客户流程

ruleId

string

质检项 ID

wcm\_start

bizType

string

规则业务类型

No

ruleType

string

规则正负向类型 0：负向，1：正向。

0

subNodeCol

array

子节点

subNodeCol

any

子节点的质检结果，结构与 qualityCheckList 相同

{ "ruleId": "wxx\_regulatory\_authorities", "ruleDescription": "具体某机构预警", "checked": "HIT", "checkProcess": "通过审查对话记录，客户主要询问了关于贷款资方信息和结清证明的问题，并表达了想要注销账户的意愿。在整个对话过程中，客户并未提及任何具体的部门名称，也没有明确表示要向部门投诉的意图。", "originDialogue": null, "checkPassed": "NOT\_PASSED", "checkExplanation": null, "mode": "0", "gmtStart": "2024-12-02 10:38:39", "gmtEnd": "2024-12-02 10:38:43", "qualityGroupId": "warning\_customers", "bizType": null, "ruleType": "0", "subNodeCol": null }

status

string

任务状态

枚举值：

-   CANCELLED：已取消。
-   INIT：初始化。
-   COMPLETED：已结束。
-   PROCESSING：进行中。
-   FAIL：失败。

INIT

taskId

string

任务 ID

1703557101831

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

67C7021A-D268-553D-8C15-A087B9604028

success

boolean

是否成功

true

time

string

时间戳

2024-01-01 00:00:00

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 0,
  "data": {
    "conversationList": {
      "callType": 1,
      "customerId": 234234,
      "customerName": "张三",
      "customerServiceId": 23984763826,
      "customerServiceName": "李四",
      "dialogueList": [
        {
          "begin": 0,
          "beginTime": "2024-09-27 11:23:20",
          "content": "您好，我是2001，很高兴为您服务！",
          "customerId": null,
          "customerServiceId": "李四",
          "customerServiceType": 0,
          "end": 0,
          "id": 1,
          "role": 0,
          "type": "TEXT"
        }
      ],
      "gmtService": "2024-09-27 11:23:20"
    },
    "gmtCreate": "2024-09-27 11:23:20",
    "gmtEnd": "2024-09-27 11:23:20",
    "gmtStart": "2024-09-27 11:23:20",
    "qualityCheckList": [
      {
        "checkExplanation": "暂无",
        "checkPassed": "PASSED",
        "checkProcess": "暂无",
        "checked": "HIT",
        "gmtEnd": "2024-05-23 14:57:50",
        "gmtStart": "2024-05-23 14:57:50",
        "mode": 0,
        "originDialogue": [
          {
            "begin": 0,
            "beginTime": "2024-05-23 14:57:50",
            "content": "您好，我是2001，很高兴为您服务！",
            "customerId": "xxx",
            "customerServiceId": 23876432,
            "customerServiceType": 0,
            "end": 0,
            "id": 1,
            "role": 0,
            "type": "TEXT"
          }
        ],
        "qualityGroupId": "warning_customers",
        "ruleDescription": "进入检测预警客户流程",
        "ruleId": "wcm_start",
        "bizType": "No",
        "ruleType": 0,
        "subNodeCol": [
          {
            "ruleId": "wxx_regulatory_authorities",
            "ruleDescription": "具体某机构预警",
            "checked": "HIT",
            "checkProcess": "通过审查对话记录，客户主要询问了关于贷款资方信息和结清证明的问题，并表达了想要注销账户的意愿。在整个对话过程中，客户并未提及任何具体的部门名称，也没有明确表示要向部门投诉的意图。",
            "originDialogue": null,
            "checkPassed": "NOT_PASSED",
            "checkExplanation": null,
            "mode": 0,
            "gmtStart": "2024-12-02 10:38:39",
            "gmtEnd": "2024-12-02 10:38:43",
            "qualityGroupId": "warning_customers",
            "bizType": null,
            "ruleType": 0,
            "subNodeCol": null
          }
        ]
      }
    ],
    "status": "INIT",
    "taskId": 1703557101831
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "67C7021A-D268-553D-8C15-A087B9604028",
  "success": true,
  "time": "2024-01-01 00:00:00"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
