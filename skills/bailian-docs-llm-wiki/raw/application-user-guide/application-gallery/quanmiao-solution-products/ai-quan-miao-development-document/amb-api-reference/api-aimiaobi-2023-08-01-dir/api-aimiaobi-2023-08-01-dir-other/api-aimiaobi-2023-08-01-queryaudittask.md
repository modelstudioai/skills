# QueryAuditTask - 查询审核结果

查询审核结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/QueryAuditTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/QueryAuditTask)

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

aimiaobi:QueryAuditTask

get

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

ContentAuditTaskId

string

否

审核任务 ID（任务 ID 与文章 ID 二选一）

xxx

ArticleId

string

否

文章 ID（任务 ID 与文章 ID 二选一）

xxxx

WorkspaceId

string

否

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxxx

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

xxxxx

Success

boolean

此次请求是否成功

true

Code

string

错误码

DataNotExists

Message

string

错误消息

错误消息

HttpStatusCode

integer

http 错误码

400

Data

object

异步任务对象

TaskStatus

integer

任务执行状态，0-待执行、1-执行中、2-执行成功、3-暂停、4-执行失败,6-任务取消

1

Content

string

审核时的原文

审核时的原文

AuditTime

string

审核时间

2025-05-13 12:12:12

Response

object

审核结果

Header

object

审核响应头

Event

string

事件

task-failed

ErrorCode

string

错误码

DataNotExists

ErrorMessage

string

错误信息

数据不存在

SessionId

string

对话唯一标识

49eab783-9172-487a-b9df-c6372c47392c

TaskId

string

多轮对话唯一标识

896b733535274d28b1a61c78bc145217

Payload

object

响应体

Output

object

响应体

Text

string

最终响应结果（json 数组结构）

x'x'x

Usage

object

用量

OutputTokens

integer

输出 token

100

InputTokens

integer

输入 token

200

TotalTokens

integer

总 token

300

Status

string

任务执行状态，PENDING-待执行、RUNNING-执行中、SUCCESSED-成功、SUSPENDED-暂停、FAILED-失败、CANCELLED-取消

RUNNING

HtmlContent

string

格式化的审核时的内容

格式化的审核时的内容

Title

string

内容标题

内容标题

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "xxxxx",
  "Success": true,
  "Code": "DataNotExists",
  "Message": "错误消息",
  "HttpStatusCode": 400,
  "Data": {
    "TaskStatus": 1,
    "Content": "审核时的原文",
    "AuditTime": "2025-05-13 12:12:12",
    "Response": {
      "Header": {
        "Event": "task-failed",
        "ErrorCode": "DataNotExists",
        "ErrorMessage": "数据不存在",
        "SessionId": "49eab783-9172-487a-b9df-c6372c47392c",
        "TaskId": "896b733535274d28b1a61c78bc145217"
      },
      "Payload": {
        "Output": {
          "Text": "x'x'x"
        },
        "Usage": {
          "OutputTokens": 100,
          "InputTokens": 200,
          "TotalTokens": 300
        }
      }
    },
    "Status": "RUNNING",
    "HtmlContent": "格式化的审核时的内容\n\n",
    "Title": "内容标题\n\n"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
