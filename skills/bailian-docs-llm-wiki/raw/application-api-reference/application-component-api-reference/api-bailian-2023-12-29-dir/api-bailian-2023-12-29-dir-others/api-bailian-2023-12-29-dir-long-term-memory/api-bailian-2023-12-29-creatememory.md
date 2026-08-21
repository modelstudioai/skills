# CreateMemory - 创建长期记忆体

创建一个长期记忆体。

## 接口说明

-   您可以将对话过程中的特定信息（即记忆片段，详见[长期记忆](https://help.aliyun.com/zh/model-studio/user-guide/long-term-memory)）存储到长期记忆体（Memory）中，智能体应用将在后续对话中持续引用这些信息（非自动，您需要先调用 [CreateMemory](https://help.aliyun.com/zh/model-studio/developer-reference/api-bailian-2023-12-29-creatememory) 接口创建长期记忆体，获取`memoryId`。然后[通过 API 调用智能体应用](https://help.aliyun.com/zh/model-studio/user-guide/application-calling)时，传入该`memoryId`）。
    
    **说明** 长期记忆体尚不支持存储与管理用户画像，请您通过控制台进行相关操作，详见[长期记忆](https://help.aliyun.com/zh/model-studio/user-guide/long-term-memory#578ebae524m6l)。
    
-   若传入`memoryId`，系统会根据对话记录，在指定长期记忆体下自动创建记忆片段（MemoryNode）。您也可以调用 [CreateMemoryNode](https://help.aliyun.com/zh/model-studio/developer-reference/api-bailian-2023-12-29-creatememorynode) 接口手动创建记忆片段。
-   本接口不具备幂等性。

**限流说明：** 请确保两次请求间隔至少 1 秒，否则可能触发系统限流。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/CreateMemory)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/CreateMemory)

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

sfm:CreateMemory

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/memories HTTP/1.1
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

description

string

否

长期记忆体的描述信息。长度为 1~50 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等）。可以包含半角冒号（:）、下划线（\_）、半角句号（.）或者短划线（-）。

我的大模型应用$APP\_ID关于A用户的长期记忆体

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

memoryId

string

长期记忆体 ID。

**说明** 请妥善保管该值，它将用于后续所有与此长期记忆体相关的 API 操作。

6bff4f317a14442fbc9f73d29dbxxxx

requestId

string

请求 ID。

17204B98-xxxx-4F9A--2446A84821CA

## 示例

正常返回示例

`JSON`格式

```
{
  "memoryId": "6bff4f317a14442fbc9f73d29dbxxxx",
  "requestId": "17204B98-xxxx-4F9A--2446A84821CA"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

400

Memory.DescriptionInvalid

Input parameter description is invalid.

长期记忆的描述信息无效

404

Memory.MemoryIdNotFound

Memory Id not exist or is not authorized.

memoryId 未找到

500

Memory.InternalError

Memory service inner exception.

长期记忆服务内部异常。

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
