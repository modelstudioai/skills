# CreateTextFile - 上传合同审查文件

该接口用于将文档上传到合同审查模块中，添加成功之后，系统会自动启动文件的解析，并返回对应的文件ID用于后续生成审查规则和审查结果。文件解析有排队机制，如果队列较长，文件可能需要等待一段时间才能解析完成。

## 接口说明

-   该接口需要开通法睿商品相关的后付费服务（开通免费），可以使用该账号的 AccessKey 和 AccessSecret 来调用我们的 OpenApi 服务
-   接口的调用需要阿里云百炼平台的工作空间权限。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/FaRui/2024-06-28/CreateTextFile)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{WorkspaceId}/data/textFile HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

否

阿里云百炼平台工作空间 ID

llm-9w5y60lseff0jiqm

ClientToken

string

否

客户端 Token，用于保证请求的幂等性。从您的客户端生成一个参数值，确保不同请求间该参数值唯一。ClientToken 只支持 ASCII 字符。若您未指定，则系统自动使用 API 请求的 RequestId 作为 ClientToken 标识。每次 API 请求的 RequestId 可能不一样。

e9a93201-7e96-4dc1-9678-2832fc132d08

CreateTime

string

否

创建时间

1714476549

TextFileName

string

否

上传文件名(带后缀)

测试文件.docx

TextFileUrl

string

否

上传文件的下载 url。需要通过文件直接上传的请使用 SDK 的 CreateFileAdvanceRequest 请求

[https://xx](https://xx).测试文件.docx

ContractId

string

否

合同比对场景下使用，第一次上传文件会返回 ContractId，如果需要比对，则第二次上传传递该参数并上传标准文档

123

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Code

string

错误 Code 码

null

Data

object

调用成功时，返回的文件信息。

TextFileId

string

创建的文件 ID

36d6447d277c4a1c9fd0def1d16341f1

TextFileName

string

文件名

测试文件.docx

TextFileUrl

string

文件 URL

[https://xx](https://xx).测试文件.docx

ContractId

string

合同记录，比对模式关注该值

11123

HttpStatusCode

long

HTTP 状态码

200

Message

string

请求异常，返回具体异常错误信息。

null

RequestId

string

Id of the request

81E6F6D2-8ACB-5BDA-9C7C-4D6268CD9652

Success

boolean

是否调用成功。true：调用成功。false：调用失败。

True

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": null,
  "Data": {
    "TextFileId": "36d6447d277c4a1c9fd0def1d16341f1",
    "TextFileName": "测试文件.docx",
    "TextFileUrl": "https://xx.测试文件.docx",
    "ContractId": 11123
  },
  "HttpStatusCode": 200,
  "Message": null,
  "RequestId": "81E6F6D2-8ACB-5BDA-9C7C-4D6268CD9652",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/FaRui/2024-06-28/errorCode)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-11-13

OpenAPI 入参发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/FaRui/2024-06-28/CreateTextFile?updateTime=2025-11-13#workbench-doc-change-demo)
