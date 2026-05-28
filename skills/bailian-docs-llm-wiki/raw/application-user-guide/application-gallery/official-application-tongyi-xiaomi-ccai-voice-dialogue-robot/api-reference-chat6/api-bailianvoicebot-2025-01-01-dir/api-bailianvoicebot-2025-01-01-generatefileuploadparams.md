# GenerateFileUploadParams - 获取文件上传参数

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/GenerateFileUploadParams)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/GenerateFileUploadParams)

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

bailianvoicebot:GenerateFileUploadParams

update

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

BusinessUnitId

string

是

百炼业务空间 ID

llm-c11iig67g863rih8

FileName

string

是

文件名

test.wav

BusinessType

string

是

文件类型

枚举值：

-   Vocabulary：Vocabulary。
-   CloneVoice：CloneVoice。

CloneVoice

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Code

string

内部错误码

OK

HttpStatusCode

integer

http 状态码

200

Message

string

错误信息

Instance llm-xdne77rxe14ziszr does not exist.

RequestId

string

请求 ID

D771A1B6-3D5F-174A-BEE1-98CE1000D337

Data

object

文件上传参数

Signature

string

根据 AccessKey Secret 和 Policy 计算出的签名信息。调用 OSS API 时，OSS 验证该签名信息，从而确认 Post 请求的合法性。

6oETypl+gbYHwbgcwnQiyDYoQbA=

Policy

string

OSS 通过该参数验证请求表单域的合法性

eyJleHBpcmF0aW9uIjoiMjAyNi0wMy0yOVQxMzoyNDoyNi4yMDNaIiwiY29uZGl0aW9ucyI6W239

AccessKeyId

string

签名使用的 AccessKeyId。

STS.NYGg9ejEjYqySx3EsuRutagbd

Host

string

OSS 的接入域名。

http://cab.oss-cn-hangzhou.aliyuncs.com

FileKey

string

上传文件路径

vocabulary/B678CA67-C8CB-150C-AD7F-6FA7F0A811BA\_热词导入模版 (7).zip

ExpirationTime

long

上传有效期

1774794266093

SecurityToken

string

安全 token

CAISzwJ1q6Ft5B2yfSjIr5ryLIjRh5pL7rOSUV6CoXMgXvpYjqLJhjz2IHhMfnlvB+gYsfU2m2xR5/Yclrp6SJtIXleCZtF94oxN9h2gb4fb42Jqag+/08/LI3OaLjKm9u2wCryLYbGwU/OpbE++5U0X6LDmdDKkckW4OJmS8/BOZcgWWQ/KBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO/ks0GG3ASmlrFF+9mufMb5M/MBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs+02c5onHUwYPu0vZYrOLroQ+fFFjHKMzDdtPq/7ylPI9ofDamIXxxAarin3kufQeLmrJ4LwneIvBXr5RHd5wa2rbWAEsmLNBEhL2EJMKtT476hcbIAuUI3bC5F+kxOHp9i6ErImtRWbLssUUla4R5TGOWbLJWzkTH93xuRqAAapuIRuRt0d2Odr1hsaYukMd42UkNapdTrehzmXeR6lyv1jlLmkAHve9Cbl9N5bO3A96FSlEfjHksQBWG0CEXRm3jLW41bpR00dgnM6gpOj7lRW2z33L0dTtaRw79X3+Uqz3gv9md5QvoaVi1jnr/cFRNxbjl7DI39pdcGlTI2lqIAA=

AccessKeySecret

string

Oss 授权上传文件的 Secret。

DGhwedF4SsbsqUMfzNBCjZFLJZSAdhiSE4hFPbKMm6JE

Bucket

string

OSS 文件保存桶名称。

cab

Region

string

地域

cn-hangzhou

Params

array

动态错误参数列表

param

string

动态错误参数

llm-xdne77rxe14ziszr

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "Instance llm-xdne77rxe14ziszr\n does not exist.",
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "Data": {
    "Signature": "6oETypl+gbYHwbgcwnQiyDYoQbA=",
    "Policy": "eyJleHBpcmF0aW9uIjoiMjAyNi0wMy0yOVQxMzoyNDoyNi4yMDNaIiwiY29uZGl0aW9ucyI6W239",
    "AccessKeyId": "STS.NYGg9ejEjYqySx3EsuRutagbd",
    "Host": "http://cab.oss-cn-hangzhou.aliyuncs.com",
    "FileKey": "vocabulary/B678CA67-C8CB-150C-AD7F-6FA7F0A811BA_热词导入模版 (7).zip",
    "ExpirationTime": 1774794266093,
    "SecurityToken": "CAISzwJ1q6Ft5B2yfSjIr5ryLIjRh5pL7rOSUV6CoXMgXvpYjqLJhjz2IHhMfnlvB+gYsfU2m2xR5/Yclrp6SJtIXleCZtF94oxN9h2gb4fb42Jqag+/08/LI3OaLjKm9u2wCryLYbGwU/OpbE++5U0X6LDmdDKkckW4OJmS8/BOZcgWWQ/KBlgvRq0hRG1YpdQdKGHaONu0LxfumRCwNkdzvRdmgm4NgsbWgO/ks0GG3ASmlrFF+9mufMb5M/MBZskvD42Hu8VtbbfE3SJq7BxHybx7lqQs+02c5onHUwYPu0vZYrOLroQ+fFFjHKMzDdtPq/7ylPI9ofDamIXxxAarin3kufQeLmrJ4LwneIvBXr5RHd5wa2rbWAEsmLNBEhL2EJMKtT476hcbIAuUI3bC5F+kxOHp9i6ErImtRWbLssUUla4R5TGOWbLJWzkTH93xuRqAAapuIRuRt0d2Odr1hsaYukMd42UkNapdTrehzmXeR6lyv1jlLmkAHve9Cbl9N5bO3A96FSlEfjHksQBWG0CEXRm3jLW41bpR00dgnM6gpOj7lRW2z33L0dTtaRw79X3+Uqz3gv9md5QvoaVi1jnr/cFRNxbjl7DI39pdcGlTI2lqIAA=",
    "AccessKeySecret": "DGhwedF4SsbsqUMfzNBCjZFLJZSAdhiSE4hFPbKMm6JE",
    "Bucket": "cab",
    "Region": "cn-hangzhou"
  },
  "Params": [
    "llm-xdne77rxe14ziszr"
  ]
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-04-20

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GenerateFileUploadParams?updateTime=2026-04-20#workbench-doc-change-demo)
