# GetInterveneRuleDetail - 获得干预规则的详情

获得干预项规则详情。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetInterveneRuleDetail)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetInterveneRuleDetail)

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

aimiaobi:GetInterveneRuleDetail

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

2daaa2e0c209xb26acb97009ea77bd4b\_p\_efm

RuleId

long

否

规则 id

12345

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

0

Data

object

业务数据

InterveneRuleDetail

object

规则详情结构

AnswerConfig

array<object>

答案信息配置

AnswerConfig

object

AnswerType

integer

答案类型

枚举值：

-   0-统一回复：0-统一回复。
-   1-定向回复 ：1-定向回复 。

0

Message

string

答案内容

早上好

Namespace

string

命名空间

枚举值：

-   namespace\_writing\_query （写作输入干预）： namespace\_writing\_query （写作输入干预）。
-   namespace\_qa\_result （问答结果干预）： namespace\_qa\_result （问答结果干预）。
-   namespace\_qa\_query （问答输入干预）：namespace\_qa\_query （问答输入干预）。
-   namespace\_writing\_result （写作结果干预）： namespace\_writing\_result （写作结果干预）。

namespace\_qa\_query

EffectConfig

object

生效配置

EffectType

integer

生效类型

枚举值：

-   0-永久生效 ：0-永久生效 。
-   1-按时间生效：1-按时间生效。

0

EndTime

string

结束时间

2023-11-25 14:21:15

StartTime

string

开始时间

2023-11-25 14:21:15

InterveneType

integer

干预类型

枚举值：

-   3-关键词库干预项 ：3-关键词库干预项 。
-   0-相似问干预项目 ：0-相似问干预项目 。
-   2-正则表达式干预项 ： 2-正则表达式干预项 。
-   4-URL干预：4-URL干预。
-   1-关键词表达式干预项：1-关键词表达式干预项。

0

NamespaceList

array

命名空间列表

NamespaceList

string

干预维度

枚举值：

-   namespace\_writing\_image （智能配图）：namespace\_writing\_image （智能配图）。
-   namespace\_qa\_query （问答输入干预）：namespace\_qa\_query （问答输入干预）。
-   namespace\_qa\_article （问答参考）：namespace\_qa\_article （问答参考）。
-   namespace\_writing\_article （写作参考）：namespace\_writing\_article （写作参考）。
-   namespace\_qa\_result （问答结果干预）：namespace\_qa\_result （问答结果干预）。
-   namespace\_writing\_result （写作结果干预）：namespace\_writing\_result （写作结果干预）。
-   namespace\_writing\_query （写作输入干预）：namespace\_writing\_query （写作输入干预）。

namespace\_qa\_query

RuleId

long

规则 id

100418

RuleName

string

规则名字

规则001

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

428DCC0D-3C63-5306-BD1B-124396AB97BE

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": 0,
  "Data": {
    "InterveneRuleDetail": {
      "AnswerConfig": [
        {
          "AnswerType": 0,
          "Message": "早上好",
          "Namespace": "namespace_qa_query"
        }
      ],
      "EffectConfig": {
        "EffectType": 0,
        "EndTime": "2023-11-25 14:21:15",
        "StartTime": "2023-11-25 14:21:15"
      },
      "InterveneType": 0,
      "NamespaceList": [
        "namespace_qa_query"
      ],
      "RuleId": 100418,
      "RuleName": "规则001"
    },
    "Code": 0
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "428DCC0D-3C63-5306-BD1B-124396AB97BE",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
