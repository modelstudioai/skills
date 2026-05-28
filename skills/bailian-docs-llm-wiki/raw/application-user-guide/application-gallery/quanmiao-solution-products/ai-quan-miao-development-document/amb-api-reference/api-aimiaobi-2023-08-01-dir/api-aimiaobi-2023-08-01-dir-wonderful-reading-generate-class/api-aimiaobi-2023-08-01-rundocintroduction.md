# RunDocIntroduction - 文档导读

针对一篇文章、视频或者URL，生成文章的导读内容，包含全文总结、关键要点、章节速览（即分段、每段的总结、段落摘要）。此外支持多种多语言的输入和输出。如果用户仅需要对文章进行全文总结，可使用RunDocSummary接口实现，具体请参见https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocIntroduction)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocIntroduction)

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

aimiaobi:RunDocIntroduction

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaodu/stream/runDocIntroduction HTTP/1.1
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

xxxx

DocId

string

是

文档 ID

12345

SessionId

string

是

对话 ID

a3b5eb35-6b28-4cf9-ac09-1dec25ab4df6

SummaryPrompt

string

否

总结内容自定义要求

用英文输出

KeyPointPrompt

string

否

关键点自定义要求

用英文输出

IntroductionPrompt

string

否

导读内容自定义要求

用英文输出

CleanCache

boolean

否

清除缓存

true

referenceContent

string

否

要进行导读的内容，如果不为空，该值优先于 docId

要进行导读的内容

ModelName

string

否

用户自定义模型名称

quanmiao-max、quanmiao-plus

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

success

ErrorMessage

string

错误信息。

success

Event

string

事件类型

task-started

EventInfo

string

事件描述

模型生成事件

SessionId

string

会话 ID

20247a52-23e2-46fb-943d-309cdee2bc6d

TaskId

string

任务 ID

8a9cecb7-6d20-32db-8823-5882c217b647

TraceId

string

全链路 ID

0bd58ea2-dc38-45da-ac02-17f05cb9040b

Payload

object

响应体

Output

object

输出

Introductions

array<object>

分段导读内容数组

introductions

object

Blocks

array<object>

位置信息数组

blocks

object

位置信息

Height

integer

文本块高

600

PageId

integer

文本块所在页号

10

Width

integer

文本块宽

600

X

integer

块左上角 X 坐标

10

Y

integer

块左上角 Y 坐标

10

BeginTime

long

段落开始时间

0

EndTime

long

段落结束时间

1200

StartPageId

integer

多个文本块的起始页号

10

Summary

string

本段摘要

本段摘要内容

Title

string

本段标题

本段标题内容

KeyPoint

string

要点内容

要点1；要点2；

Summary

string

大纲摘要

大纲摘要内容

Usage

object

token 用量

InputTokens

long

输入 Token 数量

100

OutputTokens

long

输出 Token 数量

100

TotalTokens

long

总 Token 数量

200

RequestId

string

请求 Id

C9B5BEA6-E8C4-5861-BE37-D906D516510E

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "success",
    "ErrorMessage": "success",
    "Event": "task-started",
    "EventInfo": "模型生成事件",
    "SessionId": "20247a52-23e2-46fb-943d-309cdee2bc6d",
    "TaskId": "8a9cecb7-6d20-32db-8823-5882c217b647",
    "TraceId": "0bd58ea2-dc38-45da-ac02-17f05cb9040b"
  },
  "Payload": {
    "Output": {
      "Introductions": [
        {
          "Blocks": [
            {
              "Height": 600,
              "PageId": 10,
              "Width": 600,
              "X": 10,
              "Y": 10,
              "BeginTime": 0,
              "EndTime": 1200
            }
          ],
          "StartPageId": 10,
          "Summary": "本段摘要内容",
          "Title": "本段标题内容"
        }
      ],
      "KeyPoint": "要点1；要点2；",
      "Summary": "大纲摘要内容"
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
    }
  },
  "RequestId": "C9B5BEA6-E8C4-5861-BE37-D906D516510E"
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
