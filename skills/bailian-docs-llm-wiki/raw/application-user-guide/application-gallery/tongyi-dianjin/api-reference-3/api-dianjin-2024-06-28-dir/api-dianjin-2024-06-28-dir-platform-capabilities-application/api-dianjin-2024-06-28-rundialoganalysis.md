# RunDialogAnalysis - 会话分析结果生成

流式接口，获取会话分析结果。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/RunDialogAnalysis)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/RunDialogAnalysis)

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

dianjin:RunDialogAnalysis

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/virtualHuman/dialog/stream/analysis HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

业务空间 id

llm-xxxx

body

object

否

请求体参数。

sessionId

string

是

会话 ID

1759457905S001vejpvd6vej

## 返回参数

名称

类型

描述

示例值

object

ResultCode

success

boolean

是否成功

true

dataType

string

数据类型

null

time

string

时间戳

2024-04-24 11:54:34

errCode

string

错误码

0

message

string

错误信息

ok

data

object

响应数据

dialogAnalysisRespList

array<object>

会话分析结果列表

dialogAnalysisRespList

object

会话分析结果

sessionId

string

会话 ID

1759457905S001vejpvd6vej

gmtCreate

string

会话的创建时间

2024-04-24 11:54:34

status

string

会话分析的任务执行状态

枚举值：

-   success：success。
-   pending：pending。
-   error：error。

success

analysisResp

object

会话分析的结果

dialogLabels

array<object>

会话标签列表

dialogLabel

object

会话标签

name

string

标签名称

二级标签

value

string

标签值

协商还款

dialogSummary

string

会话摘要

\- 是否有资金需求：否\\\\n- 是否有意向：否，客户认为自己已经解决，对当前状态表示不解\\\\n- 是否可营销：否，对话中未表现出对营销信息的兴趣或接受度\\\\n- 待满足需求：客户希望在三天内解决问题

dialogExecPlan

string

会话执行计划

1\. 核实客户账户信息，确认还款情况。\\\\n2. 若未收到还款，联系财务部门确认是否到账延迟。\\\\n3. 若已还款，更新客户记录并致歉。\\\\n4. 跟进客户，确保问题解决。

dialogSop

string

会话 SOP

营销

dialogProcessAnalysis

object

会话过程分析

any

会话过程分析内容

{ "dialogues": \[ { "result": \[ { "value": "开场白", "key": "客服" }, { "value": "拒绝", "key": "客户" } \], "round": 1.0 }, { "result": \[ { "value": "挽留", "key": "客服" }, { "value": "中性", "key": "客户" } \], "round": 2.0 } \], "dialogProcessAnalysisStr": "第一轮对话：客服-开场白，客户-拒绝\\\\n第二轮对话：客服-挽留，客户-中性" }

dialogOpenAnalysis

object

会话开放分析

any

会话开放分析内容

{ "dialogues": \[ { "result": \[ { "value": "开场白", "key": "客服" }, { "value": "拒绝", "key": "客户" } \], "round": 1.0 }, { "result": \[ { "value": "挽留", "key": "客服" }, { "value": "中性", "key": "客户" } \], "round": 2.0 } \], "dialogProcessAnalysisStr": "第一轮对话：客服-开场白，客户-拒绝\\\\n第二轮对话：客服-挽留，客户-中性" }

failNode

array

失败节点列表

failNode

string

失败节点

DIALOG\_OPEN\_ANALYSIS

requestId

string

请求 id

02CD4454-3F2C-57D0-9060-68DEAA1F6993

cost

long

耗时

null

## 示例

正常返回示例

`JSON`格式

```
{
  "success": true,
  "dataType": null,
  "time": "2024-04-24 11:54:34",
  "errCode": 0,
  "message": "ok",
  "data": {
    "dialogAnalysisRespList": [
      {
        "sessionId": "1759457905S001vejpvd6vej",
        "gmtCreate": "2024-04-24 11:54:34\n",
        "status": "success",
        "analysisResp": {
          "dialogLabels": [
            {
              "name": "二级标签",
              "value": "协商还款"
            }
          ],
          "dialogSummary": "- 是否有资金需求：否\\\\n- 是否有意向：否，客户认为自己已经解决，对当前状态表示不解\\\\n- 是否可营销：否，对话中未表现出对营销信息的兴趣或接受度\\\\n- 待满足需求：客户希望在三天内解决问题",
          "dialogExecPlan": "1. 核实客户账户信息，确认还款情况。\\\\n2. 若未收到还款，联系财务部门确认是否到账延迟。\\\\n3. 若已还款，更新客户记录并致歉。\\\\n4. 跟进客户，确保问题解决。",
          "dialogSop": "营销",
          "dialogProcessAnalysis": {
            "key": {
              "dialogues": [
                {
                  "result": [
                    {
                      "value": "开场白",
                      "key": "客服"
                    },
                    {
                      "value": "拒绝",
                      "key": "客户"
                    }
                  ],
                  "round": 1
                },
                {
                  "result": [
                    {
                      "value": "挽留",
                      "key": "客服"
                    },
                    {
                      "value": "中性",
                      "key": "客户"
                    }
                  ],
                  "round": 2
                }
              ],
              "dialogProcessAnalysisStr": "第一轮对话：客服-开场白，客户-拒绝\\n第二轮对话：客服-挽留，客户-中性"
            }
          },
          "dialogOpenAnalysis": {
            "key": {
              "dialogues": [
                {
                  "result": [
                    {
                      "value": "开场白",
                      "key": "客服"
                    },
                    {
                      "value": "拒绝",
                      "key": "客户"
                    }
                  ],
                  "round": 1
                },
                {
                  "result": [
                    {
                      "value": "挽留",
                      "key": "客服"
                    },
                    {
                      "value": "中性",
                      "key": "客户"
                    }
                  ],
                  "round": 2
                }
              ],
              "dialogProcessAnalysisStr": "第一轮对话：客服-开场白，客户-拒绝\\n第二轮对话：客服-挽留，客户-中性"
            }
          }
        },
        "failNode": [
          "DIALOG_OPEN_ANALYSIS"
        ]
      }
    ]
  },
  "requestId": "02CD4454-3F2C-57D0-9060-68DEAA1F6993",
  "cost": 0
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
