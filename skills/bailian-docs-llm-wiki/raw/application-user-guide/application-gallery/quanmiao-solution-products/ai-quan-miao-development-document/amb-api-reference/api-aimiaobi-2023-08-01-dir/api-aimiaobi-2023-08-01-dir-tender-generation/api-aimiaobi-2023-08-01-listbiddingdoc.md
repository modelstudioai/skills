# ListBiddingDoc - 列出标书写作任务

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListBiddingDoc)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListBiddingDoc)

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

aimiaobi:ListBiddingDoc

list

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

否

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

TaskName

string

否

任务名称定义

任务名称

TaskStatus

integer

否

任务状态

0-waiting、1-running、2-success、3-pause、4-fail

CreateTimeStart

string

否

起始创建时间，时间戳形式。

2023-02-19 07:28:11

CreateTimeEnd

string

否

截止创建时间，时间戳形式。

2023-03-18 02:00:00

Current

integer

否

当前页码

1

Size

integer

否

每页条数：默认 10

10

Skip

integer

否

废弃

null

MaxResults

integer

否

废弃

null

NextToken

string

否

废弃

null

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

Id of the request

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Code

string

状态码

success

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

Success

boolean

是否成功：true 成功，false 失败

true

MaxResults

integer

废弃

null

NextToken

string

废弃

null

TotalCount

integer

废弃

null

Current

integer

当前页码

1

Size

integer

每页条数

10

Total

integer

总记录数

10

Data

array<object>

返回数据

Data

object

业务数据

TaskId

string

任务 ID。

3f7045e099474ba28ceca1b4eb6d6e21

TaskName

string

任务名称

任务名称

TaskStatus

integer

任务状态

1

CreateTimeStart

string

创建时间-开始范围，格式：yyyy-MM-dd HH:mm:ss

2023-03-18 02:00:00

TaskStep

string

任务阶段

analysis writing

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Code": "success",
  "HttpStatusCode": 200,
  "Message": "success",
  "Success": true,
  "MaxResults": 0,
  "NextToken": null,
  "TotalCount": 0,
  "Current": 1,
  "Size": 10,
  "Total": 10,
  "Data": [
    {
      "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
      "TaskName": "任务名称",
      "TaskStatus": 1,
      "CreateTimeStart": "2023-03-18 02:00:00\n",
      "TaskStep": "analysis\nwriting"
    }
  ]
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
