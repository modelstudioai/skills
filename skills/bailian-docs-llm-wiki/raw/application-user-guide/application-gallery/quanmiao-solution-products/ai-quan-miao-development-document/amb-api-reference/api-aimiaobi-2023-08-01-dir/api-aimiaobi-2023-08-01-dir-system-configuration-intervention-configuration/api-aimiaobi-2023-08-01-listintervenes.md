# ListIntervenes - 列出干预项

获得干预项列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListIntervenes)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListIntervenes)

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

aimiaobi:ListIntervenes

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

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

33a2658aaabf4c24b45d50e575125311\_p\_beebot\_public

RuleId

long

否

规则 id

mqtt\_outRule\_1679019634514

Query

string

否

问题

小猫

InterveneType

integer

否

干预类型

枚举值：

-   0-相似问干预项目：0-相似问干预项目。
-   2-正则表达式干预项 ：2-正则表达式干预项 。
-   1-关键词表达式干预项 ： 1-关键词表达式干预项 。
-   3-关键词库干预项：3-关键词库干预项。
-   4-URL干预： 4-URL干预。

干预类型

PageIndex

integer

否

页号

1

PageSize

integer

否

页面尺寸

10

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

0

Data

object

业务数据

InterveneList

array<object>

干预项列表

InterveneList

object

Id

string

id

36559

Query

string

干预 query

伊家楼

PageIndex

integer

页号

1

PageSize

integer

页尺寸

10

TotalSize

long

总页书

1

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

RequestId

string

请求唯一标识

428DCC0D-3C63-5306-BD1B-124396AB97BE

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": 0,
  "Data": {
    "InterveneList": [
      {
        "Id": 36559,
        "Query": "伊家楼"
      }
    ],
    "PageIndex": 1,
    "PageSize": 10,
    "TotalSize": 1,
    "Code": 0
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "428DCC0D-3C63-5306-BD1B-124396AB97BE",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
