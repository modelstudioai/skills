# SubmitCustomHotTopicBroadcastJob - 提交自定义播报单任务

提交自定义播报单任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitCustomHotTopicBroadcastJob)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitCustomHotTopicBroadcastJob)

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

aimiaobi:SubmitCustomHotTopicBroadcastJob

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

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

HotTopicBroadcastConfig

object

是

新闻播报单配置

StepForNewsBroadcastContentConfig

object

是

配置播报单内容

Categories

array

否

选择的频道列表

Categorie

string

否

频道

科技

CustomHotValueWeights

array<object>

否

自定义热度权重

CustomHotValueWeight

object

否

自定义权重

Dimension

string

否

维度 KEY

views

DimensionName

string

否

维度名称

维度名称

Weight

integer

否

权重

1

TopicCount

integer

否

话题数量

10

StepForCustomSummaryStyleConfig

object

是

自定义输出风格配置

SummaryImageCount

integer

否

摘要-配图数量

3

SummaryModel

string

否

摘要模型

qwen-max

SummaryPrompt

string

否

摘要-自定义 Prompt

xxxx

HotTopicVersion

string

否

热点版本

热点版本

Topics

array

否

话题筛选

Topic

string

否

热点主题名称

热点主题名称

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

HttpStatusCode

integer

HTTP 状态码

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
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
