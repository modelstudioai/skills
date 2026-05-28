# DashscopeAsyncTaskFinishEvent - Dashscope异步任务完成回调事件

Dashscope异步任务完成回调事件

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/DashscopeAsyncTaskFinishEvent)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/DashscopeAsyncTaskFinishEvent)

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

dianjin:DashscopeAsyncTaskFinishEvent

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/event/dashscopeAsyncTaskFinish HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

X-Load-Test

boolean

否

用户标识是否压测流量

workspaceId

string

是

业务空间 ID

llm-xxx

body

object

否

请求体参数

any

否

请求体参数

{}

## 返回参数

名称

类型

描述

示例值

object

WanProdResponse

code

string

返回码

0

message

string

返回信息

成功

success

boolean

返回是否成功

retryAble

boolean

是否可重试

## 示例

正常返回示例

`JSON`格式

```
{
  "code": 0,
  "message": "成功",
  "success": true,
  "retryAble": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-12-30

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/DianJin/2024-06-28/DashscopeAsyncTaskFinishEvent?updateTime=2025-12-30#workbench-doc-change-demo)
