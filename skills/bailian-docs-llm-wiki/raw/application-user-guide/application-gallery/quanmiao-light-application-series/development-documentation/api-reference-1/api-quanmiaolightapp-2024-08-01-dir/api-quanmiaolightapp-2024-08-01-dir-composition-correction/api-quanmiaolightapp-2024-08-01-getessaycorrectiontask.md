# GetEssayCorrectionTask - 获取作文批改任务结果

获取作文批改结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetEssayCorrectionTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetEssayCorrectionTask)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

quanmiaolightapp:GetEssayCorrectionTask

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/quanmiao/lightapp/getEssayCorrectionTask HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

workspaceId

string

否

[百炼业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

taskId

string

否

任务唯一标识

a3d1c2ac-f086-4a21-9069-f5631542f5a2

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

requestId

string

Id of the request

117F5ABE-CF02-5502-9A3F-E56BC9081A64

code

string

错误码

successful

httpStatusCode

integer

Http 状态码

200

message

string

响应失败时的消息

successful

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

results

array<object>

结果列表

array<object>

结果对象

customId

string

xxx

1

errorMessage

string

报错信息（当报错时，此字段会有值）

触发模型限流

errorCode

string

错误码（当报错时，此字段会有值）

RateLimit

result

string

评阅结果

评阅结果

score

integer

作文审阅得分

58

dimensionResults

array<object>

各维度评分结果（自定义维度模式）

object

维度评分结果

name

string

维度名称

内容完整度

analysis

string

优劣势分析

文章内容较为完整，涵盖了题目的核心要求，但部分论述略显简略。

score

number

得分

25.5

maxScore

number

满分

30

overallComment

string

总评

整体表现良好，建议在论述深度上进一步加强。

usage

[ModelUsage](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-struct-modelusage)

单个任务的 token 消耗数

totalUsage

[ModelUsage](https://help.aliyun.com/zh/model-studio/api-quanmiaolightapp-2024-08-01-struct-modelusage)

所有任务总模型 token 消耗数

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "code": "successful",
  "httpStatusCode": 200,
  "message": "successful",
  "success": false,
  "data": {
    "status": "PENDING",
    "errorMessage": "任务错误消息\n\n",
    "results": [
      {
        "customId": "1",
        "errorMessage": "触发模型限流",
        "errorCode": "RateLimit",
        "result": "评阅结果\n\n",
        "score": 58,
        "dimensionResults": [
          {
            "name": "内容完整度",
            "analysis": "文章内容较为完整，涵盖了题目的核心要求，但部分论述略显简略。",
            "score": 25.5,
            "maxScore": 30
          }
        ],
        "overallComment": "整体表现良好，建议在论述深度上进一步加强。",
        "usage": {
          "inputTokens": 951,
          "outputTokens": 13,
          "totalTokens": 964
        }
      }
    ],
    "totalUsage": {
      "inputTokens": 951,
      "outputTokens": 13,
      "totalTokens": 964
    }
  }
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/GetEssayCorrectionTask#workbench-doc-change-demo)。
