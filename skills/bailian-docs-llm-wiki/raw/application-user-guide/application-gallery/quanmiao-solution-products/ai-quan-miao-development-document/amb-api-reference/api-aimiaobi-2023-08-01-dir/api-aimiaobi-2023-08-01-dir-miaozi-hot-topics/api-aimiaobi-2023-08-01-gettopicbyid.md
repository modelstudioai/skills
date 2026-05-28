# GetTopicById - 获取热点对象

根据ID获取热点事件信息。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetTopicById)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetTopicById)

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

aimiaobi:GetTopicById

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

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

xxxxx\_p\_efm

Id

string

是

数据 ID

数据ID

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

NoData

Data

object

业务数据

AsyncTaskId

string

异步任务 ID（自定义主题场景下使用）

异步任务ID（自定义主题场景下使用）

CreateUser

string

创建用户 ID（自定义主题场景下使用）

创建用户ID（自定义主题场景下使用）

HotValue

long

热度值

43

Id

string

热榜 ID

热榜ID

Status

string

异步任务状态（自定义事件场景下使用） (PENDING: 待执行, RUNNING: 执行中, SUCCESSED: 成功, SUSPENDED: 暂停, FAILED: 失败, CANCELED: 取消)

PENDING

StructureSummary

array<object>

结构化主题摘要列表

StructureSummary

object

结构化主题摘要对象

DocList

array<object>

生成该标题摘要引用的文章

DocList

object

文章对象

Source

string

文章源

头条

Title

string

文章标题

文章标题

Url

string

文章 URL

http://www.example.com

Summary

string

摘要

摘要

Title

string

标题

标题

Summary

string

热榜摘要

热榜摘要

TaskErrorMessage

string

异步任务失败错误信息

异步任务失败错误信息

TaskStatus

integer

异步任务状态。0-待执行，1-执行中，2-执行成功，3-暂停（暂不使用），4-执行失败，6-任务取消（自定义事件场景下使用）。

14

Topic

string

主题唯一名称

主题唯一名称

TopicSource

string

热榜源，目前支持的热榜源：

-   Toutiao：头条
    
-   Quark：夸克
    
-   Baidu：百度
    
-   Sina：新浪
    
-   Custom：自定义
    
-   Aggregation：热点话题榜
    

Toutiao

Version

string

数据版本

数据版本

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": {
    "AsyncTaskId": "异步任务ID（自定义主题场景下使用）",
    "CreateUser": "创建用户ID（自定义主题场景下使用）",
    "HotValue": 43,
    "Id": "热榜ID",
    "Status": "PENDING",
    "StructureSummary": [
      {
        "DocList": [
          {
            "Source": "头条",
            "Title": "文章标题",
            "Url": "http://www.example.com"
          }
        ],
        "Summary": "摘要",
        "Title": "标题"
      }
    ],
    "Summary": "热榜摘要",
    "TaskErrorMessage": "异步任务失败错误信息",
    "TaskStatus": 14,
    "Topic": "主题唯一名称",
    "TopicSource": "Toutiao",
    "Version": "数据版本"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
