# GetCustomTopicSelectionPerspectiveAnalysisTask - 获取自定义选题视角分析任务结果

获取自定义选题视角分析任务结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetCustomTopicSelectionPerspectiveAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetCustomTopicSelectionPerspectiveAnalysisTask)

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

aimiaobi:GetCustomTopicSelectionPerspectiveAnalysisTask

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

xxxxx\_p\_efm

TaskId

string

是

任务唯一 ID

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

0dbf1055f8a2475d99904c3b76a0ffba

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

CustomViewPointsResult

object

自定义选题分析任务结果

Attitudes

array<object>

自定义观点列表。默认会根据 Prompt 输入生成一个观点

Attitude

object

Attitude

string

当前观点

当前观点

AttitudeType

string

观点类型

观点类型

Ratio

string

当前观点占比

当前观点占比

ViewPoints

array<object>

选题视角列表

ViewPoint

object

Outlines

array<object>

大纲

Outline

object

Outline

string

大纲

大纲

Summary

string

大纲摘要

大纲摘要

Point

string

生成的视角

视角

Summary

string

摘要

摘要

Topic

string

热点主题事件

热点主题事件

ErrorMessage

string

错误信息

错误信息

Status

string

任务状态 (PENDING: 待执行, RUNNING: 执行中, SUCCESSED: 成功, SUSPENDED: 暂停, FAILED: 失败, CANCELED: 取消)

FAILED

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
    "CustomViewPointsResult": {
      "Attitudes": [
        {
          "Attitude": "当前观点",
          "AttitudeType": "观点类型",
          "Ratio": "当前观点占比",
          "ViewPoints": [
            {
              "Outlines": [
                {
                  "Outline": "大纲",
                  "Summary": "大纲摘要"
                }
              ],
              "Point": "视角",
              "Summary": "摘要"
            }
          ]
        }
      ],
      "Topic": "热点主题事件"
    },
    "ErrorMessage": "错误信息",
    "Status": "FAILED"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
