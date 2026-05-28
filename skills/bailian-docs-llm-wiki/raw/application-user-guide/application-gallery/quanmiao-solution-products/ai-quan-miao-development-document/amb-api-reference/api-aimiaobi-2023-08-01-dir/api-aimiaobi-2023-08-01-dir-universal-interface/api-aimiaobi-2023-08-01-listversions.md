# ListVersions - 获取版本信息

获取用户购买的版本信息。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListVersions)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListVersions)

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

aimiaobi:ListVersions

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

DataNotExists

Data

array<object>

业务数据

Data

object

列表对象

ConcurrentCount

integer

并发数

43

EndTime

string

服务到期时间

2023-04-23 02:00:34

InstanceCount

integer

实例数

55

InstanceId

string

实例 ID

ga-bp12pismsw4v3tzhf62p1

OrderId

long

订单 ID

7

ProductType

string

版本类型 (TRIAL: 试用版, STANDARD: 专业版, CUSTOMIZE: 定制版)

CUSTOMIZE

Quota

integer

试用版限额次数

13

StartTime

string

服务开始时间

2023-05-27 04:11:00

UseQuota

integer

试用版已使用次数

65

VersionDetail

string

版本明细

标准版-公共并发：1并发

VersionName

string

版本

试用版

VersionStatus

integer

有效状态：0-表示有效、1-版本过期-续费页、2-版本不可用-购买页

87

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

数据不存在

RequestId

string

请求唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "DataNotExists",
  "Data": [
    {
      "ConcurrentCount": 43,
      "EndTime": "2023-04-23 02:00:34",
      "InstanceCount": 55,
      "InstanceId": "ga-bp12pismsw4v3tzhf62p1",
      "OrderId": 7,
      "ProductType": "CUSTOMIZE",
      "Quota": 13,
      "StartTime": "2023-05-27 04:11:00",
      "UseQuota": 65,
      "VersionDetail": "标准版-公共并发：1并发",
      "VersionName": "试用版",
      "VersionStatus": 87
    }
  ],
  "HttpStatusCode": 200,
  "Message": "数据不存在",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
