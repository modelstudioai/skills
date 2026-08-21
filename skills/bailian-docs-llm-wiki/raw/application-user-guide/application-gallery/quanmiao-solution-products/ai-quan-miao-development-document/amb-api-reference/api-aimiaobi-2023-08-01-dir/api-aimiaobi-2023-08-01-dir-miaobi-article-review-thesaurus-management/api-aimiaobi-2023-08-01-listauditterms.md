# ListAuditTerms - 获取自定义词库记录

获取词库列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAuditTerms)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAuditTerms)

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

aimiaobi:ListAuditTerms

list

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

NextToken

string

否

下一页的 Token

XXXX

MaxResults

integer

否

返回的最大记录数

10

TermsName

string

否

词典名称。可选。不填默认 Default

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

array<object>

业务数据

data

object

是否删除成功

Id

string

任务主键 ID

1

Keyword

string

关键词

龘

SuggestWord

string

建议词

龘(dá)

TermsDesc

string

审核依据

龙行龘龘出自四库本《玉篇》23龙部第8字，文字释义为群龙腾飞的样子，昂扬而热烈。

ExceptionWord

array

例外语句

exceptionWord

string

词典名称

TermsName

string

词典名称

MaxResults

integer

最大返回结果数

77

NextToken

string

下一页的 Token

x'x'x

TotalCount

integer

总数

58

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
  "Data": [
    {
      "Id": 1,
      "Keyword": "龘",
      "SuggestWord": "龘(dá)",
      "TermsDesc": "龙行龘龘出自四库本《玉篇》23龙部第8字，文字释义为群龙腾飞的样子，昂扬而热烈。",
      "ExceptionWord": [
        ""
      ],
      "TermsName": ""
    }
  ],
  "MaxResults": 77,
  "NextToken": "x'x'x",
  "TotalCount": 58
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-11-11

OpenAPI 入参发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListAuditTerms?updateTime=2025-11-11#workbench-doc-change-demo)
