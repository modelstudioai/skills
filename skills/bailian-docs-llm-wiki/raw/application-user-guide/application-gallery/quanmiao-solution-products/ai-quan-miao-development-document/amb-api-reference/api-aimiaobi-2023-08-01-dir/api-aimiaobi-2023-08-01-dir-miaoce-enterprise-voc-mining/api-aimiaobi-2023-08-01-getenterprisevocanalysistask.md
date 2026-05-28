# GetEnterpriseVocAnalysisTask - 获取企业VOC挖掘任务结果

获取企业VOC分析任务结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetEnterpriseVocAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetEnterpriseVocAnalysisTask)

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

aimiaobi:GetEnterpriseVocAnalysisTask

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

企业 VOC 分析结果

StatisticsOverview

object

统计概览

Count

integer

总分析数据条数

100

TagDimensionStatistics

object

内容标签统计

TagValueCountStatistic

array<object>

标签值数量统计

tagValueCountStatistic

object

TagName

string

标签名称

xxx

TagTaskType

string

标签挖掘任务类型（单标签：singleTagValue，多标签：multiTagValues，总结概括：summaryAndOverview）

multiTagValues

ValueCount

integer

标签值数量

100

FilterDimensionStatistics

object

筛选标签统计

TagValueCountStatistic

array<object>

标签值数量统计

tagValueCountStatistic

object

TagName

string

标签名称

xxx

TagTaskType

string

标签挖掘任务类型（单标签：singleTagValue，多标签：multiTagValues，总结概括：summaryAndOverview）

multiTagValues

ValueCount

integer

标签值数量

100

Usage

object

消耗量统计

OutputTokens

long

输出 token 数

100

InputTokens

long

输入 token 数

200

Status

string

任务状态（PENDING：待执行，RUNNING：执行中，SUCCESSED：成功，FAILED：失败，CANCELED：已取消）

SUCCESSED

ErrorMessage

string

错误信息

error

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
    "StatisticsOverview": {
      "Count": 100,
      "TagDimensionStatistics": {
        "TagValueCountStatistic": [
          {
            "TagName": "xxx",
            "TagTaskType": "multiTagValues",
            "ValueCount": 100
          }
        ]
      },
      "FilterDimensionStatistics": {
        "TagValueCountStatistic": [
          {
            "TagName": "xxx",
            "TagTaskType": "multiTagValues",
            "ValueCount": 100
          }
        ]
      }
    },
    "Usage": {
      "OutputTokens": 100,
      "InputTokens": 200
    },
    "Status": "SUCCESSED",
    "ErrorMessage": "error"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
