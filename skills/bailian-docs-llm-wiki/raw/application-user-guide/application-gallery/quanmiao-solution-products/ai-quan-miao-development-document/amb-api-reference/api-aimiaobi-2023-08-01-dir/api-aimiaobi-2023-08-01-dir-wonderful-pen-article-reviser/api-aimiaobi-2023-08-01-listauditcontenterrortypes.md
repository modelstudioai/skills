# ListAuditContentErrorTypes - 获取审校维度列表

获取审核维度列表

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAuditContentErrorTypes)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListAuditContentErrorTypes)

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

aimiaobi:ListAuditContentErrorTypes

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

否

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

MaxResults

integer

否

最大记录数

100

NextToken

string

否

下一页 Token

cEoBWREAXdxaOyjq/cqAbg==

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

xxxxx

Code

string

错误码

DataNotExists

Message

string

错误消息

success

HttpStatusCode

integer

HTTP 状态码

200

Success

boolean

此次请求是否成功

true

Data

array<object>

审核维度列表

data

object

主审核维度

MajorClassCode

string

主审核维度 Code

ContentAccuracy

SubClasses

array<object>

子审核维度列表

subClasses

object

子审核维度

ClassCode

string

子审核维度 Code

PunctuationError

ClassName

string

子审核维度名称

标点符号错误

MajorClassName

string

子审核维度名称

内容准确性

NextToken

string

下一页 Token

下一页的token

TotalCount

integer

总记录条数

20

MaxResults

integer

当前返回的最大记录数

20

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "xxxxx",
  "Code": "DataNotExists",
  "Message": "success",
  "HttpStatusCode": 200,
  "Success": true,
  "Data": [
    {
      "MajorClassCode": "ContentAccuracy",
      "SubClasses": [
        {
          "ClassCode": "PunctuationError",
          "ClassName": "标点符号错误"
        }
      ],
      "MajorClassName": "内容准确性"
    }
  ],
  "NextToken": "下一页的token",
  "TotalCount": 20,
  "MaxResults": 20
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
