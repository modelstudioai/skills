# FetchImageTask - 获取图片任务执行结果

获取图片任务执行结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/FetchImageTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/FetchImageTask)

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

aimiaobi:FetchImageTask

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

cd327c3d5d5e44159cc716e23bfa530e\_p\_beebot\_public

TaskIdList

array

是

任务 ID 列表

TaskIdList

string

是

TaskId，任务唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

9c5ac65f-fcac-416c-81d0-4ab81e1373fd

ArticleTaskId

string

是

文章 taskId

e1be065b-adc3-435e-bd01-1c18c5ed75d3

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

TaskInfoList

array<object>

智能配图生成的图片信息

TaskInfoList

object

Id

long

段落 ID

1

ImageList

array<object>

图片信息

ImageList

object

Code

string

如果图片没有生成返回的异常 code 标识

NoData

Message

string

如果图片没有生成返回的异常信息描述

错误

Url

string

图片地址

http://www.example.com/aaa.png

TaskId

string

任务 ID 任务唯一标识

net-7eb32699000d4193a3c59fc64ae1e55f

TaskStatus

string

当前任务状态 SUCCESSED=任务执行成功 ，FAILED=任务执行失败 ，CANCELED=任务被取消 ，PENDIN=任务排队中 ，SUSPENDE=任务挂起 RUNNIN=任务处理中

SUCCESSED

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
    "TaskInfoList": [
      {
        "Id": 1,
        "ImageList": [
          {
            "Code": "NoData",
            "Message": "错误",
            "Url": "http://www.example.com/aaa.png"
          }
        ],
        "TaskId": "net-7eb32699000d4193a3c59fc64ae1e55f",
        "TaskStatus": "SUCCESSED"
      }
    ]
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "DD656AF9-0839-521A-A3D2-F320009F9C87",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
