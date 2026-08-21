# UpdateVideoAnalysisTask - 视频理解-修改异步任务状态

视频理解-修改任务状态：目前仅支持取消任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/UpdateVideoAnalysisTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/UpdateVideoAnalysisTask)

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

quanmiaolightapp:UpdateVideoAnalysisTask

update

\*全部资源

`*`

无

无

## 请求语法

```
PUT /{workspaceId}/quanmiao/lightapp/videoAnalysis/updateVideoAnalysisTask HTTP/1.1
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

xxxx

taskStatus

string

是

任务状态：

-   CANCELED：取消任务

CANCELED

## 返回参数

名称

类型

描述

示例值

object

响应

requestId

string

请求唯一标识

117F5ABE-CF02-5502-9A3F-E56BC9081A64

code

string

状态码

DataNotExists

message

string

错误消息

任务不存在

success

boolean

是否成功：true 成功，false 失败

false

httpStatusCode

integer

http 状态码

200

data

object

任务信息

taskId

string

任务唯一标识

3feb69ed02d9b1a17d0f1a942675d300

taskStatus

string

任务状态

CANCELED

taskErrorMessage

string

任务失败信息

主动取消

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "code": "DataNotExists",
  "message": "任务不存在",
  "success": false,
  "httpStatusCode": 200,
  "data": {
    "taskId": "3feb69ed02d9b1a17d0f1a942675d300",
    "taskStatus": "CANCELED",
    "taskErrorMessage": "主动取消"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
