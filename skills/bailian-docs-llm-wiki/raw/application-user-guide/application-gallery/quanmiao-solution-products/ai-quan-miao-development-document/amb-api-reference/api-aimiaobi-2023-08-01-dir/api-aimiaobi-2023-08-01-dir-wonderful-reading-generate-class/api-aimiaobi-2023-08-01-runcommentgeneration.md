# RunCommentGeneration - 客户之声预测

针对指定文章，预测用户之声。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunCommentGeneration)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunCommentGeneration)

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

aimiaobi:RunCommentGeneration

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runCommentGeneration HTTP/1.1
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

路径参数，阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-3kcs1w3lltrtbfkr

SessionId

string

否

对话 Id

3f7045e099474ba28ceca1b4eb6d6e21

Length

string

否

一条评论的长度

20

NumComments

string

是

评论的条数

10

Style

string

否

评论的风格

积极正面

SourceMaterial

string

是

要评论的文章

ps5是sony新一代的游戏机，他创新性的...

AllowEmoji

boolean

否

是否允许使用表情默认为 false

true

Type

object

是

评论类型

key 可选值

-   emotion （情感表达型）
-   opinion （观点阐述型）
-   interaction （互动交流型）
-   experience （经验分享型）
-   humor （幽默调侃型）

{"emotion":"50","opinion":"50"}

Sentiment

object

是

情感倾向

key 可选值

-   positive （正向）
-   neutral （中立）
-   negative （负向）

{"positive":"50","negative":"50"}

LengthRange

object

是

长度范围

key 可选值

-   short （20 字以内）
-   medium （20-50 字）
-   long （50-100 字）

{"short":"50","long":“50”}

ExtraInfo

string

否

补充要求

不要输出额外其他信息

ModelId

string

否

模型 id

quanmiao-max、quanmiao-plus

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

3f7045e099474ba28ceca1b4eb6d6e21

End

boolean

是否结束

Header

object

返回结果的 header

Event

string

event 名称

result-generated

EventInfo

string

事件描述

可空

RequestId

string

请求 RequestId

1813ceee-7fe5-41b4-87e5-982a4d18cca5

SessionId

string

对话 ID

3f7045e099474ba28ceca1b4eb6d6e21

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

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

Text

string

输出内容

评论内容

Usage

object

token 用量

InputTokens

long

输入使用的 Token 数量

1

OutputTokens

long

输出 Token 数量

2

TotalTokens

long

总 token 数量

3

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "End": true,
  "Header": {
    "Event": "result-generated\n",
    "EventInfo": "可空\n",
    "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "0bd58ea2-dc38-45da-ac02-17f05cb9040b"
  },
  "Payload": {
    "Output": {
      "Text": "评论内容"
    },
    "Usage": {
      "InputTokens": 1,
      "OutputTokens": 2,
      "TotalTokens": 3
    }
  }
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
