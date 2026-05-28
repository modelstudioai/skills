# SubmitDeepWriteTask - 提交深度写作任务

提交深度写作任务。 用户可以根据要研究或分析的主题，填入问题、指令、附件等信息，来提交深度写作任务。该任务会在系统后台调度和执行。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitDeepWriteTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitDeepWriteTask)

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

aimiaobi:SubmitDeepWriteTask

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

否

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-1setzb9xb8m11vrc

Input

string

是

用户的问题

北京2025年新能源汽车发展趋势

Instructions

string

否

指令

请根据北京新能源汽车在汽车品牌、新车发布、能源等方面进行分析

Files

array<object>

否

附件列表

object

否

FileKey

string

否

附件的 OSS 地址

oss://default/aimiaobi-poc/aimiaobi/deep-write-upload/1\_1/xxx.txt

FileDescription

string

否

附件的备注

附件的说明

FileName

string

否

附件的名称

附件的名称

AgentOrchestration

object

否

智能体选配

DataCollectorAgent

object

否

数据收集智能体

Name

string

否

名称

DataCollectorAgent

DataAnalystAgent

object

否

数据分析智能体

Name

string

否

名称

DataAnalystAgent

EnableSearch

boolean

否

开启检索

true

ReporterAgent

object

否

报告智能体

Name

string

否

名称

ReporterAgent

EnableCitation

boolean

否

开启引用

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

任务响应对象

TaskId

string

任务 ID

xbabac91-fdad-44d6-95ce-\*\*\*\*\*\*

Status

string

任务状态

枚举值：

-   in\_progress：运行中。
-   queued：排队中。
-   cancelled：已取消。
-   completed：已完成。
-   failed：失败。

queued

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
    "TaskId": "xbabac91-fdad-44d6-95ce-******",
    "Status": "queued"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
