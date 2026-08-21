# SubmitTopicSelectionPerspectiveAnalysisTask - 提交选题热点分析任务

提交选题热点分析任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitTopicSelectionPerspectiveAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitTopicSelectionPerspectiveAnalysisTask)

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

aimiaobi:SubmitTopicSelectionPerspectiveAnalysisTask

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

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

xxxxx\_p\_efm

Documents

array<object>

否

待分析的文档列表。（documents 与 topic 二者至少传一个）

Document

object

否

文档列表信息

Author

string

否

作者

作者

Comments

array<object>

否

内容列表

object

否

对象

Text

string

否

内容

内容

Username

string

否

用户名

用户名

Content

string

是

内容

文章内容

PubTime

string

否

发布时间。格式：YYYY-MM-dd HH:mm:ss

2024-01-22 10:29:00

Source

string

否

文章来源

新浪

Summary

string

否

摘要

文章摘要

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

Topic

string

否

待分析的主题名（documents 与 topic 二者至少传一个）

待分析的主题名（documents与topic二者至少传一个）

PerspectiveTypes

array

否

要分析的选题视角任务，默认为空，空表示分析所有任务。 (TopicSummary: 主题事件摘要, HotViewPoints: 热门视角选题, TimedViewPoints: 时效视角选题, WebReviewPoints: 网评视角选题, FreshViewPoints: 新颖视角选题)

PerspectiveType

string

否

要分析的选题视角任务

TopicSummary

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

TaskId

string

任务唯一 ID

3f7045e099474ba28ceca1b4eb6d6e21

TaskName

string

任务名称

任务名称

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
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TaskName": "任务名称"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
