# RunContractRuleGeneration - 生成合同审查规则

该接口用于合同审查模块的智能规则生成，调用大模型返回合同的审查规则和对应风险。传入合同审查文件的ID、审查立场，会通过sse的方式增量式返回模型生成的审查规则。

## 接口说明

请确保在使用该接口前，已充分了解法睿产品的收费方式和价格。

-   该接口需要开通法睿商品相关的后付费服务（开通免费），可以使用该账号的 AccessKey 和 AccessSecret 来调用我们的 OpenApi 服务
-   服务的响应结果是以流式的形式来返回（SSE）。
-   接口的调用需要阿里云百炼平台的工作空间权限。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/FaRui/2024-06-28/RunContractRuleGeneration)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/farui/contract/rule/genarate HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

appId

string

否

应用 ID

farui

stream

boolean

否

是否是流式输出

true

workspaceId

string

否

阿里云百炼平台工作空间 ID

llm-9w5y60lseff0jiqm

assistant

object

否

智能体

metaData

object

否

智能体元数据

fileId

string

否

文件 ID。

9a6b1ba60d9944249363ec3cc1529b7b

position

string

否

审查立场，0=中立，1=甲方，2=乙方

1

type

string

否

智能体类型

contract\_examime

version

string

否

智能体版本

1.0.0

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Code

string

错误 Code 码

null

Message

string

请求异常，返回具体异常错误信息。

null

Output

object

输出信息

ruleTaskId

string

生成规则任务的 ID

b265b416-ca1f-425d-9340-c968f39624e9

rules

array<object>

模型生成的规则（增量式）

rules

object

riskLevel

string

规则风险等级(high-高风险、medium-中风险、low-低风险)

medium

ruleSequence

string

规则序号

1.1

ruleTag

string

规则标签（类型）

审查条款的合法性

ruleTitle

string

规则标题

审查该合同标的条款中，标的合法性相关的风险

RequestId

string

阿里云为该请求生成的唯一标识符。

744419D0-671A-5997-9840-E8AE48356194

Success

boolean

是否调用成功。true：调用成功。 false：调用失败。

True

Usage

object

本次调用的使用量（合同审查按页码计费）

input

long

输入的文档页数

5

unit

string

单元（固定为 page）

page

httpStatusCode

integer

HTTP 状态码

200

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": null,
  "Message": null,
  "Output": {
    "ruleTaskId": "b265b416-ca1f-425d-9340-c968f39624e9",
    "rules": [
      {
        "riskLevel": "medium",
        "ruleSequence": 1.1,
        "ruleTag": "审查条款的合法性",
        "ruleTitle": "审查该合同标的条款中，标的合法性相关的风险"
      }
    ]
  },
  "RequestId": "744419D0-671A-5997-9840-E8AE48356194",
  "Success": true,
  "Usage": {
    "input": 5,
    "unit": "page"
  },
  "httpStatusCode": 200
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/FaRui/2024-06-28/errorCode)查看更多错误码。
