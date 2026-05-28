# CreateDialog - 创建外呼会话

创建外呼会话。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/CreateDialog)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/CreateDialog)

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

dianjin:CreateDialog

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/virtualHuman/dialog/create HTTP/1.1
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

playCode

string

是

剧本编码

live\_broadcast\_qa

channel

string

是

渠道

taobao

metaData

object

否

其他信息

null

qaLibraryList

array

否

QA 问答库 ID 列表

qaLibraryList

string

否

QA 问答库 ID

d86a4b9cd3

requestId

string

是

请求 ID

ebf83826-dc1c-46f8-9759-0fb6da4c8xxx

enableLibrary

boolean

否

是否开启意图库

false

selfDirected

boolean

否

是否开启自主问答

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

sessionId

string

会话 ID

1728545917713234

openingRemarks

string

开场白

你好，我是XX客服人员。

requestId

string

请求 id

003D019A-1BB3-53EC-A0D2-CE76DA5D73B1

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
    "sessionId": 1728545917713234,
    "openingRemarks": "你好，我是XX客服人员。"
  },
  "requestId": "003D019A-1BB3-53EC-A0D2-CE76DA5D73B1",
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
