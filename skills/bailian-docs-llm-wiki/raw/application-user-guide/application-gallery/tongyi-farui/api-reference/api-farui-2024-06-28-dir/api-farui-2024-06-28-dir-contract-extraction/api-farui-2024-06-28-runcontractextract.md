# RunContractExtract

该接口用于根据合同内容抽取相应的字段。用户输入合同链接和抽取字段信息后会进行对应字段抽取

## 接口说明

请确保在使用该接口前，已充分了解法睿产品的收费方式和价格。

-   该接口需要开通法睿商品相关的后付费服务（开通免费），可以使用该账号的 AccessKey 和 AccessSecret 来调用我们的 OpenApi 服务
-   接口的调用需要阿里云百炼平台的工作空间权限。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/pop/contract/extraction HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

workspaceId

string

否

阿里云百炼平台工作空间 ID

llm-sds12344

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

appId

string

否

应用 ID

farui

regionId

string

否

地域 ID。

cn-hangzhou

fileOssUrl

string

是

公网可访问的文件 oss 链接

ttps://xxxxx.oss-cn-hangzhou.aliyuncs.com/legalmind/userdownload/4a83e0fe-baee-41d5-89f6-e33c8d462839/contract/report/9ce843d2-a05e-4351-9d69-15ae96bd910a\_1713348901026.pdf

fieldsToExtract

array<object>

否

需要抽取的字段

object

否

字段

extractItem

string

否

抽取字段的名称

乙方主体名称

option

array

否

抽取字段的固定枚举值

string

否

字段枚举

"固定金额"

desc

string

否

抽取字段描述

当金额类型为收入或支出时可选其一

## 返回参数

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

requestId

string

Id of the request

C844BE6B-33A9-5AC4-A1AE-97B131849E0F

data

object

返回信息

contractText

string

合同内容

甲方与乙方签署的技术服务合作协议...

extractResult

array<object>

抽取结果

array<object>

抽取结果实体类

extractItem

string

抽取字段的名称

合同编号

option

string

抽取字段的固定枚举值

null

desc

string

抽取字段描述

合同唯一标识编号，格式如 HT-YYYY-XXXXX

value

array<object>

抽取字段的值

object

抽取字段

data

string

抽取字段的值

HT-2022-0001

originalText

string

抽取字段的原文内容

合同编号：HT-2022-0001

httpStatusCode

integer

HTTP 状态码

200

code

string

响应状态码。

200

success

boolean

调用是否成功

True

message

string

错误信息

错误

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "C844BE6B-33A9-5AC4-A1AE-97B131849E0F",
  "data": {
    "contractText": "甲方与乙方签署的技术服务合作协议...",
    "extractResult": [
      {
        "extractItem": "合同编号",
        "option": "null",
        "desc": "合同唯一标识编号，格式如 HT-YYYY-XXXXX",
        "value": [
          {
            "data": "HT-2022-0001",
            "originalText": "合同编号：HT-2022-0001"
          }
        ]
      }
    ]
  },
  "httpStatusCode": 200,
  "code": "200",
  "success": true,
  "message": "错误"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/FaRui/2024-06-28/errorCode)查看更多错误码。

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/FaRui/2024-06-28/RunContractExtract#workbench-doc-change-demo)。
