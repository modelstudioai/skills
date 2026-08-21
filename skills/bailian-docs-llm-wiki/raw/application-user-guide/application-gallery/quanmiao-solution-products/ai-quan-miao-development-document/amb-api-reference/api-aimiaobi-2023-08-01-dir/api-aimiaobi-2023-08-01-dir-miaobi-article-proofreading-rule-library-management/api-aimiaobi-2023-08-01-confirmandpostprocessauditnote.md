# ConfirmAndPostProcessAuditNote - 确认提交规则库用于审核

是否将本次提交自定义规则库得到的解析结果用于审核任务。由于解析结果可能不满足用户需求，因此我们为您提供了该接口用于二次确认。如果对提交的规则库解析满意，则可以直接将本次提交任务的 TaskId 作为入参，系统会对您上传的规则库做后处理，使它可以被用于审核。反之，您可以重新调用 SubmitAuditNote 接口上传修改之后的规则库。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ConfirmAndPostProcessAuditNote)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ConfirmAndPostProcessAuditNote)

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

aimiaobi:ConfirmAndPostProcessAuditNote

none

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

TaskId

string

是

用户通过 SubmitAuditNote 接口得到的 TaskId。这是自定义规则库任务索引的唯一标识，在使用时务必妥善保存。

xxx\_Default\_1241541251241

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

Id of the request

F2F366D6-E9FE-1006-BB70-2C650896AAB5

Success

boolean

此次请求是否成功

true

Code

string

状态码

DataNotExists

Message

string

错误说明

success

HttpStatusCode

integer

http 状态码

200

Data

string

确认使用该解析结果后得到的任务 ID。实际上与入参一致，在这里返回是为了方便您取值。

33

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "F2F366D6-E9FE-1006-BB70-2C650896AAB5",
  "Success": true,
  "Code": "DataNotExists",
  "Message": "success",
  "HttpStatusCode": 200,
  "Data": 33
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
