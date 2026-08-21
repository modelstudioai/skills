# SubmitFactAuditUrl - 提交事实性审核 URL

妙笔为您提供了新的事实性审核能力，在联网搜索并判断正误的前提下，还支持用户自定义配置搜索来源 URL。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitFactAuditUrl)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitFactAuditUrl)

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

aimiaobi:SubmitFactAuditUrl

create

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

Url

string

是

用户希望使用的审核信息来源 URL。通过该接口新增信源 URL 后，事实性审核的信息来源会只从配置好的 URL 列表中获取；如果不新增 URL，则默认从全网检索审核所需的信息。每位用户最多可以配置 10 条信源 URL。

https://aliyun.com

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

新增 URL 的成功提示。

SUCCESSED

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
  "Data": "SUCCESSED"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
