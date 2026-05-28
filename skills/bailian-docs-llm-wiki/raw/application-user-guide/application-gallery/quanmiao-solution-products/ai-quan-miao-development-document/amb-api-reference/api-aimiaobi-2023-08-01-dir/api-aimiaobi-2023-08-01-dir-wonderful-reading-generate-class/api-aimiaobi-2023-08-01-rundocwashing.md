# RunDocWashing - 改写

把一篇文章改换成指定风格。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocWashing)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocWashing)

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

aimiaobi:RunDocWashing

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runDocWashing HTTP/1.1
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

llm-2setzb9x4ewsd

SessionId

string

否

通道 Id

3f7045e099474ba28ceca1b4eb6d6e21

WritingTypeName

string

否

文体类型名字

小红书文体 朋友圈文体 专业新闻文体 政府公文文体 报纸文章文体 意见信文体

WritingTypeRefDoc

string

否

文体示例文章

该值若不为空则按该值优先

ReferenceContent

string

是

要进行改写的文章

文章内容

Topic

string

否

改写文章主题

云南旅游主题

WordNumber

integer

否

改写后的字数要求

500

Prompt

string

否

附加要求提示词

按英文输出

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

1813ceee-7fe5-41b4-87e5-982a4d18cca5

End

boolean

响应包是否结束

false

Header

object

响应头

Event

string

事件类型

task-finished

EventInfo

string

事件描述

模型生成事件

RequestId

string

请求 RequestId

3f7045e099474ba28ceca1b4eb6d6e21

SessionId

string

会话 ID

20247a52-23e2-46fb-943d-309cdee2bc6d

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

TraceId

string

全链路 ID

2150451a17191950923411783e2927

Payload

object

响应体

Output

object

输出

Text

string

输出内容

文本生成结果

Usage

object

token 消耗

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

总 oken 数量

200

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "End": false,
  "Header": {
    "Event": "task-finished",
    "EventInfo": "模型生成事件",
    "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "SessionId": "20247a52-23e2-46fb-943d-309cdee2bc6d",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "2150451a17191950923411783e2927"
  },
  "Payload": {
    "Output": {
      "Text": "文本生成结果"
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
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
