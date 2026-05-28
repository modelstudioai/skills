# CreateQualityCheckTask - 创建质检任务

创建质检任务。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/CreateQualityCheckTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/CreateQualityCheckTask)

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

dianjin:CreateQualityCheckTask

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/qualitycheck/task/submit HTTP/1.1
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

conversationList

object

是

会话内容，关联质检场景需要传入多个会话，否则只有一个会话

callType

string

否

呼叫类型:

枚举值：

-   1：呼入。
-   2：呼出。

1

customerId

string

否

客户 ID

1

customerName

string

否

客户名称

张三

customerServiceId

string

否

客服 ID

xxx

customerServiceName

string

否

客服名称

李四

dialogueList

array<object>

是

对话明细列表

dialogueList

object

否

对话明细

begin

integer

否

本句话的开始时间，相对于会话开始点的偏移时间 ms

0

beginTime

string

否

这句话的开始时间

2024-05-23 14:57:50

content

string

是

对话的具体内容

您好，我是2001，很高兴为您服务！

customerId

string

否

对话角色的唯一标识

2348234

customerServiceId

string

否

客服 ID

23874627346

customerServiceType

string

否

坐席类型

枚举值：

-   0：机器人。
-   1：人工。

0

end

integer

否

本句话的结束时间，相对于会话开始点的偏移时间 ms

0

role

string

是

角色

枚举值：

-   0：客户。
-   1：坐席。

1

type

string

是

对话内容的类型

枚举值：

-   IMAGE：图片。
-   TEXT：文本。
-   AUDIO：语音。

TEXT

gmtService

string

否

会话时间

2024-09-27 11:23:20

gmtService

string

是

业务发生时间，用于系统记录提交时间，任务调度优先级决策等

2024-09-27 11:23:20

metaData

object

否

元数据，用于规则执行过程中需要消费的一些业务相关的属性，由业务系统在发起质检的时候实时传入。

string

否

元数据

{ "isSpecialArchive": false, "hasProcessingWorkOrder": false, "primaryArchiveType": "其他", "businessType": "预警", "workOrderActionType":"业务升级" }

qualityGroup

array

否

质检规则组

qualityGroup

string

否

质检规则

warning\_customers

requestId

string

是

请求 ID

0FC6636E-380A-5369-AE01-D1C15BB9B254

type

string

是

质检类型

枚举值：

-   0：离线文本会话质检。

0

sceneCode

string

否

场景编码。

o9c8u8

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

taskId

string

taskId

172373500521

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

EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258

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
    "taskId": 172373500521
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258",
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

2025-12-11

API 内部配置变更，不影响调用

[查看变更详情](https://api.aliyun.com/document/DianJin/2024-06-28/CreateQualityCheckTask?updateTime=2025-12-11#workbench-doc-change-demo)
