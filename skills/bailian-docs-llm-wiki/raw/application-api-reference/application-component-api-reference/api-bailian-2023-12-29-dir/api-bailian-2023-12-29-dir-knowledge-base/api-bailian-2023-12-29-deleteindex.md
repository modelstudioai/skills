# DeleteIndex - 删除知识库

永久性删除指定的知识库。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:DeleteIndex 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。
-   如果知识库正在被应用调用，需要先解除关联后才可删除。此操作当前只能通过控制台完成。具体操作请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
-   删除操作不可逆，被删知识库将无法恢复，请谨慎操作。
-   调用本接口不会删除[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)中已导入的文件。
-   本接口具有幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndex)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndex)

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

sfm:DeleteIndex

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/index/delete HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

IndexId

string

是

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

f89ie0xxxx

WorkspaceId

string

是

知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vexxxx

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Code

string

错误状态码。

Index.InvalidParameter

Message

string

错误信息。

Required parameter(%s) missing or invalid, please check the request parameters.

RequestId

string

请求 ID。

17204B98-xxxx-4F9A-8464-2446A84821CA

Status

string

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值：

-   true：成功
-   false：失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Index.InvalidParameter",
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Status": 200,
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
