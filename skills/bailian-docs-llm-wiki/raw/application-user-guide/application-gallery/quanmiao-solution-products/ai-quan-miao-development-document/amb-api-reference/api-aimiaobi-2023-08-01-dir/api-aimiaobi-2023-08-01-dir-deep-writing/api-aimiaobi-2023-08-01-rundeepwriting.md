# RunDeepWriting - 查询深度写作事件

查询深度写作事件。 系统以SSE事件的形式下发任务执行过程中的详细信息。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDeepWriting)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDeepWriting)

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

aimiaobi:RunDeepWriting

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /pop/deepWrite/runDeepWriting HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-ir8zkqry2fncaxwq

TaskId

string

否

任务 ID

95c2fbe6-5a20-4fc2-8a93-376ed05fbe13

Cursor

integer

否

游标。流式事件的序号

10

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Header

object

响应头

ErrorCode

string

错误码

403

ErrorMessage

string

错误信息。

错误消息

Event

string

SSE 事件。

枚举值：

-   response.sub\_task.created：子任务已创建。
-   response.output\_item.done：中间结果输出完成。
-   response.completed：任务完成。
-   response.created：任务已创建。

response.output\_item.done

SessionId

string

会话 ID

c2e2e991-f96a-4fcc-9ff7-d0df46c6d232

StatusCode

integer

http 响应码

200

TaskId

string

任务 ID

b84d31a5-44b2-4a35-9c6d-878d459c93d0

TraceId

string

全链路 ID

FAB10D42-F081-557B-8DCB-D6FB7AAF100B

Payload

object

响应体

Output

object

输出

Type

string

类型

同上级Event

SequenceNumber

string

流式事件的序号

1

OutputIndex

integer

本次事件新加的输出 item 的序号

1

Response

object

响应体

Id

string

本次任务的唯一标识

b2dc224b38694e0b668020159a7c5732

Status

string

本次任务的执行状态

枚举值：

-   in\_progress：处理中。
-   completed：已完成。

in\_progress

Item

object

本次事件新加的输出 item

Id

string

item 的唯一标识

88f6ed9e85c4f9377378da23e6a370d1

Status

string

item 的状态

枚举值：

-   in\_progress：in\_progress。
-   completed：completed。

completed

Type

string

item 的类型

枚举值：

-   function\_call：function\_call。
-   message：message。

function\_call

Arguments

string

参数

item类型为function\_call时，此字段有值，为调用函数的入参

Name

string

参数名称

item类型为function\_call时，此字段有值，为调用的函数名字

Result

string

item 的结果

item类型为function\_call时，此字段有值，为调用的函数的输出

Agent

string

输出此 item 的 agent 名字

ProjectManager

Content

array<object>

item 类型为 message 时，此字段有值，是输出 content 的列表

content

object

文本内容

Type

string

item 类型为 message 时，此字段的值是 output\_text

output\_text

Text

string

item 类型为 message 时, 输出的文本内容

<TASK\_DONE>

RequestId

string

唯一请求 ID

31AC01F1-88FB-5C4D-B6F5-E8BB136CD5A3

HttpStatusCode

string

Http 状态码

200

Code

string

状态码

successful

Message

string

错误信息。

success

Success

boolean

此次请求是否成功

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": 403,
    "ErrorMessage": "错误消息",
    "Event": "response.output_item.done",
    "SessionId": "c2e2e991-f96a-4fcc-9ff7-d0df46c6d232",
    "StatusCode": 200,
    "TaskId": "b84d31a5-44b2-4a35-9c6d-878d459c93d0",
    "TraceId": "FAB10D42-F081-557B-8DCB-D6FB7AAF100B"
  },
  "Payload": {
    "Output": {
      "Type": "同上级Event",
      "SequenceNumber": 1,
      "OutputIndex": 1,
      "Response": {
        "Id": "b2dc224b38694e0b668020159a7c5732",
        "Status": "in_progress"
      },
      "Item": {
        "Id": "88f6ed9e85c4f9377378da23e6a370d1",
        "Status": "completed",
        "Type": "function_call",
        "Arguments": "item类型为function_call时，此字段有值，为调用函数的入参",
        "Name": "item类型为function_call时，此字段有值，为调用的函数名字",
        "Result": "item类型为function_call时，此字段有值，为调用的函数的输出",
        "Agent": "ProjectManager",
        "Content": [
          {
            "Type": "output_text",
            "Text": "<TASK_DONE>"
          }
        ]
      }
    }
  },
  "RequestId": "31AC01F1-88FB-5C4D-B6F5-E8BB136CD5A3",
  "HttpStatusCode": 200,
  "Code": "successful",
  "Message": "success",
  "Success": true
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
