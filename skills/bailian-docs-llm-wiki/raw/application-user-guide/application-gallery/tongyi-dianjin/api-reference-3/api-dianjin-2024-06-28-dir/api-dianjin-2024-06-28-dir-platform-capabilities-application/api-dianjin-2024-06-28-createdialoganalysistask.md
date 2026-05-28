# CreateDialogAnalysisTask - 创建会话分析任务

创建会话分析任务，创建成功后可根据会话ID使用GetDialogAnalysisResult查询结果

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/CreateDialogAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/CreateDialogAnalysisTask)

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

dianjin:CreateDialogAnalysisTask

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/virtualHuman/dialog/analysis/submit HTTP/1.1
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

请求体。

metaData

object

否

元数据，用于会话分析过程中需要消费的一些业务相关的属性，由业务系统在发起会话分析任务的时候实时传入。

```
{
  "labels": "XXX",  // 标签
  "summaryConstraints": "XXX",   // 摘要维度
  "sopInfo": "XXX"  // SOP 信息
}
```

{ "labels": "XXX", "summaryConstraints": "XXX", "sopInfo": "XXX" }

playCode

string

是

会话场景编码，关联会话分析配置

common

analysisNodes

array

否

分析节点列表，默认为空，表示全部节点。可传入一个或者多个。

analysisNode

string

否

分析节点

枚举值：

-   DIALOG\_EXECUTION\_PLAN：执行计划。
-   DIALOG\_SUMMARY：会话小结。
-   DIALOG\_SOP：会话SOP。
-   DIALOG\_LABEL：会话标签。

DIALOG\_LABEL

requestId

string

是

请求 ID

0FC6636E-380A-5369-AE01-D1C15BB9B254

conversationList

array<object>

是

会话内容，可传入多个会话。

object

否

会话内容

dialogueList

array<object>

是

对话列表

object

否

对话

content

string

是

对话的具体内容

您好，我是2001，很高兴为您服务！

role

string

是

角色（0: 客户；1: 坐席）

1

## 返回参数

名称

类型

描述

示例值

object

ResultCode<List\>

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

array

响应数据，返回会话 ID 列表。

data

string

会话 ID

1876540295480209409

requestId

string

请求 id

EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258

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
  "data": [
    1876540295480209400
  ],
  "requestId": "EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258",
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
