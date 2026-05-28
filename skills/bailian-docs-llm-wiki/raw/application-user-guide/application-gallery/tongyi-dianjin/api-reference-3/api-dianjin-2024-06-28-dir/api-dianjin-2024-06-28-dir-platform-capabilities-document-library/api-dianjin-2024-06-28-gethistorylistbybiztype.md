# GetHistoryListByBizType - 根据业务类型获取对话历史记录

根据业务类型获取对话历史记录。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetHistoryListByBizType)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetHistoryListByBizType)

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

dianjin:GetHistoryListByBizType

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/api/history/list HTTP/1.1
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

page

integer

否

页码

1

pageSize

integer

否

页面大小

10

bizType

string

是

业务类型，目前支持：模型问答（LlmChat）、文档库问答（LibraryChat）

LibraryChat

bizId

string

是

业务唯一标识，当 bizType 为 LibraryChat 时，bizId 指的是文档库 id

GysYBsxx

## 返回参数

名称

类型

描述

示例值

object

ResultCode<PageVO\>

cost

long

耗时

null

data

object

响应数据

currentPage

long

当前页

1

pageSize

long

每页记录数

10

records

array<object>

记录

record

object

数据

bizId

string

业务 id

GysYBsxx

bizType

string

业务类型

LibraryChat

extraMessage

any

扩展信息

null

gmtCreate

string

创建时间

2024-01-01 00:00:00

gmtModified

string

修改时间

2024-01-01 00:00:00

id

long

历史记录 id

210

llmAnswer

string

大模型回答

你好。

llmPrompt

string

大模型提示词

请使用以下上下文来回答最后的问题。\\n以下是上下文内容：

llmType

string

大模型类型

qwen-max

sessionId

string

会话 id

null

userQuery

string

用户问题

你是谁

totalPages

long

总页数

10

totalRecords

long

总记录数

100

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

9DF9B3F3-9FFE-52CB-A8DC-F7BD5F842F0E

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
    "currentPage": 1,
    "pageSize": 10,
    "records": [
      {
        "bizId": "GysYBsxx",
        "bizType": "LibraryChat",
        "extraMessage": null,
        "gmtCreate": "2024-01-01 00:00:00",
        "gmtModified": "2024-01-01 00:00:00\n",
        "id": 210,
        "llmAnswer": "你好。",
        "llmPrompt": "请使用以下上下文来回答最后的问题。\\n以下是上下文内容：",
        "llmType": "qwen-max",
        "sessionId": null,
        "userQuery": "你是谁"
      }
    ],
    "totalPages": 10,
    "totalRecords": 100
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "9DF9B3F3-9FFE-52CB-A8DC-F7BD5F842F0E",
  "success": true,
  "time": "2024-01-01 00:00:00"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
