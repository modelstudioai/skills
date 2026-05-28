# RunQuickWriting - 快速写作

可直接输入写作指令，进行快速写作。

## 接口说明

### [](#接入说明)接入说明：

-   由于 OpenAPI 门户目前对 SSE 推理协议不兼容（无法直接调试），接口 SDK 方式调用示例请参考[妙笔最佳实践](https://help.aliyun.com/zh/model-studio/best-practices-for-miaobi-api/)文档。
-   获取 Java 异步 SDK 的最新版本：请点击[链接](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)获取。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunQuickWriting)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunQuickWriting)

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

aimiaobi:RunQuickWriting

create

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

是

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

TaskId

string

否

任务 ID，多轮对话可复用同一轮任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

Articles

array<object>

否

引用的文章

集合

object

否

文章对象

Title

string

否

文章标题

文章标题

Content

string

否

文章内容

文章内容

Url

string

否

文章 URL

https://www.example.com/aaa.docx

Prompt

string

是

其他写作参数（prompt 和 writingParams 二选一）

请按英文输出

SearchSources

array<object>

否

使用指定的搜索源列表

object

否

搜索源对象

Code

string

否

SystemSearch：系统内置搜索，CustomSemanticSearch：自建语义索引搜索，ThirdSearch：三方 API 搜索

SystemSearch

DatasetName

string

否

数据源唯一标识

QuarkCommonNews

## 返回参数

名称

类型

描述

示例值

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

Text

string

文本生成结果

文本生成结果

Usage

object

Token 用量信息

InputTokens

long

输入使用的 Token 数量

78

OutputTokens

long

输出 Token 数量

34

TotalTokens

long

总 Token 数量

38

RequestId

string

请求 ID

3f7045e099474ba28ceca1b4eb6d6e21

End

boolean

响应包是否结束

false

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "错误码",
    "ErrorMessage": "错误信息",
    "Event": "task-started",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "StatusCode": 400,
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "全链路ID"
  },
  "Payload": {
    "Output": {
      "Text": "文本生成结果"
    },
    "Usage": {
      "InputTokens": 78,
      "OutputTokens": 34,
      "TotalTokens": 38
    }
  },
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "End": false
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

## 变更历史

变更时间

变更内容概要

操作

2025-12-04

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunQuickWriting?updateTime=2025-12-04#workbench-doc-change-demo)
