# GetCustomSourceTopicAnalysisTask - 获取自定义源话题分析任务结果

获取自定义数据源-选题视角分析任务结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetCustomSourceTopicAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetCustomSourceTopicAnalysisTask)

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

aimiaobi:GetCustomSourceTopicAnalysisTask

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

WorkspaceId

string

是

业务空间唯一标识：AgentKey

xxxxx\_p\_efm

TaskId

string

是

任务唯一 ID

c9f226b02cca4f42a84c5e955c39dfd2

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

ErrorMessage

string

错误信息

错误信息

Status

string

任务状态（PENDING：待执行，RUNNING：执行中，SUCCESSED：成功，FAILED：失败，CANCELED：已取消）

SUCCESSED

ParsedNewsSize

integer

解析文件后的新闻数量

10

ClusterCount

integer

聚类后的文档数量

5

MaxClusteredTopicNewsSize

integer

聚合后的最大新闻数量

8

ClusterResults

array<object>

新闻聚合结果列表

clusterResults

object

聚合结果对象

ClusterNews

array<object>

聚合新闻列表（不包含正文）

clusterNews

object

新闻对象

Title

string

新闻标题

新闻标题

Url

string

新闻 Url

http://www.example.com/xxx.html

Topic

string

聚合话题名称

话题名称

usages

object

token 使用情况。可能使用到的付费项为： quanmiaoMax、quanmiaoPlus

long

token 使用数量

200

rt

long

总运行时长，单位毫秒

1000

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

HttpStatusCode

integer

http 状态码

200

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": {
    "ErrorMessage": "错误信息",
    "Status": "SUCCESSED",
    "ParsedNewsSize": 10,
    "ClusterCount": 5,
    "MaxClusteredTopicNewsSize": 8,
    "ClusterResults": [
      {
        "ClusterNews": [
          {
            "Title": "新闻标题\n\n",
            "Url": "http://www.example.com/xxx.html"
          }
        ],
        "Topic": "话题名称"
      }
    ],
    "usages": {
      "key": 200
    },
    "rt": 1000
  },
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "HttpStatusCode": 200
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
