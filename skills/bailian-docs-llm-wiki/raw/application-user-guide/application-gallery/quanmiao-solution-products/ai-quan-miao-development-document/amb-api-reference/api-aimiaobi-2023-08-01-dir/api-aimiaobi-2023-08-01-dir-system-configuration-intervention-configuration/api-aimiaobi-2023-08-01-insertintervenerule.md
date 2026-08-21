# InsertInterveneRule - 插入干预规则

插入干预规则。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/InsertInterveneRule)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/InsertInterveneRule)

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

aimiaobi:InsertInterveneRule

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

InterveneRuleConfig

object

否

干预规则配置

AnswerConfig

array<object>

否

答案配置

AnswerConfig

object

否

答案配置项

AnswerType

integer

否

答案类型

枚举值：

-   1-定向回复：1-定向回复。
-   0-统一回复： 0-统一回复。

0

Message

string

否

答案内容

抱歉我无法回答

Namespace

string

否

命名空间

枚举值：

-   namespace\_writing\_query （写作输入干预）： namespace\_writing\_query （写作输入干预）。
-   namespace\_qa\_result （问答结果干预）： namespace\_qa\_result （问答结果干预）。
-   namespace\_qa\_query （问答输入干预）：namespace\_qa\_query （问答输入干预）。
-   namespace\_writing\_result （写作结果干预）： namespace\_writing\_result （写作结果干预）。

namespace\_qa\_query

EffectConfig

object

否

生效配置

EffectType

integer

否

生效类型

枚举值：

-   0-永久生效 ：0-永久生效 。
-   1-按时间生效：1-按时间生效。

0

EndTime

string

否

结束时间

2023-03-28 06:04:29

StartTime

string

否

开始时间

2023-03-28 06:04:29

InterveneConfigList

array<object>

否

干预配置列表

InterveneConfigList

object

否

Id

string

否

id

37249

OperationType

integer

否

操作类型

枚举值：

-   0-新建：0-新建。
-   1-更新 ： 1-更新 。
-   2-删除：2-删除。

0

Query

string

否

干预 query 配置

早上好

InterveneType

integer

否

干预类型

枚举值：

-   0-相似问干预项目：0-相似问干预项目。
-   2-正则表达式干预项 ： 2-正则表达式干预项 。
-   3-关键词库干预项：3-关键词库干预项。
-   4-URL干预： 4-URL干预。
-   1-关键词表达式干预项：1-关键词表达式干预项。

0

NamespaceList

array

否

命名空间列表

NamespaceList

string

否

干预维度

枚举值：

-   namespace\_writing\_image （智能配图）：namespace\_writing\_image （智能配图）。
-   namespace\_qa\_query （问答输入干预）：namespace\_qa\_query （问答输入干预）。
-   namespace\_qa\_article （问答参考）：namespace\_qa\_article （问答参考）。
-   namespace\_writing\_article （写作参考）：namespace\_writing\_article （写作参考）。
-   namespace\_qa\_result （问答结果干预）：namespace\_qa\_result （问答结果干预）。
-   namespace\_writing\_result （写作结果干预）：namespace\_writing\_result （写作结果干预）。
-   namespace\_writing\_query （写作输入干预）：namespace\_writing\_query （写作输入干预）。

namespace\_qa\_query （问答输入干预）

RuleId

long

否

规则 Id

2

RuleName

string

否

规则名字

tf-test-rule

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

success

Data

object

业务数据

RuleId

long

规则 id

12345

Code

integer

干预服务返回的状态码

200

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

RequestId

string

请求唯一标识

DD656AF9-0839-521A-A3D2-F320009F9C87

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "success",
  "Data": {
    "RuleId": 12345,
    "Code": 200
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "DD656AF9-0839-521A-A3D2-F320009F9C87",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
