# RunSummaryGenerate - 摘要生成

内容摘要生成。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunSummaryGenerate)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunSummaryGenerate)

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

aimiaobi:RunSummaryGenerate

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runSummaryGenerate HTTP/1.1
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

Content

string

是

需要生成摘要的内容

创新政务社交媒体功能。鼓励各地区、各部门结合实际，开发政务社交媒体的特色功能，如在线咨询服务、政策解读、互动问答等，增强政务社交媒体的互动性和实用性，提升公众参与度。

Prompt

string

否

自定义摘要 Prompt.

请为上述内容生成一段摘要，字数在100~200字以内。

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

End

boolean

输出是否完成，true 表示完成

Header

object

流式输出 header 头，包含返回通用信息

ErrorCode

string

异常错误码

403

ErrorMessage

string

异常错误信息

Pop sign mismatch, please check.

Event

string

事件类型

result-generated

EventInfo

string

事件描述

模型生成事件

SessionId

string

一次会话 ID

3cd10828-0e42-471c-8f1a-931cde20b035

TaskId

string

一次生成任务 ID

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

TraceId

string

链路 traceid

2150451a17191950923411783e2927

Payload

object

返回结果的 payload,json 结构

Output

object

输出内容对象

Text

string

输出内容

这是测试输出

Usage

object

大模型 token 用量信息

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

RequestId

string

请求唯一 ID

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

## 示例

正常返回示例

`JSON`格式

```
{
  "End": true,
  "Header": {
    "ErrorCode": 403,
    "ErrorMessage": "Pop sign mismatch, please check.",
    "Event": "result-generated",
    "EventInfo": "模型生成事件",
    "SessionId": "3cd10828-0e42-471c-8f1a-931cde20b035",
    "TaskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "TraceId": "2150451a17191950923411783e2927"
  },
  "Payload": {
    "Output": {
      "Text": "这是测试输出"
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
    }
  },
  "RequestId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99"
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
