# RunContractResultGeneration

该接口用于合同审查模块的审查结果生成，调用大模型返回合同的审查结果、审查风险项、建议修改内容等。传入合同审查文件的ID、审查立场、审查规则，会通过sse的方式增量式返回模型生成的审查结果。

## 接口说明

请确保在使用该接口前，已充分了解法睿产品的收费方式和价格。

-   该接口需要开通法睿商品相关的后付费服务（开通免费），可以使用该账号的 AccessKey 和 AccessSecret 来调用我们的 OpenApi 服务
-   服务的响应结果是以流式的形式来返回（SSE）。
-   接口的调用需要阿里云百炼平台的工作空间权限。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/farui/contract/result/genarate HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

workspaceId

string

是

阿里云百炼平台工作空间 ID

llm-kqtrcpdee4xm29xc

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

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

assistant

object

否

智能体

metaData

object

否

智能体元数据。生成审查结果须传入审查规则：rules、ruleTaskId、customRuleConfig.customRules 三者至少提供其一，全部省略将无法生成审查结果。

customRuleConfig

object

否

自定义规则配置

customRules

array<object>

否

自定义规则列表

object

否

riskLevel

string

否

规则风险等级(high-高风险、medium-中风险、low-低风险)

high

ruleDesc

string

否

规则描述

所有涉及法律引用的合同条款，包括但不限于合同的管辖法律、争议解决机制、合规要求、特定行业法规以及其他法律义务和权利的引用。

ruleTitle

string

否

规则标题

审查条款的合法性

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

ruleTaskId

string

否

生成审查规则任务的 ID

b265b416-ca1f-425d-9340-c968f39624e1

rules

array<object>

否

模型生成的规则列表，规则至少有一条数据

object

否

规则对象，至少有一个

riskLevel

string

否

规则风险等级(high-高风险、medium-中风险、low-低风险)

medium

ruleSequence

string

否

规则序号

2.1

ruleTag

string

否

规则标签（类型）

审查通用条款的常见风险

ruleTitle

string

否

规则标题

审查该合同免责条款中，法定免责情形审查相关的风险。

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

**名称**

**类型**

**描述**

**示例值**

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

result

object

合同审查结果

examineBrief

string

审查结果概述

合同中未明确法定免责条款，尤其是不可抗力的定义和后果，可能在发生不可抗力事件时导致双方权益不明，因此需要进行补充

examineResult

string

审查结论

需要修改

riskLevel

string

规则风险等级(high-高风险、medium-中风险、low-低风险)

high

ruleSequence

string

该审查结果对应的规则序号

"1.1"

ruleTag

string

该审查结果对应的规则标签

审查通用条款的常见风险

ruleTitle

string

该审查结果对应的规则标题

审查该合同免责条款中，法定免责情形审查相关的风险。

subRisks

array<object>

审查结果的风险子项

object

originalContent

string

风险项对应的合同原文

14\. 其他约定事项：

standardOriginalContent

string

合同比对模式下才有该值

resultContent

string

修改后文本

14.1 不可抗力条款14.1.1 不可抗力定义：指在本协议签署后发生的、本协议签署时不能预见的、其发生与后果是无法避免或克服的、妨碍任何一方全部或部分履约的所有事件。上述事件包括但不限于地震、台风、洪水、火灾、战争、国际或国内运输中断、流行病、罢工，以及根据中国法律或一般国际商业惯例认作不可抗力的其他事件。14.1.2 不可抗力的后果：14.1.2.1 如果发生不可抗力事件，影响一方履行其在本协议项下的义务，则在不可抗力造成的延误期内中止履行，而不视为违约。14.1.2.2 宣称发生不可抗力的一方应迅速书面通知其他各方，并在其后的十五(15)天内提供证明不可抗力发生及其持续时间的足够证据。14.1.2.3 如果发生不可抗力事件，各方应立即互相协商，以找到公平的解决办法，并且应尽一切合理努力将不可抗力的影响减少到最低限度。14.1.2.4 金钱债务的迟延责任不得因不可抗力而免除。14.1.2.5 迟延履行期间发生的不可抗力不具有免责效力。

resultType

string

风险项审查结果建议（需修改/需删除/需新增/通过）

需修改

riskBrief

string

风险简述

未定义不可抗力及其后果，可能导致在发生不可抗力时，双方权益无法得到保障

riskClause

string

风险条款名称

不可抗力条款

riskExplain

string

风险点说明

未明确法定免责情形—不可抗力

resultTaskId

string

生成审查结果任务的 ID

eaa56e1e-e205-4f5e-926e-5e2269ae7f68

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

本次调用的使用量

input

integer

输入的文档页数

5

unit

string

单元（固定为 page）

page

httpStatusCode

string

HTTP 状态码

200

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "null",
  "Message": "null",
  "Output": {
    "result": {
      "examineBrief": "合同中未明确法定免责条款，尤其是不可抗力的定义和后果，可能在发生不可抗力事件时导致双方权益不明，因此需要进行补充",
      "examineResult": "需要修改",
      "riskLevel": "high",
      "ruleSequence": "\"1.1\"",
      "ruleTag": "审查通用条款的常见风险",
      "ruleTitle": "审查该合同免责条款中，法定免责情形审查相关的风险。",
      "subRisks": [
        {
          "originalContent": "14. 其他约定事项：",
          "standardOriginalContent": "",
          "resultContent": "14.1 不可抗力条款14.1.1 不可抗力定义：指在本协议签署后发生的、本协议签署时不能预见的、其发生与后果是无法避免或克服的、妨碍任何一方全部或部分履约的所有事件。上述事件包括但不限于地震、台风、洪水、火灾、战争、国际或国内运输中断、流行病、罢工，以及根据中国法律或一般国际商业惯例认作不可抗力的其他事件。14.1.2 不可抗力的后果：14.1.2.1 如果发生不可抗力事件，影响一方履行其在本协议项下的义务，则在不可抗力造成的延误期内中止履行，而不视为违约。14.1.2.2 宣称发生不可抗力的一方应迅速书面通知其他各方，并在其后的十五(15)天内提供证明不可抗力发生及其持续时间的足够证据。14.1.2.3 如果发生不可抗力事件，各方应立即互相协商，以找到公平的解决办法，并且应尽一切合理努力将不可抗力的影响减少到最低限度。14.1.2.4 金钱债务的迟延责任不得因不可抗力而免除。14.1.2.5 迟延履行期间发生的不可抗力不具有免责效力。",
          "resultType": "需修改",
          "riskBrief": "未定义不可抗力及其后果，可能导致在发生不可抗力时，双方权益无法得到保障",
          "riskClause": "不可抗力条款",
          "riskExplain": "未明确法定免责情形—不可抗力"
        }
      ]
    },
    "resultTaskId": "eaa56e1e-e205-4f5e-926e-5e2269ae7f68"
  },
  "RequestId": "744419D0-671A-5997-9840-E8AE48356194",
  "Success": true,
  "Usage": {
    "input": 5,
    "unit": "page"
  },
  "httpStatusCode": "200"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/FaRui/2024-06-28/errorCode)查看更多错误码。

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/FaRui/2024-06-28/RunContractResultGeneration#workbench-doc-change-demo)。
