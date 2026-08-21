# ExportCustomSourceAnalysisTask - 导出自定义源-话题分析任务结果

导出-自定义数据源-选题视角分析任务结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ExportCustomSourceAnalysisTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ExportCustomSourceAnalysisTask)

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

aimiaobi:ExportCustomSourceAnalysisTask

get

\*全部资源

`*`

无

无

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

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

ExportType

string

否

导出格式类型，默认 jsonLine jsonline: 导出为 jsonLine 格式 excel：导出为 excel 格式

jsonLine

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

PlainResult

Code

string

状态码

NoData

Data

string

可公网访问的 URL

http://www.example.com/xxx.jsonLine

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

文件返回格式为 jsonLine，每行为一个 json 对象。json 对象格式如下：

字段名称

字段类型

字段描述

topic

string

话题名称

topicSummaryResult

array<TopicSummaryResult>

话题摘要列表

hotViewPointsResult

HotViewPointsResult

热门视角分析结果

timedViewPointsResult

TimedViewPointsResult

时效性视角分析结果

webReviewPointsResult

WebReviewPointsResult

网友视角分析结果

freshViewPointsResult

FreshViewPointsResult

新颖视角分析结果

## TopicSummaryResult（话题摘要）

字段名称

字段类型

字段描述

summaries

array<SummaryItem>

话题摘要列表

### SummaryItem（话题摘要）

字段名称

字段类型

字段描述

title

string

话题摘要标题

summary

string

话题摘要内容

docList

array<DocItem>

摘要引用的文档列表

### DocItem（引用的文档）

字段名称

字段类型

字段描述

title

string

文档标题

url

string

文档链接

source

string

文档来源

## HotViewPointsResult（热门视角分析结果）

字段名称

字段类型

字段描述

attitudes

array<HotAttitudeItem>

热门视角列表

### HotAttitudeItem（热门视角）

字段名称

字段类型

字段描述

attitude

string

热门视角

attitudeType

string

热门视角类型

news

array<HotNewsItem>

热门视角引用的文章列表

ratio

string

该热门视角在整个话题中的占比

viewPoints

array<HotViewPointItem>

热门视角的策划提案列表

### HotNewsItem（热门视角引用的文章）

字段名称

字段类型

字段描述

title

string

文章标题

url

string

文章链接

source

string

文章来源

### HotViewPointItem（热门视角选题）

字段名称

字段类型

字段描述

point

string

选题策划方向

summary

string

选题策划方向的概要

outlines

array<OutlineItem>

选题策划方向的提纲

### OutlineItem

字段名称

字段类型

字段描述

outline

string

提纲标题

summary

string

提纲概要

## TimedViewPointsResult（时效性视角分析结果）

字段名称

字段类型

字段描述

attitudes

array<TimedAttitudeItem>

时效性视角列表

### TimedAttitudeItem（时效性视角）

字段名称

字段类型

字段描述

docUuid

string

新闻唯一标识

title

string

新闻标题

url

string

新闻链接

source

string

新闻来源

pubTime

string

新闻发布时间

viewPoints

array<TimedViewPointItem>

时效性视角的策划提案列表

### TimedViewPointItem（时效性视角选题）

字段名称

字段类型

字段描述

point

string

选题策划方向

summary

string

选题策划方向的概要

outlines

array<OutlineItem>

选题策划方向的提纲

### OutlineItem

字段名称

字段类型

字段描述

outline

string

提纲标题

summary

string

提纲概要

## WebReviewPointsResult（网友视角分析结果）

字段名称

字段类型

字段描述

attitudes

array<WebReviewAttitudeItem>

网友视角列表

### WebReviewAttitudeItem（网友视角）

字段名称

字段类型

字段描述

attitude

string

网友视角

attitudeType

string

网友视角类型

ratio

string

该网友视角在整个话题中的占比

comments

array<WebReviewCommentItem>

网友评论列表

viewPoints

array<WebReviewViewPointItem>

网友视角的策划提案列表

### WebReviewCommentItem（网友评论）

字段名称

字段类型

字段描述

text

string

网友评论

source

string

网友评论来源

url

string

网友评论来源新闻链接

title

string

网友评论来源新闻标题

### WebReviewViewPointItem（网友视角选题）

字段名称

字段类型

字段描述

point

string

选题策划方向

summary

string

选题策划方向的概要

outlines

array<OutlineItem>

选题策划方向的提纲

### OutlineItem

字段名称

字段类型

字段描述

outline

string

提纲标题

summary

string

提纲概要

## FreshViewPointsResult（）

字段名称

字段类型

字段描述

attitudes

array<FreshAttitudeItem>

新颖视角列表

### FreshAttitudeItem（新颖视角）

字段名称

字段类型

字段描述

viewPoints

array<FreshViewPointItem>

新颖视角的策划提案列表

### FreshViewPointItem（新颖视角选题）

字段名称

字段类型

字段描述

point

string

选题策划方向

summary

string

选题策划方向的概要

outlines

array<OutlineItem>

选题策划方向的提纲

### OutlineItem

字段名称

字段类型

字段描述

outline

string

提纲标题

summary

string

提纲概要

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": "http://www.example.com/xxx.jsonLine\n",
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ExportCustomSourceAnalysisTask#workbench-doc-change-demo)。
