# GetEnterpriseVocAnalysisTask - 获取企业VOC分析任务结果

获取企业VOC分析任务结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.alibabacloud.com/api/QuanMiaoLightApp/2024-08-01/GetEnterpriseVocAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.alibabacloud.com/api/QuanMiaoLightApp/2024-08-01/GetEnterpriseVocAnalysisTask)

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

quanmiaolightapp:GetEnterpriseVocAnalysisTask

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/quanmiao/lightapp/getEnterpriseVocAnalysisTask HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

否

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

taskId

string

否

任务 ID

a3d1c2ac-f086-4a21-9069-f5631542f5a2

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

Id of the request

117F5ABE-CF02-5502-9A3F-E56BC9081A64

code

string

错误码

NoPermission

httpStatusCode

integer

Http 状态码

403

message

string

响应失败时的消息

无权限访问接口

success

boolean

true:此次接口响应成功,false:响应失败

false

data

object

结果对象

status

string

任务状态(PENDING:待执行,RUNNING:执行中,SUCCESSED:成功,FAILED:失败,CANCELED:已取消)

PENDING

errorMessage

string

错误信息

任务错误消息

usage

object

消耗量统计

outputTokens

integer

输出 Token 数量

2

inputTokens

integer

输入 token 量

1

statisticsOverview

object

统计概览

count

integer

总分析数据条数

17

tagDimensionStatistics

object

标签统计

tagValueCountStatistic

array<object>

标签值数量统计

tagValueCountStatistic

object

标签值数量统计

tagName

string

标签名称

标签名称

valueCount

integer

标签值数量

10

filterDimensionStatistics

object

筛选标签统计

tagValueCountStatistic

array<object>

标签值数量统计

tagValueCountStatistic

object

标签值数量统计

tagName

string

标签名称

标签名称

valueCount

integer

标签值数量

10

modelId

string

此次使用的模型 ID

qwen-max

modelName

string

此次使用的模型名称

千问-MAX

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "code": "NoPermission",
  "httpStatusCode": 403,
  "message": "无权限访问接口",
  "success": false,
  "data": {
    "status": "PENDING",
    "errorMessage": "任务错误消息\n\n",
    "usage": {
      "outputTokens": 2,
      "inputTokens": 1
    },
    "statisticsOverview": {
      "count": 17,
      "tagDimensionStatistics": {
        "tagValueCountStatistic": [
          {
            "tagName": "标签名称",
            "valueCount": 10
          }
        ]
      },
      "filterDimensionStatistics": {
        "tagValueCountStatistic": [
          {
            "tagName": "标签名称\n",
            "valueCount": 10
          }
        ]
      }
    },
    "modelId": "qwen-max",
    "modelName": "千问-MAX"
  }
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.alibabacloud.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
