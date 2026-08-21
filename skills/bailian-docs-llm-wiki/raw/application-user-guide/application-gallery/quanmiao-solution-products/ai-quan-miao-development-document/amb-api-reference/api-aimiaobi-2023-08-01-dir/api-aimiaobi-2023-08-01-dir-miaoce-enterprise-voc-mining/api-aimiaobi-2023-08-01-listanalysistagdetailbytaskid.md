# ListAnalysisTagDetailByTaskId - 根据任务ID获取标签分析明细列表

分页获取企业VOC分析任务明细列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAnalysisTagDetailByTaskId)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAnalysisTagDetailByTaskId)

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

aimiaobi:ListAnalysisTagDetailByTaskId

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

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

TaskId

string

是

任务唯一 ID

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

xxx

Categories

array

否

分类筛选列表

string

否

分类筛选

分类1

NextToken

string

否

下一页标识

token-xxxx

MaxResults

integer

否

每页最大数量

10

Size

integer

否

请求记录数

3

Current

integer

否

当前页码

1

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

array<object>

标签挖掘分类明细列表

data

object

标签挖掘分类明细

Id

long

数据主键 ID

112

TaskId

string

任务 ID

xxx

TagTaskType

string

标签挖掘任务类型（单标签：singleTagValue，多标签：multiTagValues，总结概括：summaryAndOverview）

summaryAndOverview

Content

string

标签内容

xxx

ContentTags

array<object>

标签内容列表

contentTags

object

标签值列表

TagName

string

标签名称

xxx

SummaryOverview

string

总结概括

xxx

Tags

array

标签值列表

tags

string

标签值

标签值列表

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

NextToken

string

下一页标识

token-xxxx

MaxResults

integer

每页最大数量

10

TotalCount

integer

总数

10

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": [
    {
      "Id": 112,
      "TaskId": "xxx",
      "TagTaskType": "summaryAndOverview",
      "Content": "xxx",
      "ContentTags": [
        {
          "TagName": "xxx",
          "SummaryOverview": "xxx",
          "Tags": [
            "标签值列表"
          ]
        }
      ]
    }
  ],
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "NextToken": "token-xxxx",
  "MaxResults": 10,
  "TotalCount": 10
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
