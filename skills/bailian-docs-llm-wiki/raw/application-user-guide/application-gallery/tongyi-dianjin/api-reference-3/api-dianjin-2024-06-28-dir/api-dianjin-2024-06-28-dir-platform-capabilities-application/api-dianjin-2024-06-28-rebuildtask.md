# RebuildTask - 重建任务

对已有任务进行重建，但在队列中或执行中的任务不可重建。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/RebuildTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/RebuildTask)

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

dianjin:RebuildTask

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/task/rebuild HTTP/1.1
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

业务空间 Id

llm-xxxxx

body

object

否

请求体参数

taskIds

array

是

任务 ID 列表

taskId

string

否

任务 ID

3894763764

## 返回参数

名称

类型

描述

示例值

object

ResultCode<List<Map<String, Object>>>

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

array<object>

响应数据

data

object

重建任务操作的响应结果。其中 taskId 表示任务 id，status 表示操作的状态（success 为成功，error 为失败），message 为详细信息。

```
{
    "message": "任务正在执行中，不能重新构建",
    "taskId": "-253103935",
    "status": "error"
}
```

{ "message": "任务正在执行中，不能重新构建", "taskId": "-253103935", "status": "error" }

requestId

string

请求 id

EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258

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
  "data": [
    {
      "message": "任务正在执行中，不能重新构建",
      "taskId": -253103935,
      "status": "error"
    }
  ],
  "requestId": "EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258",
  "cost": 0
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
