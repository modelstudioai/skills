# GetVideoAnalysisTask - 视频理解-获取异步任务状态和结果

轻应用-获取视频理解异步任务结果。

## 接口说明

阿里云百炼轻应用-视频理解-获取异步任务状态和结果：通过这个接口可以查看“提交异步任务”接口提交的视频理解任务状态和结果。欢迎前往[视频理解控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/video-comprehend)体验。

**说明**

当返回结果中包含`header -> errorCode = ViolationOfSecurityPolicy`时，表明该请求触发了系统的安全策略限制，请对请求内容进行相应的修改。此时，`videoAnalysisResult`等业务数据返回为空。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetVideoAnalysisTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetVideoAnalysisTask)

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

quanmiaolightapp:GetVideoAnalysisTask

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/quanmiao/lightapp/videoAnalysis/getVideoAnalysisTask HTTP/1.1
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

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

taskId

string

是

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

5D0E915E-655D-59A8-894F-93873F73AAE5

code

string

状态码

successful

message

string

错误说明

success

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

videoAnalysisResult

object

语言分析对应生成内容

generateFinished

boolean

当前任务是否已生成结束

true

text

string

vl 生成文本结果

xxx

usage

object

Token 数量

inputTokens

integer

输入 Token 数量

0

outputTokens

integer

输出 Token 数量

0

totalTokens

integer

总 Token 数量

0

imageTokens

integer

图片 token

1

videoShotAnalysisResults

array<object>

视频每个分镜对应语言分析结果：：因内容较大，请从 resultJsonFileUrl 文件中获取

object

视频分镜结果

endTime

integer

结束时间，相对时间，单位毫秒

10000

startTime

integer

开始时间，相对时间，单位毫秒

1000

text

string

生成原始内容

xxxx

videoCaptionResult

object

视频字幕

generateFinished

boolean

当前任务是否已生成结束

true

videoCaptions

array<object>

视频字幕

object

视频字幕

endTime

integer

结束时间，相对时间，单位毫秒

20000

endTimeFormat

string

结束时间，格式化结果

00:01

startTime

integer

开始时间，相对时间，单位毫秒

1000

startTimeFormat

string

开始时间，格式化结果

00:01

text

string

字幕内容

xxxx

speaker

string

角色

张三

videoGenerateResult

object

文本总结结果：多任务时，请从 videoGenerateResults 字段获取结果

generateFinished

boolean

当前任务是否已生成结束

true

text

string

生成文本

xxx

usage

object

输出 Token 数量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 Token 数量

1

totalTokens

integer

总 Token 数量

2

modelId

string

模型 id

qwen-max-latest

modelReduce

boolean

模型是否被降级：如果模型是 qwen-max 或 qwen-max-latest，且超过 prompt 输入上限时，会尝试降级到 qwen-plus-latest 模型，保证信息完整性

qwen-plus-latest

reasonText

string

模型思考过程

xx

index

integer

多任务标号：1 开始

1

videoMindMappingGenerateResult

object

脑图生成结束

generateFinished

boolean

当前任务是否已生成结束

true

text

string

生成文本

小吃街

usage

object

输入 Token 数量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 Token 数量

1

totalTokens

integer

总 Token 数量

2

videoMindMappings

array<object>

脑图结果

array<object>

子节点

childNodes

array<object>

子节点

array<object>

子节点

childNodes

array<object>

子节点

object

节点描述

name

string

节点描述

三级节点

name

string

节点描述

二级节点

name

string

节点描述

三级节点

videoTitleGenerateResult

object

标题生成结果

generateFinished

boolean

当前任务是否已生成结束

true

text

string

文本生成结果

xxxx

usage

object

Token 数量

inputTokens

integer

输入 Token 数量

0

outputTokens

integer

输出 Token 数量

0

totalTokens

integer

总 Token 数量

0

resultJsonFileUrl

string

结果 json 文件地址：

由于响应结果过大，部分数据获取改为文件方式，可以通过当前字段 url 下载文件，并解析使用：

-   当前包含的字段：数据结构定义见 RunVideoAnalysis 接口
    -   videoShotSnapshotResult：每个分片抽帧信息，包括每帧 url
        
    -   videoShotAnalysisResults：每个分片语言分析结果明细
        
-   其他字段获取方式不变，文本方式返回。
    
-   文件类型：json
    
-   文件内容：全量报文，包含文本方式返回的 返回 event：task-finished
    

http://xxx

videoGenerateResults

array<object>

当入参为多任务时（textProcessTasks 有值），返回文本加工结果对应这个字段，可以通过数据所在数组位置（下标）或 index（1 开始）找到对应结果。

array<object>

文本加工任务结果

generateFinished

boolean

当前任务是否已生成结束

true

modelId

string

模型 id

xx

index

integer

多任务标号：1 开始

1

text

string

生成内容

xx

reasonText

string

模型思考过程

xx

usage

object

用量

inputTokens

integer

输入 Token 数量

1

outputTokens

integer

输出 token 数

1

totalTokens

integer

总 token

2

videoRoleRecognitionResult

object

自动识别结果

videoRoles

array<object>

角色列表

array<object>

roleName

string

角色名称

xx

roleInfo

string

人物信息

xx

timeIntervals

array<object>

角色出场时间段列表

object

startTime

integer

开始时间

0

endTime

integer

结束时间

342463553646

timestamp

integer

当前时间段角色出场时间

42553453253

url

string

角色图片

http://

ratio

number

出场率

0.2

isAutoRecognition

boolean

自动识别是否使用的是自动识别单独的视频地址（是：则人脸图片无法使用时间与视频帧用时间对应，因为可能是不同的视频）

videoCalculatorResult

object

费用估算结果

items

array<object>

计费项明细

object

计费项明细

name

string

计费项名称

xxx

type

string

类型

token

inputToken

integer

输入 token

1

outputToken

integer

输出 token

1

time

integer

计费时长

1

inputExpense

number

输入 token 计费

1

outputExpense

number

输入 token 计费

1

timeExpense

number

输出 token 计费

1

totalExpense

number

费用

0.098

addDatasetDocumentsResult

object

自动保存执行结果

status

integer

自动保存任务状态：1 成功，0 失败

1

title

string

视频名称

xx

docId

string

视频 docId

xxx

errorMessage

string

如果自动保存失败，则输出错误信息

xx

docUuid

string

视频的 docUuid

xxx

usage

object

token 描述

inputTokens

integer

输入 Token 数量

0

outputTokens

integer

输出 Token 数量

0

totalTokens

integer

总 Token 数量

0

taskRunInfo

object

运行信息

concurrentChargeEnable

boolean

是否使用付费并发：true 时，按照实际运行时长计量

true

responseTime

integer

运行时长：从任务被调度开始到任务完成的耗时，单位毫秒

1000

taskStatus

string

任务状态。

-   PENDING：待执行
    
-   RUNNING：执行中
    
-   SUCCESSED：成功
    
-   SUSPENDED：暂停
    
-   FAILED：失败
    
-   CANCELED： 取消
    

SUCCESSED

taskId

string

任务 ID

3feb69ed02d9b1a17d0f1a942675d300

errorMessage

string

异常错误信息

Access was denied, message: No such namespace namespaces/mjp-test-default.

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "5D0E915E-655D-59A8-894F-93873F73AAE5",
  "code": "successful",
  "message": "success",
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
        "videoAnalysisResult": {
          "generateFinished": true,
          "text": "xxx",
          "usage": {
            "inputTokens": 0,
            "outputTokens": 0,
            "totalTokens": 0,
            "imageTokens": 1
          },
          "videoShotAnalysisResults": [
            {
              "endTime": 10000,
              "startTime": 1000,
              "text": "xxxx"
            }
          ]
        },
        "videoCaptionResult": {
          "generateFinished": true,
          "videoCaptions": [
            {
              "endTime": 20000,
              "endTimeFormat": "00:01",
              "startTime": 1000,
              "startTimeFormat": "00:01",
              "text": "xxxx",
              "speaker": "张三"
            }
          ]
        },
        "videoGenerateResult": {
          "generateFinished": true,
          "text": "xxx",
          "usage": {
            "inputTokens": 1,
            "outputTokens": 1,
            "totalTokens": 2
          },
          "modelId": "qwen-max-latest",
          "modelReduce": true,
          "reasonText": "xx",
          "index": 1
        },
        "videoMindMappingGenerateResult": {
          "generateFinished": true,
          "text": "小吃街",
          "usage": {
            "inputTokens": 1,
            "outputTokens": 1,
            "totalTokens": 2
          },
          "videoMindMappings": [
            {
              "childNodes": [
                {
                  "childNodes": [
                    {
                      "name": "三级节点"
                    }
                  ],
                  "name": "二级节点"
                }
              ],
              "name": "三级节点"
            }
          ]
        },
        "videoTitleGenerateResult": {
          "generateFinished": true,
          "text": "xxxx",
          "usage": {
            "inputTokens": 0,
            "outputTokens": 0,
            "totalTokens": 0
          }
        },
        "resultJsonFileUrl": "http://xxx",
        "videoGenerateResults": [
          {
            "generateFinished": true,
            "modelId": "xx",
            "index": 1,
            "text": "xx",
            "reasonText": "xx",
            "usage": {
              "inputTokens": 1,
              "outputTokens": 1,
              "totalTokens": 2
            }
          }
        ],
        "videoRoleRecognitionResult": {
          "videoRoles": [
            {
              "roleName": "xx",
              "roleInfo": "xx",
              "timeIntervals": [
                {
                  "startTime": 0,
                  "endTime": 342463553646,
                  "timestamp": 42553453253,
                  "url": "http://"
                }
              ],
              "ratio": 0.2,
              "isAutoRecognition": true
            }
          ]
        },
        "videoCalculatorResult": {
          "items": [
            {
              "name": "xxx",
              "type": "token",
              "inputToken": 1,
              "outputToken": 1,
              "time": 1,
              "inputExpense": 1,
              "outputExpense": 1,
              "timeExpense": 1,
              "totalExpense": 0.098
            }
          ]
        },
        "addDatasetDocumentsResult": {
          "status": 1,
          "title": "xx",
          "docId": "xxx",
          "errorMessage": "xx",
          "docUuid": "xxx"
        }
      },
      "usage": {
        "inputTokens": 0,
        "outputTokens": 0,
        "totalTokens": 0
      }
    },
    "taskRunInfo": {
      "concurrentChargeEnable": true,
      "responseTime": 1000
    },
    "taskStatus": "SUCCESSED",
    "taskId": "3feb69ed02d9b1a17d0f1a942675d300",
    "errorMessage": "Access was denied, message: No such namespace namespaces/mjp-test-default."
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

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/GetVideoAnalysisTask#workbench-doc-change-demo)。
