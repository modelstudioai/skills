# DeleteMemoryNode - 删除记忆片段

删除记忆片段。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/DeleteMemoryNode)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/DeleteMemoryNode)

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

sfm:DeleteMemoryNode

delete

\*全部资源

`*`

无

无

## 请求语法

```
DELETE /{workspaceId}/memories/{memoryId}/memoryNodes/{memoryNodeId} HTTP/1.1
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

llm-us9hjmt32nysdm5v

memoryId

string

是

长期记忆体 Id

6bff4f317a14442fbc9f73d29dbd5fc3

memoryNodeId

string

是

记忆片段 Id

68de06c95368463a8be4a84efc872cc5

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

请求 Id

8C56C7AF-6573-19CE-B018-E05E1EDCF4C5

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "8C56C7AF-6573-19CE-B018-E05E1EDCF4C5"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

400

Memory.MemoryNodeContentInvalid

Memory node content is invalid.

长期记忆节点的内容无效

404

Memory.MemoryIdNotFound

Memory Id not exist or is not authorized.

memoryId 未找到

404

Memory.MemoryNodeNotFound

MemoryNode not found.

长期记忆节点未找到

500

Memory.InternalError

Memory service inner exception.

长期记忆服务内部异常。

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
