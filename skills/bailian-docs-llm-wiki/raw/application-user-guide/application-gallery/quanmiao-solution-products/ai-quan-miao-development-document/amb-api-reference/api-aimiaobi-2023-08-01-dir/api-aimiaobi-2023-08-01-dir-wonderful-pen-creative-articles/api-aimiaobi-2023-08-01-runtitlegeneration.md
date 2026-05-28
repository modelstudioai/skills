# RunTitleGeneration - 标题生成

妙笔：标题生成。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunTitleGeneration)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunTitleGeneration)

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

aimiaobi:RunTitleGeneration

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runTitleGeneration HTTP/1.1
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

llm-xxx

ReferenceData

object

是

要生成标题的数据

Contents

array

是

正文列表

string

是

正文

xxx

TaskId

string

否

关联创作文章唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

xxxx

TitleCount

string

否

标题生成个数，最大 10 个。

10

DeduplicatedTitles

array

否

新生成的标题 需要与之去重的标题集合。所有标题字数最多 5K 个字

string

否

待去重的标题

标题xxxx

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

AccessForbid

ErrorMessage

string

错误码消息。

xxx

Event

string

SSE 事件。

task-failed

SessionId

string

会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

StatusCode

integer

状态码。

400

TaskId

string

任务 ID

50a1cc8e-717e-4a2b-a76b-dc9734a8564b

TraceId

string

全链路 ID

0a3d448f17000139741898287e0eb3

Payload

object

响应体

Output

object

输出

Text

string

文章标题

xxx

Usage

object

token 用量

InputTokens

long

输入使用的 Token 数量

1

OutputTokens

long

输出使用的 Token 数量

1

TotalTokens

long

本次调用使用的所有 Token 数总和

2

RequestId

string

请求唯一标识

94512A33-8EC1-5452-A793-5C91F18ED2F0

HttpStatusCode

string

http 状态码

200

Code

string

状态码

AccessForbid

Message

string

错误说明

数据不存在

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "AccessForbid",
    "ErrorMessage": "xxx",
    "Event": "task-failed",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "StatusCode": 400,
    "TaskId": "50a1cc8e-717e-4a2b-a76b-dc9734a8564b",
    "TraceId": "0a3d448f17000139741898287e0eb3"
  },
  "Payload": {
    "Output": {
      "Text": "xxx"
    },
    "Usage": {
      "InputTokens": 1,
      "OutputTokens": 1,
      "TotalTokens": 2
    }
  },
  "RequestId": "94512A33-8EC1-5452-A793-5C91F18ED2F0",
  "HttpStatusCode": 200,
  "Code": "AccessForbid",
  "Message": "数据不存在",
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
