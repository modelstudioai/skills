# ListBuildConfigs - 获取系统自定义预设

获取系统自定义预设，用于创作文章 -> 直接生成中的内置选项。例如：写作文体、文章篇幅、输出语言、生成文章篇数等选项。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListBuildConfigs)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListBuildConfigs)

## 授权信息

当前API暂无授权信息透出。

## 请求参数

名称

类型

必填

描述

示例值

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

cd327c3d5d5e44159cc716e23bfa530e\_p\_beebot\_public

Type

string

否

政务和传媒类别,media:传媒,government:政务

枚举值：

-   market：营销文稿。
-   government：政务文稿。
-   media：传媒文稿。
-   office：办公文稿。

media

## 返回参数

名称

类型

描述

示例值

object

PlainResult<List\>

Code

string

状态码

200

Data

array<object>

业务数据

Data

object

业务对象

BuildIn

boolean

是否为内置

true

CreateTime

string

创建时间

2023-04-11 06:14:07

CreateUser

string

创建用户

1

Id

long

主键 ID

主键ID，内置配置（buildIn=true）无该字段

Keywords

array<object>

标签可选的值列表

Keyword

object

标签可选的值定义

Description

string

预设标签的描述

新闻内容

Key

string

预设标签的 KEY

新闻内容

Tag

string

标签 key 值

writingStyle

TagDescription

string

标签描述

文体

Type

string

区分政务和传媒,media:传媒,government:政务

media

UpdateTime

string

更新时间

2023-04-11 06:14:07

UpdateUser

string

更新用户

1

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

Success

RequestId

string

请求唯一标识

DA021073-17CE-5CCF-9FEB-93226C766887

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": 200,
  "Data": [
    {
      "BuildIn": true,
      "CreateTime": "2023-04-11 06:14:07",
      "CreateUser": 1,
      "Id": 0,
      "Keywords": [
        {
          "Description": "新闻内容",
          "Key": "新闻内容"
        }
      ],
      "Tag": "writingStyle",
      "TagDescription": "文体",
      "Type": "media",
      "UpdateTime": "2023-04-11 06:14:07\n",
      "UpdateUser": 1
    }
  ],
  "HttpStatusCode": 200,
  "Message": "Success",
  "RequestId": "DA021073-17CE-5CCF-9FEB-93226C766887",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
