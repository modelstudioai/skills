# ListPlanningProposal - 获取选题策划列表

获取选题策划列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListPlanningProposal)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListPlanningProposal)

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

aimiaobi:ListPlanningProposal

list

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

ViewPointType

string

是

选题策划类型

-   CustomViewPoints：自定义视角
    
-   HotViewPoints：热门视角
    
-   TimedViewPoints：时效性视角
    
-   WebReviewPoints：网友视角
    
-   FreshViewPoints：新颖视角
    

CustomViewPoints

Titles

array

否

选题策划标题筛选，对应各个选题策划类型的视角名称

Title

string

否

视角筛选

标题 \*

CustomViewPointId

string

否

自定义视角 ID（用于自定义视角选题策划场景）

e7b26a9e1211444db8f0a984361a5e0f

CustomViewPointIds

array

否

自定义视角 ID 列表（用于自定义视角选题策划场景）

CustomViewPointId

string

否

自定义视角 ID（用于自定义视角选题策划场景） \*

3c67e87fc9044a8aae534f617195ab31

TopicSource

string

是

热榜源

热榜源

Topic

string

是

热榜主题

热榜主题

TopicVersion

string

否

热点事件数据版本

2024-09-10\_08

NextToken

string

否

下一页的 Token

下一页的Token

MaxResults

integer

否

最大返回结果数

73

## 返回参数

名称

类型

描述

示例值

object

PageResult2

Code

string

状态码

NoData

Data

array<object>

业务数据

Data

object

选题策划对象

Outlines

array<object>

大纲列表

Outline

object

大纲对象

Outline

string

大纲

大纲

Summary

string

大纲摘要

大纲摘要

Summary

string

摘要

摘要

Title

string

标题

标题

HttpStatusCode

integer

http 状态码

200

MaxResults

integer

最大返回结果数

77

Message

string

错误说明

success

NextToken

string

下一页的 token

下一页的token

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

TotalCount

integer

总数

80

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": [
    {
      "Outlines": [
        {
          "Outline": "大纲",
          "Summary": "大纲摘要"
        }
      ],
      "Summary": "摘要",
      "Title": "标题"
    }
  ],
  "HttpStatusCode": 200,
  "MaxResults": 77,
  "Message": "success",
  "NextToken": "下一页的token",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "TotalCount": 80
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
