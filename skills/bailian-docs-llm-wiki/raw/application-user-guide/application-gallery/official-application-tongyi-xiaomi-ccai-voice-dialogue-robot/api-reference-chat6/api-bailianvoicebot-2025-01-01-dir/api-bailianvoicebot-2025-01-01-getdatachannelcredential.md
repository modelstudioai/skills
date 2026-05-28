# GetDataChannelCredential - 获取数据通道凭证

获取数据通道凭证。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/GetDataChannelCredential)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/GetDataChannelCredential)

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

bailianvoicebot:GetDataChannelCredential

get

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

DeviceId

string

是

设备 ID

device-3i5x4234f2j4w55e

## 返回参数

名称

类型

描述

示例值

object

GenericResponse

Data

object

返回数据

DeviceId

string

设备 ID

device-3i5x4234f2j4w55e

Topic

string

Topic

datachannel-prepub-a/dc52807f0eff4b9b8224d06c7f240c07

ClientId

string

客户端 ID

26c2f022-b6c0-4ab0-9019-6e1a42dc5582

Endpoint

string

节点

mqtt-cn-ux146hgtt04.mqtt.aliyuncs.com

UserName

string

用户名称

Token|LTAI5tRYzHUYYi4XstgMCsL4|mqtt-cn-ux146hgtt04

Password

string

密码

\*\*\*

ExpirationTime

long

链接有效期。

**说明** 返回值为时间戳形式。

1745004535507

RequestId

string

请求 ID

D771A1B6-3D5F-174A-BEE1-98CE1000D337

HttpStatusCode

integer

http 状态码

200

Code

string

接口状态或 POP 错误码。

OK

Message

string

响应信息

success

Params

array

响应参数。

Param

string

错误参数。

\['02022042312', 'jrtj'\]

## 示例

正常返回示例

`JSON`格式

```
{
  "Data": {
    "DeviceId": "device-3i5x4234f2j4w55e",
    "Topic": "datachannel-prepub-a/dc52807f0eff4b9b8224d06c7f240c07",
    "ClientId": "26c2f022-b6c0-4ab0-9019-6e1a42dc5582",
    "Endpoint": "mqtt-cn-ux146hgtt04.mqtt.aliyuncs.com",
    "UserName": "Token|LTAI5tRYzHUYYi4XstgMCsL4|mqtt-cn-ux146hgtt04",
    "Password": "***",
    "ExpirationTime": 1745004535507
  },
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "HttpStatusCode": 200,
  "Code": "OK",
  "Message": "success",
  "Params": [
    "['02022042312', 'jrtj']"
  ]
}
```

## 错误码

HTTP status code

错误码

错误信息

400

Parameter.Blank

The parameter %s must not be null or empty.

400

Parameter.Empty

The parameter %s may not be null or empty.

400

Parameter.Null

The parameter %s may not be null.

403

Permission.Instance

You have no permission to access instance %s.

404

NotExists.InstanceId

The specified instance %s does not exist.

500

InternalService.Common

An internal service error occurred. %s

访问[错误中心](< https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-02-02

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GetDataChannelCredential?updateTime=2026-02-02#workbench-doc-change-demo)
