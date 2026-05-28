# SubmitIndexJob - 提交知识库创建任务

提交指定的 CreateIndex 任务以完成知识库创建。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:SubmitIndexJob 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，您必须预先调用 **CreateIndex** 接口，并且获取到对应的`IndexId`。
-   调用本接口后，任务需一定时间执行，高峰期可能耗时数小时。任务完成前请勿重复发起请求。如果需要查询任务的执行状态，可调用 **GetIndexJobStatus** 接口查询。
-   知识库创建完成后，接下来您便可以在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中将创建好的知识库与您位于相同的业务空间里的智能体应用或者工作流应用 关联（或者通过[应用调用](https://help.aliyun.com/zh/model-studio/application-calling-guide)的`rag_options`传入`IndexID`），以便为您的阿里云百炼应用补充私有知识和提供最新信息。当然，您也可以选择不使用阿里云百炼应用，直接通过调用 **Retrieve** 接口来查询知识库。
-   本接口不具备幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexJob)

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

sfm:SubmitIndexJob

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/index/submit_index_job HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3shx2gu255oqxxxx

IndexId

string

是

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

79c0alxxxx

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

Data

object

接口返回的业务字段。

Id

string

任务 ID，即调用 **GetIndexJobStatus** 接口时需要用到的任务`JobId`。

eFDr2fGRzP9gdDZWAdo3xxxx

IndexId

string

知识库 ID。

79c0alxxxx

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

-   true：成功。
-   false：失败。

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Index.InvalidParameter",
  "Data": {
    "Id": "eFDr2fGRzP9gdDZWAdo3xxxx",
    "IndexId": "79c0alxxxx"
  },
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Status": 200,
  "Success": true
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

400

RagIndex.IdempotentParameterMismatch

The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical.

该请求使用与先前但不相同的请求相同的客户端令牌。不要重复使用具有不同请求的客户端令牌，除非请求相同。

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
