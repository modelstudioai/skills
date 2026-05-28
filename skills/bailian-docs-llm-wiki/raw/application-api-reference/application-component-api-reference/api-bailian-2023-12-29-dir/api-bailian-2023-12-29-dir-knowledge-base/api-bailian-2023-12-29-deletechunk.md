# DeleteChunk - 删除切片

删除知识库中的指定文本切片，被删的文本切片将无法被检索和召回。

## 接口说明

**警告** 文本切片被删除后无法恢复（硬删除），请谨慎操作。

-   **权限要求**：
    -   **RAM 用户（子账号）**：需先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（可使用`AliyunBailianDataFullAccess`策略，该策略已包含本接口所需的 sfm:DeleteChunk 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，才能调用本接口。
    -   **阿里云账号（主账号）**：默认拥有权限，可直接调用。
-   **调用方式**：推荐使用最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)调用，SDK 已封装复杂的签名计算逻辑，可简化您的调用过程。
-   **生效延迟**：更新后通常立即生效，高峰期可能稍有延迟（秒级）。
-   **幂等性**：本接口具有幂等性。对已成功删除的文本切片进行重复操作时，接口将返回成功响应。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/DeleteChunk)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/DeleteChunk)

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

sfm:DeleteChunk

delete

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/chunk/delete HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

PipelineId

string

是

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

79c0alxxxx

WorkspaceId

string

是

知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vexxxx

ChunkIds

array

是

需要删除的文本切片列表（单次最多传入 10 个文本切片 ID）。

string

是

文本切片 ID，即 **ListChunks** 接口返回的 Node 对象里`Metadata`中的`_id`字段。

llm-5ip55o1zrzxx\_09fe52x\_xxxxx\_033b551e10024029992e79767b151fxx\_10024xx\_0

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

请求 ID。

35A267BF-xxxx-54DB-8394-AA3B0742D833

Code

string

错误状态码。

Message

string

错误信息。

Success

boolean

接口调用是否成功，可能值：

-   true：成功。
-   false：失败。

true

Data

boolean

请求成功返回的业务数据。

true

Status

string

接口返回的状态码。

200

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "35A267BF-xxxx-54DB-8394-AA3B0742D833\n",
  "Code": "",
  "Message": "",
  "Success": true,
  "Data": true,
  "Status": 200
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
