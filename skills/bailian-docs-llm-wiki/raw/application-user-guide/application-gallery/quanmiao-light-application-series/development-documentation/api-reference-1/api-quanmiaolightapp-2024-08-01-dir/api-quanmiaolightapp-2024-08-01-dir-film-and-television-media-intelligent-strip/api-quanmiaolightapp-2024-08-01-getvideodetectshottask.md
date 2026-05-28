# GetVideoDetectShotTask - 智能拆条-获取异步任务状态和结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetVideoDetectShotTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetVideoDetectShotTask)

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

quanmiaolightapp:GetVideoDetectShotTask

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/quanmiao/lightapp/getVideoDetectShotTask HTTP/1.1
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

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

taskId

string

是

任务唯一标识

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

状态码

successful

message

string

错误说明

successful

httpStatusCode

integer

http 状态码

200

success

boolean

是否成功：true 成功，false 失败

True

data

object

结果

header

object

event 名称

errorCode

string

异常错误码

success

errorMessage

string

异常错误信息

Deduct task already success,Please do not resubmit.token '369e8f2c-d283-424a-96c4-c83efe08c89e'

event

string

事件类型

TIMEOUT\_CLOSE\_ORDER

eventInfo

string

事件描述

xxx

sessionId

string

会话唯一标识

d5c38cf6-a4bf-4a57-a697-9f449926f0c9

taskId

string

生成唯一标识

6e223291-729b-4e84-9271-c13ada1a776b

traceId

string

全量路 ID

215045f817272303448235204efdef

payload

object

结果

output

object

结果

videoSplitResult

object

结果

text

string

拆条结果

xxx

reasonText

string

深度思考结果

xxx

videoParts

array<object>

拆条结果结构化，如果结构化失败则参数不存在，请根据 text 的返回结果进行解析；参数可通过 prompt 进行自定义调整，可参考 modelCustomPromptTemplateId（通过/getLightAppGeneralConfig 接口获取）进行改写

视频拆条结构化数组

object

string

xxx

xxx

videoRecognitionResult

array<object>

视频识别结果列表，根据入参的 recognitionOptions 选项进行视频内容识别后的结果

识别结果

object

startTime

long

当前识别结果的开始时间

1758108425000

endTime

long

当前识别结果的结束时间

1748483740000

asr

string

音频转文字的结果

xxx

ocr

string

画面中的文字内容识别结果

xxx

vl

string

画面内容识别结果

xxx

usage

object

token 数量

inputTokens

long

输入 Token 数量

36

outputTokens

long

输出 Token 数量

13

totalTokens

long

总 Token 数量

49

taskRunInfo

object

运行信息

concurrentChargeEnable

boolean

是否使用付给并发：true 时，按照实际运行时长计量

true

responseTime

long

运行时长：rt

1000

taskStatus

string

任务状态

SUCCESSED

taskId

string

任务 ID

3feb69ed02d9b1a17d0f1a942675d300

errorMessage

string

异常错误信息

Failed to proxy flink ui request, message: An error occurred: Invalid UUID string: jobsn.

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "code": "successful",
  "message": "successful",
  "httpStatusCode": 200,
  "success": true,
  "data": {
    "header": {
      "errorCode": "success",
      "errorMessage": "Deduct task already success,Please do not resubmit.token '369e8f2c-d283-424a-96c4-c83efe08c89e'",
      "event": "TIMEOUT_CLOSE_ORDER",
      "eventInfo": "xxx",
      "sessionId": "d5c38cf6-a4bf-4a57-a697-9f449926f0c9",
      "taskId": "6e223291-729b-4e84-9271-c13ada1a776b",
      "traceId": "215045f817272303448235204efdef"
    },
    "payload": {
      "output": {
        "videoSplitResult": {
          "text": "xxx",
          "reasonText": "xxx",
          "videoParts": [
            {
              "key": "xxx"
            }
          ],
          "videoRecognitionResult": [
            {
              "startTime": 1758108425000,
              "endTime": 1748483740000,
              "asr": "xxx",
              "ocr": "xxx",
              "vl": "xxx"
            }
          ]
        }
      },
      "usage": {
        "inputTokens": 36,
        "outputTokens": 13,
        "totalTokens": 49
      }
    },
    "taskRunInfo": {
      "concurrentChargeEnable": true,
      "responseTime": 1000
    },
    "taskStatus": "SUCCESSED",
    "taskId": "3feb69ed02d9b1a17d0f1a942675d300",
    "errorMessage": "Failed to proxy flink ui request, message: An error occurred: Invalid UUID string: jobsn."
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

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-10-20

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/GetVideoDetectShotTask?updateTime=2025-10-20#workbench-doc-change-demo)
