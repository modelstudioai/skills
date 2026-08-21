# GetTagMiningAnalysisTask - 获取标签挖掘分析任务结果

获取挖掘分析任务结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetTagMiningAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GetTagMiningAnalysisTask)

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

quanmiaolightapp:GetTagMiningAnalysisTask

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/quanmiao/lightapp/getTagMiningAnalysisTask HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

taskId

string

否

任务 ID

a3d1c2ac-f086-4a21-9069-f5631542f5a2

workspaceId

string

否

[workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

状态码

successful

httpStatusCode

string

HTTP 响应吗

200

data

object

业务响应结果

results

array<object>

分析结果列表

results

object

分析对象

payload

object

载荷对象

output

object

输出对象

text

string

模型响应文本

xxxx

usage

object

用量

inputToken

long

输入 token

100

outputToken

long

输出 token

200

totalToken

long

总 token 数

300

header

object

响应头信息

requestId

string

大模型请求 ID

085BE2D2-BB7E-59A6-B688-F2CB32124E7F

event

string

事件

task-finished

errorCode

string

错误码

DataNotExists

errorMessage

string

错误信息

数据不存在

customId

string

索引

1

status

string

任务状态 SUCCESSED=任务执行成功 ，FAILED=任务执行失败 ，CANCELED=任务被取消 ，PENDIN=任务排队中 ，SUSPENDE=任务挂起 RUNNIN=任务处理中

RUNNIN

errorCode

string

任务错误 Code

任务错误Code

errorMessage

string

任务错误消息

任务错误消息

message

string

接口错误信息

DataNotExists

requestId

string

requestId

085BE2D2-BB7E-59A6-B688-F2CB32124E7F

success

boolean

是否成功

true

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "successful",
  "httpStatusCode": 200,
  "data": {
    "results": [
      {
        "payload": {
          "output": {
            "text": "xxxx"
          },
          "usage": {
            "inputToken": 100,
            "outputToken": 200,
            "totalToken": 300
          }
        },
        "header": {
          "requestId": "085BE2D2-BB7E-59A6-B688-F2CB32124E7F",
          "event": "task-finished",
          "errorCode": "DataNotExists",
          "errorMessage": "数据不存在"
        },
        "customId": 1
      }
    ],
    "status": "RUNNIN",
    "errorCode": "任务错误Code\n\n",
    "errorMessage": "任务错误消息\n\n"
  },
  "message": "DataNotExists",
  "requestId": "085BE2D2-BB7E-59A6-B688-F2CB32124E7F",
  "success": true
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
