# UpdateVideoAnalysisTasks - 视频理解-批量取消任务

视频理解-批量取消任务

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/UpdateVideoAnalysisTasks)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/UpdateVideoAnalysisTasks)

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

quanmiaolightapp:UpdateVideoAnalysisTasks

update

\*全部资源

`*`

无

无

## 请求语法

```
PUT /{workspaceId}/quanmiao/lightapp/videoAnalysis/updateVideoAnalysisTasks HTTP/1.1
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

taskIds

array

是

任务 id 列表

string

是

任务 id

xxx

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

Schema of Response

requestId

string

Id of the request

04DA1A52-4E51-56CB-BA64-FDDA0B53BAE8

code

string

响应 Code 码

successful

message

string

错误消息

success

success

boolean

是否成功：true 成功，false 失败

true

httpStatusCode

integer

http 响应码

200

data

array<object>

删除结果

data

object

删除结果

taskId

string

任务 id

xx

taskStatus

string

任务状态

CANCELED

taskErrorMessage

string

任务失败信息

xx

taskErrorCode

string

任务失败 code

xx

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "04DA1A52-4E51-56CB-BA64-FDDA0B53BAE8",
  "code": "successful",
  "message": "success",
  "success": true,
  "httpStatusCode": 200,
  "data": [
    {
      "taskId": "xx",
      "taskStatus": "CANCELED",
      "taskErrorMessage": "xx",
      "taskErrorCode": "xx"
    }
  ]
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
