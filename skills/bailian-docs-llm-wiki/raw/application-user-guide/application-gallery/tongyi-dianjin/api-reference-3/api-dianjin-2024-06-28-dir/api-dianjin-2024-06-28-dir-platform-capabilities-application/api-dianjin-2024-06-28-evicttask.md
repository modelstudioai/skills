# EvictTask - 取消任务

中断任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/EvictTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/EvictTask)

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

dianjin:EvictTask

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/task/evict HTTP/1.1
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

taskId

string

是

任务 Id

17071319

## 返回参数

名称

类型

描述

示例值

object

ResultCode

cost

long

耗时

null

data

string

响应数据，返回任务 id。

17071319

dataType

string

数据类型

null

errCode

string

错误码

0

message

string

错误信息

返回任务取消的结果，成功/失败。

requestId

string

请求 id

44BD277A-87F9-5310-8D63-3E6645F1DA85

success

boolean

是否成功

true

time

string

时间戳

2024-04-24 11:54:34

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 0,
  "data": 17071319,
  "dataType": null,
  "errCode": 0,
  "message": "返回任务取消的结果，成功/失败。",
  "requestId": "44BD277A-87F9-5310-8D63-3E6645F1DA85",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
