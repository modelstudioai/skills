# GetMemory - 获取长期记忆体

获取指定长期记忆体的描述信息。

## 接口说明

-   本接口具有幂等性。

**限流说明：** 请确保两次请求间隔至少 1 秒，否则可能触发系统限流。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/GetMemory)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/GetMemory)

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

sfm:GetMemory

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/memories/{memoryId} HTTP/1.1
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

长期记忆体所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vexxxx

memoryId

string

是

长期记忆体 ID，对应 [CreateMemory](https://help.aliyun.com/zh/model-studio/developer-reference/api-bailian-2023-12-29-creatememory) 接口返回的`memoryId`。

6bff4f317a14442fbc9f73d29dbxxxx

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

description

string

长期记忆体的描述信息。

我的大模型应用$APP\_ID关于A用户的长期记忆体

memoryId

string

长期记忆体 ID。

6bff4f317a14442fbc9f73d29dbdxxxx

requestId

string

请求 ID。

6a71f2d9-f1c9-913b-818b-11402910xxxx

workspaceId

string

长期记忆体所属的业务空间 ID。

llm-3z7uw7fwz0vexxxx

## 示例

正常返回示例

`JSON`格式

```
{
  "description": "我的大模型应用$APP_ID关于A用户的长期记忆体",
  "memoryId": "6bff4f317a14442fbc9f73d29dbdxxxx",
  "requestId": "6a71f2d9-f1c9-913b-818b-11402910xxxx",
  "workspaceId": "llm-3z7uw7fwz0vexxxx"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

404

Memory.MemoryIdNotFound

Memory Id not exist or is not authorized.

memoryId 未找到

500

Memory.InternalError

Memory service inner exception.

长期记忆服务内部异常。

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
