# BridgeWebCall - 软电话测试通话

创建软电话测试通话。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/BridgeWebCall)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/BridgeWebCall)

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

bailianvoicebot:BridgeWebCall

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

BusinessUnitId

string

是

百炼业务空间 ID

llm-c11iig67g863rih8

ApplicationId

string

是

百炼应用 ID

a395011f-a247-400f-bc69-28796749fd52

Caller

string

否

呼入主叫号码(用于展示)。

13052253537

DeviceId

string

是

设备 ID

467539456766097392-cn-shenzhen

TimeoutSeconds

integer

否

超时时间，呼叫在经过该参数指定的时间仍然未接通的情况下，则主动挂断，单位秒

3

Tags

string

否

随路数据

{'ENV': 'production'}

SampleRate

integer

否

采样率

8000

Sandbox

boolean

否

是否测试环境

true

AudioCodec

string

否

编码类型，不传默认 PCM 编码。

-   PCM
-   OPUS

PCM

## 返回参数

名称

类型

描述

示例值

object

返回结果

RequestId

string

请求 ID

CF6D3484-19A1-5C77-863B-AC8B5754D37C

Success

boolean

是否成功

True

HttpStatusCode

string

http 状态码

200

Code

string

状态码，200 表示正常

OK

ErrorMsg

string

错误信息

connect timed out

Data

object

返回数据

InstanceId

string

实例 ID。

i-uf6abxo1tuuwarrtffpp

SessionId

string

会话 ID

ws-4b7c263f-9b4c-4b28-baae-a65e9155e380

ChannelId

string

通道 ID。

894526715106764802

ExpirationTime

string

Token 有效期。

**说明** 返回值为时间戳形式。

1744964682422

ServerUrl

string

服务地址

wss://sh-voicebot.aliyuncs.com:443/audio

Token

string

认证签名。

83480f806b48f022313de37b691e167e

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "CF6D3484-19A1-5C77-863B-AC8B5754D37C",
  "Success": true,
  "HttpStatusCode": 200,
  "Code": "OK",
  "ErrorMsg": "connect timed out",
  "Data": {
    "InstanceId": "i-uf6abxo1tuuwarrtffpp",
    "SessionId": "ws-4b7c263f-9b4c-4b28-baae-a65e9155e380",
    "ChannelId": 894526715106764800,
    "ExpirationTime": 1744964682422,
    "ServerUrl": "wss://sh-voicebot.aliyuncs.com:443/audio",
    "Token": "83480f806b48f022313de37b691e167e"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-04-07

OpenAPI 入参发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/BridgeWebCall?updateTime=2026-04-07#workbench-doc-change-demo)
