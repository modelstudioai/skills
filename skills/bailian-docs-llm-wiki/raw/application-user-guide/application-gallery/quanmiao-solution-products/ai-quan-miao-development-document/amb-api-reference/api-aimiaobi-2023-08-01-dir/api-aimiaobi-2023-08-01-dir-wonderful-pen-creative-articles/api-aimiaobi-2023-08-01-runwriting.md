# RunWriting - 直接写作

直接写作

## 接口说明

该接口已过时，请参考： [RunWritingV2](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-runwritingv2)

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](https://help.aliyun.com/zh/model-studio/iframe-embedding-scheme)

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunWriting)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunWriting)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

aimiaobi:RunWriting

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runWriting HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

Prompt

string

是

提示词

提示词

TaskId

string

否

任务 ID，多轮对话可复用同一轮任务 ID

**说明**

TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

3f7045e099474ba28ceca1b4eb6d6e21

SessionId

string

否

单轮对话的 ID

3f7045e099474ba28ceca1b4eb6d6e21

OriginSessionId

string

否

重新生成时原始对话的 ID

3f7045e099474ba28ceca1b4eb6d6e21

WritingConfig

object

否

写作配置

Domain

string

否

写作领域

-   media:传媒
    
-   government:政务
    
-   market:营销
    

media

PromptTag

object

否

提示词小助手

NecessaryTips

string

否

必要提示

必要提示

Position

string

否

立场

立场

ReverseWords

string

否

反向词

反向词

Theme

string

否

主题

主题

Tags

array<object>

否

写作时的文体、篇幅、输出语言等控制参数

object

否

写作时的文体、篇幅、输出语言等控制参数

Keyword

string

否

选项的值

10

Tag

string

否

选项的 Tag。例如 gcNumberSizeTag=10

gcNumberSizeTag

UseSearch

boolean

否

是否自动补充素材

true

ReferenceData

object

否

写作时的参考文章数据

Articles

array<object>

否

写作时的参考文章数据

object

否

写作时的参考文章数据

Author

string

否

作者

作者

Content

string

否

内容

文章内容

DocId

string

否

文档-自定义的唯一 ID

文档-自定义的唯一ID

DocUuid

string

否

内部文档唯一标识

2124ca4d48a542d788aa86151e1a8c8b

PubTime

string

否

发布时间

2024-08-28 11:38:28

Source

string

否

来源

央视网

Summary

string

否

文章摘要

文章摘要

Tag

string

否

标签

文章标签

Title

string

否

标题

文章标题

Url

string

否

文章 URL

https://www.example.com/aaa.docx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

BaseLlmResponse

Header

object

响应头

ErrorCode

string

错误码

错误码

ErrorMessage

string

错误信息

错误信息

Event

string

SSE 事件。task-started:开始，task-finished:结束，task-failed:失败

task-started

OriginSessionId

string

父会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

SessionId

string

会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

StatusCode

integer

http 响应码

400

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

TraceId

string

全链路 ID

全链路ID

Payload

object

响应体

Output

object

输出

Articles

array<object>

参照文章

object

参照文章

Author

string

作者

作者

Content

string

内容

文章内容

DocId

string

文档-自定义的唯一 ID

文档-自定义的唯一ID

DocUuid

string

内部文档唯一标识

98229f6001cf4deeb1668191d4eccc75

PubTime

string

发布时间

2024-08-28 11:38:28

Source

string

来源

央视网

Summary

string

文章摘要

文章摘要

Tag

string

标签

文章标签

Title

string

标题

文章标题

Url

string

文章 URL

https://www.example.com/aaa.docx

MiniDoc

array

文章精排之后的片段列表

文章精排之后的片段

string

文章精排之后的片段 \*

文章精排之后的片段

SearchQuery

string

query 改写结果

大模型改变世界

Text

string

文本生成结果

文本生成结果

Usage

object

token 消耗

InputTokens

integer

输入使用的 Token 数量

1

OutputTokens

integer

输出使用的 Token 数量

1

TokenMap

object

token 消耗明细

integer

token 消耗明细

44

TotalTokens

integer

本次调用使用的所有 Token 数总和

2

RequestId

string

请求 ID

3f7045e099474ba28ceca1b4eb6d6e21

End

boolean

此次请求是否结束

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "错误码",
    "ErrorMessage": "错误信息",
    "Event": "task-started",
    "OriginSessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "StatusCode": 400,
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "全链路ID"
  },
  "Payload": {
    "Output": {
      "Articles": [
        {
          "Author": "作者",
          "Content": "文章内容",
          "DocId": "文档-自定义的唯一ID",
          "DocUuid": "98229f6001cf4deeb1668191d4eccc75",
          "PubTime": "2024-08-28 11:38:28",
          "Source": "央视网",
          "Summary": "文章摘要",
          "Tag": "文章标签",
          "Title": "文章标题",
          "Url": "https://www.example.com/aaa.docx"
        }
      ],
      "MiniDoc": [
        "文章精排之后的片段"
      ],
      "SearchQuery": "大模型改变世界",
      "Text": "文本生成结果"
    },
    "Usage": {
      "InputTokens": 1,
      "OutputTokens": 1,
      "TokenMap": {
        "key": 44
      },
      "TotalTokens": 2
    }
  },
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "End": true
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunWriting#workbench-doc-change-demo)。
